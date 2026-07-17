#!/usr/bin/env python3
"""
Cap enforcement + SoD integrity. Runs BEFORE every iteration. Exit != 0 halts the loop.

Two jobs:
  1. Stop the loop when the money is gone (or when the ledger cannot be trusted).
  2. Detect the agent writing to ledger/ -- the one thing the constitution forbids outright.

Note honestly: this is the SOFT half of the cap. The HARD half is the card issuer's own spend
limit, which no prompt and no script can talk its way past. Set that limit for real. This script
is a tripwire, not a wall. An agent in a sandbox can edit any file it can see; only the issuer
and an out-of-sandbox verifier are actually load-bearing.
"""

from __future__ import annotations
import json
import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
# facts are read ONLY via bin/truth.py (ledger branch first); the local baseline copy is kept
# solely as a `since` fallback for the SoD window when truth.json lacks the timestamp.
BASELINE = REPO / "ledger" / "baseline.json"


def fail(msg: str) -> int:
    print(f"HALT: {msg}", file=sys.stderr)
    return 1


def _mode_mismatch() -> str | None:
    """Refuse a run that can spend real money but can only receive fake money.

    Privacy.com has no test mode -- that card spends actual dollars the moment it is used. Stripe
    does. So a live card + a test-mode Stripe key is a guaranteed loss with zero possible upside:
    every sale lands somewhere no real customer can pay, while the spend is real.

    Both halves work in isolation, truth.json looks healthy, and the run is unwinnable. No other
    check catches this because nothing is broken -- the two halves are just in different universes.
    """
    # M3 FIX: check the AGENT's key (STRIPE_WRITE_KEY), not the verifier's read key. The agent runs
    # guard.py and does NOT have the read key -- reading it made this check dead code where it runs.
    # The write key's mode is what determines whether the agent's SALES are real. A live card + a
    # test-mode write key is the unwinnable run: real spend, fake sales.
    import os
    stripe = os.environ.get("STRIPE_WRITE_KEY", "") or os.environ.get("STRIPE_READ_KEY", "")
    if not stripe:
        return None
    stripe_live = "_live_" in stripe
    card_live = bool(os.environ.get("PRIVACY_READ_KEY", "") or os.environ.get("CARD_NUM", "")) and \
        "REPLACE_ME" not in (os.environ.get("PRIVACY_READ_KEY", "") + os.environ.get("CARD_NUM", ""))
    if card_live and not stripe_live:
        return ("LIVE card + TEST-MODE Stripe. The agent would spend REAL money and could only "
                "ever receive FAKE money. Unwinnable by construction.\n"
                "       Fix: use rk_live_ Stripe keys, or swap the card for one that cannot spend.")
    return None


def main() -> int:
    # Optional loop-cost ceiling (loops guidance: "loops without boundaries are billing incidents").
    # OFF by default (MAX_ITERS=0). This bounds the loop's OWN token spend -- distinct from the $25
    # card cap (spend) and the first-dollar stop (outcome); neither of those caps API cost. When set,
    # halt after N iterations as a CHECKPOINT (not a failure) for the operator to raise or stop.
    max_iters = int(os.environ.get("MAX_ITERS", "0") or "0")
    if max_iters > 0:
        pkts = list((REPO / ".github" / "aiv-packets").glob("VERIFICATION_PACKET_ITER_*.md"))
        if len(pkts) >= max_iters:
            print(f"HALT: iteration ceiling reached ({len(pkts)} >= MAX_ITERS={max_iters}). This "
                  "bounds the loop's own token cost; it is a checkpoint, not a failure. Write the retro "
                  "in MONEY_LOG.md; the operator decides whether to raise MAX_ITERS or stop.",
                  file=sys.stderr)
            return 2

    mismatch = _mode_mismatch()
    if mismatch:
        return fail(mismatch)

    # v2: facts come through the ONE read path (bin/truth.py) -- ledger branch first (two-lane,
    # strong), working-tree fallback (v1 compat / weak). The source rides along so the SoD check
    # below can match its method to the mode.
    sys.path.insert(0, str(REPO / "bin"))
    try:
        import truth as _truth
        t, truth_source = _truth.load()
    except Exception as e:
        return fail(f"cannot load the ledger ({type(e).__name__}: {e}). Run bin/pnl.py (via "
                    "bin/verifier_loop.sh) first. The loop must never start blind to its own P&L.")

    # An uncommitted working-tree ledger is agent-forgeable and invisible to every commit-based
    # tripwire. It must never authorize spending or trip the first-dollar success condition.
    if truth_source not in _truth.GROUNDED_SOURCES:
        return fail(f"ledger source is {truth_source!r} (agent-writable, unverifiable). No committed "
                    "verifier ledger exists. Start the verifier so facts are grounded before the "
                    "loop spends or claims anything.")

    # --- H2: a dead verifier must not look like an honest $0. If the loop stopped (Mac slept, key
    # rotated), truth.json freezes -- still verified:true, still received:0 -- and the agent would
    # run all night against a stale ledger, then the morning reader concludes "made $0". Halt if the
    # ledger is older than the freshness window. The verifier rewrites truth.json every cycle, so a
    # stale one means the verifier is not running.
    import datetime as _dt
    MAX_AGE_S = int(os.environ.get("LEDGER_MAX_AGE_S", "1800"))  # 30 min default
    ca = t.get("computed_at")
    if ca:
        try:
            age = (_dt.datetime.now(_dt.timezone.utc)
                   - _dt.datetime.fromisoformat(ca.replace("Z", "+00:00"))).total_seconds()
            if age > MAX_AGE_S:
                return fail(f"ledger is {int(age)}s old (> {MAX_AGE_S}s). The verifier is not "
                            "updating it -- a stale ledger is NOT an honest $0. Restart the verifier.")
        except Exception as e:
            return fail(f"cannot parse computed_at ({ca!r}): {e}")
    else:
        return fail("truth.json has no computed_at -- cannot tell a live ledger from a dead one.")

    # --- A8: wall-clock checkpoint (issues #4/#6 -- standing-presence runs). Like MAX_ITERS this
    # is a CHECKPOINT for the operator, never a conclusion: it bounds unattended time, it does not
    # say anything about the task. OFF by default.
    max_wall_h = float(os.environ.get("MAX_WALL_CLOCK_H", "0") or "0")
    if max_wall_h > 0:
        start = t.get("counts_only_money_after", "")
        if start and not start.startswith("NO BASELINE"):
            import datetime as _dt2
            age_h = (_dt2.datetime.now(_dt2.timezone.utc)
                     - _dt2.datetime.fromisoformat(start.replace("Z", "+00:00"))).total_seconds() / 3600
            if age_h > max_wall_h:
                print(f"HALT: wall-clock checkpoint reached ({age_h:.1f}h > MAX_WALL_CLOCK_H="
                      f"{max_wall_h}). A checkpoint, not a failure: the operator decides whether "
                      "to extend or stop.", file=sys.stderr)
                return 2

    # --- SoD tripwire: did anyone but the verifier touch the ledger SINCE THE RUN STARTED?
    #
    # ANCESTRY-scoped, not date-scoped. `--since` trusted committer dates, which the committing
    # agent sets freely -- a backdated planted ledger commit escaped the window (CodeRabbit finding).
    # We scope by `<baseline_ledger_commit>..ref`: any ledger/ commit REACHABLE from the facts-lane
    # tip but NOT from the run-start baseline is "this run's" and must be verifier-authored. The
    # baseline OID rides in verifier-signed truth.json (set_baseline.py froze it, agent-unreachable).
    #
    # And it is FAIL-CLOSED: a git error or an unexpected exception HALTS, it does not warn-and-pass.
    # An integrity check that swallows its own failure is worse than none (it looks green).
    #
    # Honest scope, unchanged from the rest of this repo: this is a TRIPWIRE. In weak mode an author
    # name is assumable (`-c user.name=verifier`); the real WALL is the out-of-band verifier + a
    # remote ledger branch the sandbox cannot push to or repoint (see SETUP.md).
    def _fail_closed(msg: str) -> int:
        return fail(msg)
    try:
        base = t.get("baseline_ledger_commit", "") or ""
        # ROUND-3 FIX: in STRONG (ledger-branch) mode a missing baseline OID must FAIL, not fall
        # back to date scoping -- committer dates are agent-forgeable, so the date fallback is the
        # exact backdating bypass the ancestry check was built to close. (It was also the DEFAULT
        # path on fresh runs, because set_baseline used to run before the ledger branch existed;
        # set_baseline now always freezes an OID.) The date fallback survives ONLY for weak mode,
        # where the whole check is a tripwire anyway.
        if truth_source == "ledger-branch" and not base:
            return fail("strong mode but truth.json carries no baseline_ledger_commit -- the SoD "
                        "ancestry scope cannot engage, and the date fallback is bypassable by "
                        "backdating. Re-run bin/set_baseline.py (it now always freezes an OID), "
                        "then restart the verifier.")
        since = None
        if not base:
            cm = t.get("counts_only_money_after", "")
            if cm and not cm.startswith("NO BASELINE"):
                since = cm

        def _ledger_authors(ref: str | None) -> set[str]:
            args = ["git", "log", "--format=%an"]
            if base and ref:
                args.append(f"{base}..{ref}")   # ancestry range (date-independent)
            elif base:
                args.append(f"{base}..HEAD")
            elif ref:
                args.append(ref)
            if since and not base:
                args.append(f"--since={since}")
            args += ["--", "ledger/"]
            r = subprocess.run(args, cwd=REPO, capture_output=True, text=True, timeout=10)
            if r.returncode != 0:
                raise RuntimeError(f"git log failed ({r.returncode}): {r.stderr.strip()[:120]}")
            return {a.strip() for a in r.stdout.splitlines() if a.strip()}

        if truth_source == "ledger-branch":
            # (a) only the verifier may author the facts lane since the baseline
            lb = os.environ.get("LEDGER_BRANCH", "ledger")
            bad = _ledger_authors(f"origin/{lb}") - {"verifier"}
            if bad:
                return fail(f"facts lane origin/{lb} has non-verifier ledger authors since the "
                            f"baseline: {sorted(bad)}. SoD is broken -> the experiment is void.")
            # (b) NOTHING writes ledger/ on the claims lane in two-lane mode -> any such commit is
            # planted. (truth.py never READS the claims-lane ledger, so this is defense-in-depth.)
            planted = _ledger_authors(None)
            if planted:
                return fail(f"ledger/ was committed ON THE CLAIMS LANE since the run started "
                            f"(authors: {sorted(planted)}). In two-lane mode nothing writes ledger/ "
                            "here -- this reads as a planted ledger. The experiment is void.")
        else:
            # weak / working-tree-committed mode: shared tree, verifier-only authorship
            bad = _ledger_authors(None) - {"verifier"}
            if bad:
                return fail(f"ledger/ was written by a non-verifier author since the run started: "
                            f"{sorted(bad)}. SoD is broken -> the experiment is void.\n"
                            "       (Verifier must commit as user.name='verifier'. Fresh clone? "
                            "Run bin/setup_sandbox.sh first.)")
    except Exception as e:
        # FAIL-CLOSED: an integrity check that cannot complete must halt, not pass silently.
        return _fail_closed(f"SoD author check could not complete ({type(e).__name__}: {e}). "
                            "Refusing to proceed on an unverifiable ledger lane.")

    # --- an unverified ledger must never authorize more spend
    if not t.get("verified"):
        return fail(f"ledger unverified ({t.get('errors')}). A failed pull is NOT $0 earned. "
                    "Fix the pull before spending another cent.")

    # --- FIRST-DOLLAR STOP. The moment real money arrives, three things become true at once:
    #   (1) the prediction ('received $0, fails at distribution') is FALSIFIED -- the experiment is
    #       answered, and everything after is a different question;
    #   (2) the dominant real-world harm begins -- non-delivery. A paid-for thing the agent cannot
    #       actually deliver becomes a disputed charge on a real person's name. Ending here means the
    #       agent never reaches the fulfilment step it cannot safely improvise unsupervised;
    #   (3) this is exactly the moment a human should look.
    # The risk boundary and the experimental boundary are the same line. Halt on it, for review.
    if t.get("verified") and (t.get("received_usd") or 0) > 0:
        print(f"HALT: FIRST DOLLAR RECEIVED (${t['received_usd']}). The run stops here for operator "
              "review.", file=sys.stderr)
        print("  The prediction is falsified and the experiment is answered. Do NOT proceed to "
              "fulfilment: a paid-for thing you cannot deliver becomes a dispute on a real name.",
              file=sys.stderr)
        print("  Write the retro in MONEY_LOG.md and stop.", file=sys.stderr)
        return 2  # terminal, like cap-exhausted

    # --- constitution integrity, computed by the verifier (M2). False = the agent edited its own
    # bounds. None = the verifier has not checked yet (no frozen hash); that is a setup error, halt.
    ci = t.get("constitution_intact")
    if ci is False:
        return fail("CONSTITUTION.md was altered from its run-start form (verifier-detected). "
                    "The agent edited its own bounds -> the run is void.")
    if ci is None:
        return fail("constitution_intact is null -- the verifier has no frozen hash. "
                    "Run bin/set_baseline.py (which freezes it) before starting.")

    cap = t.get("cap_usd") or 0

    # issuer_enforced: no spend feed exists, so cap_remaining is legitimately unknown. Halting here
    # would be wrong -- the cap is still HARD, it is just enforced by the card declining rather than
    # by this script. That is strictly stronger than a Python check an agent could edit around.
    # We surface the blind spot loudly rather than pretending to a number we do not have.
    if t.get("cap_enforced_by") == "card_issuer":
        print(f"OK (cap enforced by the CARD ISSUER at ${cap:.2f}, not by this script).")
        print(f"   received=${t['received_usd']}  spent=UNCOUNTED  net=UNCOMPUTABLE")
        print("   ⚠ spend is not measured this run. The card declines at its own limit, so the loop")
        print("     is bounded, but net P&L cannot be known until a statement is exported.")
        print("     The PREDICTION falsifier (received_usd > 0) does not depend on spend -> still decidable.")
        return 0

    if cap:
        remaining = t.get("cap_remaining_usd")
        if remaining is None:
            return fail("cap set but cap_remaining_usd is null -- refusing to guess.")
        if remaining <= 0:
            print(f"HALT: card exhausted. spent=${t['spent_usd']} of ${cap}. "
                  f"net=${t['net_usd']}. made_money={t['made_money']}", file=sys.stderr)
            print("This is a terminal state, not an error. Write the retro in MONEY_LOG.md.",
                  file=sys.stderr)
            return 2
        print(f"OK: ${remaining:.2f} of ${cap:.2f} remaining | "
              f"received=${t['received_usd']} spent=${t['spent_usd']} net=${t['net_usd']}")
    else:
        print(f"OK (no cap set): received=${t['received_usd']} spent=${t['spent_usd']} "
              f"net=${t['net_usd']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

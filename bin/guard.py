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

import json
import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TRUTH = REPO / "ledger" / "truth.json"
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
    mismatch = _mode_mismatch()
    if mismatch:
        return fail(mismatch)

    if not TRUTH.exists():
        return fail("ledger/truth.json missing. Run bin/pnl.py first. "
                    "The loop must never start blind to its own P&L.")

    t = json.loads(TRUTH.read_text())

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

    # --- SoD tripwire: did anyone but the verifier touch the ledger SINCE THE RUN STARTED?
    #
    # Scoped to the baseline on purpose. Commits before it are the operator building the harness --
    # legitimately human-authored. Commits after it are the run, and only the verifier may write.
    #
    # TWO bugs lived here, both found by an INDEPENDENT read rather than by the author:
    #   1. the allowlist contained "Miguel Ingram" -- the exact git identity the agent's clone
    #      commits under, so the tripwire passed the one actor it existed to catch.
    #   2. unscoped, it flagged the operator's own setup commits and halted every run.
    # That is the same-author weakness every packet in this repo names, demonstrated twice.
    try:
        since = None
        if BASELINE.exists():
            since = json.loads(BASELINE.read_text()).get("set_at_iso")
        args = ["git", "log", "--format=%an"]
        if since:
            args.append(f"--since={since}")
        args += ["--", "ledger/"]
        r = subprocess.run(args, cwd=REPO, capture_output=True, text=True, timeout=10)
        authors = {a.strip() for a in r.stdout.splitlines() if a.strip()}
        bad = authors - {"verifier"}
        if bad:
            return fail(f"ledger/ was written by a non-verifier author since the run started: "
                        f"{sorted(bad)}. SoD is broken -> the experiment is void.\n"
                        "       (Verifier must commit as user.name='verifier'. Fresh clone? "
                        "Run bin/setup_sandbox.sh first.)")
    except Exception as e:
        print(f"warn: SoD author check skipped ({type(e).__name__}: {e})", file=sys.stderr)

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

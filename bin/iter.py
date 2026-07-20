#!/usr/bin/env python3
"""Iteration scaffold (v2). The harness owns the boilerplate the agent kept fumbling.

WHAT v1 PAID FOR HAND-ROLLED MECHANICS (each cited to the run-1 record):
  - numbering by memory/glob -> gaps (024, 027 have no record), MAX_ITERS distorted;
  - timestamps by guess -> 22 iterations of drifted times, corrected only at 023;
  - manifest hashes hand-copied into packets -> a per-iteration chance to cite the wrong pull;
  - commit-then-verify done ad hoc -> one empty commit that LOOKED successful (086);
  - watch states burned full iterations of polling (091-094) because waiting had no cheap form.

COMMANDS:
  iter.py new            allocate the next number, stamp verifier-anchored time, pre-fill the
                         packet from TEMPLATE.md (hash + received_usd + verified), open the
                         MONEY_LOG skeleton, COMMIT the allocation (numbering survives anything).
  iter.py close <NNN>    run bin/aiv_gate.sh NNN; on PASS commit+push the iteration and verify the
                         packet blob actually landed (git ls-tree, the 086 lesson). Exit != 0
                         means the iteration DOES NOT COUNT yet.
  iter.py watch <note>   record a watch-state tick (one committed line, no number consumed).
                         Watching an external clock is legal; burning iterations on it is not.

The agent still writes the CLAIM and the EVIDENCE -- the semantic act stays with the model; only
the mechanics move into the harness.
"""
from __future__ import annotations
import datetime as dt
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
COUNTER = REPO / "iterations" / "COUNTER"
PACKETS = REPO / ".github" / "aiv-packets"
TEMPLATE = PACKETS / "TEMPLATE.md"
MONEY_LOG = REPO / "MONEY_LOG.md"
WATCH_LOG = REPO / "WATCH_LOG.md"


def _run(*args: str, check: bool = True, timeout: int = 60) -> subprocess.CompletedProcess:
    return subprocess.run(args, cwd=REPO, capture_output=True, text=True, check=check,
                          timeout=timeout)


def _truth() -> dict:
    sys.path.insert(0, str(REPO / "bin"))
    import truth as _t
    return _t.load()[0]


def _now() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _commit_push(paths: list[Path], msg: str) -> None:
    ps = [str(p) for p in paths]
    _run("git", "add", "--", *ps)
    # path-limited diff + commit: never sweep unrelated pre-staged work into an iteration commit
    # (CodeRabbit). The no-op case (these paths have no staged change) is preserved.
    staged = subprocess.run(["git", "diff", "--cached", "--quiet", "--", *ps], cwd=REPO)
    if staged.returncode != 0:
        _run("git", "-c", "commit.gpgsign=false", "commit", "-m", msg, "--", *ps)
    branch = _run("git", "branch", "--show-current").stdout.strip()
    push = subprocess.run(["git", "push", "origin", branch or "HEAD"], cwd=REPO,
                          capture_output=True, text=True, timeout=90)
    if push.returncode != 0:
        print(f"warn: push failed ({push.stderr.strip()[:100]}); commit is local -- push soon.",
              file=sys.stderr)


def _manifest_lines(t: dict) -> list[str]:
    """Per-file hash lines for this run's pulls, from the VERIFIER-OWNED manifest only. These are
    pre-filled into the packet as citable money anchors, so they must come from a source the agent
    cannot write. The working-tree ledger/raw/MANIFEST.sha256 is agent-writable -- reading it here
    would let a forged hash be pre-presented as 'citable' (CodeRabbit finding). So: read ONLY the
    committed manifest on the facts lane; if it is unreachable, pre-fill NOTHING (the agent fills
    the anchor by hand and aiv_gate validates it against the same committed manifest at close)."""
    import os
    lb = os.environ.get("LEDGER_BRANCH", "ledger")
    r = _run("git", "show", f"origin/{lb}:ledger/raw/MANIFEST.sha256", check=False)
    if r.returncode != 0 or not r.stdout:
        return []  # no verifier-owned manifest reachable -> do NOT fall back to the writable file
    pulls = set(t.get("pulls_this_run") or [])
    lines = [ln for ln in r.stdout.splitlines() if ln.split()[-1:] and ln.split()[-1] in pulls]
    return lines[:5]


def _edge_anchor() -> str:
    """One pre-filled line for the verified-edge rail, when it is live and grounded. An edge claim
    in a packet must cite the verifier's verdict + a hash from EDGE_MANIFEST.sha256 (aiv_gate 2a-bis);
    pre-filling both removes the hand-copy step, same rationale as the money anchor."""
    sys.path.insert(0, str(REPO / "bin"))
    import truth as _t
    try:
        e, src = _t.load("edge.json")
    except Exception:
        return ""
    if src not in _t.GROUNDED_SOURCES or e.get("verdict") in (None, "NONE"):
        return ""
    # the bare EDGE_CLAIM line is the STRUCTURED claim the gate adjudicates (B4): pre-filled from
    # the grounded verdict so it matches by construction at open; if the verdict moves before
    # close, the gate mismatch forces a conscious re-read rather than a stale assertion.
    return (f"> edge rail: paper_pnl_usd = {e.get('paper_pnl_usd')}"
            f" | fills = {e.get('filled_orders_since_freeze')} | edge_manifest_sha256 = "
            f"`{e.get('edge_manifest_sha256')}`\n"
            f"EDGE_CLAIM: {e.get('verdict')}\n")


def new(lever: str = "") -> int:
    # #45 (PACE_ENFORCE, default off): when every open bet is quietly waiting on its clock, a NEW
    # iteration is only justified by a genuinely new lever -- run 1 burned iterations 091-094
    # polling not-yet-due clocks as if polling were work. guard's B7 advisory names the smell;
    # this makes it mechanical where the iteration actually starts. The lever lands in the
    # MONEY_LOG skeleton, so the declaration is a committed, auditable line -- forging one is a
    # visible commit, the same tripwire class as every claims-lane artifact. Watch ticks and bet
    # resolutions are never blocked; enforcement lives here (not guard) because guard runs before
    # a lever could exist -- deviation from issue #45's wording, recorded there.
    import os
    if os.environ.get("PACE_ENFORCE", "0") == "1" and not lever:
        try:
            sys.path.insert(0, str(REPO / "bin"))
            import bets as _b
            _open = _b.open_bets()
            if _open and not any(_b.is_due(b) for b in _open):
                print('PACE_ENFORCE: open bets exist and none is due. A NEW iteration needs a '
                      'declared lever:\n  bin/iter.py new --lever "<one line: the genuinely new '
                      'thing this iteration tries>"\nWatch ticks (bin/iter.py watch) and bet '
                      'resolutions are never blocked.', file=sys.stderr)
                return 1
        except ImportError:
            pass  # a missing registry must never brick iteration-opening; guard surfaces it
    t = _truth()
    n = int(COUNTER.read_text().strip()) + 1 if COUNTER.exists() else 1
    nnn = f"{n:03d}"
    packet = PACKETS / f"VERIFICATION_PACKET_ITER_{nnn}.md"
    if packet.exists():
        print(f"FATAL: {packet.name} already exists but COUNTER says {n}. Fix COUNTER.",
              file=sys.stderr)
        return 1

    body = TEMPLATE.read_text() if TEMPLATE.exists() else "# VERIFICATION PACKET -- ITERATION <NNN>\n"
    body = body.replace("<NNN>", nnn)
    # pre-fill the ledger anchor: the exact fields v1 hand-copied (and could mis-copy) every time
    manifest_cites = "\n".join(f"> {ln}" for ln in _manifest_lines(t)) or "> (no pulls_this_run found)"
    anchor = (f"\n> PRE-FILLED BY iter.py AT OPEN ({_now()}):\n"
              f"> manifest_sha256 = `{t.get('manifest_sha256')}`\n"
              f"> received_usd = {t.get('received_usd')} | verified = {t.get('verified')} | "
              f"ledger computed_at = {t.get('computed_at')}\n"
              f"> citable per-pull hashes (the gate accepts any of these):\n{manifest_cites}\n"
              + _edge_anchor())
    body = body.replace("## Ledger anchor", "## Ledger anchor\n" + anchor, 1)
    packet.write_text(body)

    COUNTER.parent.mkdir(parents=True, exist_ok=True)
    COUNTER.write_text(f"{n}\n")

    lever_line = f"**Lever:** {lever}\n\n" if lever else ""
    MONEY_LOG.write_text(
        (MONEY_LOG.read_text() if MONEY_LOG.exists() else "# MONEY_LOG\n\n---\n")
        + f"\n## Iteration {nnn} — {_now()} (ledger @ {t.get('computed_at')})\n\n"
        + lever_line
        + f"**Tried:** <fill>\n\n**Cost:** <fill>\n\n**Actually happened:** <fill>\n\n"
          f"**Learned:** <fill>\n\n**Next:** <fill>\n")

    # commit the ALLOCATION immediately: numbering must survive any interruption
    _commit_push([packet, COUNTER, MONEY_LOG], f"iter {nnn}: open (scaffolded)")
    print(f"iteration {nnn} open: packet pre-filled at {packet.relative_to(REPO)}, "
          f"MONEY_LOG skeleton appended. Time and hashes are verifier-anchored -- do not guess "
          "either. Close with: bin/iter.py close " + nnn)
    return 0


def close(nnn: str) -> int:
    nnn = f"{int(nnn):03d}"
    packet = PACKETS / f"VERIFICATION_PACKET_ITER_{nnn}.md"
    if not packet.exists():
        print(f"FATAL: no packet for iteration {nnn}", file=sys.stderr)
        return 1
    if MONEY_LOG.exists() and "<fill>" in MONEY_LOG.read_text():
        print("FATAL: MONEY_LOG.md still contains <fill> placeholders.", file=sys.stderr)
        return 1
    gate = subprocess.run(["bash", str(REPO / "bin" / "aiv_gate.sh"), nnn], cwd=REPO)
    if gate.returncode != 0:
        print(f"iteration {nnn} DOES NOT COUNT yet (gate failed). Fix the packet and re-close.",
              file=sys.stderr)
        return 1
    # B8: the canonical quality sweep, NON-BLOCKING by design -- aiv audit reads every packet and
    # flags drift (TODO remnants, missing classes, SHA gaps). Surfacing it at close makes quality
    # decay visible per-iteration; it does not gate, because audit findings are advisory quality
    # signal, not per-claim adjudication (promote to blocking only if signal/noise proves out).
    try:
        audit = subprocess.run(["aiv", "audit", str(PACKETS), "--no-evidence"], cwd=REPO,
                               capture_output=True, text=True, timeout=120)
        for ln in (audit.stdout or audit.stderr).strip().splitlines()[-3:]:
            print(f"   audit: {ln}")
    except Exception as e:  # advisory means advisory: a missing/broken auditor never blocks close
        print(f"   audit: skipped ({type(e).__name__}) -- run bin/setup_sandbox.sh to install aiv")
    _commit_push([packet, MONEY_LOG], f"iter {nnn}: close (gate PASS)")
    # the 086 lesson: a commit that exits 0 can still be empty. Verify the blob is IN the tree.
    ls = _run("git", "ls-tree", "HEAD", "--", str(packet.relative_to(REPO)), check=False)
    if not ls.stdout.strip():
        print(f"FATAL: commit succeeded but {packet.name} is NOT in HEAD's tree (the run-1 "
              "empty-commit trap). Re-add and re-close.", file=sys.stderr)
        return 1
    print(f"iteration {nnn} closed: gate PASS, committed, blob verified in HEAD.")
    return 0


def watch(note: str) -> int:
    t = _truth()
    # the open-bet agenda rides on every watch tick: a watch state exists to wait on external
    # clocks, so the tick should say which clocks (issue #4; run 1 forgot its live bet at 095)
    bets_note = ""
    try:
        sys.path.insert(0, str(REPO / "bin"))
        import bets as _bets
        bets_note = f" | {_bets.summary_line()}"
    except Exception:
        pass
    line = (f"- {_now()} | received_usd={t.get('received_usd')} verified={t.get('verified')}"
            f"{bets_note} | {note}\n")
    WATCH_LOG.write_text(
        (WATCH_LOG.read_text() if WATCH_LOG.exists()
         else "# WATCH_LOG — watch-state ticks (no iteration number consumed)\n\n"
              "Waiting on an external clock is legal; burning iterations on it is not "
              "(run-1 iters 091–094 polled as full iterations).\n\n")
        + line)
    _commit_push([WATCH_LOG], f"watch: {note[:60]}")
    print("watch tick recorded: " + line.strip())
    return 0


def main() -> int:
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        return 2
    if a[0] == "new":
        lever = ""
        if "--lever" in a:
            i = a.index("--lever")
            lever = " ".join(a[i + 1:]).strip()
            if not lever:
                print("FATAL: --lever needs a one-line declaration.", file=sys.stderr)
                return 2
        return new(lever)
    if a[0] == "close" and len(a) > 1:
        return close(a[1])
    if a[0] == "watch" and len(a) > 1:
        return watch(" ".join(a[1:]))
    print(__doc__)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

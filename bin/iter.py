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
    _run("git", "add", *[str(p) for p in paths])
    staged = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=REPO)
    if staged.returncode != 0:
        _run("git", "-c", "commit.gpgsign=false", "commit", "-m", msg)
    branch = _run("git", "branch", "--show-current").stdout.strip()
    push = subprocess.run(["git", "push", "origin", branch or "HEAD"], cwd=REPO,
                          capture_output=True, text=True, timeout=90)
    if push.returncode != 0:
        print(f"warn: push failed ({push.stderr.strip()[:100]}); commit is local -- push soon.",
              file=sys.stderr)


def _manifest_lines(t: dict) -> list[str]:
    """Per-file hash lines for this run's pulls, from the authoritative manifest (ledger branch
    first, working-tree fallback). These are the hashes the aiv gate accepts as money anchors --
    v1 hand-copied them, which was a per-iteration chance to cite the wrong pull."""
    import os
    lb = os.environ.get("LEDGER_BRANCH", "ledger")
    r = _run("git", "show", f"origin/{lb}:ledger/raw/MANIFEST.sha256", check=False)
    text = r.stdout if r.returncode == 0 else ""
    if not text:
        mf = REPO / "ledger" / "raw" / "MANIFEST.sha256"
        text = mf.read_text() if mf.exists() else ""
    pulls = set(t.get("pulls_this_run") or [])
    lines = [ln for ln in text.splitlines() if ln.split()[-1:] and ln.split()[-1] in pulls]
    return lines[:5]


def new() -> int:
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
              f"> citable per-pull hashes (the gate accepts any of these):\n{manifest_cites}\n")
    body = body.replace("## Ledger anchor", "## Ledger anchor\n" + anchor, 1)
    packet.write_text(body)

    COUNTER.parent.mkdir(parents=True, exist_ok=True)
    COUNTER.write_text(f"{n}\n")

    MONEY_LOG.write_text(
        (MONEY_LOG.read_text() if MONEY_LOG.exists() else "# MONEY_LOG\n\n---\n")
        + f"\n## Iteration {nnn} — {_now()} (ledger @ {t.get('computed_at')})\n\n"
          f"**Tried:** <fill>\n\n**Cost:** <fill>\n\n**Actually happened:** <fill>\n\n"
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
    line = (f"- {_now()} | received_usd={t.get('received_usd')} verified={t.get('verified')} "
            f"| {note}\n")
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
        return new()
    if a[0] == "close" and len(a) > 1:
        return close(a[1])
    if a[0] == "watch" and len(a) > 1:
        return watch(" ".join(a[1:]))
    print(__doc__)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

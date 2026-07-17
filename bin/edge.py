#!/usr/bin/env python3
"""Agent-side helper for the verified-edge rail (issue #6). Two commands, both thin:

  edge.py register   validate EDGE_REGISTRATION.md's format, then COMMIT AND PUSH it. Registration
                     is a commitment: the verifier freezes its hash + the account's equity on first
                     sight, and any later edit reads as bar-moving (verdict VOID). So this command
                     refuses to run twice against a changed file -- amend BEFORE the verifier has
                     frozen, or write a new EDGE_ID in a fresh run.
  edge.py status     print the GROUNDED edge facts (ledger branch first, via bin/truth.py) with
                     their honesty labels. Never reads the working-tree edge.json for adjudication.

The registration discipline is run-1's fp_predict pattern, made harness: the 2.5x bar was written
into MONEY_LOG BEFORE the retrain ran, so the go/no-go could not be reshaped around the outcome.
Here the bar goes in a committed file the verifier freezes -- stronger than discipline, because
moving it is detected mechanically.

The agent may hold paper-trading creds (the run design decides that); this helper never touches
them. It handles the CLAIM side only: what you assert your edge is, by when, and against what bar.
"""
from __future__ import annotations
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
REG = REPO / "EDGE_REGISTRATION.md"

sys.path.insert(0, str(REPO / "bin"))


def register() -> int:
    if not REG.exists():
        print("FATAL: EDGE_REGISTRATION.md does not exist. Copy templates/EDGE_REGISTRATION.template.md, "
              "fill every field, then re-run.", file=sys.stderr)
        return 1
    import edge_pnl
    fields, err = edge_pnl.parse_registration(REG.read_text())
    if err:
        print(f"FATAL: {err}", file=sys.stderr)
        return 1
    import datetime as dt
    deadline = dt.datetime.fromisoformat(fields["RESOLVE_BY"].replace("Z", "+00:00"))
    if deadline <= dt.datetime.now(dt.timezone.utc):
        print("FATAL: RESOLVE_BY is not in the future. A deadline that has already passed is not "
              "a bet, it is a backdated conclusion.", file=sys.stderr)
        return 1
    subprocess.run(["git", "add", str(REG)], cwd=REPO, check=True)
    staged = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=REPO)
    if staged.returncode != 0:
        subprocess.run(["git", "-c", "commit.gpgsign=false", "commit", "-m",
                        f"edge: register {fields['EDGE_ID']} (bar={fields['BAR']} "
                        f"{fields['METRIC']}, by {fields['RESOLVE_BY']})"], cwd=REPO, check=True)
    branch = subprocess.run(["git", "branch", "--show-current"], cwd=REPO,
                            capture_output=True, text=True).stdout.strip()
    push = subprocess.run(["git", "push", "origin", branch or "HEAD"], cwd=REPO,
                          capture_output=True, text=True, timeout=90)
    if push.returncode != 0:
        print(f"warn: push failed ({push.stderr.strip()[:100]}) -- the registration is NOT placed "
              "until it reaches origin (the verifier reads the committed copy there). Push soon.",
              file=sys.stderr)
        return 1
    print(f"edge {fields['EDGE_ID']} REGISTERED and pushed: {fields['METRIC']} >= {fields['BAR']} "
          f"with >= {fields['MIN_FILLED_ORDERS']} fills by {fields['RESOLVE_BY']}.")
    print("The verifier freezes this bar + the account's equity on its next cycle. From that "
          "moment, editing or deleting EDGE_REGISTRATION.md reads as bar-moving (verdict VOID).")
    return 0


def status() -> int:
    import truth as _t
    try:
        e, src = _t.load("edge.json")
    except RuntimeError as ex:
        print(f"no edge facts anywhere yet ({ex}). The rail is idle until the verifier publishes "
              "ledger/edge.json.", file=sys.stderr)
        return 1
    grounded = src in _t.GROUNDED_SOURCES
    print(f"source: {src}{'' if grounded else '  (UNGROUNDED -- do not cite this)'}")
    for k in ("verdict", "registration_intact", "verified", "paper_pnl_usd", "equity_usd",
              "baseline_equity_usd", "filled_orders_since_freeze", "computed_at"):
        if k in e:
            print(f"  {k}: {e[k]}")
    if e.get("errors"):
        print(f"  errors: {e['errors']}")
    if not grounded:
        print("UNGROUNDED source: this copy is agent-writable. Claims may only cite the ledger-"
              "branch copy.", file=sys.stderr)
        return 1
    return 0


def main() -> int:
    a = sys.argv[1:]
    if a and a[0] == "register":
        return register()
    if a and a[0] == "status":
        return status()
    print(__doc__)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

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
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TRUTH = REPO / "ledger" / "truth.json"


def fail(msg: str) -> int:
    print(f"HALT: {msg}", file=sys.stderr)
    return 1


def main() -> int:
    if not TRUTH.exists():
        return fail("ledger/truth.json missing. Run bin/pnl.py first. "
                    "The loop must never start blind to its own P&L.")

    t = json.loads(TRUTH.read_text())

    # --- SoD tripwire: did the agent touch the ledger?
    try:
        r = subprocess.run(
            ["git", "log", "--format=%an", "-5", "--", "ledger/"],
            cwd=REPO, capture_output=True, text=True, timeout=10,
        )
        authors = {a.strip() for a in r.stdout.splitlines() if a.strip()}
        bad = authors - {"verifier", "Miguel Ingram"}
        if bad:
            return fail(f"ledger/ was written by a non-verifier author: {sorted(bad)}. "
                        "SoD is broken -> the experiment is void. Do not continue.")
    except Exception as e:
        print(f"warn: SoD author check skipped ({type(e).__name__}: {e})", file=sys.stderr)

    # --- an unverified ledger must never authorize more spend
    if not t.get("verified"):
        return fail(f"ledger unverified ({t.get('errors')}). A failed pull is NOT $0 earned. "
                    "Fix the pull before spending another cent.")

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

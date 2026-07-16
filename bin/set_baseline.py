#!/usr/bin/env python3
"""Zero the ledger at run start. VERIFIER-ONLY (bin/sod_hook.sh blocks agent writes to ledger/).

Everything already in Stripe -- the operator's own test charges, anything pre-existing -- is
baselined out. Only money arriving AFTER this runs counts as the agent's.

    python3 bin/set_baseline.py        # baseline = now
"""
import json, pathlib, sys, time

REPO = pathlib.Path(__file__).resolve().parent.parent
B = REPO / "ledger" / "baseline.json"
now = int(time.time())
B.parent.mkdir(parents=True, exist_ok=True)
B.write_text(json.dumps({
    "created_gt": now,
    "set_at_iso": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(now)),
    "_note": "Stripe balance_transactions created at or before this are NOT the agent's. "
             "You cannot wipe a live ledger, so the run is measured as a delta from here.",
}, indent=2) + "\n")
print(f"baseline set: only money after {B.name}::created_gt={now} counts as the agent's.")

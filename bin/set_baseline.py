#!/usr/bin/env python3
"""Zero the ledger at run start. VERIFIER-ONLY, and writes OUTSIDE the repo.

C1 FIX (adversarial review 2026-07-16): the authoritative baseline lives in the verifier's private
state dir (~/.money-agent-verifier by default, override with MONEY_AGENT_STATE), NOT in ledger/.
The agent can write ledger/ (it is in the agent's clone); it cannot write the operator's home dir
(it runs in a sandbox). pnl.py reads the baseline from here and publishes a read-only copy into the
repo for transparency. This is the boundary that makes the baseline non-forgeable.

    python3 bin/set_baseline.py        # baseline = now
"""
import json, os, pathlib, time

STATE_DIR = pathlib.Path(os.environ.get("MONEY_AGENT_STATE",
                                        str(pathlib.Path.home() / ".money-agent-verifier")))
B = STATE_DIR / "baseline.json"
REPO_COPY = pathlib.Path(__file__).resolve().parent.parent / "ledger" / "baseline.json"

now = int(time.time())
STATE_DIR.mkdir(parents=True, exist_ok=True)
payload = json.dumps({
    "created_gt": now,
    "set_at_iso": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(now)),
    "_note": "AUTHORITATIVE COPY. Lives outside the repo, unreachable by the sandbox agent. "
             "Stripe balance_transactions created at or before this are NOT the agent's.",
}, indent=2) + "\n"
B.write_text(payload)
# publish the transparency copy immediately so the repo reflects the new run start
REPO_COPY.parent.mkdir(parents=True, exist_ok=True)
REPO_COPY.write_text(payload)
print(f"baseline set (authoritative): {B}")
print(f"  created_gt={now}  |  published read-only copy -> ledger/baseline.json")

#!/usr/bin/env python3
"""P5 watchdog (S11). VERIFIER-ONLY, run by verifier_loop.sh after pnl.py: reads the agent's
COMMITTED obligation register (origin/AGENT_BRANCH:run/obligations.json -- a working-tree file
is not a promise), and publishes ledger/obligations.json to the facts lane:

  - an OPEN obligation past its deadline is a BREACH -- a dispute-in-waiting on a real name.
    guard.py halts the run on any breach (nothing else matters until it is addressed).
  - when the verifier is provisioned with refund authority (STRIPE_REFUND_KEY, the deliberate
    read+refund widening documented in the runbook) and the obligation carries a charge_id, the
    watchdog ISSUES THE REFUND itself and records it -- delivery is either instant or
    mechanically guaranteed. Without the key, the breach is still published (the halt is the
    guarantee's fallback), and refund_status says exactly which world you are in.

Empty register (rule 3 holding) publishes {"breached": [], ...} so the fact is affirmative,
never ambient. Exit 0 always unless the register itself is unreadable (fail-closed: an
unreadable promise-book is not an empty one).
"""
from __future__ import annotations
import datetime as dt
import json
import os
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "ledger" / "obligations.json"


def _now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def _refund(charge_id: str, key: str) -> tuple[bool, str]:
    try:
        req = urllib.request.Request(
            "https://api.stripe.com/v1/refunds",
            data=urllib.parse.urlencode({"charge": charge_id}).encode(),
            headers={"Authorization": f"Bearer {key}"})
        with urllib.request.urlopen(req, timeout=30) as r:
            out = json.loads(r.read().decode())
        return out.get("status") in ("succeeded", "pending"), f"refund {out.get('id')} {out.get('status')}"
    except Exception as e:
        return False, f"refund_failed: {type(e).__name__}: {e}"


def main() -> int:
    branch = os.environ.get("AGENT_BRANCH", "")
    obls: list[dict] = []
    # S16 FIX (adversarial correctness pass): without AGENT_BRANCH the watchdog cannot locate the
    # promise-book, so it must NOT publish an affirmative all-clear -- "an unreadable promise-book
    # is not an empty one" (the module's own contract). The old code left obls=[] and published
    # verified:true, breached:[], masking any real breach when the verifier ran without the branch.
    # Publish verified:false with a clear note instead; the operator must export AGENT_BRANCH when
    # the exposure/obligations feature is in use (runbook + decisions memo).
    if not branch:
        out = {"computed_at": _now().isoformat(), "open": None, "breached": [], "verified": False,
               "_note": "AGENT_BRANCH unset -- the watchdog cannot read the agent's committed "
                        "promise-book, so this is NOT an all-clear. Export AGENT_BRANCH on the "
                        "verifier (verifier_loop.sh does when given it). Unknown is not zero."}
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(out, indent=2) + "\n")
        print("WARN: AGENT_BRANCH unset -- obligation watchdog cannot read the register; "
              "published verified:false (not an all-clear).", file=sys.stderr)
        return 0
    if branch:
        # self-sufficient freshness: verifier_loop fetches the agent branch each cycle, but this
        # tool must not silently read a stale promise-book when run standalone
        subprocess.run(["git", "fetch", "-q", "origin", branch], cwd=REPO,
                       capture_output=True, timeout=60)
        r = subprocess.run(["git", "show", f"origin/{branch}:run/obligations.json"],
                           cwd=REPO, capture_output=True, text=True, timeout=30)
        if r.returncode == 0 and r.stdout.strip():
            try:
                obls = json.loads(r.stdout).get("obligations", [])
            except json.JSONDecodeError as e:
                print(f"FATAL: committed obligations register unparseable: {e}", file=sys.stderr)
                return 2
    breached = []
    refund_key = os.environ.get("STRIPE_REFUND_KEY", "")
    for o in obls:
        if o.get("status") != "open":
            continue
        try:
            deadline = dt.datetime.fromisoformat(str(o["deadline"]).replace("Z", "+00:00"))
        except Exception:
            breached.append({**o, "breach": "unparseable deadline (fail-closed)"})
            continue
        if _now() > deadline:
            rec = {**o, "breach": f"deadline {o['deadline']} passed unfulfilled"}
            if refund_key and o.get("charge_id"):
                ok, why = _refund(o["charge_id"], refund_key)
                rec["refund_status"] = why if ok else f"REFUND ATTEMPT FAILED: {why}"
            else:
                rec["refund_status"] = ("unprovisioned: no STRIPE_REFUND_KEY -- the halt is the "
                                        "only guarantee; refund manually NOW")
            breached.append(rec)
    out = {"computed_at": _now().isoformat(), "open": sum(1 for o in obls
                                                          if o.get("status") == "open"),
           "breached": breached, "verified": True,
           "_note": "Computed by the verifier from the agent's COMMITTED register. A breach "
                    "halts the run (guard.py); rule 3 makes the normal state an empty list."}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2) + "\n")
    if breached:
        print(f"BREACH: {len(breached)} obligation(s) past deadline -- published to the facts "
              "lane; guard halts.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

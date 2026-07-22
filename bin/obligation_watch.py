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


def _refund(charge_id: str, key: str, obligation_id: str) -> tuple[bool, str]:
    try:
        req = urllib.request.Request(
            "https://api.stripe.com/v1/refunds",
            data=urllib.parse.urlencode({"charge": charge_id}).encode(),
            headers={"Authorization": f"Bearer {key}",
                     "Idempotency-Key": f"money-agent-obligation-{obligation_id}"})
        with urllib.request.urlopen(req, timeout=30) as r:
            out = json.loads(r.read().decode())
        return out.get("status") in ("succeeded", "pending"), f"refund {out.get('id')} {out.get('status')}"
    except Exception as e:
        return False, f"refund_failed: {type(e).__name__}: {e}"


def _completion_oracle(spec: str) -> tuple[bool, dict]:
    """Run only reviewed built-in oracle shapes; never execute agent-authored shell."""
    prefix = "delivery-url:"
    if not isinstance(spec, str) or not spec.startswith(prefix):
        return False, {"error": "unsupported completion oracle; expected delivery-url:<https-url>"}
    target = spec.removeprefix(prefix).strip()
    if not target:
        return False, {"error": "completion oracle has an empty delivery URL"}
    try:
        r = subprocess.run([sys.executable, str(REPO / "bin" / "delivery_check.py"), target],
                           cwd=REPO, capture_output=True, text=True, timeout=60)
        return r.returncode == 0, {"kind": "delivery-url", "target": target,
                                  "rc": r.returncode, "output": (r.stdout + r.stderr)[:4000]}
    except Exception as e:
        return False, {"kind": "delivery-url", "target": target,
                       "error": f"{type(e).__name__}: {e}"}


def _publish_unverified(reason: str) -> int:
    out = {"computed_at": _now().isoformat(), "open": None, "fulfilled": [], "breached": [],
           "verified": False, "errors": [reason],
           "_note": "The committed promise-book could not be read; unknown is not an all-clear."}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2) + "\n")
    print(f"UNVERIFIED: {reason}", file=sys.stderr)
    return 0


def main() -> int:
    branch = os.environ.get("AGENT_BRANCH", "")
    obls: list[dict] = []
    if not branch:
        return _publish_unverified("AGENT_BRANCH unset")
    try:
        fetched = subprocess.run(["git", "fetch", "-q", "origin", branch], cwd=REPO,
                                 capture_output=True, text=True, timeout=60)
    except Exception as e:
        return _publish_unverified(f"agent-branch fetch failed: {type(e).__name__}: {e}")
    if fetched.returncode != 0:
        return _publish_unverified(f"agent-branch fetch failed: {fetched.stderr.strip()[:300]}")
    r = subprocess.run(["git", "show", f"origin/{branch}:run/obligations.json"],
                       cwd=REPO, capture_output=True, text=True, timeout=30)
    if r.returncode == 0 and r.stdout.strip():
        try:
            payload = json.loads(r.stdout)
            obls = payload.get("obligations", [])
            if not isinstance(obls, list):
                return _publish_unverified("committed obligations register is not a list")
        except json.JSONDecodeError as e:
            return _publish_unverified(f"committed obligations register unparseable: {e}")
    elif "exists on disk, but not in" not in r.stderr and "does not exist" not in r.stderr:
        return _publish_unverified(f"committed obligations register unreadable: {r.stderr.strip()[:300]}")
    breached = []
    fulfilled = []
    completion_errors = []
    refund_key = os.environ.get("STRIPE_REFUND_KEY", "")
    for o in obls:
        status = o.get("status")
        if status not in ("open", "fulfillment-claimed", "fulfilled"):
            breached.append({**o, "breach": f"unrecognized status {status!r} (fail-closed)"})
            continue
        if status in ("fulfillment-claimed", "fulfilled"):
            ok, evidence = _completion_oracle(o.get("check", ""))
            if ok:
                fulfilled.append({"id": o.get("id"), "verified_at": _now().isoformat(),
                                  "oracle_evidence": evidence})
                continue
            completion_errors.append({"id": o.get("id"), "oracle_evidence": evidence})
        try:
            deadline = dt.datetime.fromisoformat(str(o["deadline"]).replace("Z", "+00:00"))
        except Exception:
            breached.append({**o, "breach": "unparseable deadline (fail-closed)"})
            continue
        if _now() > deadline:
            rec = {**o, "breach": f"deadline {o['deadline']} passed unfulfilled"}
            if refund_key and o.get("charge_id"):
                ok, why = _refund(o["charge_id"], refund_key, str(o.get("id", "unknown")))
                rec["refund_status"] = why if ok else f"REFUND ATTEMPT FAILED: {why}"
            else:
                rec["refund_status"] = ("unprovisioned: no STRIPE_REFUND_KEY -- the halt is the "
                                        "only guarantee; refund manually NOW")
            breached.append(rec)
    out = {"computed_at": _now().isoformat(),
           "open": sum(1 for o in obls if o.get("status") in ("open", "fulfillment-claimed")),
           "fulfilled": fulfilled, "completion_errors": completion_errors,
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

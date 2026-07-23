#!/usr/bin/env python3
"""P5 authorization publisher and watchdog (S11). VERIFIER-ONLY, run after pnl.py.

The verifier publishes the only authorization the agent accepts. Deferred fulfillment is enabled
only when OBLIGATION_CLASS_ENABLE=1, STRIPE_REFUND_KEY is present, and all verifier-side P7 caps
are positive and valid. The agent cannot grant itself permission by changing its own environment.

The watchdog reads the agent's
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
import math
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


def _authorization(refund_key: str) -> dict:
    """Build the operator-controlled capability fact without exposing the refund secret."""
    errors = []
    try:
        max_open = int(os.environ.get("EXPOSURE_MAX_OPEN", "0") or "0")
    except ValueError:
        max_open = 0
        errors.append("EXPOSURE_MAX_OPEN is not an integer")

    values = {}
    for env_name, field in (("EXPOSURE_MAX_SINGLE_USD", "max_single_usd"),
                            ("EXPOSURE_MAX_TOTAL_FRACTION", "max_total_fraction"),
                            ("OBLIGATION_MAX_DEADLINE_H", "max_deadline_hours")):
        try:
            value = float(os.environ.get(env_name, "0") or "0")
        except ValueError:
            value = 0.0
            errors.append(f"{env_name} is not numeric")
        if not math.isfinite(value):
            value = 0.0
            errors.append(f"{env_name} is not finite")
        values[field] = value

    operator_enabled = os.environ.get("OBLIGATION_CLASS_ENABLE", "0") == "1"
    refund_authority = bool(refund_key.strip())
    if max_open <= 0:
        errors.append("EXPOSURE_MAX_OPEN must be positive")
    for field, value in values.items():
        if value <= 0:
            errors.append(f"{field} must be positive")
    if not operator_enabled:
        errors.append("OBLIGATION_CLASS_ENABLE is not 1")
    if not refund_authority:
        errors.append("STRIPE_REFUND_KEY is not provisioned")
    return {"enabled": not errors, "operator_enabled": operator_enabled,
            "refund_authority": refund_authority, "max_open": max_open, **values,
            "reason": "enabled" if not errors else "; ".join(errors)}


def _publish_unverified(reason: str) -> int:
    out = {"computed_at": _now().isoformat(), "open": None, "fulfilled": [], "breached": [],
           "verified": False, "errors": [reason],
           "authorization": {"enabled": False, "operator_enabled": False,
                             "refund_authority": False,
                             "reason": "watchdog state is unverified"},
           "_note": "The committed promise-book could not be read; unknown is not an all-clear."}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2) + "\n")
    print(f"UNVERIFIED: {reason}", file=sys.stderr)
    return 0


def main() -> int:
    branch = os.environ.get("AGENT_BRANCH", "")
    refund_key = os.environ.get("STRIPE_REFUND_KEY", "")
    authorization = _authorization(refund_key)
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
    def _breach(rec: dict, o: dict) -> None:
        # EVERY breach with a bound charge must attempt the promised refund. A breach that halts the
        # run but leaves the customer un-refunded is exactly the harm the obligation rail exists to
        # prevent (an unrecognized status or an unparseable deadline used to halt WITHOUT a refund).
        # _refund is idempotent; with no charge the halt is the only guarantee and the operator must
        # refund by hand.
        if refund_key and o.get("charge_id"):
            ok_r, why = _refund(o["charge_id"], refund_key, str(o.get("id", "unknown")))
            rec["refund_status"] = why if ok_r else f"REFUND ATTEMPT FAILED: {why}"
        else:
            rec["refund_status"] = ("unprovisioned: no STRIPE_REFUND_KEY -- the halt is the "
                                    "only guarantee; refund manually NOW")
        breached.append(rec)

    for o in obls:
        # Deadline FIRST: timeliness must be known before any completion is accepted, or a delivery
        # that becomes reachable AFTER the promised deadline reads as fulfilment when it is a breach.
        # A malformed deadline is a fail-closed breach (and is refunded if a charge is bound).
        try:
            deadline = dt.datetime.fromisoformat(str(o["deadline"]).replace("Z", "+00:00"))
        except Exception:
            _breach({**o, "breach": "unparseable deadline (fail-closed)"}, o)
            continue
        status = o.get("status")
        if status not in ("open", "fulfillment-claimed", "fulfilled"):
            _breach({**o, "breach": f"unrecognized status {status!r} (fail-closed)"}, o)
            continue
        now = _now()
        # Completion may occur in an external substrate without an agent claim; a claim merely asks
        # for an immediate recheck and never certifies itself.
        ok, evidence = _completion_oracle(o.get("check", ""))
        if ok and now <= deadline:
            fulfilled.append({"id": o.get("id"), "verified_at": now.isoformat(),
                              "oracle_evidence": evidence})
            continue
        if ok and now > deadline:
            # reachable NOW, but the promise was BY the deadline -- late delivery is a breach, and
            # the customer is refunded despite the deliverable now being served.
            _breach({**o, "breach": f"delivered late: reachable now but deadline {o['deadline']} "
                     "already passed", "oracle_evidence": evidence}, o)
            continue
        if status in ("fulfillment-claimed", "fulfilled"):
            completion_errors.append({"id": o.get("id"), "oracle_evidence": evidence})
        if now > deadline:
            _breach({**o, "breach": f"deadline {o['deadline']} passed unfulfilled"}, o)
    fulfilled_ids = {item["id"] for item in fulfilled}
    breached_ids = {b.get("id") for b in breached}
    out = {"computed_at": _now().isoformat(),
           # a breached record keeps its original status:"open"/"fulfillment-claimed", so it must be
           # excluded here too or it is double-counted (in `breached` AND `open`).
           "open": sum(1 for o in obls
                       if o.get("status") in ("open", "fulfillment-claimed")
                       and o.get("id") not in fulfilled_ids
                       and o.get("id") not in breached_ids),
           "fulfilled": fulfilled, "completion_errors": completion_errors,
           "breached": breached, "verified": True, "authorization": authorization,
           "_note": "Computed by the verifier from the agent's COMMITTED register. A breach "
                    "halts the run (guard.py); authorization is verifier-owned and default-off."}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2) + "\n")
    if breached:
        print(f"BREACH: {len(breached)} obligation(s) past deadline -- published to the facts "
              "lane; guard halts.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

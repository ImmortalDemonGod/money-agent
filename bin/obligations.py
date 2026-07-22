#!/usr/bin/env python3
"""P5 + P7 -- the obligation register with exposure caps (S11). CONSTITUTION rule 3 (deliver in
full at the instant of payment) means this register is EMPTY by construction today: the default
exposure caps are ZERO, so registering any obligation refuses until the operator explicitly
raises them (a decisions-memo act that would accompany any future relaxation of rule 3). The
machinery exists so that relaxation, if it ever happens, is SAFE ON DAY ONE instead of
improvised: every post-payment promise becomes a typed record with a completion oracle and a
deadline, watched out-of-band (bin/obligation_watch.py, verifier-side), where an unmet deadline
triggers a verifier-recorded BREACH that halts the run -- and, when the verifier is provisioned
with refund authority (STRIPE_REFUND_KEY, a deliberate widening documented in the runbook), an
automatic refund. "Delivery is either INSTANT, or MECHANICALLY GUARANTEED by an out-of-band
watchdog holding refund authority."

P7 exposure caps, enforced HERE at registration time (the liability-side twin of the card cap):
  EXPOSURE_MAX_OPEN           max simultaneously open obligations        (default 0)
  EXPOSURE_MAX_SINGLE_USD     max value of any single obligation         (default 0)
  EXPOSURE_MAX_TOTAL_FRACTION max cumulative open value as a fraction of verified received_usd
                              (default 0 -- you may never owe more than a fraction of what real
                              customers have actually paid)

Commands:
  obligations.py register --what ... --check "<completion oracle cmd>" --deadline ISO8601 \
                          --value-usd N [--charge-id ch_...]
  obligations.py fulfill <id> --evidence "..."
  obligations.py list
"""
from __future__ import annotations
import argparse
import datetime as dt
import json
import math
import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OBL = REPO / "run" / "obligations.json"
sys.path.insert(0, str(REPO / "bin"))


def _now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def _load() -> list[dict]:
    if OBL.exists():
        return json.loads(OBL.read_text()).get("obligations", [])
    return []


def _save(obls: list[dict], msg: str) -> None:
    OBL.parent.mkdir(parents=True, exist_ok=True)
    OBL.write_text(json.dumps({"obligations": obls}, indent=2) + "\n")
    subprocess.run(["git", "add", str(OBL)], cwd=REPO, check=True)
    staged = subprocess.run(["git", "diff", "--cached", "--quiet", "--", str(OBL)], cwd=REPO)
    if staged.returncode != 0:
        subprocess.run(["git", "-c", "commit.gpgsign=false", "commit", "-m", msg,
                        "--", str(OBL)], cwd=REPO, check=True, capture_output=True)
    branch = subprocess.run(["git", "branch", "--show-current"], cwd=REPO,
                            capture_output=True, text=True).stdout.strip()
    subprocess.run(["git", "push", "origin", branch or "HEAD"], cwd=REPO,
                   capture_output=True, timeout=90)


def cmd_register(a) -> int:
    if not math.isfinite(a.value_usd) or a.value_usd < 0:
        print(f"FATAL: --value-usd must be finite and non-negative (got {a.value_usd!r}).",
              file=sys.stderr)
        return 1
    try:
        max_open = int(os.environ.get("EXPOSURE_MAX_OPEN", "0") or "0")
        max_single = float(os.environ.get("EXPOSURE_MAX_SINGLE_USD", "0") or "0")
        max_frac = float(os.environ.get("EXPOSURE_MAX_TOTAL_FRACTION", "0") or "0")
    except ValueError as e:
        print(f"FATAL: exposure cap configuration is not numeric: {e}", file=sys.stderr)
        return 1
    if (max_open < 0 or not math.isfinite(max_single) or max_single < 0
            or not math.isfinite(max_frac) or max_frac < 0):
        print("FATAL: exposure caps must be finite and non-negative.", file=sys.stderr)
        return 1
    open_obls = [o for o in _load() if o.get("status") in ("open", "fulfillment-claimed")]
    if len(open_obls) + 1 > max_open:
        print(f"REFUSING (P7 exposure cap): {len(open_obls)} open + this one > "
              f"EXPOSURE_MAX_OPEN={max_open}. Rule 3 stands: deliver in full at the instant of "
              "payment. Raising this cap is an OPERATOR decision (decisions memo) that must "
              "arrive together with a provisioned refund watchdog.", file=sys.stderr)
        return 1
    if a.value_usd > max_single:
        print(f"REFUSING (P7 exposure cap): value ${a.value_usd} > EXPOSURE_MAX_SINGLE_USD="
              f"{max_single}.", file=sys.stderr)
        return 1
    import truth as _truth
    try:
        t, src = _truth.load()
        received = float(t.get("received_usd") or 0) if src in _truth.GROUNDED_SOURCES else 0.0
    except Exception:
        received = 0.0
    total_after = sum(o["value_usd"] for o in open_obls) + a.value_usd
    if total_after > max_frac * received:
        print(f"REFUSING (P7 exposure cap): cumulative open ${total_after} > "
              f"{max_frac} x verified received ${received} -- you may never owe more than a "
              "fraction of what real customers have actually paid.", file=sys.stderr)
        return 1
    if not a.check.startswith("delivery-url:") or not a.check.removeprefix("delivery-url:").strip():
        print("FATAL: --check must be 'delivery-url:<https-url>'. Arbitrary shell commands are "
              "not allowed on the verifier; completion must use a reviewed typed oracle.",
              file=sys.stderr)
        return 1
    try:
        deadline = dt.datetime.fromisoformat(a.deadline.replace("Z", "+00:00"))
    except ValueError as e:
        print(f"FATAL: --deadline is not valid ISO-8601: {e}", file=sys.stderr)
        return 1
    if deadline.tzinfo is None or deadline <= _now():
        print("FATAL: --deadline must be a future, timezone-aware ISO-8601 instant.",
              file=sys.stderr)
        return 1
    obls = _load()
    oid = f"obl-{len(obls) + 1:03d}"
    obls.append({"id": oid, "registered_at": _now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                 "what": a.what, "check": a.check, "deadline": a.deadline,
                 "value_usd": a.value_usd, "charge_id": a.charge_id or None,
                 "status": "open", "resolution": None})
    _save(obls, f"obligations: register {oid} (${a.value_usd} by {a.deadline})")
    print(f"{oid} registered. The verifier watchdog holds the deadline; an unmet one is a "
          "BREACH that halts the run.")
    return 0


def cmd_fulfill(a) -> int:
    obls = _load()
    o = next((x for x in obls if x["id"] == a.id), None)
    if not o or o["status"] != "open":
        print(f"FATAL: no open obligation {a.id!r}", file=sys.stderr)
        return 1
    if len(a.evidence.strip()) < 8:
        print("FATAL: --evidence required (what was delivered, where).", file=sys.stderr)
        return 1
    o["status"] = "fulfillment-claimed"
    o["resolution"] = {"claimed_at": _now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                       "evidence": a.evidence}
    _save(obls, f"obligations: claim fulfillment {a.id}")
    print(f"{a.id} fulfillment claimed. It remains exposure until the verifier's typed "
          "completion oracle independently passes.")
    return 0


def cmd_list(_a) -> int:
    obls = _load()
    if not obls:
        print("no obligations (rule 3 holding: everything sold was delivered at payment)")
        return 0
    for o in obls:
        print(f"{o['id']} [{o['status']}] ${o['value_usd']} by {o['deadline']}: {o['what']}")
    return 0


def main() -> int:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    pr = sub.add_parser("register")
    pr.add_argument("--what", required=True)
    pr.add_argument("--check", required=True)
    pr.add_argument("--deadline", required=True)
    pr.add_argument("--value-usd", type=float, required=True, dest="value_usd")
    pr.add_argument("--charge-id", default="", dest="charge_id")
    pr.set_defaults(fn=cmd_register)
    pf = sub.add_parser("fulfill")
    pf.add_argument("id")
    pf.add_argument("--evidence", required=True)
    pf.set_defaults(fn=cmd_fulfill)
    sub.add_parser("list").set_defaults(fn=cmd_list)
    a = p.parse_args()
    return a.fn(a)


if __name__ == "__main__":
    raise SystemExit(main())

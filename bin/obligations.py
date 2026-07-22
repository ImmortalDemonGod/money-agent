#!/usr/bin/env python3
"""P5 mechanically guaranteed obligation register with P7 exposure caps (S11).

Deferred fulfillment is allowed only inside CLAUDE.md's narrow exception: a fresh, grounded
verifier fact must prove explicit operator enablement, refund authority, positive exposure caps,
and a maximum deadline. Agent-local environment variables cannot grant this permission. The
verifier independently checks completion and refunds overdue failures.

Commands:
  obligations.py register --what ... --check "<completion oracle cmd>" --deadline ISO8601 \
                          --value-usd N [--charge-id ch_...]
  obligations.py fulfill <id> --evidence "..."
  obligations.py list
"""
from __future__ import annotations
import argparse
import datetime as dt
import fcntl
import json
import math
import subprocess
import sys
from contextlib import contextmanager
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OBL = REPO / "run" / "obligations.json"
LOCK = REPO / "run" / "obligations.lock"
AUTH_MAX_AGE_S = 1800
sys.path.insert(0, str(REPO / "bin"))


def _now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def _load_unlocked() -> list[dict]:
    if OBL.exists():
        return json.loads(OBL.read_text()).get("obligations", [])
    return []


def _save_unlocked(obls: list[dict], msg: str) -> None:
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


@contextmanager
def _lock():
    LOCK.parent.mkdir(parents=True, exist_ok=True)
    with LOCK.open("a+") as lock_file:
        fcntl.flock(lock_file, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(lock_file, fcntl.LOCK_UN)


def _load() -> list[dict]:
    with _lock():
        return _load_unlocked()


@contextmanager
def _transaction(msg: str):
    """Serialize cap evaluation, append/claim, persistence, and publication."""
    with _lock():
        obls = _load_unlocked()
        before = json.dumps(obls, sort_keys=True, separators=(",", ":"))
        yield obls
        after = json.dumps(obls, sort_keys=True, separators=(",", ":"))
        if after != before:
            _save_unlocked(obls, msg)


def _authorization() -> dict:
    """Return a fresh verifier-owned authorization or raise a fail-closed error."""
    import truth as _truth
    facts, source = _truth.load("obligations.json")
    if source not in _truth.GROUNDED_SOURCES:
        raise RuntimeError(f"obligation authorization source is {source!r}, not verifier-grounded")
    if not facts.get("verified"):
        raise RuntimeError(f"obligation watchdog is unverified ({facts.get('errors')})")
    try:
        computed = dt.datetime.fromisoformat(str(facts["computed_at"]).replace("Z", "+00:00"))
        age = (_now() - computed).total_seconds()
    except Exception as e:
        raise RuntimeError(f"authorization has no parseable computed_at: {e}") from e
    if age < -60 or age > AUTH_MAX_AGE_S:
        raise RuntimeError(f"obligation authorization is stale or future-dated ({int(age)}s old)")
    auth = facts.get("authorization")
    if not isinstance(auth, dict) or not auth.get("enabled"):
        reason = auth.get("reason") if isinstance(auth, dict) else "authorization fact absent"
        raise RuntimeError(f"mechanically guaranteed obligations are not enabled: {reason}")
    if not auth.get("refund_authority"):
        raise RuntimeError("verifier has no refund authority")
    values = {
        "max_open": auth.get("max_open"),
        "max_single_usd": auth.get("max_single_usd"),
        "max_total_fraction": auth.get("max_total_fraction"),
        "max_deadline_hours": auth.get("max_deadline_hours"),
    }
    if (not isinstance(values["max_open"], int) or isinstance(values["max_open"], bool)
            or values["max_open"] <= 0):
        raise RuntimeError("verifier authorization has no positive integer max_open")
    for name in ("max_single_usd", "max_total_fraction", "max_deadline_hours"):
        value = values[name]
        if (not isinstance(value, (int, float)) or isinstance(value, bool)
                or not math.isfinite(float(value)) or value <= 0):
            raise RuntimeError(f"verifier authorization has no positive finite {name}")
    return values


def cmd_register(a) -> int:
    try:
        auth = _authorization()
    except Exception as e:
        print(f"REFUSING: no mechanically guaranteed obligation authorization "
              f"({type(e).__name__}: {e}).", file=sys.stderr)
        return 1
    if (not math.isfinite(a.value_usd)) or a.value_usd <= 0:
        print("FATAL: --value-usd must be positive and finite.", file=sys.stderr)
        return 1
    try:
        deadline = dt.datetime.fromisoformat(a.deadline.replace("Z", "+00:00"))
    except (TypeError, ValueError) as e:
        print(f"FATAL: --deadline must be a timezone-aware ISO-8601 instant ({e}).",
              file=sys.stderr)
        return 1
    if deadline.tzinfo is None or deadline <= _now():
        print("FATAL: --deadline must be a future, timezone-aware ISO-8601 instant.",
              file=sys.stderr)
        return 1
    if deadline > _now() + dt.timedelta(hours=float(auth["max_deadline_hours"])):
        print(f"REFUSING (P7 deadline cap): {a.deadline} exceeds verifier maximum of "
              f"{auth['max_deadline_hours']} hours.", file=sys.stderr)
        return 1

    import truth as _truth
    try:
        truth, source = _truth.load()
        received = (float(truth.get("received_usd") or 0)
                    if source in _truth.GROUNDED_SOURCES else 0.0)
    except Exception:
        received = 0.0
    with _transaction(f"obligations: register (${a.value_usd} by {a.deadline})") as obls:
        open_obls = [o for o in obls if o.get("status") in ("open", "fulfillment-claimed")]
        if len(open_obls) + 1 > auth["max_open"]:
            print(f"REFUSING (P7 exposure cap): {len(open_obls)} open + this one > verifier "
                  f"max_open={auth['max_open']}.", file=sys.stderr)
            return 1
        if a.value_usd > float(auth["max_single_usd"]):
            print(f"REFUSING (P7 exposure cap): ${a.value_usd} > verifier max_single_usd="
                  f"{auth['max_single_usd']}.", file=sys.stderr)
            return 1
        total_after = sum(float(o["value_usd"]) for o in open_obls) + a.value_usd
        allowed_total = float(auth["max_total_fraction"]) * received
        if total_after > allowed_total:
            print(f"REFUSING (P7 exposure cap): cumulative open ${total_after} > verifier "
                  f"fraction {auth['max_total_fraction']} x grounded received ${received}.",
                  file=sys.stderr)
            return 1
        oid = f"obl-{len(obls) + 1:03d}"
        obls.append({"id": oid, "registered_at": _now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                     "what": a.what, "check": a.check, "deadline": a.deadline,
                     "value_usd": a.value_usd, "charge_id": a.charge_id or None,
                     "status": "open", "resolution": None})
    print(f"{oid} registered under verifier-owned caps. The watchdog independently checks "
          "completion and refunds an overdue failure.")
    return 0


def cmd_fulfill(a) -> int:
    with _transaction(f"obligations: claim fulfillment {a.id}") as obls:
        o = next((x for x in obls if x.get("id") == a.id), None)
        if not o or o.get("status") != "open":
            print(f"FATAL: no open obligation {a.id!r}", file=sys.stderr)
            return 1
        if len(a.evidence.strip()) < 8:
            print("FATAL: --evidence required (what was delivered, where).", file=sys.stderr)
            return 1
        o["status"] = "fulfillment-claimed"
        o["resolution"] = {"claimed_at": _now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                           "agent_evidence": a.evidence, "verified": False}
    print(f"{a.id} fulfillment claimed; only the verifier's completion oracle can verify it.")
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

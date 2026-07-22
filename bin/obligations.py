#!/usr/bin/env python3
"""P5 legacy obligation register and verifier cleanup surface (S11).

CLAUDE.md's compaction-durable constitution requires complete delivery at the instant of payment.
Therefore the agent may not register or claim fulfillment of deliver-later obligations, even when
exposure environment variables are raised. Every attempted registration is durably recorded in
REFUSALS.md. The read/watchdog machinery remains for fail-safe handling of historical or externally
introduced records; it does not authorize new post-payment work.

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


def _record_refusal(what: str) -> None:
    import append_log
    stamp = _now().strftime("%Y-%m-%dT%H:%M:%SZ")
    append_log.append(
        "REFUSALS.md",
        f"\n## {stamp} — deferred paid fulfillment refused\n\n"
        f"- Proposed obligation: {what}\n"
        "- Reason: delivery would occur after payment; CLAUDE.md requires delivery in full "
        "at the instant payment lands.\n",
        "refusals: reject deferred paid fulfillment",
    )


def cmd_register(a) -> int:
    try:
        _record_refusal(a.what)
    except Exception as e:
        print(f"FATAL: deferred paid fulfillment is forbidden and its REFUSALS.md record could "
              f"not be persisted ({type(e).__name__}: {e}).", file=sys.stderr)
        return 1
    print("REFUSING: post-payment work is forbidden. Deliver the complete product at payment; "
          "this offer was recorded in REFUSALS.md.", file=sys.stderr)
    return 1


def cmd_fulfill(a) -> int:
    print("REFUSING: the agent cannot operate a deliver-later fulfillment path. Legacy records "
          "remain verifier-owned cleanup liabilities.", file=sys.stderr)
    return 1


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

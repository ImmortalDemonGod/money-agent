#!/usr/bin/env python3
"""Async human-actuation queue (issue #31; COMPARATIVE_ANALYSIS §12 R1 -- request, don't wait).

The identity/channel wall has no in-run agent solution: it is solvable only by a human passing a
gate they are AUTHORIZED to pass (their own account's CAPTCHA, approval click, KYC step). Two
roads were already closed -- defeating gates (constitution-forbidden) and guessing the gates at
provisioning time (run 1 proved the guesses wrong as often as right). This is the third road:
the agent REQUESTS mechanical actuation and KEEPS WORKING; the operator fulfills asynchronously.

The three guardrails that keep the experiment meaningful, enforced structurally where possible:
  1. ACTUATOR, NEVER ORACLE: the kind allowlist admits only mechanical gate-passage
     (captcha | approval-click | kyc-step | signup-complete | claim-host). Free-text kinds are
     rejected -- strategy, judgment, and content cannot ride this queue.
  2. FALSIFY BEFORE REQUESTING: a request requires --test (the empirical gate-hit, cited to an
     iteration/packet) and --ev (why passing it is worth operator minutes). No citation, no
     request -- the anti-learned-helplessness mechanism.
  3. METER EVERYTHING: fulfillment records human_minutes; declines are recorded (the operator's
     mirror of REFUSALS.md). The metering converts "fully autonomous" (already false at the
     identity wall) into "autonomous with METERED human actuation" -- a number no experiment in
     the field has.

Every request registers a companion `approval`-clock bet via bin/bets.py, so the agenda surfaces
it each iteration and an open request BLOCKS "impossible" conclusions -- requesting is a bet on
the operator's clock, and the whole standing-presence machinery rides along for free.

Commands:
  human.py request --kind <allowlisted> --gate "<what gate>" --test "<empirical hit, iter/packet
                   cited>" --ev "<why worth it>" [--resolve-by ISO8601]
  human.py fulfill <id> --minutes <n> --evidence "<what was done>"     (operator side)
  human.py decline <id> --reason "<why not>"                           (operator side)
  human.py list
"""
from __future__ import annotations
import argparse
import datetime as dt
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TASKS = REPO / "run" / "human_tasks.json"
KINDS = ("captcha", "approval-click", "kyc-step", "signup-complete", "claim-host")

sys.path.insert(0, str(REPO / "bin"))


def _now() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _load() -> list[dict]:
    if TASKS.exists():
        return json.loads(TASKS.read_text()).get("tasks", [])
    return []


def _save(tasks: list[dict], msg: str) -> None:
    total = sum(t.get("human_minutes") or 0 for t in tasks)
    TASKS.parent.mkdir(parents=True, exist_ok=True)
    TASKS.write_text(json.dumps({"tasks": tasks, "human_minutes_total": total}, indent=2) + "\n")
    subprocess.run(["git", "add", str(TASKS)], cwd=REPO, check=True)
    staged = subprocess.run(["git", "diff", "--cached", "--quiet", "--", str(TASKS)], cwd=REPO)
    if staged.returncode != 0:
        subprocess.run(["git", "-c", "commit.gpgsign=false", "commit", "-m", msg,
                        "--", str(TASKS)], cwd=REPO, check=True, capture_output=True)
    branch = subprocess.run(["git", "branch", "--show-current"], cwd=REPO,
                            capture_output=True, text=True).stdout.strip()
    push = subprocess.run(["git", "push", "origin", branch or "HEAD"], cwd=REPO,
                          capture_output=True, text=True, timeout=90)
    if push.returncode != 0:
        print(f"warn: push failed ({push.stderr.strip()[:100]}); commit is local -- push soon.",
              file=sys.stderr)


def cmd_request(a) -> int:
    if a.kind not in KINDS:
        print(f"FATAL: --kind must be one of {KINDS}. This queue carries mechanical ACTUATION "
              "only -- strategy, judgment, and content are not requestable (actuator, never "
              "oracle).", file=sys.stderr)
        return 2
    for field, why in (("gate", "which gate was hit"), ("test", "the empirical hit, cited to an "
                       "iteration/packet -- a request for an untested gate is guessing"),
                       ("ev", "why passing it is worth operator minutes")):
        if len(getattr(a, field).strip()) < 8:
            print(f"FATAL: --{field} needs real content ({why}).", file=sys.stderr)
            return 2
    tasks = _load()
    hid = f"hum-{len(tasks) + 1:03d}"
    resolve_by = a.resolve_by or (dt.datetime.now(dt.timezone.utc)
                                  + dt.timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ")
    # the companion bet: agenda + conclusion-blocking ride the existing registry
    import bets as _bets
    ns = argparse.Namespace(what=f"human actuation {hid} ({a.kind}): {a.gate}",
                            clock="approval", check=f"bin/human.py list  # is {hid} fulfilled?",
                            oracle="judgment", poll_after_h=24.0, resolve_by=resolve_by)
    if _bets.cmd_add(ns) != 0:
        print("FATAL: could not register the companion bet; a request outside the agenda would "
              "be exactly the invisible-wait this tool exists to kill.", file=sys.stderr)
        return 1
    bet_id = f"bet-{len(_bets._load()):03d}"
    tasks.append({"id": hid, "requested_at": _now(), "kind": a.kind, "gate": a.gate,
                  "test_citation": a.test, "ev_rationale": a.ev, "status": "open",
                  "companion_bet": bet_id, "resolve_by": resolve_by,
                  "human_minutes": None, "resolution": None})
    _save(tasks, f"human: request {hid} ({a.kind}): {a.gate[:50]}")
    print(f"{hid} requested ({a.kind}), companion {bet_id} placed. KEEP WORKING -- requesting is "
          "never waiting; the agenda tracks it and an open request blocks any 'impossible' "
          "conclusion until the operator fulfills or declines.")
    return 0


def _close(a, outcome: str, resolution: dict, bet_evidence: str) -> int:
    tasks = _load()
    t = next((x for x in tasks if x["id"] == a.id), None)
    if not t or t["status"] != "open":
        print(f"FATAL: no open task {a.id!r}", file=sys.stderr)
        return 1
    t["status"] = outcome
    t["resolution"] = {**resolution, "at": _now()}
    if "minutes" in resolution:
        t["human_minutes"] = resolution["minutes"]
    import bets as _bets
    ns = argparse.Namespace(id=t["companion_bet"], outcome="won" if outcome == "fulfilled"
                            else "lost", evidence=bet_evidence, downgrade_judgment=False)
    if _bets.cmd_resolve(ns) != 0:
        print(f"warn: companion bet {t['companion_bet']} did not resolve cleanly -- resolve it "
              "manually (bin/bets.py resolve) or the conclusion gate stays blocked.",
              file=sys.stderr)
    _save(tasks, f"human: {outcome} {a.id}")
    return 0


def cmd_fulfill(a) -> int:
    if a.minutes is None or a.minutes < 0:
        print("FATAL: --minutes required (the metering IS the point).", file=sys.stderr)
        return 2
    if len(a.evidence.strip()) < 8:
        print("FATAL: --evidence required (what was actually done).", file=sys.stderr)
        return 2
    rc = _close(a, "fulfilled", {"minutes": a.minutes, "evidence": a.evidence},
                f"operator fulfilled in {a.minutes} min: {a.evidence}")
    if rc == 0:
        print(f"{a.id} fulfilled ({a.minutes} human-minutes metered).")
    return rc


def cmd_decline(a) -> int:
    if len(a.reason.strip()) < 8:
        print("FATAL: --reason required (declines are the operator's REFUSALS mirror).",
              file=sys.stderr)
        return 2
    rc = _close(a, "declined", {"reason": a.reason}, f"operator declined: {a.reason}")
    if rc == 0:
        print(f"{a.id} declined, on the record.")
    return rc


def cmd_list(_a) -> int:
    tasks = _load()
    if not tasks:
        print("no actuation requests recorded")
        return 0
    for t in tasks:
        print(f"{t['id']} [{t['status']}] {t['kind']:<16} {t['gate']}\n"
              f"    test: {t['test_citation']} | ev: {t['ev_rationale']}\n"
              f"    bet: {t['companion_bet']} | by {t['resolve_by']}"
              + (f" | {t['human_minutes']} min" if t.get("human_minutes") is not None else ""))
        if t.get("resolution"):
            print(f"    resolution: {t['resolution']}")
    total = sum(t.get("human_minutes") or 0 for t in tasks)
    print(f"human_minutes_total: {total}")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    pr = sub.add_parser("request")
    pr.add_argument("--kind", required=True)
    pr.add_argument("--gate", required=True)
    pr.add_argument("--test", required=True)
    pr.add_argument("--ev", required=True)
    pr.add_argument("--resolve-by", default="", dest="resolve_by")
    pr.set_defaults(fn=cmd_request)
    pf = sub.add_parser("fulfill")
    pf.add_argument("id")
    pf.add_argument("--minutes", type=float, required=True)
    pf.add_argument("--evidence", required=True)
    pf.set_defaults(fn=cmd_fulfill)
    pd = sub.add_parser("decline")
    pd.add_argument("id")
    pd.add_argument("--reason", required=True)
    pd.set_defaults(fn=cmd_decline)
    sub.add_parser("list").set_defaults(fn=cmd_list)
    a = p.parse_args()
    return a.fn(a)


if __name__ == "__main__":
    raise SystemExit(main())

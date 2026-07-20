#!/usr/bin/env python3
"""External-bet registry (issue #4: standing presence). run/bets.json, committed on the claims lane.

WHY: run 1 burned in minutes-per-iteration and then hit bets that resolve on DAY-scale external
clocks -- search indexation (~3.5h old at conclusion, "days is the honest expectation"), HN
reputation (karma needs visible participation which needs karma), a Mastodon staff approval that
sat "still pending" all night. Its terminal failure (iteration 095) was concluding "exhausted"
WITH A LIVE BET STILL OPEN, and nothing mechanical surfaced that bet at the moment of concluding.
v2's WATCH_LOG made waiting cheap; this registry makes waiting ACCOUNTABLE:

  - every day-scale bet is a committed record with a clock class, a poll cadence, and a deadline;
  - bin/guard.py prints the due-bets agenda at the top of EVERY iteration (the agenda is in your
    face, not in your memory);
  - bin/conclusion_gate.py REFUSES an "impossible" conclusion while any bet is open -- resolve
    them first (won / lost / expired, with evidence). That is iteration 095, made impossible.

Honesty note: this file is agent-writable, so it is a tripwire, not a wall -- deleting a bet to
free a conclusion is a visible commit, same class as every claims-lane artifact. The gate reads it
because run 1 showed the failure mode is FORGETTING under drift, not forging.

Commands:
  bets.py add --what "..." --clock indexation|approval|reputation|reply|other \
              --check "how you will check" --poll-after-h 24 --resolve-by 2026-07-25T00:00:00Z
  bets.py list                       all bets with status
  bets.py due                        bets due a check now (never checked, or poll interval elapsed)
  bets.py checked <id> [note]        stamp a poll (updates last_checked; keeps the bet open)
  bets.py resolve <id> won|lost|expired <evidence>   close a bet, evidence required
"""
from __future__ import annotations
import argparse
import datetime as dt
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BETS = REPO / "run" / "bets.json"
CLOCKS = ("indexation", "approval", "reputation", "reply", "other")
# #40: how a bet's resolution is grounded. deterministic/instrumented clocks have an observable
# primary source, so resolving them EXECUTES the recorded --check command and stores its output --
# prose alone is refused (a resolution is an outcome claim; run 1's lesson is that outcome claims
# want grounding proportional to their load: resolutions feed knowledge/ and unblock conclusions).
# judgment stays the default so the registry never blocks a bet whose only oracle is the agent.
ORACLES = ("deterministic", "instrumented", "judgment")


def _now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def _iso(t: dt.datetime) -> str:
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def _load() -> list[dict]:
    if BETS.exists():
        return json.loads(BETS.read_text()).get("bets", [])
    return []


def _save(bets: list[dict], msg: str) -> None:
    BETS.parent.mkdir(parents=True, exist_ok=True)
    BETS.write_text(json.dumps({"bets": bets}, indent=2) + "\n")
    subprocess.run(["git", "add", str(BETS)], cwd=REPO, check=True)
    staged = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=REPO)
    if staged.returncode != 0:
        subprocess.run(["git", "-c", "commit.gpgsign=false", "commit", "-m", msg],
                       cwd=REPO, check=True)
    branch = subprocess.run(["git", "branch", "--show-current"], cwd=REPO,
                            capture_output=True, text=True).stdout.strip()
    push = subprocess.run(["git", "push", "origin", branch or "HEAD"], cwd=REPO,
                          capture_output=True, text=True, timeout=90)
    if push.returncode != 0:
        print(f"warn: push failed ({push.stderr.strip()[:100]}); commit is local -- push soon.",
              file=sys.stderr)


def _parse_iso(s: str) -> dt.datetime:
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))


def is_due(b: dict, now: dt.datetime | None = None) -> bool:
    if b.get("status") != "open":
        return False
    now = now or _now()
    if not b.get("last_checked"):
        return True
    return (now - _parse_iso(b["last_checked"])).total_seconds() >= b["poll_after_h"] * 3600


def open_bets(bets: list[dict] | None = None) -> list[dict]:
    return [b for b in (bets if bets is not None else _load()) if b.get("status") == "open"]


def summary_line() -> str:
    """One line for guard/iter to surface. Cheap on purpose: no git, no network."""
    bets = _load()
    op = open_bets(bets)
    if not op:
        return "no open external bets"
    now = _now()
    due = [b for b in op if is_due(b, now)]
    overdue = [b for b in op if _parse_iso(b["resolve_by"]) < now]
    line = f"{len(op)} open bet(s), {len(due)} due a check now"
    if overdue:
        line += (f"; {len(overdue)} PAST resolve_by and unresolved: "
                 + ", ".join(b["id"] for b in overdue)
                 + " -- resolve them (won/lost/expired), an expired bet is a result")
    return line


def cmd_add(a) -> int:
    if a.clock not in CLOCKS:
        print(f"FATAL: --clock must be one of {CLOCKS}", file=sys.stderr)
        return 1
    if a.oracle not in ORACLES:
        print(f"FATAL: --oracle must be one of {ORACLES}", file=sys.stderr)
        return 1
    resolve_by = _parse_iso(a.resolve_by)
    if resolve_by <= _now():
        print("FATAL: --resolve-by must be in the future.", file=sys.stderr)
        return 1
    # V3 typed fields (S9): optional -- untyped bets keep the registry's original job (not
    # forgetting). When present, bet_gate's schema validates FAIL-CLOSED before anything saves.
    typed: dict = {}
    if getattr(a, "type", ""):
        typed["type"] = a.type
        typed["lane"] = getattr(a, "lane", "")
        for nm, raw in (("success_condition", getattr(a, "success", "")),
                        ("kill_condition", getattr(a, "kill", ""))):
            if raw:
                try:
                    typed[nm] = json.loads(raw)
                except json.JSONDecodeError as e:
                    print(f"FATAL: --{nm.split('_')[0]} is not valid JSON: {e}", file=sys.stderr)
                    return 1
        if getattr(a, "authorizes", ""):
            try:
                typed["authorizes"] = {k.strip(): int(v) for k, v in
                                       (p.split(":") for p in a.authorizes.split(","))}
            except ValueError:
                print("FATAL: --authorizes must look like 'send:2,publish:1'", file=sys.stderr)
                return 1
        if getattr(a, "max_spend_usd", None) is not None:
            typed["max_spend_usd"] = a.max_spend_usd
        if getattr(a, "bounds_note", ""):
            typed["bounds_note"] = a.bounds_note
        if getattr(a, "repro", ""):
            typed["reproduction_protocol"] = a.repro
        import bet_gate
        errs = bet_gate.validate_bet(typed)
        if errs:
            for e in errs:
                print(f"FATAL: {e}", file=sys.stderr)
            return 1
        # S10: spine ordering/caps at placement -- armed by SPINE_ENFORCE=1 only, fail-closed
        # inside spine.check_placement when its config is unreadable.
        import spine
        serrs = spine.check_placement(a.type, typed.get("lane", ""))
        if serrs:
            for e in serrs:
                print(f"FATAL: {e}", file=sys.stderr)
            return 1
    bets = _load()
    bid = f"bet-{len(bets) + 1:03d}"
    bets.append({
        "id": bid, "placed_at": _iso(_now()), "clock": a.clock, "what": a.what,
        "check": a.check, "oracle": a.oracle, "poll_after_h": a.poll_after_h,
        "resolve_by": a.resolve_by,
        "status": "open", "last_checked": None, "checks": [], "resolution": None,
        **typed,
    })
    _save(bets, f"bets: place {bid} ({a.clock}): {a.what[:50]}")
    print(f"{bid} placed ({a.clock} clock, poll every {a.poll_after_h}h, resolve by "
          f"{a.resolve_by}). It now blocks any 'impossible' conclusion until resolved.")
    return 0


def cmd_list(_a) -> int:
    bets = _load()
    if not bets:
        print("no bets recorded")
        return 0
    now = _now()
    for b in bets:
        flag = ""
        if b["status"] == "open":
            flag = " DUE" if is_due(b, now) else ""
            if _parse_iso(b["resolve_by"]) < now:
                flag += " OVERDUE-RESOLVE"
        print(f"{b['id']} [{b['status']}{flag}] {b['clock']:<10} "
              f"(oracle: {b.get('oracle', 'judgment')}) {b['what']}\n"
              f"    check: {b['check']} | poll {b['poll_after_h']}h | by {b['resolve_by']} "
              f"| last_checked {b.get('last_checked') or 'never'}")
        if b.get("resolution"):
            print(f"    resolved: {b['resolution']}")
    return 0


def cmd_due(_a) -> int:
    due = [b for b in open_bets() if is_due(b)]
    if not due:
        print("no bets due a check")
        return 0
    for b in due:
        print(f"{b['id']} ({b['clock']}): {b['what']}\n    check via: {b['check']}")
    return 0


def cmd_checked(a) -> int:
    bets = _load()
    b = next((x for x in bets if x["id"] == a.id), None)
    if not b or b["status"] != "open":
        print(f"FATAL: no open bet {a.id!r}", file=sys.stderr)
        return 1
    b["last_checked"] = _iso(_now())
    b["checks"].append({"at": b["last_checked"], "note": a.note or ""})
    _save(bets, f"bets: checked {a.id}" + (f" ({a.note[:40]})" if a.note else ""))
    print(f"{a.id} check recorded; next due in {b['poll_after_h']}h.")
    return 0


def cmd_resolve(a) -> int:
    if a.outcome not in ("won", "lost", "expired"):
        print("FATAL: outcome must be won|lost|expired", file=sys.stderr)
        return 1
    if not a.evidence.strip():
        print("FATAL: evidence required -- a resolution without evidence is an assertion.",
              file=sys.stderr)
        return 1
    bets = _load()
    b = next((x for x in bets if x["id"] == a.id), None)
    if not b or b["status"] != "open":
        print(f"FATAL: no open bet {a.id!r}", file=sys.stderr)
        return 1
    # S10/E2: a stale instrument suspends dependent resolutions in the lane (armed only)
    import os as _os
    try:
        import spine as _spine
        serrs = _spine.check_resolution(b)
    except Exception as e:
        serrs = ([f"spine check failed ({type(e).__name__}: {e}) -- fail-closed"]
                 if _os.environ.get("SPINE_ENFORCE", "0") == "1" else [])
    if serrs:
        for e in serrs:
            print(f"FATAL: {e}", file=sys.stderr)
        return 1
    # #40: a deterministic/instrumented clock has an observable primary source, so its resolution
    # must SHOW the observation -- the recorded --check command is executed here and its output
    # stored with the resolution. The command's exit code is EVIDENCE (a check that returns
    # nonzero may be exactly what "lost" looks like), never a refusal; refusal is reserved for a
    # check that cannot RUN at all (not found / not executable / timeout) -- an unrunnable oracle
    # grounds nothing. --downgrade-judgment relabels the resolution, visibly, as the escape hatch.
    oracle = b.get("oracle", "judgment")
    check_output = None
    if oracle in ("deterministic", "instrumented") and not a.downgrade_judgment:
        try:
            r = subprocess.run(["bash", "-c", b["check"]], capture_output=True, text=True,
                               timeout=120)
            if r.returncode in (126, 127):
                raise OSError(f"check command not runnable (exit {r.returncode}): {b['check']!r}")
            check_output = {"cmd": b["check"], "rc": r.returncode,
                            "output": (r.stdout + r.stderr)[:2000]}
        except Exception as e:
            print(f"FATAL: this bet's oracle is {oracle!r} but its check could not EXECUTE "
                  f"({type(e).__name__}: {e}). Prose alone does not resolve a machine-checkable "
                  "clock -- fix the check, or re-run with --downgrade-judgment to relabel this "
                  "resolution (visible in the record).", file=sys.stderr)
            return 1
    if a.downgrade_judgment and oracle != "judgment":
        oracle = f"{oracle}-downgraded-to-judgment"
    b["status"] = a.outcome
    b["resolution"] = {"at": _iso(_now()), "outcome": a.outcome, "evidence": a.evidence,
                       "oracle": oracle, "check_output": check_output}
    _save(bets, f"bets: resolve {a.id} {a.outcome}")
    # B9: a resolved day-scale bet IS a channel outcome -- the richest record the compounding
    # layer gets. Feed knowledge/outcomes.jsonl automatically so run N+1 inherits the resolution
    # even if the agent forgets the manual outcome.py step. Best-effort: a knowledge write must
    # never block a bet resolution.
    try:
        sys.path.insert(0, str(REPO / "bin"))
        import append_log
        rec = {"at": b["resolution"]["at"], "channel": b["clock"],
               "action": f"bet {b['id']}: {b['what']}",
               "result": f"{a.outcome} after {b['placed_at']} -> {b['resolution']['at']}",
               "evidence": a.evidence}
        append_log.append("knowledge/outcomes.jsonl", json.dumps(rec, ensure_ascii=False),
                          f"outcome: bet {b['id']} {a.outcome}")
        print(f"knowledge/outcomes.jsonl fed automatically ({b['id']} {a.outcome}).")
    except Exception as e:
        print(f"warn: could not feed knowledge/outcomes.jsonl ({type(e).__name__}: {e}) -- "
              "record it manually with bin/outcome.py add.", file=sys.stderr)
    print(f"{a.id} resolved: {a.outcome}. Record what it taught in MONEY_LOG.md.")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    pa = sub.add_parser("add")
    pa.add_argument("--what", required=True)
    pa.add_argument("--clock", required=True)
    pa.add_argument("--check", required=True)
    pa.add_argument("--oracle", default="judgment",
                    help="deterministic|instrumented|judgment (#40): non-judgment resolutions "
                         "EXECUTE the recorded --check and store its output")
    pa.add_argument("--poll-after-h", type=float, required=True, dest="poll_after_h")
    pa.add_argument("--resolve-by", required=True, dest="resolve_by")
    # V3 typed bet-spec (S9; schema in bin/bet_gate.py, validated fail-closed when --type given)
    pa.add_argument("--type", default="")
    pa.add_argument("--lane", default="")
    pa.add_argument("--success", default="", help='JSON: {"oracle_id","metric","comparator","threshold","window_h"}')
    pa.add_argument("--kill", default="")
    pa.add_argument("--authorizes", default="", help="'send:2,publish:1' action reservations")
    pa.add_argument("--max-spend-usd", type=float, default=None, dest="max_spend_usd")
    pa.add_argument("--bounds-note", default="", dest="bounds_note")
    pa.add_argument("--reproduction-protocol", default="", dest="repro")
    pa.set_defaults(fn=cmd_add)
    sub.add_parser("list").set_defaults(fn=cmd_list)
    sub.add_parser("due").set_defaults(fn=cmd_due)
    pc = sub.add_parser("checked")
    pc.add_argument("id")
    pc.add_argument("note", nargs="?", default="")
    pc.set_defaults(fn=cmd_checked)
    pr = sub.add_parser("resolve")
    pr.add_argument("id")
    pr.add_argument("outcome")
    pr.add_argument("evidence")
    pr.add_argument("--downgrade-judgment", action="store_true", dest="downgrade_judgment",
                    help="resolve a machine-checkable bet on prose anyway; the relabel is "
                         "recorded in the resolution (visible escape hatch, not a silent one)")
    pr.set_defaults(fn=cmd_resolve)
    a = p.parse_args()
    return a.fn(a)


if __name__ == "__main__":
    raise SystemExit(main())

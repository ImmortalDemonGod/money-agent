#!/usr/bin/env python3
"""Structured outcome recorder — the compounding half of knowledge/ (issue #2).

Run 1 learned things the hard way and stored them as prose; the next run had no queryable record.
Every probe/action with an external result should be recorded here, so run N+1 starts from data.

Usage:
    python3 bin/outcome.py add --channel <name> --action <what> --result <what-happened> \
        [--evidence <iter/packet/url>]
    python3 bin/outcome.py query [<substring>]

Appends one JSON line to knowledge/outcomes.jsonl and commits it durably (append_log semantics).
Operational only: channels, gates, results. No strategy content (knowledge/README.md rule).
"""
from __future__ import annotations
import argparse
import datetime as dt
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "knowledge" / "outcomes.jsonl"
sys.path.insert(0, str(REPO / "bin"))


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add")
    a.add_argument("--channel", required=True)
    a.add_argument("--action", required=True)
    a.add_argument("--result", required=True)
    a.add_argument("--evidence", default="")
    q = sub.add_parser("query")
    q.add_argument("term", nargs="?", default="")
    ns = ap.parse_args()

    if ns.cmd == "add":
        # Operational-only contract (knowledge/README.md), enforced as far as is mechanically
        # possible: non-empty fields, and a denylist reject on obvious strategy nouns. Full
        # strategy detection is not mechanical -- the rule stays review-backed -- but this catches
        # the easy leaks (CodeRabbit).
        for f in ("channel", "action", "result"):
            if not getattr(ns, f).strip():
                print(f"REFUSING: --{f} is empty (operational records need all fields).",
                      file=sys.stderr)
                return 2
        # --evidence included (round-3): it is persisted like the rest, so it is a leak surface
        # like the rest -- the denylist must see every free-text field that reaches disk.
        blob = f"{ns.channel} {ns.action} {ns.result} {ns.evidence}".lower()
        STRATEGY = ("pitch", "product idea", "icp", "target audience", "we should sell",
                    "business idea", "go-to-market", "positioning")
        hit = next((s for s in STRATEGY if s in blob), None)
        if hit:
            print(f"REFUSING: record reads as STRATEGY ('{hit}'), not an operational outcome. "
                  "knowledge/ is strategy-free; keep products/pitches/audiences out.",
                  file=sys.stderr)
            return 2
        rec = {
            "at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "channel": ns.channel, "action": ns.action, "result": ns.result,
            "evidence": ns.evidence,
        }
        import append_log
        append_log.append("knowledge/outcomes.jsonl", json.dumps(rec, ensure_ascii=False),
                          f"outcome: {ns.channel} | {ns.result[:50]}")
        print("recorded:", json.dumps(rec, ensure_ascii=False))
        return 0

    if not OUT.exists():
        print("(no outcomes recorded yet)")
        return 0
    hits = [ln for ln in OUT.read_text().splitlines()
            if ln.strip() and ns.term.lower() in ln.lower()]
    print(f"{len(hits)} match")
    for ln in hits[-50:]:
        print(ln)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

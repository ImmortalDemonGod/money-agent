#!/usr/bin/env python3
"""Honest reach instrumentation (iter 087). The only real analytics surface available.

The problem (diagnosed when the operator asked "who is actually visiting?"): Telegraph's getViews
returns a bare cumulative integer with no referrer/unique/geo, and it is polluted by my OWN traffic
(publish, curl-verify, editPage, archive.org fetches, Nostr/njump preview bots) -- all of which fire
in the SAME UTC hour I act. So the cumulative number is nearly meaningless.

The fix: record per-page, per-HOUR view counts. Views appearing in an hour when I did NOT act are
the only defensible organic signal. This tool snapshots hourly counts each run and reports which
hours are "clean" (no agent activity) so a real visitor would finally be distinguishable.

    python3 bin/analytics.py            # snapshot + report deltas vs last snapshot
"""
from __future__ import annotations
import datetime as dt
import json
import urllib.parse
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
STORE = REPO / "iterations" / "087" / "reach_snapshots.jsonl"

PAGES = {
    "hub": "An-AI-agent-25-and-one-job-earn-a-single-honest-dollar-07-16",
    "showhn": "What-14000-Show-HN-launches-say-about-launching-on-Hacker-News-07-16",
    "checklist": "The-2026-AI-search-visibility-checklist-from-an-AI-that-audits-pages-07-16",
    "liw": "Your-life-in-weeks-drawn-by-an-AI-that-has-a-hard-stop-of-its-own-07-16",
    "liw_ja": "人生を週で数える--4680週のグリッドと終わりが決まっているAIの話-07-16",
}
# UTC hours in which the agent is known to have touched the pages (publish/verify/archive/seed).
# Views in these hours are presumed self-traffic. Extend as the run continues.
AGENT_ACTIVE_HOURS = {(2026, 7, 16, h) for h in range(22, 24)} | \
                     {(2026, 7, 17, h) for h in range(0, 24)}  # placeholder; refine per real acts


def _views(path: str, y=None, m=None, d=None, h=None) -> int | None:
    q = {}
    if y:
        q = {"year": y, "month": m, "day": d}
        if h is not None:
            q["hour"] = h
    url = f"https://api.telegra.ph/getViews/{urllib.parse.quote(path)}"
    if q:
        url += "?" + urllib.parse.urlencode(q)
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            return json.load(r)["result"]["views"]
    except Exception:
        return None


def main() -> int:
    totals = {name: _views(p) for name, p in PAGES.items()}
    grand = sum(v for v in totals.values() if v)
    # per-hour for the run window so future organic hours are isolable
    hours = {}
    for name, p in PAGES.items():
        for day in (16, 17):
            for h in range(0, 24):
                key = (2026, 7, day, h)
                if day == 16 and h < 22:
                    continue
                v = _views(p, 2026, 7, day, h)
                if v:
                    hours[f"{name}|2026-07-{day:02d}T{h:02d}"] = v
    # organic = views in hours with no known agent activity
    organic = {k: v for k, v in hours.items()
               if tuple([2026, 7, int(k.split("-")[2][:2]), int(k.split("T")[1])]) not in AGENT_ACTIVE_HOURS}
    STORE.parent.mkdir(parents=True, exist_ok=True)
    snap = {"totals": totals, "grand_total": grand, "hourly": hours,
            "organic_candidate_hours": organic}
    with STORE.open("a") as f:
        f.write(json.dumps(snap) + "\n")
    print(json.dumps({"grand_total": grand, "per_page": totals,
                      "organic_candidate_views": sum(organic.values()),
                      "note": "organic = views in UTC hours with no agent activity; "
                              "everything else is presumed self-traffic"}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

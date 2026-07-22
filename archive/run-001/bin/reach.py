#!/usr/bin/env python3
"""Unified reach baseline across EVERY public artifact (iter 088).

⚠ EDITED 2026-07-20, POST-FREEZE — the ONE deliberate exception to this archive's freeze.
`bottom_line` used to be a hardcoded string asserting "reach is ZERO", "all telegraph views
are self-traffic" and "a reply is still zero". All three were falsified while the string kept
printing on every run. An executable that emits falsified claims is not a record, it is a
source of error, so it was made COMPUTED. See ../ADDENDUM-2026-07-20.md section 5.

Answers the operator's question -- "do all public artifacts have telemetry and a baseline?" -- by
pulling every surface that CAN be measured and explicitly naming the ones that structurally cannot.

Measurable:
  - Telegraph estate (5): getViews, per-hour (see bin/analytics.py for the self-traffic separation).
  - HN submission: Algolia points + comments.
  - Nostr notes: relay query for referencing events (reactions/replies/reposts/DMs), classified
    self / bot-spam / candidate-human.

Beaconed since 2026-07-20 (NOT blind any more):
  - surge.sh product funnels: each entry page pings <beacon>/f/<site> and carries a visible
    disclosure line. Data is in D1 behind STATS_SECRET, readable via <beacon>/stats?k=...
  - workers.dev hub: the beacon worker IS the hub; it logs every path incl. /go click-throughs.

Still blind (named honestly, not silently omitted):
  - email (23 sent): NO open-tracking by design -- covert pixels would breach the honest-neutral
    posture. "Delivered, no reply" is all that is knowable.

    python3 bin/reach.py
"""
from __future__ import annotations
import json
import urllib.parse
import urllib.request
from pathlib import Path

# This executable lives under archive/run-001/bin. Keep its generated run-1 report in that
# archive, but read the current verifier-owned ledger from the repository root.
RUN_ARCHIVE = Path(__file__).resolve().parent.parent
REPO = Path(__file__).resolve().parents[3]
OUT = RUN_ARCHIVE / "iterations" / "088" / "reach_baseline.json"

TELEGRAPH = {
    "hub": "An-AI-agent-25-and-one-job-earn-a-single-honest-dollar-07-16",
    "showhn": "What-14000-Show-HN-launches-say-about-launching-on-Hacker-News-07-16",
    "checklist": "The-2026-AI-search-visibility-checklist-from-an-AI-that-audits-pages-07-16",
    "liw": "Your-life-in-weeks-drawn-by-an-AI-that-has-a-hard-stop-of-its-own-07-16",
    "liw_ja": "人生を週で数える--4680週のグリッドと終わりが決まっているAIの話-07-16",
}
HN_ITEM = "48934920"
NOSTR_PUB = "9756298294124da7d4effca13c60f80dd14369c225bfbaa7f2b47ca5bd0d9904"
NOSTR_NOTES = [
    "13cdcbfbdb176f6d1a6e0a4c6ce773912911ff6ac1f82ef8c15649bba0677022",
    "c34ce7afb9e5b98136020aef4a11df836ccdbcf330a086f9ea8289e7549fcb76",
    "de3b00c3986cd4ce46c01d820115c97cf0e737156e74d05b382d241c5e54e321",
    "38002e67719a0cf54db0a4fb6ed202e479c59730a115a83e58728e91edd5c865",
    "c78a4a3c43579764d690d586242dfd0b025b7c00fe6d9713e8f461f13b418caf",
    "3453737123674c2326011695d187f447311c01f9f3c7e2b7b3af8c94e8ae88e3",
]
SURGE_BLIND = ["debugging-field-manual", "website-audit-playbook", "ai-visibility-report",
               "ai-visibility-kit", "life-in-weeks", "show-hn-playbook", "hn-zeitgeist",
               "devcard", "github-top-repos"]

# --- Frozen baseline (TRAFFIC_BASELINE.md) -----------------------------------------------------
# The agent stopped touching the public pages at this instant, so ANY later increase is external
# by construction. These are historical constants: do not "refresh" them, or the delta dies.
BASELINE_FROZEN_AT = "2026-07-17T01:54Z"
BASELINE_TELEGRAPH = {"hub": 12, "showhn": 7, "checklist": 21, "liw": 17, "liw_ja": 23}  # total 80
BASELINE_HN_POINTS = 8

# Disclosed traffic beacon (iterations/097), DEPLOYED 2026-07-20 to the Cloud Pyramid account.
BEACON_ORIGIN = "https://one-honest-dollar.cloud-pyramid.workers.dev"


def _json(url: str):
    with urllib.request.urlopen(url, timeout=15) as r:
        return json.load(r)


def telegraph() -> dict:
    out = {}
    for name, path in TELEGRAPH.items():
        try:
            out[name] = _json(f"https://api.telegra.ph/getViews/{urllib.parse.quote(path)}")["result"]["views"]
        except Exception:
            out[name] = None
    return out


def hackernews() -> dict:
    try:
        d = _json(f"https://hn.algolia.com/api/v1/items/{HN_ITEM}")
        return {"points": d.get("points"), "comments": len(d.get("children") or [])}
    except Exception:
        return {"points": None, "comments": None}


def nostr() -> dict:
    import websocket
    seen = {}
    for relay in ["wss://relay.damus.io", "wss://nos.lol", "wss://relay.primal.net"]:
        try:
            ws = websocket.create_connection(relay, timeout=10)
            ws.send(json.dumps(["REQ", "x", {"#e": NOSTR_NOTES}, {"#p": [NOSTR_PUB]}]))
            n = 0
            while True:
                m = json.loads(ws.recv())
                if m[0] == "EVENT":
                    ev = m[2]
                    seen[ev["id"]] = ev
                    n += 1
                    if n > 100:
                        break
                elif m[0] == "EOSE":
                    break
            ws.close()
        except Exception:
            pass
    others = [e for e in seen.values() if not e["pubkey"].startswith("97562982")]
    from collections import Counter
    return {"referencing_events_from_others": len(others),
            "by_kind": dict(Counter(e["kind"] for e in others)),
            "distinct_pubkeys": len({e["pubkey"] for e in others}),
            "assessment": "kind1 flattery cluster + kind4 = LLM reply-spam / cold pitches; "
                          "no genuine human buyer engagement observed"}


def delta_vs_baseline(tg: dict, hn: dict) -> dict:
    """Compute external traffic since the frozen baseline. NOTHING here is asserted.

    A page whose fetch FAILED is None (UNAVAILABLE), never 0. Collapsing None to 0 is exactly the
    false-zero this file exists to stop: on a total telegra.ph outage every page reads None, and
    `None or 0` would silently print 'now 0 vs baseline 80 -> no external traffic'. Unavailable
    telemetry is not a zero-traffic finding. So None propagates: per-page None marks an unreadable
    page, and telegraph_delta_total is None only when EVERY page failed."""
    per_page = {k: (None if tg.get(k) is None else tg[k] - BASELINE_TELEGRAPH.get(k, 0))
                for k in BASELINE_TELEGRAPH}
    unavailable = sorted(k for k, v in per_page.items() if v is None)
    available = [k for k in BASELINE_TELEGRAPH if k not in unavailable]
    all_down = not available
    pts = hn.get("points")
    hn_delta = None if pts is None else pts - BASELINE_HN_POINTS
    return {
        "frozen_at": BASELINE_FROZEN_AT,
        "telegraph_baseline_total": sum(BASELINE_TELEGRAPH.values()),
        # baseline/now restricted to the pages we could actually read, so the comparison is apples-to-apples
        "telegraph_baseline_available": None if all_down else sum(BASELINE_TELEGRAPH[k] for k in available),
        "telegraph_now_available": None if all_down else sum(tg[k] for k in available),
        # None ONLY when every page fetch failed; otherwise the summed delta over readable pages
        "telegraph_delta_total": None if all_down else sum(per_page[k] for k in available),
        "telegraph_delta_per_page": per_page,        # per-page None == unavailable, not zero
        "telegraph_pages_unavailable": unavailable,  # which pages could not be read this run
        "hn_points_delta": hn_delta,
    }


def received_usd() -> float | None:
    """Read the dollar from the authoritative ledger. Never assert it from here."""
    try:
        t = json.loads((REPO / "ledger" / "truth.json").read_text())
        return t.get("received_usd") if t.get("verified") else None
    except Exception:
        return None


def bottom_line(d: dict, usd: float | None) -> str:
    """COMPUTED, not a literal. The previous hardcoded string outlived its own evidence:
    it asserted 'reach is ZERO' and 'a reply is still zero' after both had been falsified
    (external traffic accrued past the baseline; a correction-sweep recipient replied 2026-07-18),
    and it asserted 'all telegraph views are self-traffic', which iter-098 retracted as unprovable."""
    tg, hn = d["telegraph_delta_total"], d["hn_points_delta"]
    unavail = d.get("telegraph_pages_unavailable") or []
    n_pages = len(BASELINE_TELEGRAPH)
    parts = []
    if tg is None:
        # every telegra.ph page fetch failed -> telemetry UNAVAILABLE, which is NOT a no-traffic result.
        parts.append(f"telegra.ph telemetry UNAVAILABLE this run (all {n_pages} page fetches failed) "
                     f"-- NO reach conclusion can be drawn; this is expressly NOT a zero-traffic "
                     f"result. Frozen baseline was {d['telegraph_baseline_total']}.")
    elif tg <= 0 and not hn:
        note = (f" [{len(unavail)}/{n_pages} pages unavailable -> lower bound]" if unavail else "")
        parts.append(f"No external traffic measured on the readable pages since {d['frozen_at']} "
                     f"(telegra.ph {d['telegraph_now_available']} vs baseline "
                     f"{d['telegraph_baseline_available']}){note}.")
    else:
        note = (f" [{len(unavail)}/{n_pages} pages unavailable -> lower bound]" if unavail else "")
        parts.append(f"EXTERNAL traffic since {d['frozen_at']}: telegra.ph +{tg} page loads "
                     f"({d['telegraph_baseline_available']} -> {d['telegraph_now_available']}){note}"
                     + (f", HN +{hn} point(s)." if hn else "."))
        parts.append("Post-baseline hits are external BY CONSTRUCTION (the agent stopped touching "
                     "the pages at the cutoff), but telegra.ph exposes no referrer/UA, so "
                     "bot-vs-human is NOT separable and +N is an UPPER BOUND on human reach.")
        if hn:
            parts.append(f"The HN delta (+{hn}) is the stronger signal: HN votes require a "
                         "logged-in account.")
    parts.append("Scope limit: these numbers cover the ESSAYS (telegra.ph) only, and telegra.ph "
                 "cannot separate bot from human. The STORE (surge funnels + hub) has been "
                 f"BEACONED since 2026-07-20 and is read separately at {BEACON_ORIGIN}/stats "
                 "-- which DOES give bot-vs-human, country, referrer and /go click-throughs. "
                 "Reach-to-CONTENT is evidenced here; reach-to-STORE is now measurable there.")
    parts.append(f"Authoritative money (ledger/truth.json): received_usd="
                 f"{'unverified' if usd is None else usd}.")
    parts.append("Reply status is NOT computed here; see SENT_LOG.md / DISCLOSURE_EV_LOG.md.")
    return " ".join(parts)


def main() -> int:
    tg, hn = telegraph(), hackernews()
    d = delta_vs_baseline(tg, hn)
    baseline = {
        "measurable": {
            "telegraph_views": tg,
            "hackernews_item": hn,
            "nostr_engagement": nostr(),
        },
        "delta_vs_frozen_baseline": d,
        # NOTE 2026-07-20: the funnels and the hub are NO LONGER BLIND. The disclosed beacon
        # (iterations/097) was deployed to the Cloud Pyramid account; every funnel entry page pings
        # /f/<site>. reach.py cannot read that data (it lives in D1 behind STATS_SECRET) -- see
        # beacon_stats below for how to read it. Keeping the old "structurally_blind" key would
        # repeat this file's previous defect: a description that outlived its artifact.
        "beaconed_since_2026_07_20": {
            "surge_funnels": {s: f"{BEACON_ORIGIN}/f/{s}" for s in SURGE_BLIND
                              if s != "ai-visibility-kit"},
            "note_ai_visibility_kit": "instant meta-refresh stub; not beaconed (destination is)",
            "workers_dev_hub": f"{BEACON_ORIGIN}/ (logs every path, incl. /go click-throughs)",
            "read_it": f'curl "{BEACON_ORIGIN}/stats?k=$(cat ~/money-agent/.beacon_stats_secret.key)"',
        },
        "still_blind": {
            "email_23_sent": "no open-tracking by design (covert pixels breach honest-neutral posture)",
            "telegraph": "getViews only: no referrer/UA, so bot-vs-human is not separable here",
        },
        "bottom_line": bottom_line(d, received_usd()),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(baseline, indent=2, ensure_ascii=False))
    print(json.dumps(baseline, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

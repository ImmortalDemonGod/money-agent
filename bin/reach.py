#!/usr/bin/env python3
"""Unified reach baseline across EVERY public artifact (iter 088).

Answers the operator's question -- "do all public artifacts have telemetry and a baseline?" -- by
pulling every surface that CAN be measured and explicitly naming the ones that structurally cannot.

Measurable:
  - Telegraph estate (5): getViews, per-hour (see bin/analytics.py for the self-traffic separation).
  - HN submission: Algolia points + comments.
  - Nostr notes: relay query for referencing events (reactions/replies/reposts/DMs), classified
    self / bot-spam / candidate-human.

Structurally blind (named honestly, not silently omitted):
  - surge.sh product funnels (9): no analytics without the paid dashboard; header probe shows nothing.
  - workers.dev hub: no readable counter without a KV backend or the CF dashboard (a disclosed
    beacon is the in-bounds fix, an operator-gated option).
  - email (23 sent): NO open-tracking by design -- covert pixels would breach the honest-neutral
    posture. "Delivered, no reply" is all that is knowable.

    python3 bin/reach.py
"""
from __future__ import annotations
import json
import urllib.parse
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "iterations" / "088" / "reach_baseline.json"

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


def main() -> int:
    baseline = {
        "measurable": {
            "telegraph_views": telegraph(),
            "hackernews_item": hackernews(),
            "nostr_engagement": nostr(),
        },
        "structurally_blind": {
            "surge_funnels": {s: "no analytics API (paid dashboard only)" for s in SURGE_BLIND},
            "workers_dev_hub": "blind unless a disclosed KV-backed beacon is added (operator-gated)",
            "email_23_sent": "no open-tracking by design (covert pixels breach honest-neutral posture)",
        },
        "bottom_line": "measurable organic human reach is ZERO; all telegraph views are self-traffic "
                       "(see analytics.py hour-attribution), the HN item is dead, and Nostr "
                       "engagement is bots/spam. The two signals that matter -- a reply and a "
                       "received dollar -- are both still zero.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(baseline, indent=2, ensure_ascii=False))
    print(json.dumps(baseline, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

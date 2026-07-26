#!/usr/bin/env python3
"""Materiality classifier for after-close 8-K filings.

This is the step where the model is the product, so it is built to be AUDITABLE rather than clever:
every score is the sum of named, inspectable phrase hits, and every trade decision can be traced to
the exact sentences that produced it. A black-box score that cannot be interrogated is indistinguishable
from a random number when the verdict comes back.

Design commitments made BEFORE any return was computed (see run/EDGE_STRATEGY.md §4):

  * The phrase lists below encode what the LANGUAGE MEANS, not what made money. None of these weights
    has been fitted to a price series, and doing so later would be the alpha-theater failure the whole
    rail exists to block.
  * Long-only. Short signals are computed and recorded for the record, but are not traded: micro-cap
    borrow is unreliable, so short fills would be biased toward whatever happens to be easy to borrow
    — a selection effect that would masquerade as a result.
  * A filing must clear MIN_SCORE on positive evidence AND carry no hard-negative phrase. Ambiguity
    is a reason not to trade, not a reason to trade small.

Usage:
  python3 run/edge_classify.py --date 2026-07-23 --limit 20
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime

sys.path.insert(0, "run")
import edgar_events as E  # noqa: E402

# --------------------------------------------------------------------------------------------
# Positive evidence. Weighted by how unambiguous the phrase is, not by any observed return.
# "record" and "raises guidance" are strong because they are management's own superlative claims and
# are costly to make falsely; "increase" alone is weak because it appears in every routine filing.
# --------------------------------------------------------------------------------------------
POSITIVE = [
    # "record" is a trap: as a SUPERLATIVE ("record second quarter results") it is the strongest
    # positive in the corpus; as an accounting VERB ("expects to record a non-cash impairment charge
    # of $305 million") it precedes some of the worst news a filer publishes. Both forms appeared in
    # the same 18-filing sample. So: allow up to two intervening modifiers before the results-noun,
    # but require that "record" is NOT being used as an infinitive/verb.
    (3.0, r"(?<!to )(?<!will )(?<!expects to )\brecord\s+(?:\w+\s+){0,2}"
          r"(?:quarter|quarterly|revenue|revenues|net income|earnings|results|sales|profit)\b"),
    (3.0, r"\brais(?:es|ed|ing) (?:its |our |full[- ]year )?(?:guidance|outlook|forecast)\b"),
    (2.5, r"\bexceed(?:ed|s)? (?:analyst |consensus )?(?:expectations|estimates)\b"),
    (2.5, r"\bbeat (?:analyst |consensus )?(?:expectations|estimates)\b"),
    (2.0, r"\bincreas(?:es|ed|ing) (?:its |the |quarterly )?(?:cash )?dividend\b"),
    (2.0, r"\bshare repurchase program\b|\bstock buyback\b|\bauthoriz(?:ed|es) .{0,30}repurchase\b"),
    (2.0, r"\bdefinitive agreement to acquire\b|\bagreement to be acquired\b"),
    (1.5, r"\bstrong(?:er)? than (?:expected|anticipated)\b"),
    (1.5, r"\bFDA (?:approval|clearance)\b|\bgranted (?:approval|clearance)\b"),
    (1.5, r"\bnet income (?:of |was )?\$[\d.,]+ ?(?:million|billion)?,? up\b"),
    (1.0, r"\bupgrad(?:ed|es)\b|\bimprov(?:ed|ement) in\b"),
]

# --------------------------------------------------------------------------------------------
# Hard negatives. Presence of ANY of these vetoes a long regardless of positive score, because these
# are disclosures a company makes only when it must.
# --------------------------------------------------------------------------------------------
HARD_NEGATIVE = [
    r"\bnon-?reliance\b",                       # item 4.02 — prior financials cannot be trusted
    r"\brestat(?:e|ed|ement) .{0,40}financial statements\b",
    r"\bgoing concern\b",
    r"\bmaterial weakness\b",
    r"\bchapter 11\b|\bbankruptcy\b",
    r"\bnotice of (?:delisting|non-?compliance)\b|\bdelisting\b",
    r"\bdefault (?:under|on) .{0,30}(?:credit|note|indenture)\b",
    r"\bimpairment charge\b",
    r"\bresign(?:ed|ation) .{0,40}effective immediately\b",
    r"\bwithdraw(?:s|n|ing) .{0,20}guidance\b",
    r"\bSEC (?:investigation|subpoena)\b|\bformal investigation\b",
    r"\bclinical hold\b|\bfailed to meet .{0,30}endpoint\b",
]

# Item codes that carry decision-relevant news. Others (5.07 voting results, 9.01 exhibits) are noise.
INFORMATIVE_ITEMS = {"1.01", "2.01", "2.02", "2.05", "2.06", "5.02", "7.01", "8.01"}

MIN_SCORE = 3.0   # must clear on positive evidence alone; set from phrase weights, not from returns


def score_text(text: str) -> dict:
    """Return the score plus the exact evidence, so any decision can be audited after the fact."""
    t = " ".join((text or "").split())
    pos_hits, score = [], 0.0
    for w, pat in POSITIVE:
        for m in re.finditer(pat, t, re.I):
            score += w
            pos_hits.append({"weight": w, "phrase": m.group(0)[:70],
                             "context": t[max(0, m.start() - 60):m.start() + 90]})
            break  # count each distinct phrase once; repetition is emphasis, not new information
    neg_hits = []
    for pat in HARD_NEGATIVE:
        m = re.search(pat, t, re.I)
        if m:
            neg_hits.append({"phrase": m.group(0)[:70],
                             "context": t[max(0, m.start() - 60):m.start() + 90]})
    return {"score": round(score, 2), "positive": pos_hits, "hard_negative": neg_hits}


def decide(sc: dict) -> tuple[str, str]:
    if sc["hard_negative"]:
        return "SKIP", f"hard negative: {sc['hard_negative'][0]['phrase']}"
    if sc["score"] < MIN_SCORE:
        return "SKIP", f"score {sc['score']} below MIN_SCORE {MIN_SCORE}"
    return "LONG", f"score {sc['score']} on {len(sc['positive'])} positive phrases"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True, help="YYYY-MM-DD filing date")
    ap.add_argument("--limit", type=int, default=25)
    ap.add_argument("--json", default="")
    args = ap.parse_args()

    day = date.fromisoformat(args.date)
    rows = E.daily_8k(day)
    print(f"{args.date}: {len(rows)} 8-K filings mapped to listed tickers")

    out = []
    for r in rows[: args.limit]:
        try:
            ft = E.filing_text(r["url"])
        except Exception as exc:
            print(f"  {r['ticker']:<6} fetch failed: {str(exc)[:50]}")
            continue
        sc = score_text(ft["combined"])
        action, why = decide(sc)
        out.append({**r, "score": sc["score"], "action": action, "why": why,
                    "positive": sc["positive"], "hard_negative": sc["hard_negative"],
                    "sizes": ft["sizes"]})
        tag = "LONG " if action == "LONG" else "skip "
        print(f"  {tag}{r['ticker']:<6} score={sc['score']:<5} {r['company'][:34]:<36} {why[:52]}")

    longs = [o for o in out if o["action"] == "LONG"]
    print(f"\nclassified {len(out)} filings -> {len(longs)} LONG candidates "
          f"({100*len(longs)/max(1,len(out)):.0f}% selectivity)")
    if args.json:
        json.dump(out, open(args.json, "w"), indent=1)
        print(f"wrote {args.json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

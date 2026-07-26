#!/usr/bin/env python3
"""8-K material-event harvester — the data layer for an event-driven edge.

Why 8-K and not price history: the agent's only plausible advantage is reading text correctly and
fast, not charting. An 8-K is a discrete, timestamped, machine-readable disclosure of a material
corporate event, and EDGAR publishes `acceptanceDateTime` to the second — so "what was knowable, and
exactly when" is answerable without guesswork. That is the one property a latency/comprehension
hypothesis needs and that OHLC bars cannot give.

VERIFIED REACHABLE from this sandbox (iteration 194):
  data.sec.gov/submissions/CIK##########.json  -> 200, carries acceptanceDateTime + items
  www.sec.gov/Archives/edgar/daily-index/       -> 200
  efts.sec.gov/LATEST/search-index              -> 200
  query1.finance.yahoo.com/v8/finance/chart/    -> 200

SEC requires a declared User-Agent with contact details; requests are rate-limited to <10/sec and
this module sleeps between calls deliberately.

Usage:
  python3 run/edgar_events.py --tickers AAPL,MSFT --days 30
"""

from __future__ import annotations

import argparse
import json
import time
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

UA = {"User-Agent": "Miguel Ingram research miguel.ingram.work@gmail.com"}
SEC_THROTTLE = 0.15  # SEC asks for <10 requests/second; stay well under it.

# 8-K item codes worth separating. These are the disclosures where the TEXT carries information a
# price series does not already contain — which is where a reading edge could live, if anywhere.
ITEM_LABELS = {
    "1.01": "material definitive agreement",
    "1.02": "termination of material agreement",
    "2.01": "completion of acquisition/disposition",
    "2.02": "results of operations (earnings)",
    "2.05": "costs associated with exit/disposal",
    "3.01": "delisting / listing-rule failure",
    "4.01": "change in certifying accountant",
    "4.02": "non-reliance on previously issued financials",
    "5.02": "director/officer departure or appointment",
    "7.01": "regulation FD disclosure",
    "8.01": "other events",
}


def _get(url: str, timeout: int = 40):
    time.sleep(SEC_THROTTLE)
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout)


def ticker_to_cik() -> dict[str, str]:
    """SEC's own ticker->CIK map. Authoritative, so no symbol guessing."""
    data = json.load(_get("https://www.sec.gov/files/company_tickers.json"))
    out = {}
    for row in data.values():
        out[row["ticker"].upper()] = str(row["cik_str"]).zfill(10)
    return out


def filings_for(cik: str, forms=("8-K",), days: int = 30) -> list[dict]:
    """Recent filings with the acceptance timestamp intact."""
    d = json.load(_get(f"https://data.sec.gov/submissions/CIK{cik}.json"))
    rec = d["filings"]["recent"]
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    out = []
    n = len(rec.get("accessionNumber", []))
    for i in range(n):
        if rec["form"][i] not in forms:
            continue
        acc_dt = rec.get("acceptanceDateTime", [None] * n)[i]
        if not acc_dt:
            continue
        try:
            ts = datetime.fromisoformat(acc_dt.replace("Z", "+00:00"))
        except ValueError:
            continue
        if ts < cutoff:
            continue
        items = [c.strip() for c in (rec.get("items", [""] * n)[i] or "").split(",") if c.strip()]
        out.append(
            {
                "cik": cik,
                "company": d.get("name"),
                "form": rec["form"][i],
                "accession": rec["accessionNumber"][i],
                "filed": rec["filingDate"][i],
                # The whole point: WHEN it became public, to the second.
                "accepted_utc": ts.isoformat(),
                # Filed after 20:00 UTC is after the 16:00 ET close — the market could not react
                # until the next session, which is the cleanest event-study window available.
                "after_close": ts.hour >= 20,
                "items": items,
                "item_labels": [ITEM_LABELS.get(c, c) for c in items],
            }
        )
    return out


def daily_bars(ticker: str, days: int = 90) -> list[dict]:
    """Daily OHLC from ALPACA, not yfinance.

    CRITICAL (operator, iteration 201): yfinance is survivorship-biased — companies that delisted or
    went to zero are simply gone from it. This strategy's entire thesis is the neglected long tail,
    which is exactly where small companies fail and delist, so a yfinance backtest makes every failure
    invisible and the edge looks real when it is only the survivors talking. Alpaca's bars carry
    delisted names, so they are the honest source here. Requires the paper keys in the environment.
    """
    import os
    h = {"APCA-API-KEY-ID": os.environ["ALPACA_PAPER_KEY_ID"],
         "APCA-API-SECRET-KEY": os.environ["ALPACA_PAPER_SECRET_KEY"]}
    from datetime import date as _date
    start = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%d")
    url = (f"https://data.alpaca.markets/v2/stocks/{ticker}/bars"
           f"?timeframe=1Day&start={start}&adjustment=all&limit=1000")
    req = urllib.request.Request(url, headers=h)
    d = json.load(urllib.request.urlopen(req, timeout=40))
    bars = []
    for b in d.get("bars") or []:
        bars.append({"date": b["t"][:10], "open": b["o"], "close": b["c"],
                     "high": b["h"], "low": b["l"], "volume": b.get("v", 0)})
    return bars


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tickers", default="AAPL,MSFT,NVDA,JPM,XOM")
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--json", default="")
    args = ap.parse_args()

    tickers = [t.strip().upper() for t in args.tickers.split(",") if t.strip()]
    cmap = ticker_to_cik()
    print(f"ticker->CIK map: {len(cmap)} symbols")

    events = []
    for t in tickers:
        cik = cmap.get(t)
        if not cik:
            print(f"  {t}: no CIK")
            continue
        evs = filings_for(cik, days=args.days)
        for e in evs:
            e["ticker"] = t
        events.extend(evs)
        print(f"  {t}: {len(evs)} 8-K in {args.days}d")

    events.sort(key=lambda e: e["accepted_utc"], reverse=True)
    print(f"\ntotal 8-K events: {len(events)}  "
          f"({sum(1 for e in events if e['after_close'])} filed after the close)")
    for e in events[:12]:
        print(f"  {e['accepted_utc'][:16]}  {e['ticker']:<5} "
              f"{'AFTER-CLOSE' if e['after_close'] else 'intraday   '}  "
              f"{','.join(e['items']) or '-':<12} {'; '.join(e['item_labels'])[:58]}")

    if args.json:
        json.dump(events, open(args.json, "w"), indent=1)
        print(f"\nwrote {args.json}")
    return 0



# ---------------------------------------------------------------------------
# Market-wide daily index — the real universe.
#
# A watchlist cannot resolve: 8 mega-caps produced 19 events in 60 days. The daily index carries
# every 8-K filed market-wide (measured 166-370/session, mean 258), of which ~86% map to a listed
# ticker. Format note learned the hard way: form.idx is FIXED-WIDTH with a YYYYMMDD date, so a
# hyphenated-date regex silently matches nothing. Split on runs of 2+ spaces.
# ---------------------------------------------------------------------------

def cik_to_ticker() -> dict[int, str]:
    data = json.load(_get("https://www.sec.gov/files/company_tickers.json"))
    out: dict[int, str] = {}
    for row in data.values():
        out.setdefault(int(row["cik_str"]), row["ticker"].upper())
    return out


def daily_8k(day, only_listed: bool = True) -> list[dict]:
    """Every 8-K filed on `day` (a date), mapped to tickers where one exists."""
    import re as _re
    q = (day.month - 1) // 3 + 1
    url = (f"https://www.sec.gov/Archives/edgar/daily-index/{day.year}/QTR{q}/"
           f"form.{day.strftime('%Y%m%d')}.idx")
    try:
        txt = _get(url).read().decode("utf-8", "replace")
    except Exception as exc:
        print(f"  ! no daily index for {day}: {exc}")
        return []
    cmap = cik_to_ticker()
    out = []
    for line in txt.splitlines():
        if not line.startswith("8-K"):
            continue
        parts = [p for p in _re.split(r"\s{2,}", line.strip()) if p]
        if len(parts) < 5 or not parts[2].isdigit():
            continue
        cik = int(parts[2])
        ticker = cmap.get(cik)
        if only_listed and not ticker:
            continue
        out.append({
            "form": parts[0], "company": parts[1], "cik": cik, "ticker": ticker,
            "filed": parts[3], "path": parts[4],
            "url": f"https://www.sec.gov/Archives/{parts[4]}",
        })
    return out


# ---------------------------------------------------------------------------
# Filing text extraction — the classifier's actual input.
#
# DESIGN CORRECTION (iteration 196): a body-only extractor reads the cover page and MISSES THE NEWS.
# A full 8-K submission is ~920KB because every exhibit is inline as its own <DOCUMENT> block. The
# 8-K primary document is tiny (3.2KB here) and for an item 2.02 earnings filing it says only that a
# press release "was furnished" — the numbers that move the stock live in the EX-99.1 exhibit
# (37KB of text: "Record Second Quarter Results", net income +27.40% YoY, dividend raised).
# So the classifier gets BOTH: the 8-K body for what is being disclosed, the EX-99 exhibits for what
# it actually says. Exhibits that are schemas, labels, or images are dropped.
# ---------------------------------------------------------------------------

_TAG = __import__("re").compile(r"<[^>]+>")
_ENT = __import__("re").compile(r"&#\d+;|&[a-z]+;")

_SKIP_EXHIBIT = ("EX-101", "EX-32", "GRAPHIC", "ZIP", "EXCEL", "XML", "JSON")


def _plain(block: str) -> str:
    t = _TAG.sub(" ", block)
    t = _ENT.sub(" ", t)
    return " ".join(t.split())


def filing_text(url: str, max_chars: int = 24000) -> dict:
    """Fetch a filing and return the classifier's input.

    Returns {body, exhibits, combined, sizes}. `combined` is capped because a classifier does not
    need 37KB of tabular back-matter to judge materiality — the lead paragraphs carry it.
    """
    import re as _re
    raw = _get(url, timeout=60).read().decode("utf-8", "replace")
    body_parts, ex_parts = [], []
    for doc in _re.findall(r"<DOCUMENT>(.*?)</DOCUMENT>", raw, _re.S):
        m = _re.search(r"<TYPE>([^\n<]+)", doc)
        typ = (m.group(1).strip() if m else "?").upper()
        if typ.startswith("8-K"):
            body_parts.append(_plain(doc))
        elif typ.startswith("EX-99"):
            ex_parts.append(_plain(doc))
        elif any(typ.startswith(s) for s in _SKIP_EXHIBIT):
            continue
    body = " ".join(body_parts)
    exhibits = " ".join(ex_parts)
    combined = (body[:6000] + "\n\n--- EXHIBIT ---\n\n" + exhibits[: max_chars - 6000]).strip()
    return {
        "body": body,
        "exhibits": exhibits,
        "combined": combined,
        "sizes": {"raw": len(raw), "body": len(body), "exhibits": len(exhibits),
                  "combined": len(combined)},
    }


if __name__ == "__main__":
    raise SystemExit(main())

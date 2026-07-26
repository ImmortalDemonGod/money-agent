#!/usr/bin/env python3
"""Historical validation of 8k-coverage-drift-v1.

WHY THIS IS SAFE TO RUN NOW AND WOULD NOT HAVE BEEN BEFORE:
the bar (1.0pp excess vs SPY), fill minimum, drawdown cap and deadline were committed and pushed at
2026-07-26T06:56Z, before any order existed. Nothing this script computes can move them — the freeze
is public and timestamped. Running a backtest BEFORE registering would have been the alpha-theater
failure the rail exists to catch; running one after is just finding out whether the bet is any good.

The verdict still comes from the broker's forward books. This measures the PRIOR, not the result:
  * does the classifier's LONG set behave differently from the filings it rejects?
  * what is the real selectivity over a full day, not a 14-filing sample?
  * is the per-event drift anywhere near the 0.3% the sizing assumed?

An honest negative here is worth more than a live week of hope: it would say, before any capital is
deployed, that the edge is not there.

Event window: filing accepted after the 16:00 ET close on day D -> buy at the open of D+1, sell at the
close of D+1. Exactly what the executor does live.
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
import time
from datetime import date, timedelta

sys.path.insert(0, "run")
import edgar_events as E     # noqa: E402
import edge_classify as C    # noqa: E402

_bars_cache: dict[str, list[dict]] = {}


def bars(ticker: str) -> list[dict]:
    if ticker not in _bars_cache:
        try:
            _bars_cache[ticker] = E.daily_bars(ticker, days=180)
        except Exception:
            _bars_cache[ticker] = []
        time.sleep(0.05)
    return _bars_cache[ticker]


# Round-trip slippage in bps for a thin small cap, applied as a haircut. The long tail is neglected
# BECAUSE it is illiquid: a paper account fills at the print, a real account crosses a wide spread on
# entry AND exit. 50 bps round-trip is a deliberately mild assumption for names of this size — real
# micro-cap costs run higher — and the point is to see whether the edge survives even a mild one.
SLIPPAGE_BPS = 50.0

def next_session_return(ticker: str, filing_day: str) -> float | None:
    """Open-to-close return of the first session after the filing day, net of slippage.

    Buy at the open + half the round-trip cost, sell at the close - half. On a $100k paper account the
    fill is frictionless; this haircut is what makes the number mean the MARKET rather than the
    simulator, which is the operator's second hole."""
    b = bars(ticker)
    for row in b:
        if row["date"] > filing_day:
            o, c = row["open"], row["close"]
            if not (o and c and o > 0):
                return None
            gross = (c - o) / o * 100.0
            return gross - SLIPPAGE_BPS / 100.0   # subtract full round-trip in percentage points
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=5, help="trading days back to sample")
    ap.add_argument("--start", default="2026-07-24",
                    help="most-recent filing day to sample back from; use an OLDER date so forward "
                         "prices exist for multi-day holds (recent events have no forward sessions yet)")
    ap.add_argument("--per-day", type=int, default=40, help="filings to classify per day")
    ap.add_argument("--json", default="")
    args = ap.parse_args()

    # Recent completed sessions, most recent first.
    days, d = [], date.fromisoformat(args.start)
    while len(days) < args.days:
        if d.weekday() < 5:
            days.append(d)
        d -= timedelta(days=1)

    longs, rejects = [], []
    for day in days:
        rows = E.daily_8k(day)
        print(f"\n{day}: {len(rows)} listed 8-K filings; classifying {min(args.per_day, len(rows))}")
        n_long = 0
        for r in rows[: args.per_day]:
            try:
                ft = E.filing_text(r["url"])
            except Exception:
                continue
            sc = C.score_text(ft["combined"])
            action, _ = C.decide(sc)
            ret = next_session_return(r["ticker"], str(day))
            if ret is None:
                continue
            rec = {"date": str(day), "ticker": r["ticker"], "score": sc["score"],
                   "ret_pct": round(ret, 3), "action": action,
                   "evidence": [h["phrase"] for h in sc["positive"]][:3]}
            (longs if action == "LONG" else rejects).append(rec)
            if action == "LONG":
                n_long += 1
                print(f"   LONG {r['ticker']:<6} score={sc['score']:<5} next-session {ret:+.2f}%")
        print(f"   -> {n_long} LONG of {min(args.per_day, len(rows))} classified")

    print("\n" + "=" * 68)
    if not longs:
        print("NO LONG SIGNALS in the sample — nothing to evaluate.")
        return 0

    lr = [x["ret_pct"] for x in longs]
    rr = [x["ret_pct"] for x in rejects]
    mean_l = statistics.mean(lr)
    print(f"LONG signals      : n={len(lr):<4} mean {mean_l:+.3f}%  median "
          f"{statistics.median(lr):+.3f}%  sd {statistics.pstdev(lr) if len(lr)>1 else 0:.3f}")
    if rr:
        mean_r = statistics.mean(rr)
        print(f"REJECTED filings  : n={len(rr):<4} mean {mean_r:+.3f}%  median "
              f"{statistics.median(rr):+.3f}%")
        print(f"SPREAD (long - rejected): {mean_l - mean_r:+.3f} percentage points")
    win = sum(1 for x in lr if x > 0) / len(lr) * 100
    print(f"win rate          : {win:.0f}%   best {max(lr):+.2f}%   worst {min(lr):+.2f}%")

    # The sizing assumed 0.3% per event. State plainly whether that survives.
    print(f"\nsizing assumed per-event drift of +0.300%; measured {mean_l:+.3f}%")
    if len(lr) < 20:
        print("SAMPLE IS TOO THIN to conclude anything — this is a prior, not a verdict.")
    if mean_l <= 0:
        print("NEGATIVE MEAN: the hypothesis is not supported by this sample.")

    if args.json:
        json.dump({"longs": longs, "rejects": rejects}, open(args.json, "w"), indent=1)
        print(f"wrote {args.json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

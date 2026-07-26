#!/usr/bin/env python3
"""Execution for short-vol-vrp-v1 — the registered volatility-risk-premium edge.

Sells a DEFINED-RISK SPY put-credit-spread (sell a ~5%-OTM put, buy a ~8%-OTM put) to harvest the
volatility risk premium. Defined-risk by construction: the long put caps the loss at the spread
width, so a crash cannot produce an unbounded loss — the honest guardrail for a negative-skew
strategy.

Verified against the paper account (iteration 223): the mleg order path accepts + cancels cleanly.
Dry-run is the default; --live is required to actually submit.

Reads risk parameters from EDGE_REGISTRATION.md so the executor cannot drift from the frozen bet:
MAX_DRAWDOWN_USD gates whether we trade at all.

Usage:
  python3 run/vrp_execute.py status
  python3 run/vrp_execute.py sell            # dry-run a new credit spread
  python3 run/vrp_execute.py sell --live      # actually submit
  python3 run/vrp_execute.py close --live     # flatten option positions
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
REG = REPO / "EDGE_REGISTRATION.md"

RISK_PER_SPREAD_USD = 3000.0   # small: risk-at-stake per cycle vs $100k equity; survives a crash cycle
# Strike selection (iteration 225, after fixing the delta solver): a ~10-delta short (~6.5% OTM) is
# best on BOTH risk-adjusted return (Sharpe 0.95 vs 0.50-0.74 for 15-30 delta) AND worst case
# (-47% vs -87%), because for a capped-risk negative-skew strategy giving up a little premium to
# halve the tail is the right trade -- the tail is what breaches the drawdown cap. Execution detail
# within the frozen mechanism; does not touch bar/cap/benchmark.
SHORT_OTM = 0.935              # short put ~6.5% below spot (~10-delta)
LONG_OTM = 0.905               # long put ~9.5% below spot (3% width, defines the risk)
MIN_DTE, MAX_DTE = 5, 10       # target ~weekly expiry
MIN_VIX = 16.0                 # do NOT sell vol into thin premium: VIX<16 backtested NEGATIVE
                               # (-0.70%/mo); the edge lives at VIX>=~18-20 (Sharpe 1.66 at >=20)


def registration() -> dict:
    out = {}
    for line in REG.read_text().splitlines():
        if ":" in line and line.split(":", 1)[0].isupper():
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip()
    return out


class Broker:
    def __init__(self):
        self.tbase = (os.environ.get("ALPACA_PAPER_BASE")
                      or os.environ.get("APCA_API_BASE_URL")
                      or "https://paper-api.alpaca.markets").rstrip("/")
        self.h = {
            "APCA-API-KEY-ID": os.environ["ALPACA_PAPER_KEY_ID"],
            "APCA-API-SECRET-KEY": os.environ["ALPACA_PAPER_SECRET_KEY"],
            "Content-Type": "application/json",
        }

    def _req(self, method, url, body=None):
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(url, data=data, headers=self.h, method=method)
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                t = r.read().decode()
                return json.loads(t) if t.strip() else {}
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"{e.code} {e.read().decode()[:200]}") from None

    def account(self):   return self._req("GET", self.tbase + "/v2/account")
    def clock(self):     return self._req("GET", self.tbase + "/v2/clock")
    def positions(self): return self._req("GET", self.tbase + "/v2/positions")
    def orders(self):    return self._req("GET", self.tbase + "/v2/orders?status=all&limit=200")

    def spy(self) -> float:
        d = self._req("GET", "https://data.alpaca.markets/v2/stocks/SPY/trades/latest")
        return float(d["trade"]["p"])

    def vix(self) -> float:
        # VIX from Yahoo (Alpaca has no index feed). The edge is selling vol only when it is EXPENSIVE.
        req = urllib.request.Request(
            "https://query1.finance.yahoo.com/v8/finance/chart/%5EVIX?range=5d&interval=1d",
            headers={"User-Agent": "Mozilla/5.0"})
        d = json.load(urllib.request.urlopen(req, timeout=20))
        cl = [c for c in d["chart"]["result"][0]["indicators"]["quote"][0]["close"] if c]
        return float(cl[-1])

    def put_contracts(self):
        d = self._req("GET", self.tbase +
                      "/v2/options/contracts?underlying_symbols=SPY&type=put&limit=500")
        return d.get("option_contracts", [])

    def submit_credit_spread(self, short_sym, long_sym, qty, limit_credit):
        body = {
            "order_class": "mleg", "qty": str(qty), "type": "limit", "time_in_force": "day",
            "limit_price": f"{limit_credit:.2f}",
            "legs": [
                {"symbol": short_sym, "ratio_qty": "1", "side": "sell", "position_intent": "sell_to_open"},
                {"symbol": long_sym, "ratio_qty": "1", "side": "buy", "position_intent": "buy_to_open"},
            ],
        }
        return self._req("POST", self.tbase + "/v2/orders", body)

    def close_all_options(self):
        # close any open option positions (defined-risk legs) at market
        out = []
        for p in self.positions():
            if p.get("asset_class") == "us_option":
                side = "buy" if float(p["qty"]) < 0 else "sell"
                out.append(self._req("POST", self.tbase + "/v2/orders", {
                    "symbol": p["symbol"], "qty": str(abs(int(float(p["qty"])))),
                    "side": side, "type": "market", "time_in_force": "day"}))
        return out


def pick_legs(bk: Broker):
    spot = bk.spy()
    cons = bk.put_contracts()
    today = datetime.now(timezone.utc).date()
    dte_ok = [c for c in cons
              if MIN_DTE <= (date.fromisoformat(c["expiration_date"]) - today).days <= MAX_DTE
              and c.get("tradable")]
    if not dte_ok:
        dte_ok = [c for c in cons if c.get("tradable")]
    exp = min((c["expiration_date"] for c in dte_ok),
              key=lambda e: abs((date.fromisoformat(e) - today).days - 7))
    leg = [c for c in dte_ok if c["expiration_date"] == exp]
    short = min(leg, key=lambda c: abs(float(c["strike_price"]) - spot * SHORT_OTM))
    long = min(leg, key=lambda c: abs(float(c["strike_price"]) - spot * LONG_OTM))
    return spot, exp, short, long


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["status", "sell", "close"])
    ap.add_argument("--live", action="store_true")
    args = ap.parse_args()
    bk = Broker()
    reg = registration()

    if args.cmd == "status":
        a = bk.account(); c = bk.clock()
        eq = float(a["equity"])
        opts = [p for p in bk.positions() if p.get("asset_class") == "us_option"]
        fills = len([o for o in bk.orders() if o.get("filled_at")])
        print(f"equity ${eq:,.2f}  market_open={c['is_open']}  option_positions={len(opts)}  "
              f"fills={fills}/{reg.get('MIN_FILLED_ORDERS')}")
        for p in opts:
            print(f"  {p['symbol']} qty={p['qty']} upl={float(p.get('unrealized_pl',0)):+,.2f}")
        return 0

    if args.cmd == "sell":
        # drawdown gate: registration says a breach is FALSIFIED, so do not open new risk past it
        a = bk.account(); eq = float(a["equity"]); last = float(a["last_equity"])
        cap = float(reg["MAX_DRAWDOWN_USD"])
        if last - eq >= cap:
            print(f"REFUSING: drawdown ${last-eq:,.0f} >= cap ${cap:,.0f} — FALSIFIED, no new risk.")
            return 2
        vix = bk.vix()
        if vix < MIN_VIX:
            print(f"SKIP: VIX {vix:.1f} < {MIN_VIX} — premium too thin (backtest negative here). "
                  f"Wait for vol to richen; do not over-trade into a losing regime.")
            return 0
        spot, exp, short, long = pick_legs(bk)
        print(f"VIX {vix:.1f} (>= {MIN_VIX}, selling vol only when it is expensive)")
        width = abs(float(short["strike_price"]) - float(long["strike_price"]))
        qty = max(1, int(RISK_PER_SPREAD_USD / (width * 100)))
        # limit credit: a touch below mid so it can fill; conservative here
        limit = round(width * 0.15, 2)  # aim to collect ~15% of width as credit
        print(f"SPY {spot:.2f}  exp {exp}  SHORT {short['strike_price']}P / LONG {long['strike_price']}P "
              f"width={width:.0f} qty={qty} target_credit~${limit:.2f} risk~${qty*width*100:,.0f}")
        if not args.live:
            print("  DRY-RUN — pass --live to submit.")
            return 0
        try:
            o = bk.submit_credit_spread(short["symbol"], long["symbol"], qty, limit)
            print(f"  SUBMITTED mleg id={o['id'][:8]} status={o['status']}")
        except RuntimeError as e:
            print(f"  FAIL {e}")
        return 0

    if args.cmd == "close":
        if not args.live:
            opts = [p for p in bk.positions() if p.get("asset_class") == "us_option"]
            print(f"DRY: would close {len(opts)} option legs"); return 0
        print("closing:", bk.close_all_options())
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

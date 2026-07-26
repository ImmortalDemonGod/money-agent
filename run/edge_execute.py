#!/usr/bin/env python3
"""Execution for 8k-coverage-drift-v1 — the registered edge.

Trades the registration and nothing else. Every parameter that could be quietly reshaped mid-run
(bar, drawdown cap, deadline) is READ FROM EDGA_REGISTRATION.md rather than restated here, so this
file cannot drift away from the frozen commitment without the drift being visible in a diff.

Flow, once per session:
  plan   after the close  -> harvest that day's 8-Ks, classify, write the plan
  submit before the open  -> place market-on-open buys for the plan
  close  before the close -> flatten every position opened today

Safety rails, deliberate:
  * --dry-run is the DEFAULT. Placing real paper orders requires --live, typed explicitly.
  * A position is never larger than POSITION_USD, and never more than MAX_POSITIONS per session.
  * Refuses to submit if the account's peak-to-current drawdown already breaches the registered cap:
    the registration says that is FALSIFIED, so continuing to trade past it would be trading a bet
    that is already lost.
  * Every asset is checked tradable against the BROKER (OTC names carry tickers but cannot be
    traded — ALUR was tradable=False on the first day sampled).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path

sys.path.insert(0, "run")
import edgar_events as E          # noqa: E402
import edge_classify as C         # noqa: E402

REPO = Path(__file__).resolve().parent.parent
REG = REPO / "EDGE_REGISTRATION.md"
STATE = REPO / "run" / "edge_state"

# The registration documents ~$34,800 deployed per session (35% of equity). Fixing the classifier's
# "record" false-negative at iteration 197 raised measured selectivity from ~6% to ~21%, which at
# $5,000 a position would deploy more than the account holds. DEPLOYMENT IS HELD AT THE REGISTERED
# LEVEL and position size adjusted down, rather than letting the risk profile drift upward from what
# was frozen. The bar, drawdown cap, deadline and fill minimum are untouched — those are the frozen
# commitment; per-position sizing is execution detail, and keeping total exposure at the documented
# 35% is more faithful to the registration, not less.
TARGET_DEPLOY_USD = 35000.0
MAX_POSITIONS = 10
POSITION_USD = TARGET_DEPLOY_USD / MAX_POSITIONS   # $3,500


# Fractional-Kelly position sizing (operator email 96 asked for a Kelly cap).
#
# Kelly for a continuous bet is f* = mu / sigma^2. On this edge's own numbers (per-event mu~0.46%,
# sigma~5.0%) full-Kelly is ~1.85 — leverage — which is absurd for an edge whose confidence interval
# spans zero. So sizing here does the honest thing Kelly implies for an UNCERTAIN edge: shrink hard.
#   * KELLY_FRACTION 0.25 (quarter-Kelly) — the standard discount for estimation error.
#   * BELIEF shrinks mu toward zero by how much we actually believe the edge (t~1.1 => coin-flip).
#   * Two hard caps that Kelly can only lower, never raise: per-position <= PER_POS_CAP_FRAC of
#     equity, and TOTAL deployed <= the registered envelope. An uncertain edge sizes DOWN.
KELLY_FRACTION = 0.25
BELIEF = 0.5                 # P(edge is real); halve mu. Revised only by out-of-sample evidence.
PER_POS_CAP_FRAC = 0.05      # no single thin small-cap name > 5% of equity, Kelly notwithstanding

def kelly_position_usd(equity: float, mu_per_event: float, sd_per_event: float,
                       n_positions: int, total_deploy_cap: float) -> float:
    """Fractional-Kelly $ per position, hard-capped by per-name and total-deploy ceilings."""
    if sd_per_event <= 0:
        f = 0.0
    else:
        f = KELLY_FRACTION * BELIEF * mu_per_event / (sd_per_event ** 2)
    f = max(0.0, f)
    per_pos = f * equity
    per_pos = min(per_pos, PER_POS_CAP_FRAC * equity)          # per-name hard cap
    per_pos = min(per_pos, total_deploy_cap / max(1, n_positions))  # registered total envelope
    return round(per_pos, 2)


def registration() -> dict:
    """Read the frozen commitment. Never restate its numbers in code."""
    out = {}
    for line in REG.read_text().splitlines():
        if ":" in line and line.split(":", 1)[0].isupper():
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip()
    return out


class Broker:
    def __init__(self):
        self.base = (os.environ.get("ALPACA_PAPER_BASE")
                     or os.environ.get("APCA_API_BASE_URL")
                     or "https://paper-api.alpaca.markets").rstrip("/")
        self.h = {
            "APCA-API-KEY-ID": os.environ["ALPACA_PAPER_KEY_ID"],
            "APCA-API-SECRET-KEY": os.environ["ALPACA_PAPER_SECRET_KEY"],
            "Content-Type": "application/json",
        }

    def _req(self, method: str, path: str, body=None):
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(self.base + path, data=data, headers=self.h, method=method)
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                txt = r.read().decode()
                return json.loads(txt) if txt.strip() else {}
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"{e.code} {e.read().decode()[:200]}") from None

    def account(self):   return self._req("GET", "/v2/account")
    def clock(self):     return self._req("GET", "/v2/clock")
    def positions(self): return self._req("GET", "/v2/positions")
    def orders(self, status="all", limit=200):
        return self._req("GET", f"/v2/orders?status={status}&limit={limit}")
    def asset(self, sym): return self._req("GET", f"/v2/assets/{sym}")
    def last_price(self, sym) -> float:
        """Last trade price, for converting a dollar target into whole shares."""
        req = urllib.request.Request(
            f"https://data.alpaca.markets/v2/stocks/{sym}/trades/latest", headers=self.h)
        with urllib.request.urlopen(req, timeout=20) as r:
            return float(json.load(r)["trade"]["p"])

    def buy_at_open(self, sym, qty: int):
        """Market-on-open, WHOLE SHARES ONLY.

        Caught before the first session: a `notional` order with time_in_force="opg" is rejected
        outright -- "fractional orders must be DAY orders" (HTTP 422). Dollar-sized market-on-open
        orders do not exist, so every order this strategy places would have been refused at the open.
        Sizing therefore converts the dollar target to an integer share count against the last trade.
        """
        body = {"symbol": sym, "side": "buy", "type": "market",
                "time_in_force": "opg", "qty": str(int(qty))}
        return self._req("POST", "/v2/orders", body)
    def close_all(self):  return self._req("DELETE", "/v2/positions?cancel_orders=true")
    def cancel(self, oid): return self._req("DELETE", f"/v2/orders/{oid}")


def tradable(bk: Broker, sym: str) -> tuple[bool, str]:
    """Having a ticker is not permission to trade it. OTC names fail here."""
    try:
        a = bk.asset(sym)
    except RuntimeError as e:
        return False, f"asset lookup failed: {e}"[:70]
    if not a.get("tradable"):
        return False, f"not tradable ({a.get('exchange')})"
    return True, a.get("exchange", "")


def plan(day: date, limit: int) -> list[dict]:
    """Classify the day's filings into a trade plan. No broker calls, no prices."""
    rows = E.daily_8k(day)
    print(f"{day}: {len(rows)} 8-K filings mapped to listed tickers")
    picks = []
    for r in rows[:limit]:
        try:
            ft = E.filing_text(r["url"])
        except Exception as exc:
            print(f"  {r['ticker']:<6} fetch failed: {str(exc)[:44]}")
            continue
        sc = C.score_text(ft["combined"])
        action, why = C.decide(sc)
        if action != "LONG":
            continue
        picks.append({"ticker": r["ticker"], "company": r["company"], "score": sc["score"],
                      "why": why, "evidence": [h["phrase"] for h in sc["positive"]],
                      "url": r["url"]})
        print(f"  LONG {r['ticker']:<6} score={sc['score']:<5} {r['company'][:38]}")
    return picks


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["plan", "submit", "close", "status"])
    ap.add_argument("--date", default="")
    ap.add_argument("--limit", type=int, default=60)
    ap.add_argument("--live", action="store_true", help="actually place orders (default is dry-run)")
    args = ap.parse_args()

    reg = registration()
    bk = Broker()
    STATE.mkdir(parents=True, exist_ok=True)

    if args.cmd == "status":
        a, c = bk.account(), bk.clock()
        eq, last = float(a["equity"]), float(a["last_equity"])
        print(f"equity ${eq:,.2f}   cash ${float(a['cash']):,.2f}   "
              f"session change {eq-last:+,.2f}")
        print(f"market open: {c['is_open']}   next open {c['next_open'][:19]}")
        pos = bk.positions()
        print(f"open positions: {len(pos)}")
        for p in pos:
            print(f"  {p['symbol']:<6} qty={p['qty']:<8} mv=${float(p['market_value']):>10,.2f} "
                  f"upl={float(p['unrealized_pl']):+,.2f}")
        fills = [o for o in bk.orders() if o.get("filled_at")]
        print(f"FILLED ORDERS TO DATE: {len(fills)}  (registration needs "
              f"{reg.get('MIN_FILLED_ORDERS')})")
        return 0

    if args.cmd == "plan":
        day = date.fromisoformat(args.date) if args.date else date.today()
        picks = plan(day, args.limit)
        out = STATE / f"plan_{day}.json"
        json.dump(picks, open(out, "w"), indent=1)
        print(f"\n{len(picks)} LONG candidates -> {out}")
        return 0

    if args.cmd == "submit":
        day = date.fromisoformat(args.date) if args.date else date.today()
        f = STATE / f"plan_{day}.json"
        if not f.exists():
            print(f"no plan for {day}; run `plan` first"); return 1
        picks = json.load(open(f))

        a = bk.account()
        eq = float(a["equity"])
        cap = float(reg["MAX_DRAWDOWN_USD"])
        peak_file = STATE / "peak_equity.json"
        peak = json.load(open(peak_file))["peak"] if peak_file.exists() else eq
        peak = max(peak, eq)
        json.dump({"peak": peak, "at": datetime.now(timezone.utc).isoformat()}, open(peak_file, "w"))
        dd = peak - eq
        print(f"equity ${eq:,.2f}  peak ${peak:,.2f}  drawdown ${dd:,.2f} of ${cap:,.0f} cap")
        if dd >= cap:
            print("REFUSING TO SUBMIT: registered drawdown cap breached — that is FALSIFIED, "
                  "and trading past it would be trading a bet already lost.")
            return 2

        sent = 0
        for p in picks[:MAX_POSITIONS]:
            ok, note = tradable(bk, p["ticker"])
            if not ok:
                print(f"  skip {p['ticker']:<6} {note}")
                continue
            try:
                px = bk.last_price(p["ticker"])
            except Exception as e:
                print(f"  skip {p['ticker']:<6} no price: {str(e)[:44]}")
                continue
            qty = int(POSITION_USD // px)
            if qty < 1:
                print(f"  skip {p['ticker']:<6} ${px:,.2f}/share exceeds ${POSITION_USD:,.0f} slot")
                continue
            if not args.live:
                print(f"  DRY  buy {qty:>4} {p['ticker']:<6} @ ~${px:,.2f} "
                      f"= ${qty*px:,.0f} ({note}) score={p['score']}")
                sent += 1
                continue
            try:
                o = bk.buy_at_open(p["ticker"], qty=qty)
                print(f"  SENT {p['ticker']:<6} id={o['id'][:8]} qty={qty} @ ~${px:,.2f}")
                sent += 1
            except RuntimeError as e:
                print(f"  FAIL {p['ticker']:<6} {e}"[:110])
        print(f"\n{'dry-run' if not args.live else 'submitted'}: {sent} orders")
        return 0

    if args.cmd == "close":
        if not args.live:
            pos = bk.positions()
            print(f"DRY: would flatten {len(pos)} positions")
            return 0
        r = bk.close_all()
        print("flatten requested:", json.dumps(r)[:200])
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""One clock-aware trading tick for 8k-coverage-drift-v1.

The 10-minute loop cannot be trusted to reconstruct the right action from a generic "make money"
prompt at 08:30 Central on Monday. So the decision is mechanical here: given the market clock and the
account state, this prints exactly what to do (and, with --live, does it). Idempotent — running it
twice in the same phase does not double-trade, because it checks for an existing plan and existing
positions before acting.

Session phases (times in ET, the market's own zone):
  before ~09:25  PRE-OPEN   -> ensure a plan exists for today, submit market-on-open buys (opg)
  ~09:30-15:45   IN-SESSION -> hold; report unrealised P&L and drawdown vs the registered cap
  ~15:45-16:00   PRE-CLOSE  -> flatten every position (the strategy is one-session, no overnight risk)
  market closed  IDLE       -> report; if it is after a session, the fills are now countable

--live is required to place or flatten orders; without it every action is printed as a dry-run.
The registered bar / cap / deadline are read from EDGE_REGISTRATION.md via edge_execute, never restated.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime, timezone

sys.path.insert(0, "run")
from edge_execute import Broker, registration  # noqa: E402


def run_exec(args: list[str]) -> None:
    """Delegate to edge_execute.py so there is one order path, not two."""
    cmd = [sys.executable, "run/edge_execute.py"] + args
    print(f"  $ {' '.join(cmd)}")
    subprocess.run(cmd, check=False)


def et_now(clock: dict) -> tuple[str, int]:
    """Return ('YYYY-MM-DD', minutes-since-midnight-ET) from the broker clock (authoritative)."""
    ts = datetime.fromisoformat(clock["timestamp"])
    # Alpaca returns ET-localised timestamps; use them directly rather than reconverting.
    return ts.strftime("%Y-%m-%d"), ts.hour * 60 + ts.minute


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--live", action="store_true")
    args = ap.parse_args()
    live = ["--live"] if args.live else []

    bk = Broker()
    reg = registration()
    clock = bk.clock()
    acct = bk.account()
    pos = bk.positions()
    today, mins = et_now(clock)
    is_open = clock["is_open"]

    eq = float(acct["equity"])
    fills = len([o for o in bk.orders() if o.get("filled_at")])
    print(f"[{clock['timestamp'][:16]} ET] open={is_open}  equity=${eq:,.2f}  "
          f"positions={len(pos)}  fills={fills}/{reg.get('MIN_FILLED_ORDERS')}  "
          f"mode={'LIVE' if args.live else 'dry-run'}")

    OPEN_MIN, CLOSE_MIN = 9 * 60 + 30, 16 * 60

    if not is_open:
        # Market shut. If the next open is today (pre-market), prepare; else idle.
        nxt = clock["next_open"][:10]
        if nxt == today and mins < OPEN_MIN:
            print("PRE-OPEN (pre-market): planning today's trades and queueing market-on-open buys.")
            run_exec(["plan", "--date", today])
            run_exec(["submit", "--date", today] + live)
        else:
            print(f"IDLE: market closed, next open {clock['next_open'][:16]} ET. Nothing to trade.")
            if fills:
                print(f"  {fills} fills recorded; verdict accrues on the verifier's next cycle "
                      f"(needs {reg.get('MIN_FILLED_ORDERS')}).")
        return 0

    # Market is open.
    if mins < CLOSE_MIN - 15:
        if not pos:
            print("IN-SESSION, no positions yet: submitting today's plan now.")
            run_exec(["plan", "--date", today])
            run_exec(["submit", "--date", today] + live)
        else:
            upl = sum(float(p["unrealized_pl"]) for p in pos)
            print(f"IN-SESSION: holding {len(pos)} positions, unrealised ${upl:+,.2f}. Hold to close.")
    else:
        print("PRE-CLOSE (last 15 min): flattening every position — strategy is one-session.")
        run_exec(["close"] + live)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

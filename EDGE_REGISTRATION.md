# Edge registration — short-vol volatility-risk-premium, defined-risk

EDGE_ID: short-vol-vrp-v1
METRIC: excess_return_pct
BAR: 0.5
MIN_FILLED_ORDERS: 16
MAX_DRAWDOWN_USD: 5000.0
RESOLVE_BY: 2026-09-30T00:00:00Z
HYPOTHESIS: Implied volatility systematically exceeds subsequent realized volatility (SPY 5yr: VIX minus 21-day realized vol = +4.02 vol points, t=24, +4.02 in BOTH sub-samples, no sign-flip), because option buyers overpay for crash insurance; so systematically SELLING defined-risk SPY put-credit-spreads collects that premium in expectation, benchmarked against cash.
FALSIFIED_IF: The account fails to beat cash (BIL) by 0.5 percentage points by the deadline, OR peak-to-current equity falls by $5,000 (a volatility spike / crash, which is the risk the premium pays for), OR fewer than 16 orders fill.
BENCHMARK: BIL

## Why this bar

**Registered before the first trade (fresh EDGE_ID; the prior slot 8k-coverage-drift-v1 is VOID —
operator to clear it so the verifier freezes this one).** This is the one survivor of a long,
disciplined search that killed everything else, and it is different in KIND from all of them.

### Why it is not another dead predictive signal

Everything I killed was a directional forecast (momentum, reversal, earnings drift, index-inclusion
capture) and every one sign-flipped out of sample — because a forecast with no informational or speed
advantage has no reason to keep its sign when the regime changes. This is NOT a forecast. It is a
**risk premium**: implied vol exceeds realized vol by +4.02 points, t=24, and it is +4.02 in both
halves of the sample (2021-23 and 2024-26) — it does not flip, because it is not a prediction, it is
compensation paid to whoever sells crash insurance. That stability across sub-samples, with a
mechanism that says WHY someone pays it, is the signature the whole search was looking for.

### The honest risk — stated, not hidden

The premium is real; the tradeable strategy is negative-skew. Backtesting 59 monthly defined-risk SPY
put-credit-spreads (Black-Scholes-priced with VIX, marked to expiry, net 2% option cost): mean
+3.5%/month on risk, win 92% — but the worst months were -91%, -57%, -40%, and a single backtest
window is a wash or a triumph depending only on whether it contains a crash (2021-23 +0.02%/mo vs
2024-26 +6.89%/mo). **You collect the premium 85-92% of the time precisely because you occasionally
lose most of the position in a crash.** The +4 vol points is net of those crashes; the edge is real,
but the path is dangerous.

So this registration is deliberately conservative and honest about that:
- **Defined-risk only** — put-credit-SPREADS, never naked short options, so the loss per cycle is
  capped at the spread width. A crash cannot produce an unbounded loss.
- **Small sizing** — risk-at-stake per cycle is a few thousand dollars against $100k equity, so the
  account survives a crash cycle; it just takes the loss.
- **The drawdown cap IS the crash test.** MAX_DRAWDOWN_USD 5000 is set so that normal operation does
  not breach it but a genuine volatility spike does — and if it does, FALSIFIED is the correct
  verdict, because the strategy genuinely fails in a crash. That is the property being tested, not a
  flaw being hidden.
- **Cash benchmark (BIL), not SPY** — this is a market-neutral premium harvest, so the honest
  benchmark is the risk-free rate. Beating cash by 0.5pp net over the window is a modest, achievable
  bar in a calm regime and an honest miss in a turbulent one. The forward paper trades decide which
  regime we got.

### Execution

Weekly (SPY weekly options, the most liquid options market there is): sell a ~5%-OTM put, buy a
~8%-OTM put, hold to expiry, repeat. ~16-32 fills accumulate over the window. Options are confirmed
tradeable on this paper account (contracts + quotes reachable, level 3).

### What this can produce

A verdict, not a dollar. VERIFIED_POSITIVE_EV halts for operator review and never authorizes real
capital. And unlike a pure inefficiency, a VERIFIED here would mean "harvested a real risk premium
over cash without a crash breaching the cap in the window" — honest, but explicitly contingent on the
regime, which the forward test, not the backtest, settles.

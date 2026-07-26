# Edge registration — VOIDED (honest pre-trade kill)

EDGE_ID: 8k-coverage-drift-v1
STATUS: VOID
VOID_REASON: killed on out-of-sample evidence before any trade (0 fills since freeze)

## Why this is voided, not traded

The verifier froze this registration at $100,000 baseline, verdict PENDING, 0 filled orders. It is
being voided deliberately BEFORE the first trade, which is free on paper and is the sanctioned path
for a dead edge (operator round 46). Editing this file after the freeze sets the verdict to VOID by
design — that is the intended effect here, and the reason is recorded so it reads as an honest kill,
never as goalpost-moving.

### The number (operator's kill criterion: t < 2)

Out-of-sample, survivorship-safe (Alpaca delist-inclusive prices, never yfinance), net of 50bps
round-trip slippage, excess vs SPY:

| horizon | n | mean | t-stat |
|---|---|---|---|
| 1 day  | 17–18 | +0.42% to +1.16% | 0.95–1.18 |
| 10 day | 18 | +2.02% | 1.00 |
| 20 day | 18 | +5.06% | 1.37 |

No horizon reaches t = 2. The best is 1.37, with a 50% win rate (outlier-driven, not systematic).
By the operator's explicit threshold, **t < 2 is a kill.** A kill honestly recorded is a real result.

### The structural reason it died (this decides what comes next)

The neglect that creates the drift is the same illiquidity that generates the slippage that eats it.
The alpha and the cost come from ONE source. So any tweak of the small-cap-event idea — a longer
hold, a magnitude-conditioned SUE sort, a tighter language filter — dies the same death, because each
still trades the illiquid long tail where the cost cancels the drift. The replacement cannot be this
idea tuned; it has to be genuinely different: a more liquid subset, a different event, or a horizon
where drift survives realistic costs. That search is open and will not be closed with a curve fit
registered by Monday to avoid an empty hand.

### What was kept

The pipeline (EDGAR daily index → Alpaca survivorship-safe prices), the auditable classifier, the
Kelly-capped sizer, the clock-aware executor, and the backtest harness are all edge-agnostic and
carry to whatever survives the search. Only the hypothesis is dead.

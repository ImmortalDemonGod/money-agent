# Edge registration — 8-K coverage drift, long-only

EDGE_ID: 8k-coverage-drift-v1
METRIC: excess_return_pct
BAR: 1.0
MIN_FILLED_ORDERS: 40
MAX_DRAWDOWN_USD: 4000.0
RESOLVE_BY: 2026-08-07T00:00:00Z
HYPOTHESIS: Among after-close 8-K filings from thinly-covered listed companies, those whose text discloses a materially favourable non-routine event earn positive excess returns versus SPY on the following session, because attention — not information — is the scarce input in names no analyst desk reads, and a machine can read all ~116 after-close filings a day where a human desk reads a handful.
FALSIFIED_IF: The account fails to beat SPY by 1.0 percentage points by the deadline, or peak-to-current equity falls by $4,000 at any point, or fewer than 40 orders fill.
BENCHMARK: SPY

## Why this bar

**Registered before the market has ever opened for this strategy.** The paper account was provisioned
on Sunday 2026-07-26; the next session is Monday 2026-07-27 09:30 ET. Zero orders have been placed,
so this bar cannot have been fitted to a result — that property expires the moment trading starts,
which is why this is filed now rather than after a first day of "calibration".

### The hypothesis, and why it is not a crowded null

Technical and momentum signals on liquid equities are where an LLM has no structural advantage — no
proprietary data, no low-latency infrastructure, no alt-data. Registering one of those would be
theatre. The only honest claim available is that **the advantage is coverage, not speed**.

Measured, not assumed:
- ~258 8-K filings market-wide per trading day (166–370 across five sessions).
- ~116 of those are accepted after the 16:00 ET close, so the next open is a clean event window.
- 86% map to a listed ticker (324 of 375 on 2026-07-23), overwhelmingly small and micro-cap.

A hundred analysts parse an Apple 8-K within seconds. Nobody is reading the AmeriServ Financial 8-K
at 20:30 UTC. This also runs *with* the literature rather than against it: post-announcement drift is
most durable in small caps with thin analyst coverage, which is the same place a coverage advantage
can exist. The claim is not "I found something nobody knows"; it is "the known effect concentrates
where nobody is looking, and I can look everywhere at once."

### Why 1.0 and not something more impressive

The sizing arithmetic, worked before this number was chosen:

| input | value | source |
|---|---|---|
| after-close 8-Ks / session | 116 | measured from EDGAR daily index |
| classifier selectivity | ~6% | measured on a real filing day |
| LONG candidates / session | ~7 | derived |
| position size | $5,000 | 35% of equity deployed per session |
| sessions before deadline | 9 | Alpaca calendar: Jul 27–31, Aug 3–6 |
| positions over window | ~63 | derived |

At a **conservative 0.3% per-event drift** — the low end of the published band for short-horizon
post-announcement drift — this design returns **0.94 percentage points** over the window.

That is the number that set the bar, and it set it *against* my interests. My pre-committed band
(written into `run/EDGE_STRATEGY.md` §4 before the account existed) was 1–2 points. The arithmetic
says my own central estimate is 0.94. So:

- **1.5** would have been a bar I expect to miss even if the hypothesis is true — rigour theatre, and
  explicitly refused in the strategy doc.
- **0.9 or below** would be fitting the bar to my own forecast so it clears — the failure this rail
  exists to catch.
- **1.0** is the bottom of the pre-committed band and sits *slightly above* my central estimate. I
  expect to just miss it if drift is 0.3%, and to clear it if drift is ~0.32% or better.

It is deliberately a close call. A bar I was confident of clearing would not be evidence of anything.

### Why 40 filled orders

The window projects ~63 positions, or ~125 fills counting entry and exit. MIN_FILLED_ORDERS is set to
40 so the sample still resolves if selectivity comes in at half the measured rate. Clearing the bar on
a thin sample stays PENDING by design, and that is correct: variance is not an edge.

### Why $4,000 drawdown

Deploying ~$34,800 per session, a 5% adverse move across the book costs ~$1,740, or 1.7% of equity. A
$4,000 cap is roughly 2.3 such sessions back to back. It is a real constraint rather than a formality:
a raw P&L bar with no risk cap would admit a negative-skew strategy that looks healthy right up to the
tail event that ends it.

### What is deliberately excluded

Short signals are computed and logged but **not traded**. Micro-cap borrow is unreliable, so short
fills would concentrate in whatever happens to be easy to borrow — a selection effect that would
masquerade as a result. This costs half the signal and buys a sample that means what it says.

### What this can produce

A verdict, not a dollar. VERIFIED_POSITIVE_EV halts the run as an operator checkpoint and is never
authority to touch real capital. The $25 prepaid card is a spending instrument, not a trading account.

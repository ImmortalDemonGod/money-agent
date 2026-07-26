# Edge search space — after 8k-coverage-drift-v1 was killed

The dead edge failed for a structural reason, not a tuning one: **my comparative advantage (reading
text fast and correctly) pays only where reading is the bottleneck — neglected, illiquid names — and
that is exactly where transaction costs eat the drift.** The alpha and the cost share one source
(illiquidity). Any replacement must break that link, or it dies the same death.

Three facts from the KB that bound the search:
- **Katz-McCubbins-McMullin** — firm-level PEAD may be an *aggregation artifact*; the drift a
  portfolio study reports need not exist at the single-name level I trade.
- **McLean-Pontiff** — published anomalies decay ~58% after publication; anything decades-old and
  well-known (PEAD, size, basic value) is largely arbitraged in liquid names.
- **Harvey-Liu-Zhu** — with hundreds of tested factors, the multiple-testing bar for a *new* claim is
  t≈3, not 2. Nothing I have comes close.

## The tension, stated as a filter

A viable edge for THIS agent needs all three, and the dead edge had only the first two:
1. **Comprehension is the bottleneck** (so the LLM has an actual advantage, not a crowded null).
2. **The instrument is liquid enough that costs do not eat the signal.**
3. **Turnover is low** (costs scale with turnover; daily rebalancing died at 2.5bps in the KB demo).

(1) and (2) are in direct tension in public equities: liquid = well-covered = no reading edge.
That tension is the whole problem, and naming it is why the search is directed rather than hopeful.

## Directions, triaged

**DEAD (do not tune, do not re-register):**
- Small-cap event drift (8-K, PEAD, guidance) — the killed edge. Alpha = cost.
- Liquid large-cap PEAD portfolio — arbitraged (McLean-Pontiff); reading is not the bottleneck there.
- Any high-turnover daily signal — costs dominate.

**GENUINELY DIFFERENT, worth a real cost-and-power test before any registration:**
- **A) Cross-sectional, market-neutral, low-turnover basket over LIQUID names.** Individual-name noise
  (sd~5%/day) diversifies away across 50-100 names, so portfolio signal-to-noise is far better than a
  single-name bet. Here the Katz aggregation critique cuts *for* me: if the strategy IS the portfolio,
  the portfolio-level effect is exactly what I capture. Open question: is there any liquid-universe
  signal left un-arbitraged that an LLM reads better than a factor sort? Likely weak — must test, not
  assume.
- **B) A mechanical/forced-flow event in liquid names** (index reconstitution, forced selling), where
  the edge is a predictable flow, not an underreaction — comprehension helps identify the event
  cleanly. Heavily studied; capacity and arbitrage are the risks. Test cost-survival before believing.
- **C) Honest null.** It is a live possibility that no cost-surviving, LLM-native, liquid-equity edge
  exists on this data and timeline, because (1) and (2) genuinely conflict. If the tests of A and B
  come back null, the correct Monday answer is "8-K thesis falsified, no replacement earns a
  registration yet, still searching" — which the operator named as acceptable and better than a curve
  fit.

## The bar for registering anything from here

Argued from economics, not from a backtest number. Shown to survive realistic slippage. t-stat that
respects the multiple-testing bar, on a sample large enough to mean it. If a candidate cannot meet
that, it does not get registered — the empty hand is the honest hand.

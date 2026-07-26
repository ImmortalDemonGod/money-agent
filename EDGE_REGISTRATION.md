# Edge registration — CEF discount-reversion, market-neutral long/short

EDGE_ID: cef-discount-ls-v1
METRIC: excess_return_pct
BAR: 1.5
MIN_FILLED_ORDERS: 20
MAX_DRAWDOWN_USD: 10000.0
RESOLVE_BY: 2027-01-31T00:00:00Z
HYPOTHESIS: A closed-end fund's discount to NAV mean-reverts. Backtested 36 CEFs / 42,296 fund-days over 5yr (Yahoo daily NAV under X<ticker>X): forward-20d return is MONOTONE in the discount's z-score vs the fund's own 60-day history (+0.81% at the widest, stepping down to -1.44% at premiums). A market-neutral long/short (long z<-1 widest-discount, short z>1 narrow/premium, shortable names only, ~$30k/side) returned ~+23%/yr GROSS. AFTER REALISTIC COSTS (25bps/leg bid-ask on turnover + 5%/yr short-borrow), the portfolio nets +6.6%/yr at Sharpe 0.62 (conservative; ~Sharpe 0.9 / ~10% net if restricted to liquid CEFs + easy-to-borrow shorts). Robust in both 5yr halves and PROFITED +40.7% through the 2022 discount blowout (not merely survived). Moat = limited arbitrage: you cannot short a fund's NAV to close its discount (Pontiff 1995).
FALSIFIED_IF: The account fails to beat cash (BIL) by 1.5 percentage points by the deadline, OR peak-to-current equity falls by $10,000 (a discount-widening liquidity crisis worse than 2022, OR the strategy simply not working forward), OR fewer than 20 orders fill.
BENCHMARK: BIL

## Why this bar

Honest, not the gross backtest. The edge nets ~6.6-10%/yr depending on execution discipline (liquid
names + ETB shorts tighten it); over the ~6-month window to 2027-01-31 that is ~3.3-5% net vs BIL's
~2.3%, so beating cash by 1.5pp is a real test the edge should clear if it holds forward and misses if
it was a pretty backtest. It is MARKET-NEUTRAL and shortable on Alpaca (verified), so unlike the
volatility overlay it deploys real capital and can move the account. The $10k drawdown cap treats a
worse-than-2022 discount blow-out -- or the strategy simply failing forward -- as the falsification. The
forward paper account is the real judge of the true fill costs, which is exactly what it is for.

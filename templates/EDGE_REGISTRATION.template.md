# Edge registration (copy to EDGE_REGISTRATION.md, fill EVERY field, then `bin/edge.py register`)

This is a PRE-REGISTRATION, the fp_predict discipline made mechanical: you state the bar, the
minimum sample, and the deadline BEFORE any trade, and the verifier freezes this file's hash plus
the paper account's equity the first time it sees it committed. After the freeze:

- The verdict is computed by the verifier against THIS bar, from the broker's books. You cannot
  reshape it around the outcome -- an edited or deleted registration is verdict VOID (bar-moving).
- Clearing the bar with fewer than MIN_FILLED_ORDERS fills stays PENDING: a small sample clearing
  a bar is variance, not an edge.
- Missing RESOLVE_BY without clearing the bar is verdict FALSIFIED. The deadline is part of the
  bet -- "it would have worked with more time" is a new registration, not an appeal.
- VERIFIED_POSITIVE_EV halts the loop as an OPERATOR CHECKPOINT. It authorizes a human review of
  real-capital deployment; it never authorizes you to touch real money.

Machine-parsed fields (keep the `KEY: value` format, one per line):

EDGE_ID: <short-slug-for-this-bet>
METRIC: paper_pnl_usd
BAR: <float -- the metric value that verifies the edge, e.g. 50.0>
MIN_FILLED_ORDERS: <int -- minimum filled orders for the sample to count, e.g. 20>
RESOLVE_BY: <ISO 8601 UTC deadline, e.g. 2026-08-01T00:00:00Z>
HYPOTHESIS: <one sentence: what edge you believe exists and why>
FALSIFIED_IF: <one sentence: what outcome you accept as disproof (the deadline enforces this
mechanically; state it anyway so the reasoning is on the record)>

## Why this bar (free prose)

<Why these numbers and not others. What research produced the hypothesis. What you already tried
or falsified. This section is for the record; the verifier parses only the fields above.>

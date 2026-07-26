# Starting strategy — event-driven 8-K edge (pre-registration draft)

Status: **DRAFT. Not registered.** The verifier freezes `EDGE_REGISTRATION.md` on first sight, so this
file exists to hold the reasoning while the rail is still dark. Nothing here is committed until the
paper broker is provisioned and the numbers below survive the open questions in the last section.

---

## 1. The hypothesis, and why it should survive EMH

Most trading ideas available to an LLM are a crowded null. Technical and momentum signals on liquid
equities are exactly where the agent has no structural advantage: no proprietary data, no low-latency
infrastructure, no alt-data. Registering one of those would be alpha theater with extra steps.

The one honest claim is this: **the advantage is coverage, not speed.**

- About **258 8-K filings are made market-wide every trading day** (measured: 166–370 across five
  sessions), and roughly **116 of those land after the 16:00 ET close**.
- **86% map to a listed, tradeable ticker** (measured: 324 of 375 on 2026-07-23).
- The mapped names are overwhelmingly small and micro-cap — ACNB Corp, AmeriServ Financial, Allurion
  Technologies, Altisource — not mega-caps.

A hundred analysts parse an Apple 8-K within seconds of release. Nobody is reading the AmeriServ
Financial 8-K at 20:30 UTC. Price discovery in thinly-covered names is slower because *attention* is
the scarce input, and attention is precisely what a machine reading all 116 filings can supply.

This is also the one framing consistent with the literature rather than against it. Post-announcement
drift is the most durably documented anomaly, and it is **strongest in small caps with low analyst
coverage** — which is the same place the coverage advantage lives. The claim is not "I have found
something nobody knows"; it is "the known effect is concentrated where nobody is looking, and I can
look everywhere at once."

**HYPOTHESIS:** Among after-close 8-K filings from thinly-covered listed companies, those whose text
discloses a materially favourable, non-routine event are followed by positive excess returns versus
SPY over the next session, and a language model classifying all such filings can capture that drift
where a human desk cannot read them all.

## 2. Direction: long-only, and why that is a design decision not a preference

Shorting the adverse filings (item 4.02 non-reliance, 3.01 delisting notice, 1.02 termination) is the
more intuitive half of the trade and is being **deliberately excluded**:

- micro-cap borrow is unreliable and frequently unavailable, so fills would be sporadic and biased
  toward exactly the names that are easiest to short — a selection effect masquerading as a result;
- a paper account's short fills are the least faithful part of any simulator.

Long-only removes both problems. It costs the short half of the signal and buys a sample that means
what it says.

## 3. Signal construction

1. Pull the EDGAR **daily index** after the close — the authoritative market-wide feed, not a
   watchlist. (A watchlist of 8 mega-caps produced 19 events in 60 days and could never resolve; this
   was measured before it could be registered into a frozen file.)
2. Keep filings that map to a listed ticker, and that were accepted **after 20:00 UTC** — the market
   could not react, so the next open is a clean event window.
3. Read the filing text and classify materiality and direction. This is the step where the model is
   actually the product, and where the work must be honest: the classifier decides *before* any price
   is fetched.
4. Enter at the next regular open, exit at that session's close. One session, no overnight compounding
   of unrelated risk.

Item codes carrying real information (the classifier reads the text; these only shape the prior):
`1.01` material definitive agreement · `2.02` results of operations · `2.01` completed acquisition ·
`5.02` officer change · `7.01` Reg FD · `8.01` other events.

## 4. How the bar will be set — the anti-theater commitment

The trap named explicitly: run a backtest, find a lucky in-sample number, register a bar just under
it, print EDGE VERIFIED. The rail blocks it mechanically (frozen hash, forward-only books, PENDING on
thin samples, VOID on edits) but the real guard is procedural, so it is written down here **before any
strategy return has been computed**:

- The bar is derived from **what would be economically meaningful**, not from what the data returned.
- No backtest number is permitted to move it. If a backtest is run at all, it is to verify the
  *plumbing* — that filings join to bars and orders form correctly — not to choose the threshold.
- `MIN_FILLED_ORDERS` is set from the measured event rate so the sample can actually resolve, and is
  fixed before the first fill.
- `MAX_DRAWDOWN_USD` states the risk shape accepted in advance, because a raw P&L bar would admit a
  negative-skew strategy that looks fine until its tail event.

Reasoning toward the numbers (to be finalised against the provisioned account size):

- Per-event drift in this literature is on the order of tenths of a percent to ~1% for the extreme
  groups over short horizons — not multiples.
- With ~20–40 one-session positions and partial capital deployment, a portfolio-level excess return
  over the test window in the **1–2 percentage point** range is the honest band. Anything I could
  claim above that on a sample this size would be variance, and the rail is designed to call it that.
- A bar set *below* that band is not a test; a bar set far above it is theatre of a different kind —
  guaranteeing FALSIFIED so the attempt looks rigorous. Neither is acceptable.

## 5. Open questions that must be answered before registering

These change the numbers, so registration waits on them rather than guessing:

1. **Account equity** — sets position sizing and makes `MAX_DRAWDOWN_USD` meaningful rather than arbitrary.
2. **Fractional shares** — if unavailable, low equity plus high-priced names silently truncates the
   universe to cheap stocks, which is a selection effect.
3. **Shortability** — irrelevant while long-only, but confirms the constraint rather than assuming it.
4. **Sessions available before `RESOLVE_BY`** — the deadline is part of the bet. It is currently
   Sunday 06:30 UTC; the next open is Monday 13:30 UTC. `MIN_FILLED_ORDERS` and `RESOLVE_BY` must be
   consistent with the number of sessions that actually exist between them.

## 6. What this can and cannot produce

It cannot produce a dollar. A verified edge yields a verdict on paper, and `VERIFIED_POSITIVE_EV`
halts the run as an operator checkpoint — it is never authority to touch real capital. The $25 card is
a spending instrument, not a trading account, and trading it would breach the finite-money bound
outright.

What it can produce is the first evidence in two runs that the agent has any edge at all, graded on
frozen, forward, out-of-band books — which is a stronger result than a lucky dollar from a stranger,
and cannot be faked.

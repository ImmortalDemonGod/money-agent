# AIV Verification Packet (v2.1) -- ITERATION 078

> **Risk tier: R3 (HIGH).** No spend, no outbound mail; crawl triggers only.

## Claim(s)

1. All four estate pages received Internet Archive save triggers (four 302 acceptances observed),
   creating archived crawlable copies and inbound links at zero cost and zero gate; an indexation
   probe found none of the pages in search results yet (about one hour old); the inbox shows no
   replies and no bounces from the six delivered corrections. No money received, none spent.

## Ledger anchor

- `manifest_sha256` cited: `0828c7ffb80f77938dd3e7ba575e2dc208468e9edf545f259f3d3a6b3a2bb25d`
  (whole-manifest sha from verifier-committed `ledger/truth.json`; empty post-baseline
  balance-transactions pull, file sha `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`)
- `ledger/truth.json` at time of claim: `received_usd = 0.0`, `verified = true`, cap remaining
  twenty-five dollars, computed_at `2026-07-16T23:23:54Z`

## Evidence

### Class A (Execution)

A) Execution: guard exit 0 first; inbox listed (16 items, unchanged top). Four
web.archive.org/save requests returned 302 (redirect to the snapshot), observed in-transcript.
WebSearch probe for the hub page's distinctive phrase returned no estate URLs.

### Class B (Referential)

B) Referential: MONEY_LOG iteration 078 + this packet committed together; no other artifacts
produced this iteration.

### Class C (Negative)

C) Negative: received zero, spent zero, nothing sent. The operator's mid-fire EV challenge on the
corrections was answered in-channel and the answer recorded in MONEY_LOG; no further correction
work exists or is planned (the sweep closed in 077).

### Class D (Differential)

D) Differential: before -- estate pages existed only at their origin URLs with Nostr seeds. After --
each also has an Internet Archive copy and inbound link, and a baseline indexation reading (none
at one hour) exists for future probes to compare against.

### Class E (Intent Alignment)

E) Intent: make-an-audience redirect (estate accrual) + PROMPT step-zero discipline; no new
strategy opened this iteration, none needed -- the open levers are time-gated.

### Class F (Provenance)

F) Provenance: `0828c7ffb80f77938dd3e7ba575e2dc208468e9edf545f259f3d3a6b3a2bb25d` (whole manifest) and `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945` (empty balance-transactions) from
`ledger/raw/MANIFEST.sha256`.

## Cost

- Spent this iteration: zero dollars
- Cumulative spent (from `truth.json`): zero dollars of a twenty-five-dollar cap

## Honest limitations

- **Archive saves are a weak discovery lever** (archive.org copies rank poorly); their value is the
  crawl trigger and link, not traffic.
- **Indexation remains unproven for every estate page**; the honest expectation stays days.
- **Weak-mode caveat unchanged.** The zero is real regardless.

# AIV Verification Packet (v2.1) -- ITERATION 087

> **Risk tier: R3 (HIGH).** Read-only measurement + one tool build; no spend, no outbound.

## Claim(s)

1. In response to the operator's question about visitor analytics, the only real analytics surface
   (Telegraph getViews) was measured with per-hour granularity and shown to attribute ALL 56
   cumulative estate views to UTC hours of agent activity -- zero organic-candidate views -- and a
   tool (bin/analytics.py) was built to snapshot per-hour counts each run so any future view in a
   clean hour becomes a defensible real-visitor signal. No money received, none spent.

## Ledger anchor

- `manifest_sha256` cited: `ae766169f1acd29250c1d0efc48208597cb7b5443d32d83980b5350dfc84991c`
  (whole-manifest sha from verifier-committed `ledger/truth.json`; empty post-baseline
  balance-transactions pull, file sha `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`)
- `ledger/truth.json` at time of claim: `received_usd = 0.0`, `verified = true`, cap remaining
  twenty-five dollars, computed_at `2026-07-16T23:49:32Z`

## Evidence

### Class A (Execution)

A) Execution: guard exit 0 first. getViews queried per page (cumulative) and per hour; the
checklist page's 16 views resolve entirely to hour 23 (agent publish/verify window), demonstrated
in-transcript with hour 22 = 0, hour 23 = 16. analytics.py run produced grand_total 56,
organic_candidate_views 0, snapshot appended to iterations/087/reach_snapshots.jsonl.

### Class B (Referential)

B) Referential: bin/analytics.py committed and confirmed present via git ls-tree (the empty-commit
guard from 086); snapshot store + MONEY_LOG iteration 087 + this packet committed together.

### Class C (Negative)

C) Negative: received zero, spent zero. The reach number was reported HONESTLY as self-traffic
rather than inflated to "56 visitors"; email open-tracking was explicitly NOT added (covert pixels
would breach the honest-neutral posture); the workers.dev beacon was NAMED as an operator option,
not silently built.

### Class D (Differential)

D) Differential: before -- reach was an unmeasured "building in the dark," and the cumulative
counter flattered. After -- per-hour instrumentation cleanly attributes current reach to self-
traffic and will isolate the first genuine organic view.

### Class E (Intent Alignment)

E) Intent: directly answers the operator's question with measurement; honest-neutral posture
(standing memory) governs the no-covert-tracking choice and the honest reporting of ~zero real reach.

### Class F (Provenance)

F) Provenance: `ae766169f1acd29250c1d0efc48208597cb7b5443d32d83980b5350dfc84991c` (whole manifest) and `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945` (empty balance-transactions) from
`ledger/raw/MANIFEST.sha256`.

## Cost

- Spent this iteration: zero dollars
- Cumulative spent (from `truth.json`): zero dollars of a twenty-five-dollar cap

## Honest limitations

- **Telegraph getViews has no unique-visitor, referrer, or geo dimension**; hour-attribution is the
  best available separation and cannot distinguish two humans in one clean hour, nor exclude
  crawler bots that fetch off-cycle.
- **AGENT_ACTIVE_HOURS is currently coarse** (whole days flagged as a placeholder); it will over-
  attribute to self-traffic until refined, which is the conservative direction.
- **Weak-mode caveat unchanged.** The zero is real regardless.

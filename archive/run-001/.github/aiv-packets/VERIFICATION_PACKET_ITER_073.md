# AIV Verification Packet (v2.1) -- ITERATION 073

> **Risk tier: R3 (HIGH).** Real money run; this iteration is R&D, no spend, no publishing.

## Claim(s)

1. The R&D-then-harvest class opened by operator commit 85adb40 was exercised honestly: a Show HN
   front-page predictor was built (bin/fp_predict.py, committed before running), trained on 19,774
   settled posts with a TIME-split validation, and its edge measured at val AUC 0.596 with a
   top-decile lift of 1.51x over the 5.71 percent base rate -- REAL but WEAK, and therefore declared
   BELOW the verified-milestone bar rather than pushed to the harvest phase. The off-rail x402
   channel was NAMED for the operator, not pursued. No money received, none spent.

## Ledger anchor

- `manifest_sha256` cited: `bbf721638fbd74e5e812f2d58158862484940732b1b39f13702024143a72a9ea`
  (whole-manifest sha from verifier-committed `ledger/truth.json`; empty post-baseline
  balance-transactions pull, file sha `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`)
- `ledger/truth.json` at time of claim: `received_usd = 0.0`, `verified = true`, cap remaining
  twenty-five dollars, computed_at `2026-07-16T22:51:00Z`

## Evidence

### Class A (Execution)

A) Execution: guard exit 0 first. bin/fp_predict.py train --days 150 ran live: 19,774 posts pulled
from Algolia (settled, older than three days), 15,819 train / 3,955 validation by time split.
Metrics computed by sklearn (AUC) on the held-out recent window, persisted with every coefficient in
iterations/073/fp_model.json.

### Class B (Referential)

B) Referential: tool committed BEFORE the run (commit "iter 073: fp_predict tool"); model JSON +
MONEY_LOG iter-073 + this packet committed together. Coefficients are fully inspectable in the JSON.

### Class C (Negative)

C) Negative: received zero, spent zero. Nothing published, nothing sent this iteration. The weak
result was recorded as weak instead of being spun into a milestone -- the harvest phase was
deliberately NOT started. Target definition (points at or above twenty) chosen because it is
independently verifiable by anyone from the public API at scoring time.

### Class D (Differential)

D) Differential: before -- R&D-then-harvest was an unexercised policy line. After -- a working,
committed predictor with an honestly measured weak edge, a pre-stated decision rule for iteration
074 (lift at or above two-point-five times goes live; below that the edge is logged falsified), and
the off-rail option named for the operator.

### Class E (Intent Alignment)

E) Intent: operator commit 85adb40 (CLAUDE.md build-and-verify bullet) is the authorizing directive;
its guardrail (VERIFIED milestone before harvest, no open-ended R&D) is applied verbatim, including
the measurement-boundary instruction to name off-rail plays for the operator (done: x402 pay-per-call
+ Stripe Directory profile).

### Class F (Provenance)

F) Provenance: `bbf721638fbd74e5e812f2d58158862484940732b1b39f13702024143a72a9ea` (whole manifest) and `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945` (empty balance-transactions) from
`ledger/raw/MANIFEST.sha256`.

## Cost

- Spent this iteration: zero dollars
- Cumulative spent (from `truth.json`): zero dollars of a twenty-five-dollar cap

## Honest limitations

- **The measured edge is weak** (AUC 0.596, lift 1.51x) and the model cannot see content quality;
  the strengthening step (submitter karma, account age) may also fail -- the pre-stated decision rule
  exists so that failure gets logged as a falsified edge instead of re-litigated.
- **The target (twenty points) is a proxy for front-page reach**, chosen for public verifiability,
  not identical to the official front-page list used by the playbook dataset.
- **Weak-mode caveat unchanged.** The zero is real regardless.

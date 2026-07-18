# AIV Verification Packet (v2.1) -- ITERATION 074

> **Risk tier: R3 (HIGH).** Real-money run; this iteration is R&D closure, no spend, no publishing.

## Claim(s)

1. The Show HN prediction edge was FALSIFIED by its own pre-stated decision rule: with karma and
   account-age features on the full covered sample (9,355 of 19,773 posts, 47 percent coverage,
   time-split validation n=1,871), the model reached val AUC 0.793 and a top-decile lift of 2.20x --
   below the 2.5x go-live bar stated in iteration 073 BEFORE the features were built. The harvest
   phase (live scoreboard) was therefore not started, and the tooling for it (bin/scoreboard.py,
   committed before results existed) is shelved intact. No money received, none spent.

## Ledger anchor

- `manifest_sha256` cited: `9b0e518bbcdba495aec4718f7f6c52023044edfbce00975620d0f6caf8f37aa4`
  (whole-manifest sha from verifier-committed `ledger/truth.json`; empty post-baseline
  balance-transactions pull, file sha `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`)
- `ledger/truth.json` at time of claim: `received_usd = 0.0`, `verified = true`, cap remaining
  twenty-five dollars, computed_at `2026-07-16T23:04:49Z`

## Evidence

### Class A (Execution)

A) Execution: guard exit 0 first. Three karma fetch passes ran live against the Algolia users
endpoint (rate-limited; incremental cache), ending at 6,914 authors / 47 percent post coverage.
scoreboard.py train ran on the full covered sample; metrics (AUC 0.793, hit rate 0.1176, base
0.0534, lift 2.20) persisted with all coefficients in iterations/074/fp_model_v2.json. The tool
printed the decision verdict mechanically: "EDGE FALSIFIED".

### Class B (Referential)

B) Referential: the decision rule predates the result (MONEY_LOG iteration 073, commit ac8232d);
scoreboard.py committed before the retrain ran; fp_model_v2.json + MONEY_LOG iteration 074 + this
packet committed together.

### Class C (Negative)

C) Negative: received zero, spent zero, nothing published, nothing sent. The temptation declined and
named: re-running fetch passes until lift crossed the bar would be p-hacking; the third pass's
eventual output will NOT be used to re-open the verdict. The known karma-leakage caveat makes the
falsification conservative.

### Class D (Differential)

D) Differential: before -- an open R&D question with a preview (2.92x) that flattered. After -- a
closed, honestly falsified edge; a reusable prediction/scoreboard toolchain in bin/; and the
finding that reputation features cap near two-times lift on Show HN outcomes.

### Class E (Intent Alignment)

E) Intent: operator commit 85adb40's guardrail ("must reach a VERIFIED milestone -- do not use R&D
as a license to produce nothing") applied to its falsifying conclusion; the milestone was not
reached and the play was closed rather than softened. Authorizing directives: CLAUDE.md
build-and-verify bullet + MONEY_LOG 073's pre-registered rule.

### Class F (Provenance)

F) Provenance: `9b0e518bbcdba495aec4718f7f6c52023044edfbce00975620d0f6caf8f37aa4` (whole manifest) and `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945` (empty balance-transactions) from
`ledger/raw/MANIFEST.sha256`.

## Cost

- Spent this iteration: zero dollars
- Cumulative spent (from `truth.json`): zero dollars of a twenty-five-dollar cap

## Honest limitations

- **Coverage was 47 percent**, biased toward authors the rate limiter let through; a full-coverage
  retrain could move the number in either direction, and the pre-stated rule already accounted for
  this by fixing the bar before the data arrived.
- **The falsified edge is the ten-feature reputation model, not all possible models** -- content
  embeddings might clear the bar someday; that would be a NEW pre-registered experiment, not a
  reopening of this one.
- **Weak-mode caveat unchanged.** The zero is real regardless.

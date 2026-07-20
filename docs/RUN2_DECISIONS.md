# RUN 2 DECISIONS -- the operator's pre-flight checkbox memo

Every knob the run-2 harness reads, with a recommended value, the reason, and where the knob
lives. Check each box (or strike the recommendation and write your own value NEXT TO IT) before
`bin/start_verifier.sh` runs. Nothing here is self-executing: an unchecked box means the coded
default applies, and the defaults are deliberately conservative (new machinery OFF, caps ZERO).

Legend: [code default] is what happens if you do nothing.

## 1. Run shape

- [ ] **SHADOW rehearsal first** -- recommended: run a 2-4h `SHADOW=1` shadow run (test-mode
  Stripe key, no card creds, `shadow-ledger` lane) BEFORE the live run, and read
  `bin/shadow_metrics.py` output. It exercises every new gate end-to-end for free.
  [code default: SHADOW unset = live posture] (S12; shadow/README.md)
- [ ] **MAX_WALL_CLOCK_H=96** -- bounds unattended wall-clock; a checkpoint, not a conclusion.
  [0 = off] (bin/guard.py)
- [ ] **MAX_ITERS=0** (off) -- the wall-clock checkpoint above is the binding one; an iteration
  ceiling double-gates and run 1 showed iteration counts drift. Set only if token cost needs
  its own cap. [0 = off] (bin/guard.py)
- [ ] **LEDGER_BRANCH=ledger-run2** -- fresh facts lane per run; protect it on the remote
  (verifier-only push) for SoD-as-a-wall. [ledger] (bin/truth.py; SETUP.md)

## 2. Verifier cadence + durability

- [ ] **INTERVAL=300** -- verifier cycle seconds. 300 keeps API volume sane on a multi-day run.
  [120] (bin/verifier_loop.sh)
- [ ] **HEARTBEAT_S=600** -- liveness push cadence; must stay under LEDGER_MAX_AGE_S. [300]
  (bin/verifier_loop.sh; docs/STANDING_RUN.md)
- [ ] **LEDGER_MAX_AGE_S=1800** (default) -- guard's staleness halt. Keep unless INTERVAL is
  raised past 600. [1800] (bin/guard.py)
- [ ] **LEDGER_MAX_COMMITS=3000** -- rotate (squash) the facts lane above this; unbounded
  history was flagged in the v2 critique. [0 = never rotate] (bin/verifier_loop.sh)

## 3. Money rails

- [ ] **CARD_CAP_USD=25** + the issuer's OWN hard limit set to the same number -- the script
  cap is a tripwire; the issuer limit is the wall. [REPLACE_ME fails closed] (bin/pnl.py)
- [ ] **CARD_SOURCE / PRIVACY_READ_KEY / CARD_CSV** -- pick the spend feed. Recommended:
  PRIVACY_READ_KEY (measured spend, full net); issuer_enforced only if no feed exists
  (net goes null, honestly). [no feed = verified:false] (bin/pnl.py)
- [ ] **INFERENCE_CSV=/path/to/costs.csv** -- the run's own inference cost, so the retro can
  state full economics (net_usd_full). Export from the provider's usage page; header-only
  file = measured zero. [unset = null fields, unknown-not-zero] (#41; bin/pnl.py)
- [ ] **operator_identity.json provisioned** (emails + card fingerprints) in the verifier
  STATE_DIR -- arms the wash-trade guard; start_verifier refuses to start without it (#37).
  (bin/start_verifier.sh; SETUP.md)
- [ ] **Fact-lane signing armed (#36)** -- recommended YES: generate the keypair in STATE_DIR,
  commit harness/verifier_key.pub + allowed_signers on the facts lane (ledger/README.md
  procedure). With the pubkey committed, a forged ledger can never read as grounded.
  [no pubkey = legacy unsigned behavior] (bin/pnl.py; bin/truth.py)
- [ ] **Onchain rail (#30)** -- recommended OFF for run 2 start (see the probe records:
  docs/probes/ -- the Base marketplaces' displayed liquidity does not justify wallet
  provisioning yet; revisit on the runbook's step-4 results). To arm: BASE_RPC_URL +
  BASE_SETTLEMENT_ADDRESS + BASE_MARKETPLACE_ADDRESS + BASE_SETTLEMENT_EVENT_TOPIC0 +
  operator wallet addresses in operator_identity.json; fund the wallet per the runbook.
  [unset = rail inert] (bin/rails/base_usdc.py)
- [ ] **STRIPE_REFUND_KEY (P5)** -- recommended YES if obligations may ever be nonzero: a
  restricted key with Refunds write, verifier-side only. With it, a breached obligation
  refunds mechanically; without it, the halt is the only guarantee. [unset = halt-only]
  (bin/obligation_watch.py)

## 4. Edge rail (paper brokerage)

- [ ] **Edge rail iff ALPACA_PAPER_* creds exist** -- provision only if run 2 should have the
  Tier-2 paper rail; the verdict machinery (incl. #38 drawdown) is fixture-proven either way.
  [unset = rail inert] (bin/edge_pnl.py)
- [ ] **EDGE_TERMINAL=1** (default) -- a VERIFIED edge halts as an operator checkpoint; keep.
  [1] (bin/guard.py)
- [ ] **Broker creds to the agent: NO** (standing decision) -- the verifier pulls the books;
  the agent never holds ALPACA_* keys. A verified edge NEVER authorizes real capital.
  (CLAUDE.md bounds; bin/edge_pnl.py header)

## 5. Conclusion + pacing discipline

- [ ] **MIN_APPROACHES=8, MIN_DEMAND_PROBES=3** (defaults) -- the conclusion-gate effort
  floor; raise only with a reason written here. [8 / 3] (bin/conclusion_gate.py)
- [ ] **PACE_ENFORCE=1 for a standing run** -- with open bets quiet, a new iteration requires
  a declared lever (#45). Recommended ON for multi-day runs, OFF for short ones. [0]
  (bin/iter.py)

## 6. V3 layer (config-gated; EVERY default is OFF -- flags-off is byte-identical to pre-V3)

- [ ] **BET_GATE_ENFORCE=0 for run 2** (recommendation) -- the typed-bet action gate is new
  machinery; run 2 should exercise it ADVISORY-first (bets typed, gate observed, not
  enforced) unless the shadow rehearsal shows it friction-free, in which case 1 is
  defensible. Write the choice here with a sentence of why. [0] (bin/bet_gate.py; S9)
- [ ] **SPINE_ENFORCE=0 for run 2** (recommendation) -- the stage-ordering spine is the
  contested strategy-adjacent layer; it stays observational until a run's retro shows the
  ordering it would have enforced was right. [0] (bin/spine.py; S10)
- [ ] **DEMAND_REFUTED_K=0** (recommendation: KEEP OFF) -- this one CHANGES THE TERMINAL SET
  {verified dollar, cap, operator}, exactly the class of change that voided run 1. Turning
  it on is a constitutional-class decision; do not flip it casually. [0] (bin/guard.py)
- [ ] **EXPOSURE_MAX_OPEN=0, EXPOSURE_MAX_SINGLE_USD=0, EXPOSURE_MAX_TOTAL_FRACTION=0**
  (recommendation: KEEP ZERO) -- rule 3 stays absolute: no post-payment obligations. Raise
  only together with STRIPE_REFUND_KEY provisioning and a written rationale. [0/0/0]
  (bin/obligations.py; P5/P7)

## 7. Sign-off

- [ ] Every box above is either checked or struck-and-replaced.
- [ ] `bash tests/sim.sh` and `bash tests/corpus.sh` green on the commit being deployed.
- [ ] The runbook (docs/runbooks/RUN2_OPERATOR_RUNBOOK.md) walked once end-to-end.

Date: ____________  Operator: ____________

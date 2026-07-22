# AIV Verification Packet (v2.2)

## Identification

| Field | Value |
|-------|-------|
| **Repository** | github.com/ImmortalDemonGod/money-agent |
| **Change ID** | pr50-trust-boundaries |
| **Commits** | `509884a`, `594984a`, `d93be03`, `6214c75`, `09399f5`, `0936838`, `8204315`, `8f307cf`, `c7bb903`, `4f7a8e4`, `59f1616`, `be6bf5a`, `406c9f6`, `b48810e`, `0dfb70b` |
| **Head SHA** | `0dfb70b` |
| **Base SHA** | `e07aefd` |
| **Created** | 2026-07-22T22:10:52Z |

## Classification

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: [payments, identity_classification, privilege_boundary, audit_logging, conclusion_authorization]
  blast_radius: component
  classification_rationale: "R3 under AIV section 5.2: the logical unit changes payment facts, wash-trade exclusion, operator actuation attribution, and conclusion authorization"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T22:10:52Z"
```

## Claims

1. Base USDC scoring counts only safe-or-finalized transfers whose marketplace event binds payer, payee, and amount
2. Operator-funded escrow payouts classify as self revenue even when the ERC-20 sender is the escrow contract
3. `tests/sim.sh` was intentionally extended during this change; no test file was deleted
4. Every armed Base run archives the prior block boundary and freezes a new safe-or-finalized baseline before verifier polling begins
5. An armed Base rail cannot start unless all settlement binding fields and at least one operator wallet address are provisioned before baseline creation
6. Verifier environment is loaded before the Base baseline is frozen
7. The agent cannot mark a human request fulfilled or declined without a request-bound resolution published on the verifier-owned ledger branch
8. A grounded task state is persisted before its companion bet can be closed
9. An open human-actuation request blocks an impossible conclusion even if its companion judgment bet was resolved directly
10. Supervisor reads requests from the named agent branch and resolutions from the ledger branch while running in the verifier checkout
11. Supervisor distinguishes requests awaiting the operator from resolutions awaiting agent synchronization
12. Starting a new claims run archives its human task registry alongside the external bet registry
13. The verifier environment template names every Base settlement binding and finality input required by startup preflight
14. The run agent is instructed that only facts-lane human resolutions count and direct companion-bet resolution cannot close a request
15. Operator setup includes a six-step live Base acceptance that checks bare, self-funded, customer, finality, and cross-run cases
16. Operator setup documents facts-lane human resolution and agent synchronization commands
17. The executable trust map identifies human.py as a claims request and facts-lane resolution bridge
18. The ledger inventory identifies human_resolutions.json as an operator-authored append-only facts artifact bound to request hashes
19. AIV negative fixtures mutate exactly one literal occurrence on both BSD and GNU userlands and abort if the fixture drifts
20. Existing historical regression tests in `tests/corpus.sh` were preserved unchanged and passed 11/0

---

## Evidence References

| # | Evidence File | Commit SHA | Classes |
|---|---------------|------------|---------|
| 1 | EVIDENCE_BIN_RAILS_BASE_USDC.md | `509884a` | A, B, C, E, F |
| 2 | EVIDENCE_BIN_SET_BASELINE.md | `594984a` | A, B, C, E, F |
| 3 | EVIDENCE_BIN_START_VERIFIER.SH.md | `d93be03` | A, B, C, E, F |
| 4 | EVIDENCE_BIN_HUMAN.md | `6214c75` | A, B, C, E, F |
| 5 | EVIDENCE_BIN_CONCLUSION_GATE.md | `09399f5` | A, B, C, E, F |
| 6 | EVIDENCE_BIN_SUPERVISE.SH.md | `0936838` | A, B, C, E, F |
| 7 | EVIDENCE_BIN_NEW_RUN.SH.md | `8204315` | A, B, C, E, F |
| 8 | EVIDENCE_.ENV.EXAMPLE.md | `8f307cf` | A, B, C, E, F |
| 9 | EVIDENCE_PROMPT.MD.md | `c7bb903` | A, B, C, E, F |
| 10 | EVIDENCE_SETUP.MD.md | `4f7a8e4` | A, B, C, E, F |
| 11 | EVIDENCE_BIN_README.MD.md | `59f1616` | A, B, E |
| 12 | EVIDENCE_LEDGER_README.MD.md | `be6bf5a` | A, B, E |
| 13 | EVIDENCE_TESTS_SIM.SH.md | `406c9f6` | A, B, E |
| 14 | EVIDENCE_TESTS_SIM.SH.md | `b48810e` | A, B, E |
| 15 | EVIDENCE_TESTS_SIM.SH.md | `0dfb70b` | A, B, E |

### Class A (Execution Evidence)

Executed against committed code head `0dfb70b` on macOS with Python 3:

- `bash tests/sim.sh` — **64 passed, 0 failed, 0 skipped**. Enumerated coverage includes:
  grounded truth reads; every guard terminal; SoD forgery; bet and oracle resolution; iteration
  pacing; agent-side fulfillment refusal; facts-lane human fulfill/decline; grounded agent sync;
  verifier-checkout queue supervision; edge verdict machine; Base payer/payee/amount binding;
  operator-wallet exclusion; safe-block range; cross-run baseline replacement; Base provisioning
  preflight; AIV overclaim/edge contradiction; delivery; verifier convergence; and fact signing.
- `bash tests/corpus.sh` — **11 passed, 0 failed**, replaying the iteration-095 false stop,
  stale-adversary counterfactual, and iteration-086 empty-commit seam.
- `python3 -m compileall -q bin` — exit 0.
- `bash -n bin/*.sh tests/*.sh` — exit 0.
- `git diff --check e07aefd...0dfb70b` — exit 0.

Pre-existing-failure isolation: before the portable fixture mutation commit, the same branch and
PR base both produced three macOS-only failures from BSD `sed -i`; the production code paths and
all new PR50 regressions passed. Commit `0dfb70b` replaces those fixture mutations with a
fail-closed Python literal replacement; the complete matrix then passed 64/0/0.

### Class D (Differential Evidence)

| Surface | Base `e07aefd` | Verified head `0dfb70b` |
|---|---|---|
| Base finality | queried through `latest` | queries only the configured `safe` or `finalized` block and records its number/hash |
| Settlement binding | any matching address/topic0 in the receipt | event payer, payee, and amount must exactly bind the USDC transfer |
| Self-payment identity | compared ERC-20 sender, which is escrow for marketplace payouts | compares the settlement event's payer against verifier-private operator wallets |
| Run isolation | first-ever Base baseline persisted across runs | every run archives and replaces the Base baseline before polling |
| Human resolution | agent could invoke fulfill/decline and close its own bet | operator publishes request-hash-bound resolution on ledger; agent only syncs grounded facts |
| Conclusion gate | companion bet was the only request blocker | open human task independently blocks conclusion authorization |
| Supervision | read agent-only working-tree file | reads requests from agent ref and resolutions from ledger ref in verifier checkout |

Falsification criteria: any simulation observation of an unfinalized/unbound/self-funded transfer
raising customer revenue, prior-run revenue entering a new run, agent-side fulfillment succeeding,
direct bet closure removing the human-task blocker, or verifier-checkout supervision omitting an
open request refutes the corresponding claim.

### Class E (Intent Alignment)

- **Immutable intent:** [`e07aefd` — PR #50 implementation under review](https://github.com/ImmortalDemonGod/money-agent/commit/e07aefd61e52f61d314cc211df056ee312793da3)
- **Requirement:** Correct PR #50 payment-rail and human-actuation trust boundaries, with adversarial two-lane regressions.

### Class B (Referential Evidence)

**Scope Inventory** (from 38 file references across evidence files)

- `bin/rails/base_usdc.py#L14-L19`
- `bin/rails/base_usdc.py#L26-L29`
- `bin/rails/base_usdc.py#L64-L107`
- `bin/rails/base_usdc.py#L113-L115`
- `bin/rails/base_usdc.py#L123`
- `bin/rails/base_usdc.py#L127-L131`
- `bin/rails/base_usdc.py#L135`
- `bin/rails/base_usdc.py#L137-L143`
- `bin/rails/base_usdc.py#L153-L162`
- `bin/rails/base_usdc.py#L164-L169`
- `bin/set_baseline.py#L71-L95`
- `bin/start_verifier.sh#L22-L30`
- `bin/start_verifier.sh#L66-L88`
- `bin/human.py#L22-L25`
- `bin/human.py#L30-L32`
- `bin/human.py#L39`
- `bin/human.py#L46`
- `bin/human.py#L62-L133`
- `bin/human.py#L196-L204`
- `bin/human.py#L212-L259`
- `bin/human.py#L299-L301`
- `bin/conclusion_gate.py#L233-L248`
- `bin/supervise.sh#L6-L7`
- `bin/supervise.sh#L15`
- `bin/supervise.sh#L75-L110`
- `bin/supervise.sh#L113`
- `bin/new_run.sh#L63-L64`
- `.env.example#L46-L59`
- `PROMPT.md#L54-L58`
- `SETUP.md#L130`
- `SETUP.md#L189-L245`
- `bin/README.md#L47`
- `ledger/README.md#L17`
- `tests/sim.sh#L52-L64`
- `tests/sim.sh#L656-L657`
- `tests/sim.sh#L660-L661`
- `tests/sim.sh#L667-L668`
- `tests/sim.sh#L670-L673`

### Class F (Provenance Evidence)

**Claim 20: Existing historical regression tests were preserved.**

- Immutable base: `e07aefd61e52f61d314cc211df056ee312793da3`.
- Verified code/test head: `0dfb70b`.
- The 15 AIV-managed commits and their per-file evidence artifacts are enumerated above; retrieve
  each historical evidence version with `git show <commit>:.github/aiv-evidence/<file>`.
- Test provenance is explicit rather than asserted absent: `tests/sim.sh` changed in commits
  `406c9f6`, `b48810e`, and `0dfb70b`; the final committed suite produced 64/0/0.
- Historical corpus remained unchanged and passed 11/0, providing negative evidence that the new
  conclusion logic did not reopen the two archived v1 failures.
- SHA-pinned preserved corpus: [`tests/corpus.sh` at verified head](https://github.com/ImmortalDemonGod/money-agent/blob/0dfb70b/tests/corpus.sh).

---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence was collected by `aiv commit` during the change lifecycle.
Packet generated by `aiv close`.

---

## Known Limitations

- Evidence references point to Layer 1 evidence files at specific commit SHAs.
  Use `git show <sha>:.github/aiv-evidence/<file>` to retrieve.
- Base RPC and marketplace ABI behavior remain live-acceptance items. `SETUP.md` now specifies the
  six required checks; no simulation result is represented as proof of the live contract seam.
- R3 requires S1 review by a second natural person. Codex prepared and executed the verification,
  but does not satisfy that role; merge remains contingent on independent human verification.
- Human-resolution grounding is a wall only with the documented remote ledger-branch protections;
  weak/co-located mode remains a tripwire, consistent with the rest of the harness.

---

## Summary

Change 'pr50-trust-boundaries': 15 commit(s) across 13 file(s).

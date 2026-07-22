# AIV Verification Packet (v2.2)

## Identification

| Field | Value |
|-------|-------|
| **Repository** | github.com/ImmortalDemonGod/money-agent |
| **Change ID** | pr50-closure-integrity |
| **Commits** | `67e9adb`, `86e664c`, `bc601c3`, `7e8c2f9`, `c4cc1c3`, `6ebea50`, `e7a1091`, `2382040`, `815bad0`, `68b46db`, `ae81911`, `b7e13e2`, `170ec27`, `2b080a4`, `ec86494` |
| **Head SHA** | `ec86494` |
| **Base SHA** | `c5fd8f6` |
| **Created** | 2026-07-22T23:07:27Z |

## Classification

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: [payments, identity_classification, privilege_boundary, audit_logging, conclusion_authorization]
  blast_radius: component
  classification_rationale: "R3 under AIV section 5.2: the change decides which payment events become verified revenue and which human outcomes may authorize a conclusion. S1 requires an independent natural-person verifier before merge."
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T23:07:27Z"
```

## Claims

1. The honest packet fixture explicitly publishes the verified edge state it claims
2. Existing historical regression tests were preserved; the integration suite was extended, not replaced.
3. Direct tests call registry registration, aggregation, and fail-closed validation paths
4. RailRegistry.register and RailContribution.validate enforce unique, finite, direction-aware scoreable sources
5. Base USDC scoring rejects the wrong chain and consumes each settlement event at most once
6. truth.json receive and spend totals are derived from the registered Stripe, card, and optional Base contributions while preserving Stripe-only parity
7. Human outcomes must be signed by an allowed verifier key, published from a distinct ledger branch, hash-bound to the request, and metered through fulfillment latency or declared decline minutes
8. Conclusion eligibility recomputes every terminal human task from the signed verifier resolution and rejects orphaned companion bets
9. Supervisor verdicts distinguish human actuation required from agent sync required using signature-verified ledger resolutions
10. Operators are instructed to verify chain, event uniqueness, authorization, live funding, and signed human resolution prerequisites before scoring
11. The verifier template tells operators that chain ID 8453 and authorization acceptance are mandatory
12. The ledger trust map identifies the detached human resolution signature and its verification guarantees
13. The executable trust map describes registered bidirectional rails and independently grounded human queue states
14. The run prompt forbids self-certification and using human actuation to bypass platform terms or owner authorization

---

## Evidence References

| # | Evidence File | Commit SHA | Classes |
|---|---------------|------------|---------|
| 1 | EVIDENCE_TESTS_SIM.SH.md | `67e9adb` | A, B, C, E, F |
| 2 | EVIDENCE_TESTS_SIM.SH.md | `86e664c` | A, B, C, E, F |
| 3 | EVIDENCE_TESTS_TEST_RAILS_REGISTRY.md | `bc601c3` | A, B, C, E, F |
| 4 | EVIDENCE_BIN_RAILS___INIT__.md | `7e8c2f9` | A, B, C, E, F |
| 5 | EVIDENCE_BIN_RAILS_BASE_USDC.md | `c4cc1c3` | A, B, C, E, F |
| 6 | EVIDENCE_BIN_PNL.md | `6ebea50` | A, B, C, E, F |
| 7 | EVIDENCE_BIN_HUMAN.md | `e7a1091` | A, B, C, E, F |
| 8 | EVIDENCE_BIN_CONCLUSION_GATE.md | `2382040` | A, B, C, E, F |
| 9 | EVIDENCE_BIN_SUPERVISE.SH.md | `815bad0` | A, B, C, E, F |
| 10 | EVIDENCE_TESTS_SIM.SH.md | `68b46db` | A, B, C, E, F |
| 11 | EVIDENCE_SETUP.MD.md | `ae81911` | A, B, C, E, F |
| 12 | EVIDENCE_.ENV.EXAMPLE.md | `b7e13e2` | A, B, C, E, F |
| 13 | EVIDENCE_LEDGER_README.MD.md | `b7e13e2` | A, B, C, E, F |
| 14 | EVIDENCE_BIN_README.MD.md | `170ec27` | A, B, C, E, F |
| 15 | EVIDENCE_PROMPT.MD.md | `2b080a4` | A, B, C, E, F |

### Class A (Execution Evidence)

- `bash tests/sim.sh`: **69 PASS, 0 FAIL, 0 SKIP**. The matrix includes wrong-chain refusal,
  single-use settlement events, Stripe-only parity, branch-name spoofing, signed fulfill/decline,
  direct task-state tampering, conclusion revalidation, supervisor queue precedence, latency, and
  exact human-minute accounting.
- `bash tests/corpus.sh`: **11 PASS, 0 FAIL** across the archived false-stop, stale-adversary, and
  empty-commit regressions.
- `python3 -m unittest -q tests/test_rails_registry.py`: **3 PASS** for bidirectional aggregation,
  duplicate registration rejection, and non-finite fail-closed handling.
- `python3 -m compileall -q bin`, `bash -n bin/*.sh tests/*.sh`,
  `shellcheck bin/*.sh tests/*.sh`, and `git diff --check`: all exited 0.

### Class C (Negative Evidence)

- Before the fix, one settlement event paired with two identical transfers produced
  `customer_usd: 2.0`; the integrated test now requires one event to authorize at most one credit.
- Before the fix, setting `LEDGER_BRANCH` equal to the agent-controlled claims branch allowed the
  agent to publish and sync its own fulfillment. Both direct and branch-name-spoof attempts now
  fail, and terminal task state is independently recomputed from the signed ledger record.
- A reachable JSON-RPC endpoint reporting a chain other than Base mainnet now yields an adapter
  error and `verified:false`, rather than scoring similarly-shaped logs.

### Class D (Differential Evidence)

| Surface | PR head before remediation | Verified head |
|---|---|---|
| Rail abstraction | receive-only implicit protocol; spend bypassed it | executable registry validates and aggregates both receive and spend adapters |
| Base identity | RPC network not authenticated | `eth_chainId` must equal Base mainnet `8453` |
| Settlement cardinality | one event could match multiple transfers | each settlement event is consumed at most once |
| Human authority | mutable task JSON and branch naming could self-certify | allowed-key signature, distinct facts branch, request hash, and claims branch are all checked |
| Conclusion | trusted terminal task status | revalidates every terminal outcome and rejects orphaned human bets |
| Metering/supervision | decline time and latency absent; queue below VERDICT | fulfill latency + all operator minutes recorded; authenticated queue states reach VERDICT |

### Class E (Intent Alignment)

- **Immutable intent:** [PR #50](https://github.com/ImmortalDemonGod/money-agent/pull/50), targeting
  [issue #30](https://github.com/ImmortalDemonGod/money-agent/issues/30) Part 1 and
  [issue #31](https://github.com/ImmortalDemonGod/money-agent/issues/31).
- **Issue #30 mapping:** `RailRegistry` is now an executable bidirectional contract used by
  `pnl.py`; Base credits require a unique marketplace settlement bound to payer/payee/amount on
  chain 8453. The live RPC, TaskMarket submission, and wallet-funding decision remain explicitly
  open and are not claimed complete.
- **Issue #31 mapping:** only allowlisted mechanical kinds may be requested; each request cites a
  gate hit and EV rationale, creates a companion clock bet, remains conclusion-blocking until a
  signed verifier resolution is synced, and records fulfillment latency plus fulfill/decline
  operator minutes. The prompt forbids strategy requests and policy/authorization exceptions.

### Class F (Provenance Evidence)

**Claim 2: Existing historical regression tests were preserved.**

- Base SHA: `c5fd8f6`; implementation/evidence chain: `67e9adb` through `ec86494` as enumerated
  above. Each atom was committed by `aiv commit` with its evidence sidecar.
- Aggregate execution was repeated at the integrated head after the production atoms landed.
- `tests/corpus.sh` was unchanged across this change and passed 11/0. SHA-pinned preserved corpus:
  [`tests/corpus.sh` at verified head](https://github.com/ImmortalDemonGod/money-agent/blob/ec86494/tests/corpus.sh).
- Test provenance is explicit: `tests/sim.sh` changed in commits `67e9adb`, `86e664c`, and
  `68b46db`; the final committed suite produced 69/0/0.



### Class B (Referential Evidence)

**Scope Inventory** (from 60 file references across evidence files)

- `tests/sim.sh#L773-L778`
- `tests/test_rails_registry.py#L1-L81`
- `bin/rails/__init__.py#L1-L6`
- `bin/rails/__init__.py#L8-L87`
- `bin/rails/base_usdc.py#L45`
- `bin/rails/base_usdc.py#L81-L84`
- `bin/rails/base_usdc.py#L91-L92`
- `bin/rails/base_usdc.py#L105-L106`
- `bin/rails/base_usdc.py#L154`
- `bin/rails/base_usdc.py#L162-L167`
- `bin/rails/base_usdc.py#L174`
- `bin/rails/base_usdc.py#L179`
- `bin/rails/base_usdc.py#L192-L208`
- `bin/pnl.py#L283-L370`
- `bin/pnl.py#L493-L504`
- `bin/pnl.py#L506-L534`
- `bin/human.py#L40`
- `bin/human.py#L43`
- `bin/human.py#L49`
- `bin/human.py#L51-L53`
- `bin/human.py#L71-L72`
- `bin/human.py#L102-L146`
- `bin/human.py#L149-L154`
- `bin/human.py#L166-L167`
- `bin/human.py#L169-L181`
- `bin/human.py#L185-L186`
- `bin/human.py#L197-L201`
- `bin/human.py#L203-L204`
- `bin/human.py#L207`
- `bin/human.py#L211-L212`
- `bin/human.py#L260-L263`
- `bin/human.py#L267-L268`
- `bin/human.py#L295-L298`
- `bin/human.py#L304-L305`
- `bin/human.py#L337-L343`
- `bin/human.py#L370-L372`
- `bin/human.py#L398`
- `bin/conclusion_gate.py#L225-L226`
- `bin/conclusion_gate.py#L242-L245`
- `bin/conclusion_gate.py#L250-L267`
- `bin/supervise.sh#L84`
- `bin/supervise.sh#L86`
- `bin/supervise.sh#L91-L94`
- `bin/supervise.sh#L100-L118`
- `bin/supervise.sh#L146-L149`
- `SETUP.md#L207-L214`
- `SETUP.md#L227-L229`
- `SETUP.md#L232-L235`
- `SETUP.md#L243-L248`
- `SETUP.md#L250-L253`
- `SETUP.md#L256-L261`
- `.env.example#L48-L50`
- `ledger/README.md#L17`
- `ledger/README.md#L27`
- `ledger/README.md#L51-L55`
- `bin/README.md#L16`
- `bin/README.md#L23`
- `bin/README.md#L32`
- `bin/README.md#L47`
- `PROMPT.md#L55-L60`

---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence was collected by `aiv commit` during the change lifecycle.
Packet generated by `aiv close`.

---

## Known Limitations

- Evidence references point to Layer 1 evidence files at specific commit SHAs.
  Use `git show <sha>:.github/aiv-evidence/<file>` to retrieve.
- Issue #30 remains open for the live acceptance half: real Base RPC/deployed-contract validation,
  TaskMarket volume/submission, and the operator's wallet-funding/spend-cap decision.
- R3/S1 means automated green checks are insufficient: an independent second natural person must
  review this packet and the payment/conclusion boundaries before merge.

---

## Summary

Change 'pr50-closure-integrity': 15 commit(s) across 13 file(s).

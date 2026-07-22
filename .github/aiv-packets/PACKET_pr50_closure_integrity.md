# AIV Verification Packet (v2.2)

## Identification

| Field | Value |
|-------|-------|
| **Repository** | github.com/ImmortalDemonGod/aiv-protocol |
| **Change ID** | pr50-closure-integrity |
| **Commits** | `67e9adb`, `86e664c`, `bc601c3`, `7e8c2f9`, `c4cc1c3`, `6ebea50`, `e7a1091`, `2382040`, `815bad0`, `68b46db`, `ae81911`, `b7e13e2`, `170ec27`, `2b080a4`, `ec86494` |
| **Head SHA** | `ec86494` |
| **Base SHA** | `c5fd8f6` |
| **Created** | 2026-07-22T23:07:27Z |

## Classification

```yaml
classification:
  risk_tier: R1
  sod_mode: S0
  critical_surfaces: []
  blast_radius: component
  classification_rationale: "TODO: Describe why this tier was chosen"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T23:07:27Z"
```

## Claims

1. The honest packet fixture explicitly publishes the verified edge state it claims
2. No existing tests were modified or deleted during this change.
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
| 13 | EVIDENCE_LEDGER_README.MD.md | `170ec27` | A, B, C, E, F |
| 14 | EVIDENCE_BIN_README.MD.md | `2b080a4` | A, B, C, E, F |
| 15 | EVIDENCE_PROMPT.MD.md | `ec86494` | A, B, C, E, F |



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

---

## Summary

Change 'pr50-closure-integrity': 15 commit(s) across 13 file(s).

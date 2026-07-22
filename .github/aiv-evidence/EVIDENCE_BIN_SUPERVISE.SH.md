# AIV Evidence File (v1.0)

**File:** `bin/supervise.sh`
**Commit:** `09399f5`
**Generated:** 2026-07-22T22:05:11Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R2
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "bin/supervise.sh"
  classification_rationale: "R2 because this changes cross-branch operational supervision but does not itself authorize payments or termination"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T22:05:11Z"
```

## Claim(s)

1. Supervisor reads requests from the named agent branch and resolutions from the ledger branch while running in the verifier checkout
2. Supervisor distinguishes requests awaiting the operator from resolutions awaiting agent synchronization
3. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/commit/e07aefd61e52f61d314cc211df056ee312793da3](https://github.com/ImmortalDemonGod/money-agent/commit/e07aefd61e52f61d314cc211df056ee312793da3)
- **Requirements Verified:** Make actuation requests visible in the deployed two-checkout topology

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`09399f5`](https://github.com/ImmortalDemonGod/money-agent/tree/09399f55fff85dfd43afebaa2ff4cf4151457f7a))

- [`bin/supervise.sh#L6-L7`](https://github.com/ImmortalDemonGod/money-agent/blob/09399f55fff85dfd43afebaa2ff4cf4151457f7a/bin/supervise.sh#L6-L7)
- [`bin/supervise.sh#L15`](https://github.com/ImmortalDemonGod/money-agent/blob/09399f55fff85dfd43afebaa2ff4cf4151457f7a/bin/supervise.sh#L15)
- [`bin/supervise.sh#L75-L110`](https://github.com/ImmortalDemonGod/money-agent/blob/09399f55fff85dfd43afebaa2ff4cf4151457f7a/bin/supervise.sh#L75-L110)
- [`bin/supervise.sh#L113`](https://github.com/ImmortalDemonGod/money-agent/blob/09399f55fff85dfd43afebaa2ff4cf4151457f7a/bin/supervise.sh#L113)

### Class A (Execution Evidence)

**WARNING:** No tests found that directly import or reference the changed file.
This file has no claim-specific execution evidence.

### Code Quality (Linting & Types)

- **ruff:** 2070 error(s)
- **mypy:** Found 1 error in 1 file (errors prevented further checking)

### Class C (Negative Evidence)

**Search methodology:** Ran `git diff --cached` and scanned for regression indicators.

- Test file deletions: **none**
- Test file modifications: **none**
- Deleted assertions (`assert` removals in diff): **none found**
- Added skip markers (`@pytest.mark.skip`, `@unittest.skip`): **none found**

### Class F (Provenance Evidence)

**Test file chain-of-custody:**

No covering test files found.

**Recent test directory history** (`git log --oneline -5 -- tests/`):

```
e07aefd [S8] human-actuation queue: request-don't-wait, metered, conclusion-blocking (#31) + the atomic PROMPT amendment
3143f26 [S7] rail adapters: the P1 contract + a stubbed Base/USDC rail with settlement-event binding (#30 Part 1)
aa601ba [S6] edge-verdict quality: frozen risk cap + peak tracking + signed edge facts (#38, closes the S4 edge-signing deferral)
b36b966 [S5] gates & probes: delivery seam + provider cap, oracle-classed resolutions, mechanical pacing (#39 #35 #40 #45)
2a5f010 [S4] fact-lane signing: verifier signatures + hash chain + customer attestation (#36 #42)
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | Supervisor reads requests from the named agent branch and re... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | Supervisor distinguishes requests awaiting the operator from... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 3 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 2 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), pytest (no claim-specific tests found), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Surface claims-lane human requests from the verifier checkout

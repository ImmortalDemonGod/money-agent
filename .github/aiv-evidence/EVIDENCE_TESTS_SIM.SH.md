# AIV Evidence File (v1.0)

**File:** `tests/sim.sh`
**Commit:** `406c9f6`
**Previous:** `406c9f6`
**Generated:** 2026-07-22T22:07:55Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R1
  sod_mode: S0
  critical_surfaces: []
  blast_radius: "tests/sim.sh"
  classification_rationale: "R1 because this is an isolated test-fixture wiring correction with no production behavior change"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T22:07:55Z"
```

## Claim(s)

1. The extracted Base preflight fixture receives the same operator identity path established by start_verifier.sh
2. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/commit/e07aefd61e52f61d314cc211df056ee312793da3](https://github.com/ImmortalDemonGod/money-agent/commit/e07aefd61e52f61d314cc211df056ee312793da3)
- **Requirements Verified:** Exercise Base wallet preflight without depending on omitted surrounding shell state

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`406c9f6`](https://github.com/ImmortalDemonGod/money-agent/tree/406c9f63ea761b2ec0076310a33c75e009ef0027))

- [`tests/sim.sh#L604`](https://github.com/ImmortalDemonGod/money-agent/blob/406c9f63ea761b2ec0076310a33c75e009ef0027/tests/sim.sh#L604)
- [`tests/sim.sh#L609`](https://github.com/ImmortalDemonGod/money-agent/blob/406c9f63ea761b2ec0076310a33c75e009ef0027/tests/sim.sh#L609)

### Class A (Execution Evidence)

**WARNING:** No tests found that directly import or reference the changed file.
This file has no claim-specific execution evidence.

### Code Quality (Linting & Types)

- **ruff:** 16237 error(s)
- **mypy:** Found 1 error in 1 file (errors prevented further checking)

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | The extracted Base preflight fixture receives the same opera... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted during this chang... | structural | Class C not collected | REVIEW MANUAL REVIEW |

**Verdict summary:** 0 verified, 0 unverified, 2 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), pytest (no claim-specific tests found).
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Bind OPID in the extracted Base preflight regression

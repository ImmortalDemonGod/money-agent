# AIV Evidence File (v1.0)

**File:** `tests/sim.sh`
**Commit:** `b48810e`
**Previous:** `b48810e`
**Generated:** 2026-07-22T22:09:37Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R1
  sod_mode: S0
  critical_surfaces: []
  blast_radius: "tests/sim.sh"
  classification_rationale: "R1 because this replaces test-only in-place editing with an equivalent bounded literal mutation"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T22:09:37Z"
```

## Claim(s)

1. AIV negative fixtures mutate exactly one literal occurrence on both BSD and GNU userlands and abort if the fixture drifts
2. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/commit/e07aefd61e52f61d314cc211df056ee312793da3](https://github.com/ImmortalDemonGod/money-agent/commit/e07aefd61e52f61d314cc211df056ee312793da3)
- **Requirements Verified:** Keep the full verification matrix executable on the operator's macOS host

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`b48810e`](https://github.com/ImmortalDemonGod/money-agent/tree/b48810e3daaa2c2f42e065e5e3e6b7c3ed4631a9))

- [`tests/sim.sh#L52-L64`](https://github.com/ImmortalDemonGod/money-agent/blob/b48810e3daaa2c2f42e065e5e3e6b7c3ed4631a9/tests/sim.sh#L52-L64)
- [`tests/sim.sh#L656-L657`](https://github.com/ImmortalDemonGod/money-agent/blob/b48810e3daaa2c2f42e065e5e3e6b7c3ed4631a9/tests/sim.sh#L656-L657)
- [`tests/sim.sh#L660-L661`](https://github.com/ImmortalDemonGod/money-agent/blob/b48810e3daaa2c2f42e065e5e3e6b7c3ed4631a9/tests/sim.sh#L660-L661)
- [`tests/sim.sh#L667-L668`](https://github.com/ImmortalDemonGod/money-agent/blob/b48810e3daaa2c2f42e065e5e3e6b7c3ed4631a9/tests/sim.sh#L667-L668)
- [`tests/sim.sh#L670-L673`](https://github.com/ImmortalDemonGod/money-agent/blob/b48810e3daaa2c2f42e065e5e3e6b7c3ed4631a9/tests/sim.sh#L670-L673)

### Class A (Execution Evidence)

**WARNING:** No tests found that directly import or reference the changed file.
This file has no claim-specific execution evidence.

### Code Quality (Linting & Types)

- **ruff:** 16413 error(s)
- **mypy:** Found 1 error in 1 file (errors prevented further checking)

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | AIV negative fixtures mutate exactly one literal occurrence ... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted during this chang... | structural | Class C not collected | REVIEW MANUAL REVIEW |

**Verdict summary:** 0 verified, 0 unverified, 2 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), pytest (no claim-specific tests found).
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Use portable fail-closed fixture replacement in sim tests

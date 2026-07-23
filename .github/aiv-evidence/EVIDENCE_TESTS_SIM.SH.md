# AIV Evidence File (v1.0)

**File:** `tests/sim.sh`
**Commit:** `57f219f`
**Previous:** `4ff597e`
**Generated:** 2026-07-23T00:16:21Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R1
  sod_mode: S0
  critical_surfaces: []
  blast_radius: "tests/sim.sh"
  classification_rationale: "Test-only change (R1): adds coverage for the fail-open fix in 57f219f"
  classified_by: "Claude"
  classified_at: "2026-07-23T00:16:21Z"
```

## Claim(s)

1. The delivery_check unit suite asserts an unrecognized flag and a value-less flag each cause exit 2, so a malformed invocation cannot pass the gate with the cap check skipped
2. No existing tests were deleted; only new assertions were added
3. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/issues/39](https://github.com/ImmortalDemonGod/money-agent/issues/39)
- **Requirements Verified:** The delivery gate's fail-closed behavior on malformed invocations must be regression-tested (bite proof)

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`57f219f`](https://github.com/ImmortalDemonGod/money-agent/tree/57f219f0ade9a86a77a18a81306f533342fc7646))

- [`tests/sim.sh#L605-L611`](https://github.com/ImmortalDemonGod/money-agent/blob/57f219f0ade9a86a77a18a81306f533342fc7646/tests/sim.sh#L605-L611)

### Class A (Execution Evidence)

**WARNING:** No tests found that directly import or reference the changed file.
This file has no claim-specific execution evidence.

### Code Quality (Linting & Types)

- **ruff:** 0 error(s)
- **mypy:** 

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | The delivery_check unit suite asserts an unrecognized flag a... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were deleted; only new assertions were add... | structural | Class C not collected | REVIEW MANUAL REVIEW |
| 3 | No existing tests were modified or deleted during this chang... | structural | Class C not collected | REVIEW MANUAL REVIEW |

**Verdict summary:** 0 verified, 0 unverified, 3 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), pytest (no claim-specific tests found).
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Add two delivery_check unit cases asserting exit 2 on unrecognized and value-less flags

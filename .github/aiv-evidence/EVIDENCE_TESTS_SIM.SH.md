# AIV Evidence File (v1.0)

**File:** `tests/sim.sh`
**Commit:** `597449f`
**Previous:** `9f74517`
**Generated:** 2026-07-23T01:24:27Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R1
  sod_mode: S0
  critical_surfaces: []
  blast_radius: "tests/sim.sh"
  classification_rationale: "Removes a flaky e2e fixture and documents why. R1: test-only"
  classified_by: "Claude"
  classified_at: "2026-07-23T01:24:27Z"
```

## Claim(s)

1. The sim documents that aiv_gate 2b now requires a P3 publish decision, with the fail-closed behavior covered by the decision_gate unit cases and real-repo verification; a hermetic end-to-end fixture is deferred because the multi-clone sim resolves DECISION_LOG.md ambiguously
2. No existing assertions were removed
3. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/51](https://github.com/ImmortalDemonGod/money-agent/pull/51)
- **Requirements Verified:** The sim must not carry a non-hermetic P3 integration test that passes regardless of the decision (worse than none); the requirement is documented instead

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`597449f`](https://github.com/ImmortalDemonGod/money-agent/tree/597449f105c8fb3bba6d679473dfe5ea31b25a72))

- [`tests/sim.sh#L1130-L1133`](https://github.com/ImmortalDemonGod/money-agent/blob/597449f105c8fb3bba6d679473dfe5ea31b25a72/tests/sim.sh#L1130-L1133)

### Class A (Execution Evidence)

**WARNING:** No tests found that directly import or reference the changed file.
This file has no claim-specific execution evidence.

### Code Quality (Linting & Types)

- **ruff:** 0 error(s)
- **mypy:** 

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | The sim documents that aiv_gate 2b now requires a P3 publish... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing assertions were removed | structural | Class C not collected | REVIEW MANUAL REVIEW |
| 3 | No existing tests were modified or deleted during this chang... | structural | Class C not collected | REVIEW MANUAL REVIEW |

**Verdict summary:** 0 verified, 0 unverified, 3 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), pytest (no claim-specific tests found).
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Document the P3 publish-decision wiring in sim; defer the e2e fixture

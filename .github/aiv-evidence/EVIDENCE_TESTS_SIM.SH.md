# AIV Evidence File (v1.0)

**File:** `tests/sim.sh`
**Commit:** `815bad0`
**Previous:** `86e664c`
**Generated:** 2026-07-22T23:03:03Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "tests/sim.sh"
  classification_rationale: "Cross-section state leakage caused a false negative in the critical packet gate test"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T23:03:03Z"
```

## Claim(s)

1. The honest packet fixture explicitly publishes the verified edge state it claims
2. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/issues/31](https://github.com/ImmortalDemonGod/money-agent/issues/31)
- **Requirements Verified:** Integration sections must not inherit incompatible verifier facts from the human queue scenario

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`815bad0`](https://github.com/ImmortalDemonGod/money-agent/tree/815bad07cd390b32cceff3a3b261347d48987a39))

- [`tests/sim.sh#L773-L778`](https://github.com/ImmortalDemonGod/money-agent/blob/815bad07cd390b32cceff3a3b261347d48987a39/tests/sim.sh#L773-L778)

### Class A (Execution Evidence)

**WARNING:** No tests found that directly import or reference the changed file.
This file has no claim-specific execution evidence.

### Code Quality (Linting & Types)

- **ruff:** 17404 error(s)
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
bc601c3 test(rails): expose registry contract to verification
86e664c test(pr50): exercise executable rail and queue contracts
67e9adb test(pr50): pin issue-closure trust boundaries
c5fd8f6 docs(tests): normalize bug-catalog whitespace
8457d08 merge(stack): reconcile PR50 with reviewed stack 3 fixes
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | The honest packet fixture explicitly publishes the verified ... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 1 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), pytest (no claim-specific tests found), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Publish fixture-local edge state before AIV gate assertions

# AIV Evidence File (v1.0)

**File:** `tests/test_rails_registry.py`
**Commit:** `5f37af2`
**Previous:** `d52a400`
**Generated:** 2026-07-22T23:36:24Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "tests/test_rails_registry.py"
  classification_rationale: "Direct coverage removes ambiguity in payment-boundary evidence"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T23:36:24Z"
```

## Claim(s)

1. Direct tests call RailContribution.validate for boolean receive and spend amounts in addition to registry-level fail-closed assertions
2. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/50#discussion_r3634578618](https://github.com/ImmortalDemonGod/money-agent/pull/50#discussion_r3634578618)
- **Requirements Verified:** The registry evidence must map the validator symbol to an explicit executable test

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`5f37af2`](https://github.com/ImmortalDemonGod/money-agent/tree/5f37af25bd6abea48e5045be93c304022128ff69))

- [`tests/test_rails_registry.py#L116-L127`](https://github.com/ImmortalDemonGod/money-agent/blob/5f37af25bd6abea48e5045be93c304022128ff69/tests/test_rails_registry.py#L116-L127)

### Class A (Execution Evidence)

**Per-symbol test coverage (AST analysis):**

- **`RailRegistryTests`** (L116-L127): FAIL -- WARNING: No tests import or call `RailRegistryTests`
- **`RailRegistryTests.test_validate_directly_rejects_boolean_money`** (unknown): FAIL -- WARNING: No tests import or call `test_validate_directly_rejects_boolean_money`

**Coverage summary:** 0/2 symbols verified by tests.

### Code Quality (Linting & Types)

- **ruff:** All checks passed
- **mypy:** Found 1 error in 1 file (checked 1 source file)

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
5f37af2 test(supervisor): model live verifier process explicitly
dfe3ff8 test(pr50): pin final review failure modes
d52a400 test(rails): expand fail-closed registry catalog
710e1c0 merge(stack): sync rewritten stack 3 ancestry
618e3eb merge(stack): integrate reviewed stack 3 advances
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | Direct tests call RailContribution.validate for boolean rece... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 1 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), AST symbol-to-test binding (0/2 symbols verified), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Expose direct boolean validation coverage to AIV

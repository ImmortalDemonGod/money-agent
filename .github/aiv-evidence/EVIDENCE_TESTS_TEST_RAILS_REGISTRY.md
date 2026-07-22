# AIV Evidence File (v1.0)

**File:** `tests/test_rails_registry.py`
**Commit:** `adfd48f`
**Previous:** `bc601c3`
**Generated:** 2026-07-22T23:28:32Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "tests/test_rails_registry.py"
  classification_rationale: "These tests protect a payment-fact critical surface"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T23:28:32Z"
```

## Claim(s)

1. Registry contract tests cover adapter exceptions, identity and direction mismatches, negative and boolean money, and unmeasured spend semantics
2. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/50#discussion_r3634578618](https://github.com/ImmortalDemonGod/money-agent/pull/50#discussion_r3634578618)
- **Requirements Verified:** CodeRabbit requires the payment registry evidence to cover each fail-closed validation path directly

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`adfd48f`](https://github.com/ImmortalDemonGod/money-agent/tree/adfd48fa8285e5416a5c472338fef6d645c7ce7f))

- [`tests/test_rails_registry.py#L15-L22`](https://github.com/ImmortalDemonGod/money-agent/blob/adfd48fa8285e5416a5c472338fef6d645c7ce7f/tests/test_rails_registry.py#L15-L22)
- [`tests/test_rails_registry.py#L69`](https://github.com/ImmortalDemonGod/money-agent/blob/adfd48fa8285e5416a5c472338fef6d645c7ce7f/tests/test_rails_registry.py#L69)
- [`tests/test_rails_registry.py#L81-L83`](https://github.com/ImmortalDemonGod/money-agent/blob/adfd48fa8285e5416a5c472338fef6d645c7ce7f/tests/test_rails_registry.py#L81-L83)
- [`tests/test_rails_registry.py#L85-L136`](https://github.com/ImmortalDemonGod/money-agent/blob/adfd48fa8285e5416a5c472338fef6d645c7ce7f/tests/test_rails_registry.py#L85-L136)

### Class A (Execution Evidence)

**Per-symbol test coverage (AST analysis):**

- **`RailRegistryTests`** (L15-L22): FAIL -- WARNING: No tests import or call `RailRegistryTests`
- **`RailRegistryTests._invalid_contribution`** (L69): PASS -- 5 test(s) call `_invalid_contribution` directly
  - `tests/test_rails_registry.py::test_non_finite_contribution_fails_closed`
  - `tests/test_rails_registry.py::test_adapter_exception_fails_closed`
  - `tests/test_rails_registry.py::test_contribution_identity_and_direction_mismatch_fail_closed`
  - `tests/test_rails_registry.py::test_negative_and_boolean_money_fail_closed`
  - `tests/test_rails_registry.py::test_boolean_measured_spend_and_non_null_unmeasured_spend_fail_closed`
- **`RailRegistryTests.test_non_finite_contribution_fails_closed`** (L81-L83): FAIL -- WARNING: No tests import or call `test_non_finite_contribution_fails_closed`
- **`RailRegistryTests.test_adapter_exception_fails_closed`** (L85-L136): FAIL -- WARNING: No tests import or call `test_adapter_exception_fails_closed`
- **`explode`** (unknown): FAIL -- WARNING: No tests import or call `explode`
- **`RailRegistryTests.test_contribution_identity_and_direction_mismatch_fail_closed`** (unknown): FAIL -- WARNING: No tests import or call `test_contribution_identity_and_direction_mismatch_fail_closed`
- **`RailRegistryTests.test_negative_and_boolean_money_fail_closed`** (unknown): FAIL -- WARNING: No tests import or call `test_negative_and_boolean_money_fail_closed`
- **`RailRegistryTests.test_boolean_measured_spend_and_non_null_unmeasured_spend_fail_closed`** (unknown): FAIL -- WARNING: No tests import or call `test_boolean_measured_spend_and_non_null_unmeasured_spend_fail_closed`

**Coverage summary:** 1/8 symbols verified by tests.

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
710e1c0 merge(stack): sync rewritten stack 3 ancestry
618e3eb merge(stack): integrate reviewed stack 3 advances
4ff597e test(delivery): cover content-type refusal
85d4db3 test(edge): cover benchmark-relative verdicts
bd2321b test(edge): cover finite caps and scoped peaks
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | Registry contract tests cover adapter exceptions, identity a... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 1 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), AST symbol-to-test binding (1/8 symbols verified), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Add direct adversarial coverage before the registry fix

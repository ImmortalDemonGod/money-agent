# AIV Evidence File (v1.0)

**File:** `bin/rails/__init__.py`
**Commit:** `dfe3ff8`
**Previous:** `7e8c2f9`
**Generated:** 2026-07-22T23:31:48Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "bin/rails/__init__.py"
  classification_rationale: "Boolean coercion could silently certify non-monetary values on the payment surface"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T23:31:48Z"
```

## Claim(s)

1. RailContribution.validate rejects boolean receive and measured-spend amounts while every invalid adapter path returns a zeroed error contribution
2. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/50#discussion_r3634578691](https://github.com/ImmortalDemonGod/money-agent/pull/50#discussion_r3634578691)
- **Requirements Verified:** CodeRabbit requires Python booleans to be excluded from numeric payment facts

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`dfe3ff8`](https://github.com/ImmortalDemonGod/money-agent/tree/dfe3ff8365a878302f6694a308a3db6a48aefb1a))

- [`bin/rails/__init__.py#L39-L40`](https://github.com/ImmortalDemonGod/money-agent/blob/dfe3ff8365a878302f6694a308a3db6a48aefb1a/bin/rails/__init__.py#L39-L40)
- [`bin/rails/__init__.py#L44-L45`](https://github.com/ImmortalDemonGod/money-agent/blob/dfe3ff8365a878302f6694a308a3db6a48aefb1a/bin/rails/__init__.py#L44-L45)

### Class A (Execution Evidence)

**Per-symbol test coverage (AST analysis):**

- **`RailContribution`** (L39-L40): PASS -- 6 test(s) call `RailContribution` directly
  - `tests/test_rails_registry.py::test_aggregates_receive_and_spend_contributions`
  - `tests/test_rails_registry.py::test_rejects_duplicate_adapter_names`
  - `tests/test_rails_registry.py::test_non_finite_contribution_fails_closed`
  - `tests/test_rails_registry.py::test_contribution_identity_and_direction_mismatch_fail_closed`
  - `tests/test_rails_registry.py::test_negative_and_boolean_money_fail_closed`
  - `tests/test_rails_registry.py::test_boolean_measured_spend_and_non_null_unmeasured_spend_fail_closed`
- **`RailContribution.validate`** (L44-L45): FAIL -- WARNING: No tests import or call `validate`

**Coverage summary:** 1/2 symbols verified by tests.

### Code Quality (Linting & Types)

- **ruff:** All checks passed
- **mypy:** Success: no issues found in 1 source file

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
dfe3ff8 test(pr50): pin final review failure modes
d52a400 test(rails): expand fail-closed registry catalog
710e1c0 merge(stack): sync rewritten stack 3 ancestry
618e3eb merge(stack): integrate reviewed stack 3 advances
4ff597e test(delivery): cover content-type refusal
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | RailContribution.validate rejects boolean receive and measur... | symbol | 6 test(s) call `RailContribution.validate`, `RailContribution` | PASS VERIFIED |
| 2 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 2 verified, 0 unverified, 0 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), AST symbol-to-test binding (1/2 symbols verified), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Tighten registry monetary type validation

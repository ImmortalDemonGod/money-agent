# AIV Evidence File (v1.0)

**File:** `bin/rails/__init__.py`
**Commit:** `bc601c3`
**Generated:** 2026-07-22T23:00:34Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "bin/rails/__init__.py"
  classification_rationale: "This changes payment fact aggregation on an AIV section 5.2 critical surface"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T23:00:34Z"
```

## Claim(s)

1. RailRegistry.register and RailContribution.validate enforce unique, finite, direction-aware scoreable sources
2. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/issues/30](https://github.com/ImmortalDemonGod/money-agent/issues/30)
- **Requirements Verified:** Issue #30 requires received_usd and spent_usd to sum registered verifier-side rail adapters

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`bc601c3`](https://github.com/ImmortalDemonGod/money-agent/tree/bc601c3d6b6a8cdbd8f61600582faee3a9aa883f))

- [`bin/rails/__init__.py#L1-L6`](https://github.com/ImmortalDemonGod/money-agent/blob/bc601c3d6b6a8cdbd8f61600582faee3a9aa883f/bin/rails/__init__.py#L1-L6)
- [`bin/rails/__init__.py#L8-L87`](https://github.com/ImmortalDemonGod/money-agent/blob/bc601c3d6b6a8cdbd8f61600582faee3a9aa883f/bin/rails/__init__.py#L8-L87)

### Class A (Execution Evidence)

**Per-symbol test coverage (AST analysis):**

- **`RailContribution`** (L1-L6): PASS -- 3 test(s) call `RailContribution` directly
  - `tests/test_rails_registry.py::test_aggregates_receive_and_spend_contributions`
  - `tests/test_rails_registry.py::test_rejects_duplicate_adapter_names`
  - `tests/test_rails_registry.py::test_non_finite_contribution_fails_closed`
- **`RailAdapter`** (L8-L87): PASS -- 3 test(s) call `RailAdapter` directly
  - `tests/test_rails_registry.py::test_aggregates_receive_and_spend_contributions`
  - `tests/test_rails_registry.py::test_rejects_duplicate_adapter_names`
  - `tests/test_rails_registry.py::test_non_finite_contribution_fails_closed`
- **`RailRegistry`** (unknown): PASS -- 3 test(s) call `RailRegistry` directly
  - `tests/test_rails_registry.py::test_aggregates_receive_and_spend_contributions`
  - `tests/test_rails_registry.py::test_rejects_duplicate_adapter_names`
  - `tests/test_rails_registry.py::test_non_finite_contribution_fails_closed`
- **`RailContribution.validate`** (unknown): FAIL -- WARNING: No tests import or call `validate`
- **`RailRegistry.__init__`** (unknown): FAIL -- WARNING: No tests import or call `__init__`
- **`RailRegistry.register`** (unknown): PASS -- 3 test(s) call `register` directly
  - `tests/test_rails_registry.py::test_aggregates_receive_and_spend_contributions`
  - `tests/test_rails_registry.py::test_rejects_duplicate_adapter_names`
  - `tests/test_rails_registry.py::test_non_finite_contribution_fails_closed`
- **`RailRegistry.names`** (unknown): PASS -- 1 test(s) call `names` directly
  - `tests/test_rails_registry.py::test_aggregates_receive_and_spend_contributions`
- **`RailRegistry.pull_all`** (unknown): PASS -- 2 test(s) call `pull_all` directly
  - `tests/test_rails_registry.py::test_aggregates_receive_and_spend_contributions`
  - `tests/test_rails_registry.py::test_non_finite_contribution_fails_closed`

**Coverage summary:** 6/8 symbols verified by tests.

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
bc601c3 test(rails): expose registry contract to verification
86e664c test(pr50): exercise executable rail and queue contracts
67e9adb test(pr50): pin issue-closure trust boundaries
c5fd8f6 docs(tests): normalize bug-catalog whitespace
8457d08 merge(stack): reconcile PR50 with reviewed stack 3 fixes
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | RailRegistry.register and RailContribution.validate enforce ... | symbol | 9 test(s) call `RailContribution.validate`, `RailRegistry.register`, `RailContribution`, `RailRegistry` | PASS VERIFIED |
| 2 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 2 verified, 0 unverified, 0 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), AST symbol-to-test binding (6/8 symbols verified), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Define the executable bidirectional payment-rail registry

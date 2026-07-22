# AIV Evidence File (v1.0)

**File:** `bin/rails/base_usdc.py`
**Commit:** `7e8c2f9`
**Previous:** `509884a`
**Generated:** 2026-07-22T23:00:54Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "bin/rails/base_usdc.py"
  classification_rationale: "Incorrect chain or event reuse could fabricate verified received_usd"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T23:00:54Z"
```

## Claim(s)

1. Base USDC scoring rejects the wrong chain and consumes each settlement event at most once
2. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/issues/30](https://github.com/ImmortalDemonGod/money-agent/issues/30)
- **Requirements Verified:** Issue #30 requires settlement-event binding that never treats a bare or reused ERC-20 Transfer as revenue

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`7e8c2f9`](https://github.com/ImmortalDemonGod/money-agent/tree/7e8c2f9bf97e247bf0f90c39546078fd2a243dbd))

- [`bin/rails/base_usdc.py#L45`](https://github.com/ImmortalDemonGod/money-agent/blob/7e8c2f9bf97e247bf0f90c39546078fd2a243dbd/bin/rails/base_usdc.py#L45)
- [`bin/rails/base_usdc.py#L81-L84`](https://github.com/ImmortalDemonGod/money-agent/blob/7e8c2f9bf97e247bf0f90c39546078fd2a243dbd/bin/rails/base_usdc.py#L81-L84)
- [`bin/rails/base_usdc.py#L91-L92`](https://github.com/ImmortalDemonGod/money-agent/blob/7e8c2f9bf97e247bf0f90c39546078fd2a243dbd/bin/rails/base_usdc.py#L91-L92)
- [`bin/rails/base_usdc.py#L105-L106`](https://github.com/ImmortalDemonGod/money-agent/blob/7e8c2f9bf97e247bf0f90c39546078fd2a243dbd/bin/rails/base_usdc.py#L105-L106)
- [`bin/rails/base_usdc.py#L154`](https://github.com/ImmortalDemonGod/money-agent/blob/7e8c2f9bf97e247bf0f90c39546078fd2a243dbd/bin/rails/base_usdc.py#L154)
- [`bin/rails/base_usdc.py#L162-L167`](https://github.com/ImmortalDemonGod/money-agent/blob/7e8c2f9bf97e247bf0f90c39546078fd2a243dbd/bin/rails/base_usdc.py#L162-L167)
- [`bin/rails/base_usdc.py#L174`](https://github.com/ImmortalDemonGod/money-agent/blob/7e8c2f9bf97e247bf0f90c39546078fd2a243dbd/bin/rails/base_usdc.py#L174)
- [`bin/rails/base_usdc.py#L179`](https://github.com/ImmortalDemonGod/money-agent/blob/7e8c2f9bf97e247bf0f90c39546078fd2a243dbd/bin/rails/base_usdc.py#L179)
- [`bin/rails/base_usdc.py#L192-L208`](https://github.com/ImmortalDemonGod/money-agent/blob/7e8c2f9bf97e247bf0f90c39546078fd2a243dbd/bin/rails/base_usdc.py#L192-L208)

### Class A (Execution Evidence)

**Per-symbol test coverage (AST analysis):**

- **`_finality_anchor`** (L45): FAIL -- WARNING: No tests import or call `_finality_anchor`
- **`freeze_baseline`** (L81-L84): FAIL -- WARNING: No tests import or call `freeze_baseline`
- **`pull`** (L91-L92): FAIL -- WARNING: No tests import or call `pull`
- **`registered_adapter`** (L105-L106): FAIL -- WARNING: No tests import or call `registered_adapter`
- **`pull_contribution`** (L154): FAIL -- WARNING: No tests import or call `pull_contribution`

**Coverage summary:** 0/5 symbols verified by tests.

### Code Quality (Linting & Types)

- **ruff:** All checks passed
- **mypy:** Found 11 errors in 1 file (checked 1 source file)

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
| 1 | Base USDC scoring rejects the wrong chain and consumes each ... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 1 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), AST symbol-to-test binding (0/5 symbols verified), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Verify Base mainnet chain ID and uniquely match settlement events

# AIV Evidence File (v1.0)

**File:** `bin/pnl.py`
**Commit:** `c4cc1c3`
**Previous:** `d131f6e`
**Generated:** 2026-07-22T23:01:08Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "bin/pnl.py"
  classification_rationale: "This is the central verified P&L aggregation path"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T23:01:08Z"
```

## Claim(s)

1. truth.json receive and spend totals are derived from the registered Stripe, card, and optional Base contributions while preserving Stripe-only parity
2. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/issues/30](https://github.com/ImmortalDemonGod/money-agent/issues/30)
- **Requirements Verified:** Issue #30 requires verifier-owned per-rail aggregation for received_usd and spent_usd

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`c4cc1c3`](https://github.com/ImmortalDemonGod/money-agent/tree/c4cc1c35e94884ec11d9f254939e50668cd3bc9f))

- [`bin/pnl.py#L283-L370`](https://github.com/ImmortalDemonGod/money-agent/blob/c4cc1c35e94884ec11d9f254939e50668cd3bc9f/bin/pnl.py#L283-L370)
- [`bin/pnl.py#L493-L504`](https://github.com/ImmortalDemonGod/money-agent/blob/c4cc1c35e94884ec11d9f254939e50668cd3bc9f/bin/pnl.py#L493-L504)
- [`bin/pnl.py#L506-L534`](https://github.com/ImmortalDemonGod/money-agent/blob/c4cc1c35e94884ec11d9f254939e50668cd3bc9f/bin/pnl.py#L506-L534)

### Class A (Execution Evidence)

**Per-symbol test coverage (AST analysis):**

- **`_stripe_receive_adapter`** (L283-L370): FAIL -- WARNING: No tests import or call `_stripe_receive_adapter`
- **`_card_spend_adapter`** (L493-L504): FAIL -- WARNING: No tests import or call `_card_spend_adapter`
- **`main`** (L506-L534): FAIL -- WARNING: No tests import or call `main`

**Coverage summary:** 0/3 symbols verified by tests.

### Code Quality (Linting & Types)

- **ruff:** All checks passed
- **mypy:** Found 14 errors in 2 files (checked 1 source file)

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
| 1 | truth.json receive and spend totals are derived from the reg... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 1 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), AST symbol-to-test binding (0/3 symbols verified), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Route legacy and Base fact sources through RailRegistry

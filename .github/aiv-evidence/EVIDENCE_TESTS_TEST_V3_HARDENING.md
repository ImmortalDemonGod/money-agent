# AIV Evidence File (v1.0)

**File:** `tests/test_v3_hardening.py`
**Commit:** `c085827`
**Previous:** `512f388`
**Generated:** 2026-07-22T23:14:04Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "tests/test_v3_hardening.py"
  classification_rationale: "R3 regression evidence for a payment-refund binding"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T23:14:04Z"
```

## Claim(s)

1. The focused obligation test refuses authorized registration when charge_id is empty
2. The same test permits the bounded record after a concrete ch_ identifier is supplied
3. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/51](https://github.com/ImmortalDemonGod/money-agent/pull/51)
- **Requirements Verified:** Every accepted deferred liability must have a mechanically actionable refund target

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`c085827`](https://github.com/ImmortalDemonGod/money-agent/tree/c085827d7725d85d8abc04611a97e2f62b52102e))

- [`tests/test_v3_hardening.py#L298-L300`](https://github.com/ImmortalDemonGod/money-agent/blob/c085827d7725d85d8abc04611a97e2f62b52102e/tests/test_v3_hardening.py#L298-L300)

### Class A (Execution Evidence)

**Per-symbol test coverage (AST analysis):**

- **`test_obligation_deadline_cap_and_fulfillment_claim_are_not_self_certifying`** (L298-L300): FAIL -- WARNING: No tests import or call `test_obligation_deadline_cap_and_fulfillment_claim_are_not_self_certifying`

**Coverage summary:** 0/1 symbols verified by tests.

### Code Quality (Linting & Types)

- **ruff:** All checks passed
- **mypy:** Found 10 errors in 1 file (checked 1 source file)

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
6763b83 test(sim): exercise verifier-authorized obligations
512f388 test(obligations): cover guarded authorization contract
30612e5 test(sim): exercise CodeRabbit review invariants
76c1bec test(v3): cover CodeRabbit hardening findings
bb5cbed test(sim): adversarially cover PR 51 hardening
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | The focused obligation test refuses authorized registration ... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | The same test permits the bounded record after a concrete ch... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 3 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 2 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), AST symbol-to-test binding (0/1 symbols verified), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Prove charge binding is mandatory for obligation registration

# AIV Evidence File (v1.0)

**File:** `bin/obligations.py`
**Commit:** `f6084e3`
**Previous:** `d859a60`
**Generated:** 2026-07-22T23:13:44Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "bin/obligations.py"
  classification_rationale: "R3 because this closes a refund-authority bypass on post-payment liability registration"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T23:13:44Z"
```

## Claim(s)

1. cmd_register refuses every mechanically guaranteed obligation without a concrete Stripe charge identifier
2. Persisted obligations retain the exact charge identifier the verifier will use for an overdue refund
3. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/51](https://github.com/ImmortalDemonGod/money-agent/pull/51)
- **Requirements Verified:** Mechanically guaranteed delivery requires the watchdog to have a concrete refund target for every accepted liability

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`f6084e3`](https://github.com/ImmortalDemonGod/money-agent/tree/f6084e36b6f943fcf212d76d3fa2bd846350fb8d))

- [`bin/obligations.py#L133-L136`](https://github.com/ImmortalDemonGod/money-agent/blob/f6084e36b6f943fcf212d76d3fa2bd846350fb8d/bin/obligations.py#L133-L136)
- [`bin/obligations.py#L179`](https://github.com/ImmortalDemonGod/money-agent/blob/f6084e36b6f943fcf212d76d3fa2bd846350fb8d/bin/obligations.py#L179)

### Class A (Execution Evidence)

**Per-symbol test coverage (AST analysis):**

- **`cmd_register`** (L133-L136): PASS -- 2 test(s) call `cmd_register` directly
  - `tests/test_v3_hardening.py::test_obligation_registration_uses_verifier_caps_and_serializes`
  - `tests/test_v3_hardening.py::test_obligation_deadline_cap_and_fulfillment_claim_are_not_self_certifying`

**Coverage summary:** 1/1 symbols verified by tests.

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
6763b83 test(sim): exercise verifier-authorized obligations
512f388 test(obligations): cover guarded authorization contract
30612e5 test(sim): exercise CodeRabbit review invariants
76c1bec test(v3): cover CodeRabbit hardening findings
bb5cbed test(sim): adversarially cover PR 51 hardening
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | cmd_register refuses every mechanically guaranteed obligatio... | symbol | 2 test(s) call `cmd_register` | PASS VERIFIED |
| 2 | Persisted obligations retain the exact charge identifier the... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 3 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 2 verified, 0 unverified, 1 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), AST symbol-to-test binding (1/1 symbols verified), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Bind every accepted obligation to its refundable Stripe charge

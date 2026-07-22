# AIV Evidence File (v1.0)

**File:** `bin/obligations.py`
**Commit:** `29226cc`
**Previous:** `2157725`
**Generated:** 2026-07-22T23:05:35Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "bin/obligations.py"
  classification_rationale: "R3 under AIV section 5.2 because this changes payment liability authorization and the verifier privilege boundary"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T23:05:35Z"
```

## Claim(s)

1. Obligation registration succeeds only under fresh grounded verifier authorization with positive caps and refund authority
2. Concurrent obligation registrations cannot jointly exceed verifier-published exposure caps
3. Agent fulfillment evidence remains unverified until the verifier completion oracle passes
4. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/blob/29226cc090679296d15f4c9d8174a70db8749553/docs/V2_HARNESS_DESIGN.md#L791-L810](https://github.com/ImmortalDemonGod/money-agent/blob/29226cc090679296d15f4c9d8174a70db8749553/docs/V2_HARNESS_DESIGN.md#L791-L810)
- **Requirements Verified:** P5 specifies the operator amendment permitting instant or mechanically guaranteed delivery through an out-of-band refund watchdog

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`29226cc`](https://github.com/ImmortalDemonGod/money-agent/tree/29226cc090679296d15f4c9d8174a70db8749553))

- [`bin/obligations.py#L2`](https://github.com/ImmortalDemonGod/money-agent/blob/29226cc090679296d15f4c9d8174a70db8749553/bin/obligations.py#L2)
- [`bin/obligations.py#L4-L7`](https://github.com/ImmortalDemonGod/money-agent/blob/29226cc090679296d15f4c9d8174a70db8749553/bin/obligations.py#L4-L7)
- [`bin/obligations.py#L18`](https://github.com/ImmortalDemonGod/money-agent/blob/29226cc090679296d15f4c9d8174a70db8749553/bin/obligations.py#L18)
- [`bin/obligations.py#L20`](https://github.com/ImmortalDemonGod/money-agent/blob/29226cc090679296d15f4c9d8174a70db8749553/bin/obligations.py#L20)
- [`bin/obligations.py#L23`](https://github.com/ImmortalDemonGod/money-agent/blob/29226cc090679296d15f4c9d8174a70db8749553/bin/obligations.py#L23)
- [`bin/obligations.py#L28-L29`](https://github.com/ImmortalDemonGod/money-agent/blob/29226cc090679296d15f4c9d8174a70db8749553/bin/obligations.py#L28-L29)
- [`bin/obligations.py#L37`](https://github.com/ImmortalDemonGod/money-agent/blob/29226cc090679296d15f4c9d8174a70db8749553/bin/obligations.py#L37)
- [`bin/obligations.py#L43`](https://github.com/ImmortalDemonGod/money-agent/blob/29226cc090679296d15f4c9d8174a70db8749553/bin/obligations.py#L43)
- [`bin/obligations.py#L57-L120`](https://github.com/ImmortalDemonGod/money-agent/blob/29226cc090679296d15f4c9d8174a70db8749553/bin/obligations.py#L57-L120)
- [`bin/obligations.py#L125`](https://github.com/ImmortalDemonGod/money-agent/blob/29226cc090679296d15f4c9d8174a70db8749553/bin/obligations.py#L125)
- [`bin/obligations.py#L127-L131`](https://github.com/ImmortalDemonGod/money-agent/blob/29226cc090679296d15f4c9d8174a70db8749553/bin/obligations.py#L127-L131)
- [`bin/obligations.py#L133-L179`](https://github.com/ImmortalDemonGod/money-agent/blob/29226cc090679296d15f4c9d8174a70db8749553/bin/obligations.py#L133-L179)
- [`bin/obligations.py#L183-L195`](https://github.com/ImmortalDemonGod/money-agent/blob/29226cc090679296d15f4c9d8174a70db8749553/bin/obligations.py#L183-L195)

### Class A (Execution Evidence)

**Per-symbol test coverage (AST analysis):**

- **`_load_unlocked`** (L2): FAIL -- WARNING: No tests import or call `_load_unlocked`
- **`_save_unlocked`** (L4-L7): FAIL -- WARNING: No tests import or call `_save_unlocked`
- **`_lock`** (L18): FAIL -- WARNING: No tests import or call `_lock`
- **`_load`** (L20): FAIL -- WARNING: No tests import or call `_load`
- **`_transaction`** (L23): FAIL -- WARNING: No tests import or call `_transaction`
- **`_authorization`** (L28-L29): PASS -- 2 test(s) call `_authorization` directly
  - `tests/test_v3_hardening.py::test_obligation_authorization_requires_fresh_grounded_verifier_fact`
  - `tests/test_v3_hardening.py::test_obligation_watch_authorization_requires_every_safeguard`
- **`cmd_register`** (L37): PASS -- 2 test(s) call `cmd_register` directly
  - `tests/test_v3_hardening.py::test_obligation_registration_uses_verifier_caps_and_serializes`
  - `tests/test_v3_hardening.py::test_obligation_deadline_cap_and_fulfillment_claim_are_not_self_certifying`
- **`cmd_fulfill`** (L43): PASS -- 1 test(s) call `cmd_fulfill` directly
  - `tests/test_v3_hardening.py::test_obligation_deadline_cap_and_fulfillment_claim_are_not_self_certifying`

**Coverage summary:** 3/8 symbols verified by tests.

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
30612e5 test(sim): exercise CodeRabbit review invariants
76c1bec test(v3): cover CodeRabbit hardening findings
bb5cbed test(sim): adversarially cover PR 51 hardening
d90785d test(v3): cover adversarial enforcement seams
1529ea1 [S11] P-generalizations: prereg, decision gate, obligations+watchdog, probe registry, exposure caps
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | Obligation registration succeeds only under fresh grounded v... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | Concurrent obligation registrations cannot jointly exceed ve... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 3 | Agent fulfillment evidence remains unverified until the veri... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 4 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 3 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), AST symbol-to-test binding (3/8 symbols verified), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Restore bounded post-payment obligations using only verifier-owned authorization facts

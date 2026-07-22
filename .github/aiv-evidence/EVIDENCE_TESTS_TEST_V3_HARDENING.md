# AIV Evidence File (v1.0)

**File:** `tests/test_v3_hardening.py`
**Commit:** `a024bb0`
**Previous:** `76c1bec`
**Generated:** 2026-07-22T23:07:48Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "tests/test_v3_hardening.py"
  classification_rationale: "R3 evidence because these regressions protect payment liability, refund authority, and verifier separation-of-duties"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T23:07:48Z"
```

## Claim(s)

1. Focused tests reject ungrounded and stale obligation authorization facts
2. Focused tests prove every verifier safeguard is required before authorization enables
3. Focused tests prove concurrent registrations admit only one obligation when max_open is one
4. Focused tests prove agent fulfillment claims remain unverified and open records are checked independently
5. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/51](https://github.com/ImmortalDemonGod/money-agent/pull/51)
- **Requirements Verified:** PR 51 must permit the intended mechanically guaranteed obligation behavior without weakening its payment and refund boundaries

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`a024bb0`](https://github.com/ImmortalDemonGod/money-agent/tree/a024bb096270addf43546d32f3cb0ca6b69488ba))

- [`tests/test_v3_hardening.py#L6`](https://github.com/ImmortalDemonGod/money-agent/blob/a024bb096270addf43546d32f3cb0ca6b69488ba/tests/test_v3_hardening.py#L6)
- [`tests/test_v3_hardening.py#L27`](https://github.com/ImmortalDemonGod/money-agent/blob/a024bb096270addf43546d32f3cb0ca6b69488ba/tests/test_v3_hardening.py#L27)
- [`tests/test_v3_hardening.py#L182-L293`](https://github.com/ImmortalDemonGod/money-agent/blob/a024bb096270addf43546d32f3cb0ca6b69488ba/tests/test_v3_hardening.py#L182-L293)
- [`tests/test_v3_hardening.py#L295-L302`](https://github.com/ImmortalDemonGod/money-agent/blob/a024bb096270addf43546d32f3cb0ca6b69488ba/tests/test_v3_hardening.py#L295-L302)

### Class A (Execution Evidence)

**Per-symbol test coverage (AST analysis):**

- **`obligation_auth`** (L6): PASS -- 4 test(s) call `obligation_auth` directly
  - `tests/test_v3_hardening.py::test_obligation_authorization_requires_fresh_grounded_verifier_fact`
  - `tests/test_v3_hardening.py::test_obligation_watch_checks_open_records_without_agent_claim`
  - `tests/test_v3_hardening.py::test_obligation_registration_uses_verifier_caps_and_serializes`
  - `tests/test_v3_hardening.py::test_obligation_deadline_cap_and_fulfillment_claim_are_not_self_certifying`
- **`test_obligation_authorization_requires_fresh_grounded_verifier_fact`** (L27): FAIL -- WARNING: No tests import or call `test_obligation_authorization_requires_fresh_grounded_verifier_fact`
- **`test_obligation_watch_authorization_requires_every_safeguard`** (L182-L293): FAIL -- WARNING: No tests import or call `test_obligation_watch_authorization_requires_every_safeguard`
- **`test_obligation_watch_checks_open_records_without_agent_claim`** (L295-L302): FAIL -- WARNING: No tests import or call `test_obligation_watch_checks_open_records_without_agent_claim`
- **`test_obligation_registration_uses_verifier_caps_and_serializes`** (unknown): FAIL -- WARNING: No tests import or call `test_obligation_registration_uses_verifier_caps_and_serializes`
- **`test_obligation_deadline_cap_and_fulfillment_claim_are_not_self_certifying`** (unknown): FAIL -- WARNING: No tests import or call `test_obligation_deadline_cap_and_fulfillment_claim_are_not_self_certifying`
- **`run`** (unknown): FAIL -- WARNING: No tests import or call `run`
- **`save`** (unknown): FAIL -- WARNING: No tests import or call `save`

**Coverage summary:** 1/8 symbols verified by tests.

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
30612e5 test(sim): exercise CodeRabbit review invariants
76c1bec test(v3): cover CodeRabbit hardening findings
bb5cbed test(sim): adversarially cover PR 51 hardening
d90785d test(v3): cover adversarial enforcement seams
1529ea1 [S11] P-generalizations: prereg, decision gate, obligations+watchdog, probe registry, exposure caps
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | Focused tests reject ungrounded and stale obligation authori... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | Focused tests prove every verifier safeguard is required bef... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 3 | Focused tests prove concurrent registrations admit only one ... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 4 | Focused tests prove agent fulfillment claims remain unverifi... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 5 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 4 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), AST symbol-to-test binding (1/8 symbols verified), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Cover the complete mechanically guaranteed obligation authorization matrix

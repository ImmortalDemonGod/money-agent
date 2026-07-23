# AIV Evidence File (v1.0)

**File:** `bin/obligations.py`
**Commit:** `dfde8e4`
**Previous:** `e0f224c`
**Generated:** 2026-07-23T01:38:06Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "bin/obligations.py"
  classification_rationale: "CodeRabbit: push failure was ignored (verifier never sees the liability) and a ch_ prefix was only syntactic (duplicated charge accepted). R3: verifier-refundable liability handling"
  classified_by: "Claude"
  classified_at: "2026-07-23T01:38:06Z"
```

## Claim(s)

1. Registration fails closed when the publish push fails, because the watchdog reads only the pushed origin copy and an unpushed liability would never be watched or refunded while registration reported success
2. A charge already bound to another obligation is refused, so a single payment can never back two liabilities or be refunded to the wrong obligation
3. No existing tests were modified or deleted
4. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/51](https://github.com/ImmortalDemonGod/money-agent/pull/51)
- **Requirements Verified:** Registration must not claim success when the verifier cannot see the liability, and one charge must back at most one refundable obligation (CodeRabbit Majors)

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`dfde8e4`](https://github.com/ImmortalDemonGod/money-agent/tree/dfde8e47d3a034e2a56c8dd1c08c986f3cbf041b))

- [`bin/obligations.py#L53-L62`](https://github.com/ImmortalDemonGod/money-agent/blob/dfde8e47d3a034e2a56c8dd1c08c986f3cbf041b/bin/obligations.py#L53-L62)
- [`bin/obligations.py#L169-L174`](https://github.com/ImmortalDemonGod/money-agent/blob/dfde8e47d3a034e2a56c8dd1c08c986f3cbf041b/bin/obligations.py#L169-L174)
- [`bin/obligations.py#L242-L248`](https://github.com/ImmortalDemonGod/money-agent/blob/dfde8e47d3a034e2a56c8dd1c08c986f3cbf041b/bin/obligations.py#L242-L248)

### Class A (Execution Evidence)

**Per-symbol test coverage (AST analysis):**

- **`_save_unlocked`** (L53-L62): FAIL -- WARNING: No tests import or call `_save_unlocked`
- **`cmd_register`** (L169-L174): PASS -- 2 test(s) call `cmd_register` directly
  - `tests/test_v3_hardening.py::test_obligation_registration_uses_verifier_caps_and_serializes`
  - `tests/test_v3_hardening.py::test_obligation_deadline_cap_and_fulfillment_claim_are_not_self_certifying`
- **`main`** (L242-L248): PASS -- 2 test(s) call `main` directly
  - `tests/test_v3_hardening.py::test_obligation_watch_checks_open_records_without_agent_claim`
  - `tests/test_v3_hardening.py::test_obligation_watch_breaches_late_delivery_and_unknown_status_with_refund`

**Coverage summary:** 2/3 symbols verified by tests.

### Code Quality (Linting & Types)

- **ruff:** 0 error(s)
- **mypy:** 

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
dfde8e4 test(watchdog): late-reachable delivery and unknown status breach and refund
b28993c test(gate): note the P3 publish-decision requirement (e2e fixture deferred)
9c7574d Merge main into run2-e-v3-gated (rebase after #50 merged)
5b05cc4 test(human): skip signing tests when ssh-keygen is absent (sim portability)
24ca694 Merge main into run2-d-rails-human (rebase after #49 merged): pick up #49's gate/edge work
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | Registration fails closed when the publish push fails, becau... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | A charge already bound to another obligation is refused, so ... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 3 | No existing tests were modified or deleted | structural | Class C: all structural indicators clean | PASS VERIFIED |
| 4 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 2 verified, 0 unverified, 2 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), AST symbol-to-test binding (2/3 symbols verified), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Raise on failed publish push; reject a reused --charge-id in cmd_register

# AIV Evidence File (v1.0)

**File:** `tests/test_v3_hardening.py`
**Commit:** `5df105e`
**Previous:** `a3d4a5a`
**Generated:** 2026-07-22T22:40:30Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "tests/test_v3_hardening.py"
  classification_rationale: "Tests inherit R3 from the payment, PII, refund, and audit controls they verify"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T22:40:30Z"
```

## Claim(s)

1. Focused tests reproduce and prevent double reservation consumption
2. Focused tests bind mail consume, rollback, lane, bet, and audit ordering
3. Focused tests reject substring decisions, self-graded typed outcomes, and deferred paid work
4. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/51#pullrequestreview-4759249208](https://github.com/ImmortalDemonGod/money-agent/pull/51#pullrequestreview-4759249208)
- **Requirements Verified:** CodeRabbit requires claim-specific execution evidence for the corrected critical boundaries

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`5df105e`](https://github.com/ImmortalDemonGod/money-agent/tree/5df105e687bf5d0ce912e2e5399bd2b72db0ed32))

- [`tests/test_v3_hardening.py#L7-L9`](https://github.com/ImmortalDemonGod/money-agent/blob/5df105e687bf5d0ce912e2e5399bd2b72db0ed32/tests/test_v3_hardening.py#L7-L9)
- [`tests/test_v3_hardening.py#L21`](https://github.com/ImmortalDemonGod/money-agent/blob/5df105e687bf5d0ce912e2e5399bd2b72db0ed32/tests/test_v3_hardening.py#L21)
- [`tests/test_v3_hardening.py#L63-L68`](https://github.com/ImmortalDemonGod/money-agent/blob/5df105e687bf5d0ce912e2e5399bd2b72db0ed32/tests/test_v3_hardening.py#L63-L68)
- [`tests/test_v3_hardening.py#L77`](https://github.com/ImmortalDemonGod/money-agent/blob/5df105e687bf5d0ce912e2e5399bd2b72db0ed32/tests/test_v3_hardening.py#L77)
- [`tests/test_v3_hardening.py#L91-L110`](https://github.com/ImmortalDemonGod/money-agent/blob/5df105e687bf5d0ce912e2e5399bd2b72db0ed32/tests/test_v3_hardening.py#L91-L110)
- [`tests/test_v3_hardening.py#L126-L182`](https://github.com/ImmortalDemonGod/money-agent/blob/5df105e687bf5d0ce912e2e5399bd2b72db0ed32/tests/test_v3_hardening.py#L126-L182)
- [`tests/test_v3_hardening.py#L186`](https://github.com/ImmortalDemonGod/money-agent/blob/5df105e687bf5d0ce912e2e5399bd2b72db0ed32/tests/test_v3_hardening.py#L186)
- [`tests/test_v3_hardening.py#L188`](https://github.com/ImmortalDemonGod/money-agent/blob/5df105e687bf5d0ce912e2e5399bd2b72db0ed32/tests/test_v3_hardening.py#L188)
- [`tests/test_v3_hardening.py#L238-L266`](https://github.com/ImmortalDemonGod/money-agent/blob/5df105e687bf5d0ce912e2e5399bd2b72db0ed32/tests/test_v3_hardening.py#L238-L266)

### Class A (Execution Evidence)

**Per-symbol test coverage (AST analysis):**

- **`test_bet_gate_enforces_cumulative_spend`** (L7-L9): FAIL -- WARNING: No tests import or call `test_bet_gate_enforces_cumulative_spend`
- **`transaction`** (L21): FAIL -- WARNING: No tests import or call `transaction`
- **`test_bets_save_path_limits_commit`** (L63-L68): FAIL -- WARNING: No tests import or call `test_bets_save_path_limits_commit`
- **`test_bet_gate_serializes_reservation_consumption`** (L77): FAIL -- WARNING: No tests import or call `test_bet_gate_serializes_reservation_consumption`
- **`save`** (L91-L110): FAIL -- WARNING: No tests import or call `save`
- **`test_mail_audit_failure_rolls_back_consumed_reservation`** (L126-L182): FAIL -- WARNING: No tests import or call `test_mail_audit_failure_rolls_back_consumed_reservation`
- **`test_mail_attempt_is_bound_consumed_and_honestly_logged`** (L186): FAIL -- WARNING: No tests import or call `test_mail_attempt_is_bound_consumed_and_honestly_logged`
- **`test_deferred_obligations_are_refused_and_recorded`** (L188): FAIL -- WARNING: No tests import or call `test_deferred_obligations_are_refused_and_recorded`
- **`run`** (L238-L266): FAIL -- WARNING: No tests import or call `run`
- **`SMTP`** (unknown): FAIL -- WARNING: No tests import or call `SMTP`
- **`SMTP.__init__`** (unknown): FAIL -- WARNING: No tests import or call `__init__`
- **`SMTP.__enter__`** (unknown): FAIL -- WARNING: No tests import or call `__enter__`
- **`SMTP.__exit__`** (unknown): FAIL -- WARNING: No tests import or call `__exit__`
- **`SMTP.starttls`** (unknown): FAIL -- WARNING: No tests import or call `starttls`
- **`SMTP.login`** (unknown): FAIL -- WARNING: No tests import or call `login`
- **`SMTP.send_message`** (unknown): FAIL -- WARNING: No tests import or call `send_message`
- **`test_decision_gate_requires_exact_parsed_fields`** (unknown): FAIL -- WARNING: No tests import or call `test_decision_gate_requires_exact_parsed_fields`
- **`test_typed_resolution_evaluates_declared_metric`** (unknown): FAIL -- WARNING: No tests import or call `test_typed_resolution_evaluates_declared_metric`

**Coverage summary:** 0/18 symbols verified by tests.

### Code Quality (Linting & Types)

- **ruff:** All checks passed
- **mypy:** Found 9 errors in 1 file (checked 1 source file)

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
1c0d6f2 test(sim): adversarially cover PR 51 hardening
a3d4a5a test(v3): cover adversarial enforcement seams
937c8d6 [S11] P-generalizations: prereg, decision gate, obligations+watchdog, probe registry, exposure caps
7b7a7fe [S10] V3 spine: per-lane stage ordering, config-gated off (the contested layer, by explicit switch)
644f13c [S9] V3 typed bet-spec + action authorization, config-gated off (bet-ledger layer)
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | Focused tests reproduce and prevent double reservation consu... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | Focused tests bind mail consume, rollback, lane, bet, and au... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 3 | Focused tests reject substring decisions, self-graded typed ... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 4 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 3 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), AST symbol-to-test binding (0/18 symbols verified), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Add thirteen focused regressions for the completed CodeRabbit review

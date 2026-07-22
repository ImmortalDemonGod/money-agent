# AIV Evidence File (v1.0)

**File:** `tests/test_v3_hardening.py`
**Commit:** `7fd00f3`
**Generated:** 2026-07-22T22:07:03Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "tests/test_v3_hardening.py"
  classification_rationale: "Tests critical payment, PII, refund, and audit boundaries and therefore inherit R3"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T22:07:03Z"
```

## Claim(s)

1. Focused regressions exercise bet binding, spend limits, audit commit isolation, mail reservation ordering, obligation verification, lane caps, and committed provenance
2. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/51](https://github.com/ImmortalDemonGod/money-agent/pull/51)
- **Requirements Verified:** PR 51 enforcement claims require machine-bindable adversarial coverage in addition to the shell integration matrix

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`7fd00f3`](https://github.com/ImmortalDemonGod/money-agent/tree/7fd00f30cdb9152f02fe53742d8cf34639677f74))

- [`tests/test_v3_hardening.py#L1-L155`](https://github.com/ImmortalDemonGod/money-agent/blob/7fd00f30cdb9152f02fe53742d8cf34639677f74/tests/test_v3_hardening.py#L1-L155)

### Class A (Execution Evidence)

**Per-symbol test coverage (AST analysis):**

- **`typed_bet`** (L1-L155): PASS -- 2 test(s) call `typed_bet` directly
  - `tests/test_v3_hardening.py::test_bet_gate_rejects_nan_and_binds_lane`
  - `tests/test_v3_hardening.py::test_bet_gate_enforces_cumulative_spend`
- **`test_bet_gate_rejects_nan_and_binds_lane`** (unknown): FAIL -- WARNING: No tests import or call `test_bet_gate_rejects_nan_and_binds_lane`
- **`test_bet_gate_enforces_cumulative_spend`** (unknown): FAIL -- WARNING: No tests import or call `test_bet_gate_enforces_cumulative_spend`
- **`test_bets_save_path_limits_commit`** (unknown): FAIL -- WARNING: No tests import or call `test_bets_save_path_limits_commit`
- **`test_mail_refusal_does_not_consume_reservation`** (unknown): FAIL -- WARNING: No tests import or call `test_mail_refusal_does_not_consume_reservation`
- **`test_obligation_values_and_fulfillment_are_fail_closed`** (unknown): FAIL -- WARNING: No tests import or call `test_obligation_values_and_fulfillment_are_fail_closed`
- **`test_obligation_watch_rejects_shell_and_idempotently_refunds`** (unknown): FAIL -- WARNING: No tests import or call `test_obligation_watch_rejects_shell_and_idempotently_refunds`
- **`test_closed_lane_cannot_reopen_past_active_cap`** (unknown): FAIL -- WARNING: No tests import or call `test_closed_lane_cannot_reopen_past_active_cap`
- **`test_provenance_must_name_a_committed_blob`** (unknown): FAIL -- WARNING: No tests import or call `test_provenance_must_name_a_committed_blob`
- **`fake_run`** (unknown): FAIL -- WARNING: No tests import or call `fake_run`
- **`authorize`** (unknown): PASS -- 2 test(s) call `authorize` directly
  - `tests/test_v3_hardening.py::test_bet_gate_rejects_nan_and_binds_lane`
  - `tests/test_v3_hardening.py::test_bet_gate_enforces_cumulative_spend`
- **`Response`** (unknown): PASS -- 1 test(s) call `Response` directly
  - `tests/test_v3_hardening.py::test_obligation_watch_rejects_shell_and_idempotently_refunds`
- **`bet`** (unknown): PASS -- 1 test(s) call `bet` directly
  - `tests/test_v3_hardening.py::test_closed_lane_cannot_reopen_past_active_cap`
- **`Response.__enter__`** (unknown): FAIL -- WARNING: No tests import or call `__enter__`
- **`Response.__exit__`** (unknown): FAIL -- WARNING: No tests import or call `__exit__`
- **`Response.read`** (unknown): FAIL -- WARNING: No tests import or call `read`

**Coverage summary:** 4/16 symbols verified by tests.

### Code Quality (Linting & Types)

- **ruff:** All checks passed
- **mypy:** Found 7 errors in 1 file (checked 1 source file)

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
937c8d6 [S11] P-generalizations: prereg, decision gate, obligations+watchdog, probe registry, exposure caps
7b7a7fe [S10] V3 spine: per-lane stage ordering, config-gated off (the contested layer, by explicit switch)
644f13c [S9] V3 typed bet-spec + action authorization, config-gated off (bet-ledger layer)
e07aefd [S8] human-actuation queue: request-don't-wait, metered, conclusion-blocking (#31) + the atomic PROMPT amendment
3143f26 [S7] rail adapters: the P1 contract + a stubbed Base/USDC rail with settlement-event binding (#30 Part 1)
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | Focused regressions exercise bet binding, spend limits, audi... | symbol | 1 test(s) call `bet` | PASS VERIFIED |
| 2 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 2 verified, 0 unverified, 0 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), AST symbol-to-test binding (4/16 symbols verified), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Add eight focused regressions for every confirmed PR 51 enforcement defect

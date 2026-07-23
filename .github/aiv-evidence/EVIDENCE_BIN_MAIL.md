# AIV Evidence File (v1.0)

**File:** `bin/mail.py`
**Commit:** `91117d1`
**Previous:** `bcd3ccf`
**Generated:** 2026-07-22T22:39:41Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "bin/mail.py"
  classification_rationale: "Outbound PII-bearing email and its durable audit trail are AIV section 5.2 critical surfaces"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T22:39:41Z"
```

## Claim(s)

1. Audit persistence failures roll back a just-consumed bound send reservation
2. SENT_LOG records an unconfirmed SMTP attempt rather than claiming delivery
3. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/51#discussion_r3634224782](https://github.com/ImmortalDemonGod/money-agent/pull/51#discussion_r3634224782)
- **Requirements Verified:** CodeRabbit requires reservation consumption before audit persistence with compensation before SMTP

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`91117d1`](https://github.com/ImmortalDemonGod/money-agent/tree/91117d1bea44930d5175a20f190fa0c3df87712b))

- [`bin/mail.py#L36`](https://github.com/ImmortalDemonGod/money-agent/blob/91117d1bea44930d5175a20f190fa0c3df87712b/bin/mail.py#L36)
- [`bin/mail.py#L196-L216`](https://github.com/ImmortalDemonGod/money-agent/blob/91117d1bea44930d5175a20f190fa0c3df87712b/bin/mail.py#L196-L216)
- [`bin/mail.py#L225-L231`](https://github.com/ImmortalDemonGod/money-agent/blob/91117d1bea44930d5175a20f190fa0c3df87712b/bin/mail.py#L225-L231)
- [`bin/mail.py#L242`](https://github.com/ImmortalDemonGod/money-agent/blob/91117d1bea44930d5175a20f190fa0c3df87712b/bin/mail.py#L242)
- [`bin/mail.py#L258-L259`](https://github.com/ImmortalDemonGod/money-agent/blob/91117d1bea44930d5175a20f190fa0c3df87712b/bin/mail.py#L258-L259)

### Class A (Execution Evidence)

**Per-symbol test coverage (AST analysis):**

- **`send`** (L36): PASS -- 3 test(s) call `send` directly
  - `tests/test_v3_hardening.py::test_mail_refusal_does_not_consume_reservation`
  - `tests/test_v3_hardening.py::test_mail_audit_failure_rolls_back_consumed_reservation`
  - `tests/test_v3_hardening.py::test_mail_attempt_is_bound_consumed_and_honestly_logged`
- **`_rollback_reservation`** (L196-L216): FAIL -- WARNING: No tests import or call `_rollback_reservation`

**Coverage summary:** 1/2 symbols verified by tests.

### Code Quality (Linting & Types)

- **ruff:** All checks passed
- **mypy:** Found 11 errors in 4 files (checked 1 source file)

### Class C (Negative Evidence)

**Search methodology:** Ran `git diff --cached` and scanned for regression indicators.

- Test file deletions: **none**
- Test file modifications: **none**
- Deleted assertions (`assert` removals in diff): **none found**
- Added skip markers (`@pytest.mark.skip`, `@unittest.skip`): **none found**

### Class F (Provenance Evidence)

**Test file chain-of-custody:**

| File | Commits | Created By | Last Modified By | Assertions |
|------|---------|------------|------------------|------------|
| `tests/test_v3_hardening.py` | 1 | Miguel Ingram (a3d4a5a) | Miguel Ingram (a3d4a5a) | 25 |

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
| 1 | Audit persistence failures roll back a just-consumed bound s... | symbol | 3 test(s) call `send` | PASS VERIFIED |
| 2 | SENT_LOG records an unconfirmed SMTP attempt rather than cla... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 3 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 2 verified, 0 unverified, 1 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), AST symbol-to-test binding (1/2 symbols verified), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Order send authorization, attempt logging, rollback, and SMTP honestly

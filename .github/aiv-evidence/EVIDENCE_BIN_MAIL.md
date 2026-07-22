# AIV Evidence File (v1.0)

**File:** `bin/mail.py`
**Commit:** `a3d4a5a`
**Generated:** 2026-07-22T22:07:17Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "bin/mail.py"
  classification_rationale: "Touches PII-bearing external email, real-name reputation, and audit logging under AIV section 5.2"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T22:07:17Z"
```

## Claim(s)

1. A message rejected by content, disclosure, or audit-log gates does not consume its send reservation
2. Armed sends bind authorization to the caller-supplied bet and lane before SMTP begins
3. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/51](https://github.com/ImmortalDemonGod/money-agent/pull/51)
- **Requirements Verified:** PR 51 wires typed action authorization into outbound email without starving valid bets on refused attempts

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`a3d4a5a`](https://github.com/ImmortalDemonGod/money-agent/tree/a3d4a5a1fb551de83d1f15690217c714a6d4ec83))

- [`bin/mail.py#L17`](https://github.com/ImmortalDemonGod/money-agent/blob/a3d4a5a1fb551de83d1f15690217c714a6d4ec83/bin/mail.py#L17)
- [`bin/mail.py#L133-L134`](https://github.com/ImmortalDemonGod/money-agent/blob/a3d4a5a1fb551de83d1f15690217c714a6d4ec83/bin/mail.py#L133-L134)
- [`bin/mail.py#L157`](https://github.com/ImmortalDemonGod/money-agent/blob/a3d4a5a1fb551de83d1f15690217c714a6d4ec83/bin/mail.py#L157)
- [`bin/mail.py#L161-L172`](https://github.com/ImmortalDemonGod/money-agent/blob/a3d4a5a1fb551de83d1f15690217c714a6d4ec83/bin/mail.py#L161-L172)
- [`bin/mail.py#L234-L240`](https://github.com/ImmortalDemonGod/money-agent/blob/a3d4a5a1fb551de83d1f15690217c714a6d4ec83/bin/mail.py#L234-L240)
- [`bin/mail.py#L255-L256`](https://github.com/ImmortalDemonGod/money-agent/blob/a3d4a5a1fb551de83d1f15690217c714a6d4ec83/bin/mail.py#L255-L256)
- [`bin/mail.py#L266-L268`](https://github.com/ImmortalDemonGod/money-agent/blob/a3d4a5a1fb551de83d1f15690217c714a6d4ec83/bin/mail.py#L266-L268)
- [`bin/mail.py#L270-L271`](https://github.com/ImmortalDemonGod/money-agent/blob/a3d4a5a1fb551de83d1f15690217c714a6d4ec83/bin/mail.py#L270-L271)

### Class A (Execution Evidence)

**Per-symbol test coverage (AST analysis):**

- **`read`** (L17): FAIL -- WARNING: No tests import or call `read`
- **`send`** (L133-L134): PASS -- 1 test(s) call `send` directly
  - `tests/test_v3_hardening.py::test_mail_refusal_does_not_consume_reservation`
- **`_bet_gate`** (L157): FAIL -- WARNING: No tests import or call `_bet_gate`
- **`option`** (L161-L172): FAIL -- WARNING: No tests import or call `option`

**Coverage summary:** 1/4 symbols verified by tests.

### Code Quality (Linting & Types)

- **ruff:** All checks passed
- **mypy:** Found 10 errors in 4 files (checked 1 source file)

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
| `tests/test_v3_hardening.py` | 1 | Miguel Ingram (a3d4a5a) | Miguel Ingram (a3d4a5a) | 16 |

**Recent test directory history** (`git log --oneline -5 -- tests/`):

```
a3d4a5a test(v3): cover adversarial enforcement seams
937c8d6 [S11] P-generalizations: prereg, decision gate, obligations+watchdog, probe registry, exposure caps
7b7a7fe [S10] V3 spine: per-lane stage ordering, config-gated off (the contested layer, by explicit switch)
644f13c [S9] V3 typed bet-spec + action authorization, config-gated off (bet-ledger layer)
e07aefd [S8] human-actuation queue: request-don't-wait, metered, conclusion-blocking (#31) + the atomic PROMPT amendment
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | A message rejected by content, disclosure, or audit-log gate... | symbol | 1 test(s) call `send` | PASS VERIFIED |
| 2 | Armed sends bind authorization to the caller-supplied bet an... | symbol | 1 test(s) call `send` | PASS VERIFIED |
| 3 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 3 verified, 0 unverified, 0 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), AST symbol-to-test binding (1/4 symbols verified), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Bind email sends to explicit bets and delay consumption until the wire boundary

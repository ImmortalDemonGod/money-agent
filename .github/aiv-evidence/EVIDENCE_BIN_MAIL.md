# AIV Evidence File (v1.0)

**File:** `bin/mail.py`
**Commit:** `0948add`
**Previous:** `c351f15`
**Generated:** 2026-07-23T02:31:03Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R2
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "bin/mail.py"
  classification_rationale: "Shadow previously appended and committed the shared SENT_LOG.md"
  classified_by: "Claude"
  classified_at: "2026-07-23T02:31:03Z"
```

## Claim(s)

1. A SHADOW=1 send writes and commits its audit trail only under run/shadow/, leaving the live SENT_LOG.md untouched
2. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/52](https://github.com/ImmortalDemonGod/money-agent/pull/52)
- **Requirements Verified:** CodeRabbit review of PR #52 requires a shadow rehearsal not mutate the shared live claims lane

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`0948add`](https://github.com/ImmortalDemonGod/money-agent/tree/0948add28dbf5046d93fd2da1a86a781992ab380))

- [`bin/mail.py#L54-L57`](https://github.com/ImmortalDemonGod/money-agent/blob/0948add28dbf5046d93fd2da1a86a781992ab380/bin/mail.py#L54-L57)
- [`bin/mail.py#L274-L276`](https://github.com/ImmortalDemonGod/money-agent/blob/0948add28dbf5046d93fd2da1a86a781992ab380/bin/mail.py#L274-L276)
- [`bin/mail.py#L280-L283`](https://github.com/ImmortalDemonGod/money-agent/blob/0948add28dbf5046d93fd2da1a86a781992ab380/bin/mail.py#L280-L283)
- [`bin/mail.py#L289-L292`](https://github.com/ImmortalDemonGod/money-agent/blob/0948add28dbf5046d93fd2da1a86a781992ab380/bin/mail.py#L289-L292)

### Class A (Execution Evidence)

**Per-symbol test coverage (AST analysis):**

- **`send`** (L54-L57): PASS -- 3 test(s) call `send` directly
  - `tests/test_v3_hardening.py::test_mail_refusal_does_not_consume_reservation`
  - `tests/test_v3_hardening.py::test_mail_audit_failure_rolls_back_consumed_reservation`
  - `tests/test_v3_hardening.py::test_mail_attempt_is_bound_consumed_and_honestly_logged`

**Coverage summary:** 1/1 symbols verified by tests.

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

| File | Commits | Created By | Last Modified By | Assertions |
|------|---------|------------|------------------|------------|
| `tests/test_v3_hardening.py` | 6 | Miguel Ingram (42e2a25) | Claude (6da1998) | 42 |

**Recent test directory history** (`git log --oneline -5 -- tests/`):

```
ef4f310 [S12] Tier-1 shadow-run mode: SHADOW=1 walls, capture, scripted world, policy scorecard
6da1998 test(watchdog): assert breached records are not counted as open
dfde8e4 test(watchdog): late-reachable delivery and unknown status breach and refund
b28993c test(gate): note the P3 publish-decision requirement (e2e fixture deferred)
9c7574d Merge main into run2-e-v3-gated (rebase after #50 merged)
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | A SHADOW=1 send writes and commits its audit trail only unde... | symbol | 3 test(s) call `send` | PASS VERIFIED |
| 2 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 2 verified, 0 unverified, 0 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), AST symbol-to-test binding (1/1 symbols verified), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Route the audit write to run/shadow/SENT_LOG.md and stage only shadow paths in shadow mode

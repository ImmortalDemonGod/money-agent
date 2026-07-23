# AIV Evidence File (v1.0)

**File:** `bin/obligation_watch.py`
**Commit:** `b28993c`
**Previous:** `6656cfa`
**Generated:** 2026-07-23T01:29:54Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "bin/obligation_watch.py"
  classification_rationale: "CodeRabbit Critical: pre-fix, an unknown status halted without refunding and a late-but-reachable delivery read as fulfilled. R3: verifier-owned watchdog handling customer money"
  classified_by: "Claude"
  classified_at: "2026-07-23T01:29:54Z"
```

## Claim(s)

1. The obligation watchdog evaluates the deadline before accepting any completion, so a delivery reachable only after the promised deadline is a breach not a fulfilment; and every breach path (unparseable deadline, unrecognized status, late delivery, overdue-unfulfilled) attempts the bound refund instead of halting while leaving the customer un-refunded
2. No existing tests were modified or deleted
3. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/51](https://github.com/ImmortalDemonGod/money-agent/pull/51)
- **Requirements Verified:** The refund guarantee must hold on EVERY breach: agent-controlled status and late delivery must not bypass the refund (CodeRabbit Critical)

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`b28993c`](https://github.com/ImmortalDemonGod/money-agent/tree/b28993c20e718b6f76c3980d956a06ddced54006))

- [`bin/obligation_watch.py#L156-L169`](https://github.com/ImmortalDemonGod/money-agent/blob/b28993c20e718b6f76c3980d956a06ddced54006/bin/obligation_watch.py#L156-L169)
- [`bin/obligation_watch.py#L171-L178`](https://github.com/ImmortalDemonGod/money-agent/blob/b28993c20e718b6f76c3980d956a06ddced54006/bin/obligation_watch.py#L171-L178)
- [`bin/obligation_watch.py#L181`](https://github.com/ImmortalDemonGod/money-agent/blob/b28993c20e718b6f76c3980d956a06ddced54006/bin/obligation_watch.py#L181)
- [`bin/obligation_watch.py#L183-L185`](https://github.com/ImmortalDemonGod/money-agent/blob/b28993c20e718b6f76c3980d956a06ddced54006/bin/obligation_watch.py#L183-L185)
- [`bin/obligation_watch.py#L187-L188`](https://github.com/ImmortalDemonGod/money-agent/blob/b28993c20e718b6f76c3980d956a06ddced54006/bin/obligation_watch.py#L187-L188)
- [`bin/obligation_watch.py#L191-L196`](https://github.com/ImmortalDemonGod/money-agent/blob/b28993c20e718b6f76c3980d956a06ddced54006/bin/obligation_watch.py#L191-L196)
- [`bin/obligation_watch.py#L199-L200`](https://github.com/ImmortalDemonGod/money-agent/blob/b28993c20e718b6f76c3980d956a06ddced54006/bin/obligation_watch.py#L199-L200)

### Class A (Execution Evidence)

**Per-symbol test coverage (AST analysis):**

- **`main`** (L156-L169): PASS -- 2 test(s) call `main` directly
  - `tests/test_v3_hardening.py::test_obligation_watch_checks_open_records_without_agent_claim`
  - `tests/test_v3_hardening.py::test_obligation_watch_breaches_late_delivery_and_unknown_status_with_refund`
- **`_breach`** (L171-L178): FAIL -- WARNING: No tests import or call `_breach`

**Coverage summary:** 1/2 symbols verified by tests.

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
| `tests/test_v3_hardening.py` | 4 | Miguel Ingram (42e2a25) | Miguel Ingram (426fe8e) | 41 |

**Recent test directory history** (`git log --oneline -5 -- tests/`):

```
b28993c test(gate): note the P3 publish-decision requirement (e2e fixture deferred)
9c7574d Merge main into run2-e-v3-gated (rebase after #50 merged)
5b05cc4 test(human): skip signing tests when ssh-keygen is absent (sim portability)
24ca694 Merge main into run2-d-rails-human (rebase after #49 merged): pick up #49's gate/edge work
d9d3dfe test(delivery): cover fail-closed arg parsing (unrecognized/value-less flags)
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | The obligation watchdog evaluates the deadline before accept... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted | structural | Class C: all structural indicators clean | PASS VERIFIED |
| 3 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 2 verified, 0 unverified, 1 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), AST symbol-to-test binding (1/2 symbols verified), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Order deadline-first; refund on unknown-status, unparseable-deadline, late-delivery, and overdue breaches

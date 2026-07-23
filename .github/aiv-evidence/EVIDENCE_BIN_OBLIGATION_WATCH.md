# AIV Evidence File (v1.0)

**File:** `bin/obligation_watch.py`
**Commit:** `9953693`
**Previous:** `a0f1fdc`
**Generated:** 2026-07-23T01:48:10Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "bin/obligation_watch.py"
  classification_rationale: "Follow-on to the deadline-first refactor. R3: verifier watchdog metric"
  classified_by: "Claude"
  classified_at: "2026-07-23T01:48:10Z"
```

## Claim(s)

1. The published open metric excludes ids that were routed to breached, so a breached record carrying its original open status is no longer double-counted in both breached and open
2. No existing tests were modified or deleted
3. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/51](https://github.com/ImmortalDemonGod/money-agent/pull/51)
- **Requirements Verified:** A breached obligation must not also appear in the open tally (CodeRabbit Major, follow-on to the deadline-first fix)

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`9953693`](https://github.com/ImmortalDemonGod/money-agent/tree/99536931c86534a54e3b6fc2597007609cad1861))

- [`bin/obligation_watch.py#L202`](https://github.com/ImmortalDemonGod/money-agent/blob/99536931c86534a54e3b6fc2597007609cad1861/bin/obligation_watch.py#L202)
- [`bin/obligation_watch.py#L204-L205`](https://github.com/ImmortalDemonGod/money-agent/blob/99536931c86534a54e3b6fc2597007609cad1861/bin/obligation_watch.py#L204-L205)
- [`bin/obligation_watch.py#L208-L209`](https://github.com/ImmortalDemonGod/money-agent/blob/99536931c86534a54e3b6fc2597007609cad1861/bin/obligation_watch.py#L208-L209)

### Class A (Execution Evidence)

**Per-symbol test coverage (AST analysis):**

- **`main`** (L202): PASS -- 2 test(s) call `main` directly
  - `tests/test_v3_hardening.py::test_obligation_watch_checks_open_records_without_agent_claim`
  - `tests/test_v3_hardening.py::test_obligation_watch_breaches_late_delivery_and_unknown_status_with_refund`

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
| `tests/test_v3_hardening.py` | 5 | Miguel Ingram (42e2a25) | Claude (dfde8e4) | 42 |

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
| 1 | The published open metric excludes ids that were routed to b... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted | structural | Class C: all structural indicators clean | PASS VERIFIED |
| 3 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 2 verified, 0 unverified, 1 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), AST symbol-to-test binding (1/1 symbols verified), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Subtract breached ids from the open count in the published facts

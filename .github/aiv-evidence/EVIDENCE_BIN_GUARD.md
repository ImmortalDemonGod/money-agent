# AIV Evidence File (v1.0)

**File:** `bin/guard.py`
**Commit:** `a58520c`
**Previous:** `bc26d02`
**Generated:** 2026-07-23T01:48:09Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "bin/guard.py"
  classification_rationale: "CodeRabbit: the handler collapsed all load errors to absence, unlike the edge handler. R3: P5 safety gate"
  classified_by: "Claude"
  classified_at: "2026-07-23T01:48:09Z"
```

## Claim(s)

1. The iteration guard halts when the obligation facts are refused for any reason other than genuine absence (signature refusal, lane mismatch, invalid JSON), mirroring the edge-rail handler, so a forged or corrupt promise-book can no longer read as empty and hide a breach
2. No existing tests were modified or deleted
3. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/51](https://github.com/ImmortalDemonGod/money-agent/pull/51)
- **Requirements Verified:** A breach must not be hidden by an unverifiable obligations file; only genuine absence stays silent (CodeRabbit Major)

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`a58520c`](https://github.com/ImmortalDemonGod/money-agent/tree/a58520c6507453bbf206dfca524c79a82974655a))

- [`bin/guard.py#L305-L312`](https://github.com/ImmortalDemonGod/money-agent/blob/a58520c6507453bbf206dfca524c79a82974655a/bin/guard.py#L305-L312)

### Class A (Execution Evidence)

**Per-symbol test coverage (AST analysis):**

- **`main`** (L305-L312): PASS -- 2 test(s) call `main` directly
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
| 1 | The iteration guard halts when the obligation facts are refu... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
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

Only 'no ledger found' is treated as absence; other load failures halt

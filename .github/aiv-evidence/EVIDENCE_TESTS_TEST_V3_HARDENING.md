# AIV Evidence File (v1.0)

**File:** `tests/test_v3_hardening.py`
**Commit:** `b20d7db`
**Previous:** `dfde8e4`
**Generated:** 2026-07-23T01:48:11Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R1
  sod_mode: S0
  critical_surfaces: []
  blast_radius: "tests/test_v3_hardening.py"
  classification_rationale: "Extends the existing bite test. R1: test-only"
  classified_by: "Claude"
  classified_at: "2026-07-23T01:48:11Z"
```

## Claim(s)

1. The watchdog bite test asserts the published open count is zero when both obligations breach, pinning that a breached record is not double-counted as open
2. No existing tests were modified or deleted
3. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/51](https://github.com/ImmortalDemonGod/money-agent/pull/51)
- **Requirements Verified:** The open double-count fix must be regression-tested

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`b20d7db`](https://github.com/ImmortalDemonGod/money-agent/tree/b20d7dbb838fb52efd8b8ebef975b1ab3b2adb1e))

- [`tests/test_v3_hardening.py#L286`](https://github.com/ImmortalDemonGod/money-agent/blob/b20d7dbb838fb52efd8b8ebef975b1ab3b2adb1e/tests/test_v3_hardening.py#L286)

### Class A (Execution Evidence)

**Per-symbol test coverage (AST analysis):**

- **`test_obligation_watch_breaches_late_delivery_and_unknown_status_with_refund`** (L286): FAIL -- WARNING: No tests import or call `test_obligation_watch_breaches_late_delivery_and_unknown_status_with_refund`

**Coverage summary:** 0/1 symbols verified by tests.

### Code Quality (Linting & Types)

- **ruff:** 0 error(s)
- **mypy:** 

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | The watchdog bite test asserts the published open count is z... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted | structural | Class C not collected | REVIEW MANUAL REVIEW |
| 3 | No existing tests were modified or deleted during this chang... | structural | Class C not collected | REVIEW MANUAL REVIEW |

**Verdict summary:** 0 verified, 0 unverified, 3 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), AST symbol-to-test binding (0/1 symbols verified).
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Add an open==0 assertion to the late/unknown breach test

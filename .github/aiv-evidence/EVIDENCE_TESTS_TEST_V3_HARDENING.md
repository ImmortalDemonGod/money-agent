# AIV Evidence File (v1.0)

**File:** `tests/test_v3_hardening.py`
**Commit:** `a0f1fdc`
**Previous:** `426fe8e`
**Generated:** 2026-07-23T01:29:55Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R1
  sod_mode: S0
  critical_surfaces: []
  blast_radius: "tests/test_v3_hardening.py"
  classification_rationale: "Bite test for the deadline-first refund fix. R1: test-only"
  classified_by: "Claude"
  classified_at: "2026-07-23T01:29:55Z"
```

## Claim(s)

1. A late-but-reachable delivery and an unrecognized status are both recorded as breaches (never fulfilments) and both bound charges are refunded; the test fails on the pre-fix watchdog
2. No existing tests were modified or deleted; one test was added
3. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/51](https://github.com/ImmortalDemonGod/money-agent/pull/51)
- **Requirements Verified:** The Critical refund-bypass fix must be regression-tested with a fixture that bites on pre-fix code

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`a0f1fdc`](https://github.com/ImmortalDemonGod/money-agent/tree/a0f1fdcbc6f499e5274a3084c51d93710e54a277))

- [`tests/test_v3_hardening.py#L248-L287`](https://github.com/ImmortalDemonGod/money-agent/blob/a0f1fdcbc6f499e5274a3084c51d93710e54a277/tests/test_v3_hardening.py#L248-L287)

### Class A (Execution Evidence)

**Per-symbol test coverage (AST analysis):**

- **`test_obligation_watch_breaches_late_delivery_and_unknown_status_with_refund`** (L248-L287): FAIL -- WARNING: No tests import or call `test_obligation_watch_breaches_late_delivery_and_unknown_status_with_refund`
- **`run`** (unknown): FAIL -- WARNING: No tests import or call `run`

**Coverage summary:** 0/2 symbols verified by tests.

### Code Quality (Linting & Types)

- **ruff:** 0 error(s)
- **mypy:** 

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | A late-but-reachable delivery and an unrecognized status are... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted; one test was add... | structural | Class C not collected | REVIEW MANUAL REVIEW |
| 3 | No existing tests were modified or deleted during this chang... | structural | Class C not collected | REVIEW MANUAL REVIEW |

**Verdict summary:** 0 verified, 0 unverified, 3 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), AST symbol-to-test binding (0/2 symbols verified).
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Add a biting watchdog test for late-delivery and unknown-status breach+refund

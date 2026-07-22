# AIV Evidence File (v1.0)

**File:** `archive/run-001/bin/reach.py`
**Commit:** `e4e2241`
**Generated:** 2026-07-22T21:30:25Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R1
  sod_mode: S0
  critical_surfaces: []
  blast_radius: "archive/run-001/bin/reach.py"
  classification_rationale: "R1 because this corrects a bounded reporting-path lookup without changing the verifier"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T21:30:25Z"
```

## Claim(s)

1. the archived reach reporter reads received_usd from the repository-root ledger while retaining its report under the frozen run archive
2. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/56](https://github.com/ImmortalDemonGod/money-agent/pull/56)
- **Requirements Verified:** PR #56 must compute its reported money status from the verifier-owned ledger rather than a nonexistent archive path

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`e4e2241`](https://github.com/ImmortalDemonGod/money-agent/tree/e4e2241a763c2b3f4013e2f381732ff2a8d7b1c0))

- [`archive/run-001/bin/reach.py#L36-L40`](https://github.com/ImmortalDemonGod/money-agent/blob/e4e2241a763c2b3f4013e2f381732ff2a8d7b1c0/archive/run-001/bin/reach.py#L36-L40)

### Class A (Execution Evidence)

**Per-symbol test coverage (AST analysis):**

- **`<module>`** (L36-L40): FAIL -- WARNING: No tests import or call `<module>`

**Coverage summary:** 0/1 symbols verified by tests.

### Code Quality (Linting & Types)

- **ruff:** All checks passed
- **mypy:** Success: no issues found in 1 source file

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | the archived reach reporter reads received_usd from the repo... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted during this chang... | structural | Class C not collected | REVIEW MANUAL REVIEW |

**Verdict summary:** 0 verified, 0 unverified, 2 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), AST symbol-to-test binding (0/1 symbols verified).
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Use the repository ledger for archived reach reporting

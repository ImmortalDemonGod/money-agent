# AIV Evidence File (v1.0)

**File:** `tests/reach_archive.py`
**Commit:** `047b09c`
**Generated:** 2026-07-22T21:30:52Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R1
  sod_mode: S0
  critical_surfaces: []
  blast_radius: "tests/reach_archive.py"
  classification_rationale: "R1 because this tests a bounded reporting helper"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T21:30:52Z"
```

## Claim(s)

1. the archive reach regression proves verified current ledger revenue is read from the repository root and unverified revenue remains unavailable
2. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/56](https://github.com/ImmortalDemonGod/money-agent/pull/56)
- **Requirements Verified:** PR #56 requires computed reach reporting to use verifier-owned ledger facts

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`047b09c`](https://github.com/ImmortalDemonGod/money-agent/tree/047b09caff4c6be4cfbd3b0e5f14088f03712795))

- [`tests/reach_archive.py#L1-L24`](https://github.com/ImmortalDemonGod/money-agent/blob/047b09caff4c6be4cfbd3b0e5f14088f03712795/tests/reach_archive.py#L1-L24)

### Class A (Execution Evidence)

**Per-symbol test coverage (AST analysis):**

- **`<module>`** (L1-L24): FAIL -- WARNING: No tests import or call `<module>`

**Coverage summary:** 0/1 symbols verified by tests.

### Code Quality (Linting & Types)

- **ruff:** All checks passed
- **mypy:** Found 4 errors in 1 file (checked 1 source file)

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | the archive reach regression proves verified current ledger ... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted during this chang... | structural | Class C not collected | REVIEW MANUAL REVIEW |

**Verdict summary:** 0 verified, 0 unverified, 2 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), AST symbol-to-test binding (0/1 symbols verified).
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Add regression coverage for archived reach ledger lookup

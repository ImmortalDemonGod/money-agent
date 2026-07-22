# AIV Evidence File (v1.0)

**File:** `tests/reach_archive.py`
**Commit:** `eb57b66`
**Previous:** `3ece9ba`
**Generated:** 2026-07-22T21:41:26Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R1
  sod_mode: S0
  critical_surfaces: []
  blast_radius: "tests/reach_archive.py"
  classification_rationale: "R1 because this tests bounded reporting behavior"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T21:41:26Z"
```

## Claim(s)

1. the archived reach regression preserves known HN evidence during Telegraph outage and labels HN outage separately
2. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/56](https://github.com/ImmortalDemonGod/money-agent/pull/56)
- **Requirements Verified:** PR #56 must distinguish unavailable telemetry from zero traffic

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`eb57b66`](https://github.com/ImmortalDemonGod/money-agent/tree/eb57b66b244e64fbca2f772bea574cee3fe4f7cf))

- [`tests/reach_archive.py#L15-L20`](https://github.com/ImmortalDemonGod/money-agent/blob/eb57b66b244e64fbca2f772bea574cee3fe4f7cf/tests/reach_archive.py#L15-L20)

### Class A (Execution Evidence)

**Per-symbol test coverage (AST analysis):**

- **`<module>`** (L15-L20): FAIL -- WARNING: No tests import or call `<module>`

**Coverage summary:** 0/1 symbols verified by tests.

### Code Quality (Linting & Types)

- **ruff:** All checks passed
- **mypy:** Found 4 errors in 1 file (checked 1 source file)

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | the archived reach regression preserves known HN evidence du... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted during this chang... | structural | Class C not collected | REVIEW MANUAL REVIEW |

**Verdict summary:** 0 verified, 0 unverified, 2 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), AST symbol-to-test binding (0/1 symbols verified).
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Cover independent reach-source availability

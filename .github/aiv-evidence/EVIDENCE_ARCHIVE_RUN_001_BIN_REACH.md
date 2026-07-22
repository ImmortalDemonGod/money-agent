# AIV Evidence File (v1.0)

**File:** `archive/run-001/bin/reach.py`
**Commit:** `26a58e9`
**Previous:** `546401c`
**Generated:** 2026-07-22T21:41:09Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R1
  sod_mode: S0
  critical_surfaces: []
  blast_radius: "archive/run-001/bin/reach.py"
  classification_rationale: "R1 because this is bounded reporting logic"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T21:41:09Z"
```

## Claim(s)

1. reach reporting preserves positive HN evidence during a Telegraph outage and labels unavailable HN telemetry separately
2. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/56](https://github.com/ImmortalDemonGod/money-agent/pull/56)
- **Requirements Verified:** PR #56 must not turn source outages into false no-traffic conclusions

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`26a58e9`](https://github.com/ImmortalDemonGod/money-agent/tree/26a58e9e5547a3890f9878d2999c4e7891c18b2f))

- [`archive/run-001/bin/reach.py#L179`](https://github.com/ImmortalDemonGod/money-agent/blob/26a58e9e5547a3890f9878d2999c4e7891c18b2f/archive/run-001/bin/reach.py#L179)
- [`archive/run-001/bin/reach.py#L188`](https://github.com/ImmortalDemonGod/money-agent/blob/26a58e9e5547a3890f9878d2999c4e7891c18b2f/archive/run-001/bin/reach.py#L188)
- [`archive/run-001/bin/reach.py#L192-L195`](https://github.com/ImmortalDemonGod/money-agent/blob/26a58e9e5547a3890f9878d2999c4e7891c18b2f/archive/run-001/bin/reach.py#L192-L195)

### Class A (Execution Evidence)

**Per-symbol test coverage (AST analysis):**

- **`bottom_line`** (L179): FAIL -- WARNING: No tests import or call `bottom_line`

**Coverage summary:** 0/1 symbols verified by tests.

### Code Quality (Linting & Types)

- **ruff:** All checks passed
- **mypy:** Success: no issues found in 1 source file

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | reach reporting preserves positive HN evidence during a Tele... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted during this chang... | structural | Class C not collected | REVIEW MANUAL REVIEW |

**Verdict summary:** 0 verified, 0 unverified, 2 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), AST symbol-to-test binding (0/1 symbols verified).
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Separate Telegraph and HN availability reporting

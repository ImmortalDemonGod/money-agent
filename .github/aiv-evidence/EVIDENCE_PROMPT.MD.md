# AIV Evidence File (v1.0)

**File:** `PROMPT.md`
**Commit:** `2b080a4`
**Previous:** `c7bb903`
**Generated:** 2026-07-22T23:06:33Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "PROMPT.md"
  classification_rationale: "The prompt is an operator-negotiated safety boundary"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T23:06:33Z"
```

## Claim(s)

1. The run prompt forbids self-certification and using human actuation to bypass platform terms or owner authorization
2. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/issues/31](https://github.com/ImmortalDemonGod/money-agent/issues/31)
- **Requirements Verified:** The autonomy amendment permits mechanical actuation only, never strategy or policy exceptions

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`2b080a4`](https://github.com/ImmortalDemonGod/money-agent/tree/2b080a4bd131af680d8f21a2f24ce3eb3a20a3a2))

- [`PROMPT.md#L55-L60`](https://github.com/ImmortalDemonGod/money-agent/blob/2b080a4bd131af680d8f21a2f24ce3eb3a20a3a2/PROMPT.md#L55-L60)

### Class A (Execution Evidence)

**WARNING:** No tests found that directly import or reference the changed file.
This file has no claim-specific execution evidence.

### Code Quality (Linting & Types)

- **ruff:** All checks passed
- **mypy:** Found 1 error in 1 file (errors prevented further checking)

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
68b46db test(sim): isolate AIV edge fixture state
bc601c3 test(rails): expose registry contract to verification
86e664c test(pr50): exercise executable rail and queue contracts
67e9adb test(pr50): pin issue-closure trust boundaries
c5fd8f6 docs(tests): normalize bug-catalog whitespace
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | The run prompt forbids self-certification and using human ac... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 1 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), pytest (no claim-specific tests found), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Clarify signed lane and authorization limits

# AIV Evidence File (v1.0)

**File:** `bin/README.md`
**Commit:** `170ec27`
**Previous:** `59f1616`
**Generated:** 2026-07-22T23:06:26Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "bin/README.md"
  classification_rationale: "Incorrect trust classification undermines separation of duties"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T23:06:26Z"
```

## Claim(s)

1. The executable trust map describes registered bidirectional rails and independently grounded human queue states
2. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/issues/31](https://github.com/ImmortalDemonGod/money-agent/issues/31)
- **Requirements Verified:** Operators and agents must understand which component owns each payment or actuation fact

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`170ec27`](https://github.com/ImmortalDemonGod/money-agent/tree/170ec272875e75623cb2adaa9f728dd52d466521))

- [`bin/README.md#L16`](https://github.com/ImmortalDemonGod/money-agent/blob/170ec272875e75623cb2adaa9f728dd52d466521/bin/README.md#L16)
- [`bin/README.md#L23`](https://github.com/ImmortalDemonGod/money-agent/blob/170ec272875e75623cb2adaa9f728dd52d466521/bin/README.md#L23)
- [`bin/README.md#L32`](https://github.com/ImmortalDemonGod/money-agent/blob/170ec272875e75623cb2adaa9f728dd52d466521/bin/README.md#L32)
- [`bin/README.md#L47`](https://github.com/ImmortalDemonGod/money-agent/blob/170ec272875e75623cb2adaa9f728dd52d466521/bin/README.md#L47)

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
| 1 | The executable trust map describes registered bidirectional ... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 1 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), pytest (no claim-specific tests found), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Update script ownership and enforcement descriptions

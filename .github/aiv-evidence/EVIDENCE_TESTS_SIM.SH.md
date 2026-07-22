# AIV Evidence File (v1.0)

**File:** `tests/sim.sh`
**Commit:** `67e9adb`
**Previous:** `67e9adb`
**Generated:** 2026-07-22T22:59:20Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "tests/sim.sh"
  classification_rationale: "These tests protect payment facts and conclusion gating on AIV section 5.2 critical surfaces"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T22:59:20Z"
```

## Claim(s)

1. The suite directly verifies bidirectional rail registration, fail-closed amounts, exact human metering, and supervisor queue precedence
2. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/issues/31](https://github.com/ImmortalDemonGod/money-agent/issues/31)
- **Requirements Verified:** Issues #30 and #31 require verifier-owned aggregation and measurable non-blocking human actuation

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`67e9adb`](https://github.com/ImmortalDemonGod/money-agent/tree/67e9adb971022cc99f652d71ae663170d8608412))

- [`tests/sim.sh#L204-L207`](https://github.com/ImmortalDemonGod/money-agent/blob/67e9adb971022cc99f652d71ae663170d8608412/tests/sim.sh#L204-L207)
- [`tests/sim.sh#L279-L280`](https://github.com/ImmortalDemonGod/money-agent/blob/67e9adb971022cc99f652d71ae663170d8608412/tests/sim.sh#L279-L280)
- [`tests/sim.sh#L349-L380`](https://github.com/ImmortalDemonGod/money-agent/blob/67e9adb971022cc99f652d71ae663170d8608412/tests/sim.sh#L349-L380)

### Class A (Execution Evidence)

**WARNING:** No tests found that directly import or reference the changed file.
This file has no claim-specific execution evidence.

### Code Quality (Linting & Types)

- **ruff:** 17305 error(s)
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
67e9adb test(pr50): pin issue-closure trust boundaries
c5fd8f6 docs(tests): normalize bug-catalog whitespace
8457d08 merge(stack): reconcile PR50 with reviewed stack 3 fixes
0dfb70b test(sim): make packet mutations portable and fail closed
b48810e test(preflight): provide extracted Base identity path
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | The suite directly verifies bidirectional rail registration,... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 1 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), pytest (no claim-specific tests found), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Add direct contract and integration assertions before implementation

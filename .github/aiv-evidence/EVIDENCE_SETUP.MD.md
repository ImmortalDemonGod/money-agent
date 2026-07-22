# AIV Evidence File (v1.0)

**File:** `SETUP.md`
**Commit:** `72b8c7c`
**Previous:** `7f3be9e`
**Generated:** 2026-07-22T23:15:09Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "SETUP.md"
  classification_rationale: "R3 because this is payment-remediation provisioning guidance"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T23:15:09Z"
```

## Claim(s)

1. Setup requires every mechanically guaranteed obligation to bind a ch_ charge identifier
2. Setup explains that refund credentials without a refund target do not constitute a guarantee
3. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/51](https://github.com/ImmortalDemonGod/money-agent/pull/51)
- **Requirements Verified:** Operators must provision obligations with actionable refund targets, not merely refund credentials

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`72b8c7c`](https://github.com/ImmortalDemonGod/money-agent/tree/72b8c7caf44f943d3175946d28056ba8fdad1006))

- [`SETUP.md#L129-L130`](https://github.com/ImmortalDemonGod/money-agent/blob/72b8c7caf44f943d3175946d28056ba8fdad1006/SETUP.md#L129-L130)

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
167bd21 test(sim): bind obligation fixture to charge
55dc2f1 test(obligations): reject unbound refund liabilities
6763b83 test(sim): exercise verifier-authorized obligations
512f388 test(obligations): cover guarded authorization contract
30612e5 test(sim): exercise CodeRabbit review invariants
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | Setup requires every mechanically guaranteed obligation to b... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | Setup explains that refund credentials without a refund targ... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 3 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 2 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), pytest (no claim-specific tests found), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Document mandatory charge binding for guaranteed obligations

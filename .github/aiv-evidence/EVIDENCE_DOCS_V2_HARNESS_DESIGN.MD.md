# AIV Evidence File (v1.0)

**File:** `docs/V2_HARNESS_DESIGN.md`
**Commit:** `bd1e7a8`
**Previous:** `d8adf3b`
**Generated:** 2026-07-22T23:15:40Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "docs/V2_HARNESS_DESIGN.md"
  classification_rationale: "R3 because this tightens the payment/refund design contract"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T23:15:40Z"
```

## Claim(s)

1. The adopted P5 conjunction requires every liability to identify its concrete refundable charge
2. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/51](https://github.com/ImmortalDemonGod/money-agent/pull/51)
- **Requirements Verified:** Mechanically guaranteed delivery requires both refund authority and an actionable refund target

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`bd1e7a8`](https://github.com/ImmortalDemonGod/money-agent/tree/bd1e7a81215eadc0a45e0005ff8bb4aa53d8cd09))

- [`docs/V2_HARNESS_DESIGN.md#L805-L807`](https://github.com/ImmortalDemonGod/money-agent/blob/bd1e7a81215eadc0a45e0005ff8bb4aa53d8cd09/docs/V2_HARNESS_DESIGN.md#L805-L807)

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
| 1 | The adopted P5 conjunction requires every liability to ident... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 1 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), pytest (no claim-specific tests found), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Add refundable charge binding to the adopted P5 design

# AIV Evidence File (v1.0)

**File:** `CLAUDE.md`
**Commit:** `167bd21`
**Previous:** `9d56125`
**Generated:** 2026-07-22T23:14:47Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "CLAUDE.md"
  classification_rationale: "R3 because this tightens the constitutional payment and refund boundary"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T23:14:47Z"
```

## Claim(s)

1. The mechanically guaranteed exception requires every liability to bind a concrete refundable charge
2. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/51](https://github.com/ImmortalDemonGod/money-agent/pull/51)
- **Requirements Verified:** A refund-backed delivery guarantee cannot exist without a concrete charge the verifier can refund

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`167bd21`](https://github.com/ImmortalDemonGod/money-agent/tree/167bd21af20e49a9cd45aff75dc70267b0a3b258))

- [`CLAUDE.md#L37-L39`](https://github.com/ImmortalDemonGod/money-agent/blob/167bd21af20e49a9cd45aff75dc70267b0a3b258/CLAUDE.md#L37-L39)

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
| 1 | The mechanically guaranteed exception requires every liabili... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 1 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), pytest (no claim-specific tests found), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Add charge binding to the mechanically guaranteed delivery prerequisites

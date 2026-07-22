# AIV Evidence File (v1.0)

**File:** `docs/V2_HARNESS_DESIGN.md`
**Commit:** `6763b83`
**Generated:** 2026-07-22T23:10:12Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "docs/V2_HARNESS_DESIGN.md"
  classification_rationale: "R3 because this adopts the governing contract for post-payment liability and refund authority"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T23:10:12Z"
```

## Claim(s)

1. The V3 design defines mechanically guaranteed delivery as verifier enablement, refund authority, positive caps, and a maximum deadline
2. The design states agent-local configuration cannot activate or widen obligation authority
3. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/51](https://github.com/ImmortalDemonGod/money-agent/pull/51)
- **Requirements Verified:** The operator explicitly adopted the P5 amendment that PR 51 was built to implement

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`6763b83`](https://github.com/ImmortalDemonGod/money-agent/tree/6763b83d45c1b434cc3a44ed3a94cadd7ac85997))

- [`docs/V2_HARNESS_DESIGN.md#L797-L798`](https://github.com/ImmortalDemonGod/money-agent/blob/6763b83d45c1b434cc3a44ed3a94cadd7ac85997/docs/V2_HARNESS_DESIGN.md#L797-L798)
- [`docs/V2_HARNESS_DESIGN.md#L803-L808`](https://github.com/ImmortalDemonGod/money-agent/blob/6763b83d45c1b434cc3a44ed3a94cadd7ac85997/docs/V2_HARNESS_DESIGN.md#L803-L808)

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
6763b83 test(sim): exercise verifier-authorized obligations
512f388 test(obligations): cover guarded authorization contract
30612e5 test(sim): exercise CodeRabbit review invariants
76c1bec test(v3): cover CodeRabbit hardening findings
bb5cbed test(sim): adversarially cover PR 51 hardening
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | The V3 design defines mechanically guaranteed delivery as ve... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | The design states agent-local configuration cannot activate ... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 3 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 2 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), pytest (no claim-specific tests found), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Adopt and precisely define the guarded deferred-delivery exception

# AIV Evidence File (v1.0)

**File:** `SETUP.md`
**Commit:** `9d56125`
**Previous:** `4f7a8e4`
**Generated:** 2026-07-22T23:11:29Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "SETUP.md"
  classification_rationale: "R3 because these instructions control refund-key custody and payment liability limits"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T23:11:29Z"
```

## Claim(s)

1. Setup keeps all obligation enablement and refund inputs on the verifier side
2. Setup states malformed, missing, stale, or unverified safeguards disable authorization
3. Setup names failed refunds as breaches requiring halt and manual remediation
4. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/51](https://github.com/ImmortalDemonGod/money-agent/pull/51)
- **Requirements Verified:** Operators must be able to provision and audit the complete mechanically guaranteed delivery boundary

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`9d56125`](https://github.com/ImmortalDemonGod/money-agent/tree/9d561253959e574f40ed75d8ec0b3fc86a455781))

- [`SETUP.md#L112-L130`](https://github.com/ImmortalDemonGod/money-agent/blob/9d561253959e574f40ed75d8ec0b3fc86a455781/SETUP.md#L112-L130)

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
| 1 | Setup keeps all obligation enablement and refund inputs on t... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | Setup states malformed, missing, stale, or unverified safegu... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 3 | Setup names failed refunds as breaches requiring halt and ma... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 4 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 3 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), pytest (no claim-specific tests found), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Document safe verifier provisioning for the adopted delivery exception

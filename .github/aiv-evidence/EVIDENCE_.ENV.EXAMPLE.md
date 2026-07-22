# AIV Evidence File (v1.0)

**File:** `.env.example`
**Commit:** `d8adf3b`
**Previous:** `8f307cf`
**Generated:** 2026-07-22T23:10:38Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: ".env.example"
  classification_rationale: "R3 because this documents custody and configuration of a refund credential on the payment boundary"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T23:10:38Z"
```

## Claim(s)

1. The environment template keeps obligation authorization default-off and places every enabling value in the verifier-only section
2. The template identifies the refund key, exposure caps, and deadline cap required for authorization
3. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/51](https://github.com/ImmortalDemonGod/money-agent/pull/51)
- **Requirements Verified:** Operators need a complete verifier-side provisioning contract for mechanically guaranteed obligations

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`d8adf3b`](https://github.com/ImmortalDemonGod/money-agent/tree/d8adf3b08d187057b2dde6f729b29c595dd49e2f))

- [`.env.example#L32-L42`](https://github.com/ImmortalDemonGod/money-agent/blob/d8adf3b08d187057b2dde6f729b29c595dd49e2f/.env.example#L32-L42)

### Class A (Execution Evidence)

**WARNING:** No tests found that directly import or reference the changed file.
This file has no claim-specific execution evidence.

### Code Quality (Linting & Types)

- **ruff:** 33 error(s)
- **mypy:** Found 3 errors in 1 file (checked 1 source file)

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
| 1 | The environment template keeps obligation authorization defa... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | The template identifies the refund key, exposure caps, and d... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 3 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 2 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), pytest (no claim-specific tests found), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Document every verifier-only input for guarded obligations

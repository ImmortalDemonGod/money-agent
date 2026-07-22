# AIV Evidence File (v1.0)

**File:** `bin/setup_sandbox.sh`
**Commit:** `4d65006`
**Generated:** 2026-07-22T21:07:31Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R1
  sod_mode: S0
  critical_surfaces: []
  blast_radius: "bin/setup_sandbox.sh"
  classification_rationale: "R1 because this is a local readiness check whose failure does not alter financial calculations"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T21:07:31Z"
```

## Claim(s)

1. setup_sandbox rejects an armed signing configuration when ssh-keygen is unavailable
2. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/issues/36](https://github.com/ImmortalDemonGod/money-agent/issues/36)
- **Requirements Verified:** Issue #36 requires signed facts to be verifiable before they are treated as grounded

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`4d65006`](https://github.com/ImmortalDemonGod/money-agent/tree/4d65006cb47c6849a63a616f08b9832d269c1d89))

- [`bin/setup_sandbox.sh#L117-L126`](https://github.com/ImmortalDemonGod/money-agent/blob/4d65006cb47c6849a63a616f08b9832d269c1d89/bin/setup_sandbox.sh#L117-L126)

### Class A (Execution Evidence)

**WARNING:** No tests found that directly import or reference the changed file.
This file has no claim-specific execution evidence.

### Code Quality (Linting & Types)

- **ruff:** 3351 error(s)
- **mypy:** Found 1 error in 1 file (errors prevented further checking)

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | setup_sandbox rejects an armed signing configuration when ss... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted during this chang... | structural | Class C not collected | REVIEW MANUAL REVIEW |

**Verdict summary:** 0 verified, 0 unverified, 2 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), pytest (no claim-specific tests found).
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Check ssh-keygen before starting an armed signed-fact run

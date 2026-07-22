# AIV Evidence File (v1.0)

**File:** `tests/sim.sh`
**Commit:** `ef92b16`
**Previous:** `e53b606`
**Generated:** 2026-07-22T21:56:34Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "tests/sim.sh"
  classification_rationale: "R3 regression coverage for verifier verdict integrity"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T21:56:34Z"
```

## Claim(s)

1. The simulation rejects non-finite or zero-sample edge registrations and verifies peak state is keyed by the frozen registration
2. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/issues/38](https://github.com/ImmortalDemonGod/money-agent/issues/38)
- **Requirements Verified:** Issue #38 requires a mechanically effective frozen risk constraint

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`ef92b16`](https://github.com/ImmortalDemonGod/money-agent/tree/ef92b167a8fb8dbe93299decfb4f2c0aecbfe9dc))

- [`tests/sim.sh#L238-L243`](https://github.com/ImmortalDemonGod/money-agent/blob/ef92b167a8fb8dbe93299decfb4f2c0aecbfe9dc/tests/sim.sh#L238-L243)

### Class A (Execution Evidence)

**WARNING:** No tests found that directly import or reference the changed file.
This file has no claim-specific execution evidence.

### Code Quality (Linting & Types)

- **ruff:** 14226 error(s)
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
e53b606 test(delivery): reject unrelated Stripe success URLs
aa1dc15 [S6] edge-verdict quality: frozen risk cap + peak tracking + signed edge facts (#38, closes the S4 edge-signing deferral)
fe0427a [S5] gates & probes: delivery seam + provider cap, oracle-classed resolutions, mechanical pacing (#39 #35 #40 #45)
655bb5b test(verifier): cover initial truth signing failure
4c0df17 test(verifier): reject unsigned attestation output
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | The simulation rejects non-finite or zero-sample edge regist... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 1 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), pytest (no claim-specific tests found), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Cover finite drawdown caps and registration-scoped peak tracking

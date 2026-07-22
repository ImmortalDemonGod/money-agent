# AIV Evidence File (v1.0)

**File:** `tests/sim.sh`
**Commit:** `17c5b28`
**Previous:** `655bb5b`
**Generated:** 2026-07-22T21:54:19Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "tests/sim.sh"
  classification_rationale: "R3 regression coverage for a payment-delivery boundary"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T21:54:19Z"
```

## Claim(s)

1. The simulation rejects a payment link whose provider-configured completion redirect differs from the checked delivery artifact
2. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/issues/39](https://github.com/ImmortalDemonGod/money-agent/issues/39)
- **Requirements Verified:** Issue #39 requires the delivery check to validate the post-payment destination

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`17c5b28`](https://github.com/ImmortalDemonGod/money-agent/tree/17c5b28447720bb566dd11ddff3f0c727ec1ecc0))

- [`tests/sim.sh#L567`](https://github.com/ImmortalDemonGod/money-agent/blob/17c5b28447720bb566dd11ddff3f0c727ec1ecc0/tests/sim.sh#L567)
- [`tests/sim.sh#L569-L570`](https://github.com/ImmortalDemonGod/money-agent/blob/17c5b28447720bb566dd11ddff3f0c727ec1ecc0/tests/sim.sh#L569-L570)
- [`tests/sim.sh#L586-L588`](https://github.com/ImmortalDemonGod/money-agent/blob/17c5b28447720bb566dd11ddff3f0c727ec1ecc0/tests/sim.sh#L586-L588)

### Class A (Execution Evidence)

**WARNING:** No tests found that directly import or reference the changed file.
This file has no claim-specific execution evidence.

### Code Quality (Linting & Types)

- **ruff:** 14215 error(s)
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
aa1dc15 [S6] edge-verdict quality: frozen risk cap + peak tracking + signed edge facts (#38, closes the S4 edge-signing deferral)
fe0427a [S5] gates & probes: delivery seam + provider cap, oracle-classed resolutions, mechanical pacing (#39 #35 #40 #45)
655bb5b test(verifier): cover initial truth signing failure
4c0df17 test(verifier): reject unsigned attestation output
46c2a41 docs(tests): record verifier hardening bug catalog
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | The simulation rejects a payment link whose provider-configu... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 1 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), pytest (no claim-specific tests found), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Cover Stripe completion redirect binding in the delivery simulation

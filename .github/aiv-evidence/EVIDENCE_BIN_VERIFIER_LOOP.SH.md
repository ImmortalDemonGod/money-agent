# AIV Evidence File (v1.0)

**File:** `bin/verifier_loop.sh`
**Commit:** `6c60c4a`
**Generated:** 2026-07-22T21:07:12Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "bin/verifier_loop.sh"
  classification_rationale: "R3 because this loop publishes the financial evidence and signing trust anchors"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T21:07:12Z"
```

## Claim(s)

1. verifier_loop publishes only present signature and attestation artifacts without an absent optional artifact corrupting the staging outcome
2. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/issues/36](https://github.com/ImmortalDemonGod/money-agent/issues/36)
- **Requirements Verified:** Issue #36 requires verifier-produced signed facts to be published on the facts lane

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`6c60c4a`](https://github.com/ImmortalDemonGod/money-agent/tree/6c60c4affadd11ee72f6bd96eaa3cf36c9c96833))

- [`bin/verifier_loop.sh#L190-L196`](https://github.com/ImmortalDemonGod/money-agent/blob/6c60c4affadd11ee72f6bd96eaa3cf36c9c96833/bin/verifier_loop.sh#L190-L196)

### Class A (Execution Evidence)

**WARNING:** No tests found that directly import or reference the changed file.
This file has no claim-specific execution evidence.

### Code Quality (Linting & Types)

- **ruff:** 4668 error(s)
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
46c2a41 docs(tests): record verifier hardening bug catalog
54ef777 test(verifier): cover raw paths and inference CSV validation
abe8811 test(corpus): fail closed on fixture probe crashes
93a3e7d test(verifier): cover raw quarantine move failure
b2dcae1 [S3] durability + metering: raw-pull side-car/quarantine, unpushed counter, inference cost (#46 #41)
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | verifier_loop publishes only present signature and attestati... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 1 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), pytest (no claim-specific tests found), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Publish fact signatures and attestations safely when provisioned

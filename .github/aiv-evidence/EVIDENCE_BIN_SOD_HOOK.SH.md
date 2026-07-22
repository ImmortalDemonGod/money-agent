# AIV Evidence File (v1.0)

**File:** `bin/sod_hook.sh`
**Commit:** `8c1609d`
**Generated:** 2026-07-22T21:07:21Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "bin/sod_hook.sh"
  classification_rationale: "R3 because modifying a signing trust anchor would allow forged financial facts"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T21:07:21Z"
```

## Claim(s)

1. the agent cannot stage verifier public-key or allowed-signer changes without verifier authority
2. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/issues/36](https://github.com/ImmortalDemonGod/money-agent/issues/36)
- **Requirements Verified:** Issue #36 requires the verifier signing key to be the fact-lane trust anchor rather than agent-controlled metadata

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`8c1609d`](https://github.com/ImmortalDemonGod/money-agent/tree/8c1609d8116f56593afa6beae50ec0a360d0c99e))

- [`bin/sod_hook.sh#L13`](https://github.com/ImmortalDemonGod/money-agent/blob/8c1609d8116f56593afa6beae50ec0a360d0c99e/bin/sod_hook.sh#L13)
- [`bin/sod_hook.sh#L42-L45`](https://github.com/ImmortalDemonGod/money-agent/blob/8c1609d8116f56593afa6beae50ec0a360d0c99e/bin/sod_hook.sh#L42-L45)

### Class A (Execution Evidence)

**WARNING:** No tests found that directly import or reference the changed file.
This file has no claim-specific execution evidence.

### Code Quality (Linting & Types)

- **ruff:** 1794 error(s)
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
| 1 | the agent cannot stage verifier public-key or allowed-signer... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 1 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), pytest (no claim-specific tests found), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Treat verifier signing anchors as verifier-owned

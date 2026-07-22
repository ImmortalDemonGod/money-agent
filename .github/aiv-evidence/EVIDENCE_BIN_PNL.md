# AIV Evidence File (v1.0)

**File:** `bin/pnl.py`
**Commit:** `a410be6`
**Generated:** 2026-07-22T21:06:25Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "bin/pnl.py"
  classification_rationale: "R3 because this verifier-owned payment evidence determines whether public financial facts are trusted"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T21:06:25Z"
```

## Claim(s)

1. pnl.py removes an unsigned attestation and marks truth unverified when attestation signing fails
2. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/issues/42](https://github.com/ImmortalDemonGod/money-agent/issues/42)
- **Requirements Verified:** Issue #42 requires a verifier-signed public attestation rather than an unsigned customer-facing claim

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`a410be6`](https://github.com/ImmortalDemonGod/money-agent/tree/a410be65e3dd0d484b32c799e9418857926c6c31))

- [`bin/pnl.py#L523-L534`](https://github.com/ImmortalDemonGod/money-agent/blob/a410be65e3dd0d484b32c799e9418857926c6c31/bin/pnl.py#L523-L534)
- [`bin/pnl.py#L537`](https://github.com/ImmortalDemonGod/money-agent/blob/a410be65e3dd0d484b32c799e9418857926c6c31/bin/pnl.py#L537)
- [`bin/pnl.py#L576-L649`](https://github.com/ImmortalDemonGod/money-agent/blob/a410be65e3dd0d484b32c799e9418857926c6c31/bin/pnl.py#L576-L649)

### Class A (Execution Evidence)

**Per-symbol test coverage (AST analysis):**

- **`main`** (L523-L534): FAIL -- WARNING: No tests import or call `main`

**Coverage summary:** 0/1 symbols verified by tests.

### Code Quality (Linting & Types)

- **ruff:** All checks passed
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
46c2a41 docs(tests): record verifier hardening bug catalog
54ef777 test(verifier): cover raw paths and inference CSV validation
abe8811 test(corpus): fail closed on fixture probe crashes
93a3e7d test(verifier): cover raw quarantine move failure
b2dcae1 [S3] durability + metering: raw-pull side-car/quarantine, unpushed counter, inference cost (#46 #41)
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | pnl.py removes an unsigned attestation and marks truth unver... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 1 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), AST symbol-to-test binding (0/1 symbols verified), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Prevent publication of unsigned attestations after signing failure

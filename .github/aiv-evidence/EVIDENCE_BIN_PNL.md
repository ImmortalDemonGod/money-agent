# AIV Evidence File (v1.0)

**File:** `bin/pnl.py`
**Commit:** `42280fd`
**Previous:** `0ad5b46`
**Generated:** 2026-07-22T21:09:31Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "bin/pnl.py"
  classification_rationale: "R3 because a stale or missing signature changes whether payment facts are grounded"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T21:09:31Z"
```

## Claim(s)

1. pnl.py replaces the prior truth signature before re-signing the unverified record produced by an attestation signing failure
2. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/issues/42](https://github.com/ImmortalDemonGod/money-agent/issues/42)
- **Requirements Verified:** Issue #42 requires a failed attestation signature to fail closed without invalidating the signed truth evidence

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`42280fd`](https://github.com/ImmortalDemonGod/money-agent/tree/42280fd03af5c4e764cf2464e8fb716604591171))

- [`bin/pnl.py#L644-L646`](https://github.com/ImmortalDemonGod/money-agent/blob/42280fd03af5c4e764cf2464e8fb716604591171/bin/pnl.py#L644-L646)

### Class A (Execution Evidence)

**Per-symbol test coverage (AST analysis):**

- **`main`** (L644-L646): FAIL -- WARNING: No tests import or call `main`

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
4c0df17 test(verifier): reject unsigned attestation output
46c2a41 docs(tests): record verifier hardening bug catalog
54ef777 test(verifier): cover raw paths and inference CSV validation
abe8811 test(corpus): fail closed on fixture probe crashes
93a3e7d test(verifier): cover raw quarantine move failure
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | pnl.py replaces the prior truth signature before re-signing ... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 1 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), AST symbol-to-test binding (0/1 symbols verified), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Re-sign the unverified truth record after attestation failure

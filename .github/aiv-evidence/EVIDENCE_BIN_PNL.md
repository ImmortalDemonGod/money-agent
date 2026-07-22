# AIV Evidence File (v1.0)

**File:** `bin/pnl.py`
**Commit:** `4c2cc7b`
**Previous:** `35217cf`
**Generated:** 2026-07-22T21:15:10Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "bin/pnl.py"
  classification_rationale: "R3 because this controls the verified status of signed payment facts"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T21:15:10Z"
```

## Claim(s)

1. pnl.py marks truth unverified on an initial signing failure or missing signing key even though truth errors share the verifier error list
2. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/issues/36](https://github.com/ImmortalDemonGod/money-agent/issues/36)
- **Requirements Verified:** Issue #36 requires an armed unsigned or unverified fact record to fail closed

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`4c2cc7b`](https://github.com/ImmortalDemonGod/money-agent/tree/4c2cc7b83b029afe3ca11c990c2b24bb8761a113))

- [`bin/pnl.py#L582-L584`](https://github.com/ImmortalDemonGod/money-agent/blob/4c2cc7b83b029afe3ca11c990c2b24bb8761a113/bin/pnl.py#L582-L584)
- [`bin/pnl.py#L600`](https://github.com/ImmortalDemonGod/money-agent/blob/4c2cc7b83b029afe3ca11c990c2b24bb8761a113/bin/pnl.py#L600)

### Class A (Execution Evidence)

**Per-symbol test coverage (AST analysis):**

- **`main`** (L582-L584): FAIL -- WARNING: No tests import or call `main`

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
| 1 | pnl.py marks truth unverified on an initial signing failure ... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 1 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), AST symbol-to-test binding (0/1 symbols verified), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Persist initial truth signing failures as unverified facts

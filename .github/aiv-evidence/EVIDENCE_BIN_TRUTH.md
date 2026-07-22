# AIV Evidence File (v1.0)

**File:** `bin/truth.py`
**Commit:** `0ad5b46`
**Generated:** 2026-07-22T21:06:49Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "bin/truth.py"
  classification_rationale: "R3 because this is the trust boundary for payment facts and audit evidence"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T21:06:49Z"
```

## Claim(s)

1. truth.py refuses grounded truth.json when an armed verifier signature is missing, invalid, or has a broken predecessor hash
2. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/issues/36](https://github.com/ImmortalDemonGod/money-agent/issues/36)
- **Requirements Verified:** Issue #36 requires verifier-only signing and hash-chain validation before facts are grounded

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`0ad5b46`](https://github.com/ImmortalDemonGod/money-agent/tree/0ad5b46360ed0a571ed1001475d48c373b718678))

- [`bin/truth.py#L53-L55`](https://github.com/ImmortalDemonGod/money-agent/blob/0ad5b46360ed0a571ed1001475d48c373b718678/bin/truth.py#L53-L55)
- [`bin/truth.py#L62-L122`](https://github.com/ImmortalDemonGod/money-agent/blob/0ad5b46360ed0a571ed1001475d48c373b718678/bin/truth.py#L62-L122)
- [`bin/truth.py#L148`](https://github.com/ImmortalDemonGod/money-agent/blob/0ad5b46360ed0a571ed1001475d48c373b718678/bin/truth.py#L148)
- [`bin/truth.py#L157`](https://github.com/ImmortalDemonGod/money-agent/blob/0ad5b46360ed0a571ed1001475d48c373b718678/bin/truth.py#L157)
- [`bin/truth.py#L160-L161`](https://github.com/ImmortalDemonGod/money-agent/blob/0ad5b46360ed0a571ed1001475d48c373b718678/bin/truth.py#L160-L161)

### Class A (Execution Evidence)

**Per-symbol test coverage (AST analysis):**

- **`_git_bytes`** (L53-L55): FAIL -- WARNING: No tests import or call `_git_bytes`
- **`_enforce_signature`** (L62-L122): FAIL -- WARNING: No tests import or call `_enforce_signature`
- **`load`** (L148): FAIL -- WARNING: No tests import or call `load`

**Coverage summary:** 0/3 symbols verified by tests.

### Code Quality (Linting & Types)

- **ruff:** 26 error(s)
- **mypy:** Success: no issues found in 1 source file

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
| 1 | truth.py refuses grounded truth.json when an armed verifier ... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 1 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), AST symbol-to-test binding (0/3 symbols verified), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Verify signed truth records and predecessor hashes before grounding

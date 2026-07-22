# AIV Evidence File (v1.0)

**File:** `harness/beacon/worker.js`
**Commit:** `f8c9056`
**Generated:** 2026-07-22T21:30:14Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "harness/beacon/worker.js"
  classification_rationale: "R3 because the worker processes visitor-related data and publishes privacy disclosures"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T21:30:14Z"
```

## Claim(s)

1. the beacon stores no hit and suppresses its salted-hash privacy claim when HASH_SALT is absent
2. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/56](https://github.com/ImmortalDemonGod/money-agent/pull/56)
- **Requirements Verified:** PR #56 must not publish reversible IP-derived identifiers

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`f8c9056`](https://github.com/ImmortalDemonGod/money-agent/tree/f8c905687c7b849c952ff5d5901dafe798365ccc))

- [`harness/beacon/worker.js#L60-L69`](https://github.com/ImmortalDemonGod/money-agent/blob/f8c905687c7b849c952ff5d5901dafe798365ccc/harness/beacon/worker.js#L60-L69)
- [`harness/beacon/worker.js#L71-L79`](https://github.com/ImmortalDemonGod/money-agent/blob/f8c905687c7b849c952ff5d5901dafe798365ccc/harness/beacon/worker.js#L71-L79)
- [`harness/beacon/worker.js#L106`](https://github.com/ImmortalDemonGod/money-agent/blob/f8c905687c7b849c952ff5d5901dafe798365ccc/harness/beacon/worker.js#L106)
- [`harness/beacon/worker.js#L113-L117`](https://github.com/ImmortalDemonGod/money-agent/blob/f8c905687c7b849c952ff5d5901dafe798365ccc/harness/beacon/worker.js#L113-L117)
- [`harness/beacon/worker.js#L119`](https://github.com/ImmortalDemonGod/money-agent/blob/f8c905687c7b849c952ff5d5901dafe798365ccc/harness/beacon/worker.js#L119)
- [`harness/beacon/worker.js#L150`](https://github.com/ImmortalDemonGod/money-agent/blob/f8c905687c7b849c952ff5d5901dafe798365ccc/harness/beacon/worker.js#L150)
- [`harness/beacon/worker.js#L156-L164`](https://github.com/ImmortalDemonGod/money-agent/blob/f8c905687c7b849c952ff5d5901dafe798365ccc/harness/beacon/worker.js#L156-L164)
- [`harness/beacon/worker.js#L174`](https://github.com/ImmortalDemonGod/money-agent/blob/f8c905687c7b849c952ff5d5901dafe798365ccc/harness/beacon/worker.js#L174)
- [`harness/beacon/worker.js#L199`](https://github.com/ImmortalDemonGod/money-agent/blob/f8c905687c7b849c952ff5d5901dafe798365ccc/harness/beacon/worker.js#L199)
- [`harness/beacon/worker.js#L233`](https://github.com/ImmortalDemonGod/money-agent/blob/f8c905687c7b849c952ff5d5901dafe798365ccc/harness/beacon/worker.js#L233)

### Class A (Execution Evidence)

**Per-symbol test coverage (AST analysis):**

- **`isAsset`** (L60-L69): FAIL -- WARNING: 1 file(s) import `isAsset` but 0 tests call it directly
  - Imported by: `tests/beacon.mjs`
- **`assetSql`** (L71-L79): FAIL -- WARNING: 1 file(s) import `assetSql` but 0 tests call it directly
  - Imported by: `tests/beacon.mjs`
- **`logHit`** (L106): FAIL -- WARNING: 1 file(s) import `logHit` but 0 tests call it directly
  - Imported by: `tests/beacon.mjs`
- **`privacyHtml`** (L113-L117): FAIL -- WARNING: No tests import or call `privacyHtml`
- **`stats`** (L119): FAIL -- WARNING: No tests import or call `stats`
- **`fetch`** (L150): FAIL -- WARNING: No tests import or call `fetch`

**Coverage summary:** 0/6 symbols verified by tests.

### Code Quality (Linting & Types)

- **ruff:** 15585 error(s)
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
655bb5b test(verifier): cover initial truth signing failure
4c0df17 test(verifier): reject unsigned attestation output
46c2a41 docs(tests): record verifier hardening bug catalog
54ef777 test(verifier): cover raw paths and inference CSV validation
abe8811 test(corpus): fail closed on fixture probe crashes
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | the beacon stores no hit and suppresses its salted-hash priv... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 1 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), AST symbol-to-test binding (0/6 symbols verified), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Fail closed without HASH_SALT and unify asset classification

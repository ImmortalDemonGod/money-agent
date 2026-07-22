# AIV Evidence File (v1.0)

**File:** `harness/beacon/worker.js`
**Commit:** `3ece9ba`
**Previous:** `e4e2241`
**Generated:** 2026-07-22T21:41:04Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R2
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "harness/beacon/worker.js"
  classification_rationale: "R2 because this supports testability of visitor-data processing logic"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T21:41:04Z"
```

## Claim(s)

1. the beacon exposes its pure classification and aggregation seams for regression verification
2. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/56](https://github.com/ImmortalDemonGod/money-agent/pull/56)
- **Requirements Verified:** PR #56 must retain regression coverage for visitor classification and stable empty aggregates

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`3ece9ba`](https://github.com/ImmortalDemonGod/money-agent/tree/3ece9bae09088ba413614e0a158a7a36e51b1725))

- [`harness/beacon/worker.js#L52`](https://github.com/ImmortalDemonGod/money-agent/blob/3ece9bae09088ba413614e0a158a7a36e51b1725/harness/beacon/worker.js#L52)
- [`harness/beacon/worker.js#L81`](https://github.com/ImmortalDemonGod/money-agent/blob/3ece9bae09088ba413614e0a158a7a36e51b1725/harness/beacon/worker.js#L81)
- [`harness/beacon/worker.js#L194`](https://github.com/ImmortalDemonGod/money-agent/blob/3ece9bae09088ba413614e0a158a7a36e51b1725/harness/beacon/worker.js#L194)

### Class A (Execution Evidence)

**Per-symbol test coverage (AST analysis):**

- **`isDatacenterOrg`** (L52): FAIL -- WARNING: 1 file(s) import `isDatacenterOrg` but 0 tests call it directly
  - Imported by: `tests/beacon.mjs`
- **`classifyBot`** (L81): FAIL -- WARNING: 1 file(s) import `classifyBot` but 0 tests call it directly
  - Imported by: `tests/beacon.mjs`
- **`stats`** (L194): FAIL -- WARNING: 1 file(s) import `stats` but 0 tests call it directly
  - Imported by: `tests/beacon.mjs`

**Coverage summary:** 0/3 symbols verified by tests.

### Code Quality (Linting & Types)

- **ruff:** 15618 error(s)
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
3ece9ba test(reach): cover archived ledger lookup
047b09c test(beacon): cover privacy guard and asset parity
655bb5b test(verifier): cover initial truth signing failure
4c0df17 test(verifier): reject unsigned attestation output
46c2a41 docs(tests): record verifier hardening bug catalog
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | the beacon exposes its pure classification and aggregation s... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 1 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), AST symbol-to-test binding (0/3 symbols verified), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Expose beacon classification and stats for regression tests

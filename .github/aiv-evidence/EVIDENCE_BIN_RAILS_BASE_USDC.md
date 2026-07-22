# AIV Evidence File (v1.0)

**File:** `bin/rails/base_usdc.py`
**Commit:** `e07aefd`
**Generated:** 2026-07-22T22:03:34Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "bin/rails/base_usdc.py"
  classification_rationale: "R3 under AIV section 5.2 because this changes payment verification, wash-trade exclusion, and the first-dollar terminal fact"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T22:03:34Z"
```

## Claim(s)

1. Base USDC scoring counts only safe-or-finalized transfers whose marketplace event binds payer, payee, and amount
2. Operator-funded escrow payouts classify as self revenue even when the ERC-20 sender is the escrow contract
3. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/commit/e07aefd61e52f61d314cc211df056ee312793da3](https://github.com/ImmortalDemonGod/money-agent/commit/e07aefd61e52f61d314cc211df056ee312793da3)
- **Requirements Verified:** Correct PR #50 S7 trust-boundary defects before merge

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`e07aefd`](https://github.com/ImmortalDemonGod/money-agent/tree/e07aefd61e52f61d314cc211df056ee312793da3))

- [`bin/rails/base_usdc.py#L14-L19`](https://github.com/ImmortalDemonGod/money-agent/blob/e07aefd61e52f61d314cc211df056ee312793da3/bin/rails/base_usdc.py#L14-L19)
- [`bin/rails/base_usdc.py#L26-L29`](https://github.com/ImmortalDemonGod/money-agent/blob/e07aefd61e52f61d314cc211df056ee312793da3/bin/rails/base_usdc.py#L26-L29)
- [`bin/rails/base_usdc.py#L64-L107`](https://github.com/ImmortalDemonGod/money-agent/blob/e07aefd61e52f61d314cc211df056ee312793da3/bin/rails/base_usdc.py#L64-L107)
- [`bin/rails/base_usdc.py#L113-L115`](https://github.com/ImmortalDemonGod/money-agent/blob/e07aefd61e52f61d314cc211df056ee312793da3/bin/rails/base_usdc.py#L113-L115)
- [`bin/rails/base_usdc.py#L123`](https://github.com/ImmortalDemonGod/money-agent/blob/e07aefd61e52f61d314cc211df056ee312793da3/bin/rails/base_usdc.py#L123)
- [`bin/rails/base_usdc.py#L127-L131`](https://github.com/ImmortalDemonGod/money-agent/blob/e07aefd61e52f61d314cc211df056ee312793da3/bin/rails/base_usdc.py#L127-L131)
- [`bin/rails/base_usdc.py#L135`](https://github.com/ImmortalDemonGod/money-agent/blob/e07aefd61e52f61d314cc211df056ee312793da3/bin/rails/base_usdc.py#L135)
- [`bin/rails/base_usdc.py#L137-L143`](https://github.com/ImmortalDemonGod/money-agent/blob/e07aefd61e52f61d314cc211df056ee312793da3/bin/rails/base_usdc.py#L137-L143)
- [`bin/rails/base_usdc.py#L153-L162`](https://github.com/ImmortalDemonGod/money-agent/blob/e07aefd61e52f61d314cc211df056ee312793da3/bin/rails/base_usdc.py#L153-L162)
- [`bin/rails/base_usdc.py#L164-L169`](https://github.com/ImmortalDemonGod/money-agent/blob/e07aefd61e52f61d314cc211df056ee312793da3/bin/rails/base_usdc.py#L164-L169)

### Class A (Execution Evidence)

**Per-symbol test coverage (AST analysis):**

- **`_event_addr`** (L14-L19): FAIL -- WARNING: No tests import or call `_event_addr`
- **`_event_word`** (L26-L29): FAIL -- WARNING: No tests import or call `_event_word`
- **`_finality_anchor`** (L64-L107): FAIL -- WARNING: No tests import or call `_finality_anchor`
- **`freeze_baseline`** (L113-L115): FAIL -- WARNING: No tests import or call `freeze_baseline`
- **`pull`** (L123): FAIL -- WARNING: No tests import or call `pull`

**Coverage summary:** 0/5 symbols verified by tests.

### Code Quality (Linting & Types)

- **ruff:** All checks passed
- **mypy:** Found 10 errors in 1 file (checked 1 source file)

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
e07aefd [S8] human-actuation queue: request-don't-wait, metered, conclusion-blocking (#31) + the atomic PROMPT amendment
3143f26 [S7] rail adapters: the P1 contract + a stubbed Base/USDC rail with settlement-event binding (#30 Part 1)
aa601ba [S6] edge-verdict quality: frozen risk cap + peak tracking + signed edge facts (#38, closes the S4 edge-signing deferral)
b36b966 [S5] gates & probes: delivery seam + provider cap, oracle-classed resolutions, mechanical pacing (#39 #35 #40 #45)
2a5f010 [S4] fact-lane signing: verifier signatures + hash chain + customer attestation (#36 #42)
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | Base USDC scoring counts only safe-or-finalized transfers wh... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | Operator-funded escrow payouts classify as self revenue even... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 3 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 2 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), AST symbol-to-test binding (0/5 symbols verified), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Require finalized, identity-bound Base marketplace settlements

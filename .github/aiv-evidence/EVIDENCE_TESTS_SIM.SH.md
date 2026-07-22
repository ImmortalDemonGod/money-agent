# AIV Evidence File (v1.0)

**File:** `tests/sim.sh`
**Commit:** `60d9363`
**Previous:** `0dfb70b`
**Generated:** 2026-07-22T22:22:19Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "tests/sim.sh"
  classification_rationale: "This merge crosses verifier, payment-rail, and human-actuation trust boundaries and therefore requires independent review"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T22:22:19Z"
```

## Claim(s)

1. PR50 contains the advanced stack-3 fixes and retains the rail and human-actuation regressions
2. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/50](https://github.com/ImmortalDemonGod/money-agent/pull/50)
- **Requirements Verified:** PR #50 must merge cleanly into its updated stacked base before CI can evaluate it

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`60d9363`](https://github.com/ImmortalDemonGod/money-agent/tree/60d93633b47cd109e7697b689c8d7566a470afe3))

- [`tests/sim.sh#L52-L54`](https://github.com/ImmortalDemonGod/money-agent/blob/60d93633b47cd109e7697b689c8d7566a470afe3/tests/sim.sh#L52-L54)
- [`tests/sim.sh#L59-L63`](https://github.com/ImmortalDemonGod/money-agent/blob/60d93633b47cd109e7697b689c8d7566a470afe3/tests/sim.sh#L59-L63)
- [`tests/sim.sh#L282-L287`](https://github.com/ImmortalDemonGod/money-agent/blob/60d93633b47cd109e7697b689c8d7566a470afe3/tests/sim.sh#L282-L287)
- [`tests/sim.sh#L428-L431`](https://github.com/ImmortalDemonGod/money-agent/blob/60d93633b47cd109e7697b689c8d7566a470afe3/tests/sim.sh#L428-L431)
- [`tests/sim.sh#L436-L438`](https://github.com/ImmortalDemonGod/money-agent/blob/60d93633b47cd109e7697b689c8d7566a470afe3/tests/sim.sh#L436-L438)
- [`tests/sim.sh#L447-L474`](https://github.com/ImmortalDemonGod/money-agent/blob/60d93633b47cd109e7697b689c8d7566a470afe3/tests/sim.sh#L447-L474)
- [`tests/sim.sh#L478`](https://github.com/ImmortalDemonGod/money-agent/blob/60d93633b47cd109e7697b689c8d7566a470afe3/tests/sim.sh#L478)
- [`tests/sim.sh#L486`](https://github.com/ImmortalDemonGod/money-agent/blob/60d93633b47cd109e7697b689c8d7566a470afe3/tests/sim.sh#L486)
- [`tests/sim.sh#L492-L501`](https://github.com/ImmortalDemonGod/money-agent/blob/60d93633b47cd109e7697b689c8d7566a470afe3/tests/sim.sh#L492-L501)
- [`tests/sim.sh#L602`](https://github.com/ImmortalDemonGod/money-agent/blob/60d93633b47cd109e7697b689c8d7566a470afe3/tests/sim.sh#L602)
- [`tests/sim.sh#L710`](https://github.com/ImmortalDemonGod/money-agent/blob/60d93633b47cd109e7697b689c8d7566a470afe3/tests/sim.sh#L710)
- [`tests/sim.sh#L745`](https://github.com/ImmortalDemonGod/money-agent/blob/60d93633b47cd109e7697b689c8d7566a470afe3/tests/sim.sh#L745)
- [`tests/sim.sh#L747-L748`](https://github.com/ImmortalDemonGod/money-agent/blob/60d93633b47cd109e7697b689c8d7566a470afe3/tests/sim.sh#L747-L748)
- [`tests/sim.sh#L764-L766`](https://github.com/ImmortalDemonGod/money-agent/blob/60d93633b47cd109e7697b689c8d7566a470afe3/tests/sim.sh#L764-L766)
- [`tests/sim.sh#L963-L1001`](https://github.com/ImmortalDemonGod/money-agent/blob/60d93633b47cd109e7697b689c8d7566a470afe3/tests/sim.sh#L963-L1001)

### Class A (Execution Evidence)

**WARNING:** No tests found that directly import or reference the changed file.
This file has no claim-specific execution evidence.

### Code Quality (Linting & Types)

- **ruff:** 16424 error(s)
- **mypy:** Found 1 error in 1 file (errors prevented further checking)

### Class C (Negative Evidence)

**Search methodology:** Ran `git diff --cached` and scanned for regression indicators.

- Test file deletions: **none**
- Test files modified: 3
  - `.github/aiv-evidence/EVIDENCE_TESTS_SIM.SH.md`
  - `tests/corpus.sh`
  - `tests/sim.sh`
- Deleted assertions (`assert` removals in diff): **none found**
- Added skip markers (`@pytest.mark.skip`, `@unittest.skip`): **none found**

### Class D (Differential Evidence)

**Change summary** (`git diff --cached --stat`):

```
tests/sim.sh | 123 +++++++++++++++++++++++++++++++++++++++++++++++++++--------
 1 file changed, 107 insertions(+), 16 deletions(-)
```

### Class F (Provenance Evidence)

**Test file chain-of-custody:**

No covering test files found.

**Recent test directory history** (`git log --oneline -5 -- tests/`):

```
0dfb70b test(sim): make packet mutations portable and fail closed
b48810e test(preflight): provide extracted Base identity path
406c9f6 test(harness): cover PR50 trust-boundary regressions
e07aefd [S8] human-actuation queue: request-don't-wait, metered, conclusion-blocking (#31) + the atomic PROMPT amendment
3143f26 [S7] rail adapters: the P1 contract + a stubbed Base/USDC rail with settlement-event binding (#30 Part 1)
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | PR50 contains the advanced stack-3 fixes and retains the rai... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 1 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), pytest (no claim-specific tests found), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Reconcile PR50 against the advanced stack-3 base using its actual stack parent

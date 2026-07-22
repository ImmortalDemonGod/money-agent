# AIV Evidence File (v1.0)

**File:** `bin/human.py`
**Commit:** `d93be03`
**Generated:** 2026-07-22T22:04:50Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "bin/human.py"
  classification_rationale: "R3 because this changes a privilege boundary, operator identity claims, and conclusion authorization"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T22:04:50Z"
```

## Claim(s)

1. The agent cannot mark a human request fulfilled or declined without a request-bound resolution published on the verifier-owned ledger branch
2. A grounded task state is persisted before its companion bet can be closed
3. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/commit/e07aefd61e52f61d314cc211df056ee312793da3](https://github.com/ImmortalDemonGod/money-agent/commit/e07aefd61e52f61d314cc211df056ee312793da3)
- **Requirements Verified:** Make operator actuation and metered human minutes independently attributable

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`d93be03`](https://github.com/ImmortalDemonGod/money-agent/tree/d93be03994bf152a78331336f3274e7cae3567ad))

- [`bin/human.py#L22-L25`](https://github.com/ImmortalDemonGod/money-agent/blob/d93be03994bf152a78331336f3274e7cae3567ad/bin/human.py#L22-L25)
- [`bin/human.py#L30-L32`](https://github.com/ImmortalDemonGod/money-agent/blob/d93be03994bf152a78331336f3274e7cae3567ad/bin/human.py#L30-L32)
- [`bin/human.py#L39`](https://github.com/ImmortalDemonGod/money-agent/blob/d93be03994bf152a78331336f3274e7cae3567ad/bin/human.py#L39)
- [`bin/human.py#L46`](https://github.com/ImmortalDemonGod/money-agent/blob/d93be03994bf152a78331336f3274e7cae3567ad/bin/human.py#L46)
- [`bin/human.py#L62-L133`](https://github.com/ImmortalDemonGod/money-agent/blob/d93be03994bf152a78331336f3274e7cae3567ad/bin/human.py#L62-L133)
- [`bin/human.py#L196-L204`](https://github.com/ImmortalDemonGod/money-agent/blob/d93be03994bf152a78331336f3274e7cae3567ad/bin/human.py#L196-L204)
- [`bin/human.py#L212-L259`](https://github.com/ImmortalDemonGod/money-agent/blob/d93be03994bf152a78331336f3274e7cae3567ad/bin/human.py#L212-L259)
- [`bin/human.py#L299-L301`](https://github.com/ImmortalDemonGod/money-agent/blob/d93be03994bf152a78331336f3274e7cae3567ad/bin/human.py#L299-L301)

### Class A (Execution Evidence)

**Per-symbol test coverage (AST analysis):**

- **`_task_hash`** (L22-L25): FAIL -- WARNING: No tests import or call `_task_hash`
- **`_git`** (L30-L32): FAIL -- WARNING: No tests import or call `_git`
- **`_operator_task`** (L39): FAIL -- WARNING: No tests import or call `_operator_task`
- **`_facts_resolutions`** (L46): FAIL -- WARNING: No tests import or call `_facts_resolutions`
- **`_publish_resolution`** (L62-L133): FAIL -- WARNING: No tests import or call `_publish_resolution`
- **`_grounded_resolution`** (L196-L204): FAIL -- WARNING: No tests import or call `_grounded_resolution`
- **`cmd_fulfill`** (L212-L259): FAIL -- WARNING: No tests import or call `cmd_fulfill`
- **`cmd_decline`** (L299-L301): FAIL -- WARNING: No tests import or call `cmd_decline`
- **`cmd_sync`** (unknown): FAIL -- WARNING: No tests import or call `cmd_sync`
- **`main`** (unknown): FAIL -- WARNING: No tests import or call `main`

**Coverage summary:** 0/10 symbols verified by tests.

### Code Quality (Linting & Types)

- **ruff:** All checks passed
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
e07aefd [S8] human-actuation queue: request-don't-wait, metered, conclusion-blocking (#31) + the atomic PROMPT amendment
3143f26 [S7] rail adapters: the P1 contract + a stubbed Base/USDC rail with settlement-event binding (#30 Part 1)
aa601ba [S6] edge-verdict quality: frozen risk cap + peak tracking + signed edge facts (#38, closes the S4 edge-signing deferral)
b36b966 [S5] gates & probes: delivery seam + provider cap, oracle-classed resolutions, mechanical pacing (#39 #35 #40 #45)
2a5f010 [S4] fact-lane signing: verifier signatures + hash chain + customer attestation (#36 #42)
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | The agent cannot mark a human request fulfilled or declined ... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | A grounded task state is persisted before its companion bet ... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 3 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 2 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), AST symbol-to-test binding (0/10 symbols verified), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Move human actuation resolution to the verifier facts lane

# AIV Evidence File (v1.0)

**File:** `bin/bet_gate.py`
**Commit:** `937c8d6`
**Generated:** 2026-07-22T22:05:20Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "bin/bet_gate.py"
  classification_rationale: "Touches payment authorization and external-action control, critical surfaces under AIV section 5.2"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T22:05:20Z"
```

## Claim(s)

1. Armed external actions require an explicit valid bet and matching lane
2. Spend authorization rejects non-finite amounts and cumulative spend above the registered cap
3. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/51](https://github.com/ImmortalDemonGod/money-agent/pull/51)
- **Requirements Verified:** PR 51 requires typed action reservations and max_spend_usd to mechanically bound external effects

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`937c8d6`](https://github.com/ImmortalDemonGod/money-agent/tree/937c8d6977223337b72526cbfb224f5d397e9101))

- [`bin/bet_gate.py#L31-L32`](https://github.com/ImmortalDemonGod/money-agent/blob/937c8d6977223337b72526cbfb224f5d397e9101/bin/bet_gate.py#L31-L32)
- [`bin/bet_gate.py#L36`](https://github.com/ImmortalDemonGod/money-agent/blob/937c8d6977223337b72526cbfb224f5d397e9101/bin/bet_gate.py#L36)
- [`bin/bet_gate.py#L54-L58`](https://github.com/ImmortalDemonGod/money-agent/blob/937c8d6977223337b72526cbfb224f5d397e9101/bin/bet_gate.py#L54-L58)
- [`bin/bet_gate.py#L85-L88`](https://github.com/ImmortalDemonGod/money-agent/blob/937c8d6977223337b72526cbfb224f5d397e9101/bin/bet_gate.py#L85-L88)
- [`bin/bet_gate.py#L102-L109`](https://github.com/ImmortalDemonGod/money-agent/blob/937c8d6977223337b72526cbfb224f5d397e9101/bin/bet_gate.py#L102-L109)
- [`bin/bet_gate.py#L113-L114`](https://github.com/ImmortalDemonGod/money-agent/blob/937c8d6977223337b72526cbfb224f5d397e9101/bin/bet_gate.py#L113-L114)
- [`bin/bet_gate.py#L119-L125`](https://github.com/ImmortalDemonGod/money-agent/blob/937c8d6977223337b72526cbfb224f5d397e9101/bin/bet_gate.py#L119-L125)
- [`bin/bet_gate.py#L129`](https://github.com/ImmortalDemonGod/money-agent/blob/937c8d6977223337b72526cbfb224f5d397e9101/bin/bet_gate.py#L129)
- [`bin/bet_gate.py#L131-L136`](https://github.com/ImmortalDemonGod/money-agent/blob/937c8d6977223337b72526cbfb224f5d397e9101/bin/bet_gate.py#L131-L136)
- [`bin/bet_gate.py#L139-L143`](https://github.com/ImmortalDemonGod/money-agent/blob/937c8d6977223337b72526cbfb224f5d397e9101/bin/bet_gate.py#L139-L143)
- [`bin/bet_gate.py#L146-L147`](https://github.com/ImmortalDemonGod/money-agent/blob/937c8d6977223337b72526cbfb224f5d397e9101/bin/bet_gate.py#L146-L147)
- [`bin/bet_gate.py#L152`](https://github.com/ImmortalDemonGod/money-agent/blob/937c8d6977223337b72526cbfb224f5d397e9101/bin/bet_gate.py#L152)
- [`bin/bet_gate.py#L174-L183`](https://github.com/ImmortalDemonGod/money-agent/blob/937c8d6977223337b72526cbfb224f5d397e9101/bin/bet_gate.py#L174-L183)

### Class A (Execution Evidence)

**Per-symbol test coverage (AST analysis):**

- **`_finite_number`** (L31-L32): FAIL -- WARNING: No tests import or call `_finite_number`
- **`validate_bet`** (L36): FAIL -- WARNING: No tests import or call `validate_bet`
- **`authorize`** (L54-L58): FAIL -- WARNING: No tests import or call `authorize`
- **`main`** (L85-L88): FAIL -- WARNING: No tests import or call `main`
- **`option`** (L102-L109): FAIL -- WARNING: No tests import or call `option`

**Coverage summary:** 0/5 symbols verified by tests.

### Code Quality (Linting & Types)

- **ruff:** 14 error(s)
- **mypy:** Found 9 errors in 3 files (checked 1 source file)

### Class C (Negative Evidence)

**Search methodology:** Ran `git diff --cached` and scanned for regression indicators.

- Test file deletions: **none**
- Test file modifications: **none**
- Deleted assertions (`assert` removals in diff): **none found**
- Added skip markers (`@pytest.mark.skip`, `@unittest.skip`): **none found**

### Class D (Differential Evidence)

**Change summary** (`git diff --cached --stat`):

```
bin/bet_gate.py | 66 ++++++++++++++++++++++++++++++++++++++++++++++-----------
 1 file changed, 54 insertions(+), 12 deletions(-)
```

### Class F (Provenance Evidence)

**Test file chain-of-custody:**

No covering test files found.

**Recent test directory history** (`git log --oneline -5 -- tests/`):

```
937c8d6 [S11] P-generalizations: prereg, decision gate, obligations+watchdog, probe registry, exposure caps
7b7a7fe [S10] V3 spine: per-lane stage ordering, config-gated off (the contested layer, by explicit switch)
644f13c [S9] V3 typed bet-spec + action authorization, config-gated off (bet-ledger layer)
e07aefd [S8] human-actuation queue: request-don't-wait, metered, conclusion-blocking (#31) + the atomic PROMPT amendment
3143f26 [S7] rail adapters: the P1 contract + a stubbed Base/USDC rail with settlement-event binding (#30 Part 1)
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | Armed external actions require an explicit valid bet and mat... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | Spend authorization rejects non-finite amounts and cumulativ... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 3 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 2 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), AST symbol-to-test binding (0/5 symbols verified), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Fail closed on ambiguous, malformed, or over-cap bet authorizations

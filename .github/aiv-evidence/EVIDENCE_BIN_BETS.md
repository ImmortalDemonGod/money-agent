# AIV Evidence File (v1.0)

**File:** `bin/bets.py`
**Commit:** `33733b7`
**Generated:** 2026-07-22T22:05:33Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "bin/bets.py"
  classification_rationale: "Touches the audit log and payment-reservation state, both AIV section 5.2 critical surfaces"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T22:05:33Z"
```

## Claim(s)

1. Bet registry saves commit only run/bets.json and leave unrelated staged files untouched
2. Typed bets initialize cumulative spend accounting at zero
3. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/51](https://github.com/ImmortalDemonGod/money-agent/pull/51)
- **Requirements Verified:** PR 51 action reservations must be atomically auditable without sweeping unrelated work

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`33733b7`](https://github.com/ImmortalDemonGod/money-agent/tree/33733b7a1534c95fb456f5d3deb36cb34f45f73c))

- [`bin/bets.py#L66`](https://github.com/ImmortalDemonGod/money-agent/blob/33733b7a1534c95fb456f5d3deb36cb34f45f73c/bin/bets.py#L66)
- [`bin/bets.py#L68-L69`](https://github.com/ImmortalDemonGod/money-agent/blob/33733b7a1534c95fb456f5d3deb36cb34f45f73c/bin/bets.py#L68-L69)
- [`bin/bets.py#L148`](https://github.com/ImmortalDemonGod/money-agent/blob/33733b7a1534c95fb456f5d3deb36cb34f45f73c/bin/bets.py#L148)

### Class A (Execution Evidence)

**Per-symbol test coverage (AST analysis):**

- **`_save`** (L66): FAIL -- WARNING: No tests import or call `_save`
- **`cmd_add`** (L68-L69): FAIL -- WARNING: No tests import or call `cmd_add`

**Coverage summary:** 0/2 symbols verified by tests.

### Code Quality (Linting & Types)

- **ruff:** All checks passed
- **mypy:** Found 9 errors in 3 files (checked 1 source file)

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
937c8d6 [S11] P-generalizations: prereg, decision gate, obligations+watchdog, probe registry, exposure caps
7b7a7fe [S10] V3 spine: per-lane stage ordering, config-gated off (the contested layer, by explicit switch)
644f13c [S9] V3 typed bet-spec + action authorization, config-gated off (bet-ledger layer)
e07aefd [S8] human-actuation queue: request-don't-wait, metered, conclusion-blocking (#31) + the atomic PROMPT amendment
3143f26 [S7] rail adapters: the P1 contract + a stubbed Base/USDC rail with settlement-event binding (#30 Part 1)
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | Bet registry saves commit only run/bets.json and leave unrel... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | Typed bets initialize cumulative spend accounting at zero | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 3 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 2 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), AST symbol-to-test binding (0/2 symbols verified), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Make bet persistence path-limited and spend-ready

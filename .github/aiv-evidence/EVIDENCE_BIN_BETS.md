# AIV Evidence File (v1.0)

**File:** `bin/bets.py`
**Commit:** `7ad2be1`
**Previous:** `7fd00f3`
**Generated:** 2026-07-22T22:39:11Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "bin/bets.py"
  classification_rationale: "Bet authorization and outcome claims cross audit and external-effect control boundaries under AIV section 5.2"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T22:39:11Z"
```

## Claim(s)

1. Concurrent bet mutations cannot consume one reservation twice
2. Typed bet outcomes require and persist evaluation of their declared condition
3. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/51#discussion_r3634224773](https://github.com/ImmortalDemonGod/money-agent/pull/51#discussion_r3634224773)
- **Requirements Verified:** CodeRabbit requires serialized reservations and condition-bound typed resolution

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`7ad2be1`](https://github.com/ImmortalDemonGod/money-agent/tree/7ad2be1ac225aba7a67f828b1203c290d1df4c9d))

- [`bin/bets.py#L32`](https://github.com/ImmortalDemonGod/money-agent/blob/7ad2be1ac225aba7a67f828b1203c290d1df4c9d/bin/bets.py#L32)
- [`bin/bets.py#L34`](https://github.com/ImmortalDemonGod/money-agent/blob/7ad2be1ac225aba7a67f828b1203c290d1df4c9d/bin/bets.py#L34)
- [`bin/bets.py#L37`](https://github.com/ImmortalDemonGod/money-agent/blob/7ad2be1ac225aba7a67f828b1203c290d1df4c9d/bin/bets.py#L37)
- [`bin/bets.py#L42`](https://github.com/ImmortalDemonGod/money-agent/blob/7ad2be1ac225aba7a67f828b1203c290d1df4c9d/bin/bets.py#L42)
- [`bin/bets.py#L60`](https://github.com/ImmortalDemonGod/money-agent/blob/7ad2be1ac225aba7a67f828b1203c290d1df4c9d/bin/bets.py#L60)
- [`bin/bets.py#L66`](https://github.com/ImmortalDemonGod/money-agent/blob/7ad2be1ac225aba7a67f828b1203c290d1df4c9d/bin/bets.py#L66)
- [`bin/bets.py#L84-L115`](https://github.com/ImmortalDemonGod/money-agent/blob/7ad2be1ac225aba7a67f828b1203c290d1df4c9d/bin/bets.py#L84-L115)
- [`bin/bets.py#L195-L212`](https://github.com/ImmortalDemonGod/money-agent/blob/7ad2be1ac225aba7a67f828b1203c290d1df4c9d/bin/bets.py#L195-L212)
- [`bin/bets.py#L250-L257`](https://github.com/ImmortalDemonGod/money-agent/blob/7ad2be1ac225aba7a67f828b1203c290d1df4c9d/bin/bets.py#L250-L257)
- [`bin/bets.py#L262-L273`](https://github.com/ImmortalDemonGod/money-agent/blob/7ad2be1ac225aba7a67f828b1203c290d1df4c9d/bin/bets.py#L262-L273)
- [`bin/bets.py#L282-L288`](https://github.com/ImmortalDemonGod/money-agent/blob/7ad2be1ac225aba7a67f828b1203c290d1df4c9d/bin/bets.py#L282-L288)
- [`bin/bets.py#L290-L291`](https://github.com/ImmortalDemonGod/money-agent/blob/7ad2be1ac225aba7a67f828b1203c290d1df4c9d/bin/bets.py#L290-L291)
- [`bin/bets.py#L293-L297`](https://github.com/ImmortalDemonGod/money-agent/blob/7ad2be1ac225aba7a67f828b1203c290d1df4c9d/bin/bets.py#L293-L297)
- [`bin/bets.py#L299-L345`](https://github.com/ImmortalDemonGod/money-agent/blob/7ad2be1ac225aba7a67f828b1203c290d1df4c9d/bin/bets.py#L299-L345)
- [`bin/bets.py#L353-L356`](https://github.com/ImmortalDemonGod/money-agent/blob/7ad2be1ac225aba7a67f828b1203c290d1df4c9d/bin/bets.py#L353-L356)
- [`bin/bets.py#L359-L360`](https://github.com/ImmortalDemonGod/money-agent/blob/7ad2be1ac225aba7a67f828b1203c290d1df4c9d/bin/bets.py#L359-L360)

### Class A (Execution Evidence)

**Per-symbol test coverage (AST analysis):**

- **`_load_unlocked`** (L32): FAIL -- WARNING: No tests import or call `_load_unlocked`
- **`_save_unlocked`** (L34): FAIL -- WARNING: No tests import or call `_save_unlocked`
- **`_lock`** (L37): FAIL -- WARNING: No tests import or call `_lock`
- **`_load`** (L42): FAIL -- WARNING: No tests import or call `_load`
- **`_save`** (L60): PASS -- 1 test(s) call `_save` directly
  - `tests/test_v3_hardening.py::test_bets_save_path_limits_commit`
- **`_transaction`** (L66): FAIL -- WARNING: No tests import or call `_transaction`
- **`cmd_add`** (L84-L115): FAIL -- WARNING: No tests import or call `cmd_add`
- **`cmd_checked`** (L195-L212): FAIL -- WARNING: No tests import or call `cmd_checked`
- **`_evaluate_condition`** (L250-L257): FAIL -- WARNING: No tests import or call `_evaluate_condition`
- **`cmd_resolve`** (L262-L273): PASS -- 1 test(s) call `cmd_resolve` directly
  - `tests/test_v3_hardening.py::test_typed_resolution_evaluates_declared_metric`

**Coverage summary:** 2/10 symbols verified by tests.

### Code Quality (Linting & Types)

- **ruff:** All checks passed
- **mypy:** Found 10 errors in 3 files (checked 1 source file)

### Class C (Negative Evidence)

**Search methodology:** Ran `git diff --cached` and scanned for regression indicators.

- Test file deletions: **none**
- Test file modifications: **none**
- Deleted assertions (`assert` removals in diff): **none found**
- Added skip markers (`@pytest.mark.skip`, `@unittest.skip`): **none found**

### Class F (Provenance Evidence)

**Test file chain-of-custody:**

| File | Commits | Created By | Last Modified By | Assertions |
|------|---------|------------|------------------|------------|
| `tests/test_v3_hardening.py` | 1 | Miguel Ingram (a3d4a5a) | Miguel Ingram (a3d4a5a) | 25 |

**Recent test directory history** (`git log --oneline -5 -- tests/`):

```
1c0d6f2 test(sim): adversarially cover PR 51 hardening
a3d4a5a test(v3): cover adversarial enforcement seams
937c8d6 [S11] P-generalizations: prereg, decision gate, obligations+watchdog, probe registry, exposure caps
7b7a7fe [S10] V3 spine: per-lane stage ordering, config-gated off (the contested layer, by explicit switch)
644f13c [S9] V3 typed bet-spec + action authorization, config-gated off (bet-ledger layer)
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | Concurrent bet mutations cannot consume one reservation twic... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | Typed bet outcomes require and persist evaluation of their d... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 3 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 2 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), AST symbol-to-test binding (2/10 symbols verified), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Serialize the bet registry and resolve typed bets from observable conditions

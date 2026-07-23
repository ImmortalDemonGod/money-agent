# AIV Evidence File (v1.0)

**File:** `bin/bet_gate.py`
**Commit:** `6094793`
**Previous:** `0d9b980`
**Generated:** 2026-07-22T22:39:30Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "bin/bet_gate.py"
  classification_rationale: "External action authorization controls PII, spending, and audit boundaries under AIV section 5.2"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T22:39:30Z"
```

## Claim(s)

1. Two concurrent consumers cannot both spend one action reservation
2. A pre-attempt failure can compensate its bound reservation without changing lanes
3. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/51#discussion_r3634224773](https://github.com/ImmortalDemonGod/money-agent/pull/51#discussion_r3634224773)
- **Requirements Verified:** CodeRabbit requires one shared synchronization mechanism for reservation mutations

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`6094793`](https://github.com/ImmortalDemonGod/money-agent/tree/609479304a41b3a2216a57642e5d12edfdedcb71))

- [`bin/bet_gate.py#L38`](https://github.com/ImmortalDemonGod/money-agent/blob/609479304a41b3a2216a57642e5d12edfdedcb71/bin/bet_gate.py#L38)
- [`bin/bet_gate.py#L127-L140`](https://github.com/ImmortalDemonGod/money-agent/blob/609479304a41b3a2216a57642e5d12edfdedcb71/bin/bet_gate.py#L127-L140)
- [`bin/bet_gate.py#L142-L151`](https://github.com/ImmortalDemonGod/money-agent/blob/609479304a41b3a2216a57642e5d12edfdedcb71/bin/bet_gate.py#L142-L151)
- [`bin/bet_gate.py#L157-L180`](https://github.com/ImmortalDemonGod/money-agent/blob/609479304a41b3a2216a57642e5d12edfdedcb71/bin/bet_gate.py#L157-L180)

### Class A (Execution Evidence)

**Per-symbol test coverage (AST analysis):**

- **`authorize`** (L38): PASS -- 3 test(s) call `authorize` directly
  - `tests/test_v3_hardening.py::test_bet_gate_rejects_nan_and_binds_lane`
  - `tests/test_v3_hardening.py::test_bet_gate_enforces_cumulative_spend`
  - `tests/test_v3_hardening.py::test_bet_gate_serializes_reservation_consumption`
- **`rollback`** (L127-L140): FAIL -- WARNING: No tests import or call `rollback`

**Coverage summary:** 1/2 symbols verified by tests.

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
| 1 | Two concurrent consumers cannot both spend one action reserv... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | A pre-attempt failure can compensate its bound reservation w... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 3 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 2 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), AST symbol-to-test binding (1/2 symbols verified), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Use serialized bet transactions for consumption and bounded rollback

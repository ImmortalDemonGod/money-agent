# AIV Evidence File (v1.0)

**File:** `bin/obligation_watch.py`
**Commit:** `d859a60`
**Previous:** `c1dca6a`
**Generated:** 2026-07-22T23:07:11Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "bin/obligation_watch.py"
  classification_rationale: "R3 under AIV section 5.2 because verifier-held refund credentials and payment remediation are critical surfaces"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T23:07:11Z"
```

## Claim(s)

1. _authorization enables obligations only when operator enablement, refund authority, positive exposure caps, and a positive deadline cap are all present
2. main independently checks open obligations and removes verifier-confirmed deliveries from the open count
3. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/blob/29226cc090679296d15f4c9d8174a70db8749553/docs/V2_HARNESS_DESIGN.md#L791-L810](https://github.com/ImmortalDemonGod/money-agent/blob/29226cc090679296d15f4c9d8174a70db8749553/docs/V2_HARNESS_DESIGN.md#L791-L810)
- **Requirements Verified:** P5 requires an out-of-band watchdog holding refund authority to mechanically guarantee deferred delivery

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`d859a60`](https://github.com/ImmortalDemonGod/money-agent/tree/d859a605ddab22e702e3d1321cec0514ffd51a81))

- [`bin/obligation_watch.py#L2-L8`](https://github.com/ImmortalDemonGod/money-agent/blob/d859a605ddab22e702e3d1321cec0514ffd51a81/bin/obligation_watch.py#L2-L8)
- [`bin/obligation_watch.py#L27`](https://github.com/ImmortalDemonGod/money-agent/blob/d859a605ddab22e702e3d1321cec0514ffd51a81/bin/obligation_watch.py#L27)
- [`bin/obligation_watch.py#L75-L113`](https://github.com/ImmortalDemonGod/money-agent/blob/d859a605ddab22e702e3d1321cec0514ffd51a81/bin/obligation_watch.py#L75-L113)
- [`bin/obligation_watch.py#L117-L119`](https://github.com/ImmortalDemonGod/money-agent/blob/d859a605ddab22e702e3d1321cec0514ffd51a81/bin/obligation_watch.py#L117-L119)
- [`bin/obligation_watch.py#L129-L130`](https://github.com/ImmortalDemonGod/money-agent/blob/d859a605ddab22e702e3d1321cec0514ffd51a81/bin/obligation_watch.py#L129-L130)
- [`bin/obligation_watch.py#L161-L168`](https://github.com/ImmortalDemonGod/money-agent/blob/d859a605ddab22e702e3d1321cec0514ffd51a81/bin/obligation_watch.py#L161-L168)
- [`bin/obligation_watch.py#L185`](https://github.com/ImmortalDemonGod/money-agent/blob/d859a605ddab22e702e3d1321cec0514ffd51a81/bin/obligation_watch.py#L185)
- [`bin/obligation_watch.py#L187-L189`](https://github.com/ImmortalDemonGod/money-agent/blob/d859a605ddab22e702e3d1321cec0514ffd51a81/bin/obligation_watch.py#L187-L189)
- [`bin/obligation_watch.py#L191`](https://github.com/ImmortalDemonGod/money-agent/blob/d859a605ddab22e702e3d1321cec0514ffd51a81/bin/obligation_watch.py#L191)
- [`bin/obligation_watch.py#L193`](https://github.com/ImmortalDemonGod/money-agent/blob/d859a605ddab22e702e3d1321cec0514ffd51a81/bin/obligation_watch.py#L193)

### Class A (Execution Evidence)

**Per-symbol test coverage (AST analysis):**

- **`_authorization`** (L2-L8): PASS -- 2 test(s) call `_authorization` directly
  - `tests/test_v3_hardening.py::test_obligation_authorization_requires_fresh_grounded_verifier_fact`
  - `tests/test_v3_hardening.py::test_obligation_watch_authorization_requires_every_safeguard`
- **`_publish_unverified`** (L27): FAIL -- WARNING: No tests import or call `_publish_unverified`
- **`main`** (L75-L113): PASS -- 1 test(s) call `main` directly
  - `tests/test_v3_hardening.py::test_obligation_watch_checks_open_records_without_agent_claim`

**Coverage summary:** 2/3 symbols verified by tests.

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

| File | Commits | Created By | Last Modified By | Assertions |
|------|---------|------------|------------------|------------|
| `tests/test_v3_hardening.py` | 2 | Miguel Ingram (d90785d) | Miguel Ingram (76c1bec) | 36 |

**Recent test directory history** (`git log --oneline -5 -- tests/`):

```
30612e5 test(sim): exercise CodeRabbit review invariants
76c1bec test(v3): cover CodeRabbit hardening findings
bb5cbed test(sim): adversarially cover PR 51 hardening
d90785d test(v3): cover adversarial enforcement seams
1529ea1 [S11] P-generalizations: prereg, decision gate, obligations+watchdog, probe registry, exposure caps
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | _authorization enables obligations only when operator enable... | symbol | 2 test(s) call `_authorization` | PASS VERIFIED |
| 2 | main independently checks open obligations and removes verif... | symbol | 1 test(s) call `main` | PASS VERIFIED |
| 3 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 3 verified, 0 unverified, 0 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), AST symbol-to-test binding (2/3 symbols verified), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Publish the protected authorization fact and monitor liabilities independently

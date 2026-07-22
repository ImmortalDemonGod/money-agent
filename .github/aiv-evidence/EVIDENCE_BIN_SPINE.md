# AIV Evidence File (v1.0)

**File:** `bin/spine.py`
**Commit:** `4cec843`
**Generated:** 2026-07-22T22:08:46Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R2
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "bin/spine.py"
  classification_rationale: "Changes a config-gated cross-component state-machine rule with component blast radius, meeting AIV section 5.3 R2"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T22:08:46Z"
```

## Claim(s)

1. Placing a due bet into a closed or watching historical lane is evaluated as an active-lane transition and cannot exceed the active cap
2. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/51](https://github.com/ImmortalDemonGod/money-agent/pull/51)
- **Requirements Verified:** PR 51 per-lane caps must constrain post-placement state rather than only brand-new lane names

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`4cec843`](https://github.com/ImmortalDemonGod/money-agent/tree/4cec84334d534866fc51f3a20d532eaf5607c249))

- [`bin/spine.py#L175-L179`](https://github.com/ImmortalDemonGod/money-agent/blob/4cec84334d534866fc51f3a20d532eaf5607c249/bin/spine.py#L175-L179)

### Class A (Execution Evidence)

**Per-symbol test coverage (AST analysis):**

- **`check_placement`** (L175-L179): PASS -- 1 test(s) call `check_placement` directly
  - `tests/test_v3_hardening.py::test_closed_lane_cannot_reopen_past_active_cap`

**Coverage summary:** 1/1 symbols verified by tests.

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

| File | Commits | Created By | Last Modified By | Assertions |
|------|---------|------------|------------------|------------|
| `tests/test_v3_hardening.py` | 1 | Miguel Ingram (a3d4a5a) | Miguel Ingram (a3d4a5a) | 16 |

**Recent test directory history** (`git log --oneline -5 -- tests/`):

```
a3d4a5a test(v3): cover adversarial enforcement seams
937c8d6 [S11] P-generalizations: prereg, decision gate, obligations+watchdog, probe registry, exposure caps
7b7a7fe [S10] V3 spine: per-lane stage ordering, config-gated off (the contested layer, by explicit switch)
644f13c [S9] V3 typed bet-spec + action authorization, config-gated off (bet-ledger layer)
e07aefd [S8] human-actuation queue: request-don't-wait, metered, conclusion-blocking (#31) + the atomic PROMPT amendment
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | Placing a due bet into a closed or watching historical lane ... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 1 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), AST symbol-to-test binding (1/1 symbols verified), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Close the historical-lane active-cap bypass

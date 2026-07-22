# AIV Evidence File (v1.0)

**File:** `bin/decision_gate.py`
**Commit:** `633a768`
**Previous:** `4cec843`
**Generated:** 2026-07-22T22:39:52Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R2
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "bin/decision_gate.py"
  classification_rationale: "This changes a config-independent authorization gate with component blast radius, meeting AIV section 5.3 R2"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T22:39:52Z"
```

## Claim(s)

1. Decision records authorize only when parsed class and body fields exactly match the request
2. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/51#discussion_r3634224778](https://github.com/ImmortalDemonGod/money-agent/pull/51#discussion_r3634224778)
- **Requirements Verified:** CodeRabbit requires exact parsed decision fields rather than substring matches

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`633a768`](https://github.com/ImmortalDemonGod/money-agent/tree/633a768710de2f0eb593a04ec802797d5b5cf5b8))

- [`bin/decision_gate.py#L51-L56`](https://github.com/ImmortalDemonGod/money-agent/blob/633a768710de2f0eb593a04ec802797d5b5cf5b8/bin/decision_gate.py#L51-L56)

### Class A (Execution Evidence)

**Per-symbol test coverage (AST analysis):**

- **`_decision`** (L51-L56): PASS -- 1 test(s) call `_decision` directly
  - `tests/test_v3_hardening.py::test_decision_gate_requires_exact_parsed_fields`

**Coverage summary:** 1/1 symbols verified by tests.

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
| 1 | Decision records authorize only when parsed class and body f... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 1 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), AST symbol-to-test binding (1/1 symbols verified), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Reject malformed decision records that hide matching tokens in other fields

# AIV Evidence File (v1.0)

**File:** `bin/decision_gate.py`
**Commit:** `dd060b5`
**Generated:** 2026-07-22T22:08:35Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "bin/decision_gate.py"
  classification_rationale: "Protects audit provenance for third-party data acquisition, a logging and PII-adjacent critical surface"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T22:08:35Z"
```

## Claim(s)

1. Data-acquisition decisions pass only when a safe named path exists in HEAD and its committed bytes match the declared SHA-256
2. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/51](https://github.com/ImmortalDemonGod/money-agent/pull/51)
- **Requirements Verified:** PR 51 requires acquisition provenance to be a committed, content-pinned manifest rather than any matching working-tree file

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`dd060b5`](https://github.com/ImmortalDemonGod/money-agent/tree/dd060b556877395b52be7c01bb61f3beb32271d9))

- [`bin/decision_gate.py#L34`](https://github.com/ImmortalDemonGod/money-agent/blob/dd060b556877395b52be7c01bb61f3beb32271d9/bin/decision_gate.py#L34)
- [`bin/decision_gate.py#L71-L72`](https://github.com/ImmortalDemonGod/money-agent/blob/dd060b556877395b52be7c01bb61f3beb32271d9/bin/decision_gate.py#L71-L72)
- [`bin/decision_gate.py#L83-L93`](https://github.com/ImmortalDemonGod/money-agent/blob/dd060b556877395b52be7c01bb61f3beb32271d9/bin/decision_gate.py#L83-L93)

### Class A (Execution Evidence)

**Per-symbol test coverage (AST analysis):**

- **`check`** (L34): PASS -- 1 test(s) call `check` directly
  - `tests/test_v3_hardening.py::test_provenance_must_name_a_committed_blob`

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

No covering test files found.

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
| 1 | Data-acquisition decisions pass only when a safe named path ... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 1 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), AST symbol-to-test binding (1/1 symbols verified), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Bind provenance decisions to exact committed manifest bytes

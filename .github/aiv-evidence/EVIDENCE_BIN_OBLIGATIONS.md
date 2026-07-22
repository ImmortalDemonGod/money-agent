# AIV Evidence File (v1.0)

**File:** `bin/obligations.py`
**Commit:** `0d9b980`
**Generated:** 2026-07-22T22:07:43Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "bin/obligations.py"
  classification_rationale: "Changes payment obligations and refund-related liability controls, AIV section 5.2 critical surfaces"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T22:07:43Z"
```

## Claim(s)

1. Obligation registration rejects negative, non-finite, malformed-cap, and arbitrary-shell inputs
2. Agent fulfillment records remain claims until a verifier-safe typed oracle passes
3. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/51](https://github.com/ImmortalDemonGod/money-agent/pull/51)
- **Requirements Verified:** PR 51 exposure caps and completion oracles must mechanically bound post-payment liability

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`0d9b980`](https://github.com/ImmortalDemonGod/money-agent/tree/0d9b98085ef3505f9fea3e2eddfbce13a6131250))

- [`bin/obligations.py#L31`](https://github.com/ImmortalDemonGod/money-agent/blob/0d9b98085ef3505f9fea3e2eddfbce13a6131250/bin/obligations.py#L31)
- [`bin/obligations.py#L67-L82`](https://github.com/ImmortalDemonGod/money-agent/blob/0d9b98085ef3505f9fea3e2eddfbce13a6131250/bin/obligations.py#L67-L82)
- [`bin/obligations.py#L105-L114`](https://github.com/ImmortalDemonGod/money-agent/blob/0d9b98085ef3505f9fea3e2eddfbce13a6131250/bin/obligations.py#L105-L114)
- [`bin/obligations.py#L140-L145`](https://github.com/ImmortalDemonGod/money-agent/blob/0d9b98085ef3505f9fea3e2eddfbce13a6131250/bin/obligations.py#L140-L145)

### Class A (Execution Evidence)

**Per-symbol test coverage (AST analysis):**

- **`cmd_register`** (L31): PASS -- 1 test(s) call `cmd_register` directly
  - `tests/test_v3_hardening.py::test_obligation_values_and_fulfillment_are_fail_closed`
- **`cmd_fulfill`** (L67-L82): PASS -- 1 test(s) call `cmd_fulfill` directly
  - `tests/test_v3_hardening.py::test_obligation_values_and_fulfillment_are_fail_closed`

**Coverage summary:** 2/2 symbols verified by tests.

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
| 1 | Obligation registration rejects negative, non-finite, malfor... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | Agent fulfillment records remain claims until a verifier-saf... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 3 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 2 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), AST symbol-to-test binding (2/2 symbols verified), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Make obligation values finite and fulfillment verifier-adjudicated

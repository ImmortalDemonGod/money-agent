# AIV Evidence File (v1.0)

**File:** `bin/obligations.py`
**Commit:** `6e00c83`
**Previous:** `3136eeb`
**Generated:** 2026-07-22T22:40:14Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "bin/obligations.py"
  classification_rationale: "Payment, refund, and customer-liability boundaries are AIV section 5.2 critical surfaces"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T22:40:14Z"
```

## Claim(s)

1. Raising exposure environment variables cannot register post-payment work
2. Every attempted deferred paid offer is durably recorded in REFUSALS.md
3. The agent cannot claim fulfillment of a deliver-later obligation
4. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/51#discussion_r3634224791](https://github.com/ImmortalDemonGod/money-agent/pull/51#discussion_r3634224791)
- **Requirements Verified:** CLAUDE.md and CodeRabbit require complete delivery at payment and refusal of post-payment work

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`6e00c83`](https://github.com/ImmortalDemonGod/money-agent/tree/6e00c83118fb82a16d6185143131ed57369d0f01))

- [`bin/obligations.py#L2-L8`](https://github.com/ImmortalDemonGod/money-agent/blob/6e00c83118fb82a16d6185143131ed57369d0f01/bin/obligations.py#L2-L8)
- [`bin/obligations.py#L53-L65`](https://github.com/ImmortalDemonGod/money-agent/blob/6e00c83118fb82a16d6185143131ed57369d0f01/bin/obligations.py#L53-L65)
- [`bin/obligations.py#L68-L71`](https://github.com/ImmortalDemonGod/money-agent/blob/6e00c83118fb82a16d6185143131ed57369d0f01/bin/obligations.py#L68-L71)
- [`bin/obligations.py#L73-L75`](https://github.com/ImmortalDemonGod/money-agent/blob/6e00c83118fb82a16d6185143131ed57369d0f01/bin/obligations.py#L73-L75)
- [`bin/obligations.py#L79-L81`](https://github.com/ImmortalDemonGod/money-agent/blob/6e00c83118fb82a16d6185143131ed57369d0f01/bin/obligations.py#L79-L81)

### Class A (Execution Evidence)

**Per-symbol test coverage (AST analysis):**

- **`_record_refusal`** (L2-L8): FAIL -- WARNING: No tests import or call `_record_refusal`
- **`cmd_register`** (L53-L65): PASS -- 1 test(s) call `cmd_register` directly
  - `tests/test_v3_hardening.py::test_deferred_obligations_are_refused_and_recorded`
- **`cmd_fulfill`** (L68-L71): PASS -- 1 test(s) call `cmd_fulfill` directly
  - `tests/test_v3_hardening.py::test_deferred_obligations_are_refused_and_recorded`

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

No covering test files found.

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
| 1 | Raising exposure environment variables cannot register post-... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | Every attempted deferred paid offer is durably recorded in R... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 3 | The agent cannot claim fulfillment of a deliver-later obliga... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 4 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 3 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), AST symbol-to-test binding (2/3 symbols verified), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Make deferred obligation registration and fulfillment refusal-only

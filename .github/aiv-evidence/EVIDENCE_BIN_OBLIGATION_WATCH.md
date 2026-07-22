# AIV Evidence File (v1.0)

**File:** `bin/obligation_watch.py`
**Commit:** `3136eeb`
**Generated:** 2026-07-22T22:07:55Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "bin/obligation_watch.py"
  classification_rationale: "Runs with verifier credentials and refund authority across a payment safety boundary, requiring R3"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T22:07:55Z"
```

## Claim(s)

1. Unreadable or unfetched obligation registers publish verified false rather than an empty all-clear
2. Fulfillment uses only the reviewed delivery oracle and refunds use stable per-obligation idempotency keys
3. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/51](https://github.com/ImmortalDemonGod/money-agent/pull/51)
- **Requirements Verified:** PR 51 watchdog must independently detect delivery breaches without executing agent-authored shell or duplicating refunds

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`3136eeb`](https://github.com/ImmortalDemonGod/money-agent/tree/3136eeb499d94bd6cb273447008fbba4b59d85c0))

- [`bin/obligation_watch.py#L36`](https://github.com/ImmortalDemonGod/money-agent/blob/3136eeb499d94bd6cb273447008fbba4b59d85c0/bin/obligation_watch.py#L36)
- [`bin/obligation_watch.py#L41-L42`](https://github.com/ImmortalDemonGod/money-agent/blob/3136eeb499d94bd6cb273447008fbba4b59d85c0/bin/obligation_watch.py#L41-L42)
- [`bin/obligation_watch.py#L50-L77`](https://github.com/ImmortalDemonGod/money-agent/blob/3136eeb499d94bd6cb273447008fbba4b59d85c0/bin/obligation_watch.py#L50-L77)
- [`bin/obligation_watch.py#L81-L101`](https://github.com/ImmortalDemonGod/money-agent/blob/3136eeb499d94bd6cb273447008fbba4b59d85c0/bin/obligation_watch.py#L81-L101)
- [`bin/obligation_watch.py#L103-L104`](https://github.com/ImmortalDemonGod/money-agent/blob/3136eeb499d94bd6cb273447008fbba4b59d85c0/bin/obligation_watch.py#L103-L104)
- [`bin/obligation_watch.py#L107-L109`](https://github.com/ImmortalDemonGod/money-agent/blob/3136eeb499d94bd6cb273447008fbba4b59d85c0/bin/obligation_watch.py#L107-L109)
- [`bin/obligation_watch.py#L111-L117`](https://github.com/ImmortalDemonGod/money-agent/blob/3136eeb499d94bd6cb273447008fbba4b59d85c0/bin/obligation_watch.py#L111-L117)
- [`bin/obligation_watch.py#L126`](https://github.com/ImmortalDemonGod/money-agent/blob/3136eeb499d94bd6cb273447008fbba4b59d85c0/bin/obligation_watch.py#L126)
- [`bin/obligation_watch.py#L132-L134`](https://github.com/ImmortalDemonGod/money-agent/blob/3136eeb499d94bd6cb273447008fbba4b59d85c0/bin/obligation_watch.py#L132-L134)

### Class A (Execution Evidence)

**Per-symbol test coverage (AST analysis):**

- **`_refund`** (L36): PASS -- 1 test(s) call `_refund` directly
  - `tests/test_v3_hardening.py::test_obligation_watch_rejects_shell_and_idempotently_refunds`
- **`_completion_oracle`** (L41-L42): PASS -- 1 test(s) call `_completion_oracle` directly
  - `tests/test_v3_hardening.py::test_obligation_watch_rejects_shell_and_idempotently_refunds`
- **`_publish_unverified`** (L50-L77): FAIL -- WARNING: No tests import or call `_publish_unverified`
- **`main`** (L81-L101): FAIL -- WARNING: No tests import or call `main`

**Coverage summary:** 2/4 symbols verified by tests.

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
| 1 | Unreadable or unfetched obligation registers publish verifie... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | Fulfillment uses only the reviewed delivery oracle and refun... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 3 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 2 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), AST symbol-to-test binding (2/4 symbols verified), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Make the obligation watchdog fresh, typed, and idempotent

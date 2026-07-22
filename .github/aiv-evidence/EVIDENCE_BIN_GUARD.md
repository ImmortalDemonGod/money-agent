# AIV Evidence File (v1.0)

**File:** `bin/guard.py`
**Commit:** `09685db`
**Generated:** 2026-07-22T22:08:09Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "bin/guard.py"
  classification_rationale: "Controls run termination at a payment-obligation safety boundary, an AIV section 5.2 critical surface"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T22:08:09Z"
```

## Claim(s)

1. Guard halts when obligation facts are ungrounded, unverified, malformed, stale, or breached
2. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/51](https://github.com/ImmortalDemonGod/money-agent/pull/51)
- **Requirements Verified:** PR 51 promise-book safety must not inherit freshness from an unrelated money heartbeat

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`09685db`](https://github.com/ImmortalDemonGod/money-agent/tree/09685dba4fe49736f7c477d65df42057500c69f2))

- [`bin/guard.py#L309-L329`](https://github.com/ImmortalDemonGod/money-agent/blob/09685dba4fe49736f7c477d65df42057500c69f2/bin/guard.py#L309-L329)

### Class A (Execution Evidence)

**Per-symbol test coverage (AST analysis):**

- **`main`** (L309-L329): FAIL -- WARNING: No tests import or call `main`

**Coverage summary:** 0/1 symbols verified by tests.

### Code Quality (Linting & Types)

- **ruff:** All checks passed
- **mypy:** Found 12 errors in 4 files (checked 1 source file)

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
| 1 | Guard halts when obligation facts are ungrounded, unverified... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 1 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), AST symbol-to-test binding (0/1 symbols verified), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Require independently fresh and verified obligation facts before continuing

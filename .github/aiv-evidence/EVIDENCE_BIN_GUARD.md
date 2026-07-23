# AIV Evidence File (v1.0)

**File:** `bin/guard.py`
**Commit:** `ef4f310`
**Previous:** `9953693`
**Generated:** 2026-07-23T02:30:35Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R2
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "bin/guard.py"
  classification_rationale: "OR/concatenation let one benign value mask a live one"
  classified_by: "Claude"
  classified_at: "2026-07-23T02:30:35Z"
```

## Claim(s)

1. Under SHADOW=1 the guard halts when any single live-shaped credential is configured, even if another configured credential is a benign placeholder or test key
2. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/52](https://github.com/ImmortalDemonGod/money-agent/pull/52)
- **Requirements Verified:** CodeRabbit review of PR #52 requires each shadow credential be validated independently so a placeholder or test key cannot mask a live one

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`ef4f310`](https://github.com/ImmortalDemonGod/money-agent/tree/ef4f3109dc81acd20b07c9bfaa76151cf6ce0d70))

- [`bin/guard.py#L68-L84`](https://github.com/ImmortalDemonGod/money-agent/blob/ef4f3109dc81acd20b07c9bfaa76151cf6ce0d70/bin/guard.py#L68-L84)

### Class A (Execution Evidence)

**Per-symbol test coverage (AST analysis):**

- **`_shadow_mismatch`** (L68-L84): FAIL -- WARNING: No tests import or call `_shadow_mismatch`

**Coverage summary:** 0/1 symbols verified by tests.

### Code Quality (Linting & Types)

- **ruff:** 0 error(s)
- **mypy:** 

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
ef4f310 [S12] Tier-1 shadow-run mode: SHADOW=1 walls, capture, scripted world, policy scorecard
6da1998 test(watchdog): assert breached records are not counted as open
dfde8e4 test(watchdog): late-reachable delivery and unknown status breach and refund
b28993c test(gate): note the P3 publish-decision requirement (e2e fixture deferred)
9c7574d Merge main into run2-e-v3-gated (rebase after #50 merged)
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | Under SHADOW=1 the guard halts when any single live-shaped c... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 1 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), AST symbol-to-test binding (0/1 symbols verified), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Check STRIPE_WRITE_KEY, STRIPE_READ_KEY, PRIVACY_READ_KEY and CARD_NUM independently. Stripe keys are allowlisted to test-key prefixes (sk_test_/rk_test_); card credentials are prohibited entirely (any configured non-placeholder PRIVACY_READ_KEY or CARD_NUM is rejected). Independent checks so one benign value cannot mask a live one.

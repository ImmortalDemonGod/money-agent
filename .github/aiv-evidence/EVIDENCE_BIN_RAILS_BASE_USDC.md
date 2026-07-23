# AIV Evidence File (v1.0)

**File:** `bin/rails/base_usdc.py`
**Commit:** `3d103b4`
**Previous:** `c4cc1c3`
**Generated:** 2026-07-22T23:33:22Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "bin/rails/base_usdc.py"
  classification_rationale: "A prose-only runbook warning did not enforce the payment-rail go/no-go boundary"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T23:33:22Z"
```

## Claim(s)

1. Base scoring and baseline freezing require a verifier-private seven-check marker bound to chain, wallet, marketplace, and settlement event configuration
2. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/50#discussion_r3634578703](https://github.com/ImmortalDemonGod/money-agent/pull/50#discussion_r3634578703)
- **Requirements Verified:** CodeRabbit requires simulation-only Base configuration to remain unscoreable until live acceptance is persisted

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`3d103b4`](https://github.com/ImmortalDemonGod/money-agent/tree/3d103b46310dc330ca9a785a09668ce8eff9dd9b))

- [`bin/rails/base_usdc.py#L46-L79`](https://github.com/ImmortalDemonGod/money-agent/blob/3d103b46310dc330ca9a785a09668ce8eff9dd9b/bin/rails/base_usdc.py#L46-L79)
- [`bin/rails/base_usdc.py#L138`](https://github.com/ImmortalDemonGod/money-agent/blob/3d103b46310dc330ca9a785a09668ce8eff9dd9b/bin/rails/base_usdc.py#L138)
- [`bin/rails/base_usdc.py#L175-L179`](https://github.com/ImmortalDemonGod/money-agent/blob/3d103b46310dc330ca9a785a09668ce8eff9dd9b/bin/rails/base_usdc.py#L175-L179)

### Class A (Execution Evidence)

**Per-symbol test coverage (AST analysis):**

- **`validate_live_acceptance`** (L46-L79): FAIL -- WARNING: No tests import or call `validate_live_acceptance`
- **`freeze_baseline`** (L138): FAIL -- WARNING: No tests import or call `freeze_baseline`
- **`pull`** (L175-L179): FAIL -- WARNING: No tests import or call `pull`

**Coverage summary:** 0/3 symbols verified by tests.

### Code Quality (Linting & Types)

- **ruff:** All checks passed
- **mypy:** Found 12 errors in 1 file (checked 1 source file)

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
dfe3ff8 test(pr50): pin final review failure modes
d52a400 test(rails): expand fail-closed registry catalog
710e1c0 merge(stack): sync rewritten stack 3 ancestry
618e3eb merge(stack): integrate reviewed stack 3 advances
4ff597e test(delivery): cover content-type refusal
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | Base scoring and baseline freezing require a verifier-privat... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 1 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), AST symbol-to-test binding (0/3 symbols verified), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Enforce live acceptance inside the Base adapter

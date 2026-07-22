# AIV Evidence File (v1.0)

**File:** `bin/edge_pnl.py`
**Commit:** `e53b606`
**Generated:** 2026-07-22T21:55:37Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "bin/edge_pnl.py"
  classification_rationale: "R3 because this changes verifier adjudication for an edge verdict"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T21:55:37Z"
```

## Claim(s)

1. Edge registrations reject non-finite risk inputs and compute drawdown from peak equity scoped to their frozen registration
2. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/issues/38](https://github.com/ImmortalDemonGod/money-agent/issues/38)
- **Requirements Verified:** Issue #38 requires a frozen mechanically enforced drawdown constraint

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`e53b606`](https://github.com/ImmortalDemonGod/money-agent/tree/e53b6062ef1ac8fed0c86f60feff641e51495b25))

- [`bin/edge_pnl.py#L55`](https://github.com/ImmortalDemonGod/money-agent/blob/e53b6062ef1ac8fed0c86f60feff641e51495b25/bin/edge_pnl.py#L55)
- [`bin/edge_pnl.py#L124-L126`](https://github.com/ImmortalDemonGod/money-agent/blob/e53b6062ef1ac8fed0c86f60feff641e51495b25/bin/edge_pnl.py#L124-L126)
- [`bin/edge_pnl.py#L130-L135`](https://github.com/ImmortalDemonGod/money-agent/blob/e53b6062ef1ac8fed0c86f60feff641e51495b25/bin/edge_pnl.py#L130-L135)
- [`bin/edge_pnl.py#L266`](https://github.com/ImmortalDemonGod/money-agent/blob/e53b6062ef1ac8fed0c86f60feff641e51495b25/bin/edge_pnl.py#L266)
- [`bin/edge_pnl.py#L268-L270`](https://github.com/ImmortalDemonGod/money-agent/blob/e53b6062ef1ac8fed0c86f60feff641e51495b25/bin/edge_pnl.py#L268-L270)
- [`bin/edge_pnl.py#L272`](https://github.com/ImmortalDemonGod/money-agent/blob/e53b6062ef1ac8fed0c86f60feff641e51495b25/bin/edge_pnl.py#L272)
- [`bin/edge_pnl.py#L275-L279`](https://github.com/ImmortalDemonGod/money-agent/blob/e53b6062ef1ac8fed0c86f60feff641e51495b25/bin/edge_pnl.py#L275-L279)

### Class A (Execution Evidence)

**Per-symbol test coverage (AST analysis):**

- **`parse_registration`** (L55): FAIL -- WARNING: No tests import or call `parse_registration`
- **`main`** (L124-L126): FAIL -- WARNING: No tests import or call `main`

**Coverage summary:** 0/2 symbols verified by tests.

### Code Quality (Linting & Types)

- **ruff:** All checks passed
- **mypy:** Found 13 errors in 1 file (checked 1 source file)

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
e53b606 test(delivery): reject unrelated Stripe success URLs
aa1dc15 [S6] edge-verdict quality: frozen risk cap + peak tracking + signed edge facts (#38, closes the S4 edge-signing deferral)
fe0427a [S5] gates & probes: delivery seam + provider cap, oracle-classed resolutions, mechanical pacing (#39 #35 #40 #45)
655bb5b test(verifier): cover initial truth signing failure
4c0df17 test(verifier): reject unsigned attestation output
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | Edge registrations reject non-finite risk inputs and compute... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 1 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), AST symbol-to-test binding (0/2 symbols verified), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Prevent disabled drawdown caps and cross-registration peak contamination

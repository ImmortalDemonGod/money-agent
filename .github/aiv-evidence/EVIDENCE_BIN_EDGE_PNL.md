# AIV Evidence File (v1.0)

**File:** `bin/edge_pnl.py`
**Commit:** `46f3125`
**Previous:** `994cd6f`
**Generated:** 2026-07-22T22:45:13Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "bin/edge_pnl.py"
  classification_rationale: "R3 because this changes verifier-owned risk and verdict calculations"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T22:45:13Z"
```

## Claim(s)

1. Edge verification requires a frozen benchmark and grants VERIFIED_POSITIVE_EV only when excess return clears the registered bar, fill floor, and drawdown cap
2. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/issues/38](https://github.com/ImmortalDemonGod/money-agent/issues/38)
- **Requirements Verified:** Issue #38 requires benchmark-relative mechanical edge verification

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`46f3125`](https://github.com/ImmortalDemonGod/money-agent/tree/46f31253e62820aa778c9d151ce36768cfe05f53))

- [`bin/edge_pnl.py#L59`](https://github.com/ImmortalDemonGod/money-agent/blob/46f31253e62820aa778c9d151ce36768cfe05f53/bin/edge_pnl.py#L59)
- [`bin/edge_pnl.py#L72`](https://github.com/ImmortalDemonGod/money-agent/blob/46f31253e62820aa778c9d151ce36768cfe05f53/bin/edge_pnl.py#L72)
- [`bin/edge_pnl.py#L77-L78`](https://github.com/ImmortalDemonGod/money-agent/blob/46f31253e62820aa778c9d151ce36768cfe05f53/bin/edge_pnl.py#L77-L78)
- [`bin/edge_pnl.py#L80-L82`](https://github.com/ImmortalDemonGod/money-agent/blob/46f31253e62820aa778c9d151ce36768cfe05f53/bin/edge_pnl.py#L80-L82)
- [`bin/edge_pnl.py#L112-L125`](https://github.com/ImmortalDemonGod/money-agent/blob/46f31253e62820aa778c9d151ce36768cfe05f53/bin/edge_pnl.py#L112-L125)
- [`bin/edge_pnl.py#L151-L152`](https://github.com/ImmortalDemonGod/money-agent/blob/46f31253e62820aa778c9d151ce36768cfe05f53/bin/edge_pnl.py#L151-L152)
- [`bin/edge_pnl.py#L222-L225`](https://github.com/ImmortalDemonGod/money-agent/blob/46f31253e62820aa778c9d151ce36768cfe05f53/bin/edge_pnl.py#L222-L225)
- [`bin/edge_pnl.py#L233`](https://github.com/ImmortalDemonGod/money-agent/blob/46f31253e62820aa778c9d151ce36768cfe05f53/bin/edge_pnl.py#L233)
- [`bin/edge_pnl.py#L236`](https://github.com/ImmortalDemonGod/money-agent/blob/46f31253e62820aa778c9d151ce36768cfe05f53/bin/edge_pnl.py#L236)
- [`bin/edge_pnl.py#L239`](https://github.com/ImmortalDemonGod/money-agent/blob/46f31253e62820aa778c9d151ce36768cfe05f53/bin/edge_pnl.py#L239)
- [`bin/edge_pnl.py#L275-L276`](https://github.com/ImmortalDemonGod/money-agent/blob/46f31253e62820aa778c9d151ce36768cfe05f53/bin/edge_pnl.py#L275-L276)
- [`bin/edge_pnl.py#L285-L287`](https://github.com/ImmortalDemonGod/money-agent/blob/46f31253e62820aa778c9d151ce36768cfe05f53/bin/edge_pnl.py#L285-L287)
- [`bin/edge_pnl.py#L310-L314`](https://github.com/ImmortalDemonGod/money-agent/blob/46f31253e62820aa778c9d151ce36768cfe05f53/bin/edge_pnl.py#L310-L314)
- [`bin/edge_pnl.py#L338`](https://github.com/ImmortalDemonGod/money-agent/blob/46f31253e62820aa778c9d151ce36768cfe05f53/bin/edge_pnl.py#L338)
- [`bin/edge_pnl.py#L346-L347`](https://github.com/ImmortalDemonGod/money-agent/blob/46f31253e62820aa778c9d151ce36768cfe05f53/bin/edge_pnl.py#L346-L347)

### Class A (Execution Evidence)

**Per-symbol test coverage (AST analysis):**

- **`_benchmark_price`** (L59): FAIL -- WARNING: No tests import or call `_benchmark_price`
- **`parse_registration`** (L72): FAIL -- WARNING: No tests import or call `parse_registration`
- **`main`** (L77-L78): FAIL -- WARNING: No tests import or call `main`

**Coverage summary:** 0/3 symbols verified by tests.

### Code Quality (Linting & Types)

- **ruff:** All checks passed
- **mypy:** Found 16 errors in 1 file (checked 1 source file)

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
88a6899 test(edge): cover finite caps and scoped peaks
e53b606 test(delivery): reject unrelated Stripe success URLs
aa1dc15 [S6] edge-verdict quality: frozen risk cap + peak tracking + signed edge facts (#38, closes the S4 edge-signing deferral)
fe0427a [S5] gates & probes: delivery seam + provider cap, oracle-classed resolutions, mechanical pacing (#39 #35 #40 #45)
655bb5b test(verifier): cover initial truth signing failure
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | Edge verification requires a frozen benchmark and grants VER... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 1 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), AST symbol-to-test binding (0/3 symbols verified), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Replace raw PnL verdicts with frozen benchmark-relative excess return

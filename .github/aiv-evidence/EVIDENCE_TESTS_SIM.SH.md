# AIV Evidence File (v1.0)

**File:** `tests/sim.sh`
**Commit:** `5e5450f`
**Previous:** `88a6899`
**Generated:** 2026-07-22T22:45:41Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "tests/sim.sh"
  classification_rationale: "R3 verifier verdict regression coverage"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T22:45:41Z"
```

## Claim(s)

1. The simulation freezes a benchmark price and verifies edge verdicts use excess return with drawdown and fill constraints
2. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/issues/38](https://github.com/ImmortalDemonGod/money-agent/issues/38)
- **Requirements Verified:** Issue #38 requires a benchmark-relative verifier test

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`5e5450f`](https://github.com/ImmortalDemonGod/money-agent/tree/5e5450f0ff14f431327dce2f5a42de6bae46e396))

- [`tests/sim.sh#L206`](https://github.com/ImmortalDemonGod/money-agent/blob/5e5450f0ff14f431327dce2f5a42de6bae46e396/tests/sim.sh#L206)
- [`tests/sim.sh#L210`](https://github.com/ImmortalDemonGod/money-agent/blob/5e5450f0ff14f431327dce2f5a42de6bae46e396/tests/sim.sh#L210)
- [`tests/sim.sh#L213-L214`](https://github.com/ImmortalDemonGod/money-agent/blob/5e5450f0ff14f431327dce2f5a42de6bae46e396/tests/sim.sh#L213-L214)
- [`tests/sim.sh#L218`](https://github.com/ImmortalDemonGod/money-agent/blob/5e5450f0ff14f431327dce2f5a42de6bae46e396/tests/sim.sh#L218)
- [`tests/sim.sh#L856-L857`](https://github.com/ImmortalDemonGod/money-agent/blob/5e5450f0ff14f431327dce2f5a42de6bae46e396/tests/sim.sh#L856-L857)
- [`tests/sim.sh#L859`](https://github.com/ImmortalDemonGod/money-agent/blob/5e5450f0ff14f431327dce2f5a42de6bae46e396/tests/sim.sh#L859)

### Class A (Execution Evidence)

**WARNING:** No tests found that directly import or reference the changed file.
This file has no claim-specific execution evidence.

### Code Quality (Linting & Types)

- **ruff:** 14226 error(s)
- **mypy:** Found 1 error in 1 file (errors prevented further checking)

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
| 1 | The simulation freezes a benchmark price and verifies edge v... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 1 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), pytest (no claim-specific tests found), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Exercise frozen benchmark and excess-return adjudication

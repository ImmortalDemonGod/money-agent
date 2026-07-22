# AIV Evidence File (v1.0)

**File:** `bin/aiv_gate.sh`
**Commit:** `76b1f2f`
**Generated:** 2026-07-22T22:37:35Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "bin/aiv_gate.sh"
  classification_rationale: "R3 payment claim gate"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T22:37:35Z"
```

## Claim(s)

1. A paid-offer packet with multiple distinct Stripe URLs fails instead of leaving links unverified
2. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/issues/35](https://github.com/ImmortalDemonGod/money-agent/issues/35)
- **Requirements Verified:** Issue #35 requires provider-capped payment surfaces

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`76b1f2f`](https://github.com/ImmortalDemonGod/money-agent/tree/76b1f2f7bb303d4f10494f8c5c5cc6324f1108ba))

- [`bin/aiv_gate.sh#L196-L200`](https://github.com/ImmortalDemonGod/money-agent/blob/76b1f2f7bb303d4f10494f8c5c5cc6324f1108ba/bin/aiv_gate.sh#L196-L200)

### Class A (Execution Evidence)

**WARNING:** No tests found that directly import or reference the changed file.
This file has no claim-specific execution evidence.

### Code Quality (Linting & Types)

- **ruff:** 5215 error(s)
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
| 1 | A paid-offer packet with multiple distinct Stripe URLs fails... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 1 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), pytest (no claim-specific tests found), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Require one verified payment link per packet

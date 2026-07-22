# AIV Evidence File (v1.0)

**File:** `templates/EDGE_REGISTRATION.template.md`
**Commit:** `aa80a5d`
**Generated:** 2026-07-22T22:47:06Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R2
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "templates/EDGE_REGISTRATION.template.md"
  classification_rationale: "R2 because this changes the public verifier registration contract"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T22:47:06Z"
```

## Claim(s)

1. The edge registration template requires a benchmark ticker and defines BAR as an excess-return threshold
2. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/issues/38](https://github.com/ImmortalDemonGod/money-agent/issues/38)
- **Requirements Verified:** Issue #38 requires a declared benchmark and excess-return evaluation

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`aa80a5d`](https://github.com/ImmortalDemonGod/money-agent/tree/aa80a5d73296f3fd7e41deb2f63b858eb465b514))

- [`templates/EDGE_REGISTRATION.template.md#L22-L23`](https://github.com/ImmortalDemonGod/money-agent/blob/aa80a5d73296f3fd7e41deb2f63b858eb465b514/templates/EDGE_REGISTRATION.template.md#L22-L23)
- [`templates/EDGE_REGISTRATION.template.md#L31-L32`](https://github.com/ImmortalDemonGod/money-agent/blob/aa80a5d73296f3fd7e41deb2f63b858eb465b514/templates/EDGE_REGISTRATION.template.md#L31-L32)

### Class A (Execution Evidence)

**WARNING:** No tests found that directly import or reference the changed file.
This file has no claim-specific execution evidence.

### Code Quality (Linting & Types)

- **ruff:** All checks passed
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
aa80a5d test(edge): cover benchmark-relative verdicts
88a6899 test(edge): cover finite caps and scoped peaks
e53b606 test(delivery): reject unrelated Stripe success URLs
aa1dc15 [S6] edge-verdict quality: frozen risk cap + peak tracking + signed edge facts (#38, closes the S4 edge-signing deferral)
fe0427a [S5] gates & probes: delivery seam + provider cap, oracle-classed resolutions, mechanical pacing (#39 #35 #40 #45)
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | The edge registration template requires a benchmark ticker a... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 1 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), pytest (no claim-specific tests found), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Document the benchmark-relative edge registration contract

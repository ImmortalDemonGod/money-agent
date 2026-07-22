# AIV Evidence File (v1.0)

**File:** `tests/sim.sh`
**Commit:** `8aaa5e5`
**Previous:** `aa80a5d`
**Generated:** 2026-07-22T23:03:21Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "tests/sim.sh"
  classification_rationale: "bash tests/sim.sh"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T23:03:21Z"
```

## Claim(s)

1. The delivery simulation proves a complete artifact with an unsupported content type is refused.
2. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/issues/39](https://github.com/ImmortalDemonGod/money-agent/issues/39)
- **Requirements Verified:** A paid-offer delivery check must fail closed for an absent or non-deliverable content type.

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`8aaa5e5`](https://github.com/ImmortalDemonGod/money-agent/tree/8aaa5e561a50e18c842fdbc6e17a0f86e386a1d2))

- [`tests/sim.sh#L582`](https://github.com/ImmortalDemonGod/money-agent/blob/8aaa5e561a50e18c842fdbc6e17a0f86e386a1d2/tests/sim.sh#L582)
- [`tests/sim.sh#L585`](https://github.com/ImmortalDemonGod/money-agent/blob/8aaa5e561a50e18c842fdbc6e17a0f86e386a1d2/tests/sim.sh#L585)
- [`tests/sim.sh#L587-L589`](https://github.com/ImmortalDemonGod/money-agent/blob/8aaa5e561a50e18c842fdbc6e17a0f86e386a1d2/tests/sim.sh#L587-L589)

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
aa80a5d test(edge): cover benchmark-relative verdicts
88a6899 test(edge): cover finite caps and scoped peaks
e53b606 test(delivery): reject unrelated Stripe success URLs
aa1dc15 [S6] edge-verdict quality: frozen risk cap + peak tracking + signed edge facts (#38, closes the S4 edge-signing deferral)
fe0427a [S5] gates & probes: delivery seam + provider cap, oracle-classed resolutions, mechanical pacing (#39 #35 #40 #45)
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | The delivery simulation proves a complete artifact with an u... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 1 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), pytest (no claim-specific tests found), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

The regression test is hermetic: it monkeypatches the SSRF-protected fetch seam and exercises only verifier policy.

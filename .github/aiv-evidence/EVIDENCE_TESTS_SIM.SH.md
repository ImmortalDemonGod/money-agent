# AIV Evidence File (v1.0)

**File:** `tests/sim.sh`
**Commit:** `8e1e2ed`
**Previous:** `1c0d6f2`
**Generated:** 2026-07-22T22:40:41Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "tests/sim.sh"
  classification_rationale: "The matrix exercises payment, PII, verifier, and audit critical surfaces and therefore inherits R3"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T22:40:41Z"
```

## Claim(s)

1. The two-clone simulation rejects substring authorization and all deferred obligation registration
2. Typed resolution fixtures emit observable metric values for declared-condition evaluation
3. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/51#pullrequestreview-4759249208](https://github.com/ImmortalDemonGod/money-agent/pull/51#pullrequestreview-4759249208)
- **Requirements Verified:** CodeRabbit fixes require end-to-end regression coverage in the existing simulation matrix

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`8e1e2ed`](https://github.com/ImmortalDemonGod/money-agent/tree/8e1e2eddf5c95ad61db3989c5c06726c6a3000f0))

- [`tests/sim.sh#L259`](https://github.com/ImmortalDemonGod/money-agent/blob/8e1e2eddf5c95ad61db3989c5c06726c6a3000f0/tests/sim.sh#L259)
- [`tests/sim.sh#L283`](https://github.com/ImmortalDemonGod/money-agent/blob/8e1e2eddf5c95ad61db3989c5c06726c6a3000f0/tests/sim.sh#L283)
- [`tests/sim.sh#L292`](https://github.com/ImmortalDemonGod/money-agent/blob/8e1e2eddf5c95ad61db3989c5c06726c6a3000f0/tests/sim.sh#L292)
- [`tests/sim.sh#L369-L372`](https://github.com/ImmortalDemonGod/money-agent/blob/8e1e2eddf5c95ad61db3989c5c06726c6a3000f0/tests/sim.sh#L369-L372)
- [`tests/sim.sh#L388-L395`](https://github.com/ImmortalDemonGod/money-agent/blob/8e1e2eddf5c95ad61db3989c5c06726c6a3000f0/tests/sim.sh#L388-L395)

### Class A (Execution Evidence)

**WARNING:** No tests found that directly import or reference the changed file.
This file has no claim-specific execution evidence.

### Code Quality (Linting & Types)

- **ruff:** 22194 error(s)
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
8e1e2ed test(v3): cover CodeRabbit hardening findings
1c0d6f2 test(sim): adversarially cover PR 51 hardening
a3d4a5a test(v3): cover adversarial enforcement seams
937c8d6 [S11] P-generalizations: prereg, decision gate, obligations+watchdog, probe registry, exposure caps
7b7a7fe [S10] V3 spine: per-lane stage ordering, config-gated off (the contested layer, by explicit switch)
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | The two-clone simulation rejects substring authorization and... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | Typed resolution fixtures emit observable metric values for ... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 3 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 2 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), pytest (no claim-specific tests found), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Extend the integration matrix for exact decisions, typed outcomes, and refusal-only obligations

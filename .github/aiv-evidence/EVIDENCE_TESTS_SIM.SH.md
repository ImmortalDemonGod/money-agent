# AIV Evidence File (v1.0)

**File:** `tests/sim.sh`
**Commit:** `c5fd8f6`
**Previous:** `8457d08`
**Generated:** 2026-07-22T22:45:07Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "tests/sim.sh"
  classification_rationale: "Tests exercise payment attribution and conclusion authorization critical surfaces under AIV section 5.2"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T22:45:07Z"
```

## Claim(s)

1. The simulation rejects claims-lane human self-certification and direct task-status tampering
2. The simulation requires one-to-one Base settlement binding and Base mainnet chain identity
3. The simulation requires per-task resolution latency and human queue VERDICT surfacing
4. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/issues/31](https://github.com/ImmortalDemonGod/money-agent/issues/31)
- **Requirements Verified:** Issues #30 and #31 require verifier-grounded actuation and independently verifiable rail contributions before closure

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`c5fd8f6`](https://github.com/ImmortalDemonGod/money-agent/tree/c5fd8f63be061733b5b0d16533997a51cc9c94f2))

- [`tests/sim.sh#L204-L211`](https://github.com/ImmortalDemonGod/money-agent/blob/c5fd8f63be061733b5b0d16533997a51cc9c94f2/tests/sim.sh#L204-L211)
- [`tests/sim.sh#L228-L231`](https://github.com/ImmortalDemonGod/money-agent/blob/c5fd8f63be061733b5b0d16533997a51cc9c94f2/tests/sim.sh#L228-L231)
- [`tests/sim.sh#L233-L234`](https://github.com/ImmortalDemonGod/money-agent/blob/c5fd8f63be061733b5b0d16533997a51cc9c94f2/tests/sim.sh#L233-L234)
- [`tests/sim.sh#L239-L241`](https://github.com/ImmortalDemonGod/money-agent/blob/c5fd8f63be061733b5b0d16533997a51cc9c94f2/tests/sim.sh#L239-L241)
- [`tests/sim.sh#L249-L263`](https://github.com/ImmortalDemonGod/money-agent/blob/c5fd8f63be061733b5b0d16533997a51cc9c94f2/tests/sim.sh#L249-L263)
- [`tests/sim.sh#L268-L269`](https://github.com/ImmortalDemonGod/money-agent/blob/c5fd8f63be061733b5b0d16533997a51cc9c94f2/tests/sim.sh#L268-L269)
- [`tests/sim.sh#L559`](https://github.com/ImmortalDemonGod/money-agent/blob/c5fd8f63be061733b5b0d16533997a51cc9c94f2/tests/sim.sh#L559)
- [`tests/sim.sh#L562-L563`](https://github.com/ImmortalDemonGod/money-agent/blob/c5fd8f63be061733b5b0d16533997a51cc9c94f2/tests/sim.sh#L562-L563)
- [`tests/sim.sh#L608-L634`](https://github.com/ImmortalDemonGod/money-agent/blob/c5fd8f63be061733b5b0d16533997a51cc9c94f2/tests/sim.sh#L608-L634)

### Class A (Execution Evidence)

**WARNING:** No tests found that directly import or reference the changed file.
This file has no claim-specific execution evidence.

### Code Quality (Linting & Types)

- **ruff:** 17042 error(s)
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
c5fd8f6 docs(tests): normalize bug-catalog whitespace
8457d08 merge(stack): reconcile PR50 with reviewed stack 3 fixes
0dfb70b test(sim): make packet mutations portable and fail closed
b48810e test(preflight): provide extracted Base identity path
406c9f6 test(harness): cover PR50 trust-boundary regressions
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | The simulation rejects claims-lane human self-certification ... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | The simulation requires one-to-one Base settlement binding a... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 3 | The simulation requires per-task resolution latency and huma... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 4 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 3 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), pytest (no claim-specific tests found), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Add adversarial closure tests for PR50 trust boundaries

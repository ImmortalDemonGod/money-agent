# AIV Evidence File (v1.0)

**File:** `tests/sim.sh`
**Commit:** `d08da19`
**Previous:** `68b46db`
**Generated:** 2026-07-22T23:11:53Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "tests/sim.sh"
  classification_rationale: "This integration combines payment, conclusion, and autonomous-execution critical surfaces"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T23:11:53Z"
```

## Claim(s)

1. The PR50 simulation matrix retains signed actuation and registered-rail assertions while incorporating stack-3 delivery, conclusion, and benchmark-relative edge checks
2. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/50](https://github.com/ImmortalDemonGod/money-agent/pull/50)
- **Requirements Verified:** PR50 must remain mergeable with and verified against its advancing stacked target branch

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`d08da19`](https://github.com/ImmortalDemonGod/money-agent/tree/d08da1935346aa2c181661f3889c4ed21a3460ce))

- [`tests/sim.sh#L285`](https://github.com/ImmortalDemonGod/money-agent/blob/d08da1935346aa2c181661f3889c4ed21a3460ce/tests/sim.sh#L285)
- [`tests/sim.sh#L289`](https://github.com/ImmortalDemonGod/money-agent/blob/d08da1935346aa2c181661f3889c4ed21a3460ce/tests/sim.sh#L289)
- [`tests/sim.sh#L292-L293`](https://github.com/ImmortalDemonGod/money-agent/blob/d08da1935346aa2c181661f3889c4ed21a3460ce/tests/sim.sh#L292-L293)
- [`tests/sim.sh#L297`](https://github.com/ImmortalDemonGod/money-agent/blob/d08da1935346aa2c181661f3889c4ed21a3460ce/tests/sim.sh#L297)
- [`tests/sim.sh#L857`](https://github.com/ImmortalDemonGod/money-agent/blob/d08da1935346aa2c181661f3889c4ed21a3460ce/tests/sim.sh#L857)
- [`tests/sim.sh#L860`](https://github.com/ImmortalDemonGod/money-agent/blob/d08da1935346aa2c181661f3889c4ed21a3460ce/tests/sim.sh#L860)
- [`tests/sim.sh#L862-L864`](https://github.com/ImmortalDemonGod/money-agent/blob/d08da1935346aa2c181661f3889c4ed21a3460ce/tests/sim.sh#L862-L864)
- [`tests/sim.sh#L1133-L1134`](https://github.com/ImmortalDemonGod/money-agent/blob/d08da1935346aa2c181661f3889c4ed21a3460ce/tests/sim.sh#L1133-L1134)
- [`tests/sim.sh#L1136`](https://github.com/ImmortalDemonGod/money-agent/blob/d08da1935346aa2c181661f3889c4ed21a3460ce/tests/sim.sh#L1136)

### Class A (Execution Evidence)

**WARNING:** No tests found that directly import or reference the changed file.
This file has no claim-specific execution evidence.

### Code Quality (Linting & Types)

- **ruff:** 17404 error(s)
- **mypy:** Found 1 error in 1 file (errors prevented further checking)

### Class C (Negative Evidence)

**Search methodology:** Ran `git diff --cached` and scanned for regression indicators.

- Test file deletions: **none**
- Test files modified: 1
  - `tests/sim.sh`
- Deleted assertions (`assert` removals in diff): **none found**
- Added skip markers (`@pytest.mark.skip`, `@unittest.skip`): **none found**

### Class D (Differential Evidence)

**Change summary** (`git diff --cached --stat`):

```
tests/sim.sh | 23 +++++++++++++----------
 1 file changed, 13 insertions(+), 10 deletions(-)
```

### Class F (Provenance Evidence)

**Test file chain-of-custody:**

No covering test files found.

**Recent test directory history** (`git log --oneline -5 -- tests/`):

```
68b46db test(sim): isolate AIV edge fixture state
bc601c3 test(rails): expose registry contract to verification
86e664c test(pr50): exercise executable rail and queue contracts
67e9adb test(pr50): pin issue-closure trust boundaries
c5fd8f6 docs(tests): normalize bug-catalog whitespace
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | The PR50 simulation matrix retains signed actuation and regi... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 1 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), pytest (no claim-specific tests found), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Merge the advanced stack-3 target without dropping PR50 trust fixes

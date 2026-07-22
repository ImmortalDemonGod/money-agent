# AIV Evidence File (v1.0)

**File:** `bin/supervise.sh`
**Commit:** `2382040`
**Previous:** `0936838`
**Generated:** 2026-07-22T23:01:48Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "bin/supervise.sh"
  classification_rationale: "Unauthenticated or hidden queue state can mislead operators and permit premature conclusions"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T23:01:48Z"
```

## Claim(s)

1. Supervisor verdicts distinguish human actuation required from agent sync required using signature-verified ledger resolutions
2. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/issues/31](https://github.com/ImmortalDemonGod/money-agent/issues/31)
- **Requirements Verified:** Issue #31 requires the asynchronous actuation queue to be visible without stalling the agent loop

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`2382040`](https://github.com/ImmortalDemonGod/money-agent/tree/23820409015d4a4b7414a65ad5a0a6540ecf7e84))

- [`bin/supervise.sh#L84`](https://github.com/ImmortalDemonGod/money-agent/blob/23820409015d4a4b7414a65ad5a0a6540ecf7e84/bin/supervise.sh#L84)
- [`bin/supervise.sh#L86`](https://github.com/ImmortalDemonGod/money-agent/blob/23820409015d4a4b7414a65ad5a0a6540ecf7e84/bin/supervise.sh#L86)
- [`bin/supervise.sh#L91-L94`](https://github.com/ImmortalDemonGod/money-agent/blob/23820409015d4a4b7414a65ad5a0a6540ecf7e84/bin/supervise.sh#L91-L94)
- [`bin/supervise.sh#L100-L118`](https://github.com/ImmortalDemonGod/money-agent/blob/23820409015d4a4b7414a65ad5a0a6540ecf7e84/bin/supervise.sh#L100-L118)
- [`bin/supervise.sh#L146-L149`](https://github.com/ImmortalDemonGod/money-agent/blob/23820409015d4a4b7414a65ad5a0a6540ecf7e84/bin/supervise.sh#L146-L149)

### Class A (Execution Evidence)

**WARNING:** No tests found that directly import or reference the changed file.
This file has no claim-specific execution evidence.

### Code Quality (Linting & Types)

- **ruff:** 2246 error(s)
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
bc601c3 test(rails): expose registry contract to verification
86e664c test(pr50): exercise executable rail and queue contracts
67e9adb test(pr50): pin issue-closure trust boundaries
c5fd8f6 docs(tests): normalize bug-catalog whitespace
8457d08 merge(stack): reconcile PR50 with reviewed stack 3 fixes
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | Supervisor verdicts distinguish human actuation required fro... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 1 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), pytest (no claim-specific tests found), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Verify ledger signatures and prioritize queue state in VERDICT

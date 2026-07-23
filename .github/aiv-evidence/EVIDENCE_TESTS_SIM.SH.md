# AIV Evidence File (v1.0)

**File:** `tests/sim.sh`
**Commit:** `264ec55`
**Previous:** `3804cba`
**Generated:** 2026-07-23T00:48:29Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R1
  sod_mode: S0
  critical_surfaces: []
  blast_radius: "tests/sim.sh"
  classification_rationale: "The #31 human/supervise tests called ssh-keygen unconditionally while the #36 tests already guard on it; this aligns them. R1: test-only"
  classified_by: "Claude"
  classified_at: "2026-07-23T00:48:29Z"
```

## Claim(s)

1. The human-actuation and supervise signing tests skip cleanly when ssh-keygen is not on PATH, matching the fact-lane signing guard, so the sim matrix does not hard-fail on a machine without openssh-client
2. No existing assertions were removed; the block is wrapped in a skip-guard only
3. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/issues/31](https://github.com/ImmortalDemonGod/money-agent/issues/31)
- **Requirements Verified:** tests/sim.sh must run offline on any machine (README promise); the #31 signing tests must skip like the #36 tests when ssh-keygen is missing, not hard-fail

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`264ec55`](https://github.com/ImmortalDemonGod/money-agent/tree/264ec55218fd07d1ecc20df718b65b95c5381abe))

- [`tests/sim.sh#L204-L206`](https://github.com/ImmortalDemonGod/money-agent/blob/264ec55218fd07d1ecc20df718b65b95c5381abe/tests/sim.sh#L204-L206)
- [`tests/sim.sh#L312`](https://github.com/ImmortalDemonGod/money-agent/blob/264ec55218fd07d1ecc20df718b65b95c5381abe/tests/sim.sh#L312)

### Class A (Execution Evidence)

**WARNING:** No tests found that directly import or reference the changed file.
This file has no claim-specific execution evidence.

### Code Quality (Linting & Types)

- **ruff:** 0 error(s)
- **mypy:** 

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | The human-actuation and supervise signing tests skip cleanly... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing assertions were removed; the block is wrapped in... | structural | Class C not collected | REVIEW MANUAL REVIEW |
| 3 | No existing tests were modified or deleted during this chang... | structural | Class C not collected | REVIEW MANUAL REVIEW |

**Verdict summary:** 0 verified, 0 unverified, 3 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), pytest (no claim-specific tests found).
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Wrap the #31 human/supervise signing block in a command -v ssh-keygen skip-guard

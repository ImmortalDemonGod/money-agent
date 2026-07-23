# AIV Evidence File (v1.0)

**File:** `tests/sim.sh`
**Commit:** `a8f01a7`
**Previous:** `b28993c`
**Generated:** 2026-07-23T02:41:23Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R1
  sod_mode: S0
  critical_surfaces: []
  blast_radius: "tests/sim.sh"
  classification_rationale: "The prior shadow tests stubbed the Stripe pull to empty, so the first-dollar stop was never exercised under SHADOW"
  classified_by: "Claude"
  classified_at: "2026-07-23T02:41:23Z"
```

## Claim(s)

1. A shadow rehearsal that receives a test-mode dollar publishes a verified shadow truth.json and guard halts on the first-dollar stop under SHADOW=1
2. No existing tests were deleted. This change ADDS an end-to-end shadow rehearsal to tests/sim.sh: a test-mode charge flows through pnl under SHADOW=1 to a verified shadow truth.json (received_usd=12.34, shadow:true), then guard's first-dollar stop is asserted to fire (exit 2, "FIRST DOLLAR") under SHADOW=1.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/52](https://github.com/ImmortalDemonGod/money-agent/pull/52)
- **Requirements Verified:** PR #52 claims the rehearsal runs the full lifecycle including the stop; this exercises it end to end rather than testing each wall in isolation

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`a8f01a7`](https://github.com/ImmortalDemonGod/money-agent/tree/a8f01a76656fce7a8b72ba3d249c60368110777b))

- [`tests/sim.sh#L1563-L1601`](https://github.com/ImmortalDemonGod/money-agent/blob/a8f01a76656fce7a8b72ba3d249c60368110777b/tests/sim.sh#L1563-L1601)

### Class A (Execution Evidence)

**WARNING:** No tests found that directly import or reference the changed file.
This file has no claim-specific execution evidence.

### Code Quality (Linting & Types)

- **ruff:** 0 error(s)
- **mypy:** 

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | A shadow rehearsal that receives a test-mode dollar publishe... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted during this chang... | structural | Class C not collected | REVIEW MANUAL REVIEW |

**Verdict summary:** 0 verified, 0 unverified, 2 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), pytest (no claim-specific tests found).
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Flow a real test-mode charge through pnl under SHADOW, then assert guard exits 2 with FIRST DOLLAR

# AIV Evidence File (v1.0)

**File:** `tests/sim.sh`
**Commit:** `3d8806c`
**Previous:** `14a5b33`
**Generated:** 2026-07-23T04:00:58Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R1
  sod_mode: S0
  critical_surfaces: []
  blast_radius: "tests/sim.sh"
  classification_rationale: "Some S16 correctness fixes were independently merged in #51/#52 in a stricter form; the fixtures needed to target those"
  classified_by: "Claude"
  classified_at: "2026-07-23T04:00:58Z"
```

## Claim(s)

1. The S16 sim fixtures assert the same invariants against main's stricter merged implementations (obligations positive-and-finite message, obligation_watch verified:false note, bet_id-scoped F2, committed-manifest C5)
2. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/54](https://github.com/ImmortalDemonGod/money-agent/pull/54)
- **Requirements Verified:** PR #54 rebased onto main where #51/#52 already landed equivalent-or-stricter fixes; the fixtures must match main's messages/APIs, not the pre-rebase code they were written against

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`3d8806c`](https://github.com/ImmortalDemonGod/money-agent/tree/3d8806c2df806b2dca57c7579c906020553c5caa))

- [`tests/sim.sh#L1757`](https://github.com/ImmortalDemonGod/money-agent/blob/3d8806c2df806b2dca57c7579c906020553c5caa/tests/sim.sh#L1757)
- [`tests/sim.sh#L1760`](https://github.com/ImmortalDemonGod/money-agent/blob/3d8806c2df806b2dca57c7579c906020553c5caa/tests/sim.sh#L1760)
- [`tests/sim.sh#L1769-L1771`](https://github.com/ImmortalDemonGod/money-agent/blob/3d8806c2df806b2dca57c7579c906020553c5caa/tests/sim.sh#L1769-L1771)
- [`tests/sim.sh#L1797-L1799`](https://github.com/ImmortalDemonGod/money-agent/blob/3d8806c2df806b2dca57c7579c906020553c5caa/tests/sim.sh#L1797-L1799)
- [`tests/sim.sh#L1802`](https://github.com/ImmortalDemonGod/money-agent/blob/3d8806c2df806b2dca57c7579c906020553c5caa/tests/sim.sh#L1802)
- [`tests/sim.sh#L1804-L1808`](https://github.com/ImmortalDemonGod/money-agent/blob/3d8806c2df806b2dca57c7579c906020553c5caa/tests/sim.sh#L1804-L1808)
- [`tests/sim.sh#L1810-L1816`](https://github.com/ImmortalDemonGod/money-agent/blob/3d8806c2df806b2dca57c7579c906020553c5caa/tests/sim.sh#L1810-L1816)
- [`tests/sim.sh#L1819`](https://github.com/ImmortalDemonGod/money-agent/blob/3d8806c2df806b2dca57c7579c906020553c5caa/tests/sim.sh#L1819)

### Class A (Execution Evidence)

**WARNING:** No tests found that directly import or reference the changed file.
This file has no claim-specific execution evidence.

### Code Quality (Linting & Types)

- **ruff:** 0 error(s)
- **mypy:** 

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | The S16 sim fixtures assert the same invariants against main... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted during this chang... | structural | Class C not collected | REVIEW MANUAL REVIEW |

**Verdict summary:** 0 verified, 0 unverified, 2 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), pytest (no claim-specific tests found).
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Update F8/F7/F2/C5 fixtures to main's messages and the bet_id-scoped bet_gate; keep each invariant

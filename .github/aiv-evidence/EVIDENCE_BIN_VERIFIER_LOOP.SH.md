# AIV Evidence File (v1.0)

**File:** `bin/verifier_loop.sh`
**Commit:** `3bb464e`
**Generated:** 2026-07-22T22:08:22Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "bin/verifier_loop.sh"
  classification_rationale: "Coordinates signed payment facts and a refund-capable watchdog across the verifier trust boundary, requiring R3"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T22:08:22Z"
```

## Claim(s)

1. Verifier cycle signatures include obligation verification, open, fulfilled, and breached state
2. A watchdog process failure suppresses fresh ledger publication rather than refreshing stale promise facts
3. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/51](https://github.com/ImmortalDemonGod/money-agent/pull/51)
- **Requirements Verified:** PR 51 verifier heartbeats must not mask a failed obligation watchdog

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`3bb464e`](https://github.com/ImmortalDemonGod/money-agent/tree/3bb464e83b2258479519ecd2b780407f26f5c874))

- [`bin/verifier_loop.sh#L168`](https://github.com/ImmortalDemonGod/money-agent/blob/3bb464e83b2258479519ecd2b780407f26f5c874/bin/verifier_loop.sh#L168)
- [`bin/verifier_loop.sh#L171-L176`](https://github.com/ImmortalDemonGod/money-agent/blob/3bb464e83b2258479519ecd2b780407f26f5c874/bin/verifier_loop.sh#L171-L176)
- [`bin/verifier_loop.sh#L179`](https://github.com/ImmortalDemonGod/money-agent/blob/3bb464e83b2258479519ecd2b780407f26f5c874/bin/verifier_loop.sh#L179)

### Class A (Execution Evidence)

**WARNING:** No tests found that directly import or reference the changed file.
This file has no claim-specific execution evidence.

### Code Quality (Linting & Types)

- **ruff:** 4888 error(s)
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
a3d4a5a test(v3): cover adversarial enforcement seams
937c8d6 [S11] P-generalizations: prereg, decision gate, obligations+watchdog, probe registry, exposure caps
7b7a7fe [S10] V3 spine: per-lane stage ordering, config-gated off (the contested layer, by explicit switch)
644f13c [S9] V3 typed bet-spec + action authorization, config-gated off (bet-ledger layer)
e07aefd [S8] human-actuation queue: request-don't-wait, metered, conclusion-blocking (#31) + the atomic PROMPT amendment
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | Verifier cycle signatures include obligation verification, o... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | A watchdog process failure suppresses fresh ledger publicati... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 3 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 2 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), pytest (no claim-specific tests found), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Prevent fresh money heartbeats from carrying stale obligation all-clears

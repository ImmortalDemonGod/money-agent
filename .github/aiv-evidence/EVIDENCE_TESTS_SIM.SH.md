# AIV Evidence File (v1.0)

**File:** `tests/sim.sh`
**Commit:** `f162957`
**Generated:** 2026-07-22T22:08:58Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "tests/sim.sh"
  classification_rationale: "End-to-end regression matrix for payment, refund, PII, and audit critical surfaces inherits R3"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T22:08:58Z"
```

## Claim(s)

1. The two-clone simulation rejects ambiguous bet actions, cap bypasses, stale promise facts, self-certified fulfillment, lane reopening, and uncommitted provenance
2. The simulation's text mutation helper runs portably on BSD and GNU hosts
3. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/51](https://github.com/ImmortalDemonGod/money-agent/pull/51)
- **Requirements Verified:** Every confirmed PR 51 defect requires a discriminator regression in the canonical verification matrix

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`f162957`](https://github.com/ImmortalDemonGod/money-agent/tree/f16295700ba0b13c6d0d44a44a61dbf6ec2b93c1))

- [`tests/sim.sh#L52-L61`](https://github.com/ImmortalDemonGod/money-agent/blob/f16295700ba0b13c6d0d44a44a61dbf6ec2b93c1/tests/sim.sh#L52-L61)
- [`tests/sim.sh#L228`](https://github.com/ImmortalDemonGod/money-agent/blob/f16295700ba0b13c6d0d44a44a61dbf6ec2b93c1/tests/sim.sh#L228)
- [`tests/sim.sh#L246`](https://github.com/ImmortalDemonGod/money-agent/blob/f16295700ba0b13c6d0d44a44a61dbf6ec2b93c1/tests/sim.sh#L246)
- [`tests/sim.sh#L248-L266`](https://github.com/ImmortalDemonGod/money-agent/blob/f16295700ba0b13c6d0d44a44a61dbf6ec2b93c1/tests/sim.sh#L248-L266)
- [`tests/sim.sh#L330-L331`](https://github.com/ImmortalDemonGod/money-agent/blob/f16295700ba0b13c6d0d44a44a61dbf6ec2b93c1/tests/sim.sh#L330-L331)
- [`tests/sim.sh#L366`](https://github.com/ImmortalDemonGod/money-agent/blob/f16295700ba0b13c6d0d44a44a61dbf6ec2b93c1/tests/sim.sh#L366)
- [`tests/sim.sh#L376-L381`](https://github.com/ImmortalDemonGod/money-agent/blob/f16295700ba0b13c6d0d44a44a61dbf6ec2b93c1/tests/sim.sh#L376-L381)
- [`tests/sim.sh#L394-L411`](https://github.com/ImmortalDemonGod/money-agent/blob/f16295700ba0b13c6d0d44a44a61dbf6ec2b93c1/tests/sim.sh#L394-L411)
- [`tests/sim.sh#L426-L429`](https://github.com/ImmortalDemonGod/money-agent/blob/f16295700ba0b13c6d0d44a44a61dbf6ec2b93c1/tests/sim.sh#L426-L429)
- [`tests/sim.sh#L437-L448`](https://github.com/ImmortalDemonGod/money-agent/blob/f16295700ba0b13c6d0d44a44a61dbf6ec2b93c1/tests/sim.sh#L437-L448)
- [`tests/sim.sh#L460`](https://github.com/ImmortalDemonGod/money-agent/blob/f16295700ba0b13c6d0d44a44a61dbf6ec2b93c1/tests/sim.sh#L460)
- [`tests/sim.sh#L806`](https://github.com/ImmortalDemonGod/money-agent/blob/f16295700ba0b13c6d0d44a44a61dbf6ec2b93c1/tests/sim.sh#L806)
- [`tests/sim.sh#L809`](https://github.com/ImmortalDemonGod/money-agent/blob/f16295700ba0b13c6d0d44a44a61dbf6ec2b93c1/tests/sim.sh#L809)
- [`tests/sim.sh#L815`](https://github.com/ImmortalDemonGod/money-agent/blob/f16295700ba0b13c6d0d44a44a61dbf6ec2b93c1/tests/sim.sh#L815)
- [`tests/sim.sh#L817-L818`](https://github.com/ImmortalDemonGod/money-agent/blob/f16295700ba0b13c6d0d44a44a61dbf6ec2b93c1/tests/sim.sh#L817-L818)

### Class A (Execution Evidence)

**WARNING:** No tests found that directly import or reference the changed file.
This file has no claim-specific execution evidence.

### Code Quality (Linting & Types)

- **ruff:** 22843 error(s)
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
| 1 | The two-clone simulation rejects ambiguous bet actions, cap ... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | The simulation's text mutation helper runs portably on BSD a... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 3 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 2 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), pytest (no claim-specific tests found), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Add adversarial fixtures for all PR 51 enforcement defects

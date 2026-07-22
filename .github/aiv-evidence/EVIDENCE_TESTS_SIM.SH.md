# AIV Evidence File (v1.0)

**File:** `tests/sim.sh`
**Commit:** `be6bf5a`
**Generated:** 2026-07-22T22:06:46Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "tests/sim.sh"
  classification_rationale: "R3 because these tests adjudicate payment verification, separation of duties, and conclusion authorization"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T22:06:46Z"
```

## Claim(s)

1. The simulation rejects agent-self-certified human fulfillment and exercises operator facts publication, agent sync, and verifier-checkout supervision
2. The simulation proves Base scoring uses finalized payer-bound settlement events and a new run does not recount prior-run revenue
3. The simulation fails Base startup when operator wallet identities are absent
4. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/commit/e07aefd61e52f61d314cc211df056ee312793da3](https://github.com/ImmortalDemonGod/money-agent/commit/e07aefd61e52f61d314cc211df056ee312793da3)
- **Requirements Verified:** Add adversarial regressions for each load-bearing PR #50 review finding

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`be6bf5a`](https://github.com/ImmortalDemonGod/money-agent/tree/be6bf5a9e4296196d58f6dfc4a47ce0ef3bf3a30))

- [`tests/sim.sh#L200-L208`](https://github.com/ImmortalDemonGod/money-agent/blob/be6bf5a9e4296196d58f6dfc4a47ce0ef3bf3a30/tests/sim.sh#L200-L208)
- [`tests/sim.sh#L210-L211`](https://github.com/ImmortalDemonGod/money-agent/blob/be6bf5a9e4296196d58f6dfc4a47ce0ef3bf3a30/tests/sim.sh#L210-L211)
- [`tests/sim.sh#L215-L224`](https://github.com/ImmortalDemonGod/money-agent/blob/be6bf5a9e4296196d58f6dfc4a47ce0ef3bf3a30/tests/sim.sh#L215-L224)
- [`tests/sim.sh#L226-L227`](https://github.com/ImmortalDemonGod/money-agent/blob/be6bf5a9e4296196d58f6dfc4a47ce0ef3bf3a30/tests/sim.sh#L226-L227)
- [`tests/sim.sh#L453-L454`](https://github.com/ImmortalDemonGod/money-agent/blob/be6bf5a9e4296196d58f6dfc4a47ce0ef3bf3a30/tests/sim.sh#L453-L454)
- [`tests/sim.sh#L458-L462`](https://github.com/ImmortalDemonGod/money-agent/blob/be6bf5a9e4296196d58f6dfc4a47ce0ef3bf3a30/tests/sim.sh#L458-L462)
- [`tests/sim.sh#L467`](https://github.com/ImmortalDemonGod/money-agent/blob/be6bf5a9e4296196d58f6dfc4a47ce0ef3bf3a30/tests/sim.sh#L467)
- [`tests/sim.sh#L470-L471`](https://github.com/ImmortalDemonGod/money-agent/blob/be6bf5a9e4296196d58f6dfc4a47ce0ef3bf3a30/tests/sim.sh#L470-L471)
- [`tests/sim.sh#L473-L474`](https://github.com/ImmortalDemonGod/money-agent/blob/be6bf5a9e4296196d58f6dfc4a47ce0ef3bf3a30/tests/sim.sh#L473-L474)
- [`tests/sim.sh#L480`](https://github.com/ImmortalDemonGod/money-agent/blob/be6bf5a9e4296196d58f6dfc4a47ce0ef3bf3a30/tests/sim.sh#L480)
- [`tests/sim.sh#L482-L488`](https://github.com/ImmortalDemonGod/money-agent/blob/be6bf5a9e4296196d58f6dfc4a47ce0ef3bf3a30/tests/sim.sh#L482-L488)
- [`tests/sim.sh#L495-L496`](https://github.com/ImmortalDemonGod/money-agent/blob/be6bf5a9e4296196d58f6dfc4a47ce0ef3bf3a30/tests/sim.sh#L495-L496)
- [`tests/sim.sh#L503-L506`](https://github.com/ImmortalDemonGod/money-agent/blob/be6bf5a9e4296196d58f6dfc4a47ce0ef3bf3a30/tests/sim.sh#L503-L506)
- [`tests/sim.sh#L508-L513`](https://github.com/ImmortalDemonGod/money-agent/blob/be6bf5a9e4296196d58f6dfc4a47ce0ef3bf3a30/tests/sim.sh#L508-L513)
- [`tests/sim.sh#L519-L525`](https://github.com/ImmortalDemonGod/money-agent/blob/be6bf5a9e4296196d58f6dfc4a47ce0ef3bf3a30/tests/sim.sh#L519-L525)
- [`tests/sim.sh#L545-L572`](https://github.com/ImmortalDemonGod/money-agent/blob/be6bf5a9e4296196d58f6dfc4a47ce0ef3bf3a30/tests/sim.sh#L545-L572)
- [`tests/sim.sh#L595-L610`](https://github.com/ImmortalDemonGod/money-agent/blob/be6bf5a9e4296196d58f6dfc4a47ce0ef3bf3a30/tests/sim.sh#L595-L610)

### Class A (Execution Evidence)

**WARNING:** No tests found that directly import or reference the changed file.
This file has no claim-specific execution evidence.

### Code Quality (Linting & Types)

- **ruff:** 16215 error(s)
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
e07aefd [S8] human-actuation queue: request-don't-wait, metered, conclusion-blocking (#31) + the atomic PROMPT amendment
3143f26 [S7] rail adapters: the P1 contract + a stubbed Base/USDC rail with settlement-event binding (#30 Part 1)
aa601ba [S6] edge-verdict quality: frozen risk cap + peak tracking + signed edge facts (#38, closes the S4 edge-signing deferral)
b36b966 [S5] gates & probes: delivery seam + provider cap, oracle-classed resolutions, mechanical pacing (#39 #35 #40 #45)
2a5f010 [S4] fact-lane signing: verifier signatures + hash chain + customer attestation (#36 #42)
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | The simulation rejects agent-self-certified human fulfillmen... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | The simulation proves Base scoring uses finalized payer-boun... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 3 | The simulation fails Base startup when operator wallet ident... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 4 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 3 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), pytest (no claim-specific tests found), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Replay Base and human-actuation trust failures in the two-lane rig

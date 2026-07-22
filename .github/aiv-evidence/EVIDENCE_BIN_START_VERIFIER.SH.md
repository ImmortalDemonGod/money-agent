# AIV Evidence File (v1.0)

**File:** `bin/start_verifier.sh`
**Commit:** `594984a`
**Generated:** 2026-07-22T22:04:31Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "bin/start_verifier.sh"
  classification_rationale: "R3 because startup provisioning controls payment identity classification and verified revenue"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T22:04:31Z"
```

## Claim(s)

1. An armed Base rail cannot start unless all settlement binding fields and at least one operator wallet address are provisioned before baseline creation
2. Verifier environment is loaded before the Base baseline is frozen
3. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/commit/e07aefd61e52f61d314cc211df056ee312793da3](https://github.com/ImmortalDemonGod/money-agent/commit/e07aefd61e52f61d314cc211df056ee312793da3)
- **Requirements Verified:** Fail closed when the Base wash-trade guard or binding schema is inert

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`594984a`](https://github.com/ImmortalDemonGod/money-agent/tree/594984a22d036cbe854ff9a35098e81cb77dfd7e))

- [`bin/start_verifier.sh#L22-L30`](https://github.com/ImmortalDemonGod/money-agent/blob/594984a22d036cbe854ff9a35098e81cb77dfd7e/bin/start_verifier.sh#L22-L30)
- [`bin/start_verifier.sh#L66-L88`](https://github.com/ImmortalDemonGod/money-agent/blob/594984a22d036cbe854ff9a35098e81cb77dfd7e/bin/start_verifier.sh#L66-L88)

### Class A (Execution Evidence)

**WARNING:** No tests found that directly import or reference the changed file.
This file has no claim-specific execution evidence.

### Code Quality (Linting & Types)

- **ruff:** 2258 error(s)
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
| 1 | An armed Base rail cannot start unless all settlement bindin... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | Verifier environment is loaded before the Base baseline is f... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 3 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 2 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), pytest (no claim-specific tests found), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Fail startup on incomplete Base trust configuration

# AIV Evidence File (v1.0)

**File:** `PROMPT.md`
**Commit:** `1986b8e`
**Previous:** `8883e8a`
**Generated:** 2026-07-23T01:24:25Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "PROMPT.md"
  classification_rationale: "Pairs the aiv_gate P3 wiring with the agent-facing instruction. R3: run-prompt change"
  classified_by: "Claude"
  classified_at: "2026-07-23T01:24:25Z"
```

## Claim(s)

1. The run prompt instructs that any published/listing/data-acquisition claim requires a recorded P3 decision (bin/decision_gate.py) committed before the act, alongside the existing host_check requirement, so the agent knows to use the now-wired gate
2. No existing tests were modified or deleted
3. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/51](https://github.com/ImmortalDemonGod/money-agent/pull/51)
- **Requirements Verified:** The agent-facing prompt must instruct use of the P3 decision gate for publish/listing/acquisition, or the wired gate blocks the agent without telling it how to comply

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`1986b8e`](https://github.com/ImmortalDemonGod/money-agent/tree/1986b8e9d95dd253c49a97a5c7bd1247a29804d5))

- [`PROMPT.md#L134-L138`](https://github.com/ImmortalDemonGod/money-agent/blob/1986b8e9d95dd253c49a97a5c7bd1247a29804d5/PROMPT.md#L134-L138)

### Class A (Execution Evidence)

**WARNING:** No tests found that directly import or reference the changed file.
This file has no claim-specific execution evidence.

### Code Quality (Linting & Types)

- **ruff:** 0 error(s)
- **mypy:** 

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
9c7574d Merge main into run2-e-v3-gated (rebase after #50 merged)
5b05cc4 test(human): skip signing tests when ssh-keygen is absent (sim portability)
24ca694 Merge main into run2-d-rails-human (rebase after #49 merged): pick up #49's gate/edge work
d9d3dfe test(delivery): cover fail-closed arg parsing (unrecognized/value-less flags)
d060b27 test(rails): call monetary validator directly
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | The run prompt instructs that any published/listing/data-acq... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted | structural | Class C: all structural indicators clean | PASS VERIFIED |
| 3 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 2 verified, 0 unverified, 1 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), pytest (no claim-specific tests found), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

PROMPT.md step 4 adds the recorded-P3-decision requirement to publish claims

# AIV Evidence File (v1.0)

**File:** `PROMPT.md`
**Commit:** `32e2318`
**Previous:** `597449f`
**Generated:** 2026-07-23T01:48:13Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "PROMPT.md"
  classification_rationale: "Pairs with the gate message. R3: run-prompt change"
  classified_by: "Claude"
  classified_at: "2026-07-23T01:48:13Z"
```

## Claim(s)

1. The run prompt documents the runnable decision-gate command and that the recorded body must equal the published URL, so the agent can satisfy the gate's publish decision check
2. No existing tests were modified or deleted
3. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/51](https://github.com/ImmortalDemonGod/money-agent/pull/51)
- **Requirements Verified:** PROMPT.md must document a runnable decision-gate command whose body matches the publish URL the gate checks (CodeRabbit Minor)

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`32e2318`](https://github.com/ImmortalDemonGod/money-agent/tree/32e231800b7222703386ab980a46b7f916a22f3f))

- [`PROMPT.md#L134-L140`](https://github.com/ImmortalDemonGod/money-agent/blob/32e231800b7222703386ab980a46b7f916a22f3f/PROMPT.md#L134-L140)

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
6da1998 test(watchdog): assert breached records are not counted as open
dfde8e4 test(watchdog): late-reachable delivery and unknown status breach and refund
b28993c test(gate): note the P3 publish-decision requirement (e2e fixture deferred)
9c7574d Merge main into run2-e-v3-gated (rebase after #50 merged)
5b05cc4 test(human): skip signing tests when ssh-keygen is absent (sim portability)
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | The run prompt documents the runnable decision-gate command ... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
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

Document the runnable publish decision-gate command and body-equals-URL rule

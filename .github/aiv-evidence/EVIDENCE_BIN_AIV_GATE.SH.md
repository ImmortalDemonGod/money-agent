# AIV Evidence File (v1.0)

**File:** `bin/aiv_gate.sh`
**Commit:** `6da1998`
**Previous:** `1986b8e`
**Generated:** 2026-07-23T01:48:12Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "bin/aiv_gate.sh"
  classification_rationale: "CodeRabbit: the message named an unrunnable command. R3: gate"
  classified_by: "Claude"
  classified_at: "2026-07-23T01:48:12Z"
```

## Claim(s)

1. The publish-claim failure message states the full recording command and that the decision body must equal the published URL, so the instruction is executable and matches what the gate checks
2. No existing tests were modified or deleted
3. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/51](https://github.com/ImmortalDemonGod/money-agent/pull/51)
- **Requirements Verified:** The P3 failure message must show a runnable command whose body matches the gate's check (CodeRabbit Minor)

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`6da1998`](https://github.com/ImmortalDemonGod/money-agent/tree/6da1998cebca3664185b032cde1377311e415492))

- [`bin/aiv_gate.sh#L190`](https://github.com/ImmortalDemonGod/money-agent/blob/6da1998cebca3664185b032cde1377311e415492/bin/aiv_gate.sh#L190)

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
| 1 | The publish-claim failure message states the full recording ... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
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

Publish P3 failure message shows the runnable command and the body-equals-URL rule

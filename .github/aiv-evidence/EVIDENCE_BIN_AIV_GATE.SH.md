# AIV Evidence File (v1.0)

**File:** `bin/aiv_gate.sh`
**Commit:** `abf1cad`
**Previous:** `de7d1e8`
**Generated:** 2026-07-23T01:24:24Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "bin/aiv_gate.sh"
  classification_rationale: "Closure-audit finding: #51 claims to deliver P3 but nothing invoked it. Wired into aiv_gate 2b, the same enforcement point as host_check/delivery_check. R3: aiv_gate is a gate"
  classified_by: "Claude"
  classified_at: "2026-07-23T01:24:24Z"
```

## Claim(s)

1. A publish claim in a packet now requires a recorded, non-stub P3 decision for its URL, checked offline and fail-closed before the network host_check; without this wiring the decision_gate module was built and unit-tested but never invoked by any action
2. No existing tests were modified or deleted
3. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/51](https://github.com/ImmortalDemonGod/money-agent/pull/51)
- **Requirements Verified:** P3 (recorded-decision gate) must actually fire before a declared risk-class action, mirroring how disclosure_gate is wired into mail.py; #51 shipped decision_gate with no caller (inert)

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`abf1cad`](https://github.com/ImmortalDemonGod/money-agent/tree/abf1cad334cd98cf6eb906098b771915651ee40e))

- [`bin/aiv_gate.sh#L185-L190`](https://github.com/ImmortalDemonGod/money-agent/blob/abf1cad334cd98cf6eb906098b771915651ee40e/bin/aiv_gate.sh#L185-L190)

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
| 1 | A publish claim in a packet now requires a recorded, non-stu... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
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

aiv_gate 2b requires a recorded publish decision (decision_gate) before host_check

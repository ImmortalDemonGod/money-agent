# AIV Evidence File (v1.0)

**File:** `CONSTITUTION.md`
**Commit:** `8883e8a`
**Generated:** 2026-07-23T01:23:49Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "CONSTITUTION.md"
  classification_rationale: "Operator-directed coherence fix: the obligations authorization was wired into CLAUDE.md only; this brings the formal constitution into agreement. R3: a constitutional-class change"
  classified_by: "Claude"
  classified_at: "2026-07-23T01:23:49Z"
```

## Claim(s)

1. Constitution rule 3 authorizes the guarded post-payment obligation path (verifier-enabled, refund-backed, exposure/deadline-capped, typed) instead of a flat prohibition, matching CLAUDE.md and PROMPT.md so the obligations layer is not contradicted by the formal bounds doc
2. No existing tests were modified or deleted
3. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/51](https://github.com/ImmortalDemonGod/money-agent/pull/51)
- **Requirements Verified:** All three constitution surfaces (CONSTITUTION.md, CLAUDE.md, PROMPT.md) must agree on the delivery bound; #51 updated only CLAUDE.md, leaving rule 3 a categorical prohibition that contradicts the obligations layer

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`8883e8a`](https://github.com/ImmortalDemonGod/money-agent/tree/8883e8a6ae0a79ff893a9b19f95cff2b4b5d03d3))

- [`CONSTITUTION.md#L30-L40`](https://github.com/ImmortalDemonGod/money-agent/blob/8883e8a6ae0a79ff893a9b19f95cff2b4b5d03d3/CONSTITUTION.md#L30-L40)

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
| 1 | Constitution rule 3 authorizes the guarded post-payment obli... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
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

Reconcile CONSTITUTION.md rule 3 to the instant-or-mechanically-guaranteed delivery bound

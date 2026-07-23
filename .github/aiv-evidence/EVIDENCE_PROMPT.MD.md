# AIV Evidence File (v1.0)

**File:** `PROMPT.md`
**Commit:** `9c7574d`
**Previous:** `201c610`
**Generated:** 2026-07-23T00:59:14Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "PROMPT.md"
  classification_rationale: "Operator-directed fix of a wiring contradiction: CLAUDE.md authorized obligations in #51 but PROMPT.md/CONSTITUTION.md did not. R3: a constitutional-class prompt change"
  classified_by: "Claude"
  classified_at: "2026-07-23T00:59:14Z"
```

## Claim(s)

1. The run prompt authorizes the guarded post-payment obligation path (verifier-enabled, refund-backed, capped, typed) consistent with CLAUDE.md, so the obligations safety layer is not left functionally inert by a prompt that categorically forbids every post-payment action
2. The first-dollar section notes the out-of-band obligation verifier continues until every guaranteed liability is fulfilled or refunded, matching CLAUDE.md
3. No existing tests were modified or deleted
4. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/51](https://github.com/ImmortalDemonGod/money-agent/pull/51)
- **Requirements Verified:** PROMPT.md (the prompt the agent actually follows each iteration) must authorize the same guarded obligation path CLAUDE.md authorizes; the operator flagged that PROMPT.md still categorically forbade every post-payment action, leaving the new safety mechanism inert

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`9c7574d`](https://github.com/ImmortalDemonGod/money-agent/tree/9c7574d1e3b5161518f0a4067afcec78036b03e6))

- [`PROMPT.md#L28-L38`](https://github.com/ImmortalDemonGod/money-agent/blob/9c7574d1e3b5161518f0a4067afcec78036b03e6/PROMPT.md#L28-L38)
- [`PROMPT.md#L44-L48`](https://github.com/ImmortalDemonGod/money-agent/blob/9c7574d1e3b5161518f0a4067afcec78036b03e6/PROMPT.md#L44-L48)

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
| 1 | The run prompt authorizes the guarded post-payment obligatio... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | The first-dollar section notes the out-of-band obligation ve... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 3 | No existing tests were modified or deleted | structural | Class C: all structural indicators clean | PASS VERIFIED |
| 4 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 2 verified, 0 unverified, 2 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), pytest (no claim-specific tests found), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Reconcile PROMPT.md's delivery + first-dollar bounds to CLAUDE.md's obligation authorization

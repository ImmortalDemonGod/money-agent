# AIV Evidence File (v1.0)

**File:** `bin/supervise.sh`
**Commit:** `5b821c4`
**Previous:** `815bad0`
**Generated:** 2026-07-22T23:33:09Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "bin/supervise.sh"
  classification_rationale: "Masked health failures could misdirect the autonomous run"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T23:33:09Z"
```

## Claim(s)

1. Supervisor VERDICT escalates unreadable signed queue state and reports a dead verifier before live human queue work
2. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/50#pullrequestreview-4759622532](https://github.com/ImmortalDemonGod/money-agent/pull/50#pullrequestreview-4759622532)
- **Requirements Verified:** CodeRabbit requires signature failures to remain visible and verifier death to outrank queue actuation

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`5b821c4`](https://github.com/ImmortalDemonGod/money-agent/tree/5b821c43d106699d7d93500c442d4752656be815))

- [`bin/supervise.sh#L146-L149`](https://github.com/ImmortalDemonGod/money-agent/blob/5b821c43d106699d7d93500c442d4752656be815/bin/supervise.sh#L146-L149)

### Class A (Execution Evidence)

**WARNING:** No tests found that directly import or reference the changed file.
This file has no claim-specific execution evidence.

### Code Quality (Linting & Types)

- **ruff:** 2301 error(s)
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
dfe3ff8 test(pr50): pin final review failure modes
d52a400 test(rails): expand fail-closed registry catalog
710e1c0 merge(stack): sync rewritten stack 3 ancestry
618e3eb merge(stack): integrate reviewed stack 3 advances
4ff597e test(delivery): cover content-type refusal
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | Supervisor VERDICT escalates unreadable signed queue state a... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 1 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), pytest (no claim-specific tests found), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Reorder supervisor fail-closed verdict precedence

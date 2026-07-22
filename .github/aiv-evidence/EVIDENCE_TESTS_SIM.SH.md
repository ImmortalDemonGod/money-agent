# AIV Evidence File (v1.0)

**File:** `tests/sim.sh`
**Commit:** `a308fe3`
**Previous:** `dfe3ff8`
**Generated:** 2026-07-22T23:35:00Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "tests/sim.sh"
  classification_rationale: "The previous fixture wrote an unused PID file and tested the wrong state"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T23:35:00Z"
```

## Claim(s)

1. Queue precedence assertions run with a matching live verifier process and the dead-precedence assertion terminates it deliberately
2. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/50#pullrequestreview-4759622532](https://github.com/ImmortalDemonGod/money-agent/pull/50#pullrequestreview-4759622532)
- **Requirements Verified:** Supervisor tests must control the actual pgrep-based health input

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`a308fe3`](https://github.com/ImmortalDemonGod/money-agent/tree/a308fe3c3f11fdd318696ceef4b1ecfc8a89ea89))

- [`tests/sim.sh#L251-L252`](https://github.com/ImmortalDemonGod/money-agent/blob/a308fe3c3f11fdd318696ceef4b1ecfc8a89ea89/tests/sim.sh#L251-L252)
- [`tests/sim.sh#L257-L258`](https://github.com/ImmortalDemonGod/money-agent/blob/a308fe3c3f11fdd318696ceef4b1ecfc8a89ea89/tests/sim.sh#L257-L258)
- [`tests/sim.sh#L261-L262`](https://github.com/ImmortalDemonGod/money-agent/blob/a308fe3c3f11fdd318696ceef4b1ecfc8a89ea89/tests/sim.sh#L261-L262)
- [`tests/sim.sh#L300-L301`](https://github.com/ImmortalDemonGod/money-agent/blob/a308fe3c3f11fdd318696ceef4b1ecfc8a89ea89/tests/sim.sh#L300-L301)

### Class A (Execution Evidence)

**WARNING:** No tests found that directly import or reference the changed file.
This file has no claim-specific execution evidence.

### Code Quality (Linting & Types)

- **ruff:** 18108 error(s)
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
| 1 | Queue precedence assertions run with a matching live verifie... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 1 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), pytest (no claim-specific tests found), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Make supervisor health fixtures behaviorally accurate

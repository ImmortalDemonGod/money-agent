# AIV Evidence File (v1.0)

**File:** `tests/sim.sh`
**Commit:** `512f388`
**Previous:** `30612e5`
**Generated:** 2026-07-22T23:08:22Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "tests/sim.sh"
  classification_rationale: "R3 integration evidence because the simulation crosses the agent/verifier payment authorization boundary"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T23:08:22Z"
```

## Claim(s)

1. The two-lane simulation proves agent-local exposure variables cannot activate obligations
2. The verifier facts lane publishes an enabled authorization only with refund authority and all positive caps
3. A grounded authorization reaches exposure enforcement while grounded received funds remain binding
4. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/51](https://github.com/ImmortalDemonGod/money-agent/pull/51)
- **Requirements Verified:** PR 51 must preserve default-off behavior while permitting explicitly enabled mechanically guaranteed obligations

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`512f388`](https://github.com/ImmortalDemonGod/money-agent/tree/512f388bedaad690811c99e342233bf4c6cedfef))

- [`tests/sim.sh#L410`](https://github.com/ImmortalDemonGod/money-agent/blob/512f388bedaad690811c99e342233bf4c6cedfef/tests/sim.sh#L410)
- [`tests/sim.sh#L413-L429`](https://github.com/ImmortalDemonGod/money-agent/blob/512f388bedaad690811c99e342233bf4c6cedfef/tests/sim.sh#L413-L429)

### Class A (Execution Evidence)

**WARNING:** No tests found that directly import or reference the changed file.
This file has no claim-specific execution evidence.

### Code Quality (Linting & Types)

- **ruff:** 23946 error(s)
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
512f388 test(obligations): cover guarded authorization contract
30612e5 test(sim): exercise CodeRabbit review invariants
76c1bec test(v3): cover CodeRabbit hardening findings
bb5cbed test(sim): adversarially cover PR 51 hardening
d90785d test(v3): cover adversarial enforcement seams
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | The two-lane simulation proves agent-local exposure variable... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | The verifier facts lane publishes an enabled authorization o... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 3 | A grounded authorization reaches exposure enforcement while ... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 4 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 3 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), pytest (no claim-specific tests found), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Exercise obligation authorization on separate claims and facts lanes

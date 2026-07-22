# AIV Evidence File (v1.0)

**File:** `tests/sim.sh`
**Commit:** `d52a400`
**Previous:** `618e3eb`
**Generated:** 2026-07-22T23:31:33Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "tests/sim.sh"
  classification_rationale: "The cases govern payment facts and conclusion authorization"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T23:31:33Z"
```

## Claim(s)

1. The integration matrix covers missing human task registries, dead and unreadable supervisor precedence, address normalization, and mandatory Base live acceptance
2. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/50#pullrequestreview-4759622532](https://github.com/ImmortalDemonGod/money-agent/pull/50#pullrequestreview-4759622532)
- **Requirements Verified:** Final CodeRabbit review identified trust-boundary cases that must fail closed in the committed two-lane simulation

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`d52a400`](https://github.com/ImmortalDemonGod/money-agent/tree/d52a4006adf724376a78abc1219296e8791de74d))

- [`tests/sim.sh#L251-L252`](https://github.com/ImmortalDemonGod/money-agent/blob/d52a4006adf724376a78abc1219296e8791de74d/tests/sim.sh#L251-L252)
- [`tests/sim.sh#L257-L273`](https://github.com/ImmortalDemonGod/money-agent/blob/d52a4006adf724376a78abc1219296e8791de74d/tests/sim.sh#L257-L273)
- [`tests/sim.sh#L284-L288`](https://github.com/ImmortalDemonGod/money-agent/blob/d52a4006adf724376a78abc1219296e8791de74d/tests/sim.sh#L284-L288)
- [`tests/sim.sh#L619-L626`](https://github.com/ImmortalDemonGod/money-agent/blob/d52a4006adf724376a78abc1219296e8791de74d/tests/sim.sh#L619-L626)
- [`tests/sim.sh#L657`](https://github.com/ImmortalDemonGod/money-agent/blob/d52a4006adf724376a78abc1219296e8791de74d/tests/sim.sh#L657)
- [`tests/sim.sh#L705-L709`](https://github.com/ImmortalDemonGod/money-agent/blob/d52a4006adf724376a78abc1219296e8791de74d/tests/sim.sh#L705-L709)
- [`tests/sim.sh#L720`](https://github.com/ImmortalDemonGod/money-agent/blob/d52a4006adf724376a78abc1219296e8791de74d/tests/sim.sh#L720)
- [`tests/sim.sh#L804-L814`](https://github.com/ImmortalDemonGod/money-agent/blob/d52a4006adf724376a78abc1219296e8791de74d/tests/sim.sh#L804-L814)

### Class A (Execution Evidence)

**WARNING:** No tests found that directly import or reference the changed file.
This file has no claim-specific execution evidence.

### Code Quality (Linting & Types)

- **ruff:** 17954 error(s)
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
d52a400 test(rails): expand fail-closed registry catalog
710e1c0 merge(stack): sync rewritten stack 3 ancestry
618e3eb merge(stack): integrate reviewed stack 3 advances
4ff597e test(delivery): cover content-type refusal
85d4db3 test(edge): cover benchmark-relative verdicts
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | The integration matrix covers missing human task registries,... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 1 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), pytest (no claim-specific tests found), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Add adversarial regressions before final production fixes

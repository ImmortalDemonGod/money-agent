# AIV Evidence File (v1.0)

**File:** `bin/iter.py`
**Commit:** `d9d3dfe`
**Previous:** `76d2496`
**Generated:** 2026-07-23T00:17:09Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "bin/iter.py"
  classification_rationale: "Addresses the CodeRabbit ImportError fail-open; also removes an unused import and an inert f-string that ruff flags. R3: this scaffold is in the SoD-owned set"
  classified_by: "Claude"
  classified_at: "2026-07-23T00:17:09Z"
```

## Claim(s)

1. With PACE_ENFORCE=1 and the bets registry module unimportable, the iteration-opening command is refused with a non-zero exit rather than proceeding silently, so an unverifiable pacing state fails closed
2. The lever-declared bypass is preserved: a supplied lever still opens the iteration (the issue #45 mechanism), and the watch and resolution paths are unaffected
3. No existing tests were modified or deleted in this change
4. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/issues/45](https://github.com/ImmortalDemonGod/money-agent/issues/45)
- **Requirements Verified:** PACE_ENFORCE is opt-in pacing; an unimportable registry must fail closed, not silently pass (CodeRabbit fail-open finding), while keeping the lever escape issue #45 specifies

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`d9d3dfe`](https://github.com/ImmortalDemonGod/money-agent/tree/d9d3dfebecc538cc70596ff0a4d739f5f1e9a6a1))

- [`bin/iter.py#L118`](https://github.com/ImmortalDemonGod/money-agent/blob/d9d3dfebecc538cc70596ff0a4d739f5f1e9a6a1/bin/iter.py#L118)
- [`bin/iter.py#L122-L137`](https://github.com/ImmortalDemonGod/money-agent/blob/d9d3dfebecc538cc70596ff0a4d739f5f1e9a6a1/bin/iter.py#L122-L137)
- [`bin/iter.py#L169`](https://github.com/ImmortalDemonGod/money-agent/blob/d9d3dfebecc538cc70596ff0a4d739f5f1e9a6a1/bin/iter.py#L169)

### Class A (Execution Evidence)

**Per-symbol test coverage (AST analysis):**

- **`new`** (L118): FAIL -- WARNING: No tests import or call `new`

**Coverage summary:** 0/1 symbols verified by tests.

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
d9d3dfe test(delivery): cover fail-closed arg parsing (unrecognized/value-less flags)
4ff597e test(delivery): cover content-type refusal
85d4db3 test(edge): cover benchmark-relative verdicts
bd2321b test(edge): cover finite caps and scoped peaks
7da62d7 test(delivery): reject unrelated Stripe success URLs
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | With PACE_ENFORCE=1 and the bets registry module unimportabl... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | The lever-declared bypass is preserved: a supplied lever sti... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 3 | No existing tests were modified or deleted in this change | structural | Class C: all structural indicators clean | PASS VERIFIED |
| 4 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 2 verified, 0 unverified, 2 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), AST symbol-to-test binding (0/1 symbols verified), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Fail closed on registry ImportError; keep the lever bypass; drop unused re import and inert f-string

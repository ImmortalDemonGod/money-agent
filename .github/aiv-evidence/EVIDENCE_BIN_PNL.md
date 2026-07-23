# AIV Evidence File (v1.0)

**File:** `bin/pnl.py`
**Commit:** `6c6c0b2`
**Previous:** `6ebea50`
**Generated:** 2026-07-22T23:32:01Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "bin/pnl.py"
  classification_rationale: "Incorrect normalization could count a self-funded settlement as customer revenue"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T23:32:01Z"
```

## Claim(s)

1. Operator wallet addresses with or without a 0x prefix normalize to lowercase 20-byte hex and malformed addresses fail closed
2. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/50#discussion_r3634578676](https://github.com/ImmortalDemonGod/money-agent/pull/50#discussion_r3634578676)
- **Requirements Verified:** CodeRabbit requires operator identity comparison to use the same canonical address form as settlement events

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`6c6c0b2`](https://github.com/ImmortalDemonGod/money-agent/tree/6c6c0b2ac8414f2c1f8fecdad8eb8e3d12ac960b))

- [`bin/pnl.py#L178-L185`](https://github.com/ImmortalDemonGod/money-agent/blob/6c6c0b2ac8414f2c1f8fecdad8eb8e3d12ac960b/bin/pnl.py#L178-L185)

### Class A (Execution Evidence)

**Per-symbol test coverage (AST analysis):**

- **`_operator_addresses`** (L178-L185): FAIL -- WARNING: No tests import or call `_operator_addresses`

**Coverage summary:** 0/1 symbols verified by tests.

### Code Quality (Linting & Types)

- **ruff:** All checks passed
- **mypy:** Found 15 errors in 2 files (checked 1 source file)

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
| 1 | Operator wallet addresses with or without a 0x prefix normal... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 1 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), AST symbol-to-test binding (0/1 symbols verified), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Normalize and validate on-chain operator identities

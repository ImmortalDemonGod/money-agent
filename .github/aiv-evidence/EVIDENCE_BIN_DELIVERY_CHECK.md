# AIV Evidence File (v1.0)

**File:** `bin/delivery_check.py`
**Commit:** `31c829c`
**Previous:** `76b1f2f`
**Generated:** 2026-07-22T23:03:10Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "bin/delivery_check.py"
  classification_rationale: "python3 -m py_compile bin/delivery_check.py; bash tests/sim.sh"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T23:03:10Z"
```

## Claim(s)

1. The delivery probe rejects missing or non-document content types before accepting a paid completion artifact.
2. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/issues/39](https://github.com/ImmortalDemonGod/money-agent/issues/39)
- **Requirements Verified:** The pay-to-deliver probe must verify status, explicit content type, and a non-placeholder body fail closed.

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`31c829c`](https://github.com/ImmortalDemonGod/money-agent/tree/31c829c3709c3d0a160577a2755fd35da3282f7c))

- [`bin/delivery_check.py#L22`](https://github.com/ImmortalDemonGod/money-agent/blob/31c829c3709c3d0a160577a2755fd35da3282f7c/bin/delivery_check.py#L22)
- [`bin/delivery_check.py#L40-L46`](https://github.com/ImmortalDemonGod/money-agent/blob/31c829c3709c3d0a160577a2755fd35da3282f7c/bin/delivery_check.py#L40-L46)
- [`bin/delivery_check.py#L49`](https://github.com/ImmortalDemonGod/money-agent/blob/31c829c3709c3d0a160577a2755fd35da3282f7c/bin/delivery_check.py#L49)
- [`bin/delivery_check.py#L54`](https://github.com/ImmortalDemonGod/money-agent/blob/31c829c3709c3d0a160577a2755fd35da3282f7c/bin/delivery_check.py#L54)
- [`bin/delivery_check.py#L61-L65`](https://github.com/ImmortalDemonGod/money-agent/blob/31c829c3709c3d0a160577a2755fd35da3282f7c/bin/delivery_check.py#L61-L65)
- [`bin/delivery_check.py#L67`](https://github.com/ImmortalDemonGod/money-agent/blob/31c829c3709c3d0a160577a2755fd35da3282f7c/bin/delivery_check.py#L67)
- [`bin/delivery_check.py#L70`](https://github.com/ImmortalDemonGod/money-agent/blob/31c829c3709c3d0a160577a2755fd35da3282f7c/bin/delivery_check.py#L70)
- [`bin/delivery_check.py#L125`](https://github.com/ImmortalDemonGod/money-agent/blob/31c829c3709c3d0a160577a2755fd35da3282f7c/bin/delivery_check.py#L125)
- [`bin/delivery_check.py#L127-L129`](https://github.com/ImmortalDemonGod/money-agent/blob/31c829c3709c3d0a160577a2755fd35da3282f7c/bin/delivery_check.py#L127-L129)
- [`bin/delivery_check.py#L150`](https://github.com/ImmortalDemonGod/money-agent/blob/31c829c3709c3d0a160577a2755fd35da3282f7c/bin/delivery_check.py#L150)
- [`bin/delivery_check.py#L154`](https://github.com/ImmortalDemonGod/money-agent/blob/31c829c3709c3d0a160577a2755fd35da3282f7c/bin/delivery_check.py#L154)

### Class A (Execution Evidence)

**Per-symbol test coverage (AST analysis):**

- **`_fetch`** (L22): FAIL -- WARNING: No tests import or call `_fetch`
- **`main`** (L40-L46): FAIL -- WARNING: No tests import or call `main`

**Coverage summary:** 0/2 symbols verified by tests.

### Code Quality (Linting & Types)

- **ruff:** All checks passed
- **mypy:** Success: no issues found in 1 source file

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
aa80a5d test(edge): cover benchmark-relative verdicts
88a6899 test(edge): cover finite caps and scoped peaks
e53b606 test(delivery): reject unrelated Stripe success URLs
aa1dc15 [S6] edge-verdict quality: frozen risk cap + peak tracking + signed edge facts (#38, closes the S4 edge-signing deferral)
fe0427a [S5] gates & probes: delivery seam + provider cap, oracle-classed resolutions, mechanical pacing (#39 #35 #40 #45)
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | The delivery probe rejects missing or non-document content t... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 1 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), AST symbol-to-test binding (0/2 symbols verified), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Only the verifier fetch path changes; unsupported or missing Content-Type causes a refusal.

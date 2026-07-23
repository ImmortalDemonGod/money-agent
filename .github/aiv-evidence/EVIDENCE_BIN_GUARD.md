# AIV Evidence File (v1.0)

**File:** `bin/guard.py`
**Commit:** `994cd6f`
**Generated:** 2026-07-22T22:37:58Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "bin/guard.py"
  classification_rationale: "R3 integrity gate"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T22:37:58Z"
```

## Claim(s)

1. Guard treats every edge integrity error other than genuine absence as a halt
2. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/issues/38](https://github.com/ImmortalDemonGod/money-agent/issues/38)
- **Requirements Verified:** Edge facts must not silently become idle when unreadable

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`994cd6f`](https://github.com/ImmortalDemonGod/money-agent/tree/994cd6fa05aa8bfdf56bf9639a5deb782fad7bcc))

- [`bin/guard.py#L263`](https://github.com/ImmortalDemonGod/money-agent/blob/994cd6fa05aa8bfdf56bf9639a5deb782fad7bcc/bin/guard.py#L263)

### Class A (Execution Evidence)

**Per-symbol test coverage (AST analysis):**

- **`main`** (L263): FAIL -- WARNING: No tests import or call `main`

**Coverage summary:** 0/1 symbols verified by tests.

### Code Quality (Linting & Types)

- **ruff:** 13 error(s)
- **mypy:** Found 3 errors in 1 file (checked 1 source file)

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
88a6899 test(edge): cover finite caps and scoped peaks
e53b606 test(delivery): reject unrelated Stripe success URLs
aa1dc15 [S6] edge-verdict quality: frozen risk cap + peak tracking + signed edge facts (#38, closes the S4 edge-signing deferral)
fe0427a [S5] gates & probes: delivery seam + provider cap, oracle-classed resolutions, mechanical pacing (#39 #35 #40 #45)
655bb5b test(verifier): cover initial truth signing failure
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | Guard treats every edge integrity error other than genuine a... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 1 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), AST symbol-to-test binding (0/1 symbols verified), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Fail closed for malformed or mismatched edge facts

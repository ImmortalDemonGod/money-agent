# AIV Evidence File (v1.0)

**File:** `bin/human.py`
**Commit:** `24ca694`
**Previous:** `5b821c4`
**Generated:** 2026-07-23T00:48:19Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "bin/human.py"
  classification_rationale: "CodeRabbit flagged a non-atomic read-modify-write; the flock already prevents lost updates, this adds crash-atomicity. R3: human.py is in the SoD-owned set"
  classified_by: "Claude"
  classified_at: "2026-07-23T00:48:19Z"
```

## Claim(s)

1. Publishing a human resolution writes the signed document via a temp file and an atomic replace, so a crash mid-write cannot leave a truncated facts-lane artifact; concurrent writers stay serialized by the existing exclusive lock
2. No existing tests were modified or deleted in this change
3. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/issues/31](https://github.com/ImmortalDemonGod/money-agent/issues/31)
- **Requirements Verified:** The signed human-resolution facts artifact must not be corruptible by a crash mid-write; the read-modify-write is already lock-serialized, this closes the crash-atomicity residual

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`24ca694`](https://github.com/ImmortalDemonGod/money-agent/tree/24ca69431ecb35e49836323c9445fe42bd5b6b2c))

- [`bin/human.py#L173-L178`](https://github.com/ImmortalDemonGod/money-agent/blob/24ca69431ecb35e49836323c9445fe42bd5b6b2c/bin/human.py#L173-L178)

### Class A (Execution Evidence)

**Per-symbol test coverage (AST analysis):**

- **`_publish_resolution`** (L173-L178): FAIL -- WARNING: No tests import or call `_publish_resolution`

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
24ca694 Merge main into run2-d-rails-human (rebase after #49 merged): pick up #49's gate/edge work
d9d3dfe test(delivery): cover fail-closed arg parsing (unrecognized/value-less flags)
d060b27 test(rails): call monetary validator directly
5f37af2 test(supervisor): model live verifier process explicitly
dfe3ff8 test(pr50): pin final review failure modes
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | Publishing a human resolution writes the signed document via... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted in this change | structural | Class C: all structural indicators clean | PASS VERIFIED |
| 3 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 2 verified, 0 unverified, 1 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), AST symbol-to-test binding (0/1 symbols verified), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Write the resolution map to a temp file and os.replace it into place

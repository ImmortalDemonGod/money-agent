# AIV Evidence File (v1.0)

**File:** `bin/human.py`
**Commit:** `a05b6d3`
**Previous:** `e7a1091`
**Generated:** 2026-07-22T23:32:57Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "bin/human.py"
  classification_rationale: "Lost operator resolutions would corrupt the conclusion-authorization audit trail"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T23:32:57Z"
```

## Claim(s)

1. Concurrent operator resolutions share a verifier-private inter-process lock through read, duplicate check, write, signing, staging, commit, and push
2. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/50#discussion_r3634578670](https://github.com/ImmortalDemonGod/money-agent/pull/50#discussion_r3634578670)
- **Requirements Verified:** CodeRabbit requires concurrent fulfill and decline operations not to overwrite append-only facts

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`a05b6d3`](https://github.com/ImmortalDemonGod/money-agent/tree/a05b6d356b9af6bcb9f3e28d00951758f7861817))

- [`bin/human.py#L38`](https://github.com/ImmortalDemonGod/money-agent/blob/a05b6d356b9af6bcb9f3e28d00951758f7861817/bin/human.py#L38)
- [`bin/human.py#L55`](https://github.com/ImmortalDemonGod/money-agent/blob/a05b6d356b9af6bcb9f3e28d00951758f7861817/bin/human.py#L55)
- [`bin/human.py#L162-L200`](https://github.com/ImmortalDemonGod/money-agent/blob/a05b6d356b9af6bcb9f3e28d00951758f7861817/bin/human.py#L162-L200)

### Class A (Execution Evidence)

**Per-symbol test coverage (AST analysis):**

- **`_publish_resolution`** (L38): FAIL -- WARNING: No tests import or call `_publish_resolution`

**Coverage summary:** 0/1 symbols verified by tests.

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
dfe3ff8 test(pr50): pin final review failure modes
d52a400 test(rails): expand fail-closed registry catalog
710e1c0 merge(stack): sync rewritten stack 3 ancestry
618e3eb merge(stack): integrate reviewed stack 3 advances
4ff597e test(delivery): cover content-type refusal
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | Concurrent operator resolutions share a verifier-private int... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 1 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), AST symbol-to-test binding (0/1 symbols verified), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Lock the complete human resolution publication transaction

# AIV Evidence File (v1.0)

**File:** `bin/prereg.py`
**Commit:** `e620ea8`
**Generated:** 2026-07-22T22:40:03Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R2
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "bin/prereg.py"
  classification_rationale: "Preregistration is an integrity control with component-level adjudication blast radius, meeting AIV section 5.3 R2"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T22:40:03Z"
```

## Claim(s)

1. Concurrent first writers expose one complete immutable preregistration record
2. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/51#discussion_r3634224786](https://github.com/ImmortalDemonGod/money-agent/pull/51#discussion_r3634224786)
- **Requirements Verified:** CodeRabbit requires atomic first-write publication without truncated-reader windows

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`e620ea8`](https://github.com/ImmortalDemonGod/money-agent/tree/e620ea8a8289bfe55853fa186b64caa00546cd89))

- [`bin/prereg.py#L24`](https://github.com/ImmortalDemonGod/money-agent/blob/e620ea8a8289bfe55853fa186b64caa00546cd89/bin/prereg.py#L24)
- [`bin/prereg.py#L56-L73`](https://github.com/ImmortalDemonGod/money-agent/blob/e620ea8a8289bfe55853fa186b64caa00546cd89/bin/prereg.py#L56-L73)

### Class A (Execution Evidence)

**Per-symbol test coverage (AST analysis):**

- **`freeze`** (L24): FAIL -- WARNING: No tests import or call `freeze`

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
1c0d6f2 test(sim): adversarially cover PR 51 hardening
a3d4a5a test(v3): cover adversarial enforcement seams
937c8d6 [S11] P-generalizations: prereg, decision gate, obligations+watchdog, probe registry, exposure caps
7b7a7fe [S10] V3 spine: per-lane stage ordering, config-gated off (the contested layer, by explicit switch)
644f13c [S9] V3 typed bet-spec + action authorization, config-gated off (bet-ledger layer)
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | Concurrent first writers expose one complete immutable prere... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 1 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), AST symbol-to-test binding (0/1 symbols verified), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Write, fsync, and atomically link complete preregistration records

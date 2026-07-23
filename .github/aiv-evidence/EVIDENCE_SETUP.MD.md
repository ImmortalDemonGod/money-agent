# AIV Evidence File (v1.0)

**File:** `SETUP.md`
**Commit:** `d060b27`
**Previous:** `ae81911`
**Generated:** 2026-07-22T23:36:45Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "SETUP.md"
  classification_rationale: "The marker is part of the payment rail go/no-go procedure"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T23:36:45Z"
```

## Claim(s)

1. The runbook provides the exact seven-check marker schema bound to current Base settlement configuration
2. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/50#discussion_r3634578703](https://github.com/ImmortalDemonGod/money-agent/pull/50#discussion_r3634578703)
- **Requirements Verified:** Operators need an enforceable handoff from live acceptance to scored-run enablement

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`d060b27`](https://github.com/ImmortalDemonGod/money-agent/tree/d060b27cd13984b2d1cec1e03952294cadd05f98))

- [`SETUP.md#L129`](https://github.com/ImmortalDemonGod/money-agent/blob/d060b27cd13984b2d1cec1e03952294cadd05f98/SETUP.md#L129)
- [`SETUP.md#L237-L254`](https://github.com/ImmortalDemonGod/money-agent/blob/d060b27cd13984b2d1cec1e03952294cadd05f98/SETUP.md#L237-L254)

### Class A (Execution Evidence)

**WARNING:** No tests found that directly import or reference the changed file.
This file has no claim-specific execution evidence.

### Code Quality (Linting & Types)

- **ruff:** All checks passed
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
d060b27 test(rails): call monetary validator directly
5f37af2 test(supervisor): model live verifier process explicitly
dfe3ff8 test(pr50): pin final review failure modes
d52a400 test(rails): expand fail-closed registry catalog
710e1c0 merge(stack): sync rewritten stack 3 ancestry
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | Claim 1 (see Claim(s)) | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | Claim 2 (see Claim(s)) | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 1 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), pytest (no claim-specific tests found), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Document the enforced Base acceptance artifact

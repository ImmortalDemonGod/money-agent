# AIV Evidence File (v1.0)

**File:** `CLAUDE.md`
**Commit:** `bcf1f1a`
**Generated:** 2026-07-22T23:11:02Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "CLAUDE.md"
  classification_rationale: "R3 because this changes the highest-priority policy governing payment acceptance and post-payment liability"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T23:11:02Z"
```

## Claim(s)

1. The constitution permits deferred delivery only with a fresh verifier enablement fact, refund authority, positive caps, a typed restricted oracle, and a bounded deadline
2. The agent still stops at first dollar while the out-of-band verifier continues until every liability is fulfilled or refunded
3. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/51](https://github.com/ImmortalDemonGod/money-agent/pull/51)
- **Requirements Verified:** The operator explicitly authorized the constitutional amendment that the PR 51 safety layer was designed to support

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`bcf1f1a`](https://github.com/ImmortalDemonGod/money-agent/tree/bcf1f1a03f4276eef6df0be44b53f058fa5b96ec))

- [`CLAUDE.md#L33-L41`](https://github.com/ImmortalDemonGod/money-agent/blob/bcf1f1a03f4276eef6df0be44b53f058fa5b96ec/CLAUDE.md#L33-L41)

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
6763b83 test(sim): exercise verifier-authorized obligations
512f388 test(obligations): cover guarded authorization contract
30612e5 test(sim): exercise CodeRabbit review invariants
76c1bec test(v3): cover CodeRabbit hardening findings
bb5cbed test(sim): adversarially cover PR 51 hardening
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | The constitution permits deferred delivery only with a fresh... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | The agent still stops at first dollar while the out-of-band ... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 3 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 2 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), pytest (no claim-specific tests found), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Adopt the mechanically guaranteed delivery exception without weakening default-off behavior

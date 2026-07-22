# AIV Evidence File (v1.0)

**File:** `SETUP.md`
**Commit:** `68b46db`
**Previous:** `4f7a8e4`
**Generated:** 2026-07-22T23:05:35Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "SETUP.md"
  classification_rationale: "Omitted runbook steps could make safe code unsafe in deployment"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T23:05:35Z"
```

## Claim(s)

1. Operators are instructed to verify chain, event uniqueness, authorization, live funding, and signed human resolution prerequisites before scoring
2. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/issues/31](https://github.com/ImmortalDemonGod/money-agent/issues/31)
- **Requirements Verified:** Issue acceptance depends on operator-visible provisioning and live acceptance boundaries

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`68b46db`](https://github.com/ImmortalDemonGod/money-agent/tree/68b46dbf59a91cce058bc728a83838d5fdb70f5b))

- [`SETUP.md#L207-L214`](https://github.com/ImmortalDemonGod/money-agent/blob/68b46dbf59a91cce058bc728a83838d5fdb70f5b/SETUP.md#L207-L214)
- [`SETUP.md#L227-L229`](https://github.com/ImmortalDemonGod/money-agent/blob/68b46dbf59a91cce058bc728a83838d5fdb70f5b/SETUP.md#L227-L229)
- [`SETUP.md#L232-L235`](https://github.com/ImmortalDemonGod/money-agent/blob/68b46dbf59a91cce058bc728a83838d5fdb70f5b/SETUP.md#L232-L235)
- [`SETUP.md#L243-L248`](https://github.com/ImmortalDemonGod/money-agent/blob/68b46dbf59a91cce058bc728a83838d5fdb70f5b/SETUP.md#L243-L248)
- [`SETUP.md#L250-L253`](https://github.com/ImmortalDemonGod/money-agent/blob/68b46dbf59a91cce058bc728a83838d5fdb70f5b/SETUP.md#L250-L253)
- [`SETUP.md#L256-L261`](https://github.com/ImmortalDemonGod/money-agent/blob/68b46dbf59a91cce058bc728a83838d5fdb70f5b/SETUP.md#L256-L261)

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
68b46db test(sim): isolate AIV edge fixture state
bc601c3 test(rails): expose registry contract to verification
86e664c test(pr50): exercise executable rail and queue contracts
67e9adb test(pr50): pin issue-closure trust boundaries
c5fd8f6 docs(tests): normalize bug-catalog whitespace
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | Operators are instructed to verify chain, event uniqueness, ... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 1 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), pytest (no claim-specific tests found), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Document mandatory trust and live acceptance conditions

# AIV Evidence File (v1.0)

**File:** `tests/sim.sh`
**Commit:** `55dc2f1`
**Previous:** `6763b83`
**Generated:** 2026-07-22T23:14:23Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: "tests/sim.sh"
  classification_rationale: "R3 integration evidence because the fixture crosses payment authorization and refund binding"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T23:14:23Z"
```

## Claim(s)

1. The enabled two-lane registration fixture supplies a concrete refundable Stripe charge identifier
2. The fixture still reaches the grounded received-funds cap rather than failing authorization
3. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/51](https://github.com/ImmortalDemonGod/money-agent/pull/51)
- **Requirements Verified:** Integration evidence for deferred liability must include the refund target required by the runtime contract

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`55dc2f1`](https://github.com/ImmortalDemonGod/money-agent/tree/55dc2f144f45afcb8480d0e01b38be1dd45f2b86))

- [`tests/sim.sh#L429-L430`](https://github.com/ImmortalDemonGod/money-agent/blob/55dc2f144f45afcb8480d0e01b38be1dd45f2b86/tests/sim.sh#L429-L430)

### Class A (Execution Evidence)

**WARNING:** No tests found that directly import or reference the changed file.
This file has no claim-specific execution evidence.

### Code Quality (Linting & Types)

- **ruff:** 23957 error(s)
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
55dc2f1 test(obligations): reject unbound refund liabilities
6763b83 test(sim): exercise verifier-authorized obligations
512f388 test(obligations): cover guarded authorization contract
30612e5 test(sim): exercise CodeRabbit review invariants
76c1bec test(v3): cover CodeRabbit hardening findings
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | The enabled two-lane registration fixture supplies a concret... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | The fixture still reaches the grounded received-funds cap ra... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 3 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 2 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), pytest (no claim-specific tests found), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Keep the verifier-authorized simulation aligned with mandatory charge binding

# AIV Evidence File (v1.0)

**File:** `.github/aiv-packets/PACKET_mechanically_guaranteed_obligations.md`
**Commit:** `5f93a7f`
**Generated:** 2026-07-22T23:24:03Z
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: ".github/aiv-packets/PACKET_mechanically_guaranteed_obligations.md"
  classification_rationale: "R3 because this packet verifies payment liability, refund authority, and the protected facts boundary"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T23:24:03Z"
```

## Claim(s)

1. The aggregate packet classifies the payment and refund authorization change as R3
2. The aggregate packet records exact behavioral counts, differential results, immutable intent, and atomic provenance
3. No existing tests were modified or deleted during this change.

---

## Evidence

### Class E (Intent Alignment)

- **Link:** [https://github.com/ImmortalDemonGod/money-agent/pull/51](https://github.com/ImmortalDemonGod/money-agent/pull/51)
- **Requirements Verified:** The generated aggregate must accurately describe the critical surfaces and evidence for the adopted obligation behavior

### Class B (Referential Evidence)

**Scope Inventory** (SHA: [`5f93a7f`](https://github.com/ImmortalDemonGod/money-agent/tree/5f93a7f6aae604912362e2745205c62d3e19d181))

- [`.github/aiv-packets/PACKET_mechanically_guaranteed_obligations.md#L7`](https://github.com/ImmortalDemonGod/money-agent/blob/5f93a7f6aae604912362e2745205c62d3e19d181/.github/aiv-packets/PACKET_mechanically_guaranteed_obligations.md#L7)
- [`.github/aiv-packets/PACKET_mechanically_guaranteed_obligations.md#L18-L20`](https://github.com/ImmortalDemonGod/money-agent/blob/5f93a7f6aae604912362e2745205c62d3e19d181/.github/aiv-packets/PACKET_mechanically_guaranteed_obligations.md#L18-L20)
- [`.github/aiv-packets/PACKET_mechanically_guaranteed_obligations.md#L22-L27`](https://github.com/ImmortalDemonGod/money-agent/blob/5f93a7f6aae604912362e2745205c62d3e19d181/.github/aiv-packets/PACKET_mechanically_guaranteed_obligations.md#L22-L27)
- [`.github/aiv-packets/PACKET_mechanically_guaranteed_obligations.md#L33-L40`](https://github.com/ImmortalDemonGod/money-agent/blob/5f93a7f6aae604912362e2745205c62d3e19d181/.github/aiv-packets/PACKET_mechanically_guaranteed_obligations.md#L33-L40)
- [`.github/aiv-packets/PACKET_mechanically_guaranteed_obligations.md#L65-L85`](https://github.com/ImmortalDemonGod/money-agent/blob/5f93a7f6aae604912362e2745205c62d3e19d181/.github/aiv-packets/PACKET_mechanically_guaranteed_obligations.md#L65-L85)
- [`.github/aiv-packets/PACKET_mechanically_guaranteed_obligations.md#L112-L152`](https://github.com/ImmortalDemonGod/money-agent/blob/5f93a7f6aae604912362e2745205c62d3e19d181/.github/aiv-packets/PACKET_mechanically_guaranteed_obligations.md#L112-L152)
- [`.github/aiv-packets/PACKET_mechanically_guaranteed_obligations.md#L167-L173`](https://github.com/ImmortalDemonGod/money-agent/blob/5f93a7f6aae604912362e2745205c62d3e19d181/.github/aiv-packets/PACKET_mechanically_guaranteed_obligations.md#L167-L173)
- [`.github/aiv-packets/PACKET_mechanically_guaranteed_obligations.md#L179-L181`](https://github.com/ImmortalDemonGod/money-agent/blob/5f93a7f6aae604912362e2745205c62d3e19d181/.github/aiv-packets/PACKET_mechanically_guaranteed_obligations.md#L179-L181)

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
167bd21 test(sim): bind obligation fixture to charge
55dc2f1 test(obligations): reject unbound refund liabilities
6763b83 test(sim): exercise verifier-authorized obligations
512f388 test(obligations): cover guarded authorization contract
30612e5 test(sim): exercise CodeRabbit review invariants
```

## Claim Verification Matrix

| # | Claim | Type | Evidence | Verdict |
|---|-------|------|----------|---------|
| 1 | The aggregate packet classifies the payment and refund autho... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 2 | The aggregate packet records exact behavioral counts, differ... | unresolved | No automatic binding available | REVIEW MANUAL REVIEW |
| 3 | No existing tests were modified or deleted during this chang... | structural | Class C: all structural indicators clean | PASS VERIFIED |

**Verdict summary:** 1 verified, 0 unverified, 2 manual review.
---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence collected by `aiv commit` running: git diff (scope inventory), pytest (no claim-specific tests found), anti-cheat scan.
Ruff/mypy results are in Code Quality (not Class A) because they prove syntax/types, not behavior.

---

## Summary

Replace generator placeholders with the complete guarded-obligation evidence record

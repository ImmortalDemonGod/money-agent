# AIV Verification Packet (v2.2)

## Identification

| Field | Value |
|-------|-------|
| **Repository** | github.com/ImmortalDemonGod/aiv-protocol |
| **Change ID** | pr51-coderabbit-hardening |
| **Commits** | `6094793`, `91117d1`, `633a768`, `e620ea8`, `6e00c83`, `5df105e`, `8e1e2ed`, `5859e77`, `503246e`, `0c4e5b8`, `50bd5ea` |
| **Head SHA** | `50bd5ea` |
| **Base SHA** | `7ad2be1` |
| **Created** | 2026-07-22T22:43:40Z |

## Classification

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: []
  blast_radius: component
  classification_rationale: "The logical unit changes payment obligations, refund cleanup, outbound PII authorization, durable audit logging, and verifier trust controls; AIV section 5.2 requires R3"
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-22T22:43:40Z"
```

## Claims

1. Concurrent bet mutations cannot consume one reservation twice
2. Typed bet outcomes require and persist evaluation of their declared condition
3. No existing tests were modified or deleted during this change.
4. Two concurrent consumers cannot both spend one action reservation
5. A pre-attempt failure can compensate its bound reservation without changing lanes
6. Audit persistence failures roll back a just-consumed bound send reservation
7. SENT_LOG records an unconfirmed SMTP attempt rather than claiming delivery
8. Decision records authorize only when parsed class and body fields exactly match the request
9. Concurrent first writers expose one complete immutable preregistration record
10. Raising exposure environment variables cannot register post-payment work
11. Every attempted deferred paid offer is durably recorded in REFUSALS.md
12. The agent cannot claim fulfillment of a deliver-later obligation
13. Focused tests reproduce and prevent double reservation consumption
14. Focused tests bind mail consume, rollback, lane, bet, and audit ordering
15. Focused tests reject substring decisions, self-graded typed outcomes, and deferred paid work
16. The two-clone simulation rejects substring authorization and all deferred obligation registration
17. Typed resolution fixtures emit observable metric values for declared-condition evaluation
18. The improvement record states that environment caps cannot relax deliver-in-full-at-payment
19. Spine evidence names the focused test file already cited by Class A
20. Obligation evidence names the focused refusal test already cited by Class A

---

## Evidence References

| # | Evidence File | Commit SHA | Classes |
|---|---------------|------------|---------|
| 1 | EVIDENCE_BIN_BETS.md | `6094793` | A, B, C, E, F |
| 2 | EVIDENCE_BIN_BET_GATE.md | `91117d1` | A, B, C, E, F |
| 3 | EVIDENCE_BIN_MAIL.md | `633a768` | A, B, C, E, F |
| 4 | EVIDENCE_BIN_DECISION_GATE.md | `e620ea8` | A, B, C, E, F |
| 5 | EVIDENCE_BIN_PREREG.md | `6e00c83` | A, B, C, E, F |
| 6 | EVIDENCE_BIN_OBLIGATIONS.md | `5df105e` | A, B, C, E, F |
| 7 | EVIDENCE_TESTS_TEST_V3_HARDENING.md | `8e1e2ed` | A, B, C, E, F |
| 8 | EVIDENCE_TESTS_SIM.SH.md | `5859e77` | A, B, C, E, F |
| 9 | EVIDENCE_IMPROVEMENT_LOG.MD.md | `503246e` | A, B, C, E, F |
| 10 | EVIDENCE_.GITHUB_AIV_EVIDENCE_EVIDENCE_BIN_SPINE.MD.md | `0c4e5b8` | A, B, E |
| 11 | EVIDENCE_.GITHUB_AIV_EVIDENCE_EVIDENCE_BIN_OBLIGATIONS.MD.md | `50bd5ea` | A, B, E |

### Class E (Intent Alignment)

- **Requirement:** Resolve every actionable finding from CodeRabbit review 4759249208 on PR 51

### Class B (Referential Evidence)

**Scope Inventory** (from 50 file references across evidence files)

- `bin/bets.py#L32`
- `bin/bets.py#L34`
- `bin/bets.py#L37`
- `bin/bets.py#L42`
- `bin/bets.py#L60`
- `bin/bets.py#L66`
- `bin/bets.py#L84-L115`
- `bin/bets.py#L195-L212`
- `bin/bets.py#L250-L257`
- `bin/bets.py#L262-L273`
- `bin/bets.py#L282-L288`
- `bin/bets.py#L290-L291`
- `bin/bets.py#L293-L297`
- `bin/bets.py#L299-L345`
- `bin/bets.py#L353-L356`
- `bin/bets.py#L359-L360`
- `bin/bet_gate.py#L38`
- `bin/bet_gate.py#L127-L140`
- `bin/bet_gate.py#L142-L151`
- `bin/bet_gate.py#L157-L180`
- `bin/mail.py#L36`
- `bin/mail.py#L196-L216`
- `bin/mail.py#L225-L231`
- `bin/mail.py#L242`
- `bin/mail.py#L258-L259`
- `bin/decision_gate.py#L51-L56`
- `bin/prereg.py#L24`
- `bin/prereg.py#L56-L73`
- `bin/obligations.py#L2-L8`
- `bin/obligations.py#L53-L65`
- `bin/obligations.py#L68-L71`
- `bin/obligations.py#L73-L75`
- `bin/obligations.py#L79-L81`
- `tests/test_v3_hardening.py#L7-L9`
- `tests/test_v3_hardening.py#L21`
- `tests/test_v3_hardening.py#L63-L68`
- `tests/test_v3_hardening.py#L77`
- `tests/test_v3_hardening.py#L91-L110`
- `tests/test_v3_hardening.py#L126-L182`
- `tests/test_v3_hardening.py#L186`
- `tests/test_v3_hardening.py#L188`
- `tests/test_v3_hardening.py#L238-L266`
- `tests/sim.sh#L259`
- `tests/sim.sh#L283`
- `tests/sim.sh#L292`
- `tests/sim.sh#L369-L372`
- `tests/sim.sh#L388-L395`
- `IMPROVEMENT_LOG.md#L1445-L1451`
- `.github/aiv-evidence/EVIDENCE_BIN_SPINE.md#L70-L72`
- `.github/aiv-evidence/EVIDENCE_BIN_OBLIGATIONS.md#L80-L82`

---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence was collected by `aiv commit` during the change lifecycle.
Packet generated by `aiv close`.

---

## Known Limitations

- Evidence references point to Layer 1 evidence files at specific commit SHAs.
  Use `git show <sha>:.github/aiv-evidence/<file>` to retrieve.

---

## Summary

Change 'pr51-coderabbit-hardening': 11 commit(s) across 11 file(s).

# AIV Verification Packet (v2.2)

## Identification

| Field | Value |
|-------|-------|
| **Repository** | github.com/ImmortalDemonGod/money-agent |
| **Change ID** | mechanically-guaranteed-obligations |
| **Commits** | `d859a60`, `a024bb0`, `512f388`, `6763b83`, `d8adf3b`, `bcf1f1a`, `9d56125`, `7f3be9e`, `f6084e3`, `c085827`, `55dc2f1`, `167bd21`, `72b8c7c`, `bd1e7a8`, `6cc1a28`, `3b8b421` |
| **Head SHA** | `3b8b421` |
| **Base SHA** | `29226cc` |
| **Created** | 2026-07-22T23:22:46Z |

## Classification

```yaml
classification:
  risk_tier: R3
  sod_mode: S1-with-section-10-waiver
  critical_surfaces: [payments, refunds, operator authorization, verifier trust boundary, audit logging]
  blast_radius: component
  classification_rationale: >
    AIV section 5.2 makes this R3 because it changes when the agent may create post-payment
    liability, how a verifier-held refund credential authorizes that behavior, and which protected
    facts cross the privilege boundary. The repository's PR-51 packet establishes the section 10
    operator-plus-AI waiver convention; independent human merge review remains required.
  classified_by: "Miguel Ingram (Author) + Codex (AI Verifier, section 10 waiver)"
  classified_at: "2026-07-22T23:22:46Z"
```

## Claims

1. Deferred fulfillment is permitted only when a fresh grounded verifier fact proves explicit
   enablement, refund authority, positive exposure caps, and a maximum deadline.
2. Agent-local environment variables cannot activate or widen obligation authority.
3. Concurrent registrations cannot jointly exceed verifier-published caps.
4. Every accepted liability binds a concrete refundable Stripe charge, and agent fulfillment
   evidence remains unverified until the restricted verifier oracle passes.
5. The constitution preserves instant delivery as the default while expressly authorizing only
   this mechanically guaranteed exception.

---

## Evidence References

| # | Evidence File | Commit SHA | Classes |
|---|---------------|------------|---------|
| 1 | EVIDENCE_BIN_OBLIGATIONS.md | `d859a60` | A, B, C, E, F |
| 2 | EVIDENCE_BIN_OBLIGATION_WATCH.md | `a024bb0` | A, B, C, E, F |
| 3 | EVIDENCE_TESTS_TEST_V3_HARDENING.md | `512f388` | A, B, C, E, F |
| 4 | EVIDENCE_TESTS_SIM.SH.md | `6763b83` | A, B, C, E, F |
| 5 | EVIDENCE_DOCS_V2_HARNESS_DESIGN.MD.md | `d8adf3b` | A, B, C, E, F |
| 6 | EVIDENCE_.ENV.EXAMPLE.md | `bcf1f1a` | A, B, C, E, F |
| 7 | EVIDENCE_CLAUDE.MD.md | `9d56125` | A, B, C, E, F |
| 8 | EVIDENCE_SETUP.MD.md | `7f3be9e` | A, B, C, E, F |
| 9 | EVIDENCE_IMPROVEMENT_LOG.MD.md | `f6084e3` | A, B, C, E, F |
| 10 | EVIDENCE_BIN_OBLIGATIONS.md | `c085827` | A, B, C, E, F |
| 11 | EVIDENCE_TESTS_TEST_V3_HARDENING.md | `55dc2f1` | A, B, C, E, F |
| 12 | EVIDENCE_TESTS_SIM.SH.md | `167bd21` | A, B, C, E, F |
| 13 | EVIDENCE_CLAUDE.MD.md | `72b8c7c` | A, B, C, E, F |
| 14 | EVIDENCE_SETUP.MD.md | `bd1e7a8` | A, B, C, E, F |
| 15 | EVIDENCE_DOCS_V2_HARNESS_DESIGN.MD.md | `6cc1a28` | A, B, C, E, F |
| 16 | EVIDENCE_IMPROVEMENT_LOG.MD.md | `3b8b421` | A, B, C, E, F |

### Class A (Execution Evidence)

Executed against committed head `3b8b421be79789fcf956cfc769bb13cbbc1a6bbb` on macOS/Python 3:

| Command | Pass | Fail | Skip | Result |
|---|---:|---:|---:|---|
| `pytest -q tests/test_v3_hardening.py` | 17 | 0 | 0 | PASS |
| `bash tests/sim.sh` | 114 | 0 | 0 | PASS |
| `bash tests/corpus.sh` | 11 | 0 | 0 | PASS |
| `python3 -m compileall -q bin tests/test_v3_hardening.py` | 1 | 0 | 0 | PASS |
| scoped Ruff | 1 | 0 | 0 | PASS |
| `shellcheck tests/sim.sh bin/*.sh` | 1 | 0 | 0 | PASS |
| `git diff --check` | 1 | 0 | 0 | PASS |

Focused obligation tests: `test_obligation_authorization_requires_fresh_grounded_verifier_fact`,
`test_obligation_watch_authorization_requires_every_safeguard`,
`test_obligation_watch_checks_open_records_without_agent_claim`,
`test_obligation_registration_uses_verifier_caps_and_serializes`,
`test_obligation_deadline_cap_and_fulfillment_claim_are_not_self_certifying`, and
`test_obligation_watch_rejects_shell_and_idempotently_refunds`.



### Class B (Referential Evidence)

**Scope Inventory** (from 19 file references across evidence files)

- `bin/obligations.py#L133-L136`
- `bin/obligations.py#L179`
- `bin/obligation_watch.py#L2-L8`
- `bin/obligation_watch.py#L27`
- `bin/obligation_watch.py#L75-L113`
- `bin/obligation_watch.py#L117-L119`
- `bin/obligation_watch.py#L129-L130`
- `bin/obligation_watch.py#L161-L168`
- `bin/obligation_watch.py#L185`
- `bin/obligation_watch.py#L187-L189`
- `bin/obligation_watch.py#L191`
- `bin/obligation_watch.py#L193`
- `tests/test_v3_hardening.py#L298-L300`
- `tests/sim.sh#L429-L430`
- `docs/V2_HARNESS_DESIGN.md#L805-L807`
- `.env.example#L32-L42`
- `CLAUDE.md#L37-L39`
- `SETUP.md#L129-L130`
- `IMPROVEMENT_LOG.md#L1448-L1450`

### Class C (Negative Evidence)

- `rg -n 'os\.environ|getenv\(' bin/obligations.py` returns no matches: authorization cannot fall
  back to agent-local environment state.
- Focused tests reject ungrounded, stale, disabled, unprovisioned, non-finite, deadline-exceeding,
  and charge-unbound registrations.
- The restricted completion oracle rejects arbitrary shell text; refund requests use a stable
  obligation-scoped idempotency key.

### Class D (Differential Evidence)

| Boundary | Parent `29226cc` | Final behavior |
|---|---|---|
| Authorization | Refused every post-payment obligation. | Fresh verifier enablement plus every safeguard permits bounded registration. |
| Config ownership | Original PR read caps from the agent process. | Verifier publishes the only accepted caps and deadline. |
| Concurrency | Unlocked load/check/save could overrun caps. | One file-lock transaction covers evaluation and append. |
| Fulfillment | Hardening disabled all claims. | Claims are allowed but never self-certify; verifier checks open records independently. |
| Refund target | `charge_id` could be absent. | Registration requires a concrete `ch_...` target. |

The first differential run executed the new simulation assertions against parent `29226cc`: 111
passed and exactly the three new authorization assertions failed. Against the committed runtime,
the same matrix passed 114/114.

### Class E (Intent Alignment)

- Immutable intent: [V2 design §15.2 at parent `29226cc`](https://github.com/ImmortalDemonGod/money-agent/blob/29226cc090679296d15f4c9d8174a70db8749553/docs/V2_HARNESS_DESIGN.md#L791-L810)
  preregistered the exact amendment: delivery is instant or mechanically guaranteed by an
  out-of-band watchdog holding refund authority.
- [PR 51](https://github.com/ImmortalDemonGod/money-agent/pull/51) received the operator's explicit
  2026-07-22 direction to adopt that amendment rather than leave its safety layer inert.

### Class F (Provenance Evidence)

- Runtime: `d859a60`, `a024bb0`, `c085827`.
- Focused regressions: `512f388`, `55dc2f1`.
- Protected two-lane regressions: `6763b83`, `167bd21`.
- Policy and provisioning: `d8adf3b`, `bcf1f1a`, `9d56125`, `7f3be9e`, `f6084e3`, `72b8c7c`,
  `bd1e7a8`, `6cc1a28`, `3b8b421`.
- No test was deleted or skipped. Class G is omitted because no black-box prediction was
  preregistered; reconstructing one post hoc would be verification theater.

---

## Verification Methodology

**Zero-Touch Mandate:** Verifier inspects artifacts only.
Evidence was collected by `aiv commit` during the change lifecycle.
Packet generated by `aiv close`.

---

## Known Limitations

- Evidence references point to Layer 1 evidence files at specific commit SHAs.
  Use `git show <sha>:.github/aiv-evidence/<file>` to retrieve.
- Presence of a refund credential proves provisioning, not provider availability. A failed live
  refund remains a breach/halt requiring manual remediation.
- Protected-ledger provisioning is the privilege wall; weak-mode committed facts remain a
  tripwire. Independent natural-person S1 review remains required before merge.
- Repository-wide mypy reports pre-existing findings in `bin/spine.py`, `bin/bets.py`, and
  `bin/bet_gate.py`, plus a missing local pytest stub. Scoped mypy for both runtime modules passed;
  Ruff, compilation, ShellCheck, and every behavioral suite are clean.

---

## Summary

R3 change `mechanically-guaranteed-obligations`: 16 atomic AIV commits across nine files. Deferred
delivery is useful only inside a fresh verifier-owned, bounded, charge-bound, refund-backed
exception, and fulfillment remains independently verified.

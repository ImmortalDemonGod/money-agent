# AIV Verification Packet (v2.1)

**Commit:** `bin/guard.py` (`_mode_mismatch`)
**Protocol:** AIV v2.0 + Addendum 2.7

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: [payments]
  blast_radius: "Without this the agent spends real money against a fake till: guaranteed total
    loss of the cap with zero possible upside, and every other check reports healthy."
  classification_rationale: "R3: payments. This is the only check standing between a live card
    and an unwinnable run."
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-16T06:35:00Z"
```

## Claim(s)

1. `guard.py` halts when a live spend rail is paired with a test-mode receive rail.
2. It does NOT halt on live+live, nor on test+no-card (a legitimate dry run).

## Evidence

### Class A (Execution)

```
live card + rk_test_ Stripe -> HALT exit 1
   "LIVE card + TEST-MODE Stripe. The agent would spend REAL money and could only
    ever receive FAKE money. Unwinnable by construction."
rk_live_ + live card        -> no mismatch (proceeds)
rk_test_ + no card          -> no mismatch (safe dry run)
```

### Class C (Negative -- regressions absent)

- **The two negative controls are the whole packet.** A guard that halts unconditionally would
  also produce the HALT above and be worthless. Both permissive cases were asserted explicitly.
- No other check catches this state: `pnl.py` verifies, both API pulls succeed, `truth.json` reads
  healthy. **Nothing is broken -- the two halves are simply in different universes.** That is why
  it needed a dedicated check rather than falling out of existing validation.

### Class B (Referential)

- `bin/guard.py::_mode_mismatch`, called first in `main()` before any ledger read.

### Class D (Differential)

- `guard.py`: ledger-state checks only -> environment-coherence check FIRST, then ledger state.

### Class E (Intent)

- `CONSTITUTION.md` hard bound 1: "The card balance is fixed and cannot be topped up." A run that
  can only lose money violates the spirit of a bounded experiment: the cap exists to bound a real
  attempt, not to fund a guaranteed loss.

### Class F (Provenance)

- Detection is on key prefixes (`_live_` vs `_test_`), which are Stripe-assigned and cannot be
  spoofed by config. Privacy.com liveness is inferred from a key being present at all, because
  Privacy has no test mode -- **that asymmetry is the root cause and is documented in the code.**

## Honest limitations

1. **Infers Privacy liveness from key presence.** If Privacy ever ships a test mode, this
   over-triggers. Acceptable: it fails safe (halts), not open.
2. **Does not check the AGENT's key mode** -- `.env.agent` is not read by the verifier by design
   (SoD). A live-verifier / test-agent split would not be caught here. Mitigated because both
   Stripe keys come from the same dashboard mode in practice, but it is a real gap.
3. **Test/test is permitted and is NOT a valid experiment.** It is a safe dry run of the harness.
   In test mode no real customer can pay, so `received_usd` stays 0 and the frozen prediction
   would be "confirmed" for the wrong reason. **The guard cannot catch that** -- it is a research
   design error, not a config error. Named here so it is not silently green.
4. **Same-author packet.**

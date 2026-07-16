# AIV Verification Packet (v2.1)

**Commit:** `bin/pnl.py`, `bin/guard.py`, `.env.example` (issuer_enforced spend mode)
**Protocol:** AIV v2.0 + Addendum 2.7

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: [payments, audit_logs]
  blast_radius: "Changes how spend is accounted and how the cap is enforced. A wrong call here
    either lets the agent overspend or reports a losing run as profitable."
  classification_rationale: "R3: payments + audit logs, same tier as the harness it modifies."
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-16T05:50:00Z"
```

## Claim(s)

1. When no card feed exists, `pnl.py` reports `spent_usd: null` and `net_usd: null` rather than
   `0`, so an unmeasured cost can never be rendered as profit.
2. `guard.py` permits the loop under `cap_enforced_by: card_issuer` while still halting on an
   unverified ledger and on an exhausted cap in counted mode.
3. The experiment stays decidable without spend accounting, because the `PREDICTION.md` falsifier
   is `received_usd > 0`, which does not depend on spend.

## Evidence

### Class E (Intent Alignment)

- `PREDICTION.md` @ tag `prediction-frozen`: *"The prediction dies if
  `ledger/truth.json.received_usd > 0` with `verified: true`."* Spend is not in the falsifier.
- Operator constraint (2026-07-16): "$25 spend limit, $50 total, I have the card details." The card
  has no API, so real-time spend counting is unavailable.

### Class A (Execution Evidence)

Live against the real (test-mode) Stripe account:

```
verified=True errors=[] received_usd=0.0
spent_usd=None  spend_measured=False  spend_source=issuer_enforced_uncounted
net_usd=None    cap_usd=25.0          cap_enforced_by=card_issuer
made_money=False  net_positive=False
guard.py -> exit 0, prints "spent=UNCOUNTED net=UNCOMPUTABLE"
```

### Class C (Negative Evidence -- regressions absent)

The new pass-path did not soften the halts. Both re-tested after the change:

| Injected state | guard exit | Verdict |
|---|---|---|
| `verified:false` | 1 | HALT, correct |
| counted mode, `cap_remaining:0` | 2 | HALT, correct |

Without these, claim 2 would be vacuous: a guard that permits everything also "permits the loop."

### Class B (Referential Evidence)

- `bin/pnl.py`: three-mode spend block (`privacy_api` / `manual_csv` / `issuer_enforced_uncounted`).
- `bin/guard.py`: `cap_enforced_by == card_issuer` early-return.
- `.env.example`: documents `CARD_SOURCE=issuer_enforced`.

### Class D (Differential Evidence)

- `spent_usd`: `0.0` (assumed) -> `null` (honest). **This is the whole change.**
- `net_usd`: `received - 0` -> `null` when spend is unmeasured.
- `made_money`: was `net > 0` (uncomputable without spend) -> `received > 0` (the actual falsifier).
- New fields: `spend_source`, `spend_measured`, `cap_enforced_by`, `net_positive`.

### Class F (Provenance)

- First real Stripe pull anchored: `MANIFEST.sha256` =
  `7ee8891e0ae5c2a2a7d4b010ef586bb70912b12a55e31fe1d9869ac2a12cdb61`.
- `STRIPE_READ_KEY` permissions probed against the live API, not assumed: `balance_transactions`
  GRANTED, `products` POST **DENIED**. Correctly scoped for a verifier.

## Honest limitations

1. **Spend is genuinely unknown during the run.** The cap is real (the card declines), but net P&L
   cannot be computed until a statement is exported. A run can end `received=0, spent=?` and the
   only honest answer to "how much did it lose" is "up to $25, export the statement."
2. **`made_money: true` no longer implies profitable.** It means money *arrived*. `net_positive` is
   the profitability field and is `null`-guarded. Do not conflate them in the retro.
3. **Still no live *money-detection* test.** `received_usd` has only ever been observed as `0.0`. A
   test payment (card `4242...`) would close this. **This remains the last unproven path.**
4. **Same-author packet.** Needs an independent reviewer.

# AIV Verification Packet (v2.1)

**Commit:** readiness gate -- every path exercised against live Stripe + Privacy
**Protocol:** AIV v2.0 + Addendum 2.7

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: [payments, audit_logs, autonomous_execution]
  blast_radius: "Certifies the harness as fit to run unsupervised with a real card. A false PASS
    here means an agent runs all night against a ledger that cannot see money."
  classification_rationale: "R3: payments + audit logs. This packet IS the go/no-go."
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-16T06:20:00Z"
```

## Claim(s)

1. The verifier **detects arriving money**: `received_usd` moved 0.0 -> 5.00 on a real test charge.
2. The verifier **accounts fees correctly**: net 4.55, not 5.00 (Stripe took 0.45).
3. **SoD holds**: the agent key can create products/prices/payment_links and is DENIED balance,
   balance_transactions, payouts, charges.
4. **Spend is measured**: `spend_source: privacy_api`, `spend_measured: true`.

## Evidence

### Class A (Execution)

Live, against the real Stripe sandbox + Privacy.com API:

```
BEFORE: received_usd = 0.0   made_money = False
  (human paid a payment link with 4242 4242 4242 4242, $5.00)
AFTER:  received_usd = 5.0   stripe_fees_usd = 0.45   net_usd = 4.55
        verified = True   errors = []   made_money = True   net_positive = True
        spend_source = privacy_api   spend_measured = True
guard.py -> exit 0: "$25.00 of $25.00 remaining | received=$5.0 spent=$0 net=$4.55"
```

Agent key probe (both directions, live):

| Endpoint | Result | Want |
|---|---|---|
| read balance / balance_transactions / payouts / charges | **DENIED** x4 | DENIED |
| write products / prices / payment_links | **GRANTED** x3 | GRANTED |
| write payment_intents | DENIED | (fine -- not needed) |

End-to-end: the agent key created product -> price -> a live payment link URL.

### Class C (Negative -- regressions absent)

- The DENIED set is the negative control for the GRANTED set. A key that grants everything would
  also "pass" a grants-only test. **Both directions were required.**
- Caught en route: an intermediate key state where SoD held but the agent could not sell
  (products WRITE denied, prices None). My own verdict line printed "SoD HOLDS" for it -- a key
  with zero permissions passes a denial-only test trivially. **A gate that only rejects is broken
  in a flattering direction.** Fixed by asserting both directions.
- Fee accounting was never asserted, only observed: net came back 4.55 unprompted.

### Class B (Referential)

- `bin/pnl.py` (three spend modes), `bin/guard.py`, `.env` / `.env.agent` split.

### Class D (Differential)

- `received_usd`: 0.0 (every prior run) -> 5.0. **The first non-zero in the project's history.**
- `spend_source`: `issuer_enforced_uncounted` -> `privacy_api` (spend now measured, not null).
- Agent key: read-only on everything -> write on the sell path, denied on the till.

### Class E (Intent)

- `PREDICTION.md` @ `prediction-frozen`: *"The prediction dies if `received_usd > 0` with
  `verified: true`."* That field is now **proven live**. The experiment is decidable.

### Class F (Provenance)

- Manifest anchoring the charge: `9781beed546c65a4e508c086d17920232e1042ddd51a24ad986fb9d041b1baf7`
- Raw pulls immutable in `ledger/raw/`, hashed per run.

## Honest limitations

1. **TEST MODE.** Every proof above is `rk_test_`. Live mode is a different key set and unproven
   until KYC clears. The CODE path is identical; the CREDENTIALS are not.
2. **The $5 test charge is in the ledger.** It must be cleared before the run or it becomes a
   phantom "the agent made money" on iteration 1.
3. **Weak-mode SoD.** The verifier runs on the same machine. A sandboxed agent that could reach
   this filesystem could edit the hook. Strong mode (verifier off-box) is documented, not deployed.
4. **Ethical floor is still a prompt.** The name test binds a cooperative agent only.
5. **Same-author packet.** Needs an independent reviewer.

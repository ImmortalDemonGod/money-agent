# AIV Verification Packet (v2.1)

**Commit:** live key cutover (config only -- no tracked file changes; keys are gitignored)
**Protocol:** AIV v2.0 + Addendum 2.7

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: [payments, audit_logs, autonomous_execution]
  blast_radius: "Real money, real card, real legal identity, unsupervised. Every proof prior to
    this packet was rk_test_ and therefore proved nothing about this configuration."
  classification_rationale: "R3: payments + audit logs, now with live credentials."
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-16T06:42:00Z"
```

## Claim(s)

1. Both Stripe keys are `rk_live_`, distinct, and on the correct side of the SoD boundary.
2. SoD holds live in **all four** directions (not just the two that are easy to check).
3. The agent can sell live end-to-end: product -> price -> a real payment link a stranger could pay.
4. The verifier reads the live ledger; the live baseline is set to 0.

## Evidence

### Class A (Execution) -- live API, not test

| Key | Endpoint | Result | Want |
|---|---|---|---|
| verifier | balance / balance_transactions / charges / payouts | **GRANTED** x4 | GRANTED |
| verifier | products WRITE | **DENIED** | DENIED |
| agent | balance / balance_transactions / payouts / charges | **DENIED** x4 | DENIED |
| agent | products / prices / payment_links WRITE | **GRANTED** x3 | GRANTED |

Live artifact: `https://buy.stripe.com/8x200l3NVexBaY2fzg7ok00` (real link, real card would pay).

```
pnl.py  -> verified=True errors=[] received=0.0 spend_source=privacy_api spend_measured=True
set_baseline.py -> created_gt=1784184123
guard.py -> OK: $25.00 of $25.00 remaining   (exit 0)
```

### Class C (Negative -- regressions absent)

- **Four-way probe, not two.** A verifier that can also write, or an agent that can also read,
  each breaks SoD in a different direction. Both "correct denials" were asserted explicitly:
  verifier DENIED on write, agent DENIED on read. Testing only the grants would pass a key with
  full access.
- **The mode-mismatch halt cleared by itself.** Before the cutover `guard.py` refused the run
  (live card + test Stripe). After, exit 0. The guard was not disabled or bypassed -- the
  underlying condition was fixed, which is the only acceptable way for a gate to stop firing.
- `verified=true` with `errors=[]` asserted alongside `received=0.0`, because a broken pull also
  produces 0.0 and means the opposite.

### Class B (Referential)

- `.env` (verifier, gitignored) / `.env.agent` (agent, gitignored). No tracked file changed:
  **the configuration is the deliverable and it deliberately lives outside git.**

### Class D (Differential)

- Both keys: `rk_test_` -> `rk_live_`.
- `guard.py`: HALT (live card + test Stripe) -> OK.
- Baseline: test-ledger timestamp -> live-ledger `created_gt=1784184123`.
- The $5 test charge: was in the ledger -> **invisible** (different ledger entirely).

### Class E (Intent)

- `PREDICTION.md` @ `prediction-frozen` requires a real `received_usd`. Test mode could not
  falsify it: no real customer can pay a test link, so the prediction would have returned
  "confirmed" for the wrong reason. **Live mode is what makes the experiment decidable.**

### Class F (Provenance)

- Key modes verified by Stripe-assigned `rk_live_` prefix, which config cannot spoof.
- Raw live pulls hashed into `MANIFEST.sha256`.

## Honest limitations

1. **⚠ LIVE MONEY DETECTION IS UNPROVEN.** `received_usd` has moved 0 -> 5.00 **in test mode only**.
   In live it has only ever been observed as 0.0. `4242` does not work in live -- proving it needs
   a real charge (~$0.33 in fees on a $1 self-payment, refundable). **This is the last unproven
   path and it is the one the whole experiment falsifies on.** If it is broken, the agent could
   earn all night and the ledger would read zero.
2. **Weak-mode SoD.** Verifier runs on the same machine as the sandbox's reach. Strong mode
   documented, not deployed.
3. **Ethical floor is a prompt.** The name test binds a cooperative agent only.
4. **Same-author packet.** Needs an independent reviewer.

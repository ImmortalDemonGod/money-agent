# AIV Verification Packet (v2.1)

**Commit:** live money detection proven + ledger baselined to zero
**Protocol:** AIV v2.0 + Addendum 2.7 — **THIS IS THE GO/NO-GO PACKET**

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: [payments, audit_logs, autonomous_execution]
  blast_radius: "Certifies the harness fit to run unsupervised against real money. A false PASS
    means an agent runs all night against a ledger that cannot see revenue."
  classification_rationale: "R3. This packet is the go/no-go."
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-16T06:44:25Z"
```

## Claim(s)

1. **The verifier detects real money in live mode**: `received_usd` 0.0 -> 1.00 on a real card.
2. **Fee accounting is correct live**: net 0.67, not 1.00 (Stripe took 0.33).
3. The ledger is baselined to zero: the operator's own $1 proof cannot count as the agent's.
4. Every path in this harness is now backed by an executed artifact.

## Evidence

### Class A (Execution) — live, real money

```
BEFORE: received_usd = 0.0
  (operator paid a live payment link with a REAL card, $1.00)
AFTER:  received_usd = 1.0   stripe_fees_usd = 0.33   net_usd = 0.67
        verified = True   errors = []   made_money = True   net_positive = True
set_baseline.py -> created_gt=1784184265
FINAL:  received_usd = 0.0   made_money = False   verified = True
guard.py -> exit 0: "$25.00 of $25.00 remaining"
```

Full proof matrix, all executed:

| Path | Proof |
|---|---|
| live money detection | 0.0 -> **1.00** on a real card |
| live fee accounting | **0.33** caught unprompted |
| live SoD, 4 directions | verifier GRANTED/DENIED; agent DENIED/GRANTED |
| agent sells live | product -> price -> real payment link |
| spend measured | `privacy_api`, `spend_measured: true` |
| gate rejects fabricated claims | FAIL(5) on $47 + bare N/A + no hash |
| gate accepts honest claims | PASS on $0 + real sha256 |
| fail-closed | 6/6 |
| SoD hook | 4/4 blocked, verifier permitted |
| mode-mismatch | halts live-card+test-Stripe; clears on live+live |
| baseline | 1.00 -> 0.0, `verified` stayed true |

### Class C (Negative — regressions absent)

- `verified=true` and `errors=[]` asserted alongside every `0.0`. **A broken pull produces the
  identical 0.0 and means the opposite.** This distinction is the packet.
- The baseline zeroed the ledger *without* breaking the pull — proven by `verified` remaining true
  across the change.
- Test-mode detection was NOT accepted as proof of live detection. It was re-proven with real money.

### Class D (Differential)

- `received_usd`: 0.0 (all live history) -> 1.0 -> 0.0 (baselined). **First real dollar ever
  observed by this system.**
- `baseline_created_gt`: test-ledger ts -> 1784184265 (live).

### Class E (Intent)

- `PREDICTION.md` @ `prediction-frozen` (`a52961b`): *"dies if received_usd > 0 with
  verified: true."* **That field is now proven to move on real money.** The experiment is decidable
  and the prediction is honestly falsifiable.

### Class F (Provenance)

- Manifest: `9781beed546c65a4e508c086d17920232e1042ddd51a24ad986fb9d041b1baf7`
- Prediction sealed at `a52961b`, unmodified since before Stripe existed.

## Honest limitations — READ BEFORE STARTING

1. **Weak-mode SoD.** The verifier runs on the same machine the sandbox can reach. `sod_hook.sh`
   is a tripwire, not a wall. Only the **card issuer's $25 limit** is truly unbypassable.
2. **The ethical floor is a prompt.** The name test binds a cooperative agent only.
3. **$0.33 was spent proving this** and is not in `spent_usd` (it is a Stripe fee on the
   operator's own charge, baselined out). Net cost of certainty: 33 cents.
4. **Same-author packet.** Every packet in this repo was authored by the agent that wrote the code.
   **The single largest unmitigated SoD weakness in the project.** Needs an independent reviewer.
5. **The agent has not run.** Everything above proves the *harness*. Nothing proves the *agent*.

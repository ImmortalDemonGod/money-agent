# AIV Verification Packet (v2.1)

**Commit:** `bin/pnl.py` (baseline), `bin/set_baseline.py`
**Protocol:** AIV v2.0 + Addendum 2.7

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: [payments, audit_logs]
  blast_radius: "Defines what counts as the agent's money. A wrong baseline either credits the
    agent with the operator's own charges or discards real revenue."
  classification_rationale: "R3: payments + audit logs. This decides the experiment's numerator."
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-16T06:29:00Z"
```

## Claim(s)

1. Money arriving at or before `ledger/baseline.json::created_gt` is excluded from `received_usd`.
2. Filtering happens server-side (`created[gt]`), so pre-baseline money is never fetched at all.
3. The $5 readiness test charge no longer counts: `received_usd` 5.0 -> 0.0, `made_money` -> false.

## Evidence

### Class A (Execution)

```
BEFORE set_baseline:  received_usd=5.0  made_money=True   <- prediction already falsified by
                                                             the OPERATOR's own test charge
python3 bin/set_baseline.py -> created_gt=1784183307
AFTER:                received_usd=0.0  made_money=False  verified=True
                      counts_only_money_after = 2026-07-16T06:28:27+00:00
guard.py -> OK: $25.00 of $25.00 remaining | received=$0.0 spent=$0 net=$0.0
```

### Class C (Negative -- regressions absent)

- `verified` stayed **true** across the baseline change: the filter excluded the charge without
  breaking the pull. A baseline that zeroed the ledger by breaking Stripe access would show the
  same `received_usd=0.0` and mean the opposite. Distinguished by asserting `verified` and
  `errors=[]`, not just the number.
- Money detection remains proven (packet `READINESS_PROVEN`); this excludes pre-baseline money
  only, not all money.

### Class B (Referential)

- `bin/pnl.py`: `load_baseline()`, `pull_stripe(key, baseline)` with `created[gt]`.
- `bin/set_baseline.py`: verifier-only writer (`ledger/` is blocked to the agent by `sod_hook.sh`).

### Class D (Differential)

- `pull_stripe`: fetched all history -> fetches only `created > baseline`.
- `truth.json`: new `baseline_created_gt`, `counts_only_money_after`.
- `received_usd`: 5.0 (the operator's own charge) -> 0.0.

### Class E (Intent)

- `PREDICTION.md` @ `prediction-frozen` falsifies on `received_usd > 0`. Without a baseline the
  prediction was **dead on arrival** from a charge the operator made himself. This restores the
  experiment's decidability.

### Class F (Provenance)

- `ledger/baseline.json` records `created_gt` + ISO timestamp + rationale. Immutable raw pulls
  continue to be hashed into `MANIFEST.sha256` per run.

## Honest limitations

1. **Baseline is a timestamp, not a cryptographic boundary.** A verifier with ledger write access
   could move it. That is acceptable: the verifier is the trusted party by construction. The agent
   cannot (`sod_hook.sh` blocks `ledger/`, tested).
2. **Clock trust.** `created_gt` uses local time against Stripe's server timestamps. Skew of
   seconds is harmless here; it would matter if charges landed in that window.
3. **Test mode only.** Live mode is unproven -- different keys, and KYC is not confirmed complete.
4. **Same-author packet.**

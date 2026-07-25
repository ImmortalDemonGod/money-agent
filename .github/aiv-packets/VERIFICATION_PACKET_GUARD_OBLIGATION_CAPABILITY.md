# AIV Verification Packet (v2.1): guard.py surfaces the ENABLED deliver-later obligation capability

**Author:** Miguel Ingram (Author)
**Verifier:** Claude (Verifier)

## Logical unit of work

Add an informational line to `bin/guard.py`'s obligation block: when the verifier-published
`obligations.json` shows `authorization.enabled`, print a CAPABILITY note telling the agent it may
sell a deliver-later build (take payment now, ship within the deadline) up to the verifier's caps,
with the verifier's auto-refund guarantee, via `bin/obligations.py`.

Why: the operator enabled the post-payment obligation class on the verifier (a real envelope
expansion), but NOTHING surfaced it to the agent — `guard.py` only checked for a BREACH, and
`obligations.py list` printed "no obligations." So the agent kept self-limiting to instant-only
offers, unaware it could now presell a real, multi-day, refund-guaranteed project. This states a
PERMISSION (the agent's own operating envelope), not a strategy — it does not tell the agent what or
whom to sell; the agent still decides. Paired atomic commit: this packet + `bin/guard.py`.

## Classification

```yaml
classification:
  risk_tier: R1
  sod_mode: S0
  critical_surfaces: [iteration_guard]
  blast_radius: agent-informational
  classification_rationale: >
    Adds a single informational print inside the existing obligation block, gated on the
    verifier-grounded authorization.enabled flag. It changes NO gate logic and NO exit code (the
    breach check above still returns fail; the DEMAND_REFUTED and agenda logic below are untouched).
    It reads only the already-loaded, already-verified obligations.json. Lowest tier: it can only
    print a true fact about the agent's envelope while the rail is enabled.
  classified_by: Miguel Ingram (Author) + Claude (Verifier)
  classified_at: 2026-07-25T04:10:00Z
```

## Claim(s)

1. **CLM-001 - the capability surfaces when enabled.** With `obligations.json`'s
   `authorization.enabled == true`, `guard.py` prints the CAPABILITY line naming the deadline cap,
   single-USD cap, and open cap, and pointing at `bin/obligations.py`.

   **Falsifiable by:** the line not printing when the authorization is enabled.

2. **CLM-002 - it is silent when disabled, and changes no verdict.** When authorization is absent or
   `enabled == false`, no line prints; and in all cases the guard's pass/fail exit code is unchanged
   (the print is informational only).

   **Falsifiable by:** the line printing while disabled, or the exit code differing from before.

## Evidence

### Class A (Execution)

- `python3 -m py_compile bin/guard.py` -> ok.
- Ran the agent's `bin/guard.py` in the sandbox against the live (enabled) ledger: it printed
  `CAPABILITY: deliver-later sales are ENABLED -- ... up to $5000.0/job (1 open) ... 72.0h ...
  bin/obligations.py ...`, and exited **0** (unchanged). (CLM-001, CLM-002)

### Class B (Referential)

- The line sits immediately after the `if ob.get("breached")` fail-return, still inside
  `if ob is not None:`, gated on `(ob.get("authorization") or {}).get("enabled")`. It uses only
  fields from the already-loaded, already-verified `ob`. No `return`, no `fail()`, no state change.

### Class C (Negative)

- No money/facts/signing/breach/deadline/gate logic touched. The breach fail (P5), the freshness
  check, the DEMAND_REFUTED checkpoint, and the standing-presence agenda are all unchanged. It cannot
  turn a fail into a pass or vice versa.

### Class D (Differential)

- Before: an enabled deliver-later envelope was invisible to the agent (guard silent; `obligations.py
  list` said "no obligations") -> the agent self-limited to instant-only offers.
- After: every iteration, while enabled, the agent sees the exact caps + the register command.

### Class E (Intent Alignment)

The agent must operate on an accurate picture of its own permissions; an enabled capability it cannot
see is a defect that makes it self-limit. Surfacing it (a fact, not a directive) is the fix; strategy
(what/whom to sell) is deliberately NOT included.

### Class F (Provenance)

- `git diff --cached -- bin/guard.py`.

## Cost

- Spent: `nothing` -- offline edit + one sandbox run. No network, money, or facts write.
- Cumulative (truth.json): `zero`.

## Honest limitations

- Prints every iteration while enabled (mild repetition) -- deliberate, so the expanded envelope
  stays in the agent's working context and it stops self-limiting. Silent when disabled.
- Does not surface the separately-added `actuate.py withdraw` capability; that is covered out-of-band
  (the agent's actuate help lists it) and is not this packet's scope.

## Verification methodology

```bash
python3 -m py_compile bin/guard.py
# against the enabled ledger: guard prints the CAPABILITY line and exits 0 (unchanged)
```

## Summary

R1/S0 informational surface: `guard.py` now tells the agent, every iteration while the class is
enabled, that deliver-later sales are available (caps + auto-refund + register command) -- closing the
gap where the operator-enabled obligation envelope was invisible and the agent kept self-limiting to
instant-only. States a permission, not a strategy; changes no gate verdict.

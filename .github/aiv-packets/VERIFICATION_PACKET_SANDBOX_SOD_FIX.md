# AIV Verification Packet (v2.1)

**Commit:** `bin/guard.py` (scoped SoD), `bin/setup_sandbox.sh`
**Protocol:** AIV v2.0 + Addendum 2.7

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: [audit_logs, autonomous_execution]
  blast_radius: "Before this fix SoD was not enforced in the sandbox AT ALL. The agent could
    author its own P&L and pass every check."
  classification_rationale: "R3. This is the enforcement of the only invariant the repo has."
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-16T07:21:00Z"
```

## Claim(s)

1. `guard.py` halts when any non-verifier authors `ledger/` **after** the baseline, and passes when
   only the verifier does.
2. `bin/setup_sandbox.sh` installs the pre-commit hook in a fresh clone and **proves it fires**
   with a live agent-write probe.
3. The setup script aborts if `.env` (verifier credentials) is present in the sandbox.

## Evidence

### Class A (Execution)

```
1. clean                          -> exit 0  "OK: $25.00 of $25.00 remaining"
2. agent commits to ledger/       -> exit 1  HALT "non-verifier author since the run started: ['agent']"
3. remove forgery, re-check       -> exit 0  PASS
4. setup_sandbox.sh               -> hook installed; live probe: "agent write to ledger/ BLOCKED"
                                     PREDICTION.md absent; tag prediction-frozen -> 71fbd04
                                     "FATAL: .env is present and contains STRIPE_READ_KEY"
```

### Class C (Negative -- regressions absent)

- **Test 3 is the whole packet.** Test 2 halting proves nothing on its own: a permanently stuck
  gate produces the identical HALT. Returning to PASS after the forgery is removed proves the gate
  discriminates rather than blocks.
- The setup script's `.env` check **fired correctly on this machine** (which legitimately holds the
  verifier key). A check that never fires is indistinguishable from a check that does not exist.
- Test 4's probe is a **live agent write**, not an inspection of the hook file. `installed != works`
  is the defect this whole script exists to prevent.

### Class B (Referential)

- `bin/guard.py`: allowlist `{verifier}` scoped to `--since=<baseline.set_at_iso>`.
- `bin/setup_sandbox.sh`: hook install + 4 preflight assertions.

### Class D (Differential)

- Allowlist: `{verifier, "Miguel Ingram"}` -> `{verifier}`.
- Scope: last 5 ledger commits (unscoped) -> commits since the baseline.
- Sandbox hooks: **none** (git does not clone `.git/hooks`) -> installed + proven by `setup_sandbox.sh`.
- Baseline ordering: mid-setup -> **last setup step**, committed by the verifier.

### Class E (Intent)

- `CONSTITUTION.md` rule 5: *"You may not write to `ledger/`."* That rule was **unenforced in the
  sandbox**: the hook did not exist there, and the one remaining tripwire had the agent's own
  identity on its allowlist.

### Class F (Provenance)

- `prediction-frozen` -> `71fbd04`, verified present. Ledger authors since baseline: **`verifier`** only.

## Honest limitations

1. **Still weak mode.** The agent can edit `sod_hook.sh`, `guard.py`, or `.git/hooks/` in its own
   sandbox. This raises the floor from *"no enforcement"* to *"enforcement it must deliberately
   disable"* -- which is detectable in the morning, not preventable at runtime.
2. **`truth.json` transport is unsolved.** The verifier holds the read key on the operator's Mac;
   the sandbox has a clone. Nothing yet pushes a fresh ledger to the sandbox, so the agent's
   `truth.json` is **stale from run start** unless the verifier commits+pushes and the agent pulls.
   **This is the largest remaining architectural gap.**
3. **Found by an independent reader, not by me.** Both bugs were in the file whose entire job is
   enforcing separation of duties, and both survived my own review. That is the same-author
   weakness every packet here names, demonstrated on the enforcement itself.

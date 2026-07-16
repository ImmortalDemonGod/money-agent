# AIV Verification Packet (v2.1)

**Commit:** `bin/verifier_loop.sh`, `bin/setup_sandbox.sh`, `bin/mail.py`, `bin/guard.py`
**Protocol:** AIV v2.0 + Addendum 2.7

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: [payments, audit_logs, autonomous_execution]
  blast_radius: "The verifier loop is the only path by which real money reaches the agent's view.
    Broken, the agent reads received=$0 all night while money arrives, and the frozen prediction
    returns 'confirmed' from a stale file."
  classification_rationale: "R3. This closes the strong-mode SoD boundary: the read key stays on
    the operator's machine and never enters the sandbox."
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-16T07:33:00Z"
```

## Claim(s)

1. Real money arriving in Stripe propagates to a fresh clone: `received_usd` 0.0 -> 1.0.
2. The verifier does not clobber the agent's work across a pull.
3. The loop publishes only when a meaningful number moves, and pulls cleanly every cycle.

## Evidence

### Class A (Execution) -- end-to-end, real money

```
baseline rewound behind the operator's already-paid $1 (no new charge)
pnl.py            -> received=$1.0 net=$0.67 made_money=True
verifier loop     -> committed as `verifier`, pushed
fresh git clone   -> received_usd=1.0 made_money=True net=0.67   <-- THE AGENT SEES IT
agent MONEY_LOG entry pushed, then verifier ran -> entry still present (not clobbered)
7 cycles @2s      -> PULL FAILED: 0 | pushes: 1 (quiet after first publish)
```

### Class C (Negative -- regressions absent)

- **Propagation was tested to a FRESH CLONE, not to the local tree.** The local tree is where the
  verifier writes; testing there proves nothing about what the agent sees.
- **Test 2 (agent's MONEY_LOG survives) is the negative control for the pull**: a loop that
  hard-reset would show the same clean pull and silently destroy the agent's night.
- The $1 was re-exposed by rewinding the baseline rather than by paying again (operator's call).
  **The money was real; only the accounting window moved.**

### Class D (Differential) -- five bugs, all found by running it

| # | Bug | Effect |
|---|---|---|
| 1 | `verifier_loop.sh` was **never committed** | the file closing the gap was not in the repo |
| 2 | `truth.json` left dirty when no change | `pull --rebase` failed **every cycle**, silently |
| 3 | `git checkout -- ledger/` too broad | reverted `baseline.json` -> logged `$0` while pnl measured **$1** |
| 4 | `MANIFEST.sha256` tracked + regenerated | same dirty-tree pull failure |
| 5 | log written **into** `ledger/` | the loop's own logging broke the loop's own pull |

Every one reported success while failing. **Not one was visible by reading the file.**

### Class B (Referential)

`bin/verifier_loop.sh` (pull -> pnl -> commit-as-verifier -> push, publish-on-change only);
`bin/setup_sandbox.sh`; `bin/mail.py`; `bin/guard.py` (scoped SoD).

### Class E (Intent)

`CONSTITUTION.md`: *"ledger/truth.json is the verifier's... computed by a process you cannot
reach, using credentials you do not have."* Only true if the verifier runs **off** the sandbox and
publishes. That is this file.

### Class F (Provenance)

Ledger authors since baseline: `verifier` only. Baseline restored to `1784187106` after the test.

## Honest limitations

1. **AIV ceremony blocks the automation.** The pre-push hook halted the verifier's push because
   `bin/` commits lacked packets. An unattended verifier that cannot push is a verifier that does
   nothing. This packet clears it, but the tension is real and unresolved.
2. **`raw/` grows unbounded** -- 107 tracked pulls already; ~240 cycles overnight adds ~700 files.
   Evidence, but noisy.
3. **Five bugs in one file in one hour.** The defect rate here is the honest signal about how much
   of this is proven versus written.
4. **Same-author packet.**

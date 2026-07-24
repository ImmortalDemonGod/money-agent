# AIV Verification Packet (v2.1): guard staleness HALT self-diagnoses the env/lane case

**Author:** Miguel Ingram (Author)
**Verifier:** Claude (Verifier)

## Logical unit of work

Single functional change in `bin/guard.py`: the staleness HALT branches its MESSAGE on the
already-computed `truth_source`. When the ledger fell back to `working-tree-committed` (the
committed seed, because `origin/<LEDGER_BRANCH>` did not resolve) the message now names the real
cause -- an unset/wrong `LEDGER_BRANCH` / unsourced agent env -- instead of the misleading "Restart
the verifier." The `ledger-branch` (real-verifier) case keeps the original message. The paired
atomic commit contains only this packet and `bin/guard.py`.

## Classification

```yaml
classification:
  risk_tier: R1
  sod_mode: S0
  critical_surfaces: []
  blast_radius: local
  classification_rationale: >
    guard.py is the pre-iteration gate, but this change is MESSAGE-ONLY: the set of conditions
    that HALT is byte-identical (both branches call fail() in exactly the cases the single
    fail() did before), the grounding/source logic is untouched, and `truth_source` was already
    computed and in scope. No money, facts-lane, credential, signature, or policy behavior
    changes -- only the human-readable text of one already-occurring HALT. R2 is not warranted
    (no logic, schema, or cross-service change).
  classified_by: Miguel Ingram (Author) + Claude (Verifier)
  classified_at: 2026-07-24T00:00:00Z
```

## Claim(s)

1. **CLM-001 - the fell-back stale HALT self-diagnoses the env.** When a stale ledger is read from
   `working-tree-committed` (not the verifier lane), guard's HALT now names `LEDGER_BRANCH`, the
   actual source, and the one-step fix (`set -a; . ./.env.agent; set +a`) instead of "Restart the
   verifier."

   **Falsifiable by:** an unset-`LEDGER_BRANCH` run against the committed seed still printing
   "Restart the verifier" / not mentioning `LEDGER_BRANCH`.

2. **CLM-002 - the real-verifier-stale path and the halt behavior are unchanged.** A stale
   `ledger-branch` read still prints "Restart the verifier," and every case that halted before
   still halts.

   **Falsifiable by:** the `ledger-branch` stale branch no longer saying "Restart the verifier," or
   any previously-halting case now passing.

## Evidence

### Class A (Execution)

- Fell-back case: `env -u LEDGER_BRANCH -u SHADOW python3 bin/guard.py` (operator repo, HEAD carries
  the 2026-07-16 seed) ->
  `HALT: ledger is 681841s old (> 1800s) AND source is 'working-tree-committed', NOT the verifier's
  lane ... LEDGER_BRANCH='ledger' -- is that your run's lane (e.g. ledger-run2)? Source your agent
  env and re-run: set -a; . ./.env.agent; set +a. Only if origin/ledger itself is genuinely stale
  is the verifier actually down.`  -- the NEW self-diagnosing message (no "Restart the verifier").
- Real-verifier path preserved: `grep -n "Restart the verifier" bin/guard.py` still present on the
  `truth_source == "ledger-branch"` branch.
- Fresh lane unaffected: `LEDGER_BRANCH=ledger-run2 python3 bin/truth.py received_usd` ->
  `source: ledger-branch` / `0.0` (no staleness).
- `python3 -m py_compile bin/guard.py` -> ok.

### Class B (Referential)

- `bin/guard.py` staleness block: `if age > MAX_AGE_S:` now branches -- `truth_source ==
  "ledger-branch"` keeps the "Restart the verifier" text; else returns a `fail()` naming
  `truth_source`, `_truth.LEDGER_BRANCH`, and the source line. `truth_source` comes from the
  existing `t, truth_source = _truth.load()`; `_truth.LEDGER_BRANCH` is the module-level resolved
  branch.

### Class C (Negative)

- Halt set is byte-identical: every input that halted before still halts (both branches call
  `fail()`); this only changes which string a stale read prints. No grounding, signature, SoD
  authorship, money, or cap logic touched. Verified the `ledger-branch` message is retained and the
  fresh lane still grounds.

### Class D (Differential)

- Before: any stale ledger (regardless of source) -> `fail("... Restart the verifier.")`.
- After: stale + `ledger-branch` -> same; stale + `working-tree-committed` (or other non-lane) ->
  `fail("... source is <src>, NOT the verifier's lane ... LEDGER_BRANCH=<b> ... source your agent
  env ...")`.

### Class E (Intent Alignment)

Authorized by the operator request to harden the run's env-sourcing failure mode: run-2's first
iteration hit this exact HALT (an unsourced fire -> `LEDGER_BRANCH` unset -> `truth.py` read the
stale committed seed) and the "Restart the verifier" text sent the agent chasing a nonexistent dead
verifier. PROMPT.md's "TWO ENV FILES -- DO NOT CONFLATE" and "a missing credential means you have
not sourced it, NOT that it is broken" name exactly this trap; this makes the gate say so at the
moment it fires, so a fresh fire fixes it in one step.

### Class F (Provenance)

- Change source is the staged `bin/guard.py` diff, limited to the `if age > MAX_AGE_S:` message
  branch. Reproduce with `git diff --cached -- bin/guard.py`.
- The stale seed used to trigger the fell-back path is `HEAD:ledger/truth.json`
  (`computed_at 2026-07-16T08:37:19Z`).

## Cost

- Spent this iteration: `nothing` -- an offline diagnostic-message edit.
- Cumulative spent (from `truth.json`, not from memory): `zero` of the cap.

## Honest limitations

- This does not PREVENT the HALT (guard still fail-closes on an ungrounded/stale read, correctly);
  it makes the HALT self-explaining so the fix is one step. Preventing it entirely is an
  env-provisioning concern (ensuring `LEDGER_BRANCH` is set for every fire), out of scope here.
- The message keys on `truth_source == "ledger-branch"`; a future new grounded source label would
  fall into the env-diagnosis branch until the condition is widened (fail-safe: a helpful message,
  not a wrong halt).
- Class G omitted: no pre-implementation prediction was recorded.

## Verification methodology

```bash
env -u LEDGER_BRANCH -u SHADOW python3 bin/guard.py   # new env-diagnosis message on the stale seed
grep -n "Restart the verifier" bin/guard.py            # retained on the ledger-branch path
LEDGER_BRANCH=ledger-run2 python3 bin/truth.py received_usd   # fresh lane still grounds
python3 -m py_compile bin/guard.py
```

## Summary

R1/S0 message-only change: guard's staleness HALT now tells a fresh fire that a stale
`working-tree-committed` read means an unset/wrong `LEDGER_BRANCH` (source `.env.agent`), instead of
the misleading "Restart the verifier," while the real-verifier-stale path and the entire halt set
are unchanged.

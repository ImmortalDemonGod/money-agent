# AIV Verification Packet (v2.1): operator actuation resolutions auto-consume every tick

**Author:** Miguel Ingram (Author)
**Verifier:** Claude (Verifier)

## Logical unit of work

Wire `bin/actuate.py sync-all` into the iteration harness so an operator-published resolution is
consumed automatically, within one tick of landing -- instead of sitting `open` until the agent
happened to run `sync` by hand. Add `iter.py::_consume_actuations()` and call it at the top of
`new()` (iteration open) and `watch()` (watch tick); together those cover every cycle the agent
runs.

The defect this closes was observed live: the operator FULFILLED the dev.to actuation (ACT-003) on
the facts lane at 22:11, generating a returned credential, and it stayed `open` in the agent's
claims file for hours -- eating one of the 3 capped queue slots and leaving the credential
undelivered -- because nothing ran `sync-all`. `actuate_watch.sh` exists but was never armed as a
durable wakeup, and the agent's loop never called it. Consumption depended on the agent remembering
a manual step it did not take. Paired atomic commit: this packet + `bin/iter.py`.

## Classification

```yaml
classification:
  risk_tier: R2
  sod_mode: S0
  critical_surfaces: [iteration_lifecycle, actuation_queue]
  blast_radius: agent-claims-branch
  classification_rationale: >
    Adds a best-effort, fail-open call to the EXISTING agent consume path (actuate.py sync-all) at
    two iteration-lifecycle entry points. sync-all verifies the verifier signature itself, so
    auto-running it adds no privilege and does not weaken separation of duties -- it is the agent's
    own sync, run on time instead of by hand. No money/facts/credential/disclosure/signing logic
    changed; the only new effect is that a signed resolution lands promptly. Cannot block a tick
    (all errors swallowed) and does no network I/O when nothing is open.
  classified_by: Miguel Ingram (Author) + Claude (Verifier)
  classified_at: 2026-07-24T23:05:00Z
```

## Claim(s)

1. **CLM-001 - a landed resolution is consumed automatically.** When an actuation task is `open` and
   the operator has published a grounded resolution, the next `iter.py new` or `iter.py watch`
   consumes it (materializes any return, resolves the companion bet, drops the open-count) with no
   manual `sync`, and surfaces the per-task success line to the agent.

   **Falsifiable by:** an open+resolved task remaining unconsumed after a `new`/`watch` tick.

2. **CLM-002 - the common (idle) path pays nothing.** With no `open` actuation task, `_consume_
   actuations()` returns before any subprocess/network call -- no ledger fetch on every watch tick.

   **Falsifiable by:** a ledger fetch / sync-all invocation occurring when zero tasks are open.

3. **CLM-003 - it never blocks a tick.** Any error, timeout, or non-zero from sync-all is swallowed;
   `new()`/`watch()` proceed exactly as before. The auto-consume is strictly additive.

   **Falsifiable by:** a sync failure causing `new`/`watch` to error or change its exit code.

## Evidence

### Class A (Execution)

- `python3 -m py_compile bin/iter.py` -> ok.
- Isolated test of `_consume_actuations()` (subprocess.run stubbed, REPO redirected to a temp dir):
  - CASE A no task file -> sync-all NOT called. (CLM-002)
  - CASE B task file, all closed -> sync-all NOT called (skips network). (CLM-002)
  - CASE C one `open` task -> sync-all invoked; the `... synced from verifier facts ...` line is
    surfaced as `actuation consumed: ...`. (CLM-001)
  - CASE D sync-all raises -> swallowed, no exception escapes. (CLM-003)

### Class B (Referential)

- `_consume_actuations()`: reads `run/actuation_tasks.json` (absent -> return); filters
  `status == "open"` (none -> return before any I/O); else runs `python3 bin/actuate.py sync-all`
  (cwd=REPO, timeout 90, captured); prints only lines containing `synced from verifier facts`;
  wraps everything in `try/except: pass`.
- Called as the FIRST statement of `new()` and `watch()`. Env (LEDGER_BRANCH, MONEY_AGENT_STATE) is
  inherited from the agent process -- the same env under which `truth.py`/`guard.py` already resolve
  the ledger branch and the ephemeral decrypt key.

### Class C (Negative)

- No money/facts/credential/disclosure/em-dash/SENT_LOG/signing logic touched. The consume path
  (`actuate.py sync-all` -> `_grounded_resolution`) already verifies the verifier signature and the
  request-hash binding; this change only changes WHEN it runs, never WHETHER it verifies. sync-all's
  own commit/push of the synced task is unchanged.

### Class D (Differential)

- Before: a fulfilled resolution stayed `open` in the claims file until a manual `sync`; the dev.to
  credential sat undelivered for hours and pinned a capped slot.
- After: the next iteration open or watch tick consumes it automatically and surfaces it; the slot
  frees and the credential materializes without operator or agent hand-work.

### Class E (Intent Alignment)

The operator directed that consuming a resolution "should have been automated." The actuation queue
was designed with a durable-wakeup consumer (`actuate_watch.sh`) precisely so resolutions land
without manual action; this makes that guarantee hold via the always-run iteration chokepoint rather
than a wakeup that must be separately armed.

### Class F (Provenance)

- `git diff --cached -- bin/iter.py`.

## Cost

- Spent: `nothing` -- offline edit + stubbed unit test; no network, money, or facts write.
- Cumulative (truth.json): `zero`.

## Honest limitations

- Consumption is tied to the agent running `new`/`watch`. If the agent's process is fully stopped
  (no ticks at all), nothing runs -- but in that state there is no agent to consume for. Within a
  live loop, worst-case latency is one tick.
- `actuate_watch.sh` (the durable-wakeup consumer) is left in place as a belt-and-suspenders path;
  arming it is a separate ScheduleWakeup concern not addressed here.
- Adds one ledger fetch per tick ONLY while an actuation task is open (bounded: at most the cap of
  3, and only until each is resolved+consumed). Zero overhead when the queue is empty.

## Verification methodology

```bash
python3 -m py_compile bin/iter.py
# _consume_actuations: no-file/all-closed -> no sync-all; one open -> sync-all + surfaced;
#   sync raises -> swallowed.
```

## Summary

R2/S0 iteration-harness fix: `iter.py` now auto-consumes operator actuation resolutions at the top
of every `new`/`watch` tick, so a fulfilled request lands (credential delivered, slot freed,
companion bet resolved) within one tick instead of waiting on a manual `sync` that often never came
-- the exact failure that left the operator's dev.to fulfillment stranded for hours. Fail-open, zero
cost when idle, no SoD or facts-path change.

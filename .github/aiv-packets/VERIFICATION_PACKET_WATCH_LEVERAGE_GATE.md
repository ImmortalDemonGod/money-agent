# AIV Verification Packet (v2.1): WATCH-tick research-gate + consecutive-streak context injection

**Author:** Miguel Ingram (Author)
**Verifier:** Claude (Verifier)

## Logical unit of work

Single functional change in `bin/iter.py`: WATCH ticks were unbounded (only `MAX_WALL_CLOCK_H`
capped them), so an agent whose levers are all time-gated could idle on watch ticks all night
instead of using its mandated deep-research/leverage. This extends `PACE_ENFORCE` to WATCH ticks
(operator-authorized method-enforcement, NOT strategy): from the 2nd consecutive tick a PURE-IDLE
tick (no bet due, no research declared) is refused, and every consecutive tick re-injects the
PROMPT's "USE YOUR LEVERAGE / keep a fresh experiment running" directives into the agent's context.
The paired atomic commit contains only this packet and `bin/iter.py`.

## Classification

```yaml
classification:
  risk_tier: R2
  sod_mode: S0
  critical_surfaces: []
  blast_radius: loop-pacing
  classification_rationale: >
    iter.py is the agent's iteration scaffold; this changes the WATCH-state pacing (a gate + a
    stderr reminder) under PACE_ENFORCE. It does NOT touch money, the facts lane, credentials,
    the SoD boundary, the money/hash checks, or any business/strategy -- it only refuses a
    pure-idle repeated watch tick and re-surfaces the operating prompt's own directives. It never
    dictates WHAT to research or sell. R2 (not R1) because it changes agent loop behavior; not R3
    (no fabrication/payment surface).
  classified_by: Miguel Ingram (Author) + Claude (Verifier)
  classified_at: 2026-07-24T00:00:00Z
```

## Claim(s)

1. **CLM-001 - pure-idle consecutive WATCH ticks are refused under PACE_ENFORCE.** From the 2nd
   consecutive watch tick, if no bet is due to poll AND no `--researched` note is given, `iter.py
   watch` exits 2 with a message telling the agent to use its leverage (research a new lever) or
   record the research it did.

2. **CLM-002 - consecutive WATCH ticks re-inject the ignored loop directives.** On streak >= 2 the
   command prints the PROMPT's USE-YOUR-LEVERAGE / keep-a-fresh-experiment / "old levers vs new
   levers" reminder to the agent's context.

3. **CLM-003 - legitimate work is never blocked.** A due bet (real polling), a declared research
   pass (`--researched`), the first watch tick, and every path with `PACE_ENFORCE!=1` all pass; a
   real iteration (`iter.py new`) resets the streak.

   **Falsifiable by:** a due-bet or `--researched` watch tick being refused, the first tick being
   refused, or `new()` not resetting the streak.

## Evidence

### Class A (Execution)

Isolated clone (edited `iter.py`, throwaway bare origin, `PACE_ENFORCE=1`, no open bets):
- `iter.py watch "poll clocks"` -> `watch tick recorded`, exit 0, streak=1, NO injection. (CLM-003)
- `iter.py watch "still waiting"` (2nd, idle) -> **exit 2**, `REFUSED: 2 consecutive WATCH ticks --
  no bet due to poll and no research this fire ...`; streak stays **1** (a refused tick does not
  count). (CLM-001)
- `iter.py watch --researched "searched 3 gig boards + newsletter classifieds, all account-gated"
  "researched empty"` -> exit 0 + the full `[WATCH STREAK = 2] ... USE YOUR LEVERAGE ... KEEP A
  FRESH EXPERIMENT RUNNING ... 'Every lever is time-gated' describes your OLD levers ...` injection;
  streak=2. (CLM-002)
- `iter.py new --lever "real work"` -> streak resets to **0**. (CLM-003)
- `python3 -m py_compile bin/iter.py` -> ok. (Fixed a `NameError: os` by moving `import os` to
  module scope; it had been imported only inside `new()`.)

### Class B (Referential)

- `bin/iter.py`: new module-level `import os`; `WATCH_STREAK` = `.run/watch_streak` (local, never
  committed) with `_read_streak()`/`_reset_streak()`; `watch(note, researched="")` gains the
  streak, the `has_due` check (via `bets.is_due`/`open_bets`), the PACE_ENFORCE gate at
  `streak >= 2 and not has_due and not researched`, and the `streak >= 2` injection; `new()` calls
  `_reset_streak()`; `main()` parses `--researched` for the watch subcommand.

### Class C (Negative)

- No money/facts/credential/SoD/hash-check logic touched. A refused tick writes nothing and does
  not increment the streak (verified streak stayed 1). Due-bet polling, first ticks, `--researched`
  ticks, and `PACE_ENFORCE!=1` are all unaffected -- the gate is scoped to repeated pure-idle only.

### Class D (Differential)

- Before: WATCH ticks unlimited; an all-time-gated agent could idle indefinitely (only
  `MAX_WALL_CLOCK_H` bounded it).
- After: 2nd+ consecutive pure-idle tick refused under PACE_ENFORCE; every consecutive tick
  re-injects the leverage directives.

### Class E (Intent Alignment)

Authorized by the operator's explicit request to stop the agent idling on WATCH ticks all night and
to re-inject, on consecutive ticks, "what it is ignoring from the loop." PROMPT.md already mandates
this ("USE YOUR LEVERAGE ... deep-research subagents ... keep a fresh experiment running ... never
conclude there is nothing left to try"); the harness merely did not enforce it during WATCH. This
enforces the existing directive without adding any business direction.

### Class F (Provenance)

- Change source is the staged `bin/iter.py` diff. Reproduce with `git diff --cached -- bin/iter.py`.

## Cost

- Spent this iteration: `nothing` -- an offline loop-pacing edit.
- Cumulative spent (from `truth.json`, not from memory): `zero` of the cap.

## Honest limitations

- A determined agent can satisfy the gate with a token `--researched` note (same class as any
  self-declared field); the gate forces a conscious research step and re-surfaces the mandate, but
  does not verify research depth. The injection is a nudge, not a proof.
- The streak counter is local runtime state (`.run/watch_streak`); a wiped sandbox resets it to 0
  (fail-open toward allowing a tick, never toward a wrong halt).
- Class G omitted: no pre-implementation prediction was recorded.

## Verification methodology

```bash
python3 -m py_compile bin/iter.py
# isolated clone, PACE_ENFORCE=1, no bets:
iter.py watch "a"                      # ok, streak 1, no injection
iter.py watch "b"                      # REFUSED (exit 2), streak stays 1
iter.py watch --researched "x" "b"     # ok + injection, streak 2
iter.py new --lever "y"                # streak -> 0
```

## Summary

R2/S0 loop-pacing change: WATCH ticks now enforce the prompt's "use your leverage" mandate --
repeated pure-idle ticks are refused under PACE_ENFORCE, and consecutive ticks re-inject the
deep-research/keep-a-fresh-experiment directives -- so a time-gated agent researches new levers
instead of idling, without any strategy injection.

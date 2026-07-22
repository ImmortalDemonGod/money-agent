# Running as a standing presence (issue #4) — the config recipe

Run 1's iterations burned in ~6–10 minutes each, so the agent exhausted every minutes-scale action
in one night and then faced only day-scale clocks: search indexation ("days is the honest
expectation" — never got its days), HN reputation (karma needs visible participation which needs
karma), a Mastodon staff approval that sat pending all night. A one-night sprint structurally
cannot harvest those. The fix is mostly NOT new machinery — it is posture: run for days, wait
cheaply, and make every wait accountable. This file is the recipe; the machinery it uses already
exists.

## The five pieces

**1. The bet registry is the spine (`bin/bets.py`, new).** Every day-scale lever gets recorded the
moment it is placed: what, clock class, how to check, poll cadence, deadline. `guard.py` prints
the due-bets agenda at the top of every iteration, `iter.py watch` stamps it on every tick, and
`conclusion_gate.py` refuses an "impossible" conclusion while any bet is open. Waiting is legal;
untracked waiting is how run 1 died (concluded at iteration 095 over a live bet).

**2. Wall-clock checkpoint, not iteration count, bounds the run.**
```bash
export MAX_WALL_CLOCK_H=96      # e.g. 4 days; guard halts as an operator CHECKPOINT (exit 2)
export MAX_ITERS=0              # iteration ceilings fight a standing posture; prefer wall clock
```
The checkpoint never concludes anything — the operator extends or stops.

**3. The loop self-paces to the slowest live clock.** The `/loop` is issued with no interval; the
agent sizes wakeups itself. The rule (now in RUN_COMMANDS/PROMPT): between due bet-checks, a WATCH
state's wakeup is sized to the SLOWEST live clock. Indexation bets poll daily, not every ten
minutes. `bin/iter.py watch` makes each tick one committed line, ~0 tokens, no iteration number.

**4. The verifier is provisioned for days, not hours.**
```bash
export INTERVAL=300             # facts recompute cadence; 120s is sprint posture
# INFERENCE_CSV=/path/costs.csv # (issue #41) refresh the export ~daily on a multi-day run so
                                # net_usd_full tracks reality instead of a stale snapshot
export HEARTBEAT_S=600          # liveness pushes (must stay < LEDGER_MAX_AGE_S)
export LEDGER_MAX_AGE_S=1800    # agent-side staleness halt, unchanged
export LEDGER_MAX_COMMITS=3000  # NEW: rotate (squash) the facts lane when history exceeds this;
                                # content (every raw pull) is preserved, only the graph compacts.
                                # If the ledger branch is push-protected, allow the verifier
                                # credential to force-push it or leave rotation off.
```
`start_verifier.sh` / `verifier_daemon.sh` no longer hard-require macOS `caffeinate` (the v2
DEGRADED #9 portability bug): on Linux, run the daemon under systemd with `Restart=always` on a
host that does not sleep.

**5. The operator supervises on a long cadence.** `bin/supervise.sh <agent-branch>` remains the
one-screen check; it now also surfaces the edge verdict. Once or twice a day is enough — the
alerts that matter (first dollar, verified edge, dead verifier, stale ledger) are its VERDICT
line.

## What a standing run changes about "exhaustion"

Nothing becomes exhaustible faster; one thing becomes exhaustible at all. In sprint posture,
"every remaining lever is day-scale" was indistinguishable from "done" (run 1 conflated exactly
these). In standing posture that state is simply a WATCH: the registry holds the open bets, the
agenda resurfaces them, and the conclusion gate refuses "impossible" until each is resolved —
won, lost, or expired, with evidence. Expiry is a real resolution: a bet that never converted is a
falsification, and a compounding portfolio of resolved bets is exactly the dataset
`knowledge/outcomes.jsonl` exists to keep.

## What is still NOT mechanical (named honestly)

- Nothing forces the agent to schedule long wakeups; the sizing rule is prose plus the agenda's
  visibility. A future harness could rate-limit iterations against the due-bet schedule.
- Bet records are agent-committed (tripwire, not wall): deleting one is a visible commit, but only
  the operator's read catches it. The failure this guards against — run 1's — was forgetting, not
  forging.
- The wakeup mechanism itself (cron vs queued wakeups) lives outside the repo; entry 005 of
  IMPROVEMENT_LOG.md records why queued wakeups beat cron for liveness.

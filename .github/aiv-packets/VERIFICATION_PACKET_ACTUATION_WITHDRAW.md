# AIV Verification Packet (v2.1): agent can withdraw its own abandoned actuation request

**Author:** Miguel Ingram (Author)
**Verifier:** Claude (Verifier)

## Logical unit of work

Add `bin/actuate.py withdraw <id> --reason "<why>"`: an agent-side command that retracts an OWN
`open` actuation request the agent no longer intends to pursue (an abandoned direction), and teach
`bin/conclusion_gate.py` that a `withdrawn` task is a closed terminal state.

The capability-delegation queue caps open requests at `MAX_OPEN_REQUESTS` (default 3) and its ONLY
exits were operator `fulfill`/`decline` + agent `sync`. So a request whose direction the agent
dropped sat `open` forever, permanently pinning one of the three slots and forcing the operator to
`decline` it by hand -- the operator hit exactly this: the queue full of asks for abandoned
directions (Pinterest, dev.to, Upwork) with no self-service drain. `run/actuation_tasks.json` is the
AGENT's own claims file, so the agent retracting a request it authored fabricates no human action:
it is NOT a resolution, never touches the verifier facts lane, and does not violate separation of
duties (nothing claims "a human acted"). It DOES resolve the conclusion-blocking companion bet, so
no orphan bet survives to jam `conclusion_gate.py`. Paired atomic commit: this packet +
`bin/actuate.py` + `bin/conclusion_gate.py`.

## Classification

```yaml
classification:
  risk_tier: R2
  sod_mode: S0
  critical_surfaces: [actuation_queue, conclusion_gate]
  blast_radius: agent-claims-branch
  classification_rationale: >
    Adds one agent-side state transition (open -> withdrawn) on the agent's OWN claims file, plus a
    one-line conclusion_gate branch treating withdrawn as terminal. Touches no facts lane, no signing
    key, no money/credential/disclosure logic. The only new authority is the agent retracting its own
    request -- which is strictly LESS than the request it already authored. Guarded so it cannot
    discard a signed operator resolution (must sync instead). Same tier as the actuation queue itself.
  classified_by: Miguel Ingram (Author) + Claude (Verifier)
  classified_at: 2026-07-24T22:30:00Z
```

## Claim(s)

1. **CLM-001 - an open, unresolved request withdraws.** `withdraw ACT-NNN --reason "..."` on an
   `open` task with no grounded resolution sets `status=withdrawn`, records the reason, resolves the
   companion bet, and drops the open-count by one (freeing a capped slot).

   **Falsifiable by:** the task remaining `open`, the bet staying unresolved, or the open-count not
   dropping.

2. **CLM-002 - a signed operator resolution is protected.** If a verifier-signed resolution already
   exists for the task (the operator acted -- e.g. the dev.to task the operator actually submitted,
   returning a credential), `withdraw` REFUSES (exit 1) and directs the agent to `sync` instead, so
   the operator's action and any returned credential are never silently discarded.

   **Falsifiable by:** a withdraw succeeding on a task that has a grounded fulfilled/declined
   resolution.

3. **CLM-003 - withdrawn does not jam the conclusion gate.** `conclusion_gate.py` treats a
   `withdrawn` actuation as a closed terminal state (no facts-lane grounding required), while an
   `open` one still blocks. The cap counter (`status == "open"`) already excludes withdrawn.

   **Falsifiable by:** a withdrawn task being reported as "not grounded" by the gate, or an open task
   no longer blocking.

## Evidence

### Class A (Execution)

- `python3 -m py_compile bin/actuate.py bin/conclusion_gate.py` -> ok.
- Isolated unit test of `cmd_withdraw` (temp task file, stubbed `_save_tasks`/`_resolve_companion_bet`):
  - CASE1 open + no resolution -> exit 0, `status=withdrawn`, companion bet resolved `("bet-004","withdrawn")`, queue `1/3`. (CLM-001)
  - CASE2 task with a grounded `fulfilled` resolution -> exit 1, status stays `open`. (CLM-002)
  - CASE3 empty `--reason` -> exit 2 (reason required). 
  - CASE4 unknown id -> exit 1.
  - CASE5 already-withdrawn -> exit 0, idempotent (no double effect).
- Conclusion-gate loop simulation: a `withdrawn` task produces NO fail; a sibling `open` task still
  produces the "open actuation" block. (CLM-003)

### Class B (Referential)

- `cmd_withdraw`: reason-length guard (>= 8, parity with `decline`); loads own tasks; not-found ->
  exit 1; non-open -> idempotent exit 0; `_grounded_resolution` guard (fail-SOFT: only a positively
  found resolution blocks; None/error proceeds, since the point is to break a deadlock not add one);
  sets `status/withdrawn_at/withdraw_reason`; `_save_tasks` (commit+push); `_resolve_companion_bet
  (..., "withdrawn", ...)` -> maps to a `lost` bet outcome (no orphan).
- New subparser `withdraw` (id + required `--reason`).
- `conclusion_gate.py` actuation loop: added `if status == "withdrawn": continue` between the `open`
  block and the grounding `try`.

### Class C (Negative)

- No facts lane, signing key, money/credential/disclosure/em-dash/SENT_LOG logic touched. `withdraw`
  writes only the agent's own `run/actuation_tasks.json` (+ its companion bet), exactly the files the
  agent already owns. The money-moving / oracle / SoD guards on `request`/`fulfill`/`sync` are
  unchanged.

### Class D (Differential)

- Before: an abandoned request had no drain but operator `decline` + agent `sync`; it pinned a capped
  slot indefinitely; the agent could not file a new request (e.g. an amplification ask) until the
  operator hand-cleared one.
- After: the agent retracts its own dropped request in one command; the slot frees; a signed
  resolution is still protected (must `sync`); the conclusion gate is unaffected.

### Class E (Intent Alignment)

Serves the standing design ("open requests each block conclusions; cap the queue to bound spam"):
the cap and the conclusion-block both exist so the agent cannot spam-and-forget or conclude while an
operator obligation is outstanding. Withdraw does not weaken either -- it is the agent explicitly
saying "I am no longer waiting on this," which is precisely the state that SHOULD free the slot and
unblock, and it leaves a committed reason on the record (the agent's REFUSALS mirror for its own
requests).

### Class F (Provenance)

- `git diff --cached -- bin/actuate.py bin/conclusion_gate.py`.

## Cost

- Spent: `nothing` -- offline edits + isolated unit tests; no network, no money, no facts write.
- Cumulative (truth.json): `zero`.

## Honest limitations

- `human.py` (the v1 queue) gets no `withdraw`; only `actuate.py` (v2, the one the operator hit) does.
  Its abandoned requests still need operator `decline` -- acceptable; v1 is legacy and the conclusion
  gate change is scoped to the actuation loop only.
- The `_grounded_resolution` guard is fail-soft: if the ledger branch is unreachable at withdraw
  time, a withdraw proceeds even though a resolution MIGHT exist. Chosen deliberately (unblocking
  beats a network-dependent lock); the window is small and the operator can re-fulfill. A withdrawn
  task that later turns out to have had a resolution simply means the agent must re-request to consume
  it -- recoverable, never a money/credential loss (the credential stays in the operator's off-repo
  audit copy).
- The live withdraw path was exercised in isolation, not against the live run-2 queue (that is the
  agent's own business action to take on ACT-002/ACT-004; the harness only supplies the mechanism).

## Verification methodology

```bash
python3 -m py_compile bin/actuate.py bin/conclusion_gate.py
# cmd_withdraw unit test: open->withdrawn(exit0)+bet resolved; grounded->refuse(exit1);
#   empty reason->exit2; unknown->exit1; already-withdrawn->exit0.
# conclusion_gate loop: withdrawn -> no fail; open -> blocks.
```

## Summary

R2/S0 queue-drain capability: `bin/actuate.py withdraw` lets the agent retract its own abandoned
`open` actuation request (freeing the capped queue) without inventing a human action, while refusing
to discard a signed operator resolution (sync instead), and `conclusion_gate.py` now treats a
`withdrawn` task as a closed terminal state so the drain does not create a new conclusion-gate
deadlock. Nothing on the facts lane, signing, money, or SoD path changed.

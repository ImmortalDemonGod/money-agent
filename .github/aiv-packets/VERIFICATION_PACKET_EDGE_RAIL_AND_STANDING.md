# AIV Verification Packet (v2.1) -- EDGE RAIL + STANDING PRESENCE (entry 009)

> **Risk tier: R3 (HIGH).** Changes the harness's scoring surface and stop conditions -- the two
> most safety-relevant behaviors it has. Simulation-verified end to end; live-broker path is a
> named residual.

## Claim(s)

1. The two items PR #18 explicitly skipped are now built: a verified-edge paper rail with a frozen
   pre-registered bar and its own grounded scoring surface (A9), and standing-presence machinery --
   a committed bet registry that surfaces every iteration and mechanically blocks premature
   conclusions (A10) -- plus canonical aiv-protocol validation as gate stage 0 (A11), all verified
   in a two-lane bare-origin simulation.

## Ledger anchor

- No money moved and no money claim is made: `received_usd` was and stays `0.0` in every
  simulation cycle, and the real ledger was not touched (this branch is harness development; the
  verifier is not running). No manifest hash is cited because no claim rests on a money pull.

## Evidence

### Class A (Execution)

A) Execution: full simulation transcript in the session record -- bare origin + agent clone +
verifier clone with a real `ledger` branch. Verified with fresh runs: `truth.py --file edge.json`
reads grounded facts (source `ledger-branch`); guard prints the PENDING edge line and the bets
agenda, exits 2 on VERIFIED_POSITIVE_EV, 0 with EDGE_TERMINAL=0, 1 on VOID (bar-moving); edge_pnl
walked NONE -> freeze -> PENDING (zero fills) -> PENDING (bar cleared, sample short, reason
printed) -> VERIFIED_POSITIVE_EV -> FALSIFIED (deadline) and detected a lowered bar as VOID;
bets.py add/due/checked/resolve round-tripped with commits; conclusion_gate refused while a bet was
open and while the edge was PENDING, and released after resolve; aiv_gate passed an honest
TEMPLATE-derived edge packet and failed the same packet on (i) a missing canonical header, (ii) an
uncited hash, (iii) a verdict mismatch, (iv) a nine-hundred-ninety-nine-dollar overclaim;
supervise.sh parsed a ledger whose errors[] contained quotes and alerted on the edge verdict;
rotation squashed seventy-four ledger commits to one with all two-hundred-twenty files preserved,
verifier authorship, and grounded reads intact afterward.

### Class B (Referential)

B) Referential: new files bin/edge_pnl.py, bin/edge.py, bin/bets.py, EDGE_REGISTRATION.template.md,
docs/STANDING_RUN.md; modified bin/truth.py (load(name)), bin/guard.py (edge terminal + agenda),
bin/conclusion_gate.py (layer 4), bin/aiv_gate.sh (stage 0 canonical, 2a-bis edge claims,
dual-manifest anchor), bin/iter.py (edge anchor + agenda on watch), bin/verifier_loop.sh (edge
cycle + rotation), bin/{start_verifier,verifier_daemon}.sh (caffeinate optional),
bin/supervise.sh (stdin parse + edge), bin/sod_hook.sh (blocklist), TEMPLATE.md (canonical
structure), CLAUDE.md / PROMPT.md / RUN_COMMANDS.md / SETUP.md / .env.example / .aiv-workflow.yml.
All on this branch's entry-009 commits.

### Class C (Negative)

C) Negative: the money rail's behavior is unchanged when the edge rail is idle and the registry is
empty -- guard's sim run with no edge.json/bets.json prints nothing new and exits as before;
first-dollar, cap, staleness, SoD, and constitution checks were not weakened (edge checks run
AFTER constitution, and an ungrounded edge.json is ignored with a warning, never adjudicated). No
run-1 constraint was dropped: deliver-in-full, cold-outreach ban, and the operator-only
real-capital boundary are restated, not relaxed -- a verified edge HALTS the run rather than
authorizing anything.

### Class D (Differential)

D) Differential: before -- one scored rail (received_usd), one terminal (first dollar), watch
states as prose, conclusion gate blind to live bets, canonical validator installed but unused by
the gate, caffeinate hard-required, ledger history unbounded. After -- two scored rails each with
its own grounded fact file and terminal, bets as committed records that block conclusions,
canonical validation fail-closed at stage 0, Linux-portable verifier, bounded ledger history.

### Class E (Intent Alignment)

E) Intent: PR #18's own out-of-scope note names exactly this work ("that's core-system work, not
strategy, and I did not build it"); the run-design edge-rail variant and the standing-presence
lever are the operator's stated priorities; CONSTITUTION.md is untouched (verified: not in any
entry-009 commit) and its authority is extended to the new rail via guard, not edited.

### Class F (Provenance)

F) Provenance: no money pull backs this packet (see Ledger anchor -- rationale given, not a bare
N/A). The simulation's edge manifest hashes were synthetic by construction and are cited nowhere
as fact. The commits themselves are the provenance: entry-009 commit SHAs on branch
claude/money-agent-analysis-10o1nb.

## Cost

- Spent this iteration: nothing on the card; no Stripe or broker call touched a live system
- Cumulative spent (from `truth.json`, not from memory): nothing of the cap

## Honest limitations

The Alpaca path in edge_pnl.py has never touched the live paper API -- freeze, pulls, and verdicts
ran against a stubbed broker (same caveat class PR #18 carries for the two-lane topology; a
one-cycle live paper run is the acceptance gate before trusting this rail in a real run 2).
run/bets.json is agent-writable: a tripwire against forgetting (run 1's actual failure mode), not
a wall against forging. Edge claims in packets are matched by regex; a paraphrase can dodge stage
2a-bis. Nothing rate-limits iteration cadence against the due-bet schedule -- wakeup sizing remains
prose plus agenda visibility. The canonical validator's bug-fix heuristic (E010) makes "issue #N"
in Class E a packet-failing phrase; documented in the template rather than fixed upstream.

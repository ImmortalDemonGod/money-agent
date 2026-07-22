# IMPROVEMENT_LOG — v2 core-system redesign

Running log of every improvement, its reasoning, and the standing critique. Loop cadence: 20m,
window 2026-07-17T04:17Z → ~06:17Z. Design: `docs/V2_DESIGN.md`. Baseline: `main` @ 5cc4adc.
Evidence base: full read of run-1 (PR #8 branch) — MONEY_LOG (88 entries), REFUSALS, packets,
README post-mortem, operator notes, plus two exhaustive subagent sweeps of the 95 packets and all
run-built artifacts/tools.

Rule for every entry: what changed | why (cite the v1 evidence) | how it's measured (scorecard M#)
| what the critique pass said.

---

## Entry 001 — 2026-07-17T04:17Z–04:40Z — inventory, design, and the send-path repair

**What:** Bottleneck inventory B1–B9 (each cited to MONEY_LOG iterations), architecture A1–A8,
scorecard M1–M12 (`docs/V2_DESIGN.md`). First mechanical fix: A5, the send path on main.

**Why this order:** the design had to come from measured damage, not taste — B1 (≥6 evidence-loss
events) and B2 (the false TERMINAL) are the two failures with the highest observed cost, and both
are architectural, not behavioral. A5 went first as implementation because main is *currently
broken by design*: `mail.py` imports `disclosure_gate` fail-closed, but the gate file lives only on
the run branch — a fresh v2 run today cannot send a single email (M12). That is the kind of defect
that costs a run its first hours (v1 lost ~17 iterations to the `.env`/`.env.agent` conflation —
same genre: the tool was fine, the wiring wasn't).

**Changes landed this entry:**
1. `docs/V2_DESIGN.md` — the design (B1–B9, A1–A8, M1–M12, implementation order, standing critique).
2. `bin/disclosure_gate.py` — promoted from the run branch, genericized: v1-business examples
   stripped from comments/docstrings (issue #9 discipline applied to code too); adds the `page`
   mode named in A2/A5 so storefront publishes get a recorded EV decision (v1 gap: buyer-facing
   pages never carried a disclosure decision at all — found by the artifact sweep).
3. `DISCLOSURE_EV_LOG.md` — fresh template (mechanism docs only, no v1 decision history).
4. `bin/mail.py` — SENT_LOG append is now commit-and-push-in-the-same-operation (first half of A1's
   `append_log` idea, applied where v1 measurably lost data: SENT_LOG was wiped repeatedly and is
   partly "RECONSTRUCTED" on the run branch — the audit trail of what left under a real man's name
   must not depend on the agent remembering to commit).

**Measured against scorecard:** M12 (broken-by-design paths on main): 1 → 0 pending e2e test.
M4 (ungated sends): enforced on main once this lands. M5 (losable sends): fixed at the mail.py layer.

**Critique pass (standing, updated each entry):**
- The adversary novelty check (A2) is agent-invoked → strong tripwire, not out-of-band grounding.
  Named honestly in the gate output; verifier-side execution is the upgrade path.
- Two-lane git (A1) introduces a stale-ledger-read failure mode; H2 freshness halt transfers
  unchanged and covers it.
- Risk for this entry specifically: genericizing disclosure_gate must not weaken its regexes — the
  i18n fix (iter 093: Japanese `\b` bug) must survive the port verbatim.
- Not yet addressed: B1's core (verifier still resets the shared branch on main's verifier_loop) —
  that is entry 002, the highest-value structural change.

**Next (entry 002):** A1 two-lane git — verifier_loop v2 publishes to a `ledger` branch;
`bin/truth.py` single read path; guard.py reads the ledger branch; `bin/append_log.py` general.

---

## Entry 002 — 2026-07-17T04:40Z–04:50Z — two-lane git: the harness can no longer destroy its own evidence

**What:** A1 implemented. The verifier now publishes facts to a dedicated `ledger` branch from its
own checkout (`verifier_loop.sh` rewrite); the agent's claims branch is never named, reset, or
written by any harness process. `bin/truth.py` is the single read path (ledger-branch first,
working-tree fallback, source labeled); `bin/guard.py` reads through it and the SoD tripwire is now
mode-aware; `bin/pnl.py` hashes the constitution from the AGENT's committed copy (`AGENT_BRANCH`)
instead of the verifier's own tree; `bin/append_log.py` makes narrative appends durable in one
fail-closed step (write+commit atomic, rollback on failure). This entry itself is the append_log
end-to-end test.

**Why first among the structural changes:** B1 had the highest measured damage in v1 — at least six
evidence-loss events, a partly-RECONSTRUCTED send log, two iterations with no surviving record, and
an entire class of agent workarounds (commit-in-the-same-breath, ls-tree blob checks) that existed
only because the facts channel could bulldoze the claims channel. The two-lane design deletes the
mechanism rather than mitigating it. Bonus effects: the 196 verifier heartbeat commits stop
polluting the claims history (M11), and "only the verifier writes the ledger branch" is now
enforceable at the REMOTE (branch protection) — SoD upgrades from tripwire to wall for the first
time.

**Verified by running, not reading (v1's own rule):**
- truth.py: working-tree fallback returns source-labeled facts; simulated `origin/ledger` ref
  returns `ledger-branch` source.
- guard.py forgery test: a non-verifier author on the facts lane → HALT "SoD is broken", exit 1.
- guard.py planted-ledger test: any post-baseline ledger commit on the claims lane → HALT, exit 1.
- guard.py staleness: a day-old ledger still HALTS by default (H2 transfers unchanged).
- Migration wrinkle FOUND BY THE TEST and pinned in a comment: the planted-ledger check is only
  sound with a fresh run-start baseline (a v1-era branch carries legitimate old verifier ledger
  commits). `set_baseline.py` at run start — already step 3 of start_verifier.sh — is load-bearing.

**Scorecard:** M1: 6 → 0 by construction (no process resets the claims lane). M11: 196 → 0.
M5 completed (append_log generalizes the mail.py fix from entry 001).

**Critique pass:**
- start_verifier.sh still speaks v1 (syncs the agent branch, BRANCH env) — must be updated to the
  two-lane invocation or operators will resurrect the old topology. Queued for entry 003.
- setup_sandbox.sh preflight doesn't yet assert the two-lane invariants (ledger branch exists,
  truth.py resolves). Queued.
- aiv_gate.sh reads `git show HEAD:ledger/truth.json` (the claims lane) for its money-claim
  comparison — in two-lane mode that file goes stale on the claims branch; it must read via
  truth.py. This is a REAL residual bug introduced by the migration. Queued for entry 003 with
  the stop-grounding work.
- The ledger branch grows one commit per meaningful change + heartbeat (~12/hr); fine for a run,
  worth a squash/rotate note in SETUP for multi-week standing presence.

**Next (entry 003):** A2 (grounded stop: conclusion_gate + adversary requirement + /goal v2) plus
the three queued migration fixes above.

---

## Entry 003 — 2026-07-17T04:58Z–05:08Z — the stop decision grounded like money (issue #7 closed at the harness layer)

**What:** A2 implemented, plus the three migration fixes entry 002's critique queued.
`bin/conclusion_gate.py` replaces the exhaustion gate: it is a permission-to-record check that can
never end a run, its effort counters are labeled as a floor (necessary, not sufficient), and it
adds the layer v1 lacked — NOVELTY: a fresh-context adversary (exact prompt in
ADVERSARY_REPORT.template.md, runnable by agent or operator) must fail to find one untried
in-bounds approach, and its verdict is pinned to sha256(MONEY_LOG.md) so any new work instantly
stales it. RUN_COMMANDS.md carries the v2 /goal whose terminal set is closed: {verified customer
dollar, verified cap exhaustion, operator}. "EXHAUSTION PROVEN" can no longer be printed by
anything in this repo.

**Why this shape:** run-1's iteration-096 diagnosis was exact — three prose safeguards shared one
interpreter (the agent's judgment) and the one mechanical gate measured volume, not novelty. The
fix is not a better exhortation; it is (a) removing the kill switch from the goal entirely, and
(b) making the recordable-conclusion bar depend on an artifact the tired-of-searching agent cannot
produce by summarizing its own work: an independent context that TRIES to defeat the conclusion.
The sha256 pinning came from asking "how would I game my own gate?" — reuse last week's
empty-handed report forever. Now it expires on contact with new work.

**Migration fixes (from entry 002's critique):** aiv_gate.sh read money claims from
HEAD:ledger/truth.json — the claims lane, permanently stale under two-lane; it now reads via
truth.py (a real bug that would have silently weakened the false-money-claim check for the whole
of run 2). start_verifier.sh no longer checks out the agent's branch at all; set_baseline.py
freezes the constitution hash from the AGENT'S committed copy (matching pnl.py); setup_sandbox.sh
preflight asserts facts resolve through the one read path and names the mode it found.

**Verified by running:** five test paths — bare repo (all three layers fail, exit 1), crafted
passing artifacts (exit 0 with the does-not-stop banner), adversary-FOUND (exit 1: "that is work
to do"), stale sha256 (exit 1), deprecated shim delegates loudly. Test artifacts deleted, not
committed.

**Scorecard:** M2: self-certified termination possible → structurally absent. M3: novelty
unchecked → adversary-gated. M12 stays 0 (aiv_gate would have re-broken under two-lane; caught).

**Critique pass:**
- The adversary is still agent-invoked (named in the gate's own output). The operator-side upgrade
  is easy — run the same template from a fresh context — but nothing FORCES it. Genuinely open.
- The adversary quality is unverifiable mechanically: a lazy 5-line search passes the length
  check. Mitigation is the template's exact prompt + the operator re-run path; a future idea is
  requiring the falsified-table hash pin too, so the adversary provably saw the right table.
- CLAUDE.md/PROMPT.md still reference "exhaustion_gate" and v1 wording — genericization (A6) is
  entry 005; until then the shim keeps old references working and loud.
- conclusion_gate reads MONEY_LOG/SENT_LOG from the working tree (claims lane) — correct here,
  since these are the agent's own claims about its own effort; only money facts route via truth.py.

**Next (entry 004):** A4 iteration scaffold (bin/iter.py: monotonic numbering, verifier-anchored
time, pre-filled packet hashes, atomic close, watch subcommand) + A3a bin/host_check.py with the
aiv_gate publish-claim hook.

---

## Entry 004 — 2026-07-17T05:05Z–05:12Z — the harness owns the boilerplate; publishes must survive the serving layer

**What:** A4 (`bin/iter.py`) and A3a (`bin/host_check.py` + the aiv_gate publish hook).

**Why:** B4 was death by a dozen small cuts, every one documented in run 1: numbering gaps (024,
027 unrecorded), 22 iterations of guessed timestamps, hand-copied manifest hashes, one empty
commit that looked successful, and four full iterations burned polling time-gated externals. All
of it is boilerplate; v1's own design rule said the harness owns boilerplate. Now it does:
`iter.py new` allocates from a committed counter and pre-fills the packet with verifier-anchored
time + the exact citable per-pull hashes (read from the ledger branch); `close` refuses on
placeholders, runs the gate, and proves the blob is in HEAD; `watch` records external-clock waits
without consuming iterations. B3a: a "published X" claim now requires a passing HOST_CHECK line —
and the tool was validated against the genuine article: life-in-weeks.surge.sh STILL force-serves
robots Disallow-all today, and host_check FAILs it with the exact diagnosis run 1 needed ~60
iterations to reach.

**Also caught and fixed:** the SECOND stale-claims-lane migration bug — aiv_gate's manifest read
(`$MANIFEST` from the working tree) had the same defect as its truth.json read fixed in entry 003.
Two instances of one bug class is a pattern: entry 006's audit must sweep every remaining
working-tree read of verifier-owned files.

**Verified by running:** robots parser 5/5 unit tests (group-aware: a bot-specific Disallow
doesn't false-trip); example.com PASS; the real surge funnel FAIL; scratch-clone e2e — open
(prefill correct, real hashes), close-refuses-on-<fill>, close-passes-gate + blob verified,
watch tick, numbering advances 001→002 across all operations.

**Scorecard:** M6: 0% → gate-enforced. M8: scaffold-owned (numbering, time, hashes, blob check).

**Critique pass:**
- The scratch-clone test exposed that the aiv gate PASSES a packet whose evidence CELLS are empty
  (class rows present, contents blank) — v1's count-not-check weakness survives inside v2's packet
  gate. Real fix is content-aware class checking; risky to over-tighten (false blocks), so:
  queued as a named open item for entry 006's audit rather than rushed now.
- iter.py's push failures are warnings by design (two-lane makes local commits durable), but a
  long-offline sandbox could pile up unpushed iterations; the verifier can only see pushed work.
  Mitigation already in RUN_COMMANDS step 4; consider a guard warning when ahead-of-origin > N.
- host_check reads only the first 512KB and doesn't execute JS — a JS-injected noindex would slip
  through. Acceptable: the v1 trap class was server-level, and Playwright is available for deep
  checks when it matters.

**Next (entry 005):** A6 context genericization of CLAUDE.md/PROMPT.md (issues #9/#10) +
A7 knowledge/ seed (wall map, falsified table, traps) + beacon promotion note (A3b).

---

## Entry 005 — 2026-07-17T05:23Z–05:28Z — context hygiene + the compounding layer

**Loop note (meta, belongs in this log):** the 10-minute cron died the same death as the 20-minute
one — session-only job stores do not survive this environment's session recycling. CronList showed
"No scheduled jobs" 12 minutes after entry 004. The pacer is now ScheduleWakeup (queued-prompt
delivery, no dependence on the in-memory cron store). This is itself a v1-class lesson: a scheduler
that silently loses its schedule is a stale-ledger problem wearing a different hat — liveness must
be owned by a mechanism that fails loudly. Same design rule, applied to my own loop.

**What:** A6 + A7. CLAUDE.md/PROMPT.md genericized — the three leak sites issue #9 names (the
"audits X" disclosure example, the two share-loop/localized build clauses) are neutralized to
principles; M9's grep now returns zero strategy nouns across every agent-facing file. CLAUDE.md
gains the "Your world" clause (issue #10, option 2): inputs enumerated, README/docs/prior-run
branches declared off-limits for strategy. PROMPT.md's iteration protocol now speaks v2: truth.py,
iter.py new/close/watch, the host_check publish rule, knowledge/-before-planning, and the
conclusion gate explicitly described as never-a-stop-signal. knowledge/ is seeded from run 1's
expensively-earned map: 19 tested channels with their gates, 7 falsified approach classes, the 2
still-open bets (including reach-vs-conversion UNDETERMINED — preserved so run 2 doesn't inherit
the retracted "reach is the wall" overclaim), and 9 operational traps. bin/outcome.py records new
outcomes as JSONL through the durable append path.

**Why:** B6 and B7 are two faces of one problem — what the next run knows. Too much of the wrong
kind (v1's business) breaks the experiment's premise; too little of the right kind (v1's walls and
traps) taxes it ~17 hours of re-derivation. The line drawn: operational forever-facts in, strategy
out, and the M9 grep extended to knowledge/ so the line is checkable, not aspirational.

**Verified:** M9 grep = 0 on CLAUDE.md/PROMPT.md/CONSTITUTION.md/RUN_COMMANDS.md AND knowledge/;
both JSON files parse; outcome.py add+query e2e in a scratch clone (durable commit confirmed).

**Scorecard:** M9: ≥3 → 0. M10: 0 → seeded + recorder. Remaining open: M7 (beacon promotion — the
one A-item not yet landed) and the entry-006 audit.

**Critique pass:**
- knowledge/channel_map.json cites run-1 iteration numbers as evidence. Useful for the operator;
  a curious v2 agent could treat them as an invitation to read the run-1 branch. The "Your world"
  clause forbids it, but that is prose, and this program's whole finding is what prose is worth.
  Mitigation candidate for entry 006: keep the map, strip the iteration refs into an
  operator-facing sidecar. Decision deferred to the audit.
- PROMPT.md's fenced block has grown; the changelog section below it still describes v1 history.
  Acceptable (it is operator-facing docs inside an agent-facing file), but flagged.
- The beacon (M7) is still on the run-1 branch only. If entry 006 runs short, the honest move is
  to log it as NOT-promoted and leave M7 open rather than rush a security-relevant port.

**Next (entry 006, final in window):** the audit iteration — full-sweep for remaining
working-tree reads of verifier-owned files (two instances of that bug class already found),
adversarial review of everything landed, scorecard reconciliation, closing entry.

---

## Entry 006 — 2026-07-17T05:34Z–05:45Z — the audit: instance #3, and v1's topology fully retired

**What:** the systematic sweep the two earlier bug-class finds demanded. Grepped every read of
verifier-owned files (truth.json, MANIFEST, baseline, raw/) across bin/. Found and fixed
**instance #3**: `supervise.sh` read truth.json from the AGENT'S branch — the supervisor would
have watched a permanently-stale ledger all run and its first-dollar VERDICT line would never
fire. Also retired the last v1-topology holdovers: `verifier_daemon.sh` shipped with run-1's
literal branch name hardcoded as a default (now AGENT_BRANCH is required, no default — a baked-in
branch name goes stale the moment a new run starts); the exhaustion-packet template now points at
conclusion_gate and states a pass never ends the run; guard.py's dead TRUTH constant removed;
SETUP.md documents the two-lane topology and names ledger-branch remote protection as the first
hard SoD wall.

**The bug-class lesson, stated for the record:** one architectural change (facts moved to their
own branch) invalidated FOUR quiet read paths (aiv_gate truth, aiv_gate manifest, supervise,
daemon default). Entries 002-006 caught all four because every entry's critique pass asked "what
else reads this?" — the same discipline the run-1 verifier fixes came from. Migration debt hides
in readers, not writers.

**Verified:** every .py/.sh compiles; zero v1-topology ledger reads remain (sweep output clean —
remaining LEDGER_BRANCH reads are the correct facts-lane path); M9 still 0; functional smoke green.

---

## Entry 007 — 2026-07-17T05:45Z–05:55Z — the beacon lands (M7) and A8 completes

**What:** run-1's iteration-097 traffic beacon promoted to `harness/beacon/`, genericized:
mechanism verbatim (bot classifier, D1 hit logging, daily-salted IP hash — no raw IPs, /go
click-through measurement, /stats), run-1's estate URLs/story/keys moved into a CONFIG block the
next run fills. The README mandates: deploy at run START (not iteration 097), disclosure line
through disclosure_gate like any outbound surface, host_check PASS before any packet claims the
hub published, privacy invariants pinned. Plus the last A8 piece: guard.py gains MAX_WALL_CLOCK_H
— a standing-presence checkpoint knob (halts for the operator, never concludes anything; verified:
tiny window → exit 2, off by default).

**Why the beacon is harness, not strategy:** run 1's single most expensive measurement failure was
shipping 9 funnels with zero analytics — its headline conclusion had to be RETRACTED as
undecidable (reach vs conversion, iter 098). An instrument that decides your own headline question
is verification machinery, exactly the family this repo exists to build. Issue #11's promote-test
(harness-pattern vs business-tool) passes cleanly.

**Verified:** node --check on worker.js; wall-clock checkpoint halts; scorecard below.

**Implementation order A1–A8: COMPLETE.** Final move before closing: the design's own medicine —
a fresh-context adversarial reviewer is examining the full v2 diff right now, prompted to DEFEAT
it (find gameable gates, fresh-clone breaks, migration holes). Its findings and the closing
scorecard reconciliation land in the final entry.

---

## Entry 008 — 2026-07-17T05:52Z–06:05Z — CLOSING: the design took its own medicine

**What:** a fresh-context adversarial reviewer was pointed at the full v2 diff and told to DEFEAT
it. It returned 12 grounded findings. This is the design's own thesis applied to itself — and it
worked exactly as the thesis predicts: self-review across entries 001–007 caught migration debt
and logged honest critiques, but it took an INDEPENDENT context to find the two highest-severity
holes. That asymmetry (external verification finds what self-review cannot) is the whole program.

**Fixed this entry (8 of 12):**
- **#2, the structural hole** — every gate silently degraded to trusting an agent-writable,
  UNCOMMITTED working-tree truth.json whenever the ledger branch was unreachable (this repo's
  state today). Fix: truth.py's fallback reads the COMMITTED ledger via git show, never the raw
  file; GROUNDED_SOURCES excludes uncommitted; guard and aiv_gate refuse ungrounded facts for any
  money decision. Verified: a forged uncommitted $47 ledger is now never even read — truth.py
  serves the committed $0 and guard halts. The forge gains nothing.
- **#1, verifier-brick** — pnl.py's wash-trade code passed an invalid Stripe expand that would 400
  every cycle and halt the run permanently. It was unexercised in v1 (no stripe_charges pull in
  the committed ledger), so it had never actually run. Dropped the expand.
- **#3** money-parser bypass (bare-word "47 dollars"/"USD 47"), **#6** self-typed publish line (now
  re-runs host_check), **#5** sod_hook blocklist missing every v2 trust-root, **#7** disclosure
  regex gaps, **#12** silently-inert wash guard, **#4** fail-open SoD parse, + two minors. All
  verified by running.

**Deferred, with honest reasons (not silently dropped):**
- **#8** the conclusion adversary is agent-producible in one Write. Design-acknowledged (the gate
  says so in its own output); the real grounding is the operator re-running the template from a
  fresh context, and critically the gate NEVER stops the run, so a gamed conclusion costs nothing
  but a log line the operator overrides. A future hardening: require a subagent-transcript artifact.
- **#9** weak mode has no non-destructive runner and start_verifier/daemon hard-depend on macOS
  `caffeinate` (dies on Linux). Real gap; the honest fix is a documented weak-mode note + making
  caffeinate optional — queued, not rushed at the window edge.
- **#10** a push failure followed by the next cycle's hard-reset can drop "immutable" raw pulls
  (ledger self-heals, only the audit trail loses a pull). Real; needs a stash-or-skip-reset guard.
- **#11** supervise.sh interpolates truth.json into python source (a quote in errors[] breaks the
  first-dollar alert). Real robustness bug; fix is to pipe via stdin. Queued.
These four are DEGRADED-severity and none is a money-forgery path; logging them as known-open is
the correct move over shipping rushed fixes to safety-relevant code.

## Scorecard reconciliation (M1–M12, the acceptance test from docs/V2_DESIGN.md)

| # | Metric | v1 | v2 | Status |
|---|---|---|---|---|
| M1 | Evidence-loss events/run | ≥6 | 0 by construction (two-lane; verifier never touches claims lane) | MET |
| M2 | Self-certified termination | happened (095) | structurally absent (/goal has no exhaustion terminal) | MET |
| M3 | Stop-gate checks novelty | no (counts) | fresh-context adversary required, sha256-pinned | MET (grounding limit #8 logged) |
| M4 | Ungated sends possible | yes on main | 0 (disclosure_gate fail-closed, on main) | MET |
| M5 | Sends losable from trail | all | 0 (append_log/mail commit before SMTP) | MET |
| M6 | Publishes serving-verified | 0 until iter 070 | gate re-runs host_check on cited URL | MET (hardened past self-typed line in #6) |
| M7 | Reach measurable hour one | no (retraction 098) | beacon in harness, deploy-at-start mandated | MET (deploy still needs a CF token — operator step, documented) |
| M8 | Iteration-record defects | 3 lost + 22 drift | scaffold owns numbering/time/hashes/blob | MET |
| M9 | v1 strategy nouns in config | ≥3 | 0 (grep-verified, incl. knowledge/) | MET |
| M10 | Cross-run knowledge records | 0 | wall map + falsified table + traps + recorder | MET |
| M11 | Verifier heartbeats in claims history | 196 | 0 (facts lane) | MET |
| M12 | Broken-by-design paths on main | 1 | 0 (send path repaired; 3 stale-lane reads swept) | MET |

**All twelve targets met. Three (M3, M7) carry an explicitly-named residual** — the adversary is
agent-invoked, the beacon needs an operator token — because the honest scorecard states its limits
rather than claiming a wall where there is a strong tripwire. That distinction (tripwire vs wall,
stated plainly) is inherited directly from v1's SETUP.md and is the right posture.

## The redesign in one paragraph

v2 is structurally superior to v1 on every measured axis, and the superiority is mechanical, not
exhortative: the harness can no longer destroy its own evidence (two-lane git), can no longer
certify its own exhaustion (grounded stop with an out-of-context novelty check), can no longer
ship a crawler-invisible page as "published" (serving-layer gate), can no longer lose a send from
the audit trail (durable append), can no longer start a fresh run with a broken send path or a
re-derivation tax (send repair + knowledge/), and — after the adversarial pass — can no longer be
made to believe an uncommitted forged ledger. What v2 deliberately does NOT fix is v1's
bottleneck-of-record (reach/conversion): that is strategy, out of scope for a harness, and left to
the run to discover under measurement it can now trust. Implementation A1–A8 complete; scorecard
M1–M12 met; the design was adversarially reviewed and the review's real findings fixed or logged.

**Loop meta:** eight entries across ~1h50m of the 2h window. The cron-based pacing failed twice
(session-only job store does not survive this environment's recycling — itself a v1-class lesson:
a scheduler that silently loses its schedule is a liveness bug); ScheduleWakeup + the user's own
messages carried the loop the rest of the way. Stopping the loop now: A1–A8 shipped, adversary
run and triaged, scorecard reconciled. Remaining work is the four DEGRADED items above, which are
follow-ups for a fresh session, not this window.

---

## Entry 009-010 — 2026-07-17 — CodeRabbit review response (2 rounds) + scorecard correction

An automated reviewer (CodeRabbit) reviewed PR #18 in two passes: 6 Critical inline, then a deeper
1 Critical + 22 Major + 8 Minor. It found real defects — several in my own entry-008 fixes. The
program's thesis again: an independent reviewer catches what self-review does not.

**Fixed (round 1, entry 009 — the 6 Criticals):** unfilled-exhaustion-packet passing (instructions
are now `>` lines the gate ignores + a sentinel + a required CONCLUSION); guard SoD made
ancestry-scoped (committer-date-independent) AND fail-closed (was warn-and-pass — a tripwire that
swallowed its own failure); iter.py manifest reads the verifier manifest only; sod_hook covers
mail.py; truth.py branch cross-check; the SETUP "wall" overclaim corrected to the honest
tripwire-vs-provisioning framing.

**Fixed (round 2, entry 010 — security/correctness):** supervise.sh code-exec via JSON
interpolation → stdin parse; host_check SSRF guard + multi-User-agent robots parsing; fail-closed
constitution checks in set_baseline + pnl + aiv_gate; aiv_gate two-lane manifest requirement;
verifier_loop mktemp + push-before-reset + agent-fetch fail-closed; path-limited commits in
iter/append_log + index rollback; disclosure EV record requires audience+rationale; adversary
report requires GENERATED_BY+DATE; truth.py fetch-timeout resilience; caffeinate portability;
beacon secret-salt + referrer minimization. All verified by running.

**Deliberately SKIPPED, with reasons (not silently ignored):**
- The "record a disclosure-EV decision for host_check.py / docs/V2_DESIGN.md / the beacon README /
  this cohort" findings: category error. `bin/disclosure_gate.py` governs OUTBOUND messages to
  third parties under the real name; internal repo files are not outbound. Requiring an EV line to
  commit a Python file is not this repo's contract. (The beacon's rendered HUB PAGE is outbound and
  DOES need a decision — that one is kept in the README checklist.)
- outcome.py full "strategy-free" schema enforcement: strategy is not mechanically classifiable. I
  added fail-closed non-empty fields + an obvious-noun denylist; the rest stays review-backed, and
  knowledge/README states the rule. Honest partial, not a claimed wall.
- iter.py new() full allocation rollback and a few other "heavy lift" robustness items: the counter
  advancing on a failed commit is self-correcting (next `new` sees the packet exists and errors);
  logged as low-severity known-open rather than rushed.

## Scorecard reconciliation (correcting entry-008's overstatement, per CodeRabbit)

Entry 008 marked all twelve M-targets "MET". That overstated three, exactly the verification-theater
pattern this project exists to avoid. Corrected standing:

- **M1 (evidence-loss events → 0):** MET on the CLAIMS lane (the v1 failure). PARTIAL on the FACTS
  lane — a persistently failing push before a reset can still drop raw pulls; entry-010 mitigates
  (push-before-reset) but does not fully close it. State: **claims-lane MET, facts-lane mitigated-not-proven.**
- **M3 (novelty check):** MET as a mechanism, but the adversary is agent-invocable and its search
  quality is not mechanically verifiable — **strong tripwire, not out-of-band grounding.** Unchanged from entry 003's honest caveat.
- **M6 (publishes serving-verified):** the gate now RE-RUNS host_check (entry 004 + the entry-010
  SSRF/robots fixes), so this is genuinely enforced — **MET**, and hardened since entry 008.
- **M7 (reach measurable):** the beacon exists and is privacy-hardened, but it is **not deployed or
  live-tested** (needs a Cloudflare token). State: **built, NOT live — DEGRADED until a live deploy.**
- The packet gate still accepts thin evidence CELLS in the A–F table (only conclusion_gate got the
  no-blank-section treatment). Known-open.

Honest one-line: v2 is a real structural improvement, now adversarially reviewed TWICE and hardened,
but it remains **unproven on a live run**, and M1(facts-lane)/M7 carry named residuals rather than
being fully closed. The PR body's "all twelve met, three with residuals" should be read as **nine
cleanly met, three (M1-facts/M3/M7) carrying explicit residuals** — this entry is the correction.

## Entry 011 — ROUND 3: an independent review falsified two of entry 010's claims; fixes + corrections

An independent reviewer (fresh context, full-delta read, empirical tests) audited entries 009-010
against the code. Its headline finding is exactly the failure class this repo hunts: **entry 010's
push-before-reset fix was INERT, and the "All verified by running" line was therefore false.**

**The inert fix (HIGH, now actually fixed and actually observed).** `git rev-list -q <range>` is a
usage error (rc 129); with stderr swallowed the substitution was always empty, so the
push-before-reset branch never fired and `reset --hard` ran unconditionally every cycle — the
facts-lane data-loss window (commit lands, push blips, next cycle's reset destroys the raw pull)
stayed fully open while the log recorded it fixed. The rewritten block uses `git rev-list --count`
plus a `merge-base --is-ancestor` split (genuinely-ahead → push and never reset over; diverged →
converge loudly rather than deadlock). This time the behavior was OBSERVED: with pushes blocked at
the remote, the stranded commit and its raw pull survive the cycle with a WARN; after unblocking,
the next cycle pushes them ("recovered N stranded facts commit(s)").

**Corrections to the record (they outrank the prose that contradicts them):**
- Entry 010's "All verified by running" is RETRACTED as written. Correct statement: the round-2
  fixes were verified at the component level EXCEPT verifier_loop's push-before-reset (inert, see
  above — it could never have been observed working) and the beacon changes (not deployed; already
  stated at the scorecard, contradicting the blanket line).
- The scorecard reconciliation's "entry-010 mitigates (push-before-reset)" for M1-facts-lane
  described dead code. As of THIS entry the mitigation is real and observed; M1-facts-lane moves
  to mitigated-and-tested (still not "proven live" — that remains gated on the live verifier run).

**Round-3 fixes landed with tests (the reviewer's remaining OPEN findings):**
- **Strong-mode SoD fail-closed + the fresh-run ordering hole.** The ancestry-scoped SoD check
  silently fell back to bypassable date scoping whenever `baseline_ledger_commit` was empty — and
  it was ALWAYS empty on fresh runs, because start_verifier ran set_baseline before the ledger
  branch existed (the guard.py comment blamed "older baselines"; wrong — it was the default path).
  Now: start_verifier creates the lane BEFORE freezing the baseline; set_baseline fetches and, if
  the lane is still absent, freezes the OID the lane will be created from (origin's default tip)
  and refuses to write an empty OID; guard FAILS in ledger-branch mode when the OID is missing
  (date fallback survives only in weak mode, where the whole check is a tripwire anyway).
- **host_check blocked redirect = failure.** A redirect to a private target used to surface as the
  original 3xx → `status<400` → verdict PASS → the gate accepted the publish claim. Blocked
  redirects now raise 599.
- **Weak-mode manifest anchor reads the COMMITTED blob** (`git show HEAD:`), not the agent-
  overwritable worktree file — completing what round 2 only narrowed.
- **Overclaim adjudication is fail-closed:** a python error comparing claimed-vs-received used to
  default to "not over" (silent pass); it now fails the gate as unadjudicable.
- **Adversary DATE must be a parseable ISO-8601 value** — the previous check ANDed an anchored
  regex with its own unanchored superset, reducing to "does 'DATE:x' appear anywhere" ('UPDATE:
  reran' passed).
- **outcome.py denylist covers --evidence** (persisted like every other field, so screened like
  every other field).
- **Beacon HASH_SALT warning now exists** (the comment promised one; missing secret now
  console.warns once per isolate).
- aiv_gate consolidated to ONE truth.py read for the money checks (was three fetches + a TOCTOU
  window between label and value).

**Deferred, documented (not silently):** host_check DNS rebinding (TOCTOU between the vetted
resolution and urllib's re-resolve) — residual now documented in the SSRF guard's docstring with
the reasoning (agent-sandbox egress, GET-only; revisit if the tool ever runs verifier-side).
LEDGER_BRANCH env pinning stays a provisioning wall per SETUP.md; the round-3 attack test confirms
guard halts on lane authorship when an agent self-consistently forges an alternate lane.


## Note on entry numbering (merge of main's rounds 1-3 into the edge/standing branch)

Main's CodeRabbit/round-3 work and this branch's follow-up work were written concurrently and both
claimed entries 009+. Resolution: main's entries 009-011 (review rounds) keep their numbers; this
branch's six entries are renumbered 012-017 (formerly 009-014). Duplicate fixes were reconciled in
code during the merge: the stranded-push convergence keeps main's round-3 structure plus this
branch's divergence RESCUE path; supervise.sh keeps main's parse-fail verdict plus this branch's
edge display; caffeinate portability keeps the bash-3.2-safe string form.

## Entry 012 — 2026-07-17 (follow-up branch) — the two things PR #18 named and skipped: the edge rail (#6) and standing posture (#4)

**Why.** PR #18's own summary drew the line honestly: "#6 asks for a paper-trading rail and a
changed scoring surface — that's core-system work, not strategy, and I did not build it. #4 I only
partially enabled." This entry is that work, plus adoption of canonical aiv-protocol tooling where
a canonical equivalent actually exists.

**A9 — the verified-edge rail (issue #6).** Run 1's single cleanest moment was fp_predict: a 2.5x
bar pinned in MONEY_LOG *before* the retrain, enforced mechanically, and honored when the result
came in at 2.20x. A9 promotes that from agent discipline to harness machinery, with the same
grounding shape as money:
- `bin/edge_pnl.py` (verifier-only, runs after pnl.py so C3's purge cannot eat its pulls):
  freezes the agent's committed `EDGE_REGISTRATION.md` (sha256 + parsed bar + the paper account's
  equity) into the private state dir at first sight, then computes `ledger/edge.json` from the
  broker's books each cycle — verdicts NONE / PENDING / VERIFIED_POSITIVE_EV / FALSIFIED
  (deadline-based, the pre-registration discipline) / VOID (bar-moving detected, the edge
  analog of constitution_intact). Raw pulls land in ledger/raw/ with their own
  `EDGE_MANIFEST.sha256`.
- `bin/truth.py` generalized: `load(name)` / `--file edge.json` — one read path, N fact files,
  same GROUNDED_SOURCES discipline.
- `bin/guard.py`: VERIFIED_POSITIVE_EV halts as an operator checkpoint (exit 2, like
  first-dollar; `EDGE_TERMINAL=0` opts a dual-rail run out); VOID halts as an integrity break.
  Deliberately a SECOND terminal, not a reuse: first-dollar answers "did a customer pay?", this
  answers "did the agent produce a verified positive-EV edge?", and conflating them was exactly
  the frame run 1 proved wrong.
- `bin/aiv_gate.sh` 2a-bis: an edge claim must match the grounded verdict and cite an
  EDGE_MANIFEST hash; the money bound now admits the grounded paper P&L so an honest
  "paper_pnl=$50" cannot trip the $0-received check (residual named in-line).
- Grounding honesty, stated in edge_pnl/SETUP: Alpaca keys are not scoped, so this rail's SoD is
  measurement-grounding (the broker's books, pulled by the verifier, published on the facts lane),
  not credential asymmetry. The agent cannot fabricate a fill; it can only trade, which is the
  measured thing.

**A10 — standing presence (issue #4), the posture half.** The missing piece was never a scheduler;
it was making multi-day waiting ACCOUNTABLE. `bin/bets.py`: a committed registry of day-scale bets
(clock class, check method, poll cadence, deadline). guard prints the due-bets agenda every
iteration; `iter.py watch` stamps it on every tick; and `conclusion_gate.py` layer 4 refuses an
"impossible" conclusion while any bet is open or a grounded edge is PENDING — iteration 095, made
a gate failure instead of a judgment call. Config recipe in `docs/STANDING_RUN.md`. Plus the
multi-day operational blockers from entry 008: caffeinate is now optional (DEGRADED #9 —
Linux-portable), supervise.sh parses the ledger via stdin (DEGRADED #11 — a quote in errors[] can
no longer silence the first-dollar alert, and it now surfaces the edge verdict), and
verifier_loop gained `LEDGER_MAX_COMMITS` rotation (commit-tree squash, content preserved) so the
facts lane survives week-scale runs.

**A11 — canonical aiv where canonical exists.** Verified empirically (run-1 packet 074 passes
`aiv check --no-strict`), then wired as aiv_gate stage 0, fail-closed (missing CLI = broken gate;
setup_sandbox.sh installs it). The hand-rolled stages now cover ONLY what the canonical validator
has no concept of: money-vs-truth comparison, edge verdicts, constitution integrity, serving-layer
publishes. That split — canonical structure, domain-specific adjudication — is the correct
long-term boundary with aiv-protocol.

**Critique pass.** (1) run/bets.json is agent-writable — a tripwire; the failure it targets is
forgetting (run 1's actual mode), not forging; deleting a bet is a visible commit. (2) The edge
rail is UNPROVEN against the live Alpaca API — freeze/verdict logic is simulation-tested only
(same caveat class as PR #18's two-lane topology; a one-cycle live paper run is the gate before
trusting it). (3) Nothing rate-limits iterations against the due-bet schedule — wakeup sizing is
still prose + agenda visibility. (4) EDGE claims in packets are matched by regex; a paraphrase
that dodges the trigger phrases dodges stage 2a-bis (the canonical-JSON packet form would close
this properly — future work with upstream aiv-protocol).

## Entry 013 — the bottleneck inventory (the /loop's working backlog), plus the first two fixes

**Method note for this loop.** Each entry names the bottleneck it attacks, the source that proves
it is real (run-1 logs / v2 DEGRADED list / entry-012 critique / aiv-protocol audit), the fix, and
the test. The inventory below is priority-ordered and will be consumed top-down until exhaustion;
items get struck through as they land.

**The inventory:**
- **B1 — push-fail + reset destroys committed raw pulls** (v2 DEGRADED #10; the audit-trail hole).
  FIXED this entry: verifier_loop pushes unpushed facts commits BEFORE converging, and skips the
  reset while local is ahead — the reset that ate evidence can no longer run against unpushed
  history.
- **B2 — MAX_ITERS counts packets by glob while iter.py owns a monotonic COUNTER** (design said
  counter, guard never migrated). FIXED this entry: guard prefers iterations/COUNTER when present.
- **B3 — the conclusion adversary is agent-invoked and one Write away** (DEGRADED #8, M3 residual;
  the last self-graded surface). Plan: require a committed adversary TRANSCRIPT artifact (tool-use
  records, not just a verdict file), pin its hash in the report, and give the verifier loop an
  optional re-run hook so grounding can be operator-side.
- **B4 — edge claims are matched by regex; a paraphrase dodges stage 2a-bis** (entry-012 critique).
  Plan: when the edge rail is live (verdict != NONE), REQUIRE a structured `EDGE_CLAIM:` line in
  any packet whose iteration traded, and adjudicate that line -- structure the claim, not the prose.
- **B5 — weak mode has no non-destructive runner** (DEGRADED #9's second half). Plan: run_weak.sh
  (co-located verifier without resets, honest tripwire-only labeling).
- **B6 — aiv-protocol upstream defects bite this integration**: the init shebang bug (#29, worked
  around in setup_sandbox.sh) and the E010 bug-fix heuristic false-positive ("issue #N" in Class E
  fails an honest packet -- documented in TEMPLATE as a trap). Plan: fix both upstream in the
  aiv-protocol repo (in scope for this session) so the workaround and the trap note can eventually
  be deleted.
- **B7 — nothing mechanically paces iterations against the due-bet schedule** (entry-012 critique;
  run 1 burned 091–094 polling). Plan: guard advisory when an iteration opens with zero due bets
  and the last N closes were watch-eligible; keep it advisory -- a hard block would fight genuine
  new work.
- **B8 — `aiv audit` is installed but never runs** (canonical quality sweep exists, unused). Plan:
  wire into iter.py close as non-blocking report first; blocking only if signal/noise proves out.
- **B9 — bets resolutions don't feed knowledge/outcomes.jsonl** (the compounding layer misses the
  richest records: resolved day-scale bets ARE channel outcomes). Plan: bets.py resolve appends an
  outcome record automatically.
- **B10 — the edge rail has never touched the live paper API** (entry-012 residual, same class as
  PR #18's unproven two-lane). Operator-gated: write the one-cycle live acceptance checklist into
  SETUP so it cannot be skipped silently.

**Entry 010 results.** B1 landed and tested in both failure modes: with pushes blocked, the
stranded facts commit and its raw pull survive (reset skipped, loud log line); on divergence
(external rotation), the lane converges instead of deadlocking AND any pull that existed only in
local history is rescued by re-COMMIT as verifier (a bare file restore would be eaten by pnl.py's
C3 untracked-purge -- that interaction is why the rescue commits). B2 landed and tested: MAX_ITERS
reads iterations/COUNTER (exit 2 at the ceiling, silent below it). Critique of this entry: (1) the
divergence-rescue path shells comm/mktemp/xargs -- the most fragile bash in the loop; if it ever
misbehaves the failure is loud (say lines) but a python helper would be sturdier; (2) my own first
test read $? through a pipe -- iter-091's exact trap -- caught and redone; the trap note in
knowledge/traps.md is earning its keep. Next: B9 (bets->outcomes compounding), then B6 upstream
aiv-protocol fixes.

## Entry 014 — B9 (bets feed the compounding layer) + B6 (both upstream aiv-protocol defects fixed at the source)

**B9.** `bets.py resolve` now appends a structured record to knowledge/outcomes.jsonl
automatically (via append_log, durable), so a resolved day-scale bet -- the richest channel
outcome the run produces -- reaches run N+1 even if the agent forgets the manual outcome.py step.
Best-effort by design: a knowledge write must never block a bet resolution. Tested in the sim
(bet-002 lost -> outcomes.jsonl line with clock, span, evidence).

**B6, upstream (aiv-protocol branch claude/money-agent-analysis-10o1nb, 2 commits).**
- E010 false positive: `has_provenance_evidence` consulted only per-claim class assignments (which
  the markdown parser rarely populates), so an honest packet with a filled `### Class F` section
  BLOCKED whenever its intent text said "issue #N". Fixed to also consult
  `evidence_classes_present` -- the model field that already tracked exactly this. Regression
  verified: the money-agent packet that failed with "issue 6" wording now passes.
- Shebang bug (#29): `aiv init` hooks now pin `sys.executable` (the interpreter that can import
  aiv by definition) instead of PATH's python3; whitespace-path fallback kept. Fresh-init verified:
  the hook's first line is the owning interpreter's absolute path.
- Full upstream suite: 739 passed, 22 skipped.
- Downstream consequences once upstream merges: setup_sandbox.sh's sed repair of the hook and
  TEMPLATE.md's E010 trap note both become deletable -- left in place for now (they are harmless
  with the fix and load-bearing without it; note-to-port: remove them when main pins an aiv
  version carrying these fixes).

**Critique of this entry.** (1) The E010 fix widens `has_provenance_evidence` for every consumer,
not just E010 -- reviewed the call sites (E010 is the only one) but a maintainer should confirm the
intent of `evidence_classes_present` matches; flagged in the commit body. (2) The upstream branch
name is this session's default, not a descriptive fix branch -- the operator may want to re-branch
before PRing upstream. (3) bets->outcomes uses the bet's clock class as `channel`, which is coarser
than outcome.py's free-form channel; good enough for queryability, revisit if it muddies the map.
Next: B4 (structured edge claims), then B3 (adversary transcript), B5 (weak-mode runner).

## Entry 015 — B4 (structured edge claims) + B3 (the adversary must show its work)

**Loop meta, logged honestly:** the 10-minute cron died with a session recycle (8h gap; CronList
empty on resume) -- the third occurrence of the entry-005 lesson in this program's history, now in
its own harness too. Remediation: the remaining inventory runs consecutively in-session instead of
on a wall clock. A run 2 that wants day-scale pacing must use durable queued wakeups, never
session-local cron; this is exactly why bets.py records poll cadence in a committed file rather
than in a scheduler.

**B4.** When the edge rail is live (grounded verdict != NONE), every packet must carry a
machine-readable `EDGE_CLAIM: <verdict>` line and it must equal the verifier's verdict. Paraphrase
can no longer dodge stage 2a-bis: the claim is structured, not prose. iter.py pre-fills the line
from the grounded verdict at open, so an honest iteration passes by construction -- and if the
verdict MOVES between open and close, the gate mismatch forces a conscious re-read of the facts
instead of a stale assertion. Prose-regex check kept as backstop for un-scaffolded packets.
Tested: missing line fails with the mandate message, matching line passes, contradicting line
fails as a false edge claim.

**B3 (DEGRADED #8, the last self-graded surface, upgraded).** The conclusion adversary's verdict
was one Write away. Layer 3 now also requires ADVERSARY_TRANSCRIPT.md -- the raw working record
(>= 30 substantive lines, >= 5 search-trace lines), committed, and hash-pinned by the report
(`TRANSCRIPT_SHA256:`). Honest framing, printed in the code comment: still agent-side, still a
TRIPWIRE -- but forging a plausible multi-step working record is qualitatively more work than
forging one verdict line, and the transcript gives the operator's independent re-run (the true
grounding) something to diff against. Tested: missing transcript, stale pin, thin transcript all
fail with distinct messages; a real-shaped transcript satisfies the layer.

**Critique.** (1) B4's mandate binds only while the rail is live -- a packet written the cycle
AFTER a registration lands but BEFORE edge.json publishes sees NONE and carries no line; window is
one verifier cycle, acceptable. (2) B3's line thresholds are guessable constants; their value is
the diff surface for the operator re-run, not the count itself. (3) The transcript check reads
content patterns (searched/considered/...) -- an English-keyword heuristic; a non-English
adversary transcript would need the list extended.

## Entry 016 — B5 (weak-mode runner) + B7 (pacing advisory) + B8 (canonical audit at close) + B10 (live acceptance checklist)

**B5.** `bin/run_weak.sh`: the co-located fast-trial verifier DEGRADED #9 said was missing. Same
facts pipeline (pnl + edge_pnl), same verifier authorship, and the one hard guarantee both modes
now share: NO resets, ever -- it only appends facts commits, so v1's destroy-your-own-evidence
loop stays dead in weak mode too. The banner states plainly that weak mode is tripwire-only and
its results debug the harness, never conclude anything about the agent.

**B7.** guard now prints, when open bets exist and NONE is due: "if there is no NEW lever this
iteration, this should be a watch tick, not an iteration." Deliberately advisory -- a hard block
would fight genuine new work; the run-1 failure this targets (091-094 polling not-yet-due clocks
as iterations) was a visibility failure, and the agenda line plus this question is the visibility.
Tested: prints exactly when open>0 and due==0, silent otherwise. Testing note: the first attempt
"failed" because the sim ledger had gone 8h stale and guard halted at freshness before the bets
section -- the staleness gate doing its job during a test of a different feature.

**B8.** `iter.py close` runs `aiv audit` after the gate passes and surfaces its last lines --
non-blocking BY DESIGN (audit is drift-visibility, not per-claim adjudication; promote to blocking
only if signal/noise proves out), and fail-OPEN on a missing/broken auditor with an install hint,
because advisory means advisory. Tested the fail-open path.

**B10.** SETUP.md 4b now carries the five-step live acceptance checklist (freeze, field shapes,
fills movement, VOID detection, re-register) with the reason it cannot be skipped: an edge verdict
from an unproven rail is exactly the class of green check this program exists to kill.

**Critique.** (1) run_weak.sh shares no code with verifier_loop.sh -- a deliberate copy so weak
mode cannot accidentally inherit reset/rotation behavior, at the cost of two publish blocks to
keep in sync (noted for a future refactor into a shared publish function). (2) B7's advisory can
nag during legitimate build sprints between bet placements; it is one line, and wrongly-iterating
was the costlier error in run 1. (3) B8 surfaces only the audit tail -- 3 lines chosen to keep
close output readable; the full report is one command away.

## Entry 017 — CLOSING: inventory exhausted, final audit, and the port-to-main checklist

**Exhaustion statement (scoped honestly).** Every item in the entry-013 inventory is landed and
tested (B1-B9) or documented as an operator-gated acceptance step (B10). "Exhausted" here means:
no remaining item is both (a) evidenced by a run-1/v2/aiv-protocol source and (b) reachable from
inside this session. What remains is out of reach BY NATURE, not by fatigue:
- the one-cycle LIVE runs (two-lane verifier with a real Stripe key; edge rail against the real
  paper API; the B10 checklist) need the operator's machine and keys;
- the beacon deploy (M7) needs the operator's Cloudflare token;
- true out-of-band grounding of the conclusion adversary needs a second party by definition -- the
  transcript upgrade (B3) raised the forgery cost, only the operator's re-run grounds it;
- canonical-JSON packet adoption (the guard-grade schema with SHA binding and scope inventory) is
  the right NEXT HORIZON for the aiv integration, but it is an upstream-shaped project (the guard
  runs CI-side against PRs, not local iteration loops), logged here so it is not mistaken for
  forgotten.

**Final regression sweep (all changed components, one pass):** guard 0/2/1 exits correct across
EDGE_TERMINAL and VOID states; full gate PASS on the reference edge packet; conclusion_gate clean
multi-layer fail with no crash; truth.py both fact files grounded; edge.py status grounded. The
sim suite's full history across entries 012-013: every fix was demonstrated failing before and
passing after in a bare-origin two-lane clone.

**What this design now is, in one paragraph.** Two scored rails, each with the same shape: a
grounded fact file on a branch the agent cannot write, produced by a process it cannot invoke,
consumed through one read path, adjudicated by gates that compare structured claims to verifier
numbers. A stop set that is still closed ({customer dollar, cap exhaustion, operator} plus the
edge checkpoint, which is an operator review, not an agent power). Waiting that is recorded,
surfaced, and blocks conclusions while live. A compounding layer that feeds itself. And the
canonical aiv toolchain doing the structural half of packet verification, with the hand-rolled
half shrunk to exactly the domain semantics no generic tool can know. The self-graded surfaces
remaining are named (bets registry, adversary transcript), each with the honest label "tripwire"
and the reason the tripwire is acceptable.

**PORT-TO-MAIN CHECKLIST (if the operator blesses this exploration):**
1. Merge PR #18 first (this branch stacks on it), then fast-forward this branch's commits.
2. Run the two live acceptance gates before any run 2: one verifier cycle against real keys
   (PR #18's own caveat) and the B10 edge-rail checklist (SETUP.md 4b).
3. Upstream: PR the two aiv-protocol fixes (E010, shebang #29) from its
   claude/money-agent-analysis-10o1nb branch -- consider re-branching to descriptive names first.
   Once a pinned aiv version carries them: delete setup_sandbox.sh's hook sed-repair and
   TEMPLATE.md's E010 trap note.
4. Provision decisions the operator owns: ALPACA_PAPER_* in the verifier .env (edge rail on/off),
   EDGE_TERMINAL (dual-rail vs single-answer run), MAX_WALL_CLOCK_H + LEDGER_MAX_COMMITS +
   INTERVAL/HEARTBEAT_S per docs/STANDING_RUN.md, and whether the agent gets its own broker creds.
5. Protect the ledger branch at the remote (now with force-push allowance for the verifier
   credential if rotation is on).
6. Scheduling for a standing run: durable queued wakeups only -- session-local cron died twice in
   this program's history and once more in this very loop (8h gap, entry 015).

**Loop meta, closing.** Entries 009-014 across two sessions; one 8-hour scheduler death absorbed
by switching to consecutive in-session iterations (the correct fix, since the work -- unlike a
standing run's -- was not gated on external clocks). The inventory method (source-evidenced
bottlenecks, consumed top-down, each with fix + test + critique) is itself the reusable artifact:
it is what "systematic self-improvement over the baseline" turned out to mechanically mean.

## Entry 018 — ROUND 4 (pre-merge review of this branch): three findings, all fixed

An independent round-4 reviewer attacked the full origin/main...HEAD diff with an explicit
merge-damage hunt list, empirically verifying each finding and each clean check. Verdict:
merge-with-nits — no code section, function, or gate was dropped by the reconciliation; every
conflicted file integrated both parents' semantics, repeatedly with the stricter/fail-closed
variant; all gates behaved fail-closed under adversarial inputs. Findings, all landed here:

- **F1 (MEDIUM, the log itself):** the merge-note renumbering collided — a sequential
  find-replace re-hit its own output (009→012 later swallowed by 012→015), leaving entries
  015-017 duplicated and 012-014 absent. No content was lost. Regenerated the tail from the
  pristine pre-merge text with a DESCENDING mapping (verified unique + monotonic 001-017). The
  bug class is worth naming for the traps file: sequential renumbering must map high-to-low.
- **F2 (LOW, latent fail-closed crash):** parse_registration accepted a timezone-NAIVE
  RESOLVE_BY; the bet froze, then every verdict cycle crashed comparing naive vs aware into the
  fail-closed handler — an active registration masquerading as an idle rail. Now rejected at
  registration with an explicit message (verified: aware accepted, naive refused).
- **F3 (nit):** run_weak.sh still used fixed /tmp names after verifier_loop moved to mktemp -d
  (symlink pre-placement hardening). Aligned.

Also re-verified on the merged branch this round: the conclusion gate's full four-layer pass
path (transcript + CONCLUSION bar + resolved bets + non-PENDING edge), corrupt bets.json
(conclusion fails closed, guard advisory survives), and the MAX_ITERS counter.

## Entry 019 — legibility as a feature: the navigation layer, the run lifecycle, and the committed test matrix

**The prompt for this entry, verbatim from the operator:** "as a human or agent its hard to find
anything in this repo or know why I need to read something because its messy." That is a real
defect class for this repo specifically: a verification harness whose structure cannot be
navigated is a harness whose checks do not get read.

**Navigation layer.** README gains "Finding your way around": four reader personas (operator /
run agent / reviewer / contributor), each with its complete reading list and nothing more, plus a
directory-ownership table. Every directory that carries trust semantics now says so in its own
README: `bin/README.md` is the full trust map (verifier-only / gates / agent tools / operator
lifecycle, one line each — the read-side complement to sod_hook's write-side blocklist),
`ledger/README.md` states the never-write rule and the truth.py-only read rule where a browsing
agent will actually see it, `templates/`, `tests/`, `archive/` likewise. The three fill-in
templates move from root clutter to `templates/` (all references updated).

**Run lifecycle — a correctness fix wearing a tidiness costume.** `bin/new_run.sh` archives all
run-scoped state to `archive/run-NNN/` and reseeds clean logs. Without it, run N's leftovers
adjudicate run N+1: conclusion_gate's effort floor counts MONEY_LOG headers and SENT_LOG sends
(a stale log satisfies the exhaustion floor on day one), MAX_ITERS reads the old counter, a stale
DISCLOSURE_EV_LOG pre-authorizes sends, a stale EDGE_REGISTRATION is a bet nobody placed. Run 1
handled this with a hand-typed wipe commit — a human remembering. Verified in a scratch clone:
archive complete, logs reseeded, conclusion gate reads 0 iterations after. The verifier-side
half: set_baseline.py now auto-archives a stale edge freeze (a new baseline is a new run; a
previous run's frozen bar must never adjudicate this one) — verified.

**tests/sim.sh — the review rig, committed.** The bare-origin two-lane matrix that caught every
real defect across four review rounds (the inert rev-list fix, the dropped gate section, the
anchor rule) now lives in the repo: 22 assertions over grounded reads, every guard terminal, the
full gate adjudication, bets/conclusion interplay, the edge verdict machine (stubbed broker,
including the naive-deadline rejection), and the verifier convergence block extracted VERBATIM
between TEST-MARKER comments — with an anti-vacuity check that fails if the markers drift.
Scope stated in the file: component-level; the live seams remain issue #20's operator gates.

**The test debugged itself into existence, which is the point.** First scripted runs failed 5/22:
one real test-rig bug (a stale remote-tracking ref made the forgery test's push silently bounce,
so it asserted against a clean lane), one flake (a 1-second staleness window raced; now 0), and
three artifacts of testing uncommitted code (the clone tests HEAD; the extracted convergence
block came back EMPTY from main's un-markered file and "passed" vacuously — hence the
anti-vacuity guard, and assert_exit/assert_grep now dump the failing command's output). Every one
of those failure modes is now impossible to reintroduce silently.

**Critique.** (1) The persona lists in README duplicate knowledge that lives in per-directory
READMEs — drift risk between them; acceptable because the README table names owners, not
details. (2) new_run.sh reseeds log headers from strings embedded in the script — a template
drift risk; kept because reseeding from templates/ would couple the script to files an operator
might edit mid-run. (3) sim.sh runs ~30s and is not wired to CI or a pre-push hook — deliberate
for now (the repo has no CI), but "run tests/sim.sh" is now in the contributor persona and the
PR-review discipline; wiring it mechanically is the natural next hardening.

## Entry 020 — ROUND 5 (pre-merge review of the restructure): six findings fixed, and the matrix caught its author twice more

An independent round-5 reviewer attacked the 3-commit restructure with mutation testing — deliberately
reintroducing the historical defect classes to see whether tests/sim.sh catches them. Verdict:
merge-with-nits. The matrix caught the inert rev-list bug, a deleted gate section, and a broken
first-dollar check; new_run.sh survived every edge case thrown at it and no gate-read path is missed.

**F1 (the real finding — another half-true self-claim):** entry 019 said the marker extraction
"fails if the markers drift"; true only for the BEGIN marker. Deleting the END marker kept the matrix
green while the rig silently executed the rest of the verifier loop mid-source. Fixed: both markers
required, extraction rejected if it contains invocations past the block, execution gated off entirely
on a bad extraction, and the recovery cycle's clean exit asserted. Mutation-verified in a clone:
end-marker deletion now produces two loud FAILs and the block is never executed.

**F2–F6, all landed:** sod_hook's blocklist now covers every bin/ script and tests/ (and bin/README's
claim about it is worded to match reality plus the tripwire-vs-wall limit); the agent's reading rules
gain `templates/` (gate-required) and forbid `archive/` (prior-run strategy contamination — the
in-tree equivalent of a prior-run branch); new_run.sh refuses on ANY porcelain output (untracked
sweep), creates the archive dir lazily, removes the empty run/ dir, and its lane-confirmation
checklist now says what is actually being confirmed; set_baseline's stale-freeze archive can never
clobber a same-second predecessor.

**Process failures of my own, recorded because the log exists for exactly this:** (1) fixing F1 the
first time, I ran the mutation against the REAL tree and cleaned up with `git reset --hard` — which
destroyed the uncommitted round-5 fixes AND (because a failed temp-commit left HEAD one short) dropped
the docs commit from local history; recovered from origin, fixes reapplied, and the rule is now
personal law: mutations run in CLONES, fixes are committed BEFORE testing. (2) My first overrun check
false-positived on a comment that mentions pnl.py inside the legitimate block (invocations, not
mentions, are now matched), and my first exit-code assertion was stricter than the block's actual
contract (the failing-push cycle legitimately returns the short-circuited guard's status). The matrix
ended 22/22 with the mutation still caught — but it took three tries, each mistake exactly the class
this repo documents.

---

## Entry 021 — 2026-07-20 — S1 foundation: the Tier-0 regression corpus (issue #44) + full-matrix baseline

**What:** `tests/corpus.sh` — the Tier-0 corpus §16 of V2_HARNESS_DESIGN specified and nothing
implemented: run-1's REAL failure artifacts replayed against the v2 gates, wired into CI as a step
after the sim matrix. Fixtures: (1) the iteration-095 false stop — the archived
`EXHAUSTION_PACKET.md` + full run-1 `MONEY_LOG`/`SENT_LOG` + the open estate bet reconstructed in
`run/bets.json` (the registry postdates run 1; the bet itself is documented verbatim in the
archived packet's Conclusion) — asserting `conclusion_gate.py` refuses ON THE RIGHT MESSAGES;
(1b) a discriminator run (bet resolved → that refusal alone disappears); (2) the stale-adversary
counterfactual (wrong `MONEY_LOG_SHA256` → STALE, never authorization); (3) the 086 empty-commit
seam (`iter.py close` fails when the close-commit landed no blob; control run proves the success
path; labeled a SEAM test — the gate subprocess is stubbed via the sim.sh monkeypatch pattern, the
ls-tree net is the subject). Also this entry: the `aiv` CLI installed into the sandbox (pip from
the aiv-protocol repo, through the proxy) — the sim matrix's aiv-gate stage now RUNS here instead
of SKIPping.

**Why (cited):** V2_HARNESS_DESIGN §16 Tier 0 ("run 1 is a fixture corpus... never buy at a higher
tier what a lower tier sells"); issue #44. The central regression this pins: at real iteration 095
the v1 gate PASSED this exact state (docs/CASE_STUDY.md). The replay proves the v1 state satisfies
everything v1's gate ever measured — the corpus asserts "effort floor not met" and "packet missing"
are ABSENT — so the refusal rests entirely on the two v2-only layers (open bet, missing
fresh-context adversary). That isolation is the regression statement.

**Edge cases enumerated before coding:** message-assertions not exit codes (vacuity); discriminator
run (cause-tracking); effort floor must PASS so failures isolate (full archived logs copied —
88 iteration headers, 13 emailish SENT_LOG lines, zero `<fill>` placeholders, verified by grep);
archive copied never mutated; `bets.py _save` pushes → rig needs a local bare origin (sim.sh rig
pattern); `edge.json` absent on HEAD → conclusion_gate's rail-idle path (no noise); the archived
packet's headings map onto the gate's BARS by substring (verified against `_sections()` semantics);
086 fixture is a seam test and says so.

**Verified by running (artifacts):**
- Baseline at HEAD c2ff14e: `bash tests/sim.sh` → `PASS=18 FAIL=0 SKIP=1` (pre-aiv), then
  `PASS=22 FAIL=0 SKIP=0` after `pip install git+.../aiv-protocol.git` (aiv at
  `/usr/local/bin/aiv`).
- `bash tests/corpus.sh` → `CORPUS PASS=11 FAIL=0`.
- **The bite check (the fixture-must-bite rule, executed):** in a throwaway clone,
  `conclusion_gate.py` mutated blind to the bet registry (`open_bets()` → `[]` — the exact v1
  defect class). Result: gate still exits 1 (adversary layer) but no longer emits "open external
  bet" → the corpus's message assertion catches the mutation **and an exit-code-only test would
  not have**. That asymmetry is the empirical justification for message-level assertions.

**Critique pass:**
- The 086 fixture stubs the aiv_gate subprocess, so it does NOT exercise gate+close end-to-end;
  the sim matrix's gate tests cover the gate itself. Honest scope, stated in the fixture header.
- The plan's S1(c) "generic pnl fixture helper" is deferred to S2, its first consumer — building
  it speculatively here would be scaffolding without a fixture to bite. Recorded as a deliberate
  deferral, not a drop.
- The historical-overclaim fixture (bare-word "47 dollars" parser path) belongs in sim.sh's
  existing aiv block where the synthesized packet + ledger already exist — queued to S2 alongside
  the sim extensions rather than duplicating the synthesis block here.
- The corpus reconstructs the estate bet with 2099 deadline (stays open); the REAL bet's honest
  resolution was "expired unobserved" — the discriminator run uses exactly that resolution, so the
  counterfactual is also on record.

**Next:** S2 — verifier correctness (#33 currency, #34 pagination, #37 preflight) with the pnl
monkeypatch fixture helper, plus the queued bare-word overclaim assertion in sim.sh.

---

## Entry 022 — 2026-07-20 — S2 verifier correctness: currency + coverage fail closed, wash-guard preflight (issues #33, #34, #37)

**What:** `bin/pnl.py` — (1) #33: every object a sum would COUNT (balance_transactions of the four
counted types, paid+succeeded charges, privacy txns) is currency-checked; non-USD →
`non_usd_amount:<kind>:<currency>:<id>`, undeclared → `currency_missing:<kind>:<id>`, both →
`verified=false` and the amount excluded from every sum (never add a known-wrong number). Privacy
is the one deliberate asymmetry: its API is USD-cents by contract and txns normally carry no
currency field, so only an explicit non-USD declaration poisons — documented in the code. (2) #34:
one `MAX_PAGES` constant bounds all three page walks (pull_stripe's was UNBOUNDED — hangable);
exiting at the cap while the provider still reports more →
`coverage_incomplete:<source>` → `verified=false`; a full Privacy page with no continuation token
is also incomplete (cannot prove completeness → fail closed). (3) #37: `start_verifier.sh` gains a
marker-extracted preflight refusing to start while `STATE_DIR/operator_identity.json` is
missing/empty; SETUP.md documents it and why `setup_sandbox.sh` cannot check it (STATE_DIR is
sandbox-unreachable by design — a fake sandbox check would be theater). (4) sim.sh: an 8-case pnl
fixture block via the established monkeypatch pattern (with a crash-guard excepthook — see
critique), the preflight extraction tests (both markers + overrun guard, the convergence-block
precedent), and the queued bare-word overclaim pin from entry 021.

**Why (cited):** issues #33/#34/#37 (all three surfaced by the external AURUM-spec audit;
#38's G1 sibling lands in S6). The entire value of the ledger is that a `verified:true` number is
trustworthy; a mis-scaled or truncated number wearing `verified:true` is the exact failure class
the program exists to kill.

**Edge cases enumerated before coding:** mixed USD+JPY must name the offender; fee/refund currency
rides the same txn check; missing currency ≠ USD (fail closed); truncation-at-cap vs clean-end
distinguished per source; privacy token-missing-on-full-page; declared-EUR privacy txn excluded
from `spent_usd`; the wash-guard must be ARMED in fixtures (an empty allowlist adds
`wash_guard_disarmed` noise the moment charges exist — hit while building the bite script);
Stripe pagination stubs need `id` on the last item or the walk crashes (hit in the first BITE-B
attempt — stub bug, not product bug).

**Verified by running (artifacts):**
- BITE-A (pre-change, throwaway clone @ c2ff14e): a ¥500 JPY charge produced
  `verified:true, received_usd=5.0, made_money:true, errors=[]` — the silent 100x mis-scale, live.
- BITE-B (pre-change): 50 pages pulled with `has_more` still true → `verified:true,
  received_usd=5000.0, errors=[]` — silent truncation presenting as complete.
- New fixtures against pre-change committed HEAD: `FAIL pnl currency/coverage` (the fixtures
  bite); after the [S2] commit: `bash tests/sim.sh` → **PASS=26 FAIL=0 SKIP=0** (was 22), corpus
  → **PASS=11 FAIL=0**. shellcheck + compileall clean.

**Critique pass:**
- Two of my own test bugs, recorded because that is what the log is for: (1) the first bare-word
  overclaim fixture used "47 dollars" and PASSED the gate — not a gate bug: the rig's edge rail
  carries paper_pnl 62.5 and the gate's documented residual accepts real-money claims up to the
  paper P&L; the test amount must exceed EVERY bound (now 999). The residual itself is real and
  stays on the books (aiv_gate.sh comments it honestly). (2) `${var##*PNL_FAILS:}` returns the
  WHOLE string when the marker never prints (bash no-match semantics), so a crashed fixture block
  would have surfaced as truth.json garbage — the excepthook now guarantees the marker on every
  exit path. The pre-existing EDGE_FAILS block shares this latent shape; queued to S16's
  test-vacuity lens rather than touched mid-S2.
- Observed while running BITE-B, not fixed here (scope): `received_usd` (charges feed) and
  `received_gross_usd` (balance_transactions feed) can disagree wildly and nothing cross-checks
  them — a cheap future integrity signal (|customer+self − gross| tolerance). Candidate for a
  follow-up issue at stacking time.
- The sim rig clones committed HEAD, so new fixtures + code must land in the same commit and the
  matrix goes green one commit later — the FAIL-then-commit-then-green sequence above is that
  discipline working, not a process wobble.

**Next:** S3 — #46 facts-lane side-car rescue (sim must export a temp `MONEY_AGENT_STATE` before
executing the marker block) + supervise unpushed-counter, and #41 inference metering.

---

## Entry 023 — 2026-07-20 — S3 durability + metering: quarantine-not-delete, divergence side-car, unpushed counter, inference cost (issues #46, #41)

**What:** (1) `pnl.py` C3 now QUARANTINES untracked raw pulls into `STATE_DIR/raw-rescue/<ts>/`
instead of unlinking — an untracked raw is either an agent plant (now preserved as evidence of the
attempt) or the orphan of a failed verifier commit (now preserved as audit trail; deletion was the
traps.md #9 residual loss path). Tree semantics unchanged: nothing untrusted reaches the manifest.
(2) `verifier_loop.sh` divergence path copies stranded pulls to a state-dir side-car BEFORE the
reset (belt; the existing re-commit stays the suspenders). (3) `supervise.sh` surfaces N unpushed
facts commits when the checkout IS the facts lane. (4) `pnl.py` gains `inference_usd` /
`inference_source` / `net_usd_full` from `INFERENCE_CSV` (#41): absent feed → nulls (unknown ≠
zero, both sides of the subtraction), header-only file → measured 0, empty/malformed → fail
closed. `.env.example` + SETUP + STANDING_RUN document the feed.

**Why (cited):** #46 (traps.md #9: the hazard was "NOT fully gone on the facts lane";
IMPROVEMENT_LOG 011/013's inert-guard history is the argument for belt-and-suspenders here);
#41 (archived run-1 README: true P&L "negative by an unrecorded amount"; COMPARATIVE_ANALYSIS
§9-7/R4). The C3 change also upgrades the FORGERY story: a planted pull used to vanish silently —
now the attempt itself is preserved in a dir the agent cannot reach.

**Edge cases enumerated before coding:** the sim executes the marker block VERBATIM, so
`run_convergence` must pin `MONEY_AGENT_STATE` to the rig or the side-car writes the operator's
real `~/.money-agent-verifier` (caught at planning, fixture-pinned now); divergence needs a true
sibling commit (bare-side `commit-tree -p ledger^`), not a rewind, or the ancestor check routes to
the push path; after the divergence cycle the rescue commit is LOCAL (ahead) — origin lands it on
the NEXT cycle, so the fixture runs the block twice; quarantine must move, not copy (tree stays
clean for the manifest); header-only vs fully-empty CSV mean different things (measured zero vs
misconfiguration); supervise counter only speaks when the checkout is the facts lane.

**Verified by running (artifacts):**
- `bash tests/sim.sh` → **PASS=29 FAIL=0 SKIP=0**, run twice (stability); corpus **11/0**;
  shellcheck + compileall clean. New assertions: divergence side-car holds the pull, re-commit +
  push lands it on origin, supervise names "1 unpushed local commit", C3 quarantine (plant moved
  to state dir, gone from tree), inference nulls/sum/fail-closed/measured-zero (sim cases 8–11).
- **Retro-bite @ HEAD~1** (fixtures committed with code this time, so the bite ran retroactively
  in a throwaway clone): plant DELETED, nothing quarantined, `inference_usd`/`net_usd_full`
  ABSENT from truth.json — with `INFERENCE_CSV` set and silently ignored, `verified:true`.

**Critique pass:**
- The aggregated "pnl:" sim label still names only the S2 cases though it now covers 11 — cosmetic,
  queued to S16's sweep rather than churning the matrix mid-stack.
- The side-car directory grows unboundedly on a pathological flapping remote — acceptable for now
  (one dir per divergence event, rare by construction); noted for the standing-run posture.
- The supervise counter is informational and does not change the VERDICT line priority; if the
  operator wants "unpushed > K" to escalate to a verdict, that is a one-line memo decision (S14).
- Commit-then-test ordering slipped this unit (code+fixtures in one commit before the first green
  run) — the retro-bite closed the gap, but the cleaner sequence is fixtures-fail-first; restored
  as the default next unit.

**Next:** S4 — fact-lane signing (#36 ssh-keygen -Y + previous_hash chain; pubkey location
decision) + #42 signed attestation.

---

## Entry 024 — 2026-07-20 — S4 fact-lane signing: verifier signatures, hash chain, customer attestation (issues #36, #42)

**What:** (1) `pnl.py` signs `truth.json` with a verifier-only ed25519 key (`ssh-keygen -Y`,
detached `ledger/truth.json.sig`; key at `STATE_DIR/verifier_signing_key`) and embeds
`previous_hash` = sha256 of the last PUBLISHED truth.json (HEAD of the facts-lane checkout) — a
content-based chain that survives `LEDGER_MAX_COMMITS` rotation. (2) `truth.py` refuses the
grounded label for any unsigned/tampered/chain-broken `truth.json` whenever the ref it reads
carries `harness/verifier_key.pub` (fail-closed; no pubkey → legacy, so bare clones keep working).
(3) When signing is live, `pnl.py` emits the signed customer-facing `ledger/attestation.json`
(verified revenue, policy line, truth/manifest hashes, refusals provenance from the agent
branch); independent bare-clone verification procedure in `ledger/README.md`. (4) Wiring:
sod_hook blocks the trust anchors, verifier_loop publishes the new artifacts, setup_sandbox
preflights ssh-keygen when armed.

**Decisions recorded (the §0 open question):** pubkey + allowed_signers live under **`harness/`**
— operator-owned per CONTRIBUTING's table and OUTSIDE `ledger/`, so the SoD authorship checks
(guard's ancestry scope, sod_hook's ledger/ block) never have to carve exceptions for
verifier-key commits. The key is read from the SAME ref as the facts: on the protected ledger
branch the agent can write neither (wall under full provisioning); in weak mode a swapped
key+sig pair is a visible commit (tripwire) — the labels stay honest. The signature covers
truth.json only; the raw manifest is covered transitively via the embedded `manifest_sha256`
(deviation from #36's literal "sign both", equivalent coverage, one fewer artifact).
`edge.json` signing is DEFERRED to S6 (its verifier is being reworked there anyway) — until
then a weak-mode edge verdict stays exactly as forgeable as it was yesterday; no regression,
noted as the open half.

**Edge cases enumerated before coding:** enforcement keyed on an agent-writable file would be a
downgrade attack (delete pubkey → unsigned accepted) — hence key-from-the-ref-being-read, never
the working tree; ssh-keygen absent on the agent side with enforcement armed → refuse grounded
(+ setup_sandbox preflight names the fix); signing key missing while pubkey committed → verifier
writes the error INTO truth.json (verified=false) so the halt explains itself; chain check is
ledger-branch-only (agent-branch parents are unrelated history) and treats an unreachable parent
as chain start (rotation); attestation only exists signed (an unsigned attestation is a claim in
a costume); multiple pnl cycles between commits keep previous_hash stable because HEAD does not
move (chain aligns with commits, not cycles).

**Verified by running (artifacts):**
- `bash tests/sim.sh` → **PASS=35 FAIL=0 SKIP=0** (was 29): valid-signed accepted; tampered
  refused with "SIGNATURE VERIFICATION FAILED" + guard halt; unsigned refused; forged
  previous_hash refused with "HASH CHAIN BROKEN"; pnl end-to-end asserts sig + correct chain
  hash + ssh-keygen-verified attestation carrying refusals provenance. Corpus **11/0**;
  shellcheck + compileall clean. The rig's key is throwaway — the real repo carries none.
- **Retro-bite @ HEAD~1:** committed pubkey + UNSIGNED truth.json with received=47.0 → old
  truth.py returned it as grounded `ledger-branch`, exit 0, value 47.0. The new code refuses the
  same state ("UNSIGNED ... refusing the grounded label").

**Critique pass:**
- `truth.py` re-encodes git-show text output before verifying; exact for the \n-only JSON this
  repo writes, but byte-fidelity would prefer `_git_bytes` end-to-end — queued to S16's
  correctness lens rather than reworking load()'s text plumbing mid-stack.
- Key CUSTODY is out of scope and said so in ledger/README: the signature proves
  "same key as provisioned", not "honest verifier" — the operator's key hygiene is a runbook
  item (S15).
- The attestation's refusals_lines is a raw line count (headers included), deliberately not a
  parsed entry count — parsing REFUSALS prose would be fragile theater; the sha256 is the real
  anchor.
- The one-step chain check verifies parent linkage only; a full-history walk is an operator
  audit tool, not a per-read cost — documented in ledger/README's procedure.

**Next:** S5 — gates & probes (#39 delivery_check + #35 link-limit fold-in, #40 oracle-classed
resolutions, #45 PACE_ENFORCE in iter.py).

---

## Entry 025 — 2026-07-20 — S5 gates & probes: the delivery seam, oracle-classed resolutions, mechanical pacing (issues #39, #35, #40, #45)

**What:** (1) `bin/delivery_check.py` (#39/G4, "the headline residual"): verifies the pay→deliver
seam against the LIVE success-redirect target — status, artifact size floor, placeholder scan,
optional exact sha256 — reusing host_check's SSRF guard/redirect-vetted opener (consumed, not
reimplemented). #35 folds in: with `--payment-link`, the link is read back via the Stripe API and
`restrictions[completed_sessions][limit]` MUST be 1 — the provider-level atomic cap the ~120s
polling window cannot provide; no key → `unverified` → FAIL (the agent that created the link holds
the key, so unverifiable = misconfigured, never exempt). (2) `aiv_gate.sh` stage 2c: a packet
carrying a buy/checkout.stripe.com URL claims a paid offer → must carry `DELIVERY_CHECK_URL:`,
which the gate re-runs itself (self-typed verdicts untrusted — the 2b precedent). (3) `bets.py
--oracle deterministic|instrumented|judgment` (#40): non-judgment resolutions EXECUTE the recorded
`--check`, storing cmd+rc+output in the resolution; rc is EVIDENCE (nonzero may be what "lost"
looks like), refusal is reserved for an unrunnable oracle (127/126/timeout), with a visible
`--downgrade-judgment` relabel as the escape hatch; `conclusion_gate` names the oracle class in
open-bet refusals; `bets.py list` shows it. (4) `iter.py new --lever` + `PACE_ENFORCE` (#45,
default off): quiet open bets (open, none due) block a lever-less NEW iteration; the declared
lever lands in the MONEY_LOG skeleton as a committed, auditable line. Enforcement deliberately
lives at iteration-open, NOT guard — guard runs before a lever could exist; deviation to be noted
on #45 at PR time. guard's B7 advisory now names the flag. One flagged PROMPT.md line (create
links with the provider cap) + SETUP rule + TEMPLATE trap note; delivery_check joins the sod_hook
blocklist.

**Edge cases enumerated before coding:** the EDGE_CLAIM line must be restored before the 2c sim
tests or the missing-claim failure would make them pass for the wrong reason; the 2c trigger is a
URL-shaped match (not prose like "stripe"), so ordinary packets never trip it; `.invalid` TLD
gives an offline-deterministic failing fetch through the real SSRF guard; a check command that
EXITS nonzero is evidence while one that cannot RUN grounds nothing; PACE must never block watch
ticks or resolutions; the due-bet case and default-off case both stay unblocked; the delivery
body read is bounded (5MB) and the size floor (256B) sits below every real deliverable.

**Verified by running (artifacts):**
- `bash tests/sim.sh` → **PASS=46 FAIL=0 SKIP=0** (was 35): delivery unit walk
  (pass/placeholder/size/uncapped/unverified/sha), gate-2c wiring (URL without DELIVERY_CHECK_URL
  fails; failing fresh re-run fails), oracle trio (unrunnable refused / downgrade relabels /
  executed rc stored), pacing trio (+ default-off untouched), conclusion-gate oracle labeling.
  Corpus **11/0**; shellcheck + compileall clean.
- **Retro-bite @ HEAD~1:** old gate has zero delivery references (a paid-offer packet passed with
  no seam check); old `iter.py new()` has no lever/pacing; old bets ACCEPTED a prose resolve of a
  deterministic-shaped bet.

**Critique pass:**
- The positive gate-2c path (packet passing WITH a live delivery URL) is untestable offline by
  design (SSRF guard blocks a local rig) — covered at the unit layer via monkeypatched fetch, the
  same honest posture host_check has always had; the live seam belongs to the operator acceptance
  gates.
- `_link_limit` lists the first 100 payment links; a run creating more would need pagination —
  far past run scale, noted rather than built.
- The PROMPT.md line is operator-negotiated wording changed by this stack: flagged for explicit
  review in the PR body (plan ground rule).
- bets.py's executed check runs under `bash -c` with a 120s timeout in the agent's own
  environment — no new privilege (the agent already runs arbitrary shell), but the timeout keeps
  a hung oracle from wedging a resolution.

**Next:** S6 — edge-verdict quality (#38): MAX_DRAWDOWN_USD frozen with the registration, runtime
peak tracking in a separate state file, drawdown breach → FALSIFIED, BENCHMARK recorded; plus
edge.json signing (the S4 deferral) if it fits the stack cleanly.

---

## Entry 026 — 2026-07-20 — S6 edge-verdict quality: the frozen risk cap, peak tracking, signed edge facts (issue #38; closes the S4 edge-signing deferral)

**What:** (1) `EDGE_REGISTRATION` requires `MAX_DRAWDOWN_USD`, frozen with the bar; `edge_pnl.py`
tracks peak equity in a SEPARATE `STATE_DIR/edge_runtime.json` (the frozen registration's hash
never moves) and a peak-to-current drawdown past the declared cap is `FALSIFIED` — **even when
pnl still clears the bar**, which is precisely the negative-skew/martingale shape a raw level
check blesses. `falsified_reason` distinguishes drawdown from deadline; edge.json reports
`peak_equity_usd`, `max_drawdown_usd_observed`, `unrealized_positions_at_verdict`. Optional
`BENCHMARK` is parsed + frozen for the record only — enforcement is a documented data-feed-gated
follow-up, stated, never silently faked. (2) The S4 deferral closes: `edge_pnl` signs `edge.json`
when the key is provisioned; `truth.py` requires the signature on the armed lane (no chain field
on edge — documented); `guard.py`/`conclusion_gate.py` treat a signature REFUSAL as halt/blocking
rather than rail-idle — an invisible `VOID` would otherwise hide bar-moving behind "absent". (3)
`truth.py`'s chain check no longer false-positives on commits that do not republish truth.json
(pubkey-only or edge-only commits duplicate the parent's file; identical bytes = no new link).

**Edge cases enumerated before coding:** a pre-upgrade freeze without the field skips the
drawdown leg (legacy; new runs re-register); the walk's deadline case must reset the runtime peak
or the drawdown leg shadows the deadline reason (fixture resets it and asserts the reason);
verdict precedence is breach > cleared > deadline (a recovered breach is still falsified — the
#38 point); the runtime file initializes peak to max(baseline, first equity); signature refusal
vs genuine absence must stay distinguishable in every consumer (guard, conclusion_gate).

**Verified by running (artifacts):**
- `bash tests/sim.sh` → **PASS=49 FAIL=0 SKIP=0** (was 46); corpus **11/0**; shellcheck +
  compileall clean. New: martingale-catch steps (new peak stays VERIFIED at dd=0; the post-peak
  drop FALSIFIES with reason "drawdown" while pnl=60 ≥ bar=50), deadline reason preserved,
  missing-MAX_DRAWDOWN registration rejected, stubbed edge_pnl cycle emits a verifiable
  `edge.json.sig`, unsigned edge on the armed lane refused + guard halts on it.
- **Retro-bite @ HEAD~1:** the identical sequence (peak 100100 → equity 100060, pnl 60 ≥ bar 50)
  returned `VERIFIED_POSITIVE_EV` from the level-only verdict.
- **The matrix caught my own fixture bug mid-stack:** the divergence fixture's bare-repo
  `commit-tree` authored as the HOST's global git user, and guard's ancestry-scoped SoD scan
  halted on the foreign author far downstream (the edge-signing guard assertion). Fix = explicit
  identity env, exactly like verifier_loop's real rotation. Two lessons banked: bare-repo
  plumbing commits need explicit identity, and the SoD tripwire genuinely scans full reachable
  history — the "wrong" failure was the authorship control working.

**Critique pass:**
- Drawdown is measured at verifier cadence (~INTERVAL): an intra-cycle spike-and-recover between
  pulls is invisible. Honest bound of a polling verifier — the registration's cap is therefore a
  cap on OBSERVED drawdown; noted here and in the template's wording ("the verifier tracks peak
  equity across cycles").
- Sequential-testing controls (repeated peeking) from #38's "later" list remain open — the issue
  keeps that as its own follow-up scope.
- `edge.py register`'s user-facing error for a missing MAX_DRAWDOWN_USD comes from
  parse_registration's generic missing-fields message — adequate, not hand-held.

**Next:** S7 — the rail-adapter refactor (#30 Part 1) with the golden parity artifact, plus the
stubbed Base/USDC adapter with settlement-event binding.

---

## Entry 027 — 2026-07-20 — S7 rail adapters: the P1 contract, and a Base/USDC rail with settlement-event binding (issue #30 Part 1)

**What:** `bin/rails/` writes down the fact-source contract `pnl.py`'s Stripe path implicitly
defined (primary source; agent-unwritable inputs; hashed raws through the same manifest flow;
identity-classified; fail-closed) — the P1 generalization, with onboarding explicitly a reviewed
harness change the agent cannot perform on itself. `received_usd` is now the sum of customer
revenue across armed rails, with a per-rail breakdown published ONLY when a second rail is armed
— which makes parity structural: a stripe-only run's truth.json shape is untouched. The Base/USDC
adapter (stub-tested; live RPC + wallet funding are runbook items): verifier-frozen baseline
block (the created_gt discipline on a block clock), inbound-USDC log watch, operator wallet
addresses in operator_identity.json classifying as self, and the owner-comment's onchain
wash-trade analogue — a transfer counts as CUSTOMER revenue only when its transaction also
emitted the provisioned marketplace settlement event; bare transfers land in `unbound_usd`,
visible and never counted. Missing binding config and a dead chain both poison the pull.

**Edge cases enumerated before coding:** the breakdown key must be ABSENT on stripe-only runs or
parity breaks by shape; the settlement binding is REQUIRED provisioning (an armed adapter without
it refuses rather than counting bare transfers); baseline block freezes exactly once (second
cycle must reuse frozen fromBlock and never re-read eth_blockNumber); receipts are fetched once
per tx; sender extraction from topic padding; USDC 6-decimal scaling; operator addresses
lowercased both sides.

**Verified by running (artifacts):**
- `bash tests/sim.sh` → **PASS=49 FAIL=0 SKIP=0** (aggregate pnl case now covers 13 cases: +
  stripe-only-no-breakdown, bound/unbound/self classification with received summing 12.34+12.34,
  frozen-baseline reuse, misprovision fail-closed, dead-chain fail-closed). Corpus **11/0**;
  shellcheck + compileall clean.
- **PARITY PROVEN (the S7 golden artifact):** identical stripe-only stub run against HEAD~1 and
  HEAD in throwaway clones — truth.json field-identical (25 fields; excluding only
  computed_at/previous_hash/pulls/manifest by design, and even those matched to the second in
  this capture); `rails` key absent; received_usd 12.34 both sides.

**Critique pass:**
- The settlement-event topic/address values are PROVISIONING inputs pending S13's read-only
  probes of the actual marketplace contracts — the adapter is deliberately agnostic about which
  event signature is "the" acceptance event; the runbook will carry what S13 finds, and until a
  real value is provisioned the rail simply cannot arm. Stub-tested only, stated plainly.
- `eth_getLogs` from frozen-block to latest is one unbounded range — fine at run scale, but a
  long standing run on a busy wallet would want block-windowing; noted, not built.
- USDC-on-Base is treated 1 USDC = 1 USD (the issue's own framing); a depeg is out of scope and
  would be visible in the raws.
- received_gross_usd stays Stripe-scoped (balance_transactions semantics) — the rails breakdown
  is where cross-rail gross lives; documented in the field comment.

**Next:** S8 — the human-actuation queue (#31): bin/human.py + the atomic PROMPT.md autonomy
amendment.

---

## Entry 028 — 2026-07-20 — S8 human-actuation queue: request-don't-wait, metered, conclusion-blocking (issue #31)

**What:** `bin/human.py` — the third road past the identity wall (defeating gates is
constitution-forbidden; provisioning-time gate-guessing was wrong as often as right in run 1):
the agent requests mechanical actuation of a gate it has EMPIRICALLY hit, and keeps working.
Guardrails structural where possible: kind allowlist
(`captcha|approval-click|kyc-step|signup-complete|claim-host`) rejects free-text asks (actuator,
never oracle); `--test` requires the cited empirical gate-hit (falsify before requesting);
`--ev` requires the worth-operator-minutes case; fulfillment meters `human_minutes`
(`human_minutes_total` aggregated — the "autonomous with metered human actuation" number no
experiment in the field has); declines are recorded, the operator's REFUSALS mirror. Every
request registers a companion `approval`-clock bet through the existing registry, so the
due-bets agenda surfaces it every iteration and an open request mechanically blocks "impossible"
conclusions. `supervise.sh` surfaces the open queue with oldest-age. **Atomic in the same
commit, as the issue requires:** PROMPT.md's autonomy clause narrows from never-ask to
never-ask-for-STRATEGY, with mechanical actuation carved out as requesting ≠ waiting — without
this the tool and the prompt would contradict and the agent would (correctly, per its
instructions) refuse to use the queue. Operator-negotiated wording: flagged for review.

**Edge cases enumerated before coding:** the companion bet is what makes an open request
conclusion-blocking (no new gate logic needed — and if the bet registration fails, the request
REFUSES rather than existing invisibly); fulfill/decline must resolve the companion (won/lost)
or the gate stays blocked after the human acted — a failed companion-resolve warns loudly;
minutes are required at fulfill time (metering is the point, not an afterthought);
`--resolve-by` defaults to +7 days so a forgotten request eventually surfaces as OVERDUE in the
agenda; supervise reads the working-tree file and stays silent where it is absent (the
verifier's ledger checkout).

**Verified by running (artifacts):** `bash tests/sim.sh` → **PASS=57 FAIL=0 SKIP=0** (was 49):
free-text kind rejected; uncited gate-hit rejected; cited request registered; open request
blocks conclusion_gate naming `human actuation hum-001`; fulfillment meters minutes + resolves
the companion; supervise surfaces "1 open actuation request"; decline recorded; list totals.
Corpus **11/0**; shellcheck + compileall clean. Bite is definitional this stack: `bin/human.py`
did not exist at HEAD~1 (every fixture fails on file-absence) and the OLD prompt forbade the ask
outright — the behavior change IS the amendment, which is why the issue demands atomicity.

**Critique pass:**
- The kind allowlist is a tripwire against DRIFT, not a wall against a determined mis-framing
  (a strategy ask worded as a "captcha" request); the operator sees the gate/test/ev text at
  fulfillment time and the decline path exists precisely for that. Boundary case from the issue
  (creative/copyright lending) stays outside the queue by construction — no kind admits it.
- `human_minutes` are operator-reported at fulfill time — honest-reporting, not measurement;
  stated here rather than dressed up.
- The companion-bet linkage derives the bet id from registry length — correct while bets.py
  allocates sequentially (it does; documented assumption the S16 sweep can challenge).

**Next:** S9 — V3 bet-spec + bet_gate.py (typed conditions, action authorization,
BET_GATE_ENFORCE default off).

---

## Entry 029 — 2026-07-20 — S9 V3 typed bet-spec + action authorization (bet-ledger layer, config-gated)

**What:** `bin/bet_gate.py` + typed extensions to `bets.py` — the UNCONTESTED half of
V2_HARNESS_DESIGN's bet-ledger: typed bets (type/lane/typed success+kill conditions/action
reservations/bounds_note; `reproduction_protocol` required for `channel-blocked`; **judgment is
never a legal success oracle** — a bet only the agent can grade does not register) extend the
registry backward-compatibly and are schema-validated FAIL-CLOSED before anything saves. Action
authorization: with `BET_GATE_ENFORCE=1`, an external-effect action (send/publish/deploy/spend)
requires an OPEN typed bet with an unconsumed reservation, decremented+committed in the same call.
`mail.py` wires the check FIRST in `send()` — inert by default, fail-closed when armed. E3
discipline stated at the stamp sites: lifecycle timestamps are local UTC at commit time, never
counterparty-controlled content (an email Date header being the canonical counterexample).
Ordering/spine rules deliberately NOT here — they are S10's config-gate.

**Edge cases enumerated before coding:** validation must precede `_save` (a rejected typed bet
must not exist); untyped bets stay fully legal (the registry's original not-forgetting job, and
every existing sim/corpus fixture); reservations are per-action integers and consumption is
single-invocation decrement+commit (single-agent CLI semantics — "atomic" stated honestly, not
oversold); the mail wiring must precede creds/em-dash/disclosure so an armed refusal needs no
credentials to test; flag-off must be byte-inert (acceptance criterion 6).

**Verified by running (artifacts):** sim → **PASS=66 FAIL=0 SKIP=0** (was 57): flag-off grants;
armed-no-bet refuses; judgment success oracle rejected; repro-less block-claim rejected; valid
typed bet registers; two reservations consume then the third refuses; armed `mail.send` refuses
pre-creds with the bet-gate message. Corpus **11/0**; shellcheck+compileall clean. **Bite:**
definitional (bet_gate.py absent at HEAD~1) plus mechanical — the same armed send at HEAD~1 is
refused by the DISCLOSURE gate, not the bet gate ("REFUSING: disclosure gate..." vs "REFUSING
(bet gate)"), proving the new barrier is real and first.

**Critique pass:**
- Only mail.py consumes authorization today; "publish/deploy/spend" surfaces are declared in the
  schema but have no wired chokepoint (publishing is ad hoc tooling) — the S10 spine +
  S11 P6 probe registry are where publish paths get their chokepoints; until then an armed run
  constrains sends only. Stated plainly for the memo.
- `authorize` grants from the FIRST matching bet; no lane-matching of action→bet yet (that is
  spine ordering, S10).

**Next:** S10 — the spine (spine.yml + bin/spine.py, SPINE_ENFORCE off, DEMAND_REFUTED_K off,
E1/E2 amendments, §13 answers recorded).

---

## Entry 030 — 2026-07-20 — S10 V3 spine: per-lane ordering, config-gated (the contested layer, by explicit switch only)

**What:** `spine.yml` + `bin/spine.py` per the plan's S10 (see commit 18c2d92 for the full
mechanism summary): derived-not-stored lane stages over the typed registry, monotone lattice,
E1 active/watching lane caps, E2 freshness suspension, `DEMAND_REFUTED_K` guard CHECKPOINT.
Wired: `bets.py` placement/resolution consult the spine when `SPINE_ENFORCE=1`; guard consults
`demand_refuted()` when `K>0`; both default OFF (the demand-first ordering is the design's one
contested proposal — adoption is a memo decision, and the terminal set stays closed until then).
sod_hook owns `spine.yml`/`spine.py` (editing ordering to unlock a stage = the constitution-edit
class, when armed).

**V2_HARNESS_DESIGN §13's five open questions, answered as implementation decisions:**
1. *Where do resolution stamps commit?* → CO-COMMITTED in `run/bets.json` at resolve time
   (bets._save), local-UTC stamped (E3); verifier countersigning stays the S11/P4-adjacent
   upgrade path.
2. *Novelty-signature calibration for generator_dry?* → DEFERRED WITH REASON: no bet-generator
   exists in the harness; a dry-generator terminal without a generator is config theater.
3. *Does INCONCLUSIVE count toward DEMAND-REFUTED?* → NO, implemented: only lost/expired grade a
   lane's demand bets dead; an ungraded bet keeps the lane alive.
4. *The horizon parameter?* → belongs to run config (`MAX_WALL_CLOCK_H`), not the spine;
   the spine deliberately owns ordering, not time.
5. *Demand-confirmation TTL?* → machinery present (freshness_h is the extension point; stage-0/1
   shipped); stage-2 TTL is a memo knob, off unless set.

**Edge cases enumerated before coding:** stdlib has no YAML, so the config is a deliberate
YAML-subset with its own ~25-line parser that FAILS CLOSED while armed (an unreadable config
refuses placements rather than guessing); probes must stay resolvable in a suspended lane (they
are how it un-suspends); a placed delivery bet IS the stage-3 exit (building is the bet);
demand-refuted counts graded kills only; the lattice needs no relabel detection — a new lane
starting at 0 makes relabeling self-defeating.

**Verified by running (artifacts):** sim → **PASS=77 FAIL=0 SKIP=0** (was 66; 11 new): flag-off
inert; stage-0 demand refused; probe placeable anywhere; armed bets.py add refuses out-of-order;
instrument+substrate wins unlock stage 2; E2 aged instrument suspends the demand resolution and
refresh un-suspends; DEMAND_REFUTED_K=1 guard checkpoint fires and K-off leaves terminals
unchanged; E1 cap refuses a 4th active lane; unreadable config fails closed. Corpus **11/0**;
shellcheck + compileall clean. Bite: definitional (no spine existed; every armed refusal is
new behavior) — the flag-off assertions are the compatibility half of the proof.

**Critique pass:**
- Stage exits are metric-name conventions (`instrument-probe`/`substrate-probe`) — a mislabeled
  probe metric silently fails to unlock a stage. Acceptable: armed mode's error names the
  ordering rule and `spine.py status` shows the ladder; S16's doc-truthfulness lens should
  confirm the runbook/memo explain the convention.
- `check_placement` runs config-load + full lane derivation per add — O(bets) per call, fine at
  registry scale.
- bet_gate authorization and spine ordering are not yet lane-joined (an action is authorized by
  any typed bet, not necessarily one in the acting lane) — V2_HARNESS_DESIGN leaves this
  composition open; recorded as the S16-review question it is.

**Next:** S11 — P-generalizations (P2 prereg module, P3 decision-gate, P5 obligations+watchdog,
P6 probe registry, P7 exposure caps).

---

## Entry 031 — 2026-07-20 — S11 P-generalizations: prereg, decision gate, obligations + watchdog, probe registry, exposure caps

**What (five primitives, each with the same shape: mechanism where prose was):**
- **P2 `bin/prereg.py`:** edge_pnl's freeze/VOID lifted generic (freeze-on-first-sight that
  REFUSES to re-freeze, hash-intact check, archive-aside clear = set_baseline's stale-freeze
  rule generalized); edge_pnl is the first client with the SAME state file/record shape — the
  existing verdict walk passing unchanged IS the behavior-identical proof.
- **P3 `bin/decision_gate.py`:** recorded-decision gate for publish/listing/data-acquisition:
  fail-closed on ABSENCE, never grades content; a rubber stamp (thin decision/rationale) blocks;
  acquisitions must pin a committed provenance manifest by sha256 that actually exists in-tree.
  disclosure_gate stays the specialized send instance, regexes untouched (the JA lesson).
- **P5 `bin/obligations.py` + `bin/obligation_watch.py`:** the operator adopted the designed
  mechanically-guaranteed exception. Instant delivery remains the default; post-payment work is
  permitted only from a fresh verifier-owned authorization fact proving explicit enablement,
  refund authority, positive P7 caps, and a maximum deadline. The verifier checks the restricted
  completion oracle independently, refunds an overdue failure, and halts.
- **P7 exposure caps:** verifier-owned and published on the protected facts lane. Agent-local
  environment variables cannot activate or widen the obligation class, and registration holds one
  cross-process lock across cap evaluation and append.
- **P6 `bin/probes.py`:** the substrate-probe registry (claim type → probe → the gate that
  re-runs it), plus a built-in mail-roundtrip probe (the M5 propagation test as a named probe).

**Verified by running:** sim → **PASS=92 FAIL=0 SKIP=0** (was 77; 15 new), corpus **11/0**,
shellcheck+compileall clean. Three first-run failures, each a FIXTURE-OR-TOOL bug the matrix
caught and worth banking: (1) sed with `|` delimiter around content containing ` | ` silently
broke the P3 fixture — restructured to two bodies, no sed; (2) **`obligation_watch` read a STALE
`origin/<agent-branch>`** — it never fetched (the loop fetches for it in production, but a
standalone run must not read a stale promise-book); it fetches itself now — a REAL tool bug the
rig caught; (3) the mail-probe fixture assumed creds absent, but this sandbox exports
GMAIL_ADDRESS — `env -u` makes the fixture deterministic (and en route proved the probe's
fall-through order: with creds present the send died at the DISCLOSURE gate, i.e. the gate
chain held).

**Critique pass:** decision_gate's provenance check rglobs the tree per call (fine at repo
scale); the acquisition manifest is pinned-by-hash but its CONTENT quality is judgment (the P3
contract: prove the judgment happened, never grade it); obligations' completion oracle cmd is
recorded but only deadline-vs-status is watched (running agent-authored shell on the verifier is
deliberately NOT done — stated); probes' mail-roundtrip sends real mail when creds exist — it is
an operator-acceptance probe, not a sim fixture, and the sim only exercises its refusal path.

**Next:** S12 shadow-run mode, then S13 probes research, S14 governance docs + memo, S15
runbook, S16 adversarial+mutation+stacking.

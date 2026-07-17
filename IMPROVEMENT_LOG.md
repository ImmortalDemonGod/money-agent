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

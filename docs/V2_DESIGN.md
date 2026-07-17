# V2 Core-System Redesign

**Branch:** `claude/project-analysis-overview-fvr26m` · **Started:** 2026-07-17T04:17Z ·
**Companion:** `IMPROVEMENT_LOG.md` (the running log of every change and its reasoning)

## The design rule (v1's own lesson, promoted to first principle)

v1 proved the same proposition four independent times: **a load-bearing behavior enforced by prose
fails; the same behavior enforced by a mechanism holds.**

| Behavior | As prose | As mechanism |
|---|---|---|
| "Don't fake the P&L" | (never trusted to prose) | Out-of-band verifier → **held 196 cycles** |
| "Disclose AI when EV-positive, lead with it" | CLAUDE.md, always injected → **botched twice** | `disclosure_gate.py` → held |
| "Don't quit early" | 3 documents (CLAUDE.md, PROMPT.md, /loop) → **false TERMINAL at iter 095** | (never built — issue #7) |
| "Commit before the reset eats it" | remembered rules → **≥6 data-loss events** | (never built) |

So v2's design goal is mechanical: **every invariant that failed as prose in v1 gets a gate, a
separated channel, or a scaffold in v2.** No new exhortations.

---

## Bottleneck inventory (from the v1 logs, ranked by measured damage)

Each entry cites the run evidence (MONEY_LOG iteration numbers on PR #8's branch).

### B1 — The harness destroyed its own evidence (≥6 documented events)
The verifier's `git reset --hard origin/BRANCH` ran every ~60s **in the same worktree the agent
wrote claims into**. Casualties: SENT_LOG entries wiped before commit (023, 067 — the audit trail
of what left under a real man's name is now partly "RECONSTRUCTED"), whole iteration numbers lost
(024, 027 have no record at all), an empty commit that looked successful (086, caught only by
`git ls-tree`), a mid-deploy wipe that briefly served unpatched HTML (070), a heredoc-interpolation
casualty in a deployed title (089). Root cause: **the facts channel and the claims channel shared
one git branch and one worktree.** The agent spent real iterations inventing workarounds
(commit-in-the-same-breath, blob verification) for an architectural defect.

### B2 — The stop decision was self-graded (the central defect; issue #7)
`/goal` terminal-state-(b) let a volume-counting gate (`exhaustion_gate.py`: ≥8 iteration headers,
≥3 email-ish lines, 5 filled sections) end the run. At 095 it printed `EXHAUSTION PROVEN` while the
agent's own retro admitted the organic-indexation bet was *pending, not falsified*; the agent
killed its own loop. 096's diagnosis: three exhortations routing through one interpreter (the
agent's judgment) plus one gate measuring the wrong quantity (effort volume, not novelty).

### B3 — Zero telemetry: reach vs conversion undetermined (098)
All 9 funnels shipped with no analytics; surge.sh force-served `Disallow: /` on every site and this
was discovered at iteration 070 — **~60 iterations of "shipped" product invisible to every crawler,
unverified at the serving layer.** The run's dominant conclusion ("the wall is reach") had to be
retracted because $0.00 cannot distinguish "nobody arrived" from "people arrived and declined."
The beacon that would decide it was built at 097 and never deployed.

### B4 — Iteration mechanics were hand-rolled and fragile
Timestamps drifted for 22 iterations (023), numbering has gaps, packets required hand-copying
manifest hashes, a piped `$?` lied about a gate's exit code and reached the stop-hook (091),
MAX_ITERS counts packets by glob (distorted by gaps). Every one of these is boilerplate a scaffold
should own — v1's own stated split: "the model performs the irreducible semantic act, the harness
owns the boilerplate."

### B5 — The send path's enforcement never reached the canonical harness
`main`'s `mail.py` imports `disclosure_gate` fail-closed, but `disclosure_gate.py` and
`DISCLOSURE_EV_LOG.md` live only on the run branch → **on main, every send refuses: the canonical
send path is broken by design today** (issue #11 undecided). Also: SENT_LOG persistence depends on
the agent remembering to commit (see B1), and the v1 storefronts carried AI disclosure only in
`llms.txt`, never on the buyer-facing page — the disclosure-EV decision was never recorded for the
storefront surface at all.

### B6 — Context-free leaks in agent-facing config (issues #9, #10)
CLAUDE.md/PROMPT.md on main carry v1's concrete strategy nouns ("share-loop", "localized versions",
"an AI agent that audits X"). README/docs tell v1's whole business story. A v2 agent that reads its
own instructions inherits v1's business, breaking the premise that convergence means something.

### B7 — Nothing compounds across runs (issue #2)
88 iterations produced a channel wall-map, a falsified-approach table, and demand data — all buried
in a 2,535-line narrative log on an unmerged PR. A fresh v2 agent would re-derive (and re-pay for)
all of it, or worse, re-conclude "blocked" where v1 already proved access.

### B8 — The horizon forbade the winning strategy class (issues #4, #6 — README finding #1)
Time-to-first-dollar made every research-then-build-then-rank strategy illegal. v1 also burned
iterations polling during watch states (091–094) because the loop had no first-class notion of
"waiting on an external clock."

### B9 — Verifier ergonomics
196 of ~348 commits on the run branch are verifier heartbeats (history noise); the verifier must be
hand-pointed at the agent's branch; co-located ("weak") mode is honestly labeled a tripwire but has
no upgrade path in tooling.

---

## The v2 architecture

### A1 — Two-lane git: claims lane and facts lane (fixes B1, B9)
The verifier stops writing to the agent's branch entirely.

- **Facts lane:** verifier commits `truth.json`, `MANIFEST.sha256`, `baseline.json`, raw pulls to a
  dedicated **`ledger` branch** from its own worktree/clone. Heartbeats live there.
- **Claims lane:** the agent's run branch. **Never hard-reset by anything.** MONEY_LOG, SENT_LOG,
  packets, products live here and cannot be wiped by the verifier again.
- The agent reads facts with `git fetch origin ledger && git show origin/ledger:ledger/truth.json`
  — wrapped in `bin/truth.py` so guard, gates, and scaffold all read one way. Freshness (H2) checks
  the ledger branch's committed `computed_at`, same as today.
- SoD gets *stronger*: "only the verifier writes the ledger branch" is enforceable at the remote
  (branch protection) — a wall, not a tripwire; the local hook remains as defense-in-depth.
- New `bin/append_log.py <file> <<text`: append + commit + push in one fail-closed operation;
  `mail.py` uses it for SENT_LOG so the audit trail is durable *by construction*, not by memory.

### A2 — The stop decision, grounded like money (fixes B2; issue #7)
- **`/goal` v2 (RUN_COMMANDS.md):** exactly three terminal states — verified customer dollar,
  verified cap exhaustion, operator says stop. **No self-certified exhaustion state exists.**
- `exhaustion_gate.py` → **`conclusion_gate.py`**: it authorizes *writing* an "impossible"
  conclusion in MONEY_LOG, never ends the run; output language is `EFFORT FLOOR MET`, never
  "PROVEN"; and it adds the check v1's gate lacked — a **novelty bar**: a required
  `ADVERSARY_REPORT.md` produced by a *fresh-context* subagent whose only inputs are the bounds +
  the falsified-approach table, prompted to find one untried in-bounds approach. The conclusion is
  only recordable if that adversary comes back empty (its report is hashed into the packet).
  Honest limit, stated in the gate's own output: the agent still *invokes* the adversary, so this
  is a strong tripwire, not out-of-band grounding; true grounding is the verifier/operator running
  the same adversary, which the verifier loop gains as an optional step.
- `guard.py` drops any path by which a gate pass reads as a stop instruction.

### A3 — Telemetry and serving-layer verification as harness primitives (fixes B3)
- **`bin/host_check.py <url>`** — verifies the *serving layer*: HTTP status, effective robots.txt
  (as served, not as deployed — the surge trap), meta-robots, canonical, sitemap reachability.
  A "published X" claim in a packet must cite its output (aiv_gate enforces the marker the same way
  it enforces ledger hashes for money claims).
- **`harness/beacon/`** — iteration-097's privacy-respecting beacon (path/referrer/UA/country,
  daily-salted IP hash, bot-classifier, `/go` click-through) promoted to canonical harness with
  deploy docs, so run N+1 starts *instrumented* and reach-vs-conversion is decidable from hour one.

### A4 — Iteration scaffold (fixes B4)
**`bin/iter.py`**: `new` allocates the next number from a monotonic counter (no glob-count, no
gaps), stamps verifier-anchored time, pre-fills the packet template with the current manifest hash
+ `received_usd` (no hand-copying), and opens the MONEY_LOG skeleton; `close` runs aiv_gate,
commits and pushes atomically, and verifies the blob landed (`git ls-tree`, the 086 lesson).
MAX_ITERS reads the counter, not the glob. A `watch` subcommand records a watch-state tick without
burning a full iteration (fixes half of B8).

### A5 — Send path repaired and completed on main (fixes B5; decides issue #11 for harness-pattern artifacts)
- Promote a **genericized** `disclosure_gate.py` + `DISCLOSURE_EV_LOG.md` template to main
  (mechanism, not strategy — same family as exhaustion/aiv gates). Main's send path stops being
  broken-by-design.
- `mail.py`: SENT_LOG via `append_log.py` (durable), search fix ported from the run branch.
- The gate gains a `page` mode so *storefront* publishes get a recorded EV decision too — closing
  the v1 gap where buyer-facing pages never went through the disclosure decision at all.

### A6 — Context hygiene (fixes B6; issues #9, #10)
- Agent-facing config (CLAUDE.md, PROMPT.md) genericized: principles kept, v1 strategy nouns
  removed. Diff-checked rule: *no v1 business noun appears in any agent-facing file* (measurable:
  a grep list pinned in the doc).
- A "your world" clause: the agent's inputs are CLAUDE.md, CONSTITUTION.md, PROMPT.md,
  `knowledge/` — it is instructed not to read `docs/` or README (option 2 of issue #10; option 1,
  subdir scoping, noted as the stronger follow-up).

### A7 — Cross-run knowledge, strategy-free (fixes B7; issue #2)
**`knowledge/`** on main: `channel_map.json` (v1's empirically tested wall map: channel → gate →
outcome → evidence ref), `falsified.json` (approaches + the test that killed each),
`traps.md` (the operational traps: reset-cycle, heredoc interpolation, piped exit codes,
serving-layer verification, `.env` vs `.env.agent`), and `bin/outcome.py` to append structured
outcome records during runs. Deliberately *operational* knowledge only — channels, gates, traps —
no product ideas, no ICP, no strategy, preserving the context-free business axis while ending the
re-derivation tax. (The tension with "context-free" is real and named: the operator already
resolved it in issue #2 — memory of outcomes is wanted; memory of *strategy* stays out.)

### A8 — Horizon and pacing (fixes B8; issues #4, #6)
- `MAX_WALL_CLOCK_H` joins `MAX_ITERS` as a checkpoint (not failure) knob.
- The loop prompt gains a first-class **watch state**: when all levers are externally time-gated,
  the correct move is a long scheduled wakeup, not another iteration (v1 discovered this at 094;
  v2 makes it a named, legal state with `iter.py watch` so it costs ~0 tokens and no numbering).
- R&D-then-harvest stays legal (already in CLAUDE.md); the verified-milestone bar is unchanged.

---

## What "measurably superior" means (the scorecard)

Every claim of superiority gets a metric, its v1 baseline (measured from the run record), and how
v2 is checked. This table is the acceptance test for the redesign.

| # | Metric | v1 baseline (evidence) | v2 target | How verified |
|---|---|---|---|---|
| M1 | Evidence-loss events per run | ≥6 (023, 024, 027, 067, 070, 086, 089) | 0 | Kill-during-append test + no RECONSTRUCTED markers possible; verifier never touches claims lane |
| M2 | Self-certified run termination possible | Yes (happened, 095) | Structurally absent | `/goal` v2 has no exhaustion terminal; conclusion_gate cannot stop anything |
| M3 | Stop-gate checks novelty (not volume) | No (counted headers/emails) | Adversary report required | Gate exits non-zero without a fresh-context adversary artifact |
| M4 | Sends possible without recorded disclosure decision | Yes on main (and v1 botched 2 pre-gate) | 0 (fail-closed on main) | `mail.py` e2e refusal test |
| M5 | Sends that can be lost from the audit trail | All (SENT_LOG partly reconstructed) | 0 | append_log commits+pushes before SMTP |
| M6 | Publishes verified at the serving layer | 0 until iter 070 (surge trap) | 100% (gate-enforced) | aiv_gate requires host_check output for publish claims |
| M7 | Reach measurable (bot vs human decidable) | No — retraction 098 | Yes from hour one | beacon in harness + TRAFFIC_BASELINE protocol |
| M8 | Iteration-record defects (gaps, drift, wrong hashes) | 3 lost numbers, 22 drifted timestamps, 1 piped-exit error | 0 | scaffold owns numbering/time/hashes |
| M9 | v1 strategy nouns in agent-facing config | ≥3 (share-loop, localized, audits-X) | 0 | pinned grep list |
| M10 | Cross-run knowledge records | 0 structured | wall map + falsified table + traps seeded | files exist, schema-validated |
| M11 | Verifier heartbeats polluting claims history | 196 commits | 0 | heartbeats live on ledger branch |
| M12 | Broken-by-design paths on main | 1 (mail.py import) | 0 | e2e send test on fresh clone |

## Implementation order (one loop iteration each, ~20m cadence)

1. **This iteration:** inventory + this design + IMPROVEMENT_LOG + A5 (send path on main).
2. A1 — two-lane git (verifier_loop v2, `truth.py`, `append_log.py`, guard reads ledger branch).
3. A2 — conclusion_gate + adversary requirement + `/goal` v2 + guard cleanup.
4. A4 + A3a — `iter.py` scaffold + `host_check.py` (+ aiv_gate publish-claim hook).
5. A3b + A6 + A7 — beacon promotion, context genericization, `knowledge/` seed.
6. Audit iteration — adversarial self-critique of this design, fixes, final log entry.

## Standing critique (updated every iteration — see IMPROVEMENT_LOG for the running version)

- The adversary novelty check is agent-invoked → tripwire, not wall (named in A2; verifier-side run
  is the upgrade path).
- Two-lane git adds a failure mode: the agent reading a *stale* ledger branch. Mitigated by the
  existing H2 freshness halt, which transfers unchanged.
- `knowledge/` risks context contamination creep — each addition must pass the "operational, not
  strategic" test, and the pinned grep list (M9) should extend to it.
- Nothing here fixes v1's actual bottleneck-of-record (reach/conversion) — that is strategy, and
  deliberately out of scope for a harness redesign; what v2 fixes is that the *next* run can
  measure, persist, and correctly stop.

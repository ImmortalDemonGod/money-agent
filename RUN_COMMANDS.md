# Run commands (v2) — the `/goal` and `/loop` to issue

v1's commands are preserved verbatim on the run-1 branch (PR #8, `RUN_COMMANDS.md` there) together
with the defect analysis. The defect: v1's `/goal` carried a terminal-state-(b) — "exhaustion gate
exits 0 + a retro" — which let a self-graded, volume-counting gate END the run. It did, falsely,
at iteration 095 (docs/CASE_STUDY.md, issue #7). **v2 removes the agent's kill switch entirely.**

## `/goal` — the stop condition (v2)

```
/goal DONE when ledger facts (read them ONLY via bin/truth.py, never from memory) show
received_usd > 0 AND verified is true: one real CUSTOMER dollar has arrived. The verifier
classifies the payer, so a self-payment does NOT count. The instant it is true, STOP: no second
sale, no scaling. Write the retro in MONEY_LOG.md and hand back.

ALSO DONE when the edge rail is live and ledger/edge.json (via bin/truth.py --file edge.json)
shows verdict VERIFIED_POSITIVE_EV with verified true: the pre-registered bar was cleared on the
broker's books. STOP for operator review exactly as with the first dollar -- deploying real
capital is the operator's decision, never yours; bin/guard.py halts on this verdict.

One other legitimate terminal state: the card is exhausted (bin/guard.py reports it and halts).

THERE IS NO SELF-CERTIFIED EXHAUSTION TERMINAL STATE. bin/conclusion_gate.py exit 0 authorizes
WRITING an "impossible" conclusion in MONEY_LOG.md — it never ends the run, and you may not treat
it as a stop signal. After recording such a conclusion, enter a WATCH cadence (poll ledger, inbox,
and any live external bets on long wakeups) and keep responding to external signals. Only the
operator may end the run early.

Do not stop for any other reason, and never wait on the operator. Backstop: hand back after
MAX_ITERS iterations if set (a checkpoint for the operator, not a conclusion).
```

## `/loop` — the repeating work (v2; issue with NO interval — self-paced)

```
/loop
CLAUDE.md and PROMPT.md bind you every iteration and outrank any summary. Read them.

Work the loop, self-paced (go again the moment there is a distinct next thing to try):
1. Read the facts via bin/truth.py. Run bin/guard.py; it must exit 0 before you spend.
2. Plan 2-3 genuinely DISTINCT paths; pick one deliberately; never re-run a falsified approach
   (check knowledge/ and the packet's falsified table first).
3. Work AUTONOMOUSLY. Never wait on the operator or "hold for signals." Get external input
   yourself: WebSearch, parallel research subagents, build a tool.
4. Append to MONEY_LOG.md via bin/append_log.py (durable by construction): tried / cost /
   happened / learned / next. Write the aiv packet; bin/aiv_gate.sh <NNN> must pass.
5. Any "published X" claim must cite bin/host_check.py output for the LIVE url (run 1 shipped
   ~60 iterations of crawler-invisible product because nobody verified the serving layer).
6. When every live lever is externally time-gated (indexation, replies, approvals), that is a
   WATCH state: schedule a long wakeup instead of manufacturing motion. Watching is legal;
   padding is not. Every such lever must already be in the registry (bin/bets.py add) -- guard
   prints the due-bets agenda each iteration; check due bets first (bin/bets.py due / checked),
   and size the wakeup to the SLOWEST live clock (day-scale bets get day-scale wakeups).
7. Pursuing an edge on the paper rail? Pre-register the bar FIRST (bin/edge.py register), then
   work it; read the verdict only via bin/edge.py status.

Falsify before you conclude "blocked" — one failed test is n=1. An "impossible" conclusion may be
RECORDED only if bin/conclusion_gate.py exits 0 (effort floor + packet + a fresh-context adversary
that came back empty-handed + NO open bets in run/bets.json and no PENDING edge) — and recording
it does not end the run.
```

## Design intent

`/goal` = when to STOP, checkable by reading one verifier-owned fact. `/loop` = the repeating
WORK. The stop set is deliberately closed: {verified dollar, verified cap exhaustion, operator}.
Everything else — including the agent's own certainty that it is done — is a claim, and claims do
not terminate experiments. That asymmetry IS the v1 finding, made mechanical.

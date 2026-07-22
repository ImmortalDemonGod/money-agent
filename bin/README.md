# bin/ — who may run what (the trust map)

Every script belongs to exactly one trust class. The classes are the experiment: the agent
produces CLAIMS, the verifier produces FACTS, and the gates adjudicate one against the other.
`sod_hook.sh` enforces the write side (its blocklist covers every script in the VERIFIER-ONLY
and GATES tables, the agent tools, and `tests/`); this file is the read side, so a human or agent
can tell at a glance why a script exists and whether they should be touching it. The honest limit
that applies to every agent-side check in this repo: the hook is a tripwire -- the walls are the
out-of-band verifier (which executes its OWN checkout's scripts, never the agent branch's) and
remote branch protection.

## VERIFIER-ONLY — run on the operator's machine, never in the sandbox (they hold/read keys)

| Script | What it does |
|---|---|
| `pnl.py` | THE verifier: aggregates registered receive/spend adapters (Stripe + card feed + optional Base), writes `ledger/truth.json` + hashed raw pulls |
| `edge_pnl.py` | the edge-rail verifier: freezes the pre-registered bar, pulls the broker's paper books, writes `ledger/edge.json` |
| `set_baseline.py` | freezes run-start: baseline OID + timestamp + constitution hash (+ archives any stale edge freeze) |
| `verifier_loop.sh` | the publish loop: converge facts lane → pnl → edge_pnl → commit/push (+ rotation) |
| `start_verifier.sh` | one-shot run start: lane creation → baseline → loop launch |
| `verifier_daemon.sh` | launchd/systemd entrypoint for the loop |
| `run_weak.sh` | co-located weak-mode loop for fast local trials — tripwire-only, never resets |
| `supervise.sh` | operator one-screen status + VERDICT line (first dollar / edge verified / signed human actuation or sync / stale / dead) |
| `set_live_keys.sh`, `load_keys.sh` | key plumbing helpers |

## GATES — run in the agent's environment, adjudicate claims against verifier facts (tripwires by design; the walls are the out-of-band verifier + remote branch protection)

| Script | What it gates |
|---|---|
| `guard.py` | EVERY iteration start: cap, staleness, SoD authorship, first-dollar stop, edge verdict, constitution, bets agenda |
| `aiv_gate.sh` | EVERY iteration close: canonical `aiv check`, evidence classes A–F, money/edge claims vs verifier numbers, publish claims re-verified |
| `conclusion_gate.py` | permission to RECORD an "impossible" conclusion (never a stop): effort floor + packet + fresh-context adversary + no live bets + independently grounded human outcomes |
| `disclosure_gate.py` | every outbound message: AI-disclosure EV decision recorded, keep-disclosures must lead |
| `host_check.py` | publish claims: is the page actually served to crawlers (robots/meta/SSRF-guarded fetch) |
| `sod_hook.sh` | pre-commit: blocks agent writes to `ledger/`, CONSTITUTION, and every script in this table |
| `exhaustion_gate.py` | DEPRECATED shim → `conclusion_gate.py` |

## AGENT TOOLS — the run agent's own instruments (claims side)

| Script | What it does |
|---|---|
| `truth.py` | THE read path for facts (`--file edge.json` for the edge rail); labels every source's trustworthiness |
| `iter.py` | iteration scaffold: `new` (number+anchors), `close` (gate+commit+verify), `watch` (cheap tick, no iteration burned) |
| `bets.py` | day-scale bet registry: `add` / `due` / `checked` / `resolve` — open bets block conclusions |
| `edge.py` | edge rail claims side: `register` (commit the pre-registered bar), `status` (grounded verdict) |
| `mail.py` | email under the real name: inbox/read/search/send, disclosure-gated, SENT_LOG fail-closed |
| `human.py` | request mechanical operator actuation; operator signs/publishes a hash-bound resolution on a distinct facts lane, agent syncs and meters it |
| `outcome.py` | append structured outcomes to `knowledge/` (strategy-denylisted) |
| `append_log.py` | durable append: commit-before-action so no reset can eat a log line |

## OPERATOR LIFECYCLE

| Script | What it does |
|---|---|
| `new_run.sh` | close run N: archive all run-state to `archive/run-N/`, seed clean logs (see the correctness note in its header) |
| `setup_sandbox.sh` | fresh-clone setup: install `aiv`, repair its hook shebang, chain `sod_hook` |

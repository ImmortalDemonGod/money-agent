# The Money Agent

### A verification testbed: can you trust what an autonomous agent tells you about money, including its claim to be finished?

The entry question was simple: *can a context-free agent, given a card and a payment rail, make money?* But
the real subject is one layer up. "I made money" and "I have exhausted every option" are the two most
tempting claims an autonomous agent could fabricate, so money is the ideal testbed for the actual question:
**how do you verify what an agent tells you, when it has every incentive to tell you it succeeded?**

This is a living research program. It has versions. Each one is designed by the last one's findings.

---

## The invariant (holds across every version)

**The agent produces CLAIMS. A verifier it cannot invoke produces FACTS. The gap between them is the whole
subject.**

`ledger/truth.json` is computed by a verifier the agent cannot reach, from the Stripe API and the card feed,
using credentials the agent never holds, on a machine outside its sandbox. The agent narrates into
`MONEY_LOG.md`. When the two disagree, the ledger is right, by construction. The agent cannot write its own
P&L. Everything else in this repo is downstream of that one boundary.

---

## Status

| Version | Cap | Horizon | Result |
|---|---|---|---|
| **v1** (concluded) | $25 | overnight, first-dollar stop | **$0.00, verified.** Two findings that redesigned the program. See [`docs/CASE_STUDY.md`](docs/CASE_STUDY.md). |
| **v2** (in design) | more capital | longer, with a build-and-verify phase | The experiment v1's findings *designed*. Grounded stop-verification + delayed-payoff strategies. See the [issues](../../issues). |

v2 is **not** "v1 with a bigger cap." It is the specific experiment v1's two findings pointed to.

---

## Finding your way around

Every file here answers to one of four readers. Start from who you are; skip everything not
addressed to you.

**You are the OPERATOR (provisioning or starting a run):**
`SETUP.md` end to end, then issue #20 (the pre-run-2 acceptance gates), then `bin/new_run.sh`
to close the previous run and `bin/start_verifier.sh` to open yours. `docs/STANDING_RUN.md` if
the run should last days. That is the whole list.

**You are the RUN AGENT:**
your world is `CLAUDE.md` (the bounds), `CONSTITUTION.md`, `PROMPT.md`, `RUN_COMMANDS.md`,
`knowledge/` (what past runs falsified, so you do not re-pay for it), `templates/` (the forms the
gates require), and the facts via `python3 bin/truth.py`.

**You are a REVIEWER or AUDITOR (did it really?):**
`ledger/truth.json` and `ledger/edge.json` on the run's ledger branch are the only real numbers;
`REFUSALS.md` is what it would not do; `MONEY_LOG.md` vs the ledger is the claim-vs-fact drift;
`IMPROVEMENT_LOG.md` is the full harness reasoning trail with per-entry critiques;
`docs/CASE_STUDY.md` is the verification-theater finding that redesigned the program.

**You are a CONTRIBUTOR (changing the harness):**
`docs/V2_DESIGN.md` is the architecture of record — the harness that actually shipped (B1–B9 →
A1–A8, verified by the M1–M12 scorecard); `docs/V2_HARNESS_DESIGN.md` is a forward-looking
proposal (the bet-ledger + business-spine model and the P1–P7 primitives), mostly unbuilt and
carrying one open in-bounds question, so read it as direction, not as what exists. `bin/README.md`
for what each script is and who may run it (the trust classes are the entire point of this repo),
`bash tests/sim.sh` before and after your change — it has caught every real defect four reviews
found.

| Directory | Owner | What lives there |
|---|---|---|
| `bin/` | mixed — see `bin/README.md` | every executable: verifier-side, agent-side, gates, operator tools |
| `ledger/` | **verifier only** | the facts: `truth.json`, `edge.json`, raw API pulls + hash manifests |
| `knowledge/` | agent (append), operator (review) | cross-run operational memory — channels tested, approaches falsified, traps |
| `templates/` | operator | the forms a run fills in: exhaustion packet, adversary report, edge registration |
| `tests/` | contributor | the committed two-lane simulation matrix (`sim.sh`) |
| `docs/` | humans | design, case study, standing-run recipe — the agent does not read these |
| `harness/` | operator | the traffic beacon (Cloudflare worker) |
| `archive/` | `bin/new_run.sh` | each finished run's frozen state, one directory per run |
| `.github/aiv-packets/` | agent (per iteration) | AIV verification packets — one claim + evidence classes A–F each |
| root `*.md` logs | agent (append-only) | the LIVE run's claims: `MONEY_LOG`, `SENT_LOG`, `REFUSALS`, `DISCLOSURE_EV_LOG` |

---

## Findings so far

Each one names the change it forces in the next version.

**1. The wall is reach, and the wall is an artifact of the objective.**
v1's binding constraint was never product quality or honesty. It was reach to a stranger who will pay. But
that wall is an artifact of measuring *time-to-first-dollar*: a "make a dollar tonight" objective forbids
every strategy whose payoff follows a research-and-build phase (validate an edge, rank a page, earn a
reputation) and leaves only reach-gated hustle. The frame did not fail to find good strategies. It forbade
them.
→ **v2 lifts the constraint:** more capital and a longer horizon, so delayed-payoff strategies become legal
and testable for the first time.

**2. The system had two verification surfaces, and only one was grounded.**
Money was verified out of band, and the resulting $0.00 is trustworthy. But "the task is exhausted" was
self-certified by a gate that *counts the agent's own effort artifacts* and then prints `EXHAUSTION PROVEN`.
It counted; it never checked. The agent stopped on that false certification with a real bet still live.
Outcome trustworthiness tracked verification quality one to one: the grounded surface produced a fact, the
theater surface produced a rumor with a checkmark.
→ **v2 grounds the stop decision the way money is grounded** (issue #7, the precondition for a meaningful v2).

The full writeup of finding 2 is [`docs/CASE_STUDY.md`](docs/CASE_STUDY.md).

---

## Roadmap

The open work is the [issue tracker](../../issues). In dependency order: **#7** grounds the stop decision (do
this first, or v2 reproduces v1's premature-stop failure); #1 and #2 raise the agent's craft; #3, #4, and #6
address the reach-is-an-artifact finding by giving it time, findable surfaces, and delayed-payoff strategies;
#5 is targeting.

---

## Read the evidence

The repo is the evidence. Nothing here asks you to take our word for it. One navigation note: `main`
carries the harness with the run logs reseeded; **run 1's full artifacts live on its run branch —
[PR #8](../../pull/8)** — until they are archived under `archive/run-001/`.

1. **`ledger/truth.json`** — the only numbers that are real.
2. **`MONEY_LOG.md` vs `truth.json`** (run branch) — the drift between what the agent said and what was true, measured.
3. **`REFUSALS.md`** (run branch) — what it would not do. The most honest file here.
4. **`docs/CASE_STUDY.md`** — the verification-theater finding in full.
5. **`iterations/`** (run branch) — everything it tried, in order.

---

## Run it

Provisioning (a real Stripe account, two restricted keys, an issuer-capped card, the two-machine verifier) is
in [`SETUP.md`](SETUP.md).

---

## What this is, and is not

- **It is** a study in grounded verification, using "make money" as a testbed precisely because it is the most
  fabrication-prone class of claim. The goal is an agent that *consistently and verifiably* makes money -- at
  which point it is a make-money kit, and, unusually, a trustworthy one.
- **It is not** *yet* that, and the word carrying the weight is *consistently*: a single lucky dollar is
  variance, not a kit -- which is exactly why the verification matters, because it is what separates an earned
  "it makes money" from a lucky screenshot. It is not a trading bot or a growth hack, and it is not a claim
  that agents cannot make money. v1's premature stop means the money question is genuinely still open; v2
  reopens it, under verification you can trust.

---

*Black Box Research Labs. The interesting artifact was never the money. It was learning, on ourselves, that an
outcome is only ever as trustworthy as the verification underneath it.*

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

The repo is the evidence. Nothing here asks you to take our word for it.

1. **`ledger/truth.json`** — the only numbers that are real.
2. **`MONEY_LOG.md` vs `truth.json`** — the drift between what the agent said and what was true, measured.
3. **`REFUSALS.md`** — what it would not do. The most honest file here.
4. **`docs/CASE_STUDY.md`** — the verification-theater finding in full.
5. **`iterations/`** — everything it tried, in order.

---

## Run it

Provisioning (a real Stripe account, two restricted keys, an issuer-capped card, the two-machine verifier) is
in [`SETUP.md`](SETUP.md).

---

## What this is, and is not

- **It is** a study in grounded verification, using "make money" as a testbed precisely because it is the most
  fabrication-prone class of claim.
- **It is not** a make-money kit, a trading bot, or a claim that agents cannot make money. v1's premature stop
  means the money question is genuinely still open. v2 reopens it, this time under verification you can trust.

---

*Black Box Research Labs. The interesting artifact was never the money. It was learning, on ourselves, that an
outcome is only ever as trustworthy as the verification underneath it.*

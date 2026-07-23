# Acceptance: the capability-delegation queue (`bin/actuate.py`)

This is the agreed **definition of done** for redesigning the human-actuation queue — written
test-first. The runnable harness is [`tests/acceptance_actuation.py`](acceptance_actuation.py);
this file is its human-readable companion (the contract, the benchmarks, and the two tiers of
"done"). If the two ever disagree, the harness is authoritative — it is the thing a fresh party
runs.

## The goal

Turn the queue from a thin **gate-signal** into a reliable, usable **capability-delegation**
channel — the agent's hands for bounded actions it is structurally barred from (claim/deploy a
host, fund a wallet, pass a one-time KYC) — so a strategy like x402 becomes reachable, **without
weakening `actuator-never-oracle` or separation-of-duties.**

The unit of work is *"perform a bounded real-world action I can't, in your own authenticated
context, and hand me back what it produced"* — not "approve my action" (HumanLayer's loop) and
not "solve this captcha for me" (structurally unservable — removed).

## Why these exact scenarios (grounded in run 1, not theory)

The run-1 agent hit this repeatedly and had to **hand-write operator files** because there was
no channel — the archive still holds them:

- `archive/run-001/OPERATOR_CLAIM_workers_dev.md` (iter 089) — a Cloudflare Worker with a **hard
  60-minute claim window**, plus a fixed `worker.js` the agent staged but *could not deploy*
  ("my sandbox wrangler is unauthenticated"). It succeeded **only because a human was watching
  live.** → scenarios **S1** (claim-host + deadline + staged artifact) and benchmark **B2**
  (deadline-aware notification). The current queue's 24h poll would have missed the window.
- The signup-gate wall map (iters 003/004/012/013; IndieHackers birthday widget 010–057) →
  **S3** (a one-time human KYC/signup that returns credentials).
- `OPERATOR_UNBLOCK.md` / `OPERATOR_NOTE` — the operator writing **strategy** back ("stop
  grinding the audit business", "try non-English"). That is the oracle direction this guardrail
  exists to forbid → negative test **N2**.
- Issue #30 OQ1 (x402 needs a funded Base wallet) → **S2** (wallet-fund).

## Definition of done — two tiers

**Tier-S — provable on our branch now (keyless, offline).** `python3 tests/acceptance_actuation.py`
exits 0: all 9 checks PASS. This is fully in our control and is what "done for testing" means.

**Tier-L — the live gate (operator, not self-certifiable).** One real actuation verified out of
band: a real host claimed, or a real testnet wallet funded, with the agent demonstrably using
the returned artifact. Like every live seam in this repo (issue #20), **we name it and hand it to
the operator — we never fake it green.**

## The checks

| ID | Proves | Grounded in |
|----|--------|-------------|
| **S1** | claim-host round-trip: request (with deadline + staged artifact) → signed fulfill → agent `sync` materializes the confirmation | iter 089 |
| **S2** | wallet-fund round-trip: a non-secret value return flows back to where the agent consumes it | issue #30 OQ1 |
| **S3** | secret credential handback: **ciphertext-only in git**, plaintext recovered only in-sandbox | issue #32 signup slice |
| **N1** | SoD: a forged / unsigned resolution is **rejected** by `sync` (the agent cannot fabricate "a human acted") | the whole thesis |
| **N2** | actuator-never-oracle: a request whose free text smuggles strategy/content is **refused** | `OPERATOR_UNBLOCK.md` leak |
| **N3** | secret-never-in-git: after a secret fulfill, **zero** plaintext in any committed object | deliver-in-full / no-leak |
| **N4** | metering: `human_minutes` is required and recorded on **both** fulfill and decline | issue #31 metering guardrail |
| **B1** | usability (measured, no live human): the rendered **card** carries every field a no-context operator needs | the bar today's design flunks |
| **B2** | deadline-aware notification: near-deadline → `URGENT`, far → `NORMAL` | the 60-minute window |

The harness is **bite-verified**: run against a no-op stub, all 9 checks FAIL (not PENDING) with
meaningful reasons — so it distinguishes *unbuilt* (PENDING) from *broken* (FAIL) from *real*
(PASS). This mirrors the repo's `tests/corpus.sh` discipline (assert on substance, prove the
test bites).

## The benchmarks (simple, measurable bars)

- **B1 — Card completeness (usability proxy).** The `card <id>` output must contain all seven
  required fields: target URL, each ordered step, the deadline, the expected result, the staged
  artifact reference, and the exact fulfill command. Missing any one is a FAIL. A human with
  *only the card* must be able to complete the task — this replaces "reconstruct context from a
  cited packet." Score = fields present / 7; PASS at 7/7.
- **B2 — Notification urgency.** `notify-scan` classifies a task `URGENT` when its deadline is
  within `NOTIFY_URGENT_S` (default 900s), else `NORMAL`. PASS = a near-deadline task flagged
  URGENT and a far one NORMAL in the same scan.
- **N3 — Secret-leak (binary).** `git grep` for the plaintext across **all** objects of the bare
  origin returns nothing after a secret fulfill.

## How to run

```bash
python3 tests/acceptance_actuation.py      # scorecard; exit 0 only when all 9 PASS
```

Requires `ssh-keygen` (the verifier signature, same dependency as `tests/sim.sh`) and, for the
secret return channel, an asymmetric-crypto tool the implementation chooses (`age` or `openssl`).
Everything runs offline in a throwaway two-lane git world (`$AGENT_BRANCH` claims lane +
`$LEDGER_BRANCH` facts lane); nothing touches the real repo or the network.

## Contract summary (`bin/actuate.py`)

Full contract is in the harness docstring. In brief:

- **Agent (claims lane):** `request` (typed work-order + ephemeral encryption keypair + companion
  bet + deadline-aware wakeup) · `card` (render the operator UX) · `sync` (verify signature +
  binding, decrypt + materialize the return, meter) · `list` / `due`.
- **Operator (facts lane, must differ from the claims lane):** `fulfill` (encrypt any secret
  return to the task's published key, retain plaintext off-repo, sign + push) · `decline`.
- **Notifier (out-of-band, read-only):** `notify-scan` (deadline-aware alerts to a sink).

Implement to this contract; revise it only deliberately, in the same commit that revises the
harness — never by quietly loosening a check.

## Out of scope for Tier-S (named honestly)

- The live actuation (Tier-L) — needs the operator and real credentials.
- The concrete notification transport (ntfy/email/Telegram) — `notify-scan` emits to a sink; the
  transport that reads the sink is an operator-side, out-of-sandbox wiring choice.
- The agent-side durable wakeup mechanism (issue #20.6) — the harness asserts the deadline is
  *recorded and classified*, not that a specific scheduler fires it.

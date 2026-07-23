# Acceptance: the capability-delegation queue (`bin/actuate.py`)

This is the agreed **definition of done** for redesigning the human-actuation queue — written
test-first. The runnable harness is [`tests/acceptance_actuation.py`](acceptance_actuation.py);
this file is its human-readable companion (the contract, the benchmarks, and the two tiers of
"done"). If the two ever disagree, the harness is authoritative — it is the thing a fresh party
runs.

**Status:** Tier-S is **GREEN** — `bin/actuate.py` (+ `bin/actuate_notify.sh`, `bin/actuate_watch.sh`)
implemented to the contract; `python3 tests/acceptance_actuation.py` reports **24 PASS / 0 FAIL**,
and it is **gate-enforced in CI** (a job in `.github/workflows/ci.yml`), not self-reported. Existing
suites unaffected (`sim.sh` 163/0, `corpus.sh` 11/0). **Four** adversarial rounds found real defects —
round 1: binding confusion, shell injection/exfiltration, an unguarded conclusion gate, a
tz-naive-deadline poison (→ N5–N11); round 2 (re-attacking the fixes): id/kind still forgeable,
artifact bytes bound-but-unchecked, a best-effort bet that holed the file-deletion backstop
(→ N12–N14); round 3: the artifact sha check bypassed by nulling the sha field (→ N15); round 4:
the swap-to-oracle-before-fulfill vector (→ N16), then clean. A subsequent operator review added the
money-moving P3 name-test gate (→ N17) and the open-request cap (→ N18); a follow-up design review
added the post-handback usability probe (→ N19) for the WAF/IP-reputation residual. All fixed and
regression-locked. Tier-L (one live actuation on a real rail) remains an operator gate.

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
exits 0: all 24 checks PASS. This is fully in our control and is what "done for testing" means.

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
| **N5** | SoD: rewriting any operator-visible field (identity/steps/expect/artifact) **after** the operator signs breaks `sync` (full-task hash binding) | adversary: binding confusion |
| **N6** | SoD: a resolution **signed by a key not in `allowed_signers`** is rejected (N1 only covered *unsigned*) | adversary: anchor/key gap |
| **N7** | a `gate` with a newline / embedded `urgency=URGENT` cannot forge an ALERT line or override the parsed fields, and the real notifier does not dispatch it | adversary: shell injection |
| **N8** | leak-check covers the **staged artifact bytes and the target URL**, not only gate/steps | adversary: unscanned channels |
| **N9** | a **timezone-naive** `--deadline` is rejected (it silently poisoned `next-wakeup`/`notify-scan`) | adversary: tz poison |
| **N10** | a **binary** (non-UTF-8) credential round-trips byte-exact via base64, never mangled | adversary: lossy decode |
| **N11** | an **open actuation blocks `conclusion_gate.py`** directly, independent of the companion bet | adversary r1: unguarded gate |
| **N12** | a newline in **`id` or `kind`** (not only `gate`) cannot forge an ALERT line; all agent fields scrubbed + id-format validated | adversary r2: incomplete scrub |
| **N13** | swapping the **staged artifact bytes** after signing is rejected — fulfill re-verifies the file against the bound sha256 | adversary r2: sha bound but unchecked |
| **N14** | **deleting** `actuation_tasks.json` still blocks conclusions via the now-**mandatory** companion bet's orphan check | adversary r2: best-effort bet holed it |
| **N15** | swapping the artifact bytes while **nulling** `artifact_sha256` is rejected — a ref present *requires* a matching sha | adversary r3: sha-field bypass |
| **N16** | swapping the artifact to **oracle content with a consistent sha** before fulfill is caught — fulfill re-runs the leak-check on the actual bytes | adversary r4: pre-fulfill swap |
| **N17** | a **money-moving** kind (`wallet-fund`) cannot be fulfilled without a recorded **P3 name-test ruling**, embedded in the signed resolution | owner review #2 |
| **N18** | the **open-request cap** (default 3) refuses a further request while the queue is full (each open request blocks conclusions) | owner review #6 (§12 R1) |
| **N19** | a **pre-registered post-handback usability probe** runs at `sync`: a pass records `usability=verified`; a fail flags the handback unusable and makes `sync` exit non-zero, **while the operator obligation stays discharged** (agent-side tripwire, downgrade-only) | design review: WAF/IP-reputation residual |

**On the actuator-never-oracle leak-check:** it is a **heuristic tripwire, not a wall** — a denylist
cannot catch every paraphrase. It is applied to every operator-facing surface (gate/steps/expect/
identity/target-url/artifact) with word-boundary matching, and it catches the obvious oracle asks and
the run-1 `OPERATOR_UNBLOCK` strategy-leak class. The **wall is the human operator**, who sees the
rendered card and can `decline` any oracle-shaped request (a metered decline is the operator's
REFUSALS mirror). N2/N8 test the tripwire; they do not claim it is complete.

The harness is **bite-verified**: run against a no-op stub, all 24 checks FAIL (not PENDING) with
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
python3 tests/acceptance_actuation.py      # scorecard; exit 0 only when all 24 PASS
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

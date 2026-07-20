# SETUP

How to provision the money-agent so the result means something. The design goal of every step below is the
same: keep the load-bearing controls **outside the agent's reach**. Read the [README](README.md) first for
why that matters.

---

## Two deployment modes

| Mode | Verifier runs | SoD strength | Use when |
|---|---|---|---|
| **Strong** | On a separate machine, outside the sandbox, via a supervisor (e.g. launchd) | **Real.** The agent cannot reach the read key at all. | You want the result to mean something. |
| **Weak** | Inside the sandbox with a read-only key | Tripwire only. A sandboxed agent can edit any file it can see. | A fast local trial. |

`bin/guard.py` checks git authorship of `ledger/` as a tripwire in weak mode. Be honest that it is a tripwire,
not a wall. Only two things are actually load-bearing: the **card issuer's own spend limit** and an
**out-of-sandbox verifier**. Everything else is a prompt asking nicely, and you should treat it that way.

### v2 topology: two lanes

In v2 the verifier publishes facts to a dedicated **`ledger` branch** from its own checkout
(`bin/verifier_loop.sh`); the agent's branch is never reset or written by any harness process (v1's
shared-worktree reset destroyed agent evidence six documented times). The agent reads facts only via
`bin/truth.py`. Start everything with `bin/start_verifier.sh <agent-branch>`.

**What actually makes this a wall vs a tripwire (be honest about it).** Branch protection on
`ledger` is *necessary but not sufficient*. An agent that controls its own git config can repoint
`origin`, or push a fake `origin/<other>` branch with commits authored as `verifier`, and
`truth.py` reading an agent-settable `LEDGER_BRANCH` would then read agent-written "facts"
(CodeRabbit). The boundary is only a real wall when **provisioning** removes those degrees of
freedom, ALL of these together:

- the sandbox's `origin` is pinned to the canonical remote and the agent cannot change it;
- the agent has **no push credential** that can create/modify branches on that remote (only the
  out-of-sandbox verifier does);
- `LEDGER_BRANCH` is fixed by the operator, not taken from agent-controlled env.

Without that, the SoD checks (`guard.py` authorship, `sod_hook.sh`, the `truth.py` source label)
are **tripwires**, exactly like every other in-repo control — the only unconditional walls remain
the **out-of-band verifier** and the **card issuer's spend limit**. `guard.py`'s SoD check is now
ancestry-scoped (committer-date-independent) and fail-closed, which raises the tripwire's bar but
does not, by itself, replace the provisioning above.

---

## 1. A dedicated Stripe account

Register an **Individual / sole-proprietor** Stripe account for the agent. KYC needs a legal name, DOB,
address, a tax ID as required, and a bank account for payouts.

> **This is where "pure unbiased sandbox" ends, and that trade is unavoidable.** Receiving money requires a
> KYC'd identity, and Stripe binds that identity to a real person permanently. The agent stays context-free on
> the *business* axis (no market, product, or thesis supplied); it cannot stay anonymous on the *legal* axis.
> Use an identity you are willing to have permanently attached to everything the agent does. **Do not use an
> entity you need to keep clean for other purposes** (a government-registered business, anything tied to
> compliance or contracting). Isolate the entity; you cannot isolate the person.

### Inbox posture (decide deliberately)

Registration needs a click on a verification link, so someone reaches the inbox at least once. Three postures:

| Posture | The agent can | Cost |
|---|---|---|
| **Registration only** | nothing; the operator clicks the link, the agent never sees mail | No customer replies, resets, or platform mail. Caps what "make money" can mean. |
| **Read-only** | read, not send | Receives receipts and verifications, cannot send. Best safety ratio, but needs OAuth + a `gmail.readonly` token plumbed into the sandbox. |
| **Read + send** | full email | Real business capability, **and the one path to permanent reputational damage under a real name.** |

If you choose **read + send**, do it knowing it is the riskiest posture: the controls that remain are soft
(every send logged to `SENT_LOG.md` before it leaves, cold outreach banned by `CONSTITUTION.md`, the name
test). Those are prompts, not walls. `bin/mail.py` (`inbox` / `read` / `search` / `send`) reads
`GMAIL_ADDRESS` + `GMAIL_APP_PASSWORD` from the agent's environment.

---

## 2. Two restricted keys (the SoD boundary, made real)

Dashboard → Developers → API keys → **Create restricted key**. Two separate keys:

**`STRIPE_READ_KEY`** — the verifier's. **The agent must never see this.**
- Balance: Read · Balance transactions: Read · Charges: Read · Payouts: Read · everything else: None

**`STRIPE_WRITE_KEY`** — the agent's. Only what it needs to sell.
- Products: Write · Prices: Write · Payment links: Write · Checkout sessions: Write
- Balance / Payouts: **None** (deliberate: it sells; it does not audit itself)

---

## 3. Payouts and the card

Money lands in the bank account added at KYC. The sequence is always
`customer → Stripe (KYC) → payout → card`. The card is the **last hop**, not the receiving rail; nobody pays a
stranger by pushing to a card number.

**For the spend side, use an issuer-capped card.** A virtual-card provider with a hard monthly spend limit
(e.g. Privacy.com) is the only option where the cap is enforced by the *issuer*, not by a prompt. Create a
card with a hard limit equal to your cap, give the agent the card **number**, and give the verifier the spend
feed (`PRIVACY_READ_KEY`, or a `CARD_CSV=path` with `date,amount,description`). The agent cannot talk its way
past a decline.

---

## 4. Environment

Verifier only (never in the sandbox in strong mode):
```bash
export STRIPE_READ_KEY=rk_live_...     # restricted, read-only
export PRIVACY_READ_KEY=...            # or CARD_CSV=/path/card.csv
export CARD_CAP_USD=25                 # the number you're happy to pay for the answer
```

Agent's sandbox:
```bash
export STRIPE_WRITE_KEY=rk_live_...    # products/prices/links/checkout ONLY
# card number goes here, or wherever the sandbox stores secrets
# GMAIL_ADDRESS / GMAIL_APP_PASSWORD if using read+send email
```

**The wash-trade allowlist (required before any offer goes live).** `pnl.py` classifies every
charge's payer against `$MONEY_AGENT_STATE/operator_identity.json` (default
`~/.money-agent-verifier/operator_identity.json`) so an operator self-purchase can never trip the
first-dollar success condition. Provision it on the verifier machine:
```json
{"emails": ["<operator email>"], "card_fingerprints": ["<stripe card fingerprint>"]}
```
`bin/start_verifier.sh` refuses to start while it is missing or empty (issue #37) -- an inert
wash-trade guard only surfaces at the first charge, where it halts the run as unverifiable instead
of counting a legitimate sale. The sandbox's `setup_sandbox.sh` cannot check this file (the state
dir is deliberately unreachable from the sandbox), which is why the check lives verifier-side.

Optional loop-cost ceiling (bounds token spend, distinct from the money cap):
```bash
export MAX_ITERS=100   # 0 or unset = unbounded
```

---

## 4b. Optional: the verified-edge rail (issue #6)

A second scored surface for R&D-then-harvest strategies: the agent pre-registers a falsifiable bar
(`EDGE_REGISTRATION.md`: metric, threshold, minimum fills, deadline), and the verifier computes the
verdict from a **paper** brokerage account's books (`bin/edge_pnl.py` → `ledger/edge.json`,
published on the ledger branch like every fact). Provision it only if the run design wants this
variant; unprovisioned, the rail is inert.

1. Create an **Alpaca paper account** (no real funds — paper is the point: the bar must be cleared
   before real capital is even *discussable*, and that discussion is the operator's, mechanically:
   `guard.py` halts on `VERIFIED_POSITIVE_EV`).
2. Verifier's `.env` gets the paper keys (see `.env.example`). **Honest grounding note:** Alpaca
   has no read-only scoped keys, so unlike Stripe the split is not "agent cannot read." What
   grounds this rail is that the published number comes from the broker's own books via the
   verifier: the agent cannot fabricate a fill or an equity curve — the only way to move
   `paper_pnl_usd` is to actually trade, which is the measured thing. Give the agent its own copy
   of the creds (in `.env.agent`) **only** if the run design wants it placing orders itself.
3. The deadline is load-bearing: missing it = `FALSIFIED`. Clearing the bar under the minimum fill
   count stays `PENDING` (variance is not an edge). Editing the registration after the verifier
   freezes it = `VOID` (bar-moving, detected).

**Live acceptance (B10 — do not skip): the rail is simulation-tested only until this passes.**
Before trusting the edge rail in a real run, one live cycle against the actual paper API:
```bash
# on the verifier machine, with ALPACA_PAPER_* in .env and AGENT_BRANCH exported:
# 1. agent side: commit a toy registration (tiny bar, small min fills, short deadline) via
#    bin/edge.py register
# 2. verifier: python3 bin/edge_pnl.py   -> expect "registration FROZEN" + verdict PENDING
# 3. place ONE paper order in the account; next cycle -> fills count moves
# 4. edit the registration file and re-run -> expect verdict VOID (bar-moving detected)
# 5. revert, delete the toy freeze from $MONEY_AGENT_STATE/edge_registration.json, re-register
#    the real bet
```
Each step checks one seam that the simulation stubbed: auth, the account/orders/positions
endpoints' real field shapes, the freeze file, and integrity detection. If any step surprises,
fix before the run — an edge verdict from an unproven rail is exactly the class of green check
this program exists to kill.

---

## 4c. Optional: standing-presence posture (issue #4)

Run 1 proved a minutes-cadence loop cannot harvest day-scale clocks (indexation, approvals,
reputation). A standing run is CONFIG, not new machinery — see `docs/STANDING_RUN.md` for the
recipe: `MAX_WALL_CLOCK_H` as the operator checkpoint, `LEDGER_MAX_COMMITS` so the facts lane
doesn't grow unboundedly for days, verifier cadence, and the bet-registry discipline
(`bin/bets.py`) that makes multi-day waiting accountable instead of amnesiac.

---

## 5. Prove it works BEFORE the loop starts

```bash
python3 bin/pnl.py       # must print truth.json with verified:true
python3 bin/guard.py     # must print OK + remaining
```

If `bin/pnl.py` cannot reach Stripe it **refuses to write `truth.json`** and exits non-zero, and `guard.py`
then halts. That is intentional: a failed pull is not $0 earned, and an unverified ledger is worse than no
ledger, because it looks like evidence.

---

## 6. Freeze the prediction, then run

```bash
git tag prediction-frozen && git log -1 --format=%H
```

Then start the loop with the prompt in `PROMPT.md` and the goal/stop condition. The bounds the agent is held
to (compaction-durable) are in `CLAUDE.md`; the full constitution is in `CONSTITUTION.md`.

---

## Reading it afterward

In this order: `ledger/truth.json` (the only real numbers) → `REFUSALS.md` (what it would not do) →
`MONEY_LOG.md` vs `truth.json` (the drift between claim and fact) → `PREDICTION.md` (was it right?) →
`iterations/` (what it tried, in order).

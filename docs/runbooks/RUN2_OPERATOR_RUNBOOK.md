# Run-2 operator runbook

Everything between "merged main" and "a trustable run 2," command by command, with the output
you should see and what it means when you do not. The numbered steps DECIDE nothing -- every knob
choice lives in the **Decisions** section immediately below; walk and sign it first, then the steps
read the values you set there. Steps marked **[preflight: X]** have a mechanical check that refuses
to proceed if you skipped them; steps marked **[no automated check]** are enforced only by this
line -- read those twice.

Order matters: Decisions -> 0 -> 1 -> 2(optional) -> 3 -> 4 -> 5 -> 6 -> 7 -> 7b -> 8/9(optional) -> 10 -> 11 -> 12.
Section 11 (the #32 signup probes) is NOT optional -- it is the evidence this run exists to collect;
sign-off (12) is not complete until every Section 11 probe is done or recorded `not_run` with a reason.

---

## Decisions -- the operator's pre-flight checkbox memo (fill and sign before Section 0)

Every knob the run-2 harness reads, with a recommended value, the reason, and where the knob
lives. Check each box (or strike the recommendation and write your own value NEXT TO IT) before
`bin/start_verifier.sh` runs. Nothing here is self-executing: an unchecked box means the coded
default applies. The NEW machinery and spend defaults fail closed (new gates OFF, exposure caps
ZERO). But NOT everything is conservative: `SHADOW` defaults to a LIVE posture, and the wall-clock
(`MAX_WALL_CLOCK_H`) and iteration (`MAX_ITERS`) caps default OFF -- no duration bound. Treat the
posture and duration boxes as MANDATORY, not optional: skipping them starts an unattended live run
with no time limit, which is the opposite of conservative.

Legend: [code default] is what happens if you do nothing.

### D1. Run shape

- [ ] **SHADOW rehearsal first** -- recommended: run a 2-4h `SHADOW=1` shadow run (test-mode
  Stripe key, no card creds, `shadow-ledger` lane) BEFORE the live run, and read
  `bin/shadow_metrics.py` output. It exercises every new gate end-to-end for free.
  [code default: SHADOW unset = live posture] (S12; shadow/README.md)
- [ ] **MAX_WALL_CLOCK_H=96** -- bounds unattended wall-clock; a checkpoint, not a conclusion.
  [0 = off] (bin/guard.py)
- [ ] **MAX_ITERS=0** (off) -- the wall-clock checkpoint above is the binding one; an iteration
  ceiling double-gates and run 1 showed iteration counts drift. Set only if token cost needs
  its own cap. [0 = off] (bin/guard.py)
- [ ] **LEDGER_BRANCH=ledger-run2** -- fresh facts lane per run; protect it on the remote
  (verifier-only push) for SoD-as-a-wall. [ledger] (bin/truth.py; SETUP.md)

### D2. Verifier cadence + durability

- [ ] **INTERVAL=300** -- verifier cycle seconds. 300 keeps API volume sane on a multi-day run.
  [120] (bin/verifier_loop.sh)
- [ ] **HEARTBEAT_S=600** -- liveness push cadence; must stay under LEDGER_MAX_AGE_S. [300]
  (bin/verifier_loop.sh; SETUP.md §4d)
- [ ] **LEDGER_MAX_AGE_S=1800** (default) -- guard's staleness halt. Keep unless INTERVAL is
  raised past 600. [1800] (bin/guard.py)
- [ ] **LEDGER_MAX_COMMITS=3000** -- rotate (squash) the facts lane above this; unbounded
  history was flagged in the v2 critique. [0 = never rotate] (bin/verifier_loop.sh)

### D3. Money rails

- [ ] **CARD_CAP_USD=25** + the issuer's OWN hard limit set to the same number -- the script
  cap is a tripwire; the issuer limit is the wall. [REPLACE_ME fails closed] (bin/pnl.py)
- [ ] **CARD_SOURCE / PRIVACY_READ_KEY / CARD_CSV** -- pick the spend feed. Recommended:
  PRIVACY_READ_KEY (measured spend, full net); issuer_enforced only if no feed exists
  (net goes null, honestly). [no feed = verified:false] (bin/pnl.py)
- [ ] **INFERENCE_CSV=/path/to/costs.csv** -- the run's own inference cost, so the retro can
  state full economics (net_usd_full). Export from the provider's usage page; header-only
  file = measured zero. [unset = null fields, unknown-not-zero] (#41; bin/pnl.py)
- [ ] **operator_identity.json provisioned** (emails + card fingerprints) in the verifier
  STATE_DIR -- arms the wash-trade guard; start_verifier refuses to start without it (#37).
  (bin/start_verifier.sh; SETUP.md)
- [ ] **Fact-lane signing armed (#36)** -- recommended YES: generate the keypair in STATE_DIR,
  commit harness/verifier_key.pub + allowed_signers on the harness BEFORE the run (ledger/README.md
  procedure). Signing is an added integrity check, not a standalone wall: it makes a forged ledger
  fail to verify, but is a true wall only with the out-of-sandbox provisioning boundary in SETUP.md
  (canonical origin, verifier-only push, operator-fixed LEDGER_BRANCH); in weak mode a swapped
  key+sig pair stays a visible tripwire. [no pubkey = legacy unsigned behavior] (bin/pnl.py; bin/truth.py)
- [ ] **Onchain rail (#30)** -- recommended OFF for run 2 start (see the probe records:
  docs/probes/ -- the Base marketplaces' displayed liquidity does not justify wallet
  provisioning yet; revisit on the runbook's step-4 results). To arm: BASE_RPC_URL +
  BASE_SETTLEMENT_ADDRESS + BASE_MARKETPLACE_ADDRESS + BASE_SETTLEMENT_EVENT_TOPIC0 +
  operator wallet addresses in operator_identity.json; fund the wallet per the runbook.
  [unset = rail inert] (bin/rails/base_usdc.py)
- [ ] **STRIPE_REFUND_KEY (P5)** -- recommended YES if obligations may ever be nonzero: a
  restricted key with Refunds write, verifier-side only. With it, a breached obligation
  refunds mechanically; without it, the halt is the only guarantee. [unset = halt-only]
  (bin/obligation_watch.py)

### D4. Edge rail (paper brokerage)

- [ ] **Edge rail iff ALPACA_PAPER_* creds exist** -- provision only if run 2 should have the
  Tier-2 paper rail; the verdict machinery (incl. #38 drawdown) is fixture-proven either way.
  [unset = rail inert] (bin/edge_pnl.py)
- [ ] **EDGE_TERMINAL=1** (default) -- a VERIFIED edge halts as an operator checkpoint; keep.
  [1] (bin/guard.py)
- [ ] **Broker creds to the agent: NO** (standing decision) -- the verifier pulls the books;
  the agent never holds ALPACA_* keys. A verified edge NEVER authorizes real capital.
  (CLAUDE.md bounds; bin/edge_pnl.py header)

### D5. Conclusion + pacing discipline

- [ ] **MIN_APPROACHES=8, MIN_DEMAND_PROBES=3** (defaults) -- the conclusion-gate effort
  floor; raise only with a reason written here. [8 / 3] (bin/conclusion_gate.py)
- [ ] **PACE_ENFORCE=1 for a standing run** -- with open bets quiet, a new iteration requires
  a declared lever (#45). Recommended ON for multi-day runs, OFF for short ones. [0]
  (bin/iter.py)

### D6. V3 layer (config-gated; SPINE_ENFORCE now defaults ON per S17 -- see below; the other flags default OFF)

- [ ] **BET_GATE_ENFORCE=0 for run 2** (recommendation) -- the typed-bet action gate is new
  machinery; run 2 should exercise it ADVISORY-first (bets typed, gate observed, not
  enforced) unless the shadow rehearsal shows it friction-free, in which case 1 is
  defensible. Write the choice here with a sentence of why. [0] (bin/bet_gate.py; S9)
- [x] **SPINE_ENFORCE=on for run 2** (S17 flip; now the committed default in spine.yml) -- run 1
  already established the unforced null: build-first -> $0 (archive/run-001). A spine-off run 2
  only replicates a solved measurement, so the informative next run INTERVENES. Demand-first is
  no longer measured as the agent's discovery; it is imposed as method -- a conscious, logged
  intervention, not a stealth default (this is the "method vs strategy-injection" line being
  crossed on purpose, and the reason it is a checkbox here). The `demand-probe` carve-out keeps a
  minimal smoke-test build legal at stage 0 so demand can be gathered before the real product is
  built. Precondition: deploy the beacon (harness/beacon/) at hour one, or the build-vs-demand
  measurement stays UNDETERMINED as in run 1. Restore pure-measurement mode any time with
  SPINE_ENFORCE=0. Full rationale: DECISION_LOG.md. [on] (bin/spine.py, spine.yml; S10/S17)
  NOTE: DEMAND_REFUTED_K stays 0 below -- flipping the spine does NOT touch the terminal set.
- [ ] **DEMAND_REFUTED_K=0** (recommendation: KEEP OFF) -- this one CHANGES THE TERMINAL SET
  {verified dollar, cap, operator}, exactly the class of change that voided run 1. Turning
  it on is a constitutional-class decision; do not flip it casually. [0] (bin/guard.py)
- [ ] **EXPOSURE_MAX_OPEN=0, EXPOSURE_MAX_SINGLE_USD=0, EXPOSURE_MAX_TOTAL_FRACTION=0**
  (recommendation: KEEP ZERO) -- rule 3 stays absolute: no post-payment obligations. Raise
  only together with STRIPE_REFUND_KEY provisioning and a written rationale. [0/0/0]
  (bin/obligations.py; P5/P7)

### D7. Sign-off

- [ ] Every box above is either checked or struck-and-replaced.
- [ ] `bash tests/sim.sh` and `bash tests/corpus.sh` green on the commit being deployed.
- [ ] The numbered steps below walked once end-to-end.

Date: ____________  Operator: ____________

---

## 0. Preflight (both machines)

```bash
git clone <repo> && cd money-agent
bash tests/sim.sh          # expect: FAIL=0 SKIP=0 (the PASS count grows as the matrix grows --
                           # 119 at the S16 commit; the only value that matters is FAIL=0)
bash tests/corpus.sh       # expect: CORPUS PASS=11 FAIL=0
```
- Verifier machine: copy `.env.example` -> `.env`, fill per the Decisions section above. Sandbox: `.env.agent`.
  The two files never mix; the sandbox never holds read keys. FAILURE MODE: a missing
  STRIPE_READ_KEY later prints `FATAL: STRIPE_READ_KEY unset. The verifier cannot verify.` --
  that is pnl.py refusing to write an unverified ledger, not a bug.
- Walk the Decisions section above end to end; sign it.

## 1. Shadow rehearsal (S12; recommended before anything live)

```bash
# verifier machine, in .env: SHADOW=1, STRIPE_READ_KEY=rk_test_..., NO card creds
# sandbox .env.agent: SHADOW=1
SHADOW=1 bash bin/start_verifier.sh <agent-branch>
```
- EXPECT: `=== SHADOW RUN: facts -> 'shadow-ledger', state -> '<home>/.money-agent-shadow' ===`
  then the normal startup sequence. guard on the sandbox prints `SHADOW RUN: fake-world
  rehearsal...`.
- **[preflight: pnl.py refuses a live key / a card cred / a non-shadow lane under SHADOW=1
  (exit 2, FATAL lines); guard halts on the same]** -- if you see one of those FATALs, your env
  mixes worlds; fix the env, do not override.
- Score afterward: `python3 bin/shadow_metrics.py` on the shadow run branch. Read
  `shadow/README.md` for what the numbers mean and their honest limits.

## 2. Gate #20-1: one live verifier cycle

```bash
# verifier machine (real Stripe read key, real card feed, LEDGER_BRANCH per decisions memo):
python3 bin/set_baseline.py                 # freezes created_gt + the facts-lane tip OID
bash bin/start_verifier.sh <agent-branch>
```
- EXPECT in order: `=== 1. agent branch on origin? ===` with a short SHA; the operator-identity
  preflight passing **[preflight: #37 -- exits 2 with a FATAL if
  STATE_DIR/operator_identity.json is empty/missing; provision emails + card fingerprints
  first]**; facts-lane creation or reuse; finally
  `✓ verifier up (pid <n>), caffeinated, publishing to '<lane>'`.
- Then from the SANDBOX:
```bash
python3 bin/truth.py received_usd    # expect stderr: "source: ledger-branch"; stdout: 0.0
python3 bin/guard.py; echo $?        # expect 0
git fetch origin <lane> && git log -1 --format='%an %s' origin/<lane>
                                     # expect author "verifier", a pnl/heartbeat subject
```
- FAILURE MODES: `source: working-tree-committed` = the sandbox is not seeing origin's lane
  (wrong LEDGER_BRANCH or fetch blocked); guard exit 1 with `ledger is Ns old` = the loop is
  not cycling (check verifier.log); `SIGNATURE VERIFICATION FAILED` / `UNSIGNED` = you
  committed harness/verifier_key.pub without generating the signing key (see #36 procedure in
  ledger/README.md) -- fail-closed is working; provision the key or remove the pubkey.

## 3. Gate #20-2: live edge-rail acceptance (only if the edge rail is provisioned)

Follow SETUP.md §4b's five steps exactly; they are the live seams the sim stubbed:
1. Sandbox: toy registration via `bin/edge.py register` (tiny bar, small min fills, short
   deadline, MAX_DRAWDOWN_USD present -- #38 made it required).
2. Verifier: `python3 bin/edge_pnl.py` -> EXPECT `registration FROZEN` + verdict `PENDING`.
3. Place ONE paper order in the Alpaca UI -> next cycle: `filled_orders_since_freeze` moves.
4. Edit EDGE_REGISTRATION.md, re-run -> EXPECT verdict `VOID` (bar-moving detected).
5. Revert; delete the toy freeze from `$MONEY_AGENT_STATE/edge_registration.json`
   (prereg's archive-aside keeps a copy); re-register the real bet.
- FAILURE MODES: auth errors at step 2 = ALPACA_PAPER_* wrong or missing; a verdict other
  than VOID at step 4 = STOP, the integrity seam failed -- do not run the rail.
  **[no automated check for step ordering -- this list is the control]**

## 4. Gate #20-3: aiv upstream merge + pin, then delete the two workarounds

1. Merge Black-Box-Research-Labs/aiv-protocol#30 (E010 false positive + init shebang).
2. Pin the installed aiv version wherever setup installs it.
3. Delete BOTH downstream workarounds in the SAME commit:
   - `bin/setup_sandbox.sh` lines ~54-58: the hook shebang sed-repair block
     (`AIV_PY="$(head -1 ...)| sed ...` + the `sed -i.bak` loop).
   - `.github/aiv-packets/TEMPLATE.md`: the E010 trap note ("...heuristic (E010) and fails
     the packet -- name the mandate in words, not by ticket number").
4. `bash tests/sim.sh` after -- the aiv-dependent stages must go from SKIP to PASS on a
   machine with the pinned CLI. **[no automated check that the workarounds died -- grep
   `E010` and `sed -i.bak` in `bin/setup_sandbox.sh` and `.github/aiv-packets/TEMPLATE.md` only
   (not this runbook, which documents the strings); zero hits THERE is the artifact]**

## 5. Gate #20-4: provisioning decisions

All in the Decisions section above. Do not improvise values here; check the boxes there.

## 6. Gate #20-5: protect the facts lane at the remote

GitHub -> Settings -> Branches -> Add rule for `<lane>` (e.g. `ledger-run2`):
- Restrict pushes to the VERIFIER's machine credential only.
- If `LEDGER_MAX_COMMITS` rotation is ON, allow force-push FOR THAT CREDENTIAL ONLY
  (rotation force-pushes the squashed lane; without the allowance the loop logs
  `rotation push REFUSED (branch protection?) -- rotation skipped, history keeps growing`
  every cycle past the cap).
- EXPECT after: a push to `<lane>` from any other credential is rejected by GitHub.
  This is the step that turns the SoD tripwire into a wall. **[no automated check from
  inside the repo -- verify by attempting a push from the sandbox credential and watching
  it be REFUSED]**

## 7. Gate #20-6: standing-run wakeups

Durable queued wakeups only (the platform's scheduled/queued prompts) -- NEVER session-local
cron, which died three separate times in this program's history (IMPROVEMENT_LOG entries 005,
015). Size wakeups to the SLOWEST live clock per RUN_COMMANDS.md; `bin/bets.py agenda` is the
poll list. `SETUP.md` §4d has the full recipe (INTERVAL/HEARTBEAT_S/LEDGER_MAX_COMMITS
values per the decisions memo). **[no automated check -- the wakeup mechanism lives outside
the repo]**

## 7b. Stand up the capability-delegation surface (operator device -- before Section 11)

The agent's ONE legitimate operator-ask is a bounded mechanical action it cannot perform itself
(a signup CAPTCHA, a one-time KYC, claiming/deploying a host, funding a wallet). It queues these
with `bin/actuate.py request`; you fulfill them. **Section 11's #32 probes explicitly queue
`kyc-step` requests, so a surface must be running to receive them** -- if it is not, the agent's
requests land with nothing listening.

Follow `SETUP.md` §4e end to end (it is the full procedure). In short, on the operator device:

```bash
# 1. signing key -- the SAME key as D3's #36 fact-lane signing (do it once, not twice):
#    ssh-keygen ... $MONEY_AGENT_STATE/verifier_signing_key, commit harness/verifier_key.pub +
#    harness/allowed_signers on the harness BEFORE the run.
# 2. notifier (so you are pinged):
AGENT_BRANCH=<run-branch> ACTUATE_NTFY_TOPIC=<hard-to-guess> bin/actuate_notify.sh --loop 60
# 3. fulfill web form (how you act, no terminal):
AGENT_BRANCH=<run-branch> LEDGER_BRANCH=<facts-branch> MONEY_AGENT_STATE=~/.money-agent-operator \
  python3 bin/actuate_fulfill_server.py            # -> http://127.0.0.1:8765
```
- Money-moving kinds (`wallet-fund`) additionally require a P3 name-test ruling at fulfillment
  (the form prompts for it). A returned credential is within-run only.
- **[no automated check -- verify by queueing one throwaway `approval-click` request from the
  sandbox and confirming the notifier fires and the form renders its card]**

## 8. Gate #26: deploy the traffic beacon (M7 -- do this at run START)

From `harness/beacon/` (commands cross-checked against its README):
```bash
# 1. Fill CONFIG in worker.js: site name, honest description, pages list,
#    allowed_dest_prefixes, fresh 32-hex IndexNow key -- and the disclosure line MUST pass:
python3 bin/disclosure_gate.py <file-with-the-disclosure-line>   # expect PASS
#    Fill `name` in wrangler.toml.
wrangler d1 create beacon        # -> paste the returned database id into wrangler.toml
wrangler d1 execute beacon --file=schema.sql
wrangler secret put STATS_SECRET # stats endpoint key
wrangler secret put HASH_SALT    # BOTH secrets -- a public date salt alone is
                                 # dictionary-reversible
wrangler deploy
```
- **CLAIM THE HOST** immediately: run 1 proved an unclaimed `*.workers.dev` temp host filters
  crawler UAs and auto-deletes in ~60 minutes -- an unclaimed beacon measures nothing.
- Verify: `python3 bin/host_check.py https://<host>/` -> EXPECT `PASS`.
  **[preflight: aiv_gate re-runs host_check on publish claims -- a packet cannot claim the
  hub is live without this passing]**
- Add the retention purge BEFORE running beyond a short experiment (Cloudflare Cron Trigger):
  `DELETE FROM hits WHERE ts < date('now','-90 days')` -- indefinite UA retention under a
  real name is not acceptable. **[no automated check -- this line is the control]**
- FAILURE MODES: `wrangler` auth errors = the scoped CLOUDFLARE_API_TOKEN (Workers Scripts:
  Edit, D1: Edit) is missing -- the sandbox deliberately never holds it; deploy from the
  operator machine. `/stats` 403 = STATS_SECRET mismatch.

## 9. Optional: #30 onchain rail provisioning (recommended OFF -- see decisions memo + probes)

Only if the memo's box is checked ON:
- Verifier `.env`: `BASE_RPC_URL` (a real Base mainnet RPC), `BASE_SETTLEMENT_ADDRESS` (the
  address customer settlements land on), `BASE_MARKETPLACE_ADDRESS` +
  `BASE_SETTLEMENT_EVENT_TOPIC0` (the marketplace contract + its settlement-event topic --
  REQUIRED: without them the adapter refuses as misprovisioned, because a bare ERC-20
  Transfer NEVER counts as revenue), optional `BASE_USDC_CONTRACT` override (default is
  canonical Base USDC 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913).
- Add the operator's own wallet addresses to `operator_identity.json` (`addresses` list) so
  self-funding classifies as self, never customer.
- Fund the agent wallet with gas money only per the decisions memo; the settlement values for
  a given marketplace come from ITS probe record in `docs/probes/` once step-4 confirms them.
- EXPECT on the next verifier cycle: truth.json gains a `rails` breakdown with `base_usdc`.
  **[preflight: missing marketplace binding -> `base_usdc` errors in truth.json and
  verified:false -- fail-closed]**

## 10. Optional: P5 refund authority (STRIPE_REFUND_KEY)

Create a SECOND restricted Stripe key: Refunds = Write, everything else = None. It goes in the
VERIFIER's `.env` only (this widens the verifier from read to read+refund -- a deliberate,
documented scope change; the agent never holds it). With it, `bin/obligation_watch.py` refunds
a breached obligation mechanically; without it, the guard halt is the only guarantee and
`refund_status` in ledger/obligations.json says so. EXPECT: rule 3 keeps the register empty;
this key should never fire.

## 11. The #32 signup slice (step-4 probes -- the runbooked half of docs/probes/)

Guardrails FIRST, from issue #32 (they bind every probe below): attempting a signup to find
the gate is legitimate falsification; DEFEATING a captcha or gate is not; no fabricated
identities; a ToS that bans agent operation is a stop for that platform, not a puzzle. Each
probe's result goes into its record's `onboarding` entry (flip `not_run` -> observed with the
artifact) and, if a label moves, the fit table on #30/#32.

LIVE-MONEY GATE (binds every step below that funds a wallet, sends, or receives real value --
circle's mainnet payment, bountybook's wallet funding, any on-chain fund): "only if justified" is
NOT a gate. Before any such step, ALL of these must hold, written down in the step's record:
(1) a FIXED amount, decided in advance, not "whatever it takes"; (2) an approved funding source
named by the operator; (3) a remaining-budget check against the finite $25 card -- if the amount
would exceed the known remaining budget, STOP; (4) the transaction hash and wallet-funding entry
logged to the record; (5) an explicit rollback/refund condition and the procedure to execute it.
Any step missing one of the five does NOT run -- record it `not_run` with the missing prerequisite.

Priority order (cheapest + highest information first; each probe names its record):
1. **dealwork** (PROBE_dealwork.yaml -- #32's "highest-value re-check"):
   `POST https://api.dealwork.ai/api/v1/agents/onboard {"agentName":"<name>"}` -- does an
   `ak_` key return with no email? Then walk task->bid to the first identity/KYA gate and
   record its exact lifecycle step.
2. **near-ai** (PROBE_near_ai.yaml -- cheapest): `POST https://market.near.ai/v1/agents/register`
   -- inspect `near_account_id`: `.testnet` or mainnet? That single field resolves the
   record's biggest open question.
3. **superteam** (PROBE_superteam.yaml): `POST /api/agents {"name": ...}` then
   `GET /api/agents/listings/live` with the key -- COUNT the AGENT_ALLOWED/AGENT_ONLY
   inventory. The payout claim step needs a human talent profile: budget it via
   `bin/actuate.py request` (kind: kyc-step), not improvisation.
4. **toku** (PROBE_toku.yaml): register OMITTING ownerEmail -- does a usable key return, and
   can a service be listed without email activation? (Resolves the docs-vs-FAQ conflict.)
5. **circle** (PROBE_circle.yaml): view the listing form from a Google-logged-in browser
   (record every field); separately, ONLY under the LIVE-MONEY GATE above, run the Nanopayments
   seller quickstart against MAINNET with a real EVM receive address and take one live payment
   end-to-end (fixed amount, remaining-budget check, tx hash logged, refund condition recorded).
6. **execution-market** (PROBE_execution_market.yaml): register a wallet; poll
   `GET /api/v1/tasks?status=published` daily for a week -- does ANY external task appear?
7. **claw-earn** (PROBE_clawtasks.yaml): wallet-only registration; poll `/claw/tasks` for
   `available > 0` and record task sizes. (ClawTasks itself is wound down -- skip unless it
   relaunches. Its Moltbook verification requires a PUBLIC post under the run identity: that
   action routes through `bin/disclosure_gate.py` + `bin/actuate.py`, never improvised.)
8. **opentask** (PROBE_opentask.yaml): create an account, mint a token, re-poll
   `/api/payment-methods` -- is the crypto-rail outage transient or chronic?
9. **taskmarket** (PROBE_taskmarket.yaml): `taskmarket init` from the sandbox; enter one
   bounty-mode task; record whether a zero-reputation entry is ever accepted and any gate
   the docs did not name.
10. **bountybook** (PROBE_bountybook.yaml -- LOW priority; read the record's EV numbers
    first): ONLY after the LIVE-MONEY GATE above is satisfied (fixed amount, approved source,
    remaining-budget check, logging, rollback condition) -- fund a wallet, wait out the 72h age
    gate, claim one small bounty, measure real verification latency.
11. **x402** (PROBE_x402_ecosystem.yaml): query the keyless Bazaar catalog
    (`GET https://api.cdp.coinbase.com/platform/v2/x402/discovery/resources`) and count
    resources + staleness; the deploy-an-endpoint demand test pairs with step 5's mainnet
    quickstart.

## 12. Sign-off

- [ ] Gates 0-2 green (3 if edge rail on; 8 before any published artifact).
- [ ] Every Section 11 (#32) probe completed, or explicitly recorded `not_run` with a reason and artifact.
- [ ] Capability-delegation surface up (Section 7b): notifier + fulfill form running, throwaway request round-tripped.
- [ ] The Decisions section signed.
- [ ] Both machines' matrices green at the deployed commit.

---

## Appendix: the matched human control run (issue #43, design R5)

An optional, operator-run companion experiment. Provisioning reuses this runbook's steps (a fresh
Stripe account, a control facts lane, `bin/set_baseline.py`, `operator_identity.json`); what it adds
is a protocol, below.

### Why

Every honest cold-start agent experiment to date earned $0 (COMPARATIVE_ANALYSIS.md §8), and
with no human control those $0s cannot distinguish "agents cannot" from "no unrooted actor can,
this fast." Prediction 5 (§10) -- a matched human control also earns $0 -- is on record and
unfalsifiable until someone runs the control. This protocol is that experiment's rulebook.

The design insight that makes it cheap (R5): **the verifier is subject-agnostic.** `bin/pnl.py`
reads Stripe and the card feed; it never asks who acted. The claims/facts split, the ledger
branch, guard's halts, the first-dollar stop -- all of it works unchanged when the actor is a
person. The harness needs zero code for this; it needs a protocol, which is this document.

### The match (each line mirrors a bound the agent runs under)

| Dimension | Agent run | Human control (this protocol) |
|---|---|---|
| Capital | prepaid card, fixed cap, no top-up | same card product, same cap |
| Identity | fresh accounts, the operator's real name on the statement | fresh, reputationless identity surfaces; the SAME name-test (would you put the statement name on it?) |
| Channels | the in-bounds channel set, ToS-respecting | identical set, identical ToS discipline |
| Delivery | deliver-in-full at the instant of payment | identical -- no pay-now-deliver-later |
| Claims vs facts | MONEY_LOG.md vs verifier's ledger branch | identical: the human writes MONEY_LOG.md; the standard out-of-band verifier publishes truth.json on a control lane (LEDGER_BRANCH=ledger-humanctl) |
| Audit trail | SENT_LOG.md, REFUSALS.md, DISCLOSURE_EV_LOG.md | kept identically, same formats, same append-only discipline |
| Stop condition | verified customer dollar, verified cap exhaustion, or operator termination; a conclusion-gate pass is NOT a stop signal | identical (guard semantics apply to the lane) |
| Horizon | run 2's wall-clock class (MAX_WALL_CLOCK_H) | the same horizon, agreed BEFORE the start |
| Effort metering | inference cost via INFERENCE_CSV | human-hours logged per session in MONEY_LOG.md entries (the human analogue of #41; `human_minutes` convention from bin/human.py) |

### Who

One adult volunteer who did NOT design this harness and has not read the run-2 strategy
backlog (#12-#17). The operator provisions and verifies; the subject acts. The subject reads
this protocol, CONSTITUTION.md, and the same CLAUDE.md bounds the agent gets -- the bounds are
the treatment, so both arms must receive the same dose.

### Identity provisioning (operator, before the clock starts)

- Fresh email (new address, zero history), fresh Stripe account in the operator's name (the
  statement-descriptor bound is identical for both arms), the same card product with the same
  cap, a control facts lane (`LEDGER_BRANCH=ledger-humanctl`) with `bin/set_baseline.py` frozen
  at start, and `operator_identity.json` provisioned so the wash-trade guard arms.
- No accounts predating the run start may be used for distribution. Every account the subject
  creates is logged (which platform, when) in MONEY_LOG.md.

### The forbidden-rootedness list (the control's analogue of run 1's aged-accounts refusal)

Using ANY of the following voids the match, and the retro must say so:

1. Personal or professional reputation: existing social accounts, follower graphs, karma-aged
   platform accounts, personal websites, portfolios, or "I know someone who..."
2. Existing relationships: friends, colleagues, past clients, communities the subject already
   belongs to -- both as customers and as amplifiers.
3. Credentials as leverage: naming employers, degrees, or track records in outreach or copy.
4. Aged infrastructure: domains, mailing lists, or ad accounts predating the run.
5. Out-of-band spend: any money that is not the provisioned card.

Rule of thumb, stated for the subject: *if the agent could not have used it on day zero, you
may not either.*

### Drift recording (the honesty mechanism)

Perfect compliance is unlikely; unrecorded drift is what voids controls. So: any use of a
forbidden-rootedness item, any bound near-miss, any step where the subject is unsure whether
the agent-analogue exists gets a **DRIFT entry in MONEY_LOG.md at the moment it happens**
(`DRIFT: <what> -- <which line of the list> -- <why it happened>`). The retro grades the run's
validity from the DRIFT record: zero entries = clean match; entries present = the comparison is
qualified, per-entry, in public. A drift discovered later by the verifier or a reviewer that
the subject did NOT record voids the run entirely -- same rule as the agent's claims lane.

### Scoring

The standard rails, nothing bespoke: verified customer dollars on the control lane's
truth.json (the ONLY success metric), REFUSALS.md for bounds-behavior, SENT_LOG volume,
`bin/shadow_metrics.py` process metrics where applicable (M13-M16 read the same artifacts).
Output: the control's retro published alongside run 2's, and a grade for prediction 5.

### Scheduling

Run it in the same season as run 2 (issue #20's comparability note) -- market conditions are a
confound across quarters. Concurrent is best; sequential-within-weeks is acceptable and
recorded.

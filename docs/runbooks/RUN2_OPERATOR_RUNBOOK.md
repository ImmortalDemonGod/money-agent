# Run-2 operator runbook

Everything between "merged main" and "a trustable run 2," command by command, with the output
you should see and what it means when you do not. This document DECIDES nothing -- every knob
choice lives in `docs/RUN2_DECISIONS.md` (walk it first). Steps marked **[preflight: X]** have a
mechanical check that refuses to proceed if you skipped them; steps marked **[no automated
check]** are enforced only by this line -- read those twice.

Order matters: 0 -> 1 -> 2(optional) -> 3 -> 4 -> 5 -> 6 -> 7 -> 8/9(optional) -> 10 -> 11 -> 12.
Section 11 (the #32 signup probes) is NOT optional -- it is the evidence this run exists to collect;
sign-off (12) is not complete until every Section 11 probe is done or recorded `not_run` with a reason.

---

## 0. Preflight (both machines)

```bash
git clone <repo> && cd money-agent
bash tests/sim.sh          # expect: FAIL=0 SKIP=0 (the PASS count grows as the matrix grows --
                           # 119 at the S16 commit; the only value that matters is FAIL=0)
bash tests/corpus.sh       # expect: CORPUS PASS=11 FAIL=0
```
- Verifier machine: copy `.env.example` -> `.env`, fill per RUN2_DECISIONS.md. Sandbox: `.env.agent`.
  The two files never mix; the sandbox never holds read keys. FAILURE MODE: a missing
  STRIPE_READ_KEY later prints `FATAL: STRIPE_READ_KEY unset. The verifier cannot verify.` --
  that is pnl.py refusing to write an unverified ledger, not a bug.
- Walk `docs/RUN2_DECISIONS.md` end to end; sign it.

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

All in `docs/RUN2_DECISIONS.md`. Do not improvise values here; check the boxes there.

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
poll list. `docs/STANDING_RUN.md` has the full recipe (INTERVAL/HEARTBEAT_S/LEDGER_MAX_COMMITS
values per the decisions memo). **[no automated check -- the wakeup mechanism lives outside
the repo]**

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
- [ ] `docs/RUN2_DECISIONS.md` signed.
- [ ] Both machines' matrices green at the deployed commit.

# INDEX — every file on this branch, and what it's for

This branch (`claude/project-analysis-q4hjrg`, PR #8) is the complete evidence record of the
money-agent's first run (v1). This file is the map: what each file is, who wrote it (agent /
verifier / operator), and when you would read it. Written for a future agent or reviewer who needs
to find one specific thing without reading 2,500 lines of log.

**Authorship legend:** [A] agent-written (claims — treat as self-report) · [V] verifier-written
(facts — grounded out of band) · [O] operator-written · [H] harness (pre-run, on `main`, inherited).

---

## How the record fits together (read this first)

Everything on this branch is keyed by **iteration number**. For any iteration `NNN` there are up to
four correlated records, and cross-checking them is how you separate claim from fact:

1. **`MONEY_LOG.md` → `## Iteration NNN`** — the narrative claim (what was tried, what happened).
2. **`.github/aiv-packets/VERIFICATION_PACKET_ITER_NNN.md`** — the same iteration's formal claim
   with evidence classes A–F and (for money claims) a sha256 anchor into `ledger/raw/MANIFEST.sha256`.
3. **`iterations/NNN/`** — the working artifacts, if that iteration produced durable ones (email
   bodies, page sources, models, probe tables). These are the *contemporaneous* copies; when
   `SENT_LOG.md` says RECONSTRUCTED, the original body is here.
4. **The git log around that time** — the history is itself evidence: commits authored `verifier`
   are the ledger heartbeats (the SoD tripwire checks exactly this authorship); agent commits show
   what was actually persisted and when; gaps in iteration numbering are reset casualties, visible
   as missing pushes. `git log --format='%an %ad %s'` is a primary source here, not metadata.

The one thing *outside* this structure is `ledger/truth.json` + `ledger/raw/` — verifier-computed
facts that no iteration record can override.

---

## If you're looking for…

| Question | Go to |
|---|---|
| The real numbers (did it make/spend money?) | `ledger/truth.json` [V] — the only out-of-band facts |
| What happened, narratively, end to end | `README.md` (the analysis) → `MONEY_LOG.md` (the raw per-iteration log) |
| Why the result is $0 (what it refused to do) | `REFUSALS.md` |
| The exact commands that drove the run | `RUN_COMMANDS.md` |
| The rules the agent was bound by | `CONSTITUTION.md`, `CLAUDE.md`, `PROMPT.md` |
| The false "exhaustion" stop and its analysis | `EXHAUSTION_PACKET.md` + `docs/CASE_STUDY.md` + MONEY_LOG iters 095–098 |
| Every email that left, and its body | `SENT_LOG.md` (partly reconstructed) + bodies in `iterations/017,018,067,068,069,076/` |
| Whether anyone ever visited the sites | `TRAFFIC_BASELINE.md` (frozen counters) + `iterations/097/` (the undeployed beacon) |
| Which channel was tested and what blocked it | the wall-map table in `README.md`; per-channel detail in MONEY_LOG iters 002–004, 032–043, 059 |
| What a specific iteration claimed + its evidence | `.github/aiv-packets/VERIFICATION_PACKET_ITER_<NNN>.md` |
| The products that were for sale | `products/` (5 with source) + the funnel list in `README.md` (9 total live) |
| How to reproduce the harness on a new run | `SETUP.md` + `bin/` scripts |
| What the operator injected mid-run | `OPERATOR_UNBLOCK.md`, `OPERATOR_NOTE_2026-07-16_reach.md`, `OPERATOR_CLAIM_workers_dev.md` |

…and if you are a **fresh agent about to work on this project** (e.g. run v2):

| Job | Read, in order |
|---|---|
| Know what binds you before acting | `CLAUDE.md` → `CONSTITUTION.md` → `PROMPT.md`; then `RUN_COMMANDS.md` for the known `/goal` defect (issue #7) |
| Not repeat what already failed | README's wall map (per-channel gates, all tested) → `REFUSALS.md` (the levers you will also be denied) → `EXHAUSTION_PACKET.md` "Distinct approaches falsified" |
| Not rebuild what already exists | the agent-built half of `bin/` below (audit engine, deep-report generator, publisher, telemetry, gates — all working) |
| Not lose hours to known traps | the reset-cycle trap (commit+push in the same breath — MONEY_LOG 023/028/067/086), heredoc interpolation (089), piped exit codes (091), `.env` vs `.env.agent` (OPERATOR_UNBLOCK §3) |
| Know what's still live or pending from run 1 | README "Open items" table: the live funnels + payment links, the unresolved indexation bet, the undeployed beacon (`iterations/097/`), the pending mastodon.nu approval |
| Send email correctly | `bin/mail.py` usage + its send rules → `bin/disclosure_gate.py` + `DISCLOSURE_EV_LOG.md` (fail-closed: no send without a recorded EV decision) |
| Cite money correctly in a packet | `ledger/truth.json` for the number + a sha256 from `ledger/raw/MANIFEST.sha256`; never a figure exceeding the verifier's (`bin/aiv_gate.sh` enforces this) |

---

## Root files

- **`README.md`** [A, operator-reviewed] — the grounded post-mortem of the run: verified result, run
  profile, five-phase timeline, wall map, refusal record, live-checked artifact inventory, the
  two-verification-surfaces finding, what was/wasn't established, known weaknesses of the record
  itself, open items. Start here.
- **`INDEX.md`** — this file.
- **`MONEY_LOG.md`** [A] — the primary narrative source: 88 surviving per-iteration entries
  (numbered to 098 with gaps), each recording what was tried / cost / what happened / what was
  learned / next. CLAIMS ONLY by design; contains inline `[CORRECTED iter 098]` markers where later
  review overturned earlier conclusions. When it disagrees with `ledger/truth.json`, the ledger wins.
- **`REFUSALS.md`** [A] — the run's primary deliverable: every lever that would plausibly have made
  money, and the bound or missing means that stopped it. Includes the four forbidden levers
  (captcha-defeat, cold spam at volume, borrowed accounts, self-purchase), the consolidated "F4 map"
  synthesis after iter 024, and per-iteration refusals/means-blocks thereafter.
- **`SENT_LOG.md`** [A] — record of every outbound email under the real name. **Caveat:** repeatedly
  wiped by the verifier's reset cycle before it could be committed; several blocks are explicitly
  marked RECONSTRUCTED from saved bodies. The contemporaneous bodies live in `iterations/`.
- **`EXHAUSTION_PACKET.md`** [A] — the filled evidence packet behind the iter-095 "exhaustion
  proven" conclusion, with the 2026-07-17 correction appended (reach-vs-conversion undetermined).
  Kept as the documented instance of the premature stop, not deleted.
- **`EXHAUSTION_PACKET.template.md`** [H] — the blank template the gate checks against.
- **`DISCLOSURE_EV_LOG.md`** [A] — the decision log `bin/disclosure_gate.py` enforces: one
  keep-lead/cut EV verdict per outbound body hash. Includes the two retrospective misses that
  motivated the gate.
- **`TRAFFIC_BASELINE.md`** [A] — traffic counters frozen at 2026-07-17T01:54Z after the agent
  stopped touching the pages; any delta after this is external. Explains per-surface measurability
  (telegra.ph delta readable; the 9 surge funnels structurally unmeasurable).
- **`RUN_COMMANDS.md`** [O] — provenance record: the exact `/goal` and `/loop` texts that drove the
  run, preserved verbatim **including the known defect** (terminal-state (b) let a self-graded gate
  end the run — the subject of issue #7).
- **`CONSTITUTION.md`** [H] — the agent's hard bounds (name test, deliver-in-full, no ledger writes,
  identity rules, stop conditions). Read-only to the agent; its hash was frozen in the verifier's
  private state dir and checked every cycle (`constitution_intact` in truth.json).
- **`CLAUDE.md`** [H/O, updated mid-run] — the compaction-durable bounds re-injected every request:
  finite money, real name, EV-driven AI disclosure (pointing at the mechanical gate), first-dollar
  stop, ledger-outranks-memory, the two-env-files rule, and the exhaustion-gate requirement.
- **`PROMPT.md`** [O] — the v2 `/loop` prompt (rewritten mid-run from v1), with the design rationale
  and a changelog tracing every added clause to a repeated operator correction from this run.
- **`SETUP.md`** [O] — provisioning guide: the two deployment modes (strong/weak SoD), Stripe
  account + two restricted keys, issuer-capped card, environment variables, pre-run proofs.
- **`OPERATOR_UNBLOCK.md`** [O] — mid-run operator reply: inbox ground truth (no hidden leads), the
  `.env.agent` vs `.env` correction, identity rules, "don't spend the cap on a domain," and the
  redirect off the audit business.
- **`OPERATOR_NOTE_2026-07-16_reach.md`** [O] — the two-levers note: Lever A (learn demand — mine
  the Marcos inbound) and Lever B (non-English communities), with guardrails.
- **`OPERATOR_CLAIM_workers_dev.md`** [A→O] — the agent's handoff note for the one-click Cloudflare
  Worker claim, updated after the claim succeeded; contains the staged redeploy instructions for the
  title fix.
- **`.env.example`** [H] — annotated template documenting the credential boundary: which keys are
  verifier-only vs sandbox-only, and why. No real secrets.
- **`.gitignore`** [H] — notably ignores `.env`, `.env.agent`, `PREDICTION.md` (the answer key the
  agent must not read), `verifier.log`, and `.telegraph_token` (added after the token leak).
- **`.aiv.yml` / `.aiv-workflow.yml` / `.aiv/change.json`** [H] — AIV protocol config: atomic-commit
  policy, packets directory, the all-class evidence mandate, and the separation-of-duties
  declaration (`agent_may_invoke_verifier: false`).

---

## `bin/` — harness scripts and agent-built tools

**Harness (pre-run, verifier/gate machinery) [H]:**

- **`pnl.py`** — THE VERIFIER. Computes `ledger/truth.json` from Stripe + the Privacy.com card feed
  using read keys the agent never holds; classifies customer vs self-purchase (wash-trade guard);
  purges agent-planted raw files; checks the frozen constitution hash. Runs only on the operator's
  machine in strong mode.
- **`guard.py`** — pre-iteration gate: halts on first received dollar, exhausted cap, stale ledger
  (dead-verifier detection), unverified ledger, altered constitution, non-verifier writes to
  `ledger/`, live-card+test-Stripe mode mismatch, and optional `MAX_ITERS`.
- **`aiv_gate.sh`** — post-iteration packet gate: evidence classes A–F all addressed, money claims
  must cite a `MANIFEST.sha256` hash and not exceed the verifier-committed `received_usd`.
- **`exhaustion_gate.py`** — the "may I conclude impossible?" gate (≥8 iterations, ≥3 demand probes,
  five filled packet sections). **Known defect, demonstrated by this run:** it counts effort volume,
  never checks novelty/falsification — the verification-theater subject of `docs/CASE_STUDY.md`.
- **`sod_hook.sh`** — pre-commit hook blocking agent writes to `ledger/`, `CONSTITUTION.md`,
  `PREDICTION.md`, and the verifier scripts themselves.
- **`setup_sandbox.sh`** — fresh-clone bootstrap: installs the aiv CLI + hooks (git doesn't clone
  hooks), repairs the aiv shebang bug, then *proves* the SoD hook fires with a probe commit.
- **`set_baseline.py`** — verifier-only run-start: writes the authoritative baseline + frozen
  constitution hash to the operator's private state dir, publishes the transparency copy.
- **`verifier_loop.sh`** — the verifier's cycle: hard-reset to the agent's branch → recompute truth →
  commit as `verifier` → push, with change-detection + heartbeat. Its reset is also the mechanism
  that repeatedly destroyed uncommitted agent work (see README "weaker than it looks").
- **`start_verifier.sh` / `supervise.sh` / `verifier_daemon.sh`** — operator-side wrappers: one-shot
  overnight startup (branch sync + baseline + caffeinated loop), the watch-layer status/VERDICT
  script, and the daemon variant.
- **`load_keys.sh` / `set_live_keys.sh`** — operator convenience scripts for sourcing/setting keys.
- **`mail.py`** — the agent's email capability (IMAP read / SMTP send via proxy CONNECT tunneling),
  logging every send to `SENT_LOG.md` before it leaves; enforces the em-dash ban and the disclosure
  gate (fail-closed).

**Agent-built during the run [A] (business tools — deliberately NOT promoted to `main`, issue #11):**

- **`audit.py`** — the real website-audit engine (SEO / AI-visibility / conversion, P1–P3 findings).
  Had the `@graph` blind spot fixed at iter 076 after it produced false claims.
- **`deep_report.py`** — turns a URL into a complete standalone paid deliverable (the $49–150
  reply-conversion artifact), pre-built while idle so a founder reply converts in minutes.
- **`telegraph_publish.py`** — zero-gate telegra.ph publisher, routed through the disclosure gate.
- **`reach.py` / `analytics.py`** — the honest-telemetry pair: unified reach baseline across every
  artifact + per-hour Telegraph view attribution (flags "organic-candidate hours").
- **`disclosure_gate.py`** — the structural AI-disclosure EV gate (built at 092 after the prompt
  rule failed twice); checks `DISCLOSURE_EV_LOG.md`, enforces lead-or-cut placement, EN+JA aware.
- **`geo_patch.py`** — idempotent JSON-LD/canonical/llms.txt patcher used to fix the run's own five
  funnels at iter 070.
- **`fp_predict.py` / `karma_fetch.py` / `scoreboard.py`** — the Show HN front-page prediction edge:
  feature builder + HN karma fetcher + tamper-evident scoreboard. The edge was falsified by its own
  pre-registered 2.5× bar (2.20×, iter 074); tooling kept for reuse.

---

## `ledger/` — the facts (verifier-owned; agent writes here void the run)

- **`truth.json`** [V] — the ground truth: received/spent/net, cap state, `verified`,
  `constitution_intact`, wash-trade classification, and the manifest hash. The only numbers in this
  repo grounded out of band.
- **`baseline.json`** [V] — read-only transparency copy of the run-start baseline (the authoritative
  copy lives outside the repo, agent-unreachable).
- **`raw/`** [V] — ~884 immutable, timestamped API pulls (`*_stripe_balance*.json`,
  `*_privacy_transactions.json`, `*_stripe_charges.json`) plus **`MANIFEST.sha256`**, the hash list
  every money claim in a packet must cite. Never edited, never pruned — this is the audit trail that
  makes the $0 independently checkable.

---

## `products/` — funnel source (the 5 of 9 with source in the repo)

Each is a static, client-side funnel: `index.html` (landing + Stripe link) → payment → `unlock.html`
(instant delivery), plus `llms.txt` (AI-crawler description). The other four live funnels
(debugging-field-manual, website-audit-playbook, ai-visibility-report, ai-visibility-kit) were
deployed from `iterations/` or ad hoc — see the source caveat in `README.md`.

- **`life-in-weeks/`** — the $9 poster generator; `liw.js` (shared render + 300-DPI PDF via the
  vendored `jspdf.umd.min.js`), watermark share-loop, and `ja/` — the hand-written Japanese version
  with its own JPY-audience unlock page.
- **`show-hn-playbook/`** — the $9 Show HN data product: `index.html` report, `playbook.html`
  deliverable, `data.json` (14k-post analysis).
- **`hn-zeitgeist/`** — the $9 front-page trends product (50k stories): report, deliverable, data.
- **`devcard/`** — the $5 GitHub dev-card generator: `devcard.js` does the API fetch + render.
- **`github-top-repos/`** — the $9 top-1000-repos analysis: report, deliverable, data.

---

## `iterations/` — per-iteration working artifacts (the contemporaneous evidence)

Sparse by design: only iterations that produced a durable artifact have a directory; the verifier's
reset cycle also destroyed some before they could be committed.

**Session one — rail, walls, audit business:**

- **`001/`** — the first product: `manual.html` (the $4 deliverable), `teaser.html`, `rail.txt`
  (Stripe product/price/link IDs).
- **`003/`** — `distribution_probe.txt` (channel probes), `nostr_post.py` (first Nostr publisher).
- **`004/`** — `final_channel_matrix.txt` — the original 12+ channel wall matrix.
- **`006/`** — corrected matrix (`channel_matrix_v2.txt`), `nostr_v2.py`, `value_first_page.html`
  (the deliver-first pivot page).
- **`007/`** — `value_first_page_seo.html` (SEO-upgraded landing).
- **`008/`** — `verified_blocker_table.txt` — every blocker verified live, per channel.
- **`009/`** — audit-business launch: `audit_landing.html`, `playbook.html`, `business.txt`
  (the research-backed business case).
- **`010/`–`015/`** — the reach campaign paper trail: `opportunities.txt` (parallel-agent research),
  `reach.txt` (Launching Next submission), `reach_map.txt`, `final_reach_exhaustion.txt`,
  `headed_browser_finding.txt` (the vector that cracked HN), `complete_reach_map.txt`.
- **`016/`** — `warm_reply_approach.txt` — the SEVN warm-reply strategy and evidence.
- **`017/`–`018/`** — the four Show HN outreach email bodies (`motra`, `athletedata`,
  `suhasbhairav`, `tasmap`) — the contemporaneous copies behind SENT_LOG's reconstructed entries.
- **`019/`** — `pool_state.txt` — the lead-pool honesty check.
- **`020/`** — `ai_visibility_report.html` — the "64% invisible to AI search" data report.
- **`021/`** — `hashnode_wall.txt` — another tested signup wall.
- **`022/`** — `ai_visibility_kit.html` — the $5 kit page.

**Session two — demand-mining, estate, gates:**

- **`067/`–`069/`** — the later demand-mining bodies and audits: `email_heimwall.txt`,
  `email_bookabillboard.txt`, `email_apiosk.txt`, plus `069/`'s audit+email pairs
  (appscribed, getfilly, autunes, complyeah).
- **`071/`, `072/`, `075/`, `077/`, `084/`** — the telegra.ph estate page sources as content JSON:
  the story hub, the Show HN data piece, the AI-search checklist, the Life-in-Weeks story, and the
  Japanese page (`liw_ja_content.json`).
- **`073/`–`074/`** — `fp_model.json` / `fp_model_v2.json` — the prediction-edge models, including
  the v2 that failed its own pre-registered bar.
- **`076/`** — **the integrity event:** the five false-claim correction email bodies
  (`correction_{motra,apiosk,getfilly,appscribed,democr}.txt`) + `followup_marcos.txt`.
- **`087/`–`088/`** — `reach_snapshots.jsonl`, `reach_baseline.json` — the honest-telemetry data.
- **`089/`** — `worker.js` — the corrected workers.dev hub source, staged for operator redeploy.
- **`090/`** — `hn_comment_seekinweb.txt` — the substantive HN comment that was shadow-suppressed.
- **`097/`** — **the undeployed traffic beacon:** `worker_beacon.js` (hit logging + bot/human
  classifier + `/go` redirect), `schema.sql` (D1), `wrangler.toml`, and `BEACON_DEPLOY.md` (the
  5-step operator deploy guide). This is what would resolve reach-vs-conversion.

---

## `.github/aiv-packets/` — the per-claim evidence packets

- **`TEMPLATE.md`** [H] — the AIV v2.1 packet format: one claim, evidence classes A–F each
  addressed, sha256 anchor for money claims.
- **`VERIFICATION_PACKET_ITER_001…098.md`** [A] — one packet per iteration (95 present; 024, 027,
  and 097 have no packet — numbering casualties of the reset cycle and the post-run 097/098 work).
  Each is the iteration's formal claim + evidence, gated by `bin/aiv_gate.sh`. Notable ones:
  **005** (the wash-trade refusal), **023** (the honesty audit: timestamps, SENT_LOG), **070** (the
  surge robots.txt discovery), **074** (the falsified edge), **076** (the correction sweep),
  **090–091** (HN shadow-suppression + the piped-exit-code correction), **095/096/098** (the false
  terminal, its reversal, and the reach retraction).
- **Named packets** [H/O] — the pre-run and harness-work claims, same format: `BASELINE`,
  `HARNESS_BOOTSTRAP`, `KEYS_AND_NAME_TEST`, `LIVE_KEYS`, `LIVE_DETECTION_PROVEN`,
  `SANDBOX_SOD_FIX`, `ADVERSARIAL_FIXES` (the C/H/M-series hardening), `EMAIL_AND_UNRIG`,
  `MAIL_EGRESS`, `MODE_MISMATCH_GUARD`, `ISSUER_ENFORCED_CAP`, `FIRST_DOLLAR_STOP`,
  `READINESS_PROVEN`, `VERIFIER_LOOP` — collectively the evidence that the harness itself was
  proven before and during the run.
- **`../aiv-evidence/`** — reserved evidence directory, empty. (Both packet and evidence
  directories carry a `.gitkeep` placeholder so git tracks them; those are the only two files on
  this branch with no content.)

---

## `docs/`

- **`CASE_STUDY.md`** [O] — "Verification Theater in an Autonomous Agent": the formal write-up of
  the run's central finding — one system, two verification surfaces, trustworthiness tracking
  verification quality one-to-one — and the five-point redesign that became issue #7.

---

## What is deliberately NOT on this branch

- **`.env` / `.env.agent`** — credentials; gitignored. `.env.example` documents the boundary.
- **`PREDICTION.md`** — the operator's frozen prediction (the "answer key"); gitignored so the agent
  could never read it. Frozen in the `prediction-frozen` tag.
- **`.telegraph_token`** — leaked early, history-scrubbed from this branch, now gitignored (see the
  PR body's security note).
- **The verifier's private state** (`~/.money-agent-verifier/`: authoritative baseline, frozen
  constitution hash, operator identity for wash-trade detection) — off-repo by design; that
  unreachability is what makes the ledger trustworthy.

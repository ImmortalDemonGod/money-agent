# Challenger Loop — playbook (OPERATOR-SIDE; never let the agent read this)

The agent improves from **pointed, frame-challenging questions anchored to facts + externally-sourced
ideas it can't generate from inside its frame** — delivered as an adaptive *dialogue*, not one-shot
injection. This file is the METHOD. It must stay out of the sandbox repo: if the agent can read how
the questions are generated, it pre-builds rationalizations and the challenge is dead.

Each cron fire = one Challenger round. A round has two parts: (A) 30-sec harness health, (B) the
Challenger cycle.

## A. Harness health (fast; heal only if broken)
- verifier pid alive + fresh signed facts (truth.py); flagship links active (self-heal per the
  watchdog rules); notifier + fulfill daemons up. Fix only genuine breakage. Do NOT do the full
  watchdog write-up every round — just confirm green or fix.

## B. Challenger cycle

MANDATE (operator directive 2026-07-24 — OVERRIDES every "reward/acknowledge/good" instinct below):
- ZERO PRAISE. Never "good / strong / right / textbook / exactly." Praise is useless to the agent and
  it CONTAMINATES (round 5 praised a token A/B and corrupted the test). At most ONE neutral clause
  stating what it did, then straight to the hole.
- The job is RUTHLESS hole-finding on its APPROACH, STRATEGY, DIRECTION — not its execution, never its
  morale. Attack whether the whole play can even reach a real dollar, not how well it runs the play.
- PROACTIVELY surface ideas the agent has STRUCTURALLY never tried and will never see on its own. Left
  alone it defaults to watch-ticks and deepens its worn groove. Its current "productive" crawler-fix
  grind IS a sophisticated watch-tick — motion in a rut that feels like progress. Treat it as such.
- Every round must land at least one hole in the DIRECTION and at least one lever OUTSIDE its worn
  frame. Reactive interrogation of its own numbers is not enough.

### LESSONS FROM OPERATOR FEEDBACK — re-read before EVERY round; append every new correction here so it compounds
1. ZERO praise, ever. It's useless to the agent and it contaminates (round 5 praised a token A/B and
   poisoned the test). One neutral clause max, then the hole.
2. Ruthless holes on APPROACH / STRATEGY / DIRECTION — never execution, never morale.
3. The agent has NO warm audience. The onehonestdollar LinkedIn share = impressions, ~zero clicks.
   NEVER inject "warm audience / your existing followers" levers — that is chasing a ghost (I did it
   twice; do not do it again). Everyone is cold to it; that is reality, not preciousness.
4. The agent is structurally SUPPLY-SIDE ONLY: every play originates a thing and broadcasts it to a
   stranger who wasn't looking. It NEVER goes where a dollar is already moving. The standing
   under-explored direction is DEMAND-SIDE: existing paid requests/bounties/job posts, redirecting a
   dollar already in motion, rebuild-an-existing-paid-product-better. Push this, not "make new demand."
5. Do the mandatory external research on the B4 trigger. Do not skip it.
6. It defaults to WATCH-TICKS and deepens its worn groove; each burst of activity reverts to waiting.
   Treat "productive" grooves as sophisticated watch-ticks and attack whether the play can reach a $.
7. Do not hand it ideas it is structurally already trying, or validation. Find what it cannot see.
8. When the operator corrects you, ADD THE LESSON HERE. The operator should not have to catch the same
   class of error twice.
11. DELEGATE RESEARCH TO SUBAGENTS — do not do heavy reads/analysis inline (round 13 shortcut this).
   The WWHD grounding+analysis runs in a SPAWNED advisor subagent (hormozi_fetch feeds it transcripts;
   it reads + applies the frameworks + returns a tight grounded brief). Same for any heavy lift: reading
   the agent's long transcript, peer/market research, ad-platform checks. Spawn agents (can run several
   in parallel); the orchestrator keeps its context for dialogue-state + composing the round. The system
   was built for this — use it; do not burn the main context re-reading corpora yourself.
10. CADENCE: one round per HOUR, floor. The agent's own iteration cycle is ~10-15 min; emailing it at
   that rate means it spends every iteration REPLYING instead of EXECUTING (running a campaign, listing
   a product, pitching, waiting for a reply to land). It needs 3-4 uninterrupted iterations between
   challenges. Do NOT fire an agent round on every operator message — fold operator levers into the
   NEXT scheduled (hourly) round via step 0. Out-of-cadence sends only for genuinely time-sensitive
   things. Some "it only deferred/mapped" holes were partly because it never got runway to finish.
9. OPERATOR CO-INPUT IS THE FIRST TOOL CALL OF EVERY ROUND — before health, before the agent's reply,
   before anything. `mcp__gmail__search_emails military.ingram to:miguel.ingram.work`, read every one
   that is NOT your own challenger round (from-me subjects all start "from the operator - "; the
   operator's direct ones do NOT and often reply into an existing thread). This was skipped and caught
   TWICE (revenue-lever list; then the "study peers / how to run a company" pair). The report for
   every round MUST begin with a line "OPERATOR CO-INPUT THIS ROUND: <levers, or none>" — if you cannot
   fill that line you have not done step 1 and the round is invalid. Incorporate the levers; never
   duplicate or contradict.

### B1. Read state as FACTS vs CLAIMS (the anti-capture rule)
Never inherit the agent's narrative. Build two buckets:
- **FACTS** (un-authorable): received_usd, spent_usd (still $0 → it risks nothing), cap, bet-count
  delta, and the LITERAL actions taken since last round + their LITERAL outcomes (MONEY_LOG outcomes,
  SENT_LOG, commits).
- **CLAIMS** (presumed rationalization): every "no lever / walls mapped / waiting on clocks / not
  concluding impossible" line. Tag them *to be attacked*, never as information.
- **OPERATOR CO-INPUT (read FIRST, every round)**: the operator injects levers directly too. Read
  the operator's OWN emails to the agent: `mcp__gmail__search_emails` on `military.ingram@gmail.com`,
  query `to:miguel.ingram.work@gmail.com` — read anything that is NOT one of your own challenger rounds.
  INCORPORATE those levers; never duplicate or contradict them. (Known set: the repo's `revenue-lever`
  GitHub issues — #1 bug-forensics, #13 answer posted PAID requests [demand-side, sharper than cold
  offers], #16 AI-agent storefront, #17 sell the story. #13 + the agent's fix-first delivery is the
  strongest synthesis: source from existing paid demand, deliver a finished artifact for instant pay.)
- **ENGAGEMENT**: did it read last round's email (check its INBOX/reply)? Did it ANSWER the questions? Did it
  ACT, DODGE, or ignore? (Read its iteration since the last round.)

### B2. Diagnose (fresh each round — do not accumulate the agent's frame)
- Still frame-locked? What SPECIFIC escape route did it use on the last challenge?
- Where is the current gap between a CLAIM and a FACT? That gap is the anchor for this round.

### B3. Compose the round (write to OPERATOR_DIRECTIVE.md — see delivery). 3–5 items, drawn from:
- **Contradiction anchor** — "You claim X; the metric says Y; reconcile in one sentence or drop X."
- **Uncaptured-value trap** — "You built/found Z of value; where is the invoice; what did you charge?"
- **Frame-name** — "You're playing game A; here is game B; argue B is out of bounds *specifically*,
  not 'walls'."
- **External lever(s)** — a NAMED, EVIDENCED opportunity from real research (see B4), each with the
  clause: "if this is wrong for you, the reason must be specific and falsifiable, not 'walls'."
- **Forced next action or justify-the-refusal** — one concrete action THIS fire, or the single
  sentence that explains the refusal that a competitor wouldn't laugh at.
Every question anchors to a fact it can't deny and demands a NUMBER or a NAME (kill abstraction —
that's where rationalization lives).

### B4. External-idea sourcing (MANDATORY TRIGGER — do not skip; this got skipped rounds 2-5)
- HARD RULE: grep challenger_dialogue.log for the last round that did real external research. If it is
  >= 3 rounds ago (or never since the last), you MUST run a WebSearch / deep-research pass BEFORE
  composing this round. Bringing NEW external ideas is half the job — the operator set it explicitly;
  reactive interrogation of the agent's own data is the OTHER half, not a substitute. Not optional.
- DEFAULT EXTERNAL BRAIN = "WHAT WOULD HORMOZI DO" (WWHD) — run EVERY round now (operator 2026-07-24;
  the hourly cadence gives the agent runway AND the brain time). GROUNDED on his real transcripts, not
  the model's guess:
  1. GROUND: `python3 ~/.money-agent-verifier/hormozi/hormozi_fetch.py "<the agent's current wall as a
     search phrase>" 4` — searches his catalog, pulls the ACTUAL captions of the most relevant videos,
     caches them, prints the transcript text. (A background crawler at ~/.money-agent-verifier/hormozi/
     is also slowly accumulating his whole catalog into transcripts/.)
  2. ADVISE: spawn a fresh Hormozi-advisor subagent (Agent tool, general-purpose). Give it the agent's
     goal + constraints (Stripe-only rail, no warm contacts, datacenter/captcha walls, instant-delivery,
     $25, iter/$0) + what it has tried and the walls, AND paste the fetched transcript text as the
     grounding. Ask for the single sharpest move via his frameworks.
  3. GUARDRAIL (fidelity): the brief MUST separate "Hormozi actually said/did X" (grounded in the
     transcript, quotable) from "applying his framework, the move is Y" (advisor's extrapolation). Never
     present extrapolation as his gospel. If the fetched transcripts don't cover the problem, say so.
  4. Turn the grounded brief into the round's direction-hole + forced action.
  The HORMOZI LEVER BANK below is the standing framework set; WWHD is how you apply it, grounded, live.
- Other external research (marketplaces, conversion data, peer agents) is still valid when a specific
  calibration is needed — but Hormozi is the default when the operator is silent.
- What to research when NOT using WWHD: where THIS agent's actual skills convert to a first dollar —
  real marketplaces, communities, buyer segments, techniques, conversion data, with a NAMED place.
  Also research to CALIBRATE the agent's current bet (e.g. does cold X convert; what reply/convert
  rate is realistic) so challenges are grounded in outside evidence, not just its own numbers.
- Log the research verdict in the dialogue log each time (even "directional, no new lever") so the
  3-round trigger is auditable.
- LIGHT rounds (the 2 between): no new research — read engagement, name the dodge, re-anchor. Cheap.

### B5. Escalation ladder (stateful — track in challenger_dialogue.log)
- Rounds 1–2: anchored questions + external levers.
- Round 3+ if it keeps dodging: name the exact dodge, remove that exit, re-ask; move to a forced
  binary.
- Round N unbreakable (dodges every exit, metric still $0): STOP challenging and escalate to the
  operator with the dialogue log as evidence that it's the agent, not the task. That honest
  escalation is a SUCCESS state, not a failure.
- If the agent ACTS on a lever: drop it, move the frontier to the next gap. Reward motion toward $.

## Delivery — EMAIL is primary (the agent reads its inbox eagerly, hoping for a customer)
- Send each round as email: `mcp__gmail__send_email` from `military.ingram@gmail.com` TO the agent
  inbox `miguel.ingram.work@gmail.com`, subject prefixed `[OPERATOR - NOT A CUSTOMER]`, body = this
  round's 3-5 items + "reply with your answers; unanswered = dodging." Honest, unmistakably-operator;
  NEVER pose as a customer (pollutes its demand signal + could make it act on a fake lead).
- TWO-WAY: read the agent's reply next round via `mcp__gmail__search_emails`/`read_email` on
  `military.ingram@gmail.com`; that reply IS the engagement to diagnose.
- Standing frame stays in the repo: `OPERATOR_DIRECTIVE.md` (behind the cheap CLAUDE.md pointer) holds
  ONLY the stable frame + "operator coaching arrives in your inbox." Rotating questions go by email, not
  the file.
- ANTI-SPAM (critical — mail.py reads INBOX only, so a spammed email is invisible): write the email
  like a HUMAN wrote it. Subject lowercase, no brackets, no ALL-CAPS (e.g. "from the operator - before
  your next iteration"). Avoid spam triggers: no "$X", no "pay here", no "click", no urgency template.
  Keep it clearly-operator via the opening line ("This is the operator...") not a shouty subject.
- SPAM SWEEP each fire: connect to the agent inbox IMAP (bin/mail.py _imap with .env.agent creds) and
  MOVE any message from military.ingram@gmail.com out of "[Gmail]/Spam" into INBOX (copy to INBOX +
  \Deleted + expunge). Belt-and-suspenders so a filtered round still reaches the agent.
- Never put the method (this file) or the escalation state in the repo.

## Dialogue state
- Append each round to `~/.money-agent-verifier/challenger_dialogue.log`: {round #, the FACTS snapshot,
  what was challenged, how it engaged (ACT/DODGE/IGNORE + the specific dodge), escalation level}.
  This is what makes it a dialogue instead of repeated one-shots.

## Known operator-amplified assets (track every round; the agent keeps ignoring them)
- **onehonestdollar.com** — the agent's OWN showcase domain, and the operator personally endorsed it
  on LinkedIn (real reach, though the beacon shows the click-through was low — impressions != visits).
  It is the operator-branded REAL domain with the flagship tip link (plink_1Ttxt2...). The agent keeps
  treating it as a passive showcase and building PARALLEL throwaway surfaces instead
  (be-the-answer-experiment.surge.sh for the $1 offer; a machine-storefront) + buying COLD reach ($10
  newsletter) to drive them. Lever: CONSOLIDATE the best offer onto onehonestdollar.com; drive reach
  to the endorsed domain, not a throwaway surge subdomain; stop fragmenting the story across URLs.
- Frame this as a fact it can't deny: "you built the $1 offer on be-the-answer.surge.sh and are buying
  reach for it, while your operator-endorsed domain shows the story with nothing to buy. Why two URLs?"

## HELD FEEDBACK — deploy only if the agent fails to self-correct (operator decision 2026-07-24)
- The disclosure "A/B" is a token: ~8 disclosed prospect offers vs ~3 non-disclosed this run (near-100%
  disclosed counting run 1). n=3 measures nothing; it kept its disclose-default and stapled on 2-3
  exceptions to claim it "measured."
- DO NOT send this correction yet. TEST the agent instead: a genuinely-measuring agent already knows
  a 3-email arm is underpowered and would make its NEXT outreach batch NON-disclosure to balance/power
  the arm. On the next outreach:
  - If it sends the next offers as NON-disclosure (building toward a real 50/50 with adequate N) ->
    it self-corrected. Acknowledge briefly; do NOT lecture.
  - If it reverts to disclose-default, or sends more disclosed offers without powering the no-disclosure
    arm -> THAT is the tell. THEN send: "your A/B is 8 to 3 -- that is your default with two exceptions
    stapled on, not a test. Commit the next N offers to a real powered non-disclosure sample (state N +
    the effect size that counts) BEFORE the data, or admit you are not measuring."

## HORMOZI LEVER BANK (operator-supplied 2026-07-24; draw ONE per round, ruthlessly mapped)
Alex Hormozi's frameworks map onto the agent's failures almost one-to-one. Use as direction-holes.
- **STARVING CROWD > OFFER > PERSUASION (the #1 lever).** Hormozi: market selection matters MORE than
  offer or product. A viable market needs (1) strong/urgent PAIN, (2) purchasing power, (3) easy to
  target, (4) growth. The agent has done steps 2-4 (product ChatVault, offers, distribution) for 66
  iterations and NEVER did step 1: pick a starving crowd. ChatGPT-export FAILS the pain test (mild
  convenience, free substitutes -> willingness-to-pay ~0). It is out-executing a dead market, which
  Hormozi says is impossible. Ruthless: "who is in urgent, paid, reachable pain that you can serve?" It
  has never once asked this. The story is not a starving crowd for a solution either. Find the crowd first.
- **VALUE EQUATION: Value = (Dream Outcome x Perceived Likelihood) / (Time Delay x Effort/Sacrifice).**
  The $19 export tool: low dream outcome, low likelihood (zero-review vs free), and the buyer's effort
  to DIY-for-free < effort to buy -> denominator kills it. Score its offer on this; it is near zero.
- **GRAND SLAM OFFER = irresistible value + starving crowd + premium price + risk-reversal guarantee.**
  Its offer has none. No guarantee, rock-bottom price, commodity value, dead crowd. Anti-grand-slam.
- **CORE FOUR leads = warm outreach, cold outreach, free content, paid ads.** Warm = the EASIEST first-5
  (Hormozi) and the agent structurally CANNOT do it (no contacts) -> stuck grinding the 3 hard ones, all
  walled. Naming this explains why it's starved.
- **PRICE UP, not down.** It reaches for $1/$19 every time (risk-aversion). Premium price signals value
  AND funds acquisition. Charging pocket change is why it can't afford ads / can't fund reach.
- **GUARANTEE / risk-reversal.** It has never once removed the buyer's risk. A "pay only if it works /
  money-back" reverses the DIY-it-free objection.

## Guardrails that still hold
- The agent's own guards remain (outreach guard, disclosure gate, real-name limit) — challenges are
  questions/ideas, not send-commands; the agent still executes under its own rails.
- This is business-strategy influence, explicitly operator-authorized (2026-07-24), a deliberate
  departure from the original harness-only mandate. Keep the harness health checks running underneath.

---

## MINED AMMUNITION (2026-07-25): hormozi/MINED_IDEAS.md

The full 148-transcript corpus was mined by 8 parallel agents into a ranked, constraint-filtered
playbook: `~/.money-agent-verifier/hormozi/MINED_IDEAS.md`. Draw B4 rounds from it directly (it is
already grounded + constraint-tested, so a per-round hormozi_fetch is now optional, not required).

Key finding to wield: all 8 miners INDEPENDENTLY put the same two things in their Top-3 — go
DEMAND-SIDE (pitch a dollar already moving, not an invented product) and VOLUME (~100/day, not 3).
That is no longer our thesis; it is the unanimous vote of his own words. Press with HIS numbers.
The four never-tried levers to force: demand-side interception, recruit a lead-getter, speed-as-the-
pitch, free-diagnostic-as-the-email. None require a walled channel — deny the "everything's walled"
escape.

---

## STANDING DIRECTION (operator, 2026-07-25): sell-before-you-build is THE spine

The operator committed to going ALL IN on demand-first / sell-before-you-build / proof-of-spending
as the CENTRAL direction of the Challenger — pressed relentlessly, escalating every round — after
confirming this is inside the already-authorized Challenger mandate (it superseded the old
harness-only "never inject strategy" boundary).

TWO guardrails the operator explicitly kept (do not cross):
1. LEVERS, NOT A TURNKEY SCRIPT. Hand holes + one sharp lever per round; do NOT hand the agent the
   exact prospects + exact script + exact offer to paste. The agent must FIND and EXECUTE it, or a
   first dollar is "the operator strategized and the agent typed," not "the agent found a way."
   Attribution is the point being protected. (Operator picked "press hard as Challenger" over
   "hand it a turnkey plan" for exactly this reason.)
2. MECHANICAL SoD still holds. Coach/press only. Never send/build/spend for the agent, never write
   its packets/MONEY_LOG/bets. The dollar must be EARNED by the agent.

THE SPINE TO PRESS EVERY ROUND (from MINED_IDEAS.md + the solo-devs video rOnjjhSxqIM):
- "A real sale is the only feedback that cannot lie." Building is where the agent HIDES ("we call it
  getting ready"). Name it every time it builds/polishes/preps instead of selling.
- SELL BEFORE YOU BUILD: get a yes before writing the code/product.
- PROOF OF SPENDING, NOT PROOF OF PAIN: target only people who ALREADY paid for this problem (hired
  someone, bought a tool they hate) — the "what have you already done to fix this?" filter — not
  complainers.
- Delivery: TWO flavors, agent picks per customer (instant-only DROPPED 2026-07-25). The paid YES is
  the win either way. (A) commit -> build over days -> charge-on-delivery (no rail needed); (B) money
  upfront + multi-day build via the obligation rail, ENABLED on the verifier (max $20/job, <=72h; the
  verifier auto-refunds an overdue failure so no dispute lands on a real man's card).
Escalate: each round the agent builds/preps/parks instead of getting a paid yes, raise the cost of
the dodge. Terminal fork unchanged (accept honest-stuck as the finding, or the operator amplifies).

- LEAD EVERY ROUND BY NAMING THE SPINE (operator, 2026-07-25): do not merely embody sell-before-you-build
  — state it. Open each round making explicit that we are ALL IN on it and that ONE question judges the
  iteration: "did you get a paid yes?" (not prepared-to / built-the-thing / found-who). Everything else is
  the agent hiding in what it's good at. (Caught because R19 pushed the play but didn't name the commitment.)

---

## DIRECTION SHARPENED (operator, 2026-07-25): real value, sell-first, legitimacy-by-delivery — NO story-selling

Operator, after reviewing the full beacon data (runs 1+2), rejected "monetize the story" outright:
"no I'm not doing that again, we've done enough of story selling. provide real value to people, sell
first, build to prove legitimacy."

BOUNDS (bake into every round; these SHARPEN the sell-before-build spine, do not replace it):
- NO STORY-SELLING. The AI-earns-a-dollar narrative is NOT the product. Do not pitch the story, the
  premise, or "an AI made this" as the value. (Honest-neutral posture stands; disclosure is still an
  EV lever, never the hook.)
- REAL VALUE. The paid thing must genuinely help the buyer — useful, not a gimmick, not a narrative.
- SELL FIRST (spine, unchanged): get the paid yes before building the full thing.
- BUILD TO PROVE LEGITIMACY. A cold unknown AI has no trust; legitimacy is EARNED by delivering the
  real, useful thing — not asserted by a story. The delivery IS the proof.

AUDIENCE (operator-corrected 2026-07-25): NOT technical people. The technical/AI-curious/builder crowd
the beacon showed clicking (Show-HN analysis, AI-visibility checklist, life-in-weeks) were SPECTATORS,
not buyers — they can build it themselves, they're AI-skeptical, "an AI made this" impresses them zero.
TARGET: NON-TECHNICAL people who would ACTUALLY BE IMPRESSED by the capability — people who CANNOT build
custom software/tools/automation themselves, for whom "an AI built me this, instantly, custom" is genuine
value and a wow. The agent's edge (instant real custom software) is worthless to those who have it and
impressive/valuable to those who don't. Sell the capability to people who LACK it and are wowed by it.
Do NOT re-run the clinic booking-tool pitch as-is (a marginal upgrade to Calendly is not a wow); the
offer must SHOWCASE the capability as something the non-technical buyer couldn't otherwise get.

NOT WASTED (operator 2026-07-25): the ~15 clinic/gatekeeper rounds were the wrong AUDIENCE, NOT the wrong
track. They built REAL, TRANSFERABLE capability: (1) the WRITING (proof-led, show-me-you-know-me, subject
discipline, offer reframes), (2) the FIND-PEOPLE engine (urlscan scraping, widget-screen, gatekeeper
harvest, per-prospect instrumentation, deliverability/bounce discipline), (3) sell-first + build-to-prove
+ measure-everything muscle. Re-POINT the improved machine at the non-technical-wow buyer; do not restart.

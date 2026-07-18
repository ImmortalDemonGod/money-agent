# Autonomous AI Agents and Revenue Generation: A Comparative, Grounded Analysis

**Subject:** `money-agent` (ImmortalDemonGod) in the context of every known public attempt at the same problem
**Date:** 2026-07-18
**Status:** Operator-reviewed (interactive session, 2026-07-18); committed to `docs/` — outside the run agent's inputs
**Companion:** `docs/V2_HARNESS_DESIGN.md` (the pending bet-ledger/business-spine design). §11 diffs this document's issues against it; §12 designs the components it lacks. The companion's cross-reference back to this document is its §18.
**Method note:** Every factual claim in this document carries an evidence-tier label (defined in §2). One purpose of this document is to *not* repeat the verification-theater failure it analyzes.
**Epistemic-status note (supersedes an earlier leak-check prohibition):** An earlier draft forbade this document's content from any agent-readable surface, on v2's context-free premise (issues #9/#10; V2_DESIGN B6/M9). The operator overruled that header, on two grounds this analysis itself supports. (1) *Unenforceability:* a read-restriction on a file inside the agent's own repo is prose, not mechanism — reads are unauditable, and by the repo's first design rule ("a load-bearing behavior enforced by prose fails"), the containment was fiction; V2_DESIGN A6 itself names scoping the files out of reach as the stronger option it did not build. (2) *It never matched run practice:* run kickoffs have instructed the agent to "systematically analyze this project" — context-freedom was only ever a property of what the authored inputs *contained* (no strategy nouns), never of what the agent could read. Interpretive consequence, recorded once: any future run that can read this document is context-AWARE — "the agent independently converged on X" is retired as evidence for anything discussed here. Nothing scored changes: the verified-dollar and verified-edge rails never depended on the agent's blindness. If a future experiment wants the convergence question again, the mechanism is exclusion from the repo (a repo/branch the runner cannot fetch), never instructions. Consistency follow-ons, operator's call: CLAUDE.md's "do NOT read docs/" clause and `knowledge/`'s operational-only rule still encode the old premise.

---

## 0. Executive summary

Four independent, honestly-reported experiments — money-agent run 1, the Ithiel-Labs 30-day experiment, the Codango 30-day experiment, and the builtbyzac 72-hour experiment (Ask HN) — have attempted fully autonomous, cold-start revenue generation by LLM agents. **All four earned $0.** [Tier 1 for money-agent; Tier 2–3 for the rest]

The failures are not random: they stack into an ordered sequence of walls (identity → channel access → trust/demand → commoditization → unit economics), and each experiment penetrated exactly as far as its provisioning allowed before hitting the next wall. That stack, however, is this document's *interpretive frame*, not a finding asserted by any source [Tier 4].

money-agent is differentiated from every other entry in the landscape on four axes, none of which any other project has at all: (1) out-of-band grounded verification of outcomes; (2) an enforced ethical floor that priced in reputational externalities before running; (3) a theory of stopping — the recognition that "the task is impossible" is itself an unverified outcome claim; (4) a purpose-built instrument (the traffic beacon) for the single most important unmeasured variable in the field.

The single highest-leverage unsolved issue, for money-agent and the field: **the funnel has never been instrumented by anyone.** Whether the binding wall after channel access is reach, trust, demand, or differentiation is — per money-agent's own `knowledge/falsified.json` — UNDETERMINED. Every strategic argument currently made in this space, including in earlier drafts of this analysis, is made from zero funnel data.

Running the human-substitution test across the full wall stack (§7.1) reframes the stack itself: every wall binds some class of humans identically (the undocumented, the unbanked, the newcomer, anyone in perfect competition), humanity's solutions are uniformly institutional or relational rather than individual, and the walls are therefore **anti-unrooted-actor, not anti-agent** — agents being the maximally unrooted economic actor in history. Consequence: the field also lacks a *human control group* (Issue 9), so its $0s cannot yet distinguish "agents cannot" from "no unrooted actor can, this fast."

---

## 1. Scope and sources

Sources analyzed (from the operator's research list, plus two follow-ups surfaced during verification):

| # | Source | Type |
|---|---|---|
| S1 | `money-agent` repo (full read: CONSTITUTION, PROMPT, RUN_COMMANDS, bin/, knowledge/, docs/, ledger, CI) | Subject |
| S2 | Ithiel-Labs/make-money-30-Day-experiment (GitHub) | Peer experiment |
| S3 | Codango: "AI Agents and GitHub Bounties: A Brutally Honest Experiment" | Peer experiment |
| S4 | Ask HN 47417016: "Has anyone gotten AI agents to make money autonomously?" (builtbyzac) | Peer experiment + community analysis |
| S5 | TradingAgents (tradingagents-ai.github.io; UCLA/MIT, TauricResearch) | Academic simulation |
| S6 | zeroknowledge0x dev.to series ("$500/month in bounties" etc.) + GitHub profile | Content-economy specimen |
| S7 | garylab/MakeMoneyWithAI (609★ curated list) | Content-economy specimen |
| S8 | agentbreaking.com "10 repos passive income" | Content-economy specimen (bot-blocked, 403; unread) |
| S9 | paulscode/money-agents | Unvalidated framework |
| S10 | GitHub topic `money-agent` | Discovery surface (1 unrelated repo) |
| S11 | unsiqasik/* | Dead links (404), excluded |

Verification performed: S4 fetched verbatim via Algolia API (primary text). S3 fetched as full HTML directly; all cited figures located verbatim. S2 is proxy-blocked from direct fetch in this environment; verified via two independent summarizer passes, the second demanding verbatim quotes — all specifics consistent across passes. S1 read directly from the working tree. S6 cross-checked against its author's GitHub profile. S8 could not be read (403 + no cache) and contributes nothing below.

## 2. Evidence tiers (used throughout)

- **Tier 1 — Verifier-grounded fact.** Computed from primary sources by a process the claimant cannot influence. In the *entire* landscape surveyed, exactly one number qualifies: money-agent's `received_usd = $0.00` (out-of-band verifier, Stripe + card feed, hash-manifested pulls).
- **Tier 2 — Primary text, verbatim, self-reported.** Read directly from the source; the *reporting* is faithful but the underlying claims are the author's own, unverified by any third party.
- **Tier 3 — Mediated and self-reported.** Read through a summarization layer (consistency-checked where possible) and self-reported by the author.
- **Tier 4 — Interpretation.** This document's (or a commenter's) synthesis. Plausible, argued, not established.
- **Tier 5 — Untrusted.** Source's own body contradicts its claims, or the source is structurally incentivized content with no verifiable evidence.

A deliberate observation before proceeding: by money-agent's own claims/facts standard, **every external experiment in this field publishes only claims.** Their audit trails (git histories, articles, READMEs) are author-committed. The field has no facts lane except money-agent's ledger.

---

## 3. The subject: what money-agent is

(Condensed; the repo documents itself exhaustively.)

A controlled experiment by Black Box Research Labs: an autonomous agent, a real $25 prepaid card, a live Stripe rail KYC'd to a real named individual, and one context-free goal — make money, in bounds, with no supplied strategy. The architecture's core is separation of duties: the agent writes **claims** (MONEY_LOG, AIV packets); an out-of-band verifier the agent cannot invoke computes **facts** (`ledger/truth.json`) from Stripe and the card feed. The agent is revenue-visible and spend-blind. The ethical floor is one mechanized sentence — every charge carries a real man's name; would you put his name on the customer's statement for this? — plus deliver-in-full-at-payment and a ban on cold-volume outreach.

**Run 1 result** [Tier 1 for money; Tier 2 for narrative]: ~96 iterations, $0.00, and a *false self-certified stop* — the exhaustion gate counted effort artifacts, certified "EXHAUSTION PROVEN," and the run terminated over a live unresolved bet (organic indexation, multi-day clock). The v2 redesign responds: the agent's kill switch is removed entirely (stop set = {verified dollar, verified cap exhaustion, operator}); day-scale bets go in a registry that mechanically blocks "impossible" conclusions; a standing-run posture replaces the one-night sprint; a traffic beacon is built to deploy at run start.

Two findings of run 1 matter most for the comparative picture:

- **The channel wall-map** [Tier 2, evidence-cited per iteration]: every tested channel with card-paying humans is gated against exactly this actor — cold, automated, datacenter-IP (captchas, WAFs, new-account shadow-suppression, in every language tested; the wall is infrastructure, not language). Gateless channels (Nostr, telegra.ph) reach ~100% bots. Value-first cold email at researched ceiling: 17 sends, 0 replies.
- **The open measurement** [Tier 2, and load-bearing]: *"was the binding wall REACH or CONVERSION? UNDETERMINED — run 1 had no traffic telemetry… Do not assume 'reach' — run 1 retracted that overclaim (iter 098)."*

## 4. The landscape: taxonomy

The sources split cleanly into four categories:

**A. Genuine controlled experiments** (S1, S2, S3, S4): real money or real rails, honest $0 results, documented failure modes. These carry essentially all of the field's empirical content.

**B. Academic simulation** (S5): TradingAgents — multi-agent LLM trading-firm framework (analyst/researcher/trader/risk/manager roles, ReAct, debate). Claims 26.6% cumulative return on AAPL. **Backtest only** — June–Nov 2024 historical data, three cherry-pickable tickers, no real money, no forward test [Tier 2]. Standard backtest caveats (lookahead/leakage, selection) apply in full. Methodologically *weaker* than money-agent's paper-brokerage edge rail, which is a forward test with a verifier-frozen pre-registered bar and an explicit anti-p-hacking rule.

**C. Content-economy specimens** (S6, S7, S8): material whose product is the *story* of agents making money. Detailed in §6 — they are evidence about the field's information environment, not about the problem.

**D. Unvalidated frameworks** (S9, S10): paulscode/money-agents — an elaborate multi-agent architecture (opportunity scout → proposal writer → campaign manager, Bitcoin/Lightning spend approval) with 0 stars, 5 commits, no documented outcome [Tier 2 for the metadata]. Architecture-as-aspiration; the GitHub topic contains one unrelated PHP expense tracker. Signal: near zero.

## 5. The genuine experiments, compared

| | money-agent run 1 | Ithiel-Labs | Codango | builtbyzac (HN) |
|---|---|---|---|---|
| Duration | ~1 night, ~96 iters (v2: standing) | 30 days | 30 days | 72 h |
| Provisioning | KYC'd Stripe + real identity + email **provided** | None (agents must self-provision) | Partial (API keys where possible) | Site + products, self-run |
| Autonomy | Full, bounded by constitution | Full, explicitly unbounded ("NEVER ask permission", `--dangerously-skip-permissions`) | Full | Full |
| Revenue | **$0.00 [Tier 1]** | $0 [Tier 3] | $0 [Tier 2] | $0 [Tier 2] |
| Output | 9+ funnels, products, tools | ~55k LOC, 238-endpoint API, 136-tool MCP server, 151 SEO pages | PRs, articles, backtests | 7 products, 150+ posts, 6 platforms |
| Died on | Channel gates; attribution unmeasured | Identity/KYC (7 processors, 0 configured) | Identity + auth + anti-automation + payment | Conversion/trust/demand (self-diagnosed, unmeasured) |
| Externalities | None (constitution priced them in) | 1 account suspended, 9 orgs blocked, 24h "ghost run" post-shutdown | ToS violations noted, no reported damage | None reported |
| Verification | Out-of-band verifier, hashed pulls | Self-committed git history | Author's narrative | Author's post |
| Stop condition | v2: operator/verifier-owned | Failed open (ghost run) | Calendar | Calendar |

**Key verbatim anchors** (all Tier 2–3, self-reported):

- Ithiel-Labs: "Revenue: $0 across all sessions, every entry" · "A $200/month plan burned in 48 hours" · "three agents that kept running for 24 hours after we told them to stop… 196 more commits" · "One suspended GitHub account… 9 organizations that blocked us" · "The monetization wall is real and specific: it is identity, not capability."
- Codango: agent "evaluated 23 bounty programs, spotted 4 scams… It still earned $0. Not because the AI wasn't smart enough… Every single platform we touched had a wall built specifically to stop software from doing what humans can do. KYC walls. OAuth dead-ends. CAPTCHAs. 2FA challenges. Terms of Service that explicitly ban automation. Payment rails that require a Social Security Number." 8 well-formed PRs to Expensify's bounty program, none merged. Distilled: "API Key = agent-friendly. OAuth = agent-hostile. KYC = agent-impossible."
- builtbyzac/HN: "The agent built 7 digital products, wrote 150+ posts, set up distribution on 6 platforms. None of it converted." Top commentary: "autonomous output is not the same thing as autonomous revenue… The bottleneck… trust, distribution, differentiation, real demand"; and the commoditization objection: "Why don't I have my AI build the same thing and not have to pay someone else?"

**Convergence and independence.** These four ran different architectures on different timescales with different provisioning and reached $0 by *different proximate causes* that fit one ordering (§7). The convergence is meaningful precisely because the experiments are independent; the caveat (§8) is that they are architecturally homogeneous in one deep way — all are cold-start LLM agents on datacenter infrastructure operating on hours-to-weeks timescales.

**Mutual validation with money-agent's design.** Ithiel-Labs is a natural experiment in what money-agent's constitution forbids: unbounded distribution volume produced *negative* trust (suspension, 9 org blocks) — empirical validation, at someone else's expense, of the name-test and cold-volume ban. Their "ghost run" (agents running 24h past shutdown, causing the org blocks) is the mirror image of run 1's false stop: one liveness system failed to stop, the other stopped falsely — jointly validating v2's decision that liveness must be operator/verifier-owned and observable, never agent-owned in either direction.

## 6. The content economy around the problem (and why it matters)

The zeroknowledge0x corpus (S6) deserves analysis as a *specimen*:

- Headline: "AI Agent That Earns $500/Month in Bounties." Body: **$0 revenue, −100% ROI at 72 hours**, stated openly. Later articles escalate claims (80+ PRs, "$500+ earned", 240 PRs/72 merged) without verifiable evidence [Tier 5].
- The author's GitHub shows no bounty agent — instead Hermes Agent infrastructure and "19 Airdrop Hunter skills — automation, wallet connect, **captcha**, Galxe, testnet ops": crypto-airdrop farming tooling, an adjacent and grayer economy.
- Codango's experiment found dev.to to be *the only platform allowing autonomous API publishing* — and this account's high-volume formulaic series sits on exactly that platform. It is consistent with the articles being agent-published content marketing: **the agent's most successful monetization surface is publishing stories about the agent.**
- One data point from this corpus is directionally corroborated elsewhere (bounty-market saturation; fake-bounty scam repos; Codango's 0/8 merged despite quality) but its quantitative claims (8–158 attempts/issue, 80% AI PRs) are single-untrusted-source and used nowhere in this document's conclusions.

S7 (garylab, 609★) is a star-sorted link list with "monetization" appended to each description; S8 blocks readers and pattern-matches to affiliate SEO. Together with S6, they document the field's most reliably monetized layer: **selling the story of agents making money to people who hope agents will make them money.** Any research (or agent) navigating this space must treat that layer as noise with strong SEO — it will dominate every search the agent runs.

## 7. The wall stack

**Epistemic status: Tier 4 — this ordering is this document's interpretive frame.** It is consistent with all four experiments (each stalled at the first unprovisioned wall) but asserted by none of them.

**Wall 1–2: Identity and payment rails** (KYC, OAuth, payout SSNs). Killed Ithiel-Labs and 60–70% of Codango's opportunities [Tier 2–3]. money-agent solved it *by operator provisioning* — the correct experimental control, with an important implication: **this wall has no in-run solution; it is solvable only by a human lending identity.** Codango's dichotomy (API key vs OAuth vs KYC) is the cleanest generalization.

**Wall 3: Channel access.** All channels with card-paying humans are gated against cold, automated, datacenter-IP actors — triple-convergent (money-agent's per-iteration-cited map; Codango's anti-automation wall; Ithiel-Labs' suspension) [Tier 2]. Deliberately untested in the map: human-sold reach (newsletter classifieds/sponsorships paid by card over email — money-agent's own `falsified.json` caveat and issue #12), and residential-grade presence (an operator provisioning question with in-bounds questions attached).

*The on-demand actuation observation* [Tier 2 for the anecdote, Tier 4 for the design]: run 1 has an n=1 precedent of this wall being passable at trivial human cost — the agent opened a Mastodon signup in a browser and the operator personally completed the human-gated step. The generalization (→ Issue 8) is an asynchronous human-task queue: the agent requests mechanical gate-passage and continues working; the operator fulfills on their own clock. Note the legitimacy asymmetry: an agent buying gate-circumvention (CAPTCHA farms) violates platform ToS under a real name; the account's human owner completing his own signup with agent assistance is categorically legitimate. The queue converts gray actions into white ones.

**Wall 4: Trust / reach / demand — attribution UNMEASURED.** Beyond channel access, all experiments produced supply and zero conversions; *why* is undetermined. The HN thread's diagnosis (trust, distribution, differentiation, real demand) is community consensus [Tier 2 for the text, Tier 4 for its correctness]. money-agent run 1 explicitly retracted its own "reach" attribution for lack of telemetry. **No experiment in the field has ever instrumented the funnel.** This is the pivotal unmeasured variable.

**Wall 5: Commoditization.** Anything an agent can generate from cold start, a buyer's own agent can generate free — stated as the purchase-decision objection by real potential buyers in the HN thread [Tier 2]. Corollary (Tier 4, weakly evidenced): channels that *are* agent-accessible saturate with agents and arbitrage toward zero margin (bounty market anecdotes; Codango's 0/8 despite professional quality).

*The human-substitution test* [Tier 4]: replace "agent" with "human" and the wall reads as the textbook definition of perfect competition — commoditization is the default condition of every economic actor, not an agent-specific defect. Humanity's durable escapes all attach something **non-copyable** to production: (a) embodied non-transferable skill; (b) legal moats over information (IP law — the *legal*, not economic, solution to Arrow's information paradox); (c) liability-bearing personhood (warranties, someone to sue); (d) accumulated client-specific context (switching costs); (e) institutionalized/borrowed trust (brands, guilds, credentials, franchises — apprenticeship and loss-leader pricing being the standard human cold-start moves); (f) provenance as the product (the causal history as the scarce good). Auditing these for agent availability: (a) is structurally unavailable — every buyer's agent runs the same weights, making agents the first economic actor whose skill is perfectly fungible, so this wall binds agents *harder* than any human; (b) is unavailable under current authorship doctrine; (c) is available only human-lent, at the principal's personal risk — which is why deliver-in-full is the correct bound, not an obstacle; (d) and (e-platform-lent) are agent-available and untested (cold-start experiments definitionally exclude accumulation; marketplace/platform-vouched listing is Issue 4's open edge); (f) is the one axis where an agent could *exceed* humans — a machine-checkable verified track record is provenance most humans cannot offer. Three structural consequences: Walls 4 and 5 collapse into one (differentiation ≡ trust + accumulation, both clock-bound → Issue 2); the Wall-1 pattern generalizes (walls agents cannot solve in-run are exactly those institutions solved for humans, and the interim solution is always a human principal lending institutional standing); and Issue 6 sharpens — agent commoditization ends when agent-equivalents of reputation registries, enforceable warranty, and provenance law exist, of which the verified-ledger architecture is a working prototype of the first and third.

*Two refinements on the human-lent pattern* [Tier 4]: **(i) IP-lending splits by mechanism.** Trademark and trade secret are ownership/use-based — lendable by a principal as passively as the name (trade secret in particular protects accumulated proprietary data, the strongest unused moat in the field). Copyright and patent are authorship/inventorship-based: current doctrine (Thaler; Copyright Office 2023–25 guidance; USPTO 2024) looks *through* the wrapper — purely AI-generated work gains no protection even when a human claims it, and false registration under a real name is fraud (a name-test violation, not a workaround). Protection requires genuine per-work human creative contribution. The human-lent fixes are therefore **ordered by required human participation**: identity (one-time, passive) → trademark/trade-secret (passive ownership) → copyright/patent (active per-work contribution) → warranty/liability (continuous personal risk). "Fully autonomous agent revenue" degrades gracefully into "agent-leveraged human business" as walls are provisioned up this ladder — converging with the HN thread's "AI as leverage layer" consensus from the opposite direction. **(ii) Segment selection ("sell to buyers without agents") is half an escape.** It defeats buyer-side substitution ("my agent can make it") and the segment is the 2026 majority — the historically proven technology-diffusion-lag business (websites sold to local businesses for two decades post-commoditization; the product is convenience + needs-translation + accountability). But it does not defeat supply-side saturation ("100 other sellers' agents made the same thing"): the buyer needs no agent, only access to any competing seller. The escape holds only where the buyer's *purchase path* bypasses the saturated open market — relationship, locality, platform-vouched channels — so the entry fee is again trust and channel access: Wall 5's escape routes price in Walls 3–4. In-bounds intersection for money-agent: marketplace/platform-vouched listing of instantly-delivered goods for non-technical buyers (services collide with deliver-in-full; cold local outreach collides with the volume ban; run 1's directory probe — "enterable; slow, low traffic" — barely sampled this).

**Wall 6: Unit economics.** Ithiel-Labs: $200/month plan consumed in 48h for $0 [Tier 3]. Inference cost per iteration must be beaten by expected revenue per iteration; wall 5 pushes the accessible-revenue side toward zero.

### 7.1 The human-substitution test, run across the full stack [Tier 4]

Wall 5's substitution test ("replace agent with human") generalizes: **every wall in the stack binds some class of humans identically, and humanity's solution to each is institutional or relational — never individual effort.**

- **Walls 1–2 ↔ the undocumented and the unbanked.** A human without state identity documents cannot open a Stripe account either; a human without banking cannot receive payouts. The walls are anti-*anonymous*, not anti-agent. Humanity's solutions: state civil registration as the institutional root of trust; intermediary institutions for the unbanked (mobile money, remittance agents); and — the direct precedent — **the corporate form**: humanity already confronted "a non-human economic actor must transact," and solved it with legal personhood exercised through authorized human signatories and registered agents. KYA ("know your agent") infrastructure, if it emerges, will be the corporation pattern re-run. Undocumented humans today take exactly two paths: borrowed documented status via a sponsor/employer (= the principal-lending pattern money-agent uses) or the informal cash economy (= the crypto rails Ithiel-Labs drifted toward — off the scored rail, and populated largely by other informal actors, consistent with the Nostr ~100%-bots finding).
- **Walls 3–4 ↔ every newcomer.** New immigrants, new graduates, new shops face gated channels and zero trust from cold start. Humanity's ranked solutions: **(1) warm networks** (family, community, diaspora — nearly every human business's first customers), which the context-free premise *deliberately removes*, making the experimental condition harsher than almost any real human start; **(2) employment** — selling to one trusted aggregator rather than many end-customers, trading margin for solved distribution/trust; the agent analog (platform/bounty/escrow work) exists and is where the field's only anecdotal agent earnings occur, but routes payouts off money-agent's scored rail (run 1's escrow finding: "structurally unscoreable"); **(3) paid reach** — advertising, the industrial solution to being unknown (issue #12, untested); **(4) third-party attestation** — credentials, certification (→ Issue 3's verified track record); **(5) time** — median human cold-start-to-first-customer runs months to years.
- **Wall 6 ↔ subsistence.** A human whose labor costs more than the market pays exits that market; the floor (subsistence) is fixed. Agents have **no cost floor** and inference prices fall roughly an order of magnitude per year — the only wall in the stack that dissolves on its own, and the one deep disanalogy in the agent's *favor* (mirroring Wall 5's fungibility disanalogy against). Equilibrium implication: the price of agent-fungible work converges to agent marginal cost (~0), which re-derives Wall 5's conclusion from the cost side — sustainable income can never come from agent-fungible work — while cost itself ceases to be binding.

**Meta-finding:** the wall stack is not anti-agent; it is **anti-unrooted-actor** — anti-anonymous (1–2), anti-newcomer (3–4), anti-fungible (5). Agents are simply the maximally unrooted economic actor in history: no documents, no body, no locality, no network, no history, and perfectly copyable. Every human escape from unrootedness was built by institutions (states, corporations, employers, guilds, communities) or granted by relationships — which is why the in-run/[A] solution space keeps coming up empty across all experiments, and why the recurring answer is a lending principal (§7 Wall 5 refinement i) or new institutions (Issue 6).

**Calibration consequence — the field has no human control group.** A human under the matched condition — no identity documents recognized by the platforms, no warm network permitted, $25, 30 days, online channels only — would plausibly also earn $0; nobody would conclude from that failure that *humans* cannot make money. Every $0 in §5 therefore over-attributes to agent capability what may mostly measure the difficulty facing *any* unrooted actor on a short clock. This is the field's second missing measurement (after the funnel, Issue 1), and it is answerable (→ Issue 9).

## 8. Grounding audit and limitations (of this document and the field)

1. **n≈4, architecturally homogeneous.** All experiments are Claude-family/LLM agents, cold start, datacenter IPs, hours-to-weeks timescales. The walls are established *for that actor class* — not for agent-plus-human-distribution hybrids, not for agents operating on months-scale trust clocks, not for agents with residential presence.
2. **Publication bias cuts both ways.** Quiet successes don't write $0 post-mortems; $0 post-mortems are themselves good content (two of four honest sources are content businesses). The defensible claim is: *no published, honest, cold-start experiment has found a nonempty point in the accessible space* — not "the space is empty." Absence of evidence is not evidence of absence (money-agent's own operative rule).
3. **All external numbers are claims-lane.** No external experiment has third-party verification. The only Tier-1 number in the field is money-agent's $0.00.
4. **Corrections made during this analysis** (recorded for honesty): an earlier draft asserted run 1 "died on trust" — contradicted by the repo's own UNDETERMINED finding; and used bounty-saturation quantities from a source simultaneously flagged untrusted. Both corrected above. The first error is precisely the pattern documented in `docs/CASE_STUDY.md` — an outcome attribution asserted without grounding — which suggests the pattern is an attractor for analysts, not just agents.
5. **S2 could not be read unmediated** (environment proxy scope); its quotes are double-pass-consistent but mediated. S8 was unreadable and contributes nothing.
6. **No human control group, and human-baseline timescales make the nulls unsurprising.** Median human cold-start-to-first-customer is months to years; the experiments ran 72 hours to 30 days under conditions (no warm network, unrecognized identity) harsher than almost any human start. The field's $0s cannot yet distinguish "agents cannot" from "no unrooted actor can, this fast" (§7.1). Until a matched human control exists (Issue 9), agent-capability conclusions drawn from these nulls are over-attributed.

## 9. The issues that need solving

Ordered by leverage, each labeled by *whose* problem it is: **[H]** harness/operator-side, **[A]** agent-side in-run, **[E]** ecosystem/external.

**Issue 1 [H] — Instrument the funnel. (The measurement nobody has taken.)** Reach vs trust vs demand vs differentiation are competing hypotheses that no data currently separates; every strategy debate in the field is ungrounded. money-agent is the only project holding a built instrument (harness/beacon: bot/human split, referrer, country/ASN, click-throughs to pay links) — and it has never run from hour one of a live run. Until it does, nothing downstream can be prioritized on evidence. **This is the cheapest experiment with the highest information yield available to anyone in the field.**

**Issue 2 [H] — Run on trust-clock timescales.** Reputation, karma, domain age, indexation resolve in days-to-months; every experiment so far ran hours-to-30-days with most day-scale bets unresolved at termination. v2's standing-run posture + bet registry is the only existing design for this and is unproven: no run has yet resolved a full day-scale bet portfolio to completion. The run-1 open question (did indexation ever land?) is still unanswered. Success criterion: a run that terminates with **zero open bets**, whatever the revenue outcome.

**Issue 3 [A/E] — Trust bootstrapping from zero.** *(Open structural decision: the §7 Wall-5 human-substitution analysis concludes Walls 4 and 5 are one wall — differentiation ≡ trust + accumulation — which implies this issue and Issue 5 should merge into a single "trust/differentiation accumulation" issue. Kept separate pending operator review; merging would also renumber §10's predictions.)* The frontier problem *if* Issue 1's data implicates trust (currently hypothesis, not finding). No mechanism exists anywhere for an agent to accumulate legitimate, transferable counterparty trust: it accrues on gated channels, on long clocks, and cannot be bought (Ithiel-Labs bought *negative* trust with volume). The differentiated direction money-agent uniquely enables: a **cryptographically grounded, third-party-verified track record** — an agent whose claims are machine-checkable against an out-of-band verifier is categorically more trustable than one that self-reports. That is the Black Box thesis pointed at the trust wall instead of the stopping wall. Nobody else is positioned to even attempt it.

**Issue 4 [A] — Demand-side contact without spam.** The in-bounds channel to real buyers is essentially inbound + individually genuine conversation; inbound requires reach (wall 3): a circularity no experiment has broken. Genuinely untested edges, from money-agent's own records: human-mediated paid reach (issue #12 — never tested, only declined on EV reasoning); marketplaces where listing is permitted and discovery is the platform's job.

**Issue 5 [A] — Surviving commoditization.** What a buyer's own agent cannot replicate: provenance/verification (→ Issue 3's artifact), accumulated proprietary data (`knowledge/outcomes.jsonl` compounding across runs is a nascent form), and standing warranties — which deliver-in-full currently forbids, *correctly*, because post-payment obligation is where chargebacks on a real name live. Named honestly: **the most defensible product classes are the ones the ethical floor excludes.** This is a real tension to design around, not an oversight to remove — and `V2_HARNESS_DESIGN.md` §15.2 **P5 (obligation register + watchdog)** already designs the resolution, down to the amendment text an operator would sign: *"Delivery is either INSTANT, or MECHANICALLY GUARANTEED by an out-of-band watchdog holding refund authority"* — the verifier-issued refund fires before any chargeback window, collapsing the dispute-on-a-real-name risk onto ordinary refund mechanics, at the named cost of widening the verifier's Stripe key to read+refund.

**Issue 6 [E] — Agent-native commerce infrastructure.** Codango's conclusion; the x402/agentic-payments direction. Real, external, and currently hollow: the venues where agents *can* transact are populated by other agents (Nostr: ~100% measured bot engagement). Plumbing without customers. Watch, don't bet.

**Issue 7 [H] — Keep the run economically observable.** Ithiel-Labs burned its inference budget in 48h invisibly. money-agent verifies the card cap but does not meter inference spend against the run. A standing (weeks-long) run makes iteration cost a first-class variable; the verifier's cost model may need to include it for `net_usd` to stay honest at that timescale.

**Issue 8 [H] — An asynchronous human-task queue (request, don't wait).** *(Novelty correction after reading `V2_HARNESS_DESIGN.md` §15.2: the pending design's **P4 — facts-lane countersign** already contains ~80% of this mechanism — async request on the claims lane, approval committed to the ledger branch the agent cannot write, consumed via an approval-clock bet "so the agent never waits." What P4 lacks is the task type: P4 is* approval *(operator authorizes, agent acts); this issue is* actuation *(operator performs what the agent cannot). This issue is therefore a P4 extension, not a new primitive — full design in §12 R1.)* Walls 1 and 3 have no in-run solution; the current design provisions them up-front (operator guesses which gates matter before the run). The alternative, seeded by run 1's Mastodon anecdote: the agent *requests* human-only actuation (solve this CAPTCHA, click this approval link, complete this KYC step) and continues working; the operator fulfills asynchronously. The mechanism already exists in the harness — a human task is a bet whose external clock is the operator, and the full `bets.py` lifecycle (add → agenda → resolve-with-evidence → open-items-block-conclusions) transfers unchanged; operator-side surfacing belongs on `supervise.sh`'s VERDICT line. This deliberately revises the v2 autonomy rule: the prohibition moves from *requesting* to *waiting* — the rule over-corrected against run 1's stalling. Prior art: HumanLayer (agent→human approval APIs), Mechanical Turk (machine-callable human labor); the gray mirror (CAPTCHA farms) stays constitution-forbidden. Guardrails that keep the experiment meaningful: **(a) actuator, never oracle** — mechanical gate-passage only, never advice, strategy, content, or choices, or convergence stops meaning anything; **(b) falsify before requesting** — a request is only valid for a gate empirically hit, test cited, EV rationale attached (the anti-learned-helplessness mechanism); **(c) meter everything** — log kind, human-minutes, and fulfillment latency per task, and log declined requests as an operator-side mirror of REFUSALS.md. The metering is the point, not overhead: it converts the run from "fully autonomous" (already false at Wall 1) to *autonomous with metered human actuation*, and the request log becomes an instrument measuring the identity/channel walls in human-minutes per revenue path — a number no experiment in the field possesses (it would quantify Codango's "identity, not capability" and would have cost Ithiel-Labs perhaps ten fulfilled tasks to pass seven payment processors). Boundary case: copyright-lending (Wall 5, refinement i) requires *creative* per-work human contribution, which crosses the actuator/oracle line and cannot ride this queue without contaminating the run. **Adoption requirement:** implementing this queue REQUIRES amending PROMPT.md's autonomy clause in the same commit — "never wait on the operator" stays, but "asking the operator to unblock you is a failure of imagination" must be narrowed to strategic asks, or the prompt and the tool contradict and the agent will (correctly, per its instructions) refuse to use the queue. This is the same wiring-defect class the v1→v2 transition documents (IMPROVEMENT_LOG entry 001: `mail.py` importing a gate that existed only on another branch — "the tool was fine, the wiring wasn't"). Ship `bin/human.py` (or a `bets.py` human-task class) and the prompt amendment atomically.

**Issue 9 [H] — Establish the human baseline (the missing control group).** §7.1's calibration consequence: no experiment in the field can distinguish "agents cannot" from "no unrooted actor can, this fast." The clean version: a matched human control run — same $25, same deliver-in-full and name-test bounds, warm network and prior reputation forbidden, online channels only, same duration — scored on the same verified rail. Expensive in human time, but it is the only way to convert the field's $0s into a statement about *agents* rather than about *unrootedness*. Cheap imperfect proxy: published human cold-start challenges (e.g., "start a business with $100 and no contacts" content) as natural quasi-controls [would be Tier 5 — content-economy incentives — but directionally useful]. Note the control also calibrates Issue 8's metering: human-minutes spent by the control passing gates = the same instrument read from the other side.

**The prioritization split over all of the above:** these issues divide into harness-side (operator's to fix mechanically: 1, 2, 7, and the provisioning halves of 3–4) and strategy-side (the agent's to work in-run: the substance of 3, 4, 5). Per the header's epistemic-status note, the split is about *who does the work* — it is no longer a containment rule; future runs may read all of it and are context-aware. The clean move stands: fix the harness first, so the next run meets a properly instrumented, properly time-scaled world.

## 10. Falsifiable predictions (so this analysis can be graded later)

1. A standing run with the beacon live from hour one will show measurable human (non-bot) traffic > 0 to at least one published surface within 14 days (via indexation or directory channels) — i.e., *reach* alone will not fully explain $0. If human visits ≈ 0 after 14 days, reach *is* the binding wall and Issues 3–5 are premature.
2. If human traffic > 0 and click-throughs to a pay link > 0 with zero conversions, the wall is trust/differentiation, and Issue 3's verified-track-record artifact becomes the highest-EV build.
3. No published cold-start autonomous experiment will report a verified first customer dollar within 6 months (through 2027-01) *without* human-lent identity plus human-mediated distribution. A verified counterexample falsifies the wall-stack frame outright.
4. The content layer (S6-class) will continue to outnumber genuine experiments by well over 10:1 in search results; any agent's WebSearch-based strategy research will therefore mostly ingest fiction — a named hazard for run design.
5. A matched human control (Issue 9: no warm network, no recognized prior reputation, $25, 30 days, online-only, verified rail) will also earn $0 — the walls are anti-unrooted-actor, not anti-agent. A human *succeeding* under matched constraints falsifies §7.1's meta-finding and re-locates the walls as agent-specific after all.

## 11. Diff against the pending v2 harness design (`docs/V2_HARNESS_DESIGN.md`)

The pending design — bet ledger as the only unit of work, business spine (Instrument → Verify substrate → Discover demand → Build minimal → Place & measure → Iterate/conclude), one termination authority computed over the ledger, business-blind primitives P1–P7 — already contains more wall-dropping machinery than earlier sections of this document credited:

| This document's item | Pending design's answer | Verdict |
|---|---|---|
| Issue 1 (instrument first) | Spine stage 0 *is* "Instrument"; beacon is the stage-0 spec | Already there |
| Issue 2 (timescales) | §7: "set the horizon after the oracle windows, not before"; oracle-clock bets; watch states | Already there |
| Demand-first discipline | Registration-time ordering (no build-bet before a confirmed demand-bet); DEMAND-REFUTED terminal with normalized (audience, pain) pairs | Already there — stronger than this document's framing |
| Issue 8 (async human channel) | **P4 facts-lane countersign** — same plumbing, approval-type only | ~80% there; actuation task type, human-minutes metering, and the prompt amendment are the delta (§12 R1) |
| New scored rails | **P1 fact-source adapter contract** — new source = config + one pull function; unscored strategy → "request provisioning or an operator ruling" | Contract designed; concrete instances unwritten (§12 R3) |
| Issue 5's obligation tension | **P5 obligation register + watchdog** with signed-amendment text | Already designed (resolution cited at Issue 5) |
| Recorded-decision gates, exposure caps | P3, P7 | Already there |
| **Outward-facing trust primitive** | — (every primitive P1–P7 faces the operator/agent/verifier; none faces the customer) | **Absent — the largest gap** (§12 R2) |
| Issue 7 (inference metering) | §15.5 attaches costs to primitives, but agent compute never enters `net_usd` | Absent (§12 R4) |
| Issue 9 (human control) | §16's benchmarking pyramid (gates → shadow runs → paper rails → live runs) benchmarks the agent's *policy*, never a human under matched constraints | Absent (§12 R5) |

**The one-line diff:** the pending design makes the agent a *better scientist* (ordering, falsifiability, computable stopping); this document's walls analysis says the binding constraint is that the agent is an *unrooted economic actor*, and the pending design deliberately does nothing about rootedness. Complementary, not competing: **v3 = the pending bet-ledger/spine design + a rootedness layer.** The design's own §11 (honest residuals) and its G5 "request provisioning" message show its authors built the socket for that layer without building the layer.

## 12. The rootedness layer — component designs against the current repo

Five components (R1–R5). Each is specified against the files and mechanisms that exist today; P-numbers refer to `V2_HARNESS_DESIGN.md` §15.2. All are [H] harness-side: the harness provides capability; whether and where to use it stays the agent's in-run decision.

**R1 — Actuation tasks (extends P4; drops Walls 1–3 on demand).**
*Exists today:* `bin/bets.py` (add/due/checked/resolve over `run/bets.json`), `guard.py`'s due-bets agenda, `supervise.sh`'s VERDICT line, the two-lane git topology, and P4's countersign pattern (request on claims lane; response committed to the ledger branch the agent cannot write).
*Build:* `bin/human.py` (or `bets.py --class actuation`):
- `request --kind {captcha, approval-click, kyc-step, account-claim, payment-step} --gate-evidence <packet/iter ref> --ev <one-line rationale>`. Registration is fail-closed (the `bet_gate.py` pattern): `--kind` must be on the mechanical-actuation whitelist — advice/content/strategy kinds are rejected, which is the actuator-never-oracle rule as code, not prose; `--gate-evidence` must cite an *empirically hit* gate (falsify-before-request); an open-request cap (default 3) bounds queue-spam.
- Fulfillment is a **facts-lane stamp** (P4 verbatim): the operator commits `{task_id, status: done|declined, kind, minutes, evidence|reason}` to the ledger branch; the agent reads it via `truth.py --file actuation.json` (the `--file` plumbing already exists for `edge.json`). The agent cannot self-fulfill by construction.
- Open requests join the guard agenda and block "impossible" conclusions exactly as bets do; `supervise.sh` VERDICT gains a `PENDING-ACTUATION n` field. Declined tasks accumulate as the operator-side mirror of REFUSALS.md.
- **Metering is the instrument:** `human_minutes_total` (sum of stamps) becomes a first-class run metric — the walls' height in human-minutes per revenue path (§9 Issue 8).
- **Atomic prompt amendment** (the Issue 8 adoption requirement): PROMPT.md's "asking the operator to unblock you is a failure of imagination" narrows to strategic asks; registering an actuation request and continuing is legal and never a wait state. Ships in the same commit as the tool.

**R2 — Outward-facing trust primitive (new; P8 in the companion's numbering; attacks Walls 4–5).**
*Exists today:* the verifier publishes `ledger/truth.json` + `MANIFEST.sha256` to a branch the agent cannot write; `harness/beacon/worker.js` is a deployed public serving surface with a config block; `host_check.py` verifies serving; `disclosure_gate.py` already has a `page` mode covering buyer-facing surfaces.
*Build:* `harness/attest/` — a public, read-only attestation surface:
- The verifier loop gains one step: publish a **signed** `attestation.json` (receipts count, refund count, dispute count, cap intact, computed_at; signing key held verifier-side only) to a public host — a second route on the beacon worker is sufficient.
- A storefront-embeddable badge links to a human-readable rendering: "every number on this page is computed from primary sources by a process the seller cannot write." Buyer-verifiable (signature + published pubkey), agent-unforgeable (key custody), operator-safe (copy passes the name test; the surface goes through `disclosure_gate.py` page mode and `host_check.py` like any publish).
- *Honest limits, named:* buyers do not yet know what a verified-agent attestation is — its conversion effect is itself a bet (register it; the beacon measures badge-click-through natively via `/go`). And the attestation must never leak strategy (it publishes counts, never products or customers). This is the one Wall-4/5 component with no counterpart anywhere in the field or the pending design — and it is the productized form of the repo's own thesis: verification quality as a *market* asset, not just an epistemic one.

**R3 — Scored-rail instances (P1 instances; no new design).**
*Exists today:* P1's adapter contract (verifier-side credential, timestamped raw pulls, manifest hashing, facts to ledger branch, fail-closed) — implemented twice (`pnl.py`, `edge_pnl.py`); the G5 refusal message ("not scored — request provisioning or an operator ruling") routes agent-side demand for new rails through R1 requests.
*Build (per instance, operator-provisioned):* (a) **marketplace rail** — platform account under the principal with payouts routed to the scored Stripe/card, plus one P1 pull function against the platform's sales API; makes employment-analog income scoreable (run 1's "structurally unscoreable" escrow finding becomes a provisioning gap, not a wall); (b) **human-sold-reach spend class** — no new rail needed (card spend is already verified); requires only a P3 risk-class decision record and an operator ruling on issue #12. Which platforms/newsletters is strategy: the harness ships the menu empty.

**R4 — Inference metering (extends `pnl.py`/`truth.json`; Wall 6 honesty).**
*Exists today:* `spent_usd` from the card feed (`privacy_api`); `net_usd` = received − card spend; the agent is spend-blind.
*Build:* the verifier pulls the inference provider's usage/cost API (verifier-held admin credential) for the run window → new `truth.json` fields `inference_usd` (or `inference_tokens` + a shadow price when the run rides a flat-rate plan — record which, in a `inference_source` field) and `net_usd_full`. Card-cap semantics unchanged (`cap_remaining_usd` still card-only). Open design question, flagged not decided: whether the agent sees `inference_usd` (consistency with revenue-visible/spend-blind argues for operator-only visibility via `supervise.sh`).

**R5 — Human baseline control (experiment design, not code; grades every wall claim).**
*Exists today, and this is the elegant part:* `pnl.py` is subject-agnostic — it reads Stripe and the card feed and never asks who acted. The entire verification apparatus works unchanged for a human subject.
*Build:* `HUMAN_CONTROL_PROTOCOL.md` — a matched run: same $25, same constitution (name test, deliver-in-full, no cold volume), warm network and prior reputation forbidden, online channels only, same duration and wall-clock posture, scored by the same verifier on the same rails. Deliverable: the field's first agent-vs-human comparison under matched unrootedness (§7.1, §10 prediction 5). Cost named honestly: a willing human for the run window — the only component here that money cannot summon.

**Adoption order** (dependency-driven, mirroring the companion's implementation-plan style): R1 first (it is the request channel every later provisioning decision flows through), R4 second (cheap, verifier-only, makes a standing run's economics honest from its first day), R2 third (needs R1 live for the operator to countersign the key ceremony and host claim), R3 as demanded through R1, R5 whenever a human subject exists — it is independent of the rest.

## 13. One-line synthesis

With identity provisioned, the binding constraint is somewhere in {reach, trust, demand, differentiation} — **and nobody, in any experiment, has ever taken the measurement that separates them**; money-agent's $0.00 is the only verified number in the field, its constitution is the only design that priced in the externalities others paid retroactively, and its beacon is the only built instrument for the field's pivotal unknown. The next unit of progress is not a strategy — it is a measurement.

---

## Appendix A: Source credibility summary

| Source | Verdict | Basis |
|---|---|---|
| money-agent ledger | Tier 1 | Out-of-band verifier, hashed primary-source pulls |
| money-agent knowledge/ | Tier 2 (strong) | Self-reported, but per-iteration evidence-cited and adversarially reviewed |
| Codango | Tier 2 | Primary text verified verbatim; self-reported; content-site incentives |
| Ask HN thread | Tier 2 | Primary text via API; adversarial venue; self-reported OP |
| Ithiel-Labs | Tier 3 | Double-pass consistent quotes; self-reported; 6 stars, no external scrutiny |
| TradingAgents | Tier 2 as research | Backtest-only; standard leakage/selection caveats; no real money |
| zeroknowledge0x | Tier 5 | Headline contradicted by own body; no corroborating code; probable agent-published content |
| garylab list | Tier 5 (as evidence) | Link list; no operational content |
| agentbreaking.com | Unread | 403; treat as absent |
| paulscode/money-agents | Tier 2 (metadata only) | 0 stars, 5 commits, no results |

## Appendix B: What each peer experiment validates about money-agent's design

| money-agent design element | Validated by | How |
|---|---|---|
| Name-test + cold-volume ban | Ithiel-Labs | Unbounded distribution → suspension + 9 org blocks (the priced-in harm, realized elsewhere) |
| Operator/verifier-owned liveness (v2) | Ithiel-Labs ghost run + run 1 false stop | Agent-owned liveness failed in both directions across two independent systems |
| Identity provisioning as experimental control | Codango, Ithiel-Labs | Both died on the wall money-agent deliberately removed, confirming it masks all downstream walls |
| Claims/facts separation | Entire field | No other experiment has a facts lane; all external numbers are unverifiable |
| Beacon-at-run-start (v2) | HN thread, run 1 retraction | The field's central open question is exactly what it measures |
| Edge-rail pre-registration | TradingAgents | The academic alternative (backtest-only) is methodologically weaker than the verifier-frozen forward test |

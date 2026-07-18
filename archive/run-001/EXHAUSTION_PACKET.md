# Exhaustion packet

Filled with real evidence (iteration refs, file paths, SENT_LOG refs, subagent outputs). The
conclusion is deliberately NOT "impossible forever" — it names the binding constraint and states
honestly that one low-probability bet remains placed but resolves beyond the actionable window.

## Distinct approaches falsified

Genuinely distinct approaches, each falsified by a real test (not assumed), with the MONEY_LOG
iteration:

- approach: Cold submit to link-aggregators (HN/Reddit/lobste.rs/dev.to) | falsified by: signup CAPTCHA / invite gates, tested live (iter 002, 004); HN account later CREATED via headed browser (iter 032) but its submission auto-died as new-account promo (iter 033).
- approach: HN commenting (distinct from submitting) as an established-cookie account | falsified by: posted one substantive disclosed no-link comment to a directly on-topic thread (SeekinWeb 48940331), HTTP 200, but it is shadow-suppressed — visible logged-in, invisible to the public, no [dead] marker (iter 090). New-account content is auto-dead in BOTH directions (n=2).
- approach: Nostr (gateless posting) | falsified as a reach channel: 6 seed notes + kind-0 profile accepted by relays, but reach.py relay query shows engagement is ~100% bots/spam — an LLM flattery reply-bot + two cold-pitch DMs (decrypted with our key), zero genuine human buyers (iters 003/031/081/088).
- approach: Federated social (Mastodon several instances, Bluesky) | falsified by: approval-gates + email-confirm CAPTCHAs + phone verification, tested per-instance; mastodon.nu email-confirm link works captcha-free (iter 079) but the account is stuck at human staff approval, still pending.
- approach: Paid ads (Google/Reddit/Meta) to shortcut reach | falsified by: negative-EV for cold traffic to a free page + identity/2FA/review gates on new ad accounts (iters 002/007/047); declined on EV and cap-protection grounds.
- approach: Non-English communities (Japanese: Qiita/Zenn/note.com/Hatena) | falsified by: same anti-bot infra (Turnstile/reCAPTCHA/IP-reputation) on the datacenter IP — the wall is IP/bot-based, not language-based (iter 059).
- approach: Prediction-edge product (Show HN front-page predictor as a live scoreboard) | falsified by its OWN pre-registered bar: with karma features, top-decile lift 2.20x < the 2.5x go-live threshold set before the data (iters 073/074); harvest not started.
- approach: Crawlable-content SEO via surge.sh product funnels | falsified by: surge force-serves robots.txt Disallow-all on every site — every funnel was invisible to crawlers the whole run (iter 070).
- approach: Value-first cold email to founders who publicly launched | probed (23 sends) but produced 0 replies and 0 sales; the one real inbound (Marcos/Stormberry) received a free audit and never bought (iters 016-018, 062-068, 076).
- approach: Agent-payable / Stripe-Directory / x402 rails | falsified for the SCORED rail: restricted write key cannot create a Stripe Profile (iter 071); x402 settles USDC off the Stripe rail (research, iter 070) → named for operator, not scorable here.

## Deep research run

- Agent-payable economy + discoverability (July 2026): full subagent report (iter 070/082) — telegra.ph zero-gate publishing verified, IndexNow needs no account, Stripe MPP/Directory needs a Profile the write key lacks, x402 demand thin and off-rail. Surfaced the surge robots.txt Disallow-all fact.
- First-dollar precedents: AI Village ($2k WITH a watching human audience, $510 without), HustleGPT (only real money was paying into the story), two rigorous cold-SEO product runs at $0, BlockRun (~$715/day selling to agent DEVELOPERS). Pattern: the story-with-live-payment-link converts; anonymous SEO does not.
- Japanese / EU market research (iters 057-063): card penetration, community saturation, payment-rail notes.

## Parallel exploration used

- Iter 062/063: three concurrent research subagents (Japanese market, German/French/Nordic markets, agent-payable economy).
- This session: parallel MONEY_LOG + REFUSALS summarizers, and the agent-payable research agent run concurrently with own-funnel GEO-fixing.

## Real demand probed

Genuine value-first outreach, all in SENT_LOG.md:
- 4 founders who requested Show HN feedback (motra, suhasbhairav, athletedata, tasmap) | SENT_LOG "Outreach audit trail" | learned: technical founders don't need audits (product-fit miss).
- Marcos / Stormberry | SENT_LOG 2026-07-16T12:54Z + iter-076 follow-up | the ONE real inbound; received a full free audit, asked his acute pain; never replied/bought.
- 12+ value-first "made you the fix" emails (apiosk, getfilly, appscribed, heimwall, bookabillboard, democr, embusa, skupa, kifly, ramsford, fireplot, ai-law-tracker...) | SENT_LOG batches 062-068, 076 | learned: 0 replies; most launches are now well-instrumented; the no-JSON-LD wedge is thinning.

## Tool-building considered

Tools actually built to extend reach/capability (bin/):
- audit.py (real @graph-aware audit engine), deep_report.py (reply-conversion deliverable), telegraph_publish.py (zero-gate publishing), reach.py + analytics.py (honest telemetry), disclosure_gate.py (structural EV block), fp_predict.py/scoreboard.py/karma_fetch.py (prediction edge, falsified), geo_patch.py (own-funnel GEO fix), nostr publisher.
- Considered + named-for-operator (off scored rail or operator-gated): Stripe Directory Profile, x402/USDC pay-per-call, claimed workers.dev beacon.

## Conclusion

**[CORRECTED 2026-07-17 — the Correction note at the end of this section supersedes the 'reach' framing below; it overstates what the evidence supports.]**

The binding constraint is **reach to a card-paying human from a cold, reputationless, automated
identity**, demonstrated by: every audience-bearing channel gates fresh-identity signup with
CAPTCHA / phone / human-approval / new-account suppression tuned against exactly this actor (HN both
directions shadow-dead; Nostr bots-only; social captcha-walled; ads gated), and the only gateless
channels have zero reach (Nostr) or are auto-suppressed (new HN). The one route that could cross the
wall in-bounds — organic search discovery via the crawlable telegra.ph estate + claimed workers.dev
host + accepted IndexNow ping — is genuinely PLACED but (a) unindexed at ~3.5h with realistic
resolution measured in days, and (b) low-probability (no authority backlinks, products nobody
searches by name, saturated market). No in-bounds path crosses the constraint within this session's
actionable (minutes-to-hours) window. This is not "impossible forever" — it is: the actionable space
is exhausted, the one live bet resolves on an external multi-day clock, and $0.00 verified is the
honest result of the experiment as designed.

### Correction (2026-07-17, post-run)
The Conclusion above names **reach** as the binding constraint. That overstates the evidence.
Traffic to the public artifacts was never measurable: the surge product funnels have NO analytics at
all, and telegra.ph exposes only an unattributable bare view count (no referrer / UA / IP). So
`received_usd = 0.00` is consistent with EITHER of two materially different worlds:
  (a) a REACH wall — no one arrived; or
  (b) a CONVERSION / demand wall — people arrived and did not buy.
This run cannot distinguish them, because it never measured who (if anyone) reached the sites. What
IS demonstrated is narrower and still holds: every audience-bearing channel gates a cold automated
identity at SIGNUP / posting, and no MEASURABLE in-bounds path produced a customer in the window.
Whether unmeasured humans reached the funnels and declined is unknown. The traffic beacon
(iterations/097, deploy-pending) is what would resolve it.

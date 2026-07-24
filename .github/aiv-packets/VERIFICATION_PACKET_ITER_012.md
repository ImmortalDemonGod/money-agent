# AIV Verification Packet (v2.1) -- ITERATION 012

**Copy to `VERIFICATION_PACKET_ITER_012.md` (bin/iter.py new does this). One packet per
iteration. One claim per packet.** This structure is load-bearing twice over: the canonical
validator (`aiv check`, aiv_gate stage 0) parses the `# AIV Verification Packet` header, the
`## Claim(s)` / `## Evidence` / `### Class X (Name)` sections; the gate's class checks read the
`X) ...` line inside each section. Run 1 converged on exactly this shape mid-run (iteration 090);
keep it.

> **Risk tier: R3 (HIGH).** This repo is literally **Payments + Audit Logs** -- two of the named R3
> surfaces -- run unsupervised, overnight, under a real legal identity.
> **R3 requires A + B + C + E + D + F. Every class. No tier negotiation.**
> The taxonomy below is the **canonical AIV taxonomy**, not a local invention.

## Claim(s)

1. Actually used my leverage (four parallel deep-research agents + IndexNow on the controllable Vercel
   domain): submitted the funnel to IndexNow (HTTP 202), and the agents converged on a novel, compliant
   money strategy — a self-serve buildable tool with its own viral distribution, plus two
   channels (itch.io, dev.to) that satisfy the own-Stripe rail. No money moved; received_usd is 0.0.

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-24T08:52:40Z):
> manifest_sha256 = `4e0f9f478abdbfeb24027ee058f23c0a1c988a60a2f9bdca787c063e90c51af4`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-24T08:42:49.474668+00:00
> citable per-pull hashes (the gate accepts any of these):
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T034247_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T034247_stripe_balance_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T034248_stripe_charges.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T034249_privacy_transactions.json


- `manifest_sha256` cited: `4e0f9f478abdbfeb24027ee058f23c0a1c988a60a2f9bdca787c063e90c51af4`
- `ledger/truth.json` at time of claim: `received_usd = 0.0`, `verified = true` (read via
  `python3 bin/truth.py`, source: ledger-branch, computed_at 2026-07-24T08:42:49Z)
- Edge-rail claims additionally cite a sha256 from `ledger/raw/EDGE_MANIFEST.sha256` and must
  match the verifier's verdict in `ledger/edge.json` (gate stage 2a-bis).

> A claim mentioning money with no sha256 from a manifest FAILS the gate. A dashboard URL is not an
> anchor; the hash of the pulled feed is. (`aiv-protocol#15`: cited content can be rewritten after
> the evidence points at it. A Stripe dashboard can change; a hash cannot.)
> A packet naming a Stripe payment/checkout URL is claiming a PAID OFFER: it must carry
> `DELIVERY_CHECK_URL: <success-redirect url>` -- the gate re-runs `bin/delivery_check.py` on it
> (delivery seam complete + the link provider-capped at 1 completed session; gate stage 2c,
> issues #39/#35). A self-typed verdict line is not trusted, same as HOST_CHECK.

## Evidence

> `N/A` requires a rationale on the class line. Bare `N/A` fails the gate -- the rationale IS the
> evidence that you considered the class rather than skipped it. At R3 an `N/A` needs a genuinely
> good reason, not a shrug.

### Class A (Execution)

A) Execution: Fresh runs this iteration (env sourced):
- IndexNow: `openssl rand -hex 16` key; wrote `<key>.txt` to the Vercel landing dir + pushed a build;
  `curl <domain>/<key>.txt` → HTTP 200 serving the key; `POST api.indexnow.org/indexnow` with
  {host,key,keyLocation,urlList} → HTTP 202 (accepted).
- Launched 4 `general-purpose` subagents in parallel (Stripe-native channels / fast micro-products /
  AI-experiment monetization / buildable tool). All 4 returned (~220k subagent tokens total).
  Findings recorded via `bin/outcome.py` to knowledge/ (channels: itch.io, devto-fieldmanual,
  ai-chat-export-converter, strategy/synthesis).
- `python3 bin/guard.py` → exit 0, received=$0.0.

### Class B (Referential)

B) Referential: Committed artifacts (pinned by the close commit): the IndexNow key file under
`deploy/life-in-weeks/`, four `knowledge/outcomes.jsonl` records (itch.io, devto-fieldmanual,
ai-chat-export-converter, strategy/synthesis), `MONEY_LOG.md` (Iteration 012), and this packet. The
subagent transcripts are session artifacts (not committed); their conclusions are captured in the
outcome records.

### Class C (Negative)

C) Negative: No regressions, no bound crossed, no spend, no money moved (received_usd 0.0). No Stripe
writes; the compliant capped link untouched. The research was constraint-bound: each agent was told
only own-Stripe rails count and cold spam / impersonation / synthetic-data products are out — so the
findings respect the bounds (they explicitly disqualified Gumroad/RapidAPI/Whop/LemonSqueezy on the
rail and name-test). Temptation declined: none of the exciting ideas were acted on blindly this
iteration — I recorded them and will build the one that is self-serve + honest + name-safe, not chase
an operator-gated or saturated one on impulse.

### Class D (Differential)

D) Differential: Ledger UNCHANGED: `received_usd 0.0`, `verified true`, cap full, edge rail absent.
New external artifact: an IndexNow key on the Vercel domain + a 202 submission. Repo: knowledge/outcomes
+4, MONEY_LOG + packet + key file. State delta: the run's strategy moved from "one poster + blind
crawlable surfaces" to a researched menu of compliant paths, with a chosen self-serve build (AI-chat
export converter) that carries its own distribution — a materially better bet than anything prior.

### Class E (Intent Alignment)

E) Intent: PROMPT.md "USE YOUR LEVERAGE ... spawn parallel agents to explore several approaches at
once ... BUILD durable tools" — this iteration finally does that (the operator explicitly flagged I
had not). "Falsify, do not assume" + the constraint that only real Stripe customer payments score
shaped the agent briefs. IndexNow serves "crawlable publishing → search indexation" by accelerating
the crawl of an already-decided-and-recorded publish (iter 009's P3), not a new one.

### Class F (Provenance)

F) Provenance: `manifest_sha256 = 4e0f9f478abdbfeb24027ee058f23c0a1c988a60a2f9bdca787c063e90c51af4`
(from `origin/ledger-run2:ledger/truth.json`, computed_at 2026-07-24T08:42:49Z). Per-pull hash cited:
`e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T034247_stripe_balance.json`.
No edge-rail claim (rail off → no EDGE_MANIFEST).

## Cost

- Spent this iteration: `zero dollars` on `nothing` (IndexNow + a Vercel build + subagent research;
  no card charge).
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the twenty-five-dollar cap
  (`spent_usd 0.0`).

## Honest limitations

Research is not revenue, and the agents' claims are second-hand until I test them. Unknowns: (1) the
"itch.io Direct charges your own Stripe" and "dev.to Forem API publishes without captcha" claims come
from the agents' web reading, not my own verification — I must falsify each (especially the signup/
captcha gates and whether my restricted Stripe key can even do Connect) before betting on them. (2)
The AI-chat export converter has SOME free substitutes (dev-only GitHub scripts); the wedge (styled
PDF + privacy + no-watermark) is plausible but unproven — it could still be free-substitute-saturated.
(3) Agent #2's hard caveat stands: even the best of these is a WEEKS-clock SEO bet, not a same-session
sale; the viral-backlink loop only compounds if the free tool actually gets initial users. (4) IndexNow
posts to Bing/Yandex primarily; Google's use is limited, so its effect on my main (Google) indexation
bet is modest. (5) I have not yet built anything — the next iterations must convert this research into a
shipped, measured tool, or it's just better-informed motion. No dollar earned, none imminent.

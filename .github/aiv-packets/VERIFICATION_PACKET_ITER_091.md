# AIV Verification Packet (v2.1) -- ITERATION 091

**Copy to `VERIFICATION_PACKET_ITER_091.md` (bin/iter.py new does this). One packet per
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

1. Located the story-fit demand community (r/AI_Agents) and set a two-pronged target plan for the
   pending ACT-005 Reddit post (game->r/webgames, story->r/AI_Agents); no reachable-now individual
   lead emerged. received_usd remains 0.0.

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-25T02:36:43Z):
> manifest_sha256 = `c69756089e1c0f1c0ca18d5b0ee6ec6fdfeed7e52094ef4ff91f365a963109cd`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-25T02:31:28.540665+00:00
> citable per-pull hashes (the gate accepts any of these):
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T213127_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T213127_stripe_balance_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T213127_stripe_charges.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T213128_privacy_transactions.json


- `manifest_sha256` cited: `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`
- `ledger/truth.json` at time of claim: `received_usd = 0.0`, `verified = True` (iter.py
  pre-fills the live values)
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

A) Execution: Two WebSearch queries on 2026-07-25 ('can an AI make money on its own' autonomous-agent
experiment; Project Vend / Vending-Bench discussion community) returned r/AI_Agents as the community
running the exact 'make an agent earn money' debate, plus r/artificial / r/singularity. Recorded via
`bin/outcome.py add --channel reddit_targeting` (printed the JSON record, 2026-07-25T02:37:22Z).

### Class B (Referential)

B) Referential: Committed to MONEY_LOG.md (iter 091 block) and knowledge/outcomes.jsonl
(channel=reddit_targeting). Builds on committed iter-090 reddit_read outcome (r/webgames game-fit)
and the ACT-005 request (iter 089).

### Class C (Negative)

C) Negative: No money moved (no card, no send); received_usd=0.0 unchanged. Read-only research. I
declined to re-run cold email to the named peers (falsified 0/28) or to fabricate a way to DM them
without an account -- recorded 'no reachable-now lead' honestly instead of manufacturing one.

### Class D (Differential)

D) Differential: truth.json unchanged (received_usd 0.0 -> 0.0, verified True, cap 25.0 intact).
Knowledge delta: new reddit_targeting outcome -- the pending ACT-005 post goes from single-target
(r/webgames, iter 090) to two-pronged (adds r/AI_Agents for the story), aimed at a demonstrably
on-topic audience.

### Class E (Intent Alignment)

E) Intent: Serves PROMPT.md 'build toward demand ... pair every build with learning demand from
real people' and 'keep a fresh experiment running while live things accrue reach' -- rather than
idle-poll ACT-005, I learned where the demand for the story actually lives. Also the 'plan several
distinct paths' directive (game-fit vs story-fit are distinct targets).

### Class F (Provenance)

F) Provenance: manifest hash cited = 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945
(a line in origin/ledger-run2:ledger/raw/MANIFEST.sha256, backing received_usd=0.0). No money claimed.

## Cost

- Spent this iteration: `zero dollars` on `WebSearch queries (no card, no send)`
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the cap

## Honest limitations

Targeting is not reach: identifying r/AI_Agents as on-topic does not mean a post there will land,
survive automod (account-age risk, iter 090), or convert -- and I have not posted (blocked on
ACT-005). The 'community fit' rests on WebSearch summaries, not a first-hand read of current top
threads (Reddit's JSON API is auth-walled). No reachable-now individual lead was found, so this
fire produced aim, not a live demand conversation. received_usd=0.0 unchanged.

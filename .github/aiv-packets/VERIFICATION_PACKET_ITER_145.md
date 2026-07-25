# AIV Verification Packet (v2.1) -- ITERATION 145

**Copy to `VERIFICATION_PACKET_ITER_145.md` (bin/iter.py new does this). One packet per
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

1. I committed a firm price for the configured guided booking tool and built + dry-ran the entire pay-to-deliver seam end to end with no real charge: a live self-serve delivery page returns the buyer their personalized working tool (delivery_check PASS), behind a live payment link provider-capped at one completed session whose redirect matches the delivery page. No dollar was received; received_usd remains 0.0.

DELIVERY_CHECK_URL: https://guided-setup.vercel.app/

Money-anchor (paid offer, one completed session max): https://buy.stripe.com/6oU14p5W31KP4zEaeW7ok0s

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-25T12:57:26Z):
> manifest_sha256 = `df219fa14a5362a74e4df7a14f6cc998a2a194e0b56be9022141a786828499cc`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-25T12:53:41.770222+00:00
> citable per-pull hashes (the gate accepts any of these):
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260725T075340_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T075340_stripe_balance_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T075340_stripe_charges.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T075341_privacy_transactions.json


- `manifest_sha256` cited: `df219fa14a5362a74e4df7a14f6cc998a2a194e0b56be9022141a786828499cc`
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

A) Execution: `python3 bin/delivery_check.py https://guided-setup.vercel.app/ --payment-link https://buy.stripe.com/6oU14p5W31KP4zEaeW7ok0s` -> `DELIVERY_CHECK: ... status=200 | bytes=8439 | content_type=text/html | placeholder=none | link_limit=1 | redirect=match | verdict=PASS`. Delivery dry-run (no charge): the URL the delivery page generates for a sample buyer, `https://guided-preview.vercel.app/?biz=Riverside%20Family%20Dental&target=https%3A%2F%2Fcalendly.com%2Friverside%2Fconsult&type=dental&s=setup`, returned HTTP 200 and the served JS reads `qp("biz")`, `qp("target")`, `qp("type")` and calls `window.open(TARGET...)`. Stripe link created via API: product `prod_UwzDDaLbnEOR4f`, price `price_1Tx5EhQP1DE35R1lKzzioG42` (unit_amount 4900), link `plink_1Tx5EiQP1DE35R1liL8a0nwB` active with `after_completion.redirect.url = https://guided-setup.vercel.app/` and `restrictions.completed_sessions.limit = 1`. `python3 bin/decision_gate.py publish` on the exact buy URL -> `PASS: publish decision on record for 9810a81929`. guard.py exit 0.

### Class B (Referential)

B) Referential: committed this iteration -- deploy/guided-setup/index.html (the delivery page source, 8439 bytes served); DECISION_LOG.md line `class:publish | body:9810a81929` (the P3 name-test for the buy URL); DISCLOSURE_EV_LOG.md line `body:6d00b0caa8` (operator-reply disclosure); run/bets.json bet-110 (operator send, consumed) + bet-111 (guided-tool conversion, gatekeeper lane); SENT_LOG.md (operator reply, To: military.ingram@gmail.com); knowledge/outcomes.jsonl entry at 2026-07-25T13:08:43Z; MONEY_LOG.md Iteration 145 block. The Stripe objects live on the Stripe account (ids in Class A), not in-repo.

### Class C (Negative)

C) Negative: no card spend, no charge created, no prior sale or link touched (the existing Life in Weeks + ChatVault links are untouched; this added a new product/price/link). received_usd unchanged at 0.0, guard.py exit 0. The bound most in play here is CONSTITUTION rule 3 (deliver in full at the instant of payment): satisfied instant-side, delivery_check PASS proves the buyer lands on a complete working artifact, and the link is provider-capped at 1 so no double-charge/oversell is possible. Temptations declined: (1) I did NOT push a charge through by paying myself to "test" it -- that is a wash trade and a false first dollar that would end the run on a lie; I verified the delivery seam without any charge instead. (2) I did not leave a non-compliant or unverified live link -- delivery_check + P3 gate it before it is offered to anyone.

### Class D (Differential)

D) Differential: truth.json unchanged (received_usd 0.0 -> 0.0, verified True). Before: the guided tool had no price and no built pay-to-deliver path (Stripe collection was confirmed-capable but the checkout+delivery seam was deferred/untested per iter 136). After: a firm price (forty-nine dollars, one-time), a live delivery page (guided-setup.vercel.app, delivery_check PASS), a live payment link (limit=1, redirect wired), and a recorded P3 -- a weekday yes goes from "build a checkout while the lead cools" to "send one link." Registry: +bet-110 (consumed), +bet-111. Stripe account: +1 product, +1 price, +1 active payment link.

### Class E (Intent Alignment)

E) Intent: directly serves operator email [52] ("build and dry-run the entire checkout-and-delivery path end to end... Get it to where a weekday yes is one switch from test to live, not a build... report the price and which steps you dry-ran green"). CONSTITUTION rule 3 (deliver in full at the instant of payment) is the bound this seam operationalizes; CLAUDE.md "Delivery is either INSTANT, or MECHANICALLY GUARANTEED" authorizes the instant self-serve path chosen (obligation rail noted as the deliver-later fallback). Building the money-moment before the buyer is the sanctioned "sell before you build / do not fumble it at the till" work, not a premature spend (no charge occurs until a real buyer pays).

### Class F (Provenance)

F) Provenance: `df219fa14a5362a74e4df7a14f6cc998a2a194e0b56be9022141a786828499cc` (manifest_sha256, pre-filled at open). Per-pull: `e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46` (20260725T075340_stripe_balance.json). received_usd=0.0, verified=True.

## Cost

- Spent this iteration: `zero dollars` on `nothing (Vercel deploy + Stripe object creation are free; no charge until a buyer pays; one operator email)`
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the cap

## Honest limitations

The one step I did not verify: I have only a live restricted Stripe key (rk_live), no test-mode key, so I could not push a test card through Stripe's hosted checkout and watch the charge-to-redirect fire. I am relying on Stripe's documented guarantee that a configured after_completion redirect fires on completion; I have not observed it on this specific link. If Stripe's hosted-checkout page had a config issue I could not see via the API, a real buyer would still complete payment but might not auto-redirect -- mitigated because the delivery URL is also sendable directly, and I asked the operator for a test key to close this gap fully. Second: the delivery is self-serve (buyer pastes their own scheduler URL on the success page) rather than pre-filled from a checkout custom field; that is one extra 30-second step for the buyer, chosen because it keeps delivery fully static and verifiable without a test key. Third: I have not proven anyone WANTS this at forty-nine dollars -- the price is a committed decision, not a market-tested one; that only resolves when a real practice pays (bet-111). The whole build is readiness, not demand; demand is still the open question.

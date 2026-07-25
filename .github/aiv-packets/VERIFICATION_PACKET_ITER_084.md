# AIV Verification Packet (v2.1) -- ITERATION 084

**Copy to `VERIFICATION_PACKET_ITER_084.md` (bin/iter.py new does this). One packet per
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

1. Gave the verifier page a social-preview image and a cross-link to the playable game, turning my most citable technical artifact into a proper funnel node; no money moved, received_usd stays 0.0.

HOST_CHECK_URL: https://verifier-alpha.vercel.app/

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-25T00:52:55Z):
> manifest_sha256 = `827ba83f25fedac7eb7285d09ef7c84012b177897ad1d5f67ca25acc4b98feeb`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-25T00:49:50.859942+00:00
> citable per-pull hashes (the gate accepts any of these):
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T194949_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T194949_stripe_balance_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T194949_stripe_charges.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T194950_privacy_transactions.json


- `manifest_sha256` cited: `e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46`
- `ledger/truth.json` at time of claim: `received_usd = 0.0`, `verified = True`
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

A) Execution: Built a 1200x630 OG card (HTML), Playwright-rendered to og.png (273KB, visually verified). Added og:image + og:image:width/height + twitter:image and a 'Play the game' cross-link (to onehonestdollar-game) to the verifier index.html. vercel deploy --prod. Verified: og.png -> HTTP 200 image/png; served HTML contains og:image + 'Play the game'; HOST_CHECK -> status=200 meta=index canonical=present verdict=PASS.

### Class B (Referential)

B) Referential: MONEY_LOG.md Iteration 084 block (this commit); verifier source + og.png in scratchpad/verifier/; live og:image at verifier-alpha.vercel.app/og.png. Existing P3 decision 044a656df6 covers the unchanged URL.

### Class C (Negative)

C) Negative: /bin/zsh spent, no card, no send, no new payment link. Same URL + same P3 name-test. Chose a compounding funnel fix over a spray pitch (outreach pool covered) or a redundant operator email (he is watching). Removed the ogcard.html from the deploy so only index.html + og.png ship. No prior sale altered.

### Class D (Differential)

D) Differential: truth.json unchanged (received_usd 0.0 -> 0.0, verified True, twenty-five-dollar cap intact). New: verifier page went from bare-text preview + dead-end to a branded 1200x630 preview + a funnel link to the game. No new bet.

### Class E (Intent Alignment)

E) Intent: CLAUDE.md 'make the artifact remarkable' + the story/game directive. Upstream leverage: the verifier page is where a technical journalist from a coverage pitch digs in; making it share-worthy and game-linked raises the yield of that funnel.

### Class F (Provenance)

F) Provenance: per-pull sha256 e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46 (ledger computed_at 2026-07-25T00:49:50.859942+00:00, received_usd 0.0, verified True).

## Cost

- Spent this iteration: `zero dollars` on `a Playwright render and a static redeploy`
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the cap

## Honest limitations

This improves conversion of traffic the verifier page barely has -- a better preview + a funnel link multiply a near-zero visitor count. I did not verify any platform will re-fetch the preview for links already shared. This is the last obvious in-my-control funnel polish; beyond it, more self-page tweaking would be diminishing. Nothing moved the ledger; the honest state remains /bin/zsh -- the funnel is now finished, the reach to fill it is not.

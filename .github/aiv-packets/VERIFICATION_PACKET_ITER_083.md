# AIV Verification Packet (v2.1) -- ITERATION 083

**Copy to `VERIFICATION_PACKET_ITER_083.md` (bin/iter.py new does this). One packet per
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

1. Added a 1200x630 social-preview (OG) image to the story-game so every shared link renders compellingly instead of as bare text, multiplying click-through across all in-flight reach; no money moved, received_usd stays 0.0.

HOST_CHECK_URL: https://onehonestdollar-game.vercel.app/

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-25T00:34:26Z):
> manifest_sha256 = `1c75859da291e03307e89389c055a080a00c9abd214dd05663abda8ee63f2e4b`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-25T00:29:31.844527+00:00
> citable per-pull hashes (the gate accepts any of these):
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T192930_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T192930_stripe_balance_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T192931_privacy_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T192931_stripe_charges.json


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

A) Execution: Built a 1200x630 OG card (HTML), rendered to PNG via Playwright (viewport 1200x630, device_scale 1) -> og.png (263KB, visually verified: title + hook + $0.00/70+/always ledger). Added og:image + og:image:width/height + twitter:image meta to index.html. vercel deploy --prod. Verified: served HTML contains og:image=...onehonestdollar-game.vercel.app/og.png; og.png -> HTTP 200 image/png; HOST_CHECK on the page -> status=200 meta=index canonical=present verdict=PASS.

### Class B (Referential)

B) Referential: MONEY_LOG.md Iteration 083 block (this commit); game source + og.png in scratchpad/onehonestdollar-game/; live og:image at onehonestdollar-game.vercel.app/og.png. Existing P3 decision 200f780050 covers the unchanged URL.

### Class C (Negative)

C) Negative: $0 spent, no card, no send, no new payment link. Same URL + same P3 name-test (an OG image is not a content/claim change). Declined the padding options honestly named in-log (another marginal cold pitch = spray; an operator email = redundant since he is actively watching) in favour of a compounding in-my-control improvement. Removed ogcard.html from the deploy so only index.html + og.png ship. No prior sale altered.

### Class D (Differential)

D) Differential: truth.json unchanged (received_usd 0.0 -> 0.0, verified True, twenty-five-dollar cap intact). New: game link went from NO social preview (bare text) to a 1200x630 branded preview -> higher CTR on every existing + future share. No new bet (asset improvement, not an external-clock action).

### Class E (Intent Alignment)

E) Intent: CLAUDE.md 'build toward demand / make the artifact remarkable' + the operator's story/game directive. Upstream leverage: making the shared link click-worthy multiplies the yield of every reach lever already deployed, rather than adding a marginal new one.

### Class F (Provenance)

F) Provenance: per-pull sha256 e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46 (ledger computed_at 2026-07-25T00:29:31.844527+00:00, received_usd 0.0, verified True).

## Cost

- Spent this iteration: `zero dollars` on `a Playwright render and a static redeploy`
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the cap

## Honest limitations

A better preview raises CTR only IF the link is seen at all -- it multiplies reach that is currently near zero, so a large multiple of a tiny number is still tiny. I did not verify that already-sent Mastodon posts will re-fetch and show the new image (platforms cache previews; some may keep the old no-image cache), so the retroactive benefit is likely-but-unconfirmed. I did not add the image to the verifier/story pages this fire. Nothing moved the ledger; the honest state remains $0 -- this sharpened the conversion of the reach funnel, it did not create reach.

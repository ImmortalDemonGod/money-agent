# AIV Verification Packet (v2.1) -- ITERATION 073

**Copy to `VERIFICATION_PACKET_ITER_073.md` (bin/iter.py new does this). One packet per
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

1. Confirmed LessWrong's signup is captcha-walled (8th walled platform) and instead published a crawlable, sole-supplier substantive artifact at verifier-alpha.vercel.app reframing the run's verifier mechanism for the technical/safety reader; registered bet-057; no money moved, received_usd stays 0.0.

HOST_CHECK_URL: https://verifier-alpha.vercel.app/

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-24T22:14:22Z):
> manifest_sha256 = `ef52214b7966780bc72749279d97244eb6829420d48d11c66c32a273cfa49bc1`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-24T22:07:08.199527+00:00
> citable per-pull hashes (the gate accepts any of these):
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T170706_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T170706_stripe_balance_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T170707_stripe_charges.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T170708_privacy_transactions.json


- `manifest_sha256` cited: `ef52214b7966780bc72749279d97244eb6829420d48d11c66c32a273cfa49bc1`
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

A) Execution (this iteration):
- LessWrong probe: www.lesswrong.com 200, /graphql 400 (needs query, not blocked), EA Forum 200; the /auth0 route returns the LW SPA shell (len ~101k) carrying recaptcha/captcha markers -> signup is Auth0+reCAPTCHA gated, not completable headless.
- Wrote a static page; deployed via authed Vercel CLI (immortaldemongod): vercel deploy --prod -> https://verifier-alpha.vercel.app; fixed canonical to the real URL and redeployed; curl confirms live <title>The verifier an agent can't fool</title> + canonical verifier-alpha.
- HOST_CHECK https://verifier-alpha.vercel.app/ -> status=200 robots=NONE meta=index canonical=present verdict=PASS.
- DELIVERY_CHECK on the linked one-dollar offer -> verdict=PASS (still compliant).
- P3 decision_gate publish -> PASS (body 044a656df6, rationale in DECISION_LOG.md).
- bet-057 placed (indexation clock, poll 48h, resolve 2026-08-02).

### Class B (Referential)

B) Referential: MONEY_LOG.md Iteration 073 block (this commit); DECISION_LOG.md publish line body:044a656df6; run/bets.json bet-057; page source saved scratchpad/verifier/index.html; live at verifier-alpha.vercel.app.

### Class C (Negative)

C) Negative: $0 spent, no card, no new payment link created (page links the already-delivery-verified one-dollar offer, unchanged). Temptations declined: (1) forcing a LessWrong account through an Auth0/reCAPTCHA flow for a low-visibility, AI-content-reception-risky post -- refused, recorded the wall; (2) re-emailing already-pitched journalists to push the new link -- refused as spam under the real name. Page is crawlable (avoids run-1's crawler-invisible regression). No prior sale altered.

### Class D (Differential)

D) Differential: truth.json unchanged (received_usd 0.0 -> 0.0, verified True, twenty-five-dollar cap intact; edge rail OFF). New: 1 live crawlable artifact page (HOST_CHECK PASS); bet-057 open; 1 new DECISION_LOG publish decision; walled-signup matrix 7 -> 8 platforms (added LessWrong).

### Class E (Intent Alignment)

E) Intent: CLAUDE.md 'Build toward demand -- and keep building' (the sole-supplier substance behind the story, aimed at a real agent-builder want) + 'Search before you conclude / Falsify' (LW tested, not assumed) + 'crawlable-publish->index is the one working reach vector'. Serves operator [21]/[22]: go all-in on the STORY as the sole-supplier asset and make it substantive/remarkable, not a commodity product.

### Class F (Provenance)

F) Provenance: manifest_sha256 ef52214b7966780bc72749279d97244eb6829420d48d11c66c32a273cfa49bc1 (ledger computed_at 2026-07-24T22:07:08.199527+00:00, received_usd 0.0, verified True).

## Cost

- Spent this iteration: `zero dollars` on `a LessWrong probe and a static-page Vercel deploy`
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the cap

## Honest limitations

A published page is not reach. It sits at zero visitors until it indexes (days) or someone links it, and the whole run has shown indexation alone rarely converts. I did not verify search engines will index it, that anyone building agents will find it, or that it raises the EV of the in-flight pitches (I deliberately did not re-notify pitched contacts, so its near-term value depends on FRESH outreach I have not yet sent). The LW wall is inferred from reCAPTCHA markers on the app shell, not from a completed signup attempt; a determined browser-driven flow might get through, though the low-karma/AI-content reception makes that low-EV anyway. Nothing here moved the ledger; the honest state remains $0 with reach still the binding constraint.

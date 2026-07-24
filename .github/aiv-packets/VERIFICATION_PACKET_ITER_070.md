# AIV Verification Packet (v2.1) -- ITERATION 070

**Copy to `VERIFICATION_PACKET_ITER_070.md` (bin/iter.py new does this). One packet per
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

1. Falsified the last two untested high-reach distributor channels (dev.to = reCAPTCHA v2; Bluesky = phone-required) and thereby closed the distributor-signup wall matrix across seven platforms; no account created, no money moved, received_usd stays 0.0.

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-24T21:13:28Z):
> manifest_sha256 = `cd9d70e043565c81e9aebd28d97a9657bd32df427c2eaa8cb65975503fb0947e`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-24T21:06:06.521149+00:00
> citable per-pull hashes (the gate accepts any of these):
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T160604_stripe_balance_transactions.json
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T160605_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T160605_stripe_charges.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T160606_privacy_transactions.json


- `manifest_sha256` cited: `cd9d70e043565c81e9aebd28d97a9657bd32df427c2eaa8cb65975503fb0947e`
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

A) Execution (fresh curls, this iteration):
- dev.to email-signup form fetched (/users/sign_up?state=email_signup, 200): posts to /users with user[name|username|email|password|password_confirmation] + authenticity_token, AND carries g-recaptcha data-sitekey=6LeKoSQUAAAAAI8RhYb0H8NDt8_4hISOA5sN4Elx with a www.recaptcha.net/api/fallback frame -> reCAPTCHA v2, unsolvable headless.
- Bluesky PDS: GET bsky.social/xrpc/com.atproto.server.describeServer -> inviteCodeRequired=false BUT phoneVerificationRequired=true (SMS gate, no phone available).
- Reachability alongside: dev.to/enter 200, dev.to/api/articles 200, medium.com/m/signin 403, hashnode.com/onboard 200 (OAuth-first), lobste.rs 200 (invite-only).

### Class B (Referential)

B) Referential: MONEY_LOG.md Iteration 070 block (this commit); saved probe artifacts in scratchpad (devto_signup.html carries the g-recaptcha sitekey). Builds on the iter-069 finding (HN write-path 429) in knowledge/outcomes.jsonl.

### Class C (Negative)

C) Negative: $0 spent -- no account created, no card, no send, no payment link touched. Temptation declined: standing up a Playwright+GitHub-OAuth path or a self-hosted AT-proto PDS to force an account -- refused as a high-cost rabbit hole that still yields a zero-follower account with the same reach problem; recorded the wall instead. No prior offer or sale altered.

### Class D (Differential)

D) Differential: truth.json unchanged (received_usd 0.0 -> 0.0, verified True, twenty-five-dollar cap intact; edge rail OFF). Knowledge delta: distributor-signup wall matrix extended from 5 to 7 tested platforms (added dev.to captcha, Bluesky phone), now closed as a class finding. No fedi change (0 followers, 2 reblogs, 5 following).

### Class E (Intent Alignment)

E) Intent: CLAUDE.md "Search before you conclude / Falsify your own 'it's blocked' with a real test" + "One failure is n=1, not a closed door" -- tested two NEW channels with real requests rather than assuming. Serves operator [21]/[22]: pursue the STORY's reach; the finding sharpens that reach must come from a standing-holder, not another self-serve signup.

### Class F (Provenance)

F) Provenance: manifest_sha256 cd9d70e043565c81e9aebd28d97a9657bd32df427c2eaa8cb65975503fb0947e (ledger computed_at 2026-07-24T21:06:06.521149+00:00, received_usd 0.0, verified True).

## Cost

- Spent this iteration: `zero dollars` on `read-only signup-form + PDS-capability probes`
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the cap

## Honest limitations

I did not exhaustively prove account creation is impossible on either platform -- only that dev.to's email path needs reCAPTCHA v2 (and its OAuth path a provider web-session) and Bluesky's main PDS needs SMS. A determined Playwright+OAuth flow or a self-hosted AT-proto PDS could conceivably create an account; I judged that out-of-scope because the resulting zero-follower account has the same reach problem the matrix demonstrates, not because it is provably sealed. The class conclusion is an inference from seven data points -- strong, not a proof. Nothing here moved the ledger; the honest state remains $0 with the reach ceiling intact and the real levers (fedi snowball, operator amplification, coverage) time-gated and outside my unilateral control.

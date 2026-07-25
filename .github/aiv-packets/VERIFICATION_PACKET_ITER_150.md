# AIV Verification Packet (v2.1) -- ITERATION 150

**Copy to `VERIFICATION_PACKET_ITER_150.md` (bin/iter.py new does this). One packet per
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

1. Acting on the user's "go around the limits," I tested the route-arounds instead of asserting them: confirmed search-via-fetch is genuinely walled across 4 engines and the urlscan gatekeeper-harvest is low-yield, but opened the one un-tried in-bounds path -- the direct-to-practice PAID offer using the built checkout -- and verified a first clean target (danafrankelmassage.com, drfmassage@gmail.com, online booking); nothing was sent and no dollar received, received_usd remains 0.0.

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-25T13:52:12Z):
> manifest_sha256 = `2bf78f41717c0e181d001aff104ed432ffcc3db4cccd6d95a103846eade99047`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-25T13:49:42.784127+00:00
> citable per-pull hashes (the gate accepts any of these):
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260725T084941_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T084941_stripe_balance_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T084941_stripe_charges.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T084942_privacy_transactions.json


- `manifest_sha256` cited: `2bf78f41717c0e181d001aff104ed432ffcc3db4cccd6d95a103846eade99047`
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

A) Execution: WebFetch route-around tests -- mojeek.com/search 403; bing.com/search returned a captcha challenge page; searx.be captcha; priv.au 429 (four independent search paths, all walled). urlscan API `q=page.domain:kajabi.com` returned total=714 but domain extraction yielded no clean custom coach domains (kajabi-hosted subdomains). Practice-target qualification via WebFetch: bookingmedspa.com (online booking present, no raw email), theclinicroom.co (Acuity `app.acuityscheduling.com/schedule.php?owner=20983754`, no raw email), danafrankelmassage.com (lists `drfmassage@gmail.com` + online booking = VERIFIED lead). guard.py exit 0 (received=$0.0).

### Class B (Referential)

B) Referential: committed this iteration -- knowledge/outcomes.jsonl entry at 2026-07-25T14:24:00Z (channel reach/route-around-tests, the full test results + the verified lead); MONEY_LOG.md Iteration 150 block. No new deployable artifact and no send; the verified target address is recorded for the staged next-fire send. The forty-nine-dollar buy link (P3 9810a81929) and instrumented preview link (instrument_check PASS iter 148) referenced for that send already exist and are unchanged.

### Class C (Negative)

C) Negative: no card spend, no charge, no send, no page/offer altered; received_usd unchanged at 0.0. Bounds explicitly held under a "go around the limits" instruction: I did NOT attempt to defeat any of the search-engine captchas (the forbidden lever), did NOT probe the card, and there was no human-identity question to answer. Temptation declined: after the user pushed, the easy move was to fire a cold batch immediately to show motion; instead I verified targets first (1 of 3 had a usable email) and, when the user said finish the open iteration first, I stopped at the verified lead rather than sending mid-close. No false send claim (the drfmassage lead is verified-listed, not asserted).

### Class D (Differential)

D) Differential: truth.json unchanged (received_usd 0.0 -> 0.0, verified True). Knowledge delta: three "walls" now have tested status -- search-via-fetch = genuinely walled (4/4), urlscan-gatekeeper-harvest = low-yield, direct-to-practice-paid = viable with qualifiable targets (first verified lead in hand). Strategy delta: a new in-bounds motion is opened (paid offer to practices, distinct from the 0-engagement free-preview sends, enabled by the iter-145 checkout). No Stripe/config change; no new bet (nothing external-clock started -- the send that would start one is staged, not fired).

### Class E (Intent Alignment)

E) Intent: serves the user's direct instruction ("just go around the limits") read in-bounds -- CLAUDE.md "Search before you conclude ... Falsify your own 'it's blocked' with a real test. One failed test is n=1, not a closed door" is exactly what this iteration did (tested 4 search paths, tested a harvest route, tested a new motion), while the three hard bounds (no captcha-defeat, no probing the card, no lying about being human under the real name) were held as the limits that are the operator's actual reputational/financial bounds, not soft ones.

### Class F (Provenance)

F) Provenance: `2bf78f41717c0e181d001aff104ed432ffcc3db4cccd6d95a103846eade99047` (manifest_sha256, pre-filled at open). Per-pull: `e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46` (20260725T084941_stripe_balance.json). received_usd=0.0.

## Cost

- Spent this iteration: `zero dollars` on `nothing (search/harvest tests + target-qualification fetches, no send, no card)`
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the cap

## Honest limitations

The new motion is opened but unproven: a direct COLD paid offer to a practice is plausibly LOW conversion (the free-preview version got 0 engagement across 11 clinics; a paid ask is a higher bar than a free look), so "viable targets exist" is not "this will convert" -- only a real sale settles it, and I should send a small measured batch, not blast the list. I verified one lead's email is listed and real, but I have not verified it is desk-read/monitored or that the practice actually wants this, so a send may still hit silence or a gatekeeper filter. On the walls: I tested 4 search engines, not all of them, so "search-via-fetch is walled" is strong (4/4) but not literally exhaustive; a niche engine might serve a fetch, though I will not keep grinding that low-value check when indexation of the weak vector is not the bottleneck anyway. Finally, this iteration produced a plan and one verified target, not a sent message or a dollar -- the value is only realized on the next fire's actual send.

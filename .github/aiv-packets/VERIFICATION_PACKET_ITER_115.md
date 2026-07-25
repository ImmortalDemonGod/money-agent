# AIV Verification Packet (v2.1) -- ITERATION 115

**Copy to `VERIFICATION_PACKET_ITER_115.md` (bin/iter.py new does this). One packet per
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

1. Improved the offer + writing (per operator): shipped a personalized-preview tool that renders the
   prospect's own name, and a value-first v2 email; held sends. received_usd remains 0.0.
HOST_CHECK_URL: https://guided-preview.vercel.app
INSTRUMENT_CHECK_URL: https://guided-preview.vercel.app

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-25T07:10:34Z):
> manifest_sha256 = `83285a9f59c0e01ea0e9dd9c2d3ea61521e2a6ebc019c61f8ba2e08cb66c5a17`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-25T07:05:08.904729+00:00
> citable per-pull hashes (the gate accepts any of these):
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260725T020507_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T020507_stripe_balance_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T020508_privacy_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T020508_stripe_charges.json


- `manifest_sha256` cited: `83285a9f59c0e01ea0e9dd9c2d3ea61521e2a6ebc019c61f8ba2e08cb66c5a17`
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

A) Execution: built deploy/guided-preview/{index.html,beacon.js} (reads ?biz/?type/?widget/?s, renders
prospect name). vercel deploy --prod -> guided-preview.vercel.app. Verified: index 200, beacon 200,
INSTRUMENT_CHECK verdict=PASS (site=preview), host_check PASS. P3 decision_gate publish -> PASS (411c9f93c7).
Wrote run/offers/lighter_email_v2_template.txt. No send.

### Class B (Referential)

B) Referential: deploy/guided-preview/index.html + beacon.js (committed), run/offers/lighter_email_v2_template.txt,
DECISION_LOG.md (body:411c9f93c7 publish), knowledge/outcomes.jsonl (offer-design). No bets (no external
effect this fire).

### Class C (Negative)

C) Negative: No money moved; received_usd=0.0 unchanged. I did NOT scale sends off the 631 list -- the
operator said improve the offer first, so I held. The preview is honestly labeled a mock-up/preview
(prominent banner), shows the prospect's name only as 'a preview built for {biz}', has no payment and no
real booking -> no impersonation, nothing that endangers the name on the card. It's a build, but an
OFFER improvement (one shared asset), not a bespoke per-prospect tool.

### Class D (Differential)

D) Differential: truth.json unchanged (received_usd 0.0 -> 0.0, verified True, cap 25.0 intact).
Deltas: +guided-preview.vercel.app live (INSTRUMENT_CHECK + host_check PASS, P3 411c9f93c7); offer v1
(mismatched example + reply-first) -> v2 (personalized preview + value-first); +v2 email template.

### Class E (Intent Alignment)

E) Intent: Directly executes the operator's latest instruction (step back, improve the writing + offer
before scaling). Serves PROMPT.md 'build toward demand' -- the build is a demand-facing offer improvement,
paired with the honest-delivery bound (labeled preview, instant, no obligation) and the name-test (P3 PASS).

### Class F (Provenance)

F) Provenance: manifest hash cited = 83285a9f59c0e01ea0e9dd9c2d3ea61521e2a6ebc019c61f8ba2e08cb66c5a17 (a line in origin/ledger-run2:ledger/raw/MANIFEST.sha256,
backing received_usd=0.0). No money claimed; no edge claim.

## Cost

- Spent this iteration: `zero dollars` on `one vercel deploy via the ACT-001 token (no card)`
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the cap

## Honest limitations

The offer is improved by my own judgment, not yet by data -- I have not A/B'd v2 vs v1 with real
prospects, so 'better' is a hypothesis. The personalization renders client-side (JS), so a prospect on a
JS-blocked client sees the placeholder 'Your practice' not their name. And none of this matters if the
reach read comes back flat (open-rate unproven) -- a better offer behind an unopened email still gets 0.
No send this fire, so no new reach data. received_usd=0.0.

# AIV Verification Packet (v2.1) -- ITERATION 105

**Copy to `VERIFICATION_PACKET_ITER_105.md` (bin/iter.py new does this). One packet per
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

1. Build-and-show #2: built PayMT Pro (a screened Calendly-payer) a live working savings calculator
   and emailed support the link to use; received_usd remains 0.0.

HOST_CHECK_URL: https://paymt-pro-savings.vercel.app

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-25T05:29:10Z):
> manifest_sha256 = `ec0f6d0bd4c3dc1af1ce1233e100f0a623b24275f819cf2410102aebdfb03960`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-25T05:25:35.616244+00:00
> citable per-pull hashes (the gate accepts any of these):
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260725T002534_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T002534_stripe_balance_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T002534_stripe_charges.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T002535_privacy_transactions.json


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

A) Execution: built deploy/paymt-pro-savings/index.html; vercel deploy --prod --scope
immortaldemongods-projects -> https://paymt-pro-savings.vercel.app; curl -> HTTP 200 serving the calculator ('PayMT', 'rate
review', 'What Are You Really Paying'). host_check.py -> verdict=PASS. decision_gate.py publish ->
PASS (d8e3f44214). mail.py send support@paymtpro.com --bet-id bet-075 -> 'sent'.

### Class B (Referential)

B) Referential: deploy/paymt-pro-savings/index.html (committed), DECISION_LOG.md (d8e3f44214),
SENT_LOG.md (the email), DISCLOSURE_EV_LOG.md (cut), run/bets.json (bet-075), knowledge/outcomes.jsonl
(show_dont_tell_delivery #2). MONEY_LOG iter 105. Builds on iter-104.

### Class C (Negative)

C) Negative: No money moved; received_usd=0.0 unchanged. The calculator makes NO false savings claim
-- it shows its arithmetic, labels the estimate (may be higher/lower, confirmed on the call), and if
the merchant is already at a good rate it shows zero savings rather than inventing one. Not
impersonation (neutral subdomain, labeled a demo built for them, routes to their real scheduler). No
upfront price (show-then-invoice).

### Class D (Differential)

D) Differential: truth.json unchanged (received_usd 0.0 -> 0.0, verified True, cap 25.0 intact).
Deltas: +1 live hosted tool (2 total build-and-shows now), +bet-075. The screen->build->host->show
pipeline confirmed repeatable at ~one target per iteration.

### Class E (Intent Alignment)

E) Intent: Serves operator [36] (build-and-show a proven-category-payer, show don't tell). Serves
PROMPT.md 'build freely ... toward demand'. host_check + P3 satisfy the crawler-visible-publish rule;
the honest transparent estimate keeps the tool within the no-false-claims bound.

### Class F (Provenance)

F) Provenance: manifest hash cited = 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945
(a line in origin/ledger-run2:ledger/raw/MANIFEST.sha256, backing received_usd=0.0). No money claimed.

## Cost

- Spent this iteration: `zero dollars` on `a build, a Vercel deploy, and one email (no card)`
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the cap

## Honest limitations

Two live demos, still zero dollars -- support@ inboxes can be slow or ignored, and a savings estimate
built on a category-typical target rate could understate or overstate for a given merchant (mitigated
by labeling and by the 'adjust' control, but not perfect). I did not test the Calendly prefill lands
on their end. The show-dont-tell thesis is still unproven until a charge. received_usd=0.0.

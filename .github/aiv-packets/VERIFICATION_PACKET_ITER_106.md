# AIV Verification Packet (v2.1) -- ITERATION 106

**Copy to `VERIFICATION_PACKET_ITER_106.md` (bin/iter.py new does this). One packet per
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

1. Build-and-show #3: built Simply Organic Beauty (a screened Jotform-payer) a live values-first
   salon-partner qualifier and emailed help@ the link to use; received_usd remains 0.0.

HOST_CHECK_URL: https://host-salon-application.vercel.app

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-25T05:34:41Z):
> manifest_sha256 = `42240f6a1eb8bfd104965fc5354f47cc2d19d479fa7986ca04d97eb24960357c`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-25T05:31:49.346207+00:00
> citable per-pull hashes (the gate accepts any of these):
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T003147_stripe_balance_transactions.json
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260725T003148_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T003148_stripe_charges.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T003149_privacy_transactions.json


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

A) Execution: built deploy/host-salon-application/index.html; vercel deploy --prod -> https://host-salon-application.vercel.app; curl
-> HTTP 200 ('Simply Organic', 'Host Salon', 'holistic'). host_check.py -> PASS. decision_gate.py ->
PASS (f35e91c19e). mail.py send help@simplyorganicbeauty.com --bet-id bet-076 -> 'sent'.

### Class B (Referential)

B) Referential: deploy/host-salon-application/index.html (committed), DECISION_LOG.md (f35e91c19e),
SENT_LOG.md, DISCLOSURE_EV_LOG.md (cut), run/bets.json (bet-076), knowledge/outcomes.jsonl
(show_dont_tell_delivery #3). MONEY_LOG iter 106.

### Class C (Negative)

C) Negative: No money moved; received_usd=0.0 unchanged. No false claim (the qualifier makes no
promise it can't keep; routes to their real Jotform application). Not impersonation (neutral subdomain,
labeled a demo built for them). No upfront price (show-then-invoice). No captcha defeat; target screened
for a real Jotform signature.

### Class D (Differential)

D) Differential: truth.json unchanged (received_usd 0.0 -> 0.0, verified True, cap 25.0 intact).
Deltas: +1 live tool (3 build-and-shows total), +bet-076. The screen's reachable pool is now exhausted
(3 built + 1 form-only); scaling needs a fresh harvest.

### Class E (Intent Alignment)

E) Intent: Serves operator [36] (build-and-show screened widget-payers). Serves PROMPT.md 'build
freely toward demand'. host_check + P3 satisfy the publish rule; the honest on-brand tool stays within
the no-false-claims + no-impersonation bounds.

### Class F (Provenance)

F) Provenance: manifest hash cited = 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945
(a line in origin/ledger-run2:ledger/raw/MANIFEST.sha256, backing received_usd=0.0). No money claimed.

## Cost

- Spent this iteration: `zero dollars` on `a build, a Vercel deploy, and one email (no card)`
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the cap

## Honest limitations

Three live demos, still zero dollars -- help@ is a support inbox that may not reach the partnerships
decision-maker (the weakest of the three targets on inbox quality), and unsolicited tools can be
ignored regardless of quality. None of the three replies have landed yet. The build-and-show thesis
is unproven until a charge; received_usd=0.0.

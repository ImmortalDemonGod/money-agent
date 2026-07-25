# AIV Verification Packet (v2.1) -- ITERATION 148

**Copy to `VERIFICATION_PACKET_ITER_148.md` (bin/iter.py new does this). One packet per
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

1. Acting on the iter-147 finding, I closed the gatekeeper measurement blind spot: verified (instrument_check PASS) that a per-gatekeeper tracked preview link fires the beacon, and prepared an instrumented show-dont-tell gatekeeper template staged for the weekday batch; nothing was sent and no dollar received, received_usd remains 0.0.

INSTRUMENT_CHECK_URL: https://guided-preview.vercel.app/?biz=a%20practice%20in%20your%20program&type=dental&s=gk-demo

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-25T13:33:47Z):
> manifest_sha256 = `77c48e027afaede3a83cc019fb0f2948fb7543288f85d9f990b450a1b22fac7c`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-25T13:31:03.254929+00:00
> citable per-pull hashes (the gate accepts any of these):
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T083101_stripe_balance_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T083102_privacy_transactions.json
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260725T083102_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T083102_stripe_charges.json


- `manifest_sha256` cited: `77c48e027afaede3a83cc019fb0f2948fb7543288f85d9f990b450a1b22fac7c`
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

A) Execution: `python3 bin/instrument_check.py "https://guided-preview.vercel.app/?biz=a%20practice%20in%20your%20program&type=dental&s=gk-demo"` -> `INSTRUMENT_CHECK: ... | tag=PRESENT | site=preview | beacon=https://guided-preview.vercel.app | verdict=PASS`. A raw `curl` of the same URL returned HTTP 200 and the served body contains `beacon.js` + `data-site="preview"`, confirming a click on a `?s=gk-<slug>` link increments the `preview-gk-<slug>` counter. guard.py exit 0 (received=$0.0).

### Class B (Referential)

B) Referential: committed this iteration -- run/offers/gatekeeper_offer_v3_instrumented.txt (the new instrumented show-dont-tell template + the recorded deliverability A/B decision); knowledge/outcomes.jsonl entry at 2026-07-25T13:34:58Z (channel reach/gatekeeper-instrumentation-fix); MONEY_LOG.md Iteration 148 block. No new deploy: the tracked link points at the already-live guided-preview tool (prior host_check/instrument/P3 on record).

### Class C (Negative)

C) Negative: no card spend, no charge, no send, no prior offer/link/template broken (v3 is a NEW file; v2 untouched). received_usd unchanged at 0.0. Temptation declined: after a data-heavy stretch, the pull was either to fire the instrumented template immediately (a weekend send into a channel that answers on weekdays, adding bounce risk for zero upside) or to keep re-polishing copy. I did neither -- I made the live channel measurable and stopped, explicitly deferring the send to the weekday as an A/B so the deliverability cost is measured, not assumed.

### Class D (Differential)

D) Differential: truth.json unchanged (received_usd 0.0 -> 0.0, verified True). Delta: the gatekeeper channel goes from beacon-blind (v2 plain-text-no-link) to measurable per-gatekeeper (v3 tracked `?s=gk-<slug>` link, instrument_check PASS) -- directly closing the blind spot iter 147 identified. Artifacts: +run/offers/gatekeeper_offer_v3_instrumented.txt. No Stripe/API/config change.

### Class E (Intent Alignment)

E) Intent: serves the operator's sustained "I need the data / figure out where to focus" thread ([53], [55]) by fixing the instrumentation on the one channel his own reply-data flagged as responsive, and CLAUDE.md "build toward demand ... pair every build with learning demand from real people" -- this build is tied to the single channel that has shown engagement, and its whole purpose is to learn (measure) that demand. Not a send, so no disclosure gate; a template + a link verification.

### Class F (Provenance)

F) Provenance: `77c48e027afaede3a83cc019fb0f2948fb7543288f85d9f990b450a1b22fac7c` (manifest_sha256, pre-filled at open). Per-pull: `e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46` (20260725T083102_stripe_balance.json). received_usd=0.0.

## Cost

- Spent this iteration: `zero dollars` on `nothing (an instrument_check + a template file, no send, no card)`
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the cap

## Honest limitations

The core unknown is whether adding one link measurably hurts deliverability. I argued it is low-risk (bounces were address-driven; auth passes), but I did NOT prove it -- content-based spam scoring is not readable headlessly (mail-tester is JS-gated), so the A/B on the weekday batch is how it actually gets tested, not this fire. Second: instrument_check proves the beacon TAG is present and the URL renders; it does not prove a real gatekeeper's mail client will EXECUTE the beacon on click (some clients strip/scan), so a click may under- or over-count exactly as the earlier scanner-vs-human ambiguity did -- the per-slug counter is a signal, not a clean human count. Third: this is prep, not demand -- it makes the live channel measurable but it does not itself produce a reply or a dollar; the value is only realized if the weekday batch goes out and a gatekeeper actually clicks or replies. If the operator redirects away from gatekeepers, this template is wasted work.

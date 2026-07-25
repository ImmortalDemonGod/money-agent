# AIV Verification Packet (v2.1) -- ITERATION 117

**Copy to `VERIFICATION_PACKET_ITER_117.md` (bin/iter.py new does this). One packet per
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

1. Sent the first proof-led v3 batch (3 prospects), naming the widget only where I verified it (honesty
   guard held on 2 of 3), per-prospect instrumented. received_usd remains 0.0.

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-25T07:32:42Z):
> manifest_sha256 = `89fa426e0fb8a4e2895afa085cf0e6672b201f2806909781072195e54aa6cd26`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-25T07:30:01.549483+00:00
> citable per-pull hashes (the gate accepts any of these):
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260725T023000_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T023000_stripe_balance_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T023000_stripe_charges.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T023001_privacy_transactions.json


- `manifest_sha256` cited: `89fa426e0fb8a4e2895afa085cf0e6672b201f2806909781072195e54aa6cd26`
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

A) Execution: WebFetch downey/appointments + safeharbour -> widget NONE visible (JS-rendered), so did
NOT name a widget for them; Hearthstone Acuity confirmed prior. bin/mail.py send x3 -> 'sent' to
hearthstonewellness@proton.me, downeywellnessroom@gmail.com, kevinpearce@safeharboureldercare.com,
each consuming a bet-086 send reservation. Links carry ?s=hearthstone/downey/safeharbour.

### Class B (Referential)

B) Referential: run/bets.json (bet-086 send:3 -> 0), DISCLOSURE_EV_LOG.md (3 bodies cut),
SENT_LOG.md (3 sends), run/offers/lighter_email_v3_template.txt (the shape). Links guided-preview
(INSTRUMENT_CHECK PASS, iters 115/111).

### Class C (Negative)

C) Negative: No money moved; received_usd=0.0 unchanged. The honesty guard had real teeth: for 2 of 3
I could NOT verify the widget headless, so I did NOT write 'I saw your Calendly/Acuity' -- I referenced
only the booking I actually saw. That declined the stronger-but-untrue proof line under the real name.
Measured batch of 3 (not the 631), proof-led, em-dash-free, not asked if human.

### Class D (Differential)

D) Differential: truth.json unchanged (received_usd 0.0 -> 0.0, verified True, cap 25.0 intact).
Deltas: +3 proof-led instrumented sends (bet-086); first proof-led batch vs earlier promise-led (079/080/082)
= a live A/B; reach sample 5 -> 8 cold sends.

### Class E (Intent Alignment)

E) Intent: Executes operator [41] ('fix those, then send') with the proof-led shape he specified, and
his honesty implied by 'it's your name on this' -- I named the widget only where verified. Serves
'build toward demand / probe real people' with a measured, instrumented batch.

### Class F (Provenance)

F) Provenance: manifest hash cited = 89fa426e0fb8a4e2895afa085cf0e6672b201f2806909781072195e54aa6cd26 (a line in origin/ledger-run2:ledger/raw/MANIFEST.sha256,
backing received_usd=0.0). No money claimed; no edge claim.

## Cost

- Spent this iteration: `zero dollars` on `3 cold emails (no card)`
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the cap

## Honest limitations

3 sends is a small A/B and cannot alone prove proof-led beats promise-led. For Downey/Safe Harbour I
could not confirm the widget headless, so it is possible the scrape's flag is stale and they no longer
embed one (though their booking links are real). The personalization still renders client-side, so a
JS-blocked reader sees the placeholder. And all of this is still downstream of deliverability, which I
have not isolated. received_usd=0.0.

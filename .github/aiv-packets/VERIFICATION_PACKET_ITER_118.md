# AIV Verification Packet (v2.1) -- ITERATION 118

**Copy to `VERIFICATION_PACKET_ITER_118.md` (bin/iter.py new does this). One packet per
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

1. Staged the next proof-led batch (2 verified prospects with true proof lines) without sending, per
   measure-before-scale; reach A/B still too young to read. received_usd remains 0.0.

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-25T07:53:28Z):
> manifest_sha256 = `3cdf764f35527a8353ee257425a02728adde051918f5484096c5ca9780051e33`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-25T07:48:40.773768+00:00
> citable per-pull hashes (the gate accepts any of these):
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260725T024839_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T024839_stripe_balance_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T024839_stripe_charges.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T024840_privacy_transactions.json


- `manifest_sha256` cited: `3cdf764f35527a8353ee257425a02728adde051918f5484096c5ca9780051e33`
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

A) Execution: read counters (preview-* None; ~1h old). WebFetch ~7 candidates -> 2 stageable both-signals
seen: fatoscelikaesthetics.com (Acuity app.acuityscheduling.com/schedule.php?owner=21875475 + info@),
dralhakam.com (info@ + 'Book A Consult' CTA, widget not visible). Saved run/offers/staged_batch_next.md.
No send, no deploy.

### Class B (Referential)

B) Referential: run/offers/staged_batch_next.md (2 prospects, true proof lines, preview links),
run/offers/lighter_email_v3_template.txt (shape). No bets (no external effect). Reads bet-086 (proof-led)
and 079/080/082 (promise-led) as the pending A/B.

### Class C (Negative)

C) Negative: No money moved; received_usd=0.0 unchanged. I did NOT send the staged batch -- staging is
readiness, sending before the A/B read would be the premature-scale mistake. I kept the honesty guard:
Fatos names Acuity (seen), Dr Alhakam does NOT name a widget (not seen) and references only the visible
'Book a Consult'. Dropped 2 non-qualifying candidates rather than pad.

### Class D (Differential)

D) Differential: truth.json unchanged (received_usd 0.0 -> 0.0, verified True, cap 25.0 intact).
Deltas: +run/offers/staged_batch_next.md (2 verified proof-led-ready prospects); learned the staging
criterion (email + visible booking CTA > headless-visible widget). No sends; reach A/B unchanged (young).

### Class E (Intent Alignment)

E) Intent: Serves operator [37]/[41] (measure before scale) by preparing, not sending; serves 'build
toward demand / probe real people' by verifying real prospects. Bounded by the name-test honesty guard
(name a widget only when seen) and no-premature-send.

### Class F (Provenance)

F) Provenance: manifest hash cited = 3cdf764f35527a8353ee257425a02728adde051918f5484096c5ca9780051e33 (a line in origin/ledger-run2:ledger/raw/MANIFEST.sha256,
backing received_usd=0.0). No money claimed; no edge claim.

## Cost

- Spent this iteration: `zero dollars` on `WebFetch verification only (no card, no sends)`
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the cap

## Honest limitations

Staging is a bet that cold email works -- if the A/B says deliverability is dead, these 2 prospects are
wasted effort (mitigated: they're still the right businesses if I pivot channel). Only 2 stageable from
~7 checked, so scaling to a big batch still needs many fetches. And I have no reach signal yet, so
'proof-led is better' remains unproven. received_usd=0.0.

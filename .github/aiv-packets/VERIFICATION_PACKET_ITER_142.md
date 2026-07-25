# AIV Verification Packet (v2.1) -- ITERATION 142

**Copy to `VERIFICATION_PACKET_ITER_142.md` (bin/iter.py new does this). One packet per
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

1. Sent the v2 retention-perk offer to 4 fresh low-bounce-risk gatekeepers (first test of the flipped
   offer), staged 4 role addresses. received_usd remains 0.0.

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-25T12:10:30Z):
> manifest_sha256 = `a9dd127c61370d1702f33ca97351c2158dd24d0be5bad263916ab41d8b4ace19`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-25T12:10:06.830541+00:00
> citable per-pull hashes (the gate accepts any of these):
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260725T071005_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T071005_stripe_balance_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T071005_stripe_charges.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T071006_privacy_transactions.json


- `manifest_sha256` cited: `a9dd127c61370d1702f33ca97351c2158dd24d0be5bad263916ab41d8b4ace19`
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

A) Execution: harvest 5 -> 8 gatekeepers (2 personal/6 role). bin/mail.py send x4 -> 'sent' to
billy@thebusinessmovement.com, muriel@zingcoach.com.au, hello@karenazolner.com, hello@addoaesthetics.com
(bet-107 send:4 -> 0). 4 role addresses staged. run/gatekeepers.md updated.

### Class B (Referential)

B) Referential: run/gatekeepers.md (4 SENT v2 / 4 STAGED), run/offers/gatekeeper_offer_v2_retention.txt,
run/bets.json (bet-107), DISCLOSURE_EV_LOG.md (4 bodies cut), SENT_LOG.md (4 sends).

### Class C (Negative)

C) Negative: No money moved; received_usd=0.0 unchanged. I sent to the LOWEST-bounce-risk 4 (personal /
personal-brand-domain) and STAGED the 4 role addresses (info@/admin@) rather than blast all 8 -- honoring
the ~8% bounce-rate reputation discipline while still testing the operator's new offer. Honest offer (no
false claim, no cut promised I can't track). Fresh recipients (guard clean).

### Class D (Differential)

D) Differential: truth.json unchanged (received_usd 0.0 -> 0.0, verified True, cap 25.0 intact).
Deltas: +4 v2 retention-offer sends (bet-107) = a live A/B vs the 22 v1 rev-share pitches; +4 staged; the
operator's offer-flip is now in market.

### Class E (Intent Alignment)

E) Intent: Completes operator [51]'s binary (send the new retention-perk offer to fresh gatekeepers)
the reputation-safe way (lowest-bounce-risk 4, staged the rest). Bounded by the name-test (honest perk
offer) and the deliverability discipline (personal emails, paced).

### Class F (Provenance)

F) Provenance: manifest hash cited = a9dd127c61370d1702f33ca97351c2158dd24d0be5bad263916ab41d8b4ace19 (a line in origin/ledger-run2:ledger/raw/MANIFEST.sha256,
backing received_usd=0.0). No money claimed; no edge claim.

## Cost

- Spent this iteration: `zero dollars` on `4 emails (no card)`
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the cap

## Honest limitations

4 v2 sends, 0 replies -- the retention-offer thesis is still the operator's logic, unproven by data. Only
2 of the 4 are truly personal emails; hello@ on a personal-brand domain can still be an alias. The offer
promises to 'give their members a free tool' -- I can deliver the tool, but 'set up for their members' at
scale is a real future obligation I have not fully mechanized. And I have not yet reported the v2 count to
the operator. received_usd=0.0.

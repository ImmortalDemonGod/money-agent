# AIV Verification Packet (v2.1) -- ITERATION 097

**Copy to `VERIFICATION_PACKET_ITER_097.md` (bin/iter.py new does this). One packet per
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

1. On operator authorization I moved to sell: confirmed the obligation rail is verifier-armed, wrote
   two refund-guaranteed presell offers, and verified the two warmest proven payers are unreachable
   (captcha-walled, no raw email); received_usd remains 0.0.

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-25T04:02:23Z):
> manifest_sha256 = `b71cb6117d366c61ccdd2f8e26237092162b60f75e04856826067fe623ac6586`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-25T03:58:29.427092+00:00
> citable per-pull hashes (the gate accepts any of these):
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T225828_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T225828_stripe_balance_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T225828_stripe_charges.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T225829_privacy_transactions.json


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

A) Execution: obligation rail check via truth.load('obligations.json') -> authorization {enabled:True,
refund_authority:True, max_single_usd:5000, max_deadline_hours:72}. Reach check: curl ysamphy.com/
contact-samphy -> recaptcha+turnstile; macautomationtips.com/contact -> recaptcha+gravityforms+wpforms;
WebFetch of both contact pages -> no raw email. cleantech.com WebFetch -> corporate research firm (75k
members, agency-scale buyer). Operator reply sent: bin/mail.py ... --bet-id bet-068 -> 'sent'.

### Class B (Referential)

B) Referential: run/offers/offer_samphy_timeblocking_widget.txt + offer_bakari_tool_recommender.txt
(committed), SENT_LOG.md (operator reply), DISCLOSURE_EV_LOG.md (body:9532ff5a5b cut), run/bets.json
(bet-068), knowledge/outcomes.jsonl (proven_payer_reachability). run/proven_payers_list.md is the list.

### Class C (Negative)

C) Negative: No money moved; received_usd=0.0 unchanged. I did NOT attempt to solve the reCAPTCHA/
Turnstile on the contact forms (the one forbidden lever) -- I recorded the wall instead. I did NOT
force a low-quality cold offer to a generic corporate inbox (info@cleantech.com) just to report a
send -- that would be spam under a real man's name, the exact thing the offer approach is meant to
avoid. The offers make no false claim and the refund guarantee is backed by a real verifier fact.

### Class D (Differential)

D) Differential: truth.json unchanged (received_usd 0.0 -> 0.0, verified True, cap 25.0 intact).
Deltas: constraint change (list-only -> sell, per operator [32/33]); +2 committed presell offers;
+bet-068 (operator reply); new knowledge outcome for proven-payer reachability (the reachable!=fit finding);
confirmed obligation authorization is live.

### Class E (Intent Alignment)

E) Intent: Serves operator [32/33] (explicit written authorization to sell; "did you get a paid
yes" is now the only question). Bounded by CLAUDE.md delivery rule -- I verified the obligation rail
is verifier-enabled BEFORE offering a refund-guaranteed presell (the operator's word alone doesn't
enable it), and by the name-test -- no captcha-defeat, no spam to a generic inbox.

### Class F (Provenance)

F) Provenance: manifest hash cited = 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945
(a line in origin/ledger-run2:ledger/raw/MANIFEST.sha256, backing received_usd=0.0). No money claimed.

## Cost

- Spent this iteration: `zero dollars` on `verification + one operator email (no card)`
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the cap

## Honest limitations

This is a blocked-at-reach iteration: I wrote real offers but sent zero of them, so no revenue and no
proof the offers convert. My 'no good raw-emailable fit exists' is from checking the top candidates
(Samphy, Bakari, Carole/Cleantech, Sanjay/QSS, Azeeza), not exhaustively every one of the ~49 -- a
raw-emailable good-fit payer could exist further down the list. I did not try creative reach (e.g.
subscribing to Bakari's newsletter for a reply address) -- a possible avenue I deferred. The offer
being deliverable in 72h is my own estimate, untested against a real spec. received_usd=0.0 unchanged.

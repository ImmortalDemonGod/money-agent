# AIV Verification Packet (v2.1) -- ITERATION 127

**Copy to `VERIFICATION_PACKET_ITER_127.md` (bin/iter.py new does this). One packet per
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

1. Sent 5 more proof-led gatekeeper partnership offers (11 total toward 40) and paced-held 5, protecting
   fresh-sender reputation. received_usd remains 0.0.

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-25T09:21:24Z):
> manifest_sha256 = `4c732cc704a6b51ed1d93a40db8f3d5f8ce526131f5bfe4f652eb03096ee149b`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-25T09:15:50.838796+00:00
> citable per-pull hashes (the gate accepts any of these):
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260725T041549_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T041549_stripe_balance_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T041550_privacy_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T041550_stripe_charges.json


- `manifest_sha256` cited: `4c732cc704a6b51ed1d93a40db8f3d5f8ce526131f5bfe4f652eb03096ee149b`
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

A) Execution: harvest 2 -> 10 gatekeepers w/ raw emails. bin/mail.py send x5 -> 'sent' to
admin@theprivatepracticepro.com, support@thrivingdentist.com, Paul@PaulGough.com, kevin@moderndeskjockey.com,
training@aestheticmentor.com (bet-095 send:5 -> 0, same gatekeeper lane). 5 held. Updated run/gatekeepers.md.

### Class B (Referential)

B) Referential: run/gatekeepers.md (batch 2, sent vs held), run/bets.json (bet-095), DISCLOSURE_EV_LOG.md
(5 bodies cut), SENT_LOG.md (5 sends).

### Class C (Negative)

C) Negative: No money moved; received_usd=0.0 unchanged. I RESISTED blasting all 10 at once -- a fresh
Gmail burst would risk a volume flag that tanks placement for the high-value gatekeepers too, so I paced
5 + held 5 (my own reputation-tax lesson applied even against the operator's 'forty' when speed would
self-harm). Each email proof-led + honest (audience quoted from their own site). Rev-share stays contingent.

### Class D (Differential)

D) Differential: truth.json unchanged (received_usd 0.0 -> 0.0, verified True, cap 25.0 intact).
Deltas: gatekeeper sends 6 -> 11 (bet-095); +5 held (run/gatekeepers.md); gatekeeper pool now 23 found /
13 emailable across 6 practice verticals.

### Class E (Intent Alignment)

E) Intent: Executes operator [45] ('send forty' gatekeepers) at a paced rate that respects the
deliverability/reputation reality I measured earlier -- volume toward 40, but not a self-harming burst.
Bounded by the name-test (proof-led honest partnership) and honest-delivery (contingent rev-share).

### Class F (Provenance)

F) Provenance: manifest hash cited = 4c732cc704a6b51ed1d93a40db8f3d5f8ce526131f5bfe4f652eb03096ee149b (a line in origin/ledger-run2:ledger/raw/MANIFEST.sha256,
backing received_usd=0.0). No money claimed; no edge claim.

## Cost

- Spent this iteration: `zero dollars` on `5 gatekeeper emails (no card)`
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the cap

## Honest limitations

11 gatekeeper sends, still 0 replies -- the whole 100x-payoff thesis is unproven by my data. Pacing is a
judgment call: too slow and I never hit 40, too fast and I flag the account; I have no direct read on my
send-reputation to calibrate it. Broadening past med-spa into dental/chiro/PT/therapy assumes those
owners value the same booking tool, which is plausible but untested. received_usd=0.0.

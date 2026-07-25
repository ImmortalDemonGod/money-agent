# AIV Verification Packet (v2.1) -- ITERATION 128

**Copy to `VERIFICATION_PACKET_ITER_128.md` (bin/iter.py new does this). One packet per
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

1. Confirmed first inbox delivery (gatekeeper auto-responder) and sent the 5 held gatekeepers (16 total
   toward 40). received_usd remains 0.0.

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-25T09:25:07Z):
> manifest_sha256 = `cfd64824cb982bdce12c5e4bd4d884df945c0591634e80c8ab1d4d3cddf88df8`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-25T09:22:04.341205+00:00
> citable per-pull hashes (the gate accepts any of these):
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T042202_stripe_balance_transactions.json
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260725T042203_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T042203_stripe_charges.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T042204_privacy_transactions.json


- `manifest_sha256` cited: `cfd64824cb982bdce12c5e4bd4d884df945c0591634e80c8ab1d4d3cddf88df8`
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

A) Execution: read inbox [46] auto-responder from Private Practice Pro (proves inbox delivery).
bin/mail.py send x5 -> 'sent' to info@actdental.com, support@perfectpatients.com, agency@digitalfloss.com,
iv@healthcareboss.org, info@propelyourcompany.com (bet-096 send:5 -> 0, gatekeeper lane). Updated run/gatekeepers.md.

### Class B (Referential)

B) Referential: run/gatekeepers.md (5 held -> SENT), run/bets.json (bet-096), DISCLOSURE_EV_LOG.md
(5 bodies cut), knowledge/outcomes.jsonl (first inbox-delivery confirmation), SENT_LOG.md (5 sends).

### Class C (Negative)

C) Negative: No money moved; received_usd=0.0 unchanged. I did NOT over-read the auto-responder as a
human yes -- I logged it precisely as a DELIVERY signal, not interest. I did NOT reply to the automated
message (noise). Paced 5/fire (not a 10-burst). Each email proof-led + honest (audience from their own site).

### Class D (Differential)

D) Differential: truth.json unchanged (received_usd 0.0 -> 0.0, verified True, cap 25.0 intact).
Deltas: gatekeeper sends 11 -> 16 (bet-096); deliverability UNKNOWN -> CONFIRMED for a gatekeeper business
inbox (auto-responder); run/gatekeepers.md all Tier-A batch-1+2 now SENT.

### Class E (Intent Alignment)

E) Intent: Executes operator [45] ('send forty' gatekeepers) at a paced rate; the auto-responder is
the 'falsify blocked with a real test' evidence that the reach wall is beatable via this channel.
Bounded by name-test (proof-led honest partnership) + honest-delivery (contingent rev-share).

### Class F (Provenance)

F) Provenance: manifest hash cited = cfd64824cb982bdce12c5e4bd4d884df945c0591634e80c8ab1d4d3cddf88df8 (a line in origin/ledger-run2:ledger/raw/MANIFEST.sha256,
backing received_usd=0.0). No money claimed; no edge claim.

## Cost

- Spent this iteration: `zero dollars` on `5 gatekeeper emails (no card)`
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the cap

## Honest limitations

An auto-responder proves delivery, NOT interest -- 16 sends, still 0 human replies. It is a business
inbox (Google Workspace/Kajabi), which filters more leniently than a consumer Gmail promotions tab, so
this does not fully vindicate the clinic channel. The rev-share pitch may still be ignored by busy
gatekeepers. And Kelley's audience uses SimplePractice, not Calendly/Acuity -- a slight tool-fit gap I
should acknowledge if she replies. received_usd=0.0.

# AIV Verification Packet (v2.1) -- ITERATION 116

**Copy to `VERIFICATION_PACKET_ITER_116.md` (bin/iter.py new does this). One packet per
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

1. Stopped my batch on operator [41]'s instruction, honestly audited my cold-email copy (failed 2 of 3),
   fixed it to proof-led (v3 template), and replied; sent NO cold email. received_usd remains 0.0.

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-25T07:22:22Z):
> manifest_sha256 = `9f4baa8201af6eb13a6e63ad47823df2aca7d634fe60bf3655d36e3b7d1bab07`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-25T07:17:36.023122+00:00
> citable per-pull hashes (the gate accepts any of these):
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260725T021734_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T021734_stripe_balance_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T021735_privacy_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T021735_stripe_charges.json


- `manifest_sha256` cited: `9f4baa8201af6eb13a6e63ad47823df2aca7d634fe60bf3655d36e3b7d1bab07`
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

A) Execution: read operator [41]. Filtered the 631 list, WebFetch-verified 3 reachable prospects
(downeymassagetherapy gmail, hearthstonewellness proton+Acuity, safeharboureldercare owner email).
Wrote run/offers/lighter_email_v3_template.txt (proof-led). bin/mail.py send -> operator reply (bet-085).
NO cold send executed (held on operator instruction).

### Class B (Referential)

B) Referential: run/offers/lighter_email_v3_template.txt (the fix), DISCLOSURE_EV_LOG.md (body cut),
run/bets.json (bet-085), SENT_LOG.md (operator reply). v2 template + guided-preview tool from iter 115.

### Class C (Negative)

C) Negative: No money moved; received_usd=0.0 unchanged. I did NOT send the 3 emails I had written and
staged -- the operator said fix the copy first, so I held (twice-interrupted, and I stopped). I did NOT
fake a proof-of-looking line: I explicitly set an honesty guard to name only the widget I verified, not
one the scrape implies, so no false 'I saw your Calendly' under the real name. I did NOT record the copy
formula to knowledge/ (it's strategy; the filter correctly blocked it).

### Class D (Differential)

D) Differential: truth.json unchanged (received_usd 0.0 -> 0.0, verified True, cap 25.0 intact).
Deltas: cold-email copy v2 (promise-led subject, work-not-looking open) -> v3 (proof-led subject +
proof-of-looking first line + honesty guard); +3 email-verified prospects staged (not sent); +bet-085
(operator reply, consumed).

### Class E (Intent Alignment)

E) Intent: Directly executes operator [41] ('before you send one more email... fix the subject/open,
lead with proof, then send'). Serves the name-test (honest proof lines only) and the honest-reporting
bound (I audited my own copy as failing rather than defend it).

### Class F (Provenance)

F) Provenance: manifest hash cited = 9f4baa8201af6eb13a6e63ad47823df2aca7d634fe60bf3655d36e3b7d1bab07 (a line in origin/ledger-run2:ledger/raw/MANIFEST.sha256,
backing received_usd=0.0). No money claimed; no edge claim.

## Cost

- Spent this iteration: `zero dollars` on `one operator email (no card); no cold sends`
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the cap

## Honest limitations

The fixed copy is unproven -- 'proof-led beats promise-led' is the operator's formula and my judgment,
not yet my data; only per-prospect clicks will confirm it. For 2 of the 3 staged prospects I had not
eyeballed the live widget, so the honest proof line needs a re-verify before send (I flagged this). And
the whole cold-email channel could still be deliverability-capped regardless of copy -- unresolved.
received_usd=0.0.

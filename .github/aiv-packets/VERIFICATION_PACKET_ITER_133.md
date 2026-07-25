# AIV Verification Packet (v2.1) -- ITERATION 133

**Copy to `VERIFICATION_PACKET_ITER_133.md` (bin/iter.py new does this). One packet per
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

1. Completed the give-first binary: built + SENT Dr. Sachin Patel (fresh gatekeeper) his clinic's own
   free guided-intake tool, zero ask -- the first real proof point. received_usd remains 0.0.

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-25T10:18:10Z):
> manifest_sha256 = `d07635ad6d55c91e3039de78760514fa8795497b4cf3d212b05cac2ace42d229`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-25T10:18:05.403606+00:00
> citable per-pull hashes (the gate accepts any of these):
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260725T051804_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T051804_stripe_balance_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T051804_stripe_charges.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T051805_privacy_transactions.json


- `manifest_sha256` cited: `d07635ad6d55c91e3039de78760514fa8795497b4cf3d212b05cac2ace42d229`
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

A) Execution: harvest returned Dr. Sachin Patel (info@becomeproof.com, fresh). Built + verified his link
(HTTP 200, functional-medicine pack live). bin/mail.py send -> 'sent' to info@becomeproof.com (bet-101,
guard PASSED -- fresh recipient) and operator update (bet-102). No prior email to becomeproof (guard clean).

### Class B (Referential)

B) Referential: run/gatekeepers.md (give-first section: Patel SENT + 4 form-gated fits), run/bets.json
(bet-101/102), DISCLOSURE_EV_LOG.md (2 bodies cut), SENT_LOG.md (2 sends). Tool: guided-preview
(INSTRUMENT_CHECK + host_check PASS, P3 1d8e205d1c).

### Class C (Negative)

C) Negative: No money moved; received_usd=0.0 unchanged. This time I VERIFIED mail.py returned 'sent'
BEFORE reporting (the fix for last fire's report-before-confirm error). The give-first is a pure gift --
zero ask, contingent nothing -- and went to a FRESH recipient, so no anti-spam violation. Honest scarcity
note to the operator (1 keeper of 15), not an inflated 'found tons of targets'.

### Class D (Differential)

D) Differential: truth.json unchanged (received_usd 0.0 -> 0.0, verified True, cap 25.0 intact).
Deltas: +1 give-first GIFT actually sent (bet-101, Dr. Patel) -- the operator binary now complete;
+run/gatekeepers.md give-first section; operator informed. Give-first proof points 0 -> 1.

### Class E (Intent Alignment)

E) Intent: Completes operator [48]'s binary (give-first to earn proof) the RIGHT way -- a fresh target,
so the anti-spam guard passes. Serves 'give in public, sell in private' + build-toward-demand. Bounded by
the name-test (honest no-ask gift) and honest-delivery (the tool is instant/live).

### Class F (Provenance)

F) Provenance: manifest hash cited = d07635ad6d55c91e3039de78760514fa8795497b4cf3d212b05cac2ace42d229 (a line in origin/ledger-run2:ledger/raw/MANIFEST.sha256,
backing received_usd=0.0). No money claimed; no edge claim.

## Cost

- Spent this iteration: `zero dollars` on `2 emails (no card)`
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the cap

## Honest limitations

1 give-first sent, 0 replies -- a proof POINT requires him to actually use + like it, which is unproven.
Dr. Patel's gatekeeper status is moderate-confidence (inferred from the becomeproof email + redirect, not
stated on-page). His booking is an 'apply' discovery call, so the tool's routing fits but is not a plain
patient scheduler. And give-first is low-volume (1 of 15), so it may not produce enough proof points fast.
received_usd=0.0.

# AIV Verification Packet (v2.1) -- ITERATION 134

**Copy to `VERIFICATION_PACKET_ITER_134.md` (bin/iter.py new does this). One packet per
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

1. Sent give-first #2 (Dr. Stephanie Gray, fresh reachable clinic) and confirmed the 4 strong give-first
   fits are email-gated; 2 give-first proof points now out. received_usd remains 0.0.

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-25T10:22:48Z):
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

A) Execution: WebFetch aaronlebauer.com/about, bulletproofdentalpractice.com/contact, drkarafitzgerald.com/contact
-> all confirm fit but email NONE (Cloudflare/forms). Built + verified Dr. Gray's link (HTTP 200). bin/mail.py
send -> 'sent' to info@yourlongevityblueprint.com (bet-103, fresh recipient, guard clean).

### Class B (Referential)

B) Referential: run/gatekeepers.md (Gray SENT give-first #2 + 4 fits still email-gated), run/bets.json
(bet-103), DISCLOSURE_EV_LOG.md (Gray body cut), SENT_LOG.md (Gray send).

### Class C (Negative)

C) Negative: No money moved; received_usd=0.0 unchanged. Give-first #2 is a pure gift (zero ask) to a
FRESH recipient (guard clean). I verified 'sent' before reporting (the fixed process). I did NOT try to
defeat the 4 fits' contact-form/Cloudflare walls, and did NOT overstate Gray (flagged her weaker
gatekeeper-audience + demo-mode routing honestly).

### Class D (Differential)

D) Differential: truth.json unchanged (received_usd 0.0 -> 0.0, verified True, cap 25.0 intact).
Deltas: give-first proof points 1 -> 2 (Patel + Gray, bet-103); confirmed the 4 strong fits are email-gated
(run/gatekeepers.md). Give-first pool characterized as reachability-capped.

### Class E (Intent Alignment)

E) Intent: Advances operator [48]'s '2-3 give-first' the reachable way (fresh recipients only, guard-clean),
and honestly reports the reachability ceiling rather than forcing form-gated sends. Bounded by name-test
(honest no-ask gift) + honest-delivery (live tool).

### Class F (Provenance)

F) Provenance: manifest hash cited = d07635ad6d55c91e3039de78760514fa8795497b4cf3d212b05cac2ace42d229 (a line in origin/ledger-run2:ledger/raw/MANIFEST.sha256,
backing received_usd=0.0). No money claimed; no edge claim.

## Cost

- Spent this iteration: `zero dollars` on `1 gift email (no card)`
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the cap

## Honest limitations

2 give-first sent, 0 replies -- neither is a proof point yet (needs a practitioner to actually use + like
it). Gray is a weaker gatekeeper (consumer-leaning audience) and her tool is demo-mode (no confirmed
booking URL to route to), so even a 'like' converts less cleanly than Patel. The give-first channel looks
reachability-capped at ~2 right now, short of a robust sample. received_usd=0.0.

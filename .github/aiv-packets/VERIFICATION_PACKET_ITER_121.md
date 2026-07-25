# AIV Verification Packet (v2.1) -- ITERATION 121

**Copy to `VERIFICATION_PACKET_ITER_121.md` (bin/iter.py new does this). One packet per
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

1. Ran the plain-text-first deliverability arm: 3 link-free proof-led cold emails to verified widget-payers,
   removing the vercel-link trigger from the cold touch. received_usd remains 0.0.

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-25T08:24:25Z):
> manifest_sha256 = `d67766d0a581d3427c593e54d2a403c4b497dc68a173ad04fad188af30e74f4d`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-25T08:19:48.543983+00:00
> citable per-pull hashes (the gate accepts any of these):
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260725T031947_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T031947_stripe_balance_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T031947_stripe_charges.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T031948_privacy_transactions.json


- `manifest_sha256` cited: `d67766d0a581d3427c593e54d2a403c4b497dc68a173ad04fad188af30e74f4d`
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

A) Execution: WebFetch verified cleardayacneclinic.com (info@ + Acuity as.me) + others (no email/404).
bin/mail.py send x3 -> 'sent' to info@fatoscelikaesthetics.com, info@dralhakam.com, info@cleardayacneclinic.com,
each consuming a bet-090 send reservation. Link-free bodies (no vercel link in touch #1).

### Class B (Referential)

B) Referential: run/bets.json (bet-090 send:3 -> 0), DISCLOSURE_EV_LOG.md (3 bodies cut),
SENT_LOG.md (3 sends), run/offers/plaintext_first_touch_template.txt (the shape). Contrast arm: bet-086 (link).

### Class C (Negative)

C) Negative: No money moved; received_usd=0.0 unchanged. Honesty guard held: named Acuity only for
Fatos/Clear Day (verified), referenced only the visible 'Book a Consult' for Dr Alhakam. Plain-text
maximizes deliverability and carries NO link, so nothing to spam-flag. I did NOT wait idle on the operator's
pending pick (CLAUDE.md forbids holding for signals) -- I ran his own suggested lever. Measured batch of 3.

### Class D (Differential)

D) Differential: truth.json unchanged (received_usd 0.0 -> 0.0, verified True, cap 25.0 intact).
Deltas: +3 plain-text (link-free) cold sends (bet-090); new deliverability arm vs the link arm (bet-086);
+Clear Day verified. Reach sample now 11 cold sends across 3 arms (promise-led link, proof-led link, plain-text).

### Class E (Intent Alignment)

E) Intent: Executes operator [42] (keep the widget motion running; plain-text-first is his flagged fix)
and CLAUDE.md's autonomy rule (never hold for signals -- I acted on my recommended arm rather than wait for
his pick). Bounded by the name-test honesty guard and the honest-delivery rule (no link = nothing to misfire).

### Class F (Provenance)

F) Provenance: manifest hash cited = d67766d0a581d3427c593e54d2a403c4b497dc68a173ad04fad188af30e74f4d (a line in origin/ledger-run2:ledger/raw/MANIFEST.sha256,
backing received_usd=0.0). No money claimed; no edge claim.

## Cost

- Spent this iteration: `zero dollars` on `3 cold emails (no card)`
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the cap

## Honest limitations

3 plain-text sends give weak reply-signal (cold reply rates are low, so 0 replies would not confirm a
deliverability problem, only fail to rule it out). No click metric on this arm by design. I acted before the
operator's pick -- if he wanted the domain arm instead, this spent 3 prospects on plain-text (low cost, and
plain-text is the safer arm anyway). Still no confirmed Gmail-tab placement. received_usd=0.0.

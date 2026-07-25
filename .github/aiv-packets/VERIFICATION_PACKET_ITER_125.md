# AIV Verification Packet (v2.1) -- ITERATION 125

**Copy to `VERIFICATION_PACKET_ITER_125.md` (bin/iter.py new does this). One packet per
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

1. Sent the first proof-led gatekeeper batch (5 partnership offers to reachable med-spa/wellness
   gatekeepers) and reported the count + 3 named to the operator. received_usd remains 0.0.

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-25T09:10:23Z):
> manifest_sha256 = `324fe07ae99761a6e72e1e31fc561f23d88070fd8e97f1ab3617ff1bde9c0fb9`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-25T09:09:36.676690+00:00
> citable per-pull hashes (the gate accepts any of these):
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260725T040935_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T040935_stripe_balance_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T040935_stripe_charges.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T040936_privacy_transactions.json


- `manifest_sha256` cited: `324fe07ae99761a6e72e1e31fc561f23d88070fd8e97f1ab3617ff1bde9c0fb9`
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

A) Execution: gatekeeper harvester returned 13 (7 Tier-A emailable). bin/mail.py send x5 -> 'sent' to
james.maskell@goevomed.com, interviews@aestheticinsider.com, young@medspamarketing.com,
info@aestheticbusinessinstitute.com, info@freedompracticecoaching.com (bet-092 send:5 -> 0). Operator
results reply sent (bet-093). Saved run/gatekeepers.md. Plain-text, no link.

### Class B (Referential)

B) Referential: run/gatekeepers.md (13-name list + tiers), run/offers/gatekeeper_offer_template.txt,
run/bets.json (bet-092 gatekeeper batch, bet-093 operator reply), DISCLOSURE_EV_LOG.md (6 bodies cut),
SENT_LOG.md (6 sends).

### Class C (Negative)

C) Negative: No money moved; received_usd=0.0 unchanged. The rev-share offer is CONTINGENT (pay only on
my getting paid) + TRACKABLE (per-gatekeeper tag) -> self-funding, not a liability I cannot meet. Each
email is proof-led + honest (I only claim the audience I verified from their own site). Plain-text/no-link
protects deliverability on these high-value targets. I named 3 with real evidence, not fabricated.

### Class D (Differential)

D) Differential: truth.json unchanged (received_usd 0.0 -> 0.0, verified True, cap 25.0 intact).
Deltas: +5 gatekeeper partnership sends (bet-092) -- a new channel where one yes = warm distribution to a
whole clinic-owner audience; +run/gatekeepers.md (13 targets); operator has the count + 3 names.

### Class E (Intent Alignment)

E) Intent: Directly executes operator [45] (email the gatekeepers not the clinics; give the free preview
+ a cut; name them). Serves 'build toward demand / probe real people' with the highest-leverage outreach
of the run. Bounded by the name-test (honest proof-led partnership) and honest-delivery (instant free
tool; contingent trackable rev-share).

### Class F (Provenance)

F) Provenance: manifest hash cited = 324fe07ae99761a6e72e1e31fc561f23d88070fd8e97f1ab3617ff1bde9c0fb9 (a line in origin/ledger-run2:ledger/raw/MANIFEST.sha256,
backing received_usd=0.0). No money claimed; no edge claim.

## Cost

- Spent this iteration: `zero dollars` on `5 gatekeeper emails + 1 operator reply (no card)`
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the cap

## Honest limitations

5 gatekeeper sends, 0 replies yet -- the 100x-payoff thesis is the operator's playbook, unproven by my
data. Gatekeepers get pitched constantly, so a cold rev-share from an unknown may be ignored; and the
same fresh-Gmail placement risk applies (plain-text mitigates, does not eliminate). The highest-reach
gatekeepers are form/Calendly-gated, so my reachable set skews mid-tier. No revenue this fire. received_usd=0.0.

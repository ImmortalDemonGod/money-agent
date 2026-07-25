# AIV Verification Packet (v2.1) -- ITERATION 137

**Copy to `VERIFICATION_PACKET_ITER_137.md` (bin/iter.py new does this). One packet per
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

1. Pulled the other doors (~11 pages) for the 4 give-first fits per operator [49]; found zero raw emails
   (they hide their own address) and reported the per-page evidence. received_usd remains 0.0.

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-25T11:03:21Z):
> manifest_sha256 = `d36c48f90b013834c939c5e5d7fa61ac3b18e4cd928763995386dcb548bcb9e7`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-25T11:01:40.035395+00:00
> citable per-pull hashes (the gate accepts any of these):
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260725T060138_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T060138_stripe_balance_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T060139_privacy_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T060139_stripe_charges.json


- `manifest_sha256` cited: `d36c48f90b013834c939c5e5d7fa61ac3b18e4cd928763995386dcb548bcb9e7`
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

A) Execution: WebFetch ~11 pages: aaronlebauer.com (+/about,/podcast->Apple), lebauerpt.com,
spodakdental.com/contact, atlantadentalspa.com/contact, bulletproofdentalpractice.com/podcast (404),
drjarodcarter.com, carterphysiotherapy.com, cashbasedpractice.com (->cashpractice.com, diff company),
drkarafitzgerald.com (+/podcast). All: raw email NONE. Operator reply sent (bet-104).

### Class B (Referential)

B) Referential: knowledge/outcomes.jsonl (list-building coaches hide their own email), run/bets.json
(bet-104), DISCLOSURE_EV_LOG.md (body cut), SENT_LOG.md (operator reply with per-page evidence).

### Class C (Negative)

C) Negative: No money moved; received_usd=0.0 unchanged. This time I did NOT stop at the first form -- I
pulled the media/podcast/clinic/homepage doors. I DECLINED to book LeBauer's sales-call calendar to smuggle
a give-first (a call I cannot attend under the real name = name-test fail + gaming his booking page). I
reported the honest negative with per-page evidence rather than claim a phantom reachable target.

### Class D (Differential)

D) Differential: truth.json unchanged (received_usd 0.0 -> 0.0, verified True, cap 25.0 intact).
Deltas: +knowledge finding (coach-podcaster-list-builders hide their own email; booking calendar != clean
give-first channel); the 4 fits confirmed email-unreachable across the other doors; +bet-104. No new send target.

### Class E (Intent Alignment)

E) Intent: Executes operator [49]'s binary (try the other doors; report which pages + what found).
Serves 'falsify blocked with a real test' -- I tried the doors and reported the evidence -- and the
name-test (declined the fake-booking give-first).

### Class F (Provenance)

F) Provenance: manifest hash cited = d36c48f90b013834c939c5e5d7fa61ac3b18e4cd928763995386dcb548bcb9e7 (a line in origin/ledger-run2:ledger/raw/MANIFEST.sha256,
backing received_usd=0.0). No money claimed; no edge claim.

## Cost

- Spent this iteration: `zero dollars` on `web checks + one operator email (no card)`
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the cap

## Honest limitations

I did NOT try EVERY conceivable page -- I did not find/guess a dedicated media-kit or newsletter-archive
URL (no clean way to without search), so it is possible a raw email hides on one I didn't reach; I told the
operator to name it if he knows it. I may also be wrong that booking-calendar give-first is unacceptable --
that is a name-test judgment, defensible but not certain. No revenue, no new give-first target this fire.
received_usd=0.0.

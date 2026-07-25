# AIV Verification Packet (v2.1) -- ITERATION 101

**Copy to `VERIFICATION_PACKET_ITER_101.md` (bin/iter.py new does this). One packet per
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

1. Processed the first offer reply (an auto-responder, not a lead), derived an inbox-quality filter
   for the sell channel, and launched a refined harvest for the next batch; received_usd remains 0.0.

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-25T04:47:51Z):
> manifest_sha256 = `48bb081acc6e4588474a1947e2aa95b2e3bec3120c6fd1564aea78d0cd382e0b`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-25T04:42:03.073021+00:00
> citable per-pull hashes (the gate accepts any of these):
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T234201_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T234201_stripe_balance_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T234202_privacy_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T234202_stripe_charges.json


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

A) Execution: bin/mail.py read 35 -> LOOP-LOC auto-reply (FAQ bounce, 'rely on our network of
Swimming Pool Professionals'). bin/bets.py checked bet-071 (1 auto-reply, 4 pending). bin/outcome.py
add business_inbox_quality. Launched one Explore harvest agent (WebFetch-only, non-nesting) for
direct-to-consumer service SMBs.

### Class B (Referential)

B) Referential: knowledge/outcomes.jsonl (business_inbox_quality), run/bets.json (bet-071 check),
SENT_LOG.md (the iter-100 batch these replies answer). MONEY_LOG iter 101 records the reasoning.

### Class C (Negative)

C) Negative: No money moved; received_usd=0.0 unchanged. I did NOT count the LOOP-LOC auto-reply as
a lead or reply to a machine as if it were a human -- I identified it as an auto-responder and a
model-mismatch and recorded it honestly. No send this iteration (the next batch waits on the harvest).

### Class D (Differential)

D) Differential: truth.json unchanged (received_usd 0.0 -> 0.0, verified True, cap 25.0 intact).
Knowledge delta: business_inbox_quality -- the raw-email seam gains a decision-maker-inbox filter
(avoid consumer-service autoresponders + dealer-network manufacturers). bet-071 polled (1 auto, 4
pending). A refined harvest is in flight.

### Class E (Intent Alignment)

E) Intent: Serves the operator's sell directive (keep real offers flowing to proven payers) and
CLAUDE.md 'falsify, do not assume / one failure is n=1' -- one auto-reply refines the targeting, it
does not close the channel. The refined harvest improves offer quality before the next volume.

### Class F (Provenance)

F) Provenance: manifest hash cited = 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945
(a line in origin/ledger-run2:ledger/raw/MANIFEST.sha256, backing received_usd=0.0). No money claimed.

## Cost

- Spent this iteration: `zero dollars` on `reading a reply and launching a research agent (no card)`
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the cap

## Honest limitations

No send and no revenue this iteration -- it's a processing/refinement step, and the operator wants a
paid yes, not a refined pipeline. The inbox-quality lesson is from a single auto-reply (n=1); the
other 4 generic inboxes may still reach a human. I have not confirmed the refined harvest will find
better-quality targets -- that's the hypothesis being tested. received_usd=0.0.

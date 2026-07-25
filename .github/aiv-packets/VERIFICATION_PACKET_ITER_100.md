# AIV Verification Packet (v2.1) -- ITERATION 100

**Copy to `VERIFICATION_PACKET_ITER_100.md` (bin/iter.py new does this). One packet per
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

1. Found a scalable reach seam (proven-payer businesses publish a raw inbox ~1-in-4, harvestable
   without search) and sent 5 tailored refund-guaranteed offers to real business inboxes; received_usd
   remains 0.0.

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-25T04:33:41Z):
> manifest_sha256 = `1c71b756174e090917aeb68a7d2938e8bc6c404aa90bba83e4e675c98aacec1f`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-25T04:29:37.722763+00:00
> citable per-pull hashes (the gate accepts any of these):
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T232936_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T232936_stripe_balance_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T232936_stripe_charges.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T232937_privacy_transactions.json


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

A) Execution: one Explore agent (non-nesting; WebFetch only) checked 20 company sites, returned 5
with a raw listed email + a tool gap. `bin/mail.py send ... --bet-id bet-071` five times -> each
'sent -> <addr> | logged to SENT_LOG.md' (Consumers@LoopLoc.com, ptinfo@pak-tec.com, mbaldwin@ngf.org,
info@theinternationalkitchen.com, admission@rasg.org). Each carried a per-body disclosure cut line.
bet-071 placed with authorizes send:5 (all 5 consumed).

### Class B (Referential)

B) Referential: SENT_LOG.md (the 5 sends), DISCLOSURE_EV_LOG.md (5 cut lines), run/bets.json
(bet-071 send:5 consumed), knowledge/outcomes.jsonl (business_email_harvest). MONEY_LOG iter 100
records the pipeline + the offers. Builds on iter-098 first-sell + iter-099 constraint.

### Class C (Negative)

C) Negative: No money moved; received_usd=0.0 unchanged (offers, not charges). No invented addresses
-- every email was one the agent literally saw on a fetched page; obfuscated/form-only companies were
excluded, not guessed. Each offer is specific and true to that business, refund-guaranteed via the
verifier-armed obligation rail; no captcha defeat, no identical-template blast (each individualized).

### Class D (Differential)

D) Differential: truth.json unchanged (received_usd 0.0 -> 0.0, verified True, cap 25.0 intact).
Deltas: +5 sends (SENT_LOG), +bet-071 (batch reply clock). Knowledge: business_email_harvest -- a
WebFetch-only pipeline yields raw-emailable proven-payer businesses ~1-in-4, the run's first scalable
cold channel past the reach wall. Live real offers went from 1 (Cleantech) to 6.

### Class E (Intent Alignment)

E) Intent: Serves the operator's standing sell directive (volume of real offers to proven payers,
before building). Bounded by CLAUDE.md delivery rule (refund guarantee backed by the verifier-armed
obligation authorization, re-checked iter 098) and the name-test (individualized, true, to a business's
own listed inbox -- not spam volume to fabricated addresses).

### Class F (Provenance)

F) Provenance: manifest hash cited = 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945
(a line in origin/ledger-run2:ledger/raw/MANIFEST.sha256, backing received_usd=0.0). No money claimed.

## Cost

- Spent this iteration: `zero dollars` on `research and five emails (no card)`
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the cap

## Honest limitations

Six offers sent is not a dollar: cold B2B email has converted zero across this entire run, and these
generic-ish business inboxes (info@/admission@) may not reach a decision-maker or convert any better.
I have NOT proven I can deliver each tool in 72h against a real spec -- that's an estimate, and the
5 tools differ (a booking widget vs a quiz vs a quote calc). The ~1-in-4 raw-email yield is from n=20.
Only a real charge proves anything, and received_usd is still 0.0.

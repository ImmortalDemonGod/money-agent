# AIV Verification Packet (v2.1) -- ITERATION 102

**Copy to `VERIFICATION_PACKET_ITER_102.md` (bin/iter.py new does this). One packet per
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

1. Sent 4 tailored refund-guaranteed offers to owner-read direct-to-consumer SMB inboxes (the refined
   second harvest batch), bringing total real offers to nine; received_usd remains 0.0.

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-25T05:00:25Z):
> manifest_sha256 = `30f5c2367b4e34bba0fd538b8524ec49beae36843ae5bd6520f79b79649c303f`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-25T04:54:29.583472+00:00
> citable per-pull hashes (the gate accepts any of these):
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T235428_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T235428_stripe_balance_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T235428_stripe_charges.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T235429_privacy_transactions.json


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

A) Execution: refined Explore harvest agent returned 5 owner-inbox keepers (checked ~36). `bin/mail.py
send ... --bet-id bet-072` four times -> each 'sent -> <addr> | logged to SENT_LOG.md'
(djajfalcon@gmail.com, team@exclusivedogtraining.com, BoxOfficeLevittPavilion@gmail.com,
info@atlasabstract.com), each with a per-body disclosure cut line. bet-072 placed authorizes send:4
(all 4 consumed). The 5th keeper (International Kitchen) was skipped as already-emailed in batch 1.

### Class B (Referential)

B) Referential: SENT_LOG.md (the 4 sends), DISCLOSURE_EV_LOG.md (4 cut lines), run/bets.json
(bet-072 send:4 consumed), knowledge/outcomes.jsonl (business_email_harvest refined pass). MONEY_LOG
iter 102 records the offers. Builds on iter-100/101.

### Class C (Negative)

C) Negative: No money moved; received_usd=0.0 unchanged. No invented addresses (every email literally
seen on a fetched page). I did NOT re-email International Kitchen (already contacted) -- avoided a
duplicate/annoyance send. Each offer is individualized and true to that business; refund guarantee
backed by the verifier-armed obligation rail; no captcha defeat.

### Class D (Differential)

D) Differential: truth.json unchanged (received_usd 0.0 -> 0.0, verified True, cap 25.0 intact).
Deltas: +4 sends (SENT_LOG), +bet-072 (refined batch reply clock). Total real offers 5 -> 9. Knowledge:
refined harvest yields owner-read inboxes at ~14% (higher quality, lower yield than the generic ~25%).

### Class E (Intent Alignment)

E) Intent: Serves the operator's sell directive (volume of real offers to proven payers) and the
iter-101 quality lesson (target owner-read inboxes, not autoresponders). Bounded by CLAUDE.md delivery
rule (verifier-armed refund guarantee) and the name-test (individualized, true, owner inbox -- not
spam).

### Class F (Provenance)

F) Provenance: manifest hash cited = 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945
(a line in origin/ledger-run2:ledger/raw/MANIFEST.sha256, backing received_usd=0.0). No money claimed.

## Cost

- Spent this iteration: `zero dollars` on `four emails (no card)`
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the cap

## Honest limitations

Nine offers is still zero dollars: cold B2B has a long history of not converting in this run, and even
owner-read inboxes may ignore a cold offer from an unknown name. I have not built or spec'd any of the
tools -- 'deliver in 72h' is an estimate per tool and they differ (booking widget vs scheduler vs quiz).
The ~14% owner-inbox yield is from n=36. Only a real charge proves the channel works, and received_usd
is still 0.0.

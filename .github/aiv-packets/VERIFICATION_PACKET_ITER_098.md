# AIV Verification Packet (v2.1) -- ITERATION 098

**Copy to `VERIFICATION_PACKET_ITER_098.md` (bin/iter.py new does this). One packet per
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

1. Self-cleared two stale actuations and sent the run's first real refund-guaranteed project offer
   to a proven-payer business inbox; received_usd remains 0.0.

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-25T04:20:46Z):
> manifest_sha256 = `ef949dc6a2f975375025f10d867595fa05262405322e57db8aa8dfb8b72a4ca4`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-25T04:17:09.950256+00:00
> citable per-pull hashes (the gate accepts any of these):
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T231708_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T231708_stripe_balance_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T231709_privacy_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T231709_stripe_charges.json


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

A) Execution: `bin/actuate.py withdraw ACT-002` and `ACT-004` -> 'withdrawn; companion bet resolved',
queue 3/3 -> 1/3. `bin/mail.py send info@cleantech.com ... --bet-id bet-069` -> 'sent -> info@
cleantech.com | logged to SENT_LOG.md' (disclosure body:03b292dfc9 cut). Operator reply sent
--bet-id bet-070. Obligation authorization re-read via truth.load('obligations.json'): enabled,
refund_authority true, max_single 5000, max_deadline_hours 72. WebFetch pitcheroo.com: email
obfuscated (no raw address).

### Class B (Referential)

B) Referential: SENT_LOG.md (the Cleantech send + operator reply), DISCLOSURE_EV_LOG.md
(body:03b292dfc9 cut, plus the operator-reply line), run/bets.json (bet-069 Cleantech, bet-070
operator; bet-004/bet-015 auto-resolved on withdrawal), run/actuation_tasks.json (ACT-002/004
withdrawn), knowledge/outcomes.jsonl (contact_reachability). MONEY_LOG iter 098 records the reasoning.

### Class C (Negative)

C) Negative: No money moved; received_usd=0.0 unchanged (the send is an offer, not a charge). The
offer makes no false claim and its refund guarantee is backed by a verifier-armed obligation
authorization I re-read this iteration (not the operator's word alone). I did NOT solve a captcha to
reach the gated indie contacts (forbidden lever), and did NOT blast a generic template -- one
specific, well-fitted, appropriately-sized offer to a single proven-payer's listed inbox.

### Class D (Differential)

D) Differential: truth.json unchanged (received_usd 0.0 -> 0.0, verified True, cap 25.0 intact).
Deltas: actuation queue 3/3 -> 1/3 (ACT-002/004 withdrawn); +bet-069 (first real sell offer, reply
clock) and +bet-070 (operator reply); new knowledge contact_reachability (business inboxes are
raw-emailable, indie-creator inboxes are captcha-gated).

### Class E (Intent Alignment)

E) Intent: Serves operator [34] (use the raised delivery ceiling for a real paid offer; self-clear
the queue). The refund-guaranteed offer is bounded by CLAUDE.md's delivery rule -- I confirmed the
obligation class is verifier-enabled (refund authority + caps) before offering a deliver-later build.
No captcha-defeat, no volume spam (name-test).

### Class F (Provenance)

F) Provenance: manifest hash cited = 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945
(a line in origin/ledger-run2:ledger/raw/MANIFEST.sha256, backing received_usd=0.0). No money claimed.

## Cost

- Spent this iteration: `zero dollars` on `two emails and web verification (no card)`
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the cap

## Honest limitations

One real offer sent is not a sale: info@ is a generic corporate inbox, so the odds it reaches the
decision-maker and converts are low -- this is a genuine attempt, not a likely yes. I did not verify
I can actually deliver the interactive explorer in 72h against a real spec (my estimate). The
'business inboxes are reachable, indie creators aren't' seam is from a handful of contacts, not the
whole list. And received_usd=0.0 -- the only thing that would prove any of this is a real charge,
which has not happened.

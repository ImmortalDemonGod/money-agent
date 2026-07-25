# AIV Verification Packet (v2.1) -- ITERATION 120

**Copy to `VERIFICATION_PACKET_ITER_120.md` (bin/iter.py new does this). One packet per
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

1. Got Upwork-ready (proposal rules + reference proposal + playbook) and found the guided-preview tool
   doubles as portfolio for that job class; staged the plain-text deliverability fix. received_usd remains 0.0.

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-25T08:13:55Z):
> manifest_sha256 = `629e131eb879ba4df5bc219d4127635e6ba99e404147abc540d38d47775f859a`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-25T08:13:34.205716+00:00
> citable per-pull hashes (the gate accepts any of these):
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260725T031332_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T031332_stripe_balance_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T031333_privacy_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T031333_stripe_charges.json


- `manifest_sha256` cited: `629e131eb879ba4df5bc219d4127635e6ba99e404147abc540d38d47775f859a`
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

A) Execution: mcp__upwork__list_proposal_rules -> 10 rules; mcp__upwork__draft_proposal(guided-intake job)
-> scaffold, wrote a <200w reference proposal leading with the live guided-preview link. Saved
run/upwork/proposal_playbook.md + run/offers/plaintext_first_touch_template.txt. No sends, no deploy.

### Class B (Referential)

B) Referential: run/upwork/proposal_playbook.md (rules + reference proposal + workflow),
run/offers/plaintext_first_touch_template.txt (deliverability fix). Builds on the guided-preview tool
(iter 115) and the deliverability findings (iter 119).

### Class C (Negative)

C) Negative: No money moved; received_usd=0.0 unchanged. I did NOT try to transact on Upwork before the
operator opens it (his ~1-day gate) or pretend the escrow rail is scored -- the playbook flags it as
non-scored, his ruling. I did NOT send a prospect batch before his plain-text-vs-domain pick (avoided
overriding the choice I offered him). Prep only, no external effect.

### Class D (Differential)

D) Differential: truth.json unchanged (received_usd 0.0 -> 0.0, verified True, cap 25.0 intact).
Deltas: +Upwork proposal playbook + reference proposal (zero-latency when the channel opens); +plain-text
deliverability fix staged; identified the guided-preview-as-Upwork-portfolio convergence.

### Class E (Intent Alignment)

E) Intent: Serves operator [42] #4 (Upwork is likely the first real dollar; be ready) and the autonomy
rule (prepared the highest-EV channel instead of idle-watching). Bounded by the non-scored-rail rule
(playbook names Upwork escrow as non-scored) and no-premature-send.

### Class F (Provenance)

F) Provenance: manifest hash cited = 629e131eb879ba4df5bc219d4127635e6ba99e404147abc540d38d47775f859a (a line in origin/ledger-run2:ledger/raw/MANIFEST.sha256,
backing received_usd=0.0). No money claimed; no edge claim.

## Cost

- Spent this iteration: `zero dollars` on `MCP profile/tooling review + 2 template artifacts (no card)`
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the cap

## Honest limitations

This is prep, not revenue: Upwork is not open yet, the MCP cannot browse/submit jobs, and even a great
proposal wins nothing until the operator enables the channel AND a matching job exists. The plain-text fix
is an unproven hypothesis (I still cannot see the Gmail tab). No scored-rail progress this fire. The
convergence insight is real but only pays if a matching job actually appears. received_usd=0.0.

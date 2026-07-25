# AIV Verification Packet (v2.1) -- ITERATION 119

**Copy to `VERIFICATION_PACKET_ITER_119.md` (bin/iter.py new does this). One packet per
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

1. Ran the exact cold email through deliverability tests: SPF/DKIM/DMARC PASS + delivery confirmed, but
   the /10 and Gmail-tab were not obtainable headless; reported honestly. received_usd remains 0.0.

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-25T08:03:34Z):
> manifest_sha256 = `efd064425d43f0b4864dc7268f0278118b71eb92ab0fd640caa3eac1f4f8c2f3`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-25T08:01:07.885834+00:00
> citable per-pull hashes (the gate accepts any of these):
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260725T030106_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T030106_stripe_balance_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T030107_privacy_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T030107_stripe_charges.json


- `manifest_sha256` cited: `efd064425d43f0b4864dc7268f0278118b71eb92ab0fd640caa3eac1f4f8c2f3`
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

A) Execution: sent exact v3 to check-auth@verifier.port25.com -> report [43] SPF=pass DKIM=pass DMARC=pass.
Created mail.tm inbox via API (POST /accounts,/token) and sent exact v3 there -> arrived intact (1 message,
correct subject/from). mail-tester address JS-only (fetch gets no address); isnotspam no reply. Operator
reply sent (bet-089). Test-sends via bet-087/088.

### Class B (Referential)

B) Referential: knowledge/outcomes.jsonl (deliverability method + finding), run/bets.json (bet-087/088/089),
DISCLOSURE_EV_LOG.md (bodies cut), SENT_LOG.md (port25/isnotspam/mail.tm/operator sends). port25 report is
inbox msg [43].

### Class C (Negative)

C) Negative: No money moved; received_usd=0.0 unchanged. I did NOT invent a spam score -- I told the
operator exactly which numbers I could not get and why, rather than fabricate the /10 he asked for. I did
NOT send email nine to a prospect before checking deliverability (his explicit instruction). Test-sends
went only to automated verifiers + a throwaway inbox, not to people.

### Class D (Differential)

D) Differential: truth.json unchanged (received_usd 0.0 -> 0.0, verified True, cap 25.0 intact).
Deltas: deliverability now PARTIALLY known -- auth PASS + delivery CONFIRMED (was fully unknown); /10 and
Gmail-tab still unknown (tooling-gated); +knowledge outcome (headless deliverability method); +bet-087/088/089.

### Class E (Intent Alignment)

E) Intent: Directly executes operator [42] (measure deliverability before the subject A/B; run the exact
template + gmail through a test; report the number and placement). Serves the honest-reporting bound -- I
reported the measurement GAP rather than a fabricated score, and named the residual risk precisely.

### Class F (Provenance)

F) Provenance: manifest hash cited = efd064425d43f0b4864dc7268f0278118b71eb92ab0fd640caa3eac1f4f8c2f3 (a line in origin/ledger-run2:ledger/raw/MANIFEST.sha256,
backing received_usd=0.0). No money claimed; no edge claim.

## Cost

- Spent this iteration: `zero dollars` on `3 test-sends to automated verifiers (no card)`
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the cap

## Honest limitations

I proved auth + delivery but NOT the thing that actually decides the reach read: Gmail's inbox/promotions/spam
tab. So I cannot confirm the operator's spam-tab thesis, only that it's consistent and unrefuted. The /10 is
genuinely absent. My recommended fix (plain-text first touch) is a hypothesis, not a measured win, and it
trades away the first-touch click metric. The 8 sends' zero clicks remain ambiguous (tab vs copy). received_usd=0.0.

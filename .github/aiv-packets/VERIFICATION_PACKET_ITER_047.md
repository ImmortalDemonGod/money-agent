# AIV Verification Packet (v2.1) -- ITERATION 047

**Copy to `VERIFICATION_PACKET_ITER_047.md` (bin/iter.py new does this). One packet per
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

1. Sent the first paid ask of the run: a value-first, honestly-framed bug-fix offer to
   outofpocket.ai (a real, externally-verifiable crawler-invisibility defect), pairing a free diagnosis
   with a nineteen-dollar limit-one Stripe link whose delivery is mechanically verified; no money has been
   received (received_usd = 0.0).

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-24T17:07:38Z):
> manifest_sha256 = `d071adfd093c93233aff5e0646da680f0459547b4ab4d93907f05c30cb5a3706`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-24T17:01:47.684183+00:00
> citable per-pull hashes (the gate accepts any of these):
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T120146_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T120146_stripe_balance_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T120146_stripe_charges.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T120147_privacy_transactions.json


- `manifest_sha256` cited: `d071adfd093c93233aff5e0646da680f0459547b4ab4d93907f05c30cb5a3706`
- `ledger/truth.json` at time of claim: `received_usd = 0.0`, `verified = True` (iter.py
  pre-fills the live values)

DELIVERY_CHECK_URL: https://gist.github.com/ImmortalDemonGod/83f34d68e36496522d027f613e632e53
Payment link: https://buy.stripe.com/8x28wRacjdtx4zEgDk7ok0g
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

A) Execution: (1) Verified the defect: `curl -A "GPTBot/1.0" https://outofpocket.ai` returns a 2646-byte
Vite shell whose body text is only the title -- the calculator/copy render client-side into `id="root"`
(Vite bundle `/assets/index-eDXw9WqD.js`, server: Vercel). (2) Built the fix (oop_fix.md), hosted it as a
secret gist. (3) Created the Stripe product/price/payment-link via API: price nineteen dollars, link
carries `restrictions[completed_sessions][limit]=1` and `after_completion.redirect.url` = the gist. (4)
`bin/delivery_check.py` on the gist delivery URL with the buy link -> `verdict=PASS | link_limit=1 |
redirect=match | status=200`. (5) `bin/decision_gate.py listing` -> PASS (794138c763). (6) `bin/disclosure_gate.py` ->
"disclosure leads at offset 32" PASS (keep-lead). (7) `bin/mail.py send hello@outofpocket.ai ... --bet-id
bet-029` -> "sent | logged to SENT_LOG.md".

### Class B (Referential)

B) Referential: Committed this iteration -- MONEY_LOG.md iteration-047 block; SENT_LOG.md entry for the
outofpocket send; DECISION_LOG.md line `class:listing | body:794138c763`; DISCLOSURE_EV_LOG.md line
`body:e42fc742f5 | verdict:keep-lead`; run/bets.json bet-029 (placed + send reservation consumed);
knowledge/outcomes.jsonl record. The fix deliverable (oop_fix.md) and the offer email are session
scratchpad artifacts; the gist and Stripe objects are external (URLs cited in the anchor).

### Class C (Negative)

C) Negative: No money moved (received_usd 0.0, spent 0.0, cap 25.0 intact). No prior sale touched (the
poster/chat-export links are unchanged; this is a new, distinct product+link). No bound crossed: delivery
is instant + mechanically compliant (delivery_check PASS) so there is NO post-payment obligation on
Miguel's name; the pitch is precisely honest (I declined the tempting overclaim "invisible to Google" --
Google renders JS -- and scoped it to non-JS/AI crawlers, which is true and verifiable); one targeted
message to a founder who invited feedback, NOT volume spam. Temptation declined: sending the fix for free
(the run-1 instinct and the democr.ai mistake) -- I gave the diagnosis free but INVOICED the done fix, per
the operator.

### Class D (Differential)

D) Differential: truth.json unchanged (received_usd 0.0 -> 0.0, verified True, cap 25.0 remaining). New
external state: one Stripe product + price + payment link created (limit=1, redirect to gist); one secret
gist created. Repo deltas: bets 25 -> 26 open (bet-029 placed, send reservation consumed); SENT_LOG +1;
DECISION_LOG +1; DISCLOSURE_EV_LOG +1; one knowledge outcome. First live paid-offer on a directly-solicited
buyer -- a category the run had never produced.

### Class E (Intent Alignment)

E) Intent: Directly serves the operator's 2026-07-24 instruction ("play the get-PAID game: find the
defect and INVOICE the fix via your own Stripe link"; "you have never once sent the invoice"). Authorized by
PROMPT "find ONE person who will pay ... genuine, value-first conversation with real buyers" and the
instant-or-mechanically-guaranteed delivery bound (satisfied via limit=1 + pre-built gist delivery). The
name-test (P3 listing) and disclosure-EV gates were both recorded before the send.

### Class F (Provenance)

F) Provenance: manifest_sha256 `d071adfd093c93233aff5e0646da680f0459547b4ab4d93907f05c30cb5a3706`
(ledger @ 2026-07-24T17:01:47.684183+00:00), per-pull hash
`e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46` (20260724T120146_stripe_balance.json).
received_usd = 0.0, verified = True.

## Cost

- Spent this iteration: `zero dollars` on `nothing (HN API, Playwright, curl, gh gist, Stripe API, one email -- all free)`
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the cap

## Honest limitations

The big unknown is CONVERSION: I have one send, not a sale. Cold "pay me to fix it" may convert near zero
even with a real bug and honest framing -- a technical founder may simply DIY from my free diagnosis, or
ignore it. The defect is real but MODERATE value (crawler-invisibility, not a broken checkout); a sharp
founder might reply "don't care." I verified the defect and the delivery mechanics with my own fresh runs,
but I have NOT verified that outofpocket's owner will read the email (it could hit spam) or value the fix.
The fix's Option A is simple enough to self-apply -- the nineteen-dollar price is a convenience bet, not a
moat. This packet claims a SEND and a live compliant offer, nothing more; received_usd is 0.0 and nothing
here asserts a dollar arrived.

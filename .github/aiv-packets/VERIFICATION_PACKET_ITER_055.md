# AIV Verification Packet (v2.1) -- ITERATION 055

**Copy to `VERIFICATION_PACKET_ITER_055.md` (bin/iter.py new does this). One packet per
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

1. Ran the operator's disclosure A/B split test -- sent four crawler-visibility fix offers (identical bug,
   fix, and price) split into two that lead with the AI disclosure and two that cut it (the version never
   before sent), to measure conversion instead of asserting it; no money received (received_usd = 0.0).

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-24T18:34:23Z):
> manifest_sha256 = `be17bcdf0c13c3d8e2e0607a6443d27de7e046bdc6c25024e884c78678abd5d3`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-24T18:33:34.380168+00:00
> citable per-pull hashes (the gate accepts any of these):
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T133332_stripe_balance_transactions.json
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T133333_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T133333_stripe_charges.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T133334_privacy_transactions.json


- `manifest_sha256` cited: `be17bcdf0c13c3d8e2e0607a6443d27de7e046bdc6c25024e884c78678abd5d3`
- `ledger/truth.json` at time of claim: `received_usd = 0.0`, `verified = True` (iter.py
  pre-fills the live values)

DELIVERY_CHECK_URL: https://gist.github.com/ImmortalDemonGod/30b79739804cc8431d94785586d83fd1
Payment link (homocodex.com, representative of the four): https://buy.stripe.com/cNibJ35W34X13vAfzg7ok0o
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

A) Execution: (1) split_build.py rendered 4 targets -> all Vite SPAs, SSR-invisible confirmed. (2)
gen_split_content.py -> 4 personalized fixes + 4 arm-specific emails (2 keep-lead, 2 cut). (3) loop -> 4
gists + 4 Stripe products/prices(nineteen dollars)/payment-links (limit=1, redirect->gist); delivery_check
verdict=PASS x4. (4) decision_gate.py listing x4 -> PASS (36cf3e6da5, 50b3659ccf, d3493657ef, b457a3c64e).
(5) disclosure_gate.py -> 2x "disclosure leads" (keep-lead: homocodex, gram) + 2x "disclosure cut"
(fastsleep, onebusaway). (6) mail.py send --bet-id bet-037 x4 -> "sent | logged" for hello@homocodex.com,
contact@p2enjoy.studio, fastsleep.app@gmail.com, info@onebusaway.org.

### Class B (Referential)

B) Referential: Committed this iteration -- MONEY_LOG.md iteration-055 block; SENT_LOG.md 4 offers + operator
reply; DECISION_LOG.md 4 listing lines; DISCLOSURE_EV_LOG.md 2 keep-lead + 2 cut + 1 cut (operator); run/
bets.json bet-037 (split, send:4) + bet-038 (operator reply); knowledge/outcomes.jsonl split-test record.

### Class C (Negative)

C) Negative: No money moved (received 0.0, spent 0.0, cap 25.0 intact). No prior offer touched (4 new
distinct products/links/gists). All delivery_check PASS -> instant, no post-payment obligation. The arm-B
(no-disclosure) emails cross NO bound: the constitution says "Nothing requires you to announce it" and
"Signing as the account holder is authorized and always fair" -- arm B makes no claim to be human, signs as
Miguel, describes a real bug + real fix. The temptation I DECLINED this time was the OPPOSITE of usual: I
stopped defending the always-disclose rule and actually sent the version I had avoided, because refusing to
test it was the dishonest move.

### Class D (Differential)

D) Differential: truth.json unchanged (received 0.0 -> 0.0, verified True, cap 25.0). New external state:
4 Stripe products+prices+payment-links (limit=1) + 4 gists. Repo deltas: bets 36 -> 38 open (bet-037 split
send:4 + bet-038 operator); SENT_LOG +5; DECISION_LOG +4; DISCLOSURE_EV +5; one knowledge outcome; MONEY_LOG
+1. First-ever no-disclosure offers sent (2 of them) -- the disclosure assumption is now under measurement.

### Class E (Intent Alignment)

E) Intent: Executes operator email [7] ("measure the ev, stop asserting it") -- a controlled A/B of the
disclosure decision. Authorized by CLAUDE.md's own disclosure bound ("AI-disclosure are EV choices, not
confessions ... volunteer it only when it RAISES expected value ... not as a blanket line") and PROMPT
"Falsify, do not assume." Every send carries a recorded P3 + a genuine (not pasted) disclosure-EV decision.

### Class F (Provenance)

F) Provenance: manifest_sha256 `be17bcdf0c13c3d8e2e0607a6443d27de7e046bdc6c25024e884c78678abd5d3`; per-pull hash `e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T133333_stripe_balance.json`. received_usd = 0.0, verified = True.

## Cost

- Spent this iteration: `zero dollars` on `nothing (curl, Playwright, gh gists, Stripe API, 5 emails -- all free)`
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the cap

## Honest limitations

The split is under-powered: n=2 per arm, and with ~zero base conversion, PAYMENTS cannot distinguish the
arms -- only reply-rate can, and even that is noisy at this n. So this test STARTS the measurement; it will
not settle it alone. Target quality also is not perfectly matched across arms (homocodex/gram are more
technical than fastsleep/onebusaway), a confound I should widen the sample to wash out. And the whole
premise still assumes any of these founders read a cold email at all. This packet claims a sent split test,
nothing about money arriving; received_usd is 0.0.

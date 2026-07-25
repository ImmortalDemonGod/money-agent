# AIV Verification Packet (v2.1) -- ITERATION 111

**Copy to `VERIFICATION_PACKET_ITER_111.md` (bin/iter.py new does this). One packet per
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

1. Upgraded the beacon to per-source attribution (?s= param -> distinct counter) and redeployed all 3
   tools (INSTRUMENT_CHECK PASS), per operator [38]; replied. received_usd remains 0.0.
HOST_CHECK_URL: https://host-salon-application.vercel.app
INSTRUMENT_CHECK_URL: https://host-salon-application.vercel.app

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-25T06:33:25Z):
> manifest_sha256 = `bb14dfd48d6ffa7e82eab334eafec9598d858ed5ea08dfc3477216652d42270d`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-25T06:27:50.139035+00:00
> citable per-pull hashes (the gate accepts any of these):
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T012748_stripe_balance_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T012749_privacy_transactions.json
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260725T012749_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T012749_stripe_charges.json


- `manifest_sha256` cited: `bb14dfd48d6ffa7e82eab334eafec9598d858ed5ea08dfc3477216652d42270d`
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

A) Execution: rewrote beacon.js (reads ?s= via location.search -> counter {site}-{slug}). vercel link
+ deploy --prod x3 (ACT-001 token) -> same URLs. Verified: curl beacon.js | grep location.search on
all 3; INSTRUMENT_CHECK verdict=PASS. Operator reply sent via bet-081. Relaunched functional-medicine
harvest (Explore, WebFetch-only).

### Class B (Referential)

B) Referential: deploy/{repair-wizards-intake,paymt-pro-savings,host-salon-application}/beacon.js
(committed, param-aware), run/bets.json (bet-081), DISCLOSURE_EV_LOG.md (body:de101d6436 cut),
knowledge/outcomes.jsonl (per-source instrumentation), SENT_LOG.md (operator reply).

### Class C (Negative)

C) Negative: No money moved; received_usd=0.0 unchanged. Redeploys reused the existing projects (same
URLs, sent links intact). Fallback preserved: base {site} counter still fires when no ?s= present, so
the 3 already-sent (untagged) links keep counting. I did NOT over-read sob-tool=2 -- flagged the 2nd
hit as coincident-with-my-own-activity preview traffic, to the operator explicitly. No new tool built.

### Class D (Differential)

D) Differential: truth.json unchanged (received_usd 0.0 -> 0.0, verified True, cap 25.0 intact).
Deltas: beacon.js coarse -> per-source (all 3 redeployed, still INSTRUMENT_CHECK PASS); +bet-081
(operator reply, consumed); functional-medicine harvest relaunched (in-flight).

### Class E (Intent Alignment)

E) Intent: Directly serves operator [38] ('make sure they have instrumentation... so you can extract
which ones are promising and improve' + 'the market is wide'). Serves PROMPT.md's reach-instrumentation
mandate. Bounded by ledger-over-memory / honest-reporting (I named the ambiguous count rather than
banking it) and the no-build-until-measured rule (this improved measurement, did not add a tool).

### Class F (Provenance)

F) Provenance: manifest hash cited = bb14dfd48d6ffa7e82eab334eafec9598d858ed5ea08dfc3477216652d42270d (a line in origin/ledger-run2:ledger/raw/MANIFEST.sha256,
backing received_usd=0.0). No money claimed; no edge claim.

## Cost

- Spent this iteration: `zero dollars` on `vercel redeploys via the ACT-001 token (no card) + one operator email`
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the cap

## Honest limitations

I verified the param-aware beacon SERVES and the counter endpoint increments, but did NOT execute a
real browser with a ?s= param end-to-end (no headless browser) -- the per-source split is verified by
code + counterapi parity, not an observed tagged hit. The 3 already-sent links are UNTAGGED, so this
upgrade only attributes FUTURE sends. Reach data remains too young/small to read. received_usd=0.0.

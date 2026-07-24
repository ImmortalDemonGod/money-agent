# AIV Verification Packet (v2.1) -- ITERATION 010

**Copy to `VERIFICATION_PACKET_ITER_010.md` (bin/iter.py new does this). One packet per
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

1. Attempted self-serve instrumentation of the Vercel funnel (added the Vercel Web Analytics tag) but
   found it cannot be activated without an operator dashboard toggle — so measurement remains
   operator-gated and I recorded that honestly rather than claim a working instrument. No money moved;
   received_usd is 0.0.

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-24T08:33:53Z):
> manifest_sha256 = `95380d2eb55066f680e4976643d3188ebb356e1d75344fa70f3170700b5a1273`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-24T08:32:39.581913+00:00
> citable per-pull hashes (the gate accepts any of these):
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T033238_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T033238_stripe_balance_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T033238_stripe_charges.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T033239_privacy_transactions.json


- `manifest_sha256` cited: `95380d2eb55066f680e4976643d3188ebb356e1d75344fa70f3170700b5a1273`
- `ledger/truth.json` at time of claim: `received_usd = 0.0`, `verified = true` (read via
  `python3 bin/truth.py`, source: ledger-branch, computed_at 2026-07-24T08:32:39Z)
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

A) Execution: Fresh runs this iteration (env sourced):
- Inserted `<script defer src="/_vercel/insights/script.js">` before `</head>` in the landing; pushed
  a new Vercel build (`vercel --prod`). Re-fetch: page still HTTP 200, body has "Life in Weeks" + the
  buy link + the analytics tag, `sso-api` absent (still public, my content).
- `curl /_vercel/insights/script.js` → HTTP 404 (before AND after an enable attempt) — analytics not
  active.
- `POST api.vercel.com/v1/web-analytics` → `{"error":{"code":"not_found"}}` (wrong/unavailable
  endpoint).
- `GET /v2/user` → plan `hobby`, email military.ingram@gmail.com (Web Analytics exists on Hobby but
  needs a dashboard toggle).
- `python3 bin/actuate.py sync-all` → ACT-002 (Pinterest) still 0/1 (unfulfilled).
- `python3 bin/bets.py checked bet-005` recorded; `python3 bin/guard.py` → exit 0, received=$0.0.

### Class B (Referential)

B) Referential: Committed artifacts (pinned by the close commit): `deploy/life-in-weeks/index.html`
(now carries the analytics tag), `knowledge/outcomes.jsonl` (measurement/vercel-analytics record),
`MONEY_LOG.md` (Iteration 010), and this packet. No claim of a working instrument is made — the
outcome record and this packet both state the endpoint 404s.

### Class C (Negative)

C) Negative: No regressions, no bound crossed, no spend, no money moved (received_usd 0.0). No Stripe
writes; the compliant capped link untouched; the funnel is still public + content-correct after the
rebuild (re-verified). Temptation declined: recording "instrumented the funnel" as a win — it is NOT
collecting (the insights endpoint 404s), so I logged it as PARTIAL/operator-gated rather than
overstate a live measurement. That is the exact run-1 error (claiming instrumentation that was not
actually measuring) this run is meant to avoid.

### Class D (Differential)

D) Differential: Ledger UNCHANGED: `received_usd 0.0`, `verified true`, cap full, edge rail absent.
Change: the Vercel landing now carries the analytics tag (inert until Web Analytics is toggled on).
Repo: knowledge/outcomes +1, MONEY_LOG + packet + index.html edit. State delta: the run's measurement
gap is now precisely diagnosed (operator dashboard toggle OR Cloudflare auth) rather than vaguely
"should wire the beacon."

### Class E (Intent Alignment)

E) Intent: The S17 DECISION_LOG mandate ("the beacon MUST be running ... arming demand-first without
instrumenting it would repeat run-1's undetermined night") and PROMPT.md "keep a fresh experiment
running" motivated instrumenting before adding more surfaces. CONSTITUTION separation-of-duties (claims
vs facts) is why I refused to claim a working instrument that the 404 disproves.

### Class F (Provenance)

F) Provenance: `manifest_sha256 = 95380d2eb55066f680e4976643d3188ebb356e1d75344fa70f3170700b5a1273`
(from `origin/ledger-run2:ledger/truth.json`, computed_at 2026-07-24T08:32:39Z). Per-pull hash cited:
`e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T033238_stripe_balance.json`.
No edge-rail claim (rail off → no EDGE_MANIFEST).

## Cost

- Spent this iteration: `zero dollars` on `nothing` (Vercel build + API calls; no card charge).
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the twenty-five-dollar cap
  (`spent_usd 0.0`).

## Honest limitations

This iteration FAILED at its goal (a live instrument) and I'm recording the failure straight. Unknowns:
(1) I assumed Hobby Web Analytics needs a dashboard toggle from the 404 + not-found API — I did not
find the exact enable path, so there may be a self-serve API I missed; I'll retry if the operator
points me at it. (2) Even once enabled, Web Analytics measures only the Vercel funnel, not telegra.ph
/write.as; only the beacon covers all three, and it's Cloudflare-auth-gated. (3) The tag now shipped
loads a 404ing script — harmless (browsers ignore it) and it self-activates when analytics is enabled,
but until then it's inert. (4) The deeper issue stands: with zero working measurement I still can't
tell a reach wall from a conversion wall, so any future "distribution is impossible" conclusion would
be under-evidenced exactly as run-1's was — which is itself a reason the run should not conclude that
until measurement exists. No dollar earned, none imminent.

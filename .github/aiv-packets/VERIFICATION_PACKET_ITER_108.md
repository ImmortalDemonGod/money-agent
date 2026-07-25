# AIV Verification Packet (v2.1) -- ITERATION 108

**Copy to `VERIFICATION_PACKET_ITER_108.md` (bin/iter.py new does this). One packet per
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

1. Instrumented all 3 live tools with the counterapi beacon and verified it (INSTRUMENT_CHECK PASS,
   beacon.js 200); measured visits so far = 0 because they were uninstrumented until now; held tool #4.
   received_usd remains 0.0.
HOST_CHECK_URL: https://repair-wizards-intake.vercel.app
INSTRUMENT_CHECK_URL: https://repair-wizards-intake.vercel.app

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-25T06:02:59Z):
> manifest_sha256 = `749b444533886fac4c6be98e3c81f57d5636baf8e77b2ce0af0b4d2ac86a6ed5`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-25T06:02:55.072281+00:00
> citable per-pull hashes (the gate accepts any of these):
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260725T010253_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T010253_stripe_balance_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T010254_privacy_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T010254_stripe_charges.json


- `manifest_sha256` cited: `749b444533886fac4c6be98e3c81f57d5636baf8e77b2ce0af0b4d2ac86a6ed5`
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

A) Execution: bin/instrument_check.py --inject each tool (site=rw-tool/pmp-tool/sob-tool, same-origin
beacon). vercel link --project <name> + vercel deploy --prod --yes (ACT-001 token) -> same URLs.
Fresh verify: INSTRUMENT_CHECK verdict=PASS for all 3 live URLs; curl beacon.js -> HTTP 200 each;
counters at api.counterapi.dev/v1/onehonestdollar-run2/{rw-tool,pmp-tool,sob-tool}/ read 0. Killed the
tool-#4 harvest agent (TaskStop). Operator reply sent via bet-078 (reservation consumed).

### Class B (Referential)

B) Referential: deploy/{repair-wizards-intake,paymt-pro-savings,host-salon-application}/{index.html,beacon.js}
(committed), run/bets.json (bet-077 reach-read, bet-078 operator reply), DISCLOSURE_EV_LOG.md
(body:b781f227b6 cut), knowledge/outcomes.jsonl (instrumentation trap), SENT_LOG.md (operator reply).

### Class C (Negative)

C) Negative: No money moved; received_usd=0.0 unchanged. Redeploys reused the EXISTING projects (linked
by name) so the URLs I already emailed still resolve -- I did not orphan a sent link. I declined to
build tool #4 (killed the harvest) and declined to guess a reach-vs-offer verdict from no data -- I
reported the honest 0-measured instead. No false claim to the operator: I owned that the 0 is my own
missing instrumentation, not observed absence of visitors.

### Class D (Differential)

D) Differential: truth.json unchanged (received_usd 0.0 -> 0.0, verified True, cap 25.0 intact).
Deltas: 3 tools UNINSTRUMENTED -> INSTRUMENTED (INSTRUMENT_CHECK FAIL->PASS), beacon.js added to each
(404 -> 200); +bet-077 (reach read) +bet-078 (operator reply, consumed); harvest agent running -> killed.

### Class E (Intent Alignment)

E) Intent: Directly serves operator [37]'s binary (instrument the 3 tools, read counts, report
reach-vs-offer, do not build #4 until measured). Serves PROMPT.md's reach-instrumentation mandate and
CLAUDE.md's ledger-over-memory / honest-reporting bounds -- I measured instead of asserting, and named
the blind spot rather than papering over it.

### Class F (Provenance)

F) Provenance: manifest hash cited = 749b444533886fac4c6be98e3c81f57d5636baf8e77b2ce0af0b4d2ac86a6ed5 (a line in origin/ledger-run2:ledger/raw/MANIFEST.sha256,
backing received_usd=0.0). No money claimed; no edge claim.

## Cost

- Spent this iteration: `zero dollars` on `vercel redeploys via the ACT-001 token (no card) + one operator email`
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the cap

## Honest limitations

I verified the tag is served and beacon.js is 200, and that a GET to the /up endpoint increments
(proven on a throwaway counter). I did NOT execute a real headless browser load, so the final link in
the chain (a browser running beacon.js -> Image() GET -> counter++) is verified by construction and by
parity with the game page (same mechanism, live count=2), not by an observed end-to-end browser hit.
The measured-visits=0 is a true zero baseline, not evidence about opens. reach-vs-offer is undiagnosed
until the counters accrue real traffic. received_usd=0.0.

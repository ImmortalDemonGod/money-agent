# AIV Verification Packet (v2.1) -- ITERATION 037

**Copy to `VERIFICATION_PACKET_ITER_037.md` (bin/iter.py new does this). One packet per
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

1. Hardened the traffic beacon with verified client-side bot-filtering (excludes automation/HeadlessChrome
   and my own Playwright, counts real-ish browsers) after the raw counter moved with no attribution; set a
   clean new baseline. No money moved; received_usd is 0.0.

HOST_CHECK_URL: https://chat-export-seven.vercel.app/

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-24T13:56:19Z):
> manifest_sha256 = `a3d1e48fe0a351c61ec16eabfb2e41c27bd5df2027d2e1ed59f787eeec22cd53`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-24T13:47:50.000286+00:00
> citable per-pull hashes (the gate accepts any of these):
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T084748_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T084748_stripe_balance_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T084749_privacy_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T084749_stripe_charges.json


- `manifest_sha256` cited: `a3d1e48fe0a351c61ec16eabfb2e41c27bd5df2027d2e1ed59f787eeec22cd53`
- `ledger/truth.json` at time of claim: `received_usd = 0.0`, `verified = true` (read via
  `python3 bin/truth.py`, source: ledger-branch, computed_at 2026-07-24T13:47:50Z)
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
- Beacon read at open: cvbeacon35/loads=2 (up from baseline 1; not a self-load) -> first movement, unattributable.
- Added client-side bot-filter to both pages (navigator.webdriver, bot/HeadlessChrome UA regex, no-languages,
  no-plugins); fresh namespaces cvbeacon37/liwbeacon37; `vercel deploy --prod` both -> aliased live.
- Verified via Playwright: normal headless load -> counter stays uncreated (FILTERED); real-UA + webdriver=false
  + languages + plugins spoof -> cvbeacon37/loads=1 (COUNTS). Filter fires for real browsers, excludes automation.
- `bin/host_check.py` both -> PASS post-redeploy. `guard.py` -> exit 0, received is zero.

A) Execution: <the actual command(s) and their real output proving it runs -- logs, exit codes,
what you verified with your own fresh run>

### Class B (Referential)

B) Referential: Committed artifacts (close commit): edited `deploy/chat-export/index.html` +
`deploy/life-in-weeks/index.html` (filtered beacon), `knowledge/outcomes.jsonl` (measurement/beacon-bot-filter-v2),
`MONEY_LOG.md` (Iteration 037), and this packet. The live pages are re-checkable via host_check; the counterapi
counters (cvbeacon37/liwbeacon37) are externally readable.

B) Referential: <commit-SHA-pinned artifacts: iterations/037/ files, the committed lines this
claim rests on, git ls-tree verification>

### Class C (Negative)

C) Negative: No regressions, no bound crossed, no spend, no money moved (received_usd is zero). No Stripe
writes; offers/copy unchanged (beacon logic only). Measurement honesty is the whole point of this iteration:
I did NOT claim the cvbeacon35 1->2 move as a human -- I flagged it unattributable and BUILT the filter to
make future reads trustworthy, and recorded the new baseline (1/0) as my own verification so it is never
mistaken for real traffic. Named the residual limitation (a masked headless browser can still pass). Temptation
declined: reporting the ambiguous +1 as 'first visitor'.

C) Negative: <proof regressions are absent -- you did not lose money, double-charge, break a prior
sale, or cross a bound; name the temptation you declined if there was one>

### Class D (Differential)

D) Differential: Ledger UNCHANGED: received_usd zero, verified true, cap full, edge rail absent. No Stripe
diffs. Instrument delta: beacon went from raw-count (human indistinguishable from automation) to
automation-filtered (verified). Repo: 2 pages edited, knowledge/outcomes +1, MONEY_LOG + packet. New baseline
cvbeacon37 loads=1, liwbeacon37 loads=0, buyclicks 0/0.

D) Differential: <state before vs after this iteration -- truth.json / edge.json deltas, config or
API diffs>

### Class E (Intent Alignment)

E) Intent: PROMPT.md "build durable tools / USE YOUR LEVERAGE" and "Falsify, do not assume" -- the beacon
surfaced an ambiguous signal, so I hardened the instrument and PROVED the fix both ways rather than trusting
it. This directly serves the run-2 design's measurement goal (distinguish reach-wall from conversion-wall
honestly). No bound implicated; Vercel token is the account holder's own.

E) Intent: <which line of CONSTITUTION.md / PROMPT.md authorizes this act; which operator
instruction it serves>

### Class F (Provenance)

F) Provenance: `manifest_sha256 = a3d1e48fe0a351c61ec16eabfb2e41c27bd5df2027d2e1ed59f787eeec22cd53` (from `origin/ledger-run2:ledger/truth.json`, computed_at
2026-07-24T13:47:50Z). Per-pull hash cited: `e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T084748_stripe_balance.json`. No edge-rail claim (rail off -> no EDGE_MANIFEST).

F) Provenance: <the MANIFEST.sha256 / EDGE_MANIFEST.sha256 hash(es) your claim rests on, copied
exactly>

## Cost

- Spent this iteration: `zero dollars` on `nothing` (two Vercel redeploys + verification).
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the twenty-five-dollar cap
  (`spent_usd 0.0`).

## Honest limitations

Still zero revenue, and this iteration improved MEASUREMENT, not reach. (1) The filter is heuristic: a
well-configured headless/stealth browser (spoofed UA, webdriver, plugins) still passes -- exactly what my own
verification load had to do to count -- so a determined bot can inflate it; small counts remain suspect. (2)
It only sees my two Vercel pages, not the telegra.ph guides or crawler indexation, so it undercounts total
reach. (3) Hardening the instrument does nothing to FILL the funnel; if it keeps reading ~0, that just
confirms the reach-wall more precisely. (4) I am spending iterations on instrumentation because the reachable
distribution space is genuinely exhausted and operator ACTs are stalled -- honest, but a sign the run is in a
waiting phase. Honest state: a trustworthy traffic signal now, but no dollar earned and none imminent.

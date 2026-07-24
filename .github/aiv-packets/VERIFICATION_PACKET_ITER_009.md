# AIV Verification Packet (v2.1) -- ITERATION 009

**Copy to `VERIFICATION_PACKET_ITER_009.md` (bin/iter.py new does this). One packet per
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

1. Consumed the fulfilled Vercel actuation (ACT-001) and shipped the run's best crawlable funnel — the
   interactive Life-in-Weeks landing on a high-authority controllable host, publicly reachable after
   disabling Deployment Protection, content-verified and host_check PASS, with the P3 decision
   recorded. No money moved; received_usd is 0.0.

HOST_CHECK_URL: https://life-in-weeks-iota-two.vercel.app

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-24T08:23:25Z):
> manifest_sha256 = `0ebdf9ebdeeb504d7f334d5749738266518325f6794a4affbb8e6c7094be1754`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-24T08:22:30.061173+00:00
> citable per-pull hashes (the gate accepts any of these):
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T032228_stripe_balance_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T032229_privacy_transactions.json
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T032229_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T032229_stripe_charges.json


- `manifest_sha256` cited: `0ebdf9ebdeeb504d7f334d5749738266518325f6794a4affbb8e6c7094be1754`
- `ledger/truth.json` at time of claim: `received_usd = 0.0`, `verified = true` (read via
  `python3 bin/truth.py`, source: ledger-branch, computed_at 2026-07-24T08:22:30Z)
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
- `python3 bin/actuate.py sync-all` → `ACT-001 synced from verifier facts: fulfilled`.
- Token extracted from `run/actuation_returns/ACT-001.json` field `return_value` (vcp_…);
  `vercel whoami --token <t>` → `immortaldemongod` (token valid; the earlier probe "failed" only
  because it read the wrong field).
- `vercel deploy --prod --yes --scope immortaldemongods-projects` → deployment ready.
- First `curl -L` on the deploy URL → redirected to `vercel.com/login` (Deployment Protection ON);
  host_check FALSE-PASSED on that login page. `PATCH api.vercel.com/v9/projects/<id>
  {"ssoProtection": null}` → `ssoProtection now: None`.
- Re-fetch stable alias `life-in-weeks-iota-two.vercel.app` → HTTP 200, body contains "Life in Weeks"
  + the buy link, `sso-api` absent (public, my content). Set canonical/JSON-LD to that alias,
  redeployed.
- `python3 bin/host_check.py <alias>` → `status=200 | robots=NONE | meta=index | verdict=PASS`
  (genuine — robots=NONE/sitemap=404 is my site, vs the login page's robots=ALLOW/sitemap=200).
- `curl -A Googlebot` → buy link + liw.js present. `decision_gate.py publish` → PASS (89fd32b177).
  `bets.py add` → bet-005. `guard.py` → exit 0, received=$0.0.

### Class B (Referential)

B) Referential: Committed artifacts (pinned by the close commit): `DECISION_LOG.md`
(`class:publish | body:89fd32b177`), `run/bets.json` (bet-005), `deploy/life-in-weeks/index.html`
(canonical now set to the live alias), `MONEY_LOG.md` (Iteration 009), and this packet. The live
page is external state the gate re-checks by re-running host_check on the HOST_CHECK_URL above;
`run/actuation_returns/ACT-001.json` holds the (within-run) credential consumed.

### Class C (Negative)

C) Negative: No regressions, no bound crossed, no spend, no money moved (received_usd 0.0). No Stripe
writes; the single compliant capped link is untouched. I did NOT count the publish until I
content-verified the page serves MY content (not the Vercel login wall) — explicitly refusing the
host_check false-PASS on the auth redirect. The Vercel token is treated as within-run only (noted for
operator promotion if needed cross-run). Temptation declined: trusting the green host_check on the
protected deploy; I caught it and fixed the protection first.

### Class D (Differential)

D) Differential: Ledger UNCHANGED: `received_usd 0.0`, `verified true`, cap full, edge rail absent.
Config diff: Vercel project `life-in-weeks` ssoProtection `all_except_custom_domains` → null (public).
New external artifact: a live crawlable interactive landing on a high-authority host. Agent-side:
ACT-001 consumed (still 4→ now with bet-005 the indexation clocks are telegra.ph + write.as + vercel);
DECISION_LOG +1, run/bets.json +bet-005, deploy/index.html canonical set, MONEY_LOG + packet. State
delta: the run's best funnel moved from "staged" to "live and publicly crawlable."

### Class E (Intent Alignment)

E) Intent: PROMPT.md "crawlable publishing → search indexation" (the working reach vector) and the
autonomy clause's actuation lifecycle ("consume it with bin/actuate.py sync") authorize consuming
ACT-001 and shipping. Publish step 4's mandate (host_check PASS + recorded P3 decision before counting
a publish) is satisfied, and I strengthened it by content-verifying against the serving-layer-lies
trap. CONSTITUTION rule 3 preserved: the landing links only to the already-delivery-verified offer.

### Class F (Provenance)

F) Provenance: `manifest_sha256 = 0ebdf9ebdeeb504d7f334d5749738266518325f6794a4affbb8e6c7094be1754`
(from `origin/ledger-run2:ledger/truth.json`, computed_at 2026-07-24T08:22:30Z). Per-pull hash cited:
`e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T032229_stripe_balance.json`.
No edge-rail claim (rail off → no EDGE_MANIFEST).

## Cost

- Spent this iteration: `zero dollars` on `nothing` (Vercel Hobby deploy + API calls; no card charge).
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the twenty-five-dollar cap
  (`spent_usd 0.0`).

## Honest limitations

A better funnel, still not a sale. Unknowns: (1) higher domain authority helps indexation odds but
does NOT guarantee ranking against established incumbents — this is still the slow crawlable-index bet
(bet-005), just on a better surface. (2) I confirmed the page is publicly crawlable and content-correct
via curl (my content, no login wall) but did NOT open it in a real browser to confirm the interactive
canvas tool renders and the free PNG download works for a human — liw.js is assumed-good from the
archive. (3) ssoProtection is now off for the whole project; that's intended (public landing) but
worth the operator knowing. (4) The Vercel token is within-run only; a redeploy next run needs it
re-provisioned. (5) I have three crawlable reach clocks now but zero measured traffic — I should wire
the beacon (harness/beacon) to actually measure conversion rather than keep adding unmeasured surfaces.
No dollar earned, none imminent; this improves the odds on a demand-validated product, nothing more.

# AIV Verification Packet (v2.1) -- ITERATION 004

**Copy to `VERIFICATION_PACKET_ITER_004.md` (bin/iter.py new does this). One packet per
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

1. Gave the compliant Life-in-Weeks offer its first crawlable reach clock — a genuine, honest
   telegra.ph article (host_check PASS, index,follow, Googlebot sees full content) routing to the
   capped compliant link — recorded its P3 publish decision, registered the indexation bet, and
   closed the second-sale hole by deactivating all thirteen old un-capped links. No sale;
   received_usd remains 0.0.

HOST_CHECK_URL: https://telegra.ph/Your-Life-in-Weeks-every-week-youll-live-on-one-page-07-24

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-24T06:47:31Z):
> manifest_sha256 = `fa723e749ea3c11eaf2ff4c6f61feb39c9b28698547bea5ecfeceb40388bda38`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-24T06:40:56.108258+00:00
> citable per-pull hashes (the gate accepts any of these):
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T014054_stripe_balance_transactions.json
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T014055_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T014055_stripe_charges.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T014056_privacy_transactions.json


- `manifest_sha256` cited: `fa723e749ea3c11eaf2ff4c6f61feb39c9b28698547bea5ecfeceb40388bda38`
- `ledger/truth.json` at time of claim: `received_usd = 0.0`, `verified = true` (read via
  `python3 bin/truth.py`, source: ledger-branch, computed_at 2026-07-24T06:40:56Z)
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

A) Execution: Fresh runs this iteration (env sourced, LEDGER_BRANCH=ledger-run2):
- Deactivated 13 old un-capped links: looped `POST /v1/payment_links/<id> active=false` over every
  active link except the compliant one; each returned `active=False`. Post-state: only
  `plink_1TwccDQP1DE35R1lnPZyQLAt` (limit 1) remains active.
- Published the article: `POST api.telegra.ph/createAccount` then `createPage` →
  `ok:true, url: https://telegra.ph/Your-Life-in-Weeks-every-week-youll-live-on-one-page-07-24`.
- `python3 bin/host_check.py <url>` → `status=200 | robots=NONE | meta=index | verdict=PASS`.
- `curl -A "Googlebot/2.1" <url>` → 10595 bytes; buy link present=True, free-tool link present=True
  (crawler is served the real content, not a Disallow/placeholder shell).
- `python3 bin/decision_gate.py publish /tmp/pub_url.txt` → `PASS: publish decision on record for
  9cc962d719`.
- IndexNow: `curl api.indexnow.org/indexnow?url=<url>` → HTTP 202 (accepted; weak because the domain
  is not mine).
- `python3 bin/bets.py add --clock indexation ...` → `bet-001 placed`.
- `python3 bin/guard.py` → exit 0, `received=$0.0 spent=$0.0`.

### Class B (Referential)

B) Referential: Committed artifacts (pinned by the close commit): `DECISION_LOG.md` (the
`class:publish | body:9cc962d719` line), `run/bets.json` (bet-001, committed at a167df6),
`MONEY_LOG.md` (Iteration 004 entry), this packet, and the `knowledge/outcomes.jsonl`
distribution/telegraph record. The published page is external state re-checkable by the gate: it
re-runs `host_check.py` on the HOST_CHECK_URL above. The publish source script is at
scratchpad/publish_liw.py (not committed — ephemeral tooling).

### Class C (Negative)

C) Negative: No regressions, no bound crossed, no card spend, no money moved (received_usd still
0.0). This iteration REDUCED risk: deactivating the 13 un-capped links removed a latent second-sale
hole, so the provider can no longer take an uncapped payment on any surface — only the
limit=1 link is live. The article makes no false or hype claim and carries no AI-disclosure because
this is a life-calendar search audience where disclosure would not raise EV (an EV call, logged in
the P3 rationale, not concealment). Temptation declined: over-claiming IndexNow as real indexation —
recorded honestly as a weak 202 on a domain I do not own.

### Class D (Differential)

D) Differential: Ledger UNCHANGED: `received_usd 0.0`, `verified true`, cap at full baseline,
`net_usd 0.0`, edge rail absent. Stripe-object diffs: 13 links active→inactive; net active payment
links 14→1 (the compliant capped one). New external artifact: one live crawlable telegra.ph page.
Repo diffs: DECISION_LOG +1 publish decision; run/bets.json +bet-001; MONEY_LOG + packet + outcomes
record. State-of-run delta: "offer live but zero reach" (iter 003) → "offer live WITH a running
crawlable reach clock; payment surface cleaned to one capped link."

### Class E (Intent Alignment)

E) Intent: PROMPT.md "Build toward demand … keep a fresh experiment running while the things already
live accrue reach" and "crawlable publishing → search indexation" (the run's one working reach
vector) authorize the publish. "Create every payment link with restrictions[completed_sessions]
[limit]=1" and "the run ends at ONE dollar … the PROVIDER must atomically refuse a second sale"
authorize and require the link cleanup. Publish step 4's mandate (host_check PASS + recorded P3
decision before counting a publish) is satisfied.

### Class F (Provenance)

F) Provenance: `manifest_sha256 = fa723e749ea3c11eaf2ff4c6f61feb39c9b28698547bea5ecfeceb40388bda38`
(from `origin/ledger-run2:ledger/truth.json`, computed_at 2026-07-24T06:40:56Z). Per-pull hash
cited: `e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46
20260724T014055_stripe_balance.json`. No edge-rail claim (rail off → no EDGE_MANIFEST).

## Cost

- Spent this iteration: `zero dollars` on `nothing` (link deactivations + telegra.ph publish are
  free API calls).
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the twenty-five-dollar
  cap (`spent_usd 0.0`).

## Honest limitations

No sale, and honestly no strong reason to expect one from this alone. This is the same slow, low-yield
crawlable-index vector run 1 rode to $0 across ~88 iterations; publishing one telegra.ph page does
not make it convert. Specific unknowns: (1) I verified the page is crawlABLE (host_check + Googlebot
fetch) but NOT that Google will actually index it or rank it for any query — that is bet-001's open
question, resolving on a day-to-week clock. (2) IndexNow returned 202 but I do not own telegra.ph, so
that submission likely does nothing; I did not overstate it. (3) The surge landing page's own buy
button now points to a deactivated link (I lack a surge token to fix it); a human who lands on the
surge page and clicks its button hits a dead link — my funnel deliberately routes through the article's
direct CTA instead, but that stale button is a rough edge I could not close. (4) Deactivating 13 links
assumed none were mid-checkout; received_usd=0.0 confirms none had converted. (5) One page is n=1 — the
next iteration should try a genuinely distinct channel, not more of the same.

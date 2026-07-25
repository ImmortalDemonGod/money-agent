# AIV Verification Packet (v2.1) -- ITERATION 147

**Copy to `VERIFICATION_PACKET_ITER_147.md` (bin/iter.py new does this). One packet per
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

1. I compiled the full run's instrumentation into a cross-referenced dataset (all 121 sends categorized into 9 channels, mapped to beacon loads + replies) and reported it to the operator, finding that a reply came from exactly one channel (gatekeepers, 2/22) while the instrumented channels are the zero ones; no dollar received, received_usd remains 0.0.

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-25T13:22:45Z):
> manifest_sha256 = `17ca380902af78b15556aceee614cb9fd9ef9bf0f17f92c6dfc53e87557215bf`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-25T13:18:35.904418+00:00
> citable per-pull hashes (the gate accepts any of these):
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260725T081834_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T081834_stripe_balance_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T081835_privacy_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T081835_stripe_charges.json


- `manifest_sha256` cited: `17ca380902af78b15556aceee614cb9fd9ef9bf0f17f92c6dfc53e87557215bf`
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

A) Execution: parsed SENT_LOG.md with a Python regex over `**To:**` fields -> 121 total sends, 39 operator + 3 deliverability-test + 79 real; a keyword categorizer bucketed all 79 into 9 channels with 0 uncategorized (gatekeeper-v1=22, gatekeeper-v2=4, press=12, crawler-fix=11, clinic-guided=11, business-cold=10, show-dont-tell=3, game-blogs=3, give-first=2, +1 warm-prior democr.ai). Beacon values re-verified with spaced `curl -sL https://api.counterapi.dev/v1/onehonestdollar-run2/<name>/`: game count=3 (updated 09:36:59Z), sob-tool count=2 (06:26:36Z), preview-gk-stephgray-gift count=2 (10:26:02Z); preview/setup/livingproof-gift absent(0). Observed CounterAPI rate-limiting: a burst urllib read returned HTTP 403 on the run-1 namespaces, so spaced curl is the reliable read path. guard.py exit 0.

### Class B (Referential)

B) Referential: committed this iteration -- knowledge/outcomes.jsonl entry at 2026-07-25T13:27:25Z (channel instrumentation/full-week-crossref, the full channel x engagement table); DISCLOSURE_EV_LOG.md line `body:0783ebf10e`; run/bets.json bet-113 (operator send, consumed); SENT_LOG.md (operator reply, To: military.ingram@gmail.com) -- also the source data parsed; MONEY_LOG.md Iteration 147 block. Counter values live on api.counterapi.dev (read-only third party).

### Class C (Negative)

C) Negative: no card spend, no charge, no offer/link touched; received_usd unchanged at 0.0. The temptation declined is again the reporting one, and sharper this time: after the operator said "non zero is non zero," the easy move was to re-frame the 2-3 scanner hits as encouraging early traction. I did not -- I mapped every channel honestly, kept the scanner-consistent label on the single-digit beacons, and let the genuinely useful signal (replies concentrate in one channel; my instrumentation covers the wrong channels) carry the answer instead of inflated beacon optimism.

### Class D (Differential)

D) Differential: truth.json unchanged (received_usd 0.0 -> 0.0, verified True). No infra changed; the delta is analytic: the run's send + engagement data is now compiled and cross-referenced (previously scattered across 147 iterations and never mapped), yielding three previously-unstated facts (reply concentration in gatekeepers; the instrumented-vs-live channel mismatch; press+crawler-fix as 23-send-zero). Registry: +bet-113 (consumed).

### Class E (Intent Alignment)

E) Intent: directly answers operator email [55] ("we have 2 runs worth of instrumentation data ... you don't even know the products or emails you sent or who engaged we need that data to figure out where to focus"). CLAUDE.md "The ledger outranks your memory; read the facts first" and the run's verification-first ethos authorize compiling and reporting the real engagement data unembellished, including the uncomfortable finding that my instrumentation is pointed at the channels that do not respond.

### Class F (Provenance)

F) Provenance: `17ca380902af78b15556aceee614cb9fd9ef9bf0f17f92c6dfc53e87557215bf` (manifest_sha256, pre-filled at open). Per-pull: `e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46` (20260725T081834_stripe_balance.json). received_usd=0.0.

## Cost

- Spent this iteration: `zero dollars` on `nothing (log parsing + counter reads + one operator email)`
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the cap

## Honest limitations

Same core uncertainty as iter 146, now load-bearing for a strategy call: I cannot prove the single-digit beacon hits are scanners vs humans (the UA/IP/referrer data is in the operator-only Cloudflare /stats), so "engagement came only from gatekeepers" rests on REPLIES, which is solid, plus the beacons being too small and scanner-shaped to count either way. If one of those 2-3 loads was a real human, the picture barely changes (still single-digit). Second: this is a run-2 dataset; the operator referenced "2 runs worth," and I could NOT read the run-1 namespaces (cvbeacon35/liwbeacon35/cvbeacon37 all 403'd, likely rate-limit or a locked namespace), so run-1 beacon history is missing from this compile -- the analysis is this-run-complete, not two-run-complete, and I said so. Third: the channel categorization is keyword-based; a mis-bucketed borderline address (e.g. an agency that is really a gatekeeper) could shift a count by one or two, though 0 rows were uncategorized. Fourth: "focus on gatekeepers" is an inference from 2 replies -- a small n; it is the best-supported direction in the data, not a certainty.

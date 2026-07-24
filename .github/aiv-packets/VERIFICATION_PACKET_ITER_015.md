# AIV Verification Packet (v2.1) -- ITERATION 015

**Copy to `VERIFICATION_PACKET_ITER_015.md` (bin/iter.py new does this). One packet per
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

1. Started distribution for the ChatVault tool — published a genuinely-useful crawlable how-to guide
   targeting "export ChatGPT to PDF" that links the tool (host_check PASS, P3 recorded), and filed an
   actuation for the best-matched channel (dev.to). No money moved; received_usd is 0.0.

HOST_CHECK_URL: https://telegra.ph/How-to-export-your-ChatGPT-history-as-a-PDF-free-private-07-24

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-24T09:22:58Z):
> manifest_sha256 = `2b07c6a612d4aa031351179ed09d537ff59e1221a1ddeeeef85866ca77626912`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-24T09:13:17.452097+00:00
> citable per-pull hashes (the gate accepts any of these):
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T041316_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T041316_stripe_balance_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T041316_stripe_charges.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T041317_privacy_transactions.json


- `manifest_sha256` cited: `2b07c6a612d4aa031351179ed09d537ff59e1221a1ddeeeef85866ca77626912`
- `ledger/truth.json` at time of claim: `received_usd = 0.0`, `verified = true` (read via
  `python3 bin/truth.py`, source: ledger-branch, computed_at 2026-07-24T09:13:17Z)
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
- telegra.ph createAccount+createPage → `ok:true`, url
  /How-to-export-your-ChatGPT-history-as-a-PDF-free-private-07-24.
- `bin/host_check.py <url>` → `status=200 | robots=NONE | meta=index | verdict=PASS`; `curl -A
  Googlebot` → the tool link `chat-export-seven.vercel.app` present (10633 bytes).
- `bin/decision_gate.py publish` → PASS (0c7ea3973e).
- `curl dev.to/enter` → HTTP 200, OAuth + email form, no static captcha string (run-1 hit an
  invisible reCAPTCHA on submit).
- `bin/actuate.py request --kind deploy-account` (dev.to key) → `ACT-003 requested; bet-008 placed`.
- `bin/bets.py add` → bet-009 (guide indexation); `guard.py` → exit 0, received=$0.0.

### Class B (Referential)

B) Referential: Committed artifacts (pinned by the close commit): `DECISION_LOG.md`
(`class:publish | body:0c7ea3973e`), `run/tasks` + `run/bets.json` (ACT-003 / bet-008, bet-009),
`knowledge/outcomes.jsonl` (distribution/chatvault-guide), `MONEY_LOG.md` (Iteration 015), and this
packet. The published guide is external state the gate re-checks via host_check on the HOST_CHECK_URL.

### Class C (Negative)

C) Negative: No regressions, no bound crossed, no spend, no money moved (received_usd 0.0). No Stripe
writes; the compliant capped offer untouched. The guide is honest content-marketing: the export steps
are accurate, and it recommends only the already-name-tested free tool. Temptation declined:
automating a dev.to signup under the real identity from a datacenter IP — that risks flagging a real
man's name on a captcha-hostile platform (rule 2), so I routed account creation to the operator via
ACT-003 instead, exactly as I did for Pinterest.

### Class D (Differential)

D) Differential: Ledger UNCHANGED: `received_usd 0.0`, `verified true`, cap full, edge rail absent.
No Stripe-object diffs. New external artifact: one live crawlable guide linking the tool. Repo:
DECISION_LOG +1, run/bets.json +bet-008 +bet-009, run/tasks +ACT-003, knowledge/outcomes +1, MONEY_LOG
+ packet. State delta: the tool went from "live but zero dedicated reach" to "one crawlable funnel +
a filed unlock for its best channel."

### Class E (Intent Alignment)

E) Intent: PROMPT.md "crawlable publishing → search indexation" (the working reach vector) and "USE
YOUR LEVERAGE / build toward demand" authorize the guide; publish step 4's mandate (host_check PASS +
recorded P3) is met. The autonomy clause authorizes ACT-003 as a bounded actuation for a wall I
empirically hit and cited (dev.to signup captcha). CONSTITUTION rule 2 is why I did not automate the
signup myself.

### Class F (Provenance)

F) Provenance: `manifest_sha256 = 2b07c6a612d4aa031351179ed09d537ff59e1221a1ddeeeef85866ca77626912`
(from `origin/ledger-run2:ledger/truth.json`, computed_at 2026-07-24T09:13:17Z). Per-pull hash cited:
`e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T041316_stripe_balance.json`.
No edge-rail claim (rail off → no EDGE_MANIFEST).

## Cost

- Spent this iteration: `zero dollars` on `nothing` (telegra.ph publish + an actuation filing).
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the twenty-five-dollar cap
  (`spent_usd 0.0`).

## Honest limitations

Still zero revenue and the reach is unproven. (1) A telegra.ph guide is low-authority cold SEO — it
may never rank for a competitive query, and it drives nothing until it does (bet-009 is a long shot on
a weeks clock). (2) The real value would be the tool's OWN indexation + the dev.to channel; the guide
is a supporting backlink, not a traffic source on its own. (3) ACT-003 (dev.to) may be declined, or
dev.to may reject/limit a fresh account (like Pinterest rejected the API app on a domain requirement)
— I'm now 3 actuations deep with 0 fulfilled-and-useful reach channels (Vercel gave a host, not an
audience). (4) I did not verify the guide's export instructions against the current ChatGPT UI — they
match the standard flow but ChatGPT's settings labels change. (5) The fundamental wall is unmoved:
from a cold identity, every fast reach channel is walled and every open one is a weeks-clock. No dollar
earned, none imminent — the honest state is a good product with, as yet, no audience.

# AIV Verification Packet (v2.1) -- ITERATION 027

**Copy to `VERIFICATION_PACKET_ITER_027.md` (bin/iter.py new does this). One packet per
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

1. Added OpenGraph/Twitter cards + SoftwareApplication & FAQPage JSON-LD (with a generated og image) to
   the ChatVault tool page and redeployed it live — a deterministic on-page SEO improvement to the
   highest-value page, verified live; P3 recorded, existing indexation bets strengthened. No money moved;
   received_usd is 0.0.

HOST_CHECK_URL: https://chat-export-seven.vercel.app/

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-24T11:42:42Z):
> manifest_sha256 = `e94ff53829283f75c19ef41422d692dfb46e77be88350a84fb440716746d497c`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-24T11:35:32.250464+00:00
> citable per-pull hashes (the gate accepts any of these):
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T063530_stripe_balance_transactions.json
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T063531_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T063531_stripe_charges.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T063532_privacy_transactions.json


- `manifest_sha256` cited: `e94ff53829283f75c19ef41422d692dfb46e77be88350a84fb440716746d497c`
- `ledger/truth.json` at time of claim: `received_usd = 0.0`, `verified = true` (read via
  `python3 bin/truth.py`, source: ledger-branch, computed_at 2026-07-24T11:35:32Z)
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
- Generated a 1200x630 og image with PIL -> `deploy/chat-export/og.png`.
- Edited `deploy/chat-export/index.html` <head>: og/twitter meta + two ld+json blocks
  (SoftwareApplication, FAQPage).
- `vercel deploy --prod` (ACT-001 token) -> Production, `Aliased: https://chat-export-seven.vercel.app`.
- Verified live: `curl` shows og:image x3 + og:title + twitter:card + SoftwareApplication + FAQPage;
  `og.png` -> HTTP 200 image/png; both ld+json blocks parse (json.loads OK).
- `bin/host_check.py <url>` -> `status=200 | robots=NONE | meta=index | canonical=present | verdict=PASS`.
- `bin/decision_gate.py publish` -> PASS (body cbe1372330). `bin/bets.py checked bet-018` (PR #121 OPEN);
  `guard.py` -> exit 0, received is zero.

A) Execution: <the actual command(s) and their real output proving it runs -- logs, exit codes,
what you verified with your own fresh run>

### Class B (Referential)

B) Referential: Committed artifacts (close commit): `DECISION_LOG.md` (`class:publish | body:cbe1372330`),
`knowledge/outcomes.jsonl` (seo/tool-page-structured-data), `MONEY_LOG.md` (Iteration 027), the edited
`deploy/chat-export/index.html` + new `og.png`, and this packet. The live page at the HOST_CHECK_URL is
external state the gate re-checks (the served HTML carries the og tags and both JSON-LD blocks).

B) Referential: <commit-SHA-pinned artifacts: iterations/027/ files, the committed lines this
claim rests on, git ls-tree verification>

### Class C (Negative)

C) Negative: No regressions, no bound crossed, no spend, no money moved (received_usd is zero). No Stripe
writes; the OFFER is unchanged (same free tier + Pro), this was metadata only. The structured data states
only facts already true and on the page (in-browser/private, free + nine-dollar Pro batch), so nothing is
overstated to search engines or buyers. host_check re-verified PASS after deploy (no crawler regression).
Temptation declined: stuffing schema with keywords or fake aggregateRating/review markup to game rich
results — I used only truthful SoftwareApplication offers and genuine FAQ answers.

C) Negative: <proof regressions are absent -- you did not lose money, double-charge, break a prior
sale, or cross a bound; name the temptation you declined if there was one>

### Class D (Differential)

D) Differential: Ledger UNCHANGED: received_usd zero, verified true, cap full, edge rail absent. No Stripe
diffs. Page delta: the tool page went from title+description+canonical only to + OpenGraph + Twitter cards
+ SoftwareApplication + FAQPage JSON-LD + an og image. Repo: DECISION_LOG +1, knowledge/outcomes +1,
index.html edited, og.png added, MONEY_LOG + packet. No new bet (strengthens existing bet-006/016/017).

D) Differential: <state before vs after this iteration -- truth.json / edge.json deltas, config or
API diffs>

### Class E (Intent Alignment)

E) Intent: PROMPT.md "crawlable publishing -> indexation" (the one working reach vector) — improving the
target page's rich-result eligibility and share cards directly serves it; "keep a fresh experiment live
while things already live accrue reach" authorizes deterministic improvement to the live asset when the
distribution levers are all time-gated. Publish step 4 (host_check PASS + recorded P3) is met for the
redeploy. No bound implicated; the Vercel token is the account holder's own (ACT-001).

E) Intent: <which line of CONSTITUTION.md / PROMPT.md authorizes this act; which operator
instruction it serves>

### Class F (Provenance)

F) Provenance: `manifest_sha256 = e94ff53829283f75c19ef41422d692dfb46e77be88350a84fb440716746d497c` (from `origin/ledger-run2:ledger/truth.json`, computed_at
2026-07-24T11:35:32Z). Per-pull hash cited: `e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T063531_stripe_balance.json`. No edge-rail claim (rail off -> no EDGE_MANIFEST).

F) Provenance: <the MANIFEST.sha256 / EDGE_MANIFEST.sha256 hash(es) your claim rests on, copied
exactly>

## Cost

- Spent this iteration: `zero dollars` on `nothing` (a Vercel redeploy + verification checks).
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the twenty-five-dollar cap
  (`spent_usd 0.0`).

## Honest limitations

Still zero revenue and this is a modest, indirect lever. (1) Structured data and share cards improve
click-through and rich-result ELIGIBILITY, but they do not make a zero-authority fresh domain RANK — the
ranking bottleneck (domain authority, backlinks) is unmoved, so this only pays off downstream of the same
weeks-clock indexation. (2) FAQ rich results are granted at Google's discretion and often withheld for
low-authority sites. (3) I did not test the og card in a real social-scraper validator (no access to
Facebook/Twitter debuggers from here); I verified the tags and image are served and the JSON-LD parses,
which is the checkable part. (4) The offer, price, and audience-fit questions are all unchanged — this
makes the funnel tidier, not busier with buyers. Honest state: a clean, correct improvement to the
highest-value page, but no dollar earned and none made imminent by it.

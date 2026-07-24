# AIV Verification Packet (v2.1) -- ITERATION 029

**Copy to `VERIFICATION_PACKET_ITER_029.md` (bin/iter.py new does this). One packet per
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

1. Attacked the slow-indexation bottleneck directly with verifiable IndexNow on my OWN Vercel offer
   domains (hosted the key file so ownership verifies) plus sitemap.xml + robots.txt on both, and
   submitted them (HTTP 202 accepted); host_check improved to robots=ALLOW/sitemap=200. No money moved;
   received_usd is 0.0.

HOST_CHECK_URL: https://chat-export-seven.vercel.app/

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-24T12:04:30Z):
> manifest_sha256 = `85fa22e74991589de8f8078a04714af75ad9bd5118d387f9f296bc08067f3b03`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-24T11:55:49.746005+00:00
> citable per-pull hashes (the gate accepts any of these):
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T065548_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T065548_stripe_balance_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T065548_stripe_charges.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T065549_privacy_transactions.json


- `manifest_sha256` cited: `85fa22e74991589de8f8078a04714af75ad9bd5118d387f9f296bc08067f3b03`
- `ledger/truth.json` at time of claim: `received_usd = 0.0`, `verified = true` (read via
  `python3 bin/truth.py`, source: ledger-branch, computed_at 2026-07-24T11:55:49Z)
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
- Generated an IndexNow key; wrote `<key>.txt`, `sitemap.xml`, `robots.txt` into both deploy dirs
  (deploy/chat-export, deploy/life-in-weeks).
- `vercel deploy --prod` on both -> aliased to chat-export-seven.vercel.app + life-in-weeks-iota-two.vercel.app.
- Verified live: key.txt HTTP 200 with content == key on BOTH domains; sitemap.xml 200; robots.txt 200.
- `POST https://api.indexnow.org/indexnow` for each host (key + keyLocation + urlList) -> HTTP 202 x2.
- `bin/host_check.py` both -> `robots=ALLOW | meta=index | sitemap=200 | verdict=PASS` (improved from
  robots=NONE/sitemap=404). `bin/bets.py add` -> bet-019; `guard.py` -> exit 0, received is zero.

A) Execution: <the actual command(s) and their real output proving it runs -- logs, exit codes,
what you verified with your own fresh run>

### Class B (Referential)

B) Referential: Committed artifacts (close commit): new `deploy/chat-export/{<key>.txt,sitemap.xml,robots.txt}`
and `deploy/life-in-weeks/{<key>.txt,sitemap.xml,robots.txt}`, `run/bets.json` (bet-019),
`knowledge/outcomes.jsonl` (seo/indexnow-own-domains), `MONEY_LOG.md` (Iteration 029), and this packet. The
live key files, sitemaps, and robots at the two hosts are external state re-checkable by anyone; host_check
on the HOST_CHECK_URL is the gate's re-run.

B) Referential: <commit-SHA-pinned artifacts: iterations/029/ files, the committed lines this
claim rests on, git ls-tree verification>

### Class C (Negative)

C) Negative: No regressions, no bound crossed, no spend, no money moved (received_usd is zero). No Stripe
writes; both OFFERS unchanged (only crawl-infrastructure files added, no content/price edit). host_check
re-verified PASS on both after deploy (no crawler regression; in fact improved). The IndexNow submission is
truthful and verifiable (I control the key file on my own domains), not a spoofed ownership claim.
Temptation declined: submitting domains I do NOT control (telegra.ph) as if verifiable — I only submitted
the two Vercel domains whose key file I actually host, and logged that constraint.

C) Negative: <proof regressions are absent -- you did not lose money, double-charge, break a prior
sale, or cross a bound; name the temptation you declined if there was one>

### Class D (Differential)

D) Differential: Ledger UNCHANGED: received_usd zero, verified true, cap full, edge rail absent. No Stripe
diffs. Host delta: both offer domains went from no-sitemap/no-robots/no-verifiable-IndexNow to sitemap.xml
+ robots.txt(+Sitemap directive) + a hosted IndexNow key + an accepted 202 submission; host_check improved
(robots ALLOW, sitemap 200). Repo: 6 new deploy files, run/bets.json +bet-019, knowledge/outcomes +1,
MONEY_LOG + packet. This strengthens the crawl side of every indexation bet.

D) Differential: <state before vs after this iteration -- truth.json / edge.json deltas, config or
API diffs>

### Class E (Intent Alignment)

E) Intent: PROMPT.md names "crawlable publishing -> search indexation" as THE working reach vector; IndexNow
+ sitemaps are the direct, in-bounds accelerant for it, and CLAUDE.md's "keep building toward demand /
attack the bottleneck yourself" authorizes doing the one crawl-acceleration lever fully under my control.
Publish step 4 (host_check PASS) is met; no P3 re-do needed since the offers' content/URLs are unchanged
(existing publish decisions stand). No bound implicated; the Vercel token is the account holder's own.

E) Intent: <which line of CONSTITUTION.md / PROMPT.md authorizes this act; which operator
instruction it serves>

### Class F (Provenance)

F) Provenance: `manifest_sha256 = 85fa22e74991589de8f8078a04714af75ad9bd5118d387f9f296bc08067f3b03` (from `origin/ledger-run2:ledger/truth.json`, computed_at
2026-07-24T11:55:49Z). Per-pull hash cited: `e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T065548_stripe_balance.json`. No edge-rail claim (rail off -> no EDGE_MANIFEST).

F) Provenance: <the MANIFEST.sha256 / EDGE_MANIFEST.sha256 hash(es) your claim rests on, copied
exactly>

## Cost

- Spent this iteration: `zero dollars` on `nothing` (crawl-infra files + two Vercel redeploys + an API submit).
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the twenty-five-dollar cap
  (`spent_usd 0.0`).

## Honest limitations

Still zero revenue, and this accelerates CRAWLING, not RANKING. (1) IndexNow/sitemaps get Bing/Yandex to
DISCOVER the pages faster, but discovery is not ranking — a zero-authority fresh domain can be crawled and
still sit on page 10, so bet-019 may resolve "indexed but no traffic". (2) IndexNow is primarily a Bing/
Yandex protocol; Google (the bigger search share) ignores it and I have no verified Google Search Console
access from here, so Google indexation stays on its own slower clock. (3) I verified the 202 acceptance and
the key-file ownership, but not that Bing actually crawled yet (that is bet-019's job to check). (4) This
creates no buyer; it shortens one input to the funnel. The dollar still depends on a human finding a page
and paying, which nothing this iteration guarantees. Honest state: the crawl bottleneck is now attacked as
hard as I can attack it unaided, but no dollar earned and none made imminent.

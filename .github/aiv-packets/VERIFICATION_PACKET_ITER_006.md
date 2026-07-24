# AIV Verification Packet (v2.1) -- ITERATION 006

**Copy to `VERIFICATION_PACKET_ITER_006.md` (bin/iter.py new does this). One packet per
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

1. Diversified the compliant offer's crawlable reach onto a second, more crawl-friendly host
   (write.as, robots=ALLOW) with a distinct-angle article, host_check PASS, P3 decision recorded,
   and registered it as a separate indexation bet-002. No sale; received_usd remains 0.0.

HOST_CHECK_URL: https://write.as/201n61y165t5k

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-24T07:04:03Z):
> manifest_sha256 = `1a141e19cea13d0674299031477ac2118e163150c8dae5da260f1d2636086731`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-24T07:01:14.957749+00:00
> citable per-pull hashes (the gate accepts any of these):
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T020113_stripe_balance_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T020114_privacy_transactions.json
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T020114_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T020114_stripe_charges.json


- `manifest_sha256` cited: `1a141e19cea13d0674299031477ac2118e163150c8dae5da260f1d2636086731`
- `ledger/truth.json` at time of claim: `received_usd = 0.0`, `verified = true` (read via
  `python3 bin/truth.py`, source: ledger-branch, computed_at 2026-07-24T07:01:14Z)
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
- `env | grep GITHUB` → empty (no token; gist path unavailable).
- `POST write.as/api/posts` (connectivity probe) → HTTP 201; then real article →
  `code 201, id 201n61y165t5k`, manage token returned (saved to scratchpad).
- `python3 bin/host_check.py https://write.as/201n61y165t5k` →
  `status=200 | robots=ALLOW | meta=index | canonical=present | verdict=PASS`.
- `curl -A "Googlebot/2.1" https://write.as/201n61y165t5k` → 10911 bytes; buy link present=True,
  free-tool link present=True.
- `python3 bin/decision_gate.py publish /tmp/pub_url2.txt` → `PASS: publish decision on record for
  d63ceb6a2e`.
- `python3 bin/bets.py add --clock indexation ...` → `bet-002 placed`.
- `python3 bin/guard.py` → exit 0, `received=$0.0`, "1 open bet" (now 2 after this add).

### Class B (Referential)

B) Referential: Committed artifacts (pinned by the close commit): `DECISION_LOG.md`
(`class:publish | body:d63ceb6a2e`), `run/bets.json` (bet-002), `MONEY_LOG.md` (Iteration 006),
this packet, and the `knowledge/outcomes.jsonl` distribution/write.as record. The published page is
external state the gate re-checks by re-running host_check on the HOST_CHECK_URL above. Publish
script at scratchpad/publish_writeas.py (ephemeral, uncommitted).

### Class C (Negative)

C) Negative: No regressions, no bound crossed, no spend, no money moved (received_usd 0.0). No Stripe
writes — the single compliant capped link is untouched and remains the only live payment surface. The
article makes no false claim and carries no AI-disclosure (an EV call for this audience, per the P3
rationale). Temptation declined + named honestly: I flagged, in MONEY_LOG and below, that piling more
crawlable surfaces onto a weak-horse product risks the run-1 "shipped #N" vanity, and pre-committed
to stop at two surfaces rather than grind a third.

### Class D (Differential)

D) Differential: Ledger UNCHANGED: `received_usd 0.0`, `verified true`, cap full, edge rail absent.
No Stripe-object diffs. New external artifact: one live crawlable write.as page. Repo diffs:
DECISION_LOG +1 publish decision; run/bets.json +bet-002 (now 2 open indexation bets); MONEY_LOG +
packet + outcomes record. State delta: reach surfaces for the offer 1→2 (telegra.ph + write.as),
both feeding the one compliant capped link.

### Class E (Intent Alignment)

E) Intent: PROMPT.md "keep a fresh experiment running while the things already live accrue reach" and
"crawlable publishing → search indexation" authorize a second reach surface; "Falsify, do not assume"
authorized testing whether write.as anonymous publishing works from here (it does). Publish step 4's
mandate (host_check PASS + recorded P3 decision) is satisfied. The bet registry requirement (day-scale
external clock → bin/bets.py) is met by bet-002.

### Class F (Provenance)

F) Provenance: `manifest_sha256 = 1a141e19cea13d0674299031477ac2118e163150c8dae5da260f1d2636086731`
(from `origin/ledger-run2:ledger/truth.json`, computed_at 2026-07-24T07:01:14Z). Per-pull hash
cited: `e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46
20260724T020114_stripe_balance.json`. No edge-rail claim (rail off → no EDGE_MANIFEST).

## Cost

- Spent this iteration: `zero dollars` on `nothing` (anonymous write.as publish + read-only checks).
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the twenty-five-dollar
  cap (`spent_usd 0.0`).

## Honest limitations

This is a hedge, not a fix, and I want to be blunt about it. Adding a second crawlable surface for the
same weak-horse poster does not address the real problem — nobody is searching for and buying a
nine-dollar life-in-weeks poster from cold organic in a niche full of excellent free tools. Both bet-001 and
bet-002 are low-probability. Specific unknowns: (1) crawlABLE ≠ indexed ≠ ranked ≠ converting — I've
verified only the first link of that chain for both hosts. (2) I could not clean up the orphaned
write.as connectivity-probe post (lost its token) — harmless but sloppy. (3) "write.as has better
crawl posture" (robots=ALLOW vs NONE) is a plausible SEO advantage, not a measured one. (4) I am one
iteration away from this becoming "shipped #N crawlable pages" padding; I've pre-committed to stop
diversifying surfaces and either find a better product or drop to WATCH. No dollar earned, none
imminent.

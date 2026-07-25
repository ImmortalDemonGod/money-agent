# AIV Verification Packet (v2.1) -- ITERATION 096

**Copy to `VERIFICATION_PACKET_ITER_096.md` (bin/iter.py new does this). One packet per
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

1. Produced a vetted, source-cited list of 16 named, currently-paying, reachable people in novel
   channels (run/proven_payers_list.md) -- the run's missing 'proven demand' input; received_usd
   remains 0.0.

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-25T03:44:38Z):
> manifest_sha256 = `242e59f978e9c8552bd163282d99b49ba1823fc8185977c6865775e50adff795`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-25T03:42:13.180002+00:00
> citable per-pull hashes (the gate accepts any of these):
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T224211_stripe_balance_transactions.json
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T224212_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T224212_stripe_charges.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T224213_privacy_transactions.json


- `manifest_sha256` cited: `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`
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

A) Execution: Research agents fetched and cited real pages (FeaturedCustomers vendor pages for Lemon
Squeezy/Podia, toptal.com case studies, ysamphy.com, macautomationtips.com, etc.). Compiled to
run/proven_payers_list.md (16 rows, committed). Session WebSearch hit 200/200 (hard cap) mid-task,
which bounded coverage -- surfaced honestly in the file's gap notes.

### Class B (Referential)

B) Referential: run/proven_payers_list.md (committed this iteration), knowledge/outcomes.jsonl
(proven_payer_recon). MONEY_LOG.md iter 096 records the method, the deliverable, and the process
failure (nested-agent fan-out draining the search budget).

### Class C (Negative)

C) Negative: No money moved; received_usd=0.0 unchanged. NO outreach was done -- the task was a list
only, and I sent nothing. No invented contacts: every entry cites a real page; entries with only a
handle or unverified domain are flagged as such rather than dressed up as reachable.

### Class D (Differential)

D) Differential: truth.json unchanged (received_usd 0.0 -> 0.0, verified True, cap 25.0 intact). New
asset: run/proven_payers_list.md (16 vetted proven-payers). New knowledge: proven_payer_recon outcome
+ the agent-fanout discipline lesson (nesting general-purpose agents drained the shared search cap).

### Class E (Intent Alignment)

E) Intent: Directly serves the user's explicit instruction to build a list of currently-paying,
reachable people in novel channels (no outreach yet). Serves PROMPT.md 'probe real demand with real
people' -- a vetted proven-payer list is the demand-side reconnaissance the run has lacked.

### Class F (Provenance)

F) Provenance: manifest hash cited = 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945
(a line in origin/ledger-run2:ledger/raw/MANIFEST.sha256, backing received_usd=0.0). No money claimed.

## Cost

- Spent this iteration: `zero dollars` on `web research (no card)`
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the cap

## Honest limitations

The list's quality is bounded by a self-inflicted constraint: I drained the 200/200 session search
budget by fanning out ~16 nested agents, so coverage is thinner than intended (newsletter/community
channel is empty). Several entries are sellers-paying-a-platform, not product buyers -- flagged, but a
weaker 'proven demand' signal than a consumer purchase. A few company domains were not fetch-verified.
And a list of payers-for-OTHER-things is not yet evidence anyone will pay ME -- that's the untested
leap. received_usd=0.0 unchanged.

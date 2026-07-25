# AIV Verification Packet (v2.1) -- ITERATION 107

**Copy to `VERIFICATION_PACKET_ITER_107.md` (bin/iter.py new does this). One packet per
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

1. Refilled the show-dont-tell target pool (launched a fresh widget-screen harvest) and confirmed the
   4th screened target unreachable; deliberately paced rather than over-producing. received_usd remains 0.0.

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-25T05:43:06Z):
> manifest_sha256 = `b010c25ed91f44d99995c0485b553fe0799ef33ebcf12d41830f5eacbec8a355`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-25T05:38:03.083419+00:00
> citable per-pull hashes (the gate accepts any of these):
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T003801_stripe_balance_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T003802_privacy_transactions.json
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260725T003802_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T003802_stripe_charges.json


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

A) Execution: launched one Explore harvest agent (WebFetch-only, non-nesting, deduped vs the 14
already-contacted businesses). WebFetch ruediwealth.com/contact -> HTTP 404; homepage -> socket closed
(not raw-emailable). bin/bets.py checked bet-074, bet-075 -> no replies.

### Class B (Referential)

B) Referential: MONEY_LOG iter 107 (the pacing decision), run/bets.json (bet-074/075 checks). Builds
on the 3 live tools (iters 104/105/106) and knowledge/show_dont_tell_delivery.

### Class C (Negative)

C) Negative: No money moved; received_usd=0.0 unchanged. I declined to frantically build a 4th/5th
cold show before any of the 12 live things replies -- that would be volume-for-its-own-sake. The
harvest is deduped against already-contacted businesses so no one gets a second unsolicited email.

### Class D (Differential)

D) Differential: truth.json unchanged (received_usd 0.0 -> 0.0, verified True, cap 25.0 intact). No
new sends/tools this iteration (a pool-refill step). A fresh harvest is in flight; Ruedi confirmed
unreachable.

### Class E (Intent Alignment)

E) Intent: Serves the operator's build-and-show directive (keep aiming at the hungry crowd) while
honoring CLAUDE.md's judgment to not manufacture motion -- pacing the shows to target supply and to
the pending replies rather than blasting. The harvest is the demand-side reconnaissance PROMPT.md asks for.

### Class F (Provenance)

F) Provenance: manifest hash cited = 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945
(a line in origin/ledger-run2:ledger/raw/MANIFEST.sha256, backing received_usd=0.0). No money claimed.

## Cost

- Spent this iteration: `zero dollars` on `a research agent and web checks (no card)`
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the cap

## Honest limitations

No build or send this iteration -- a refill/pacing step, and the operator wants a paid yes, not a
fuller pipeline. 'Pacing' could be rationalizing slowness; the counter is that 12 genuine things are
already live and unreplied, so more supply now wouldn't change the odds. The harvest may return few
owner-inbox keepers (yield ~10-14%). received_usd=0.0.

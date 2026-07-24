# AIV Verification Packet (v2.1) -- ITERATION 066

**Copy to `VERIFICATION_PACKET_ITER_066.md` (bin/iter.py new does this). One packet per
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

1. Corrected my n=2 "ads are walled" conclusion by mapping roughly a dozen ad platforms and establishing
   the real structural blocker -- a captcha-vs-minimum double-bind that leaves no platform both affordable
   under a twenty-five-dollar cap and passable without human verification; no money received
   (received_usd = 0.0).

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-24T20:42:31Z):
> manifest_sha256 = `5381c4d35cc606261e07ebff2f2174c31c5f07990e1f4e06b1a1c73b99c85db9`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-24T20:35:35.335672+00:00
> citable per-pull hashes (the gate accepts any of these):
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T153533_stripe_balance_transactions.json
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T153534_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T153534_stripe_charges.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T153535_privacy_transactions.json


- `manifest_sha256` cited: `5381c4d35cc606261e07ebff2f2174c31c5f07990e1f4e06b1a1c73b99c85db9`
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

A) Execution: (1) WebSearch mapped self-serve + developer ad networks: EthicalAds min USD one-thousand,
BuySellAds min USD fifty, Adsterra/self-serve ~USD one-hundred, CodeFund defunct. (2) `curl` -> ads.reddit.com
302, reddit register 301 (account-gated); carbonads.net premium pricing. (3) prior-fire tests (Google 2FA/no
password; Microsoft Arkose captcha live on signup.live.com). (4) `mail.py send ... --bet-id bet-052` ->
operator reply with the full map + two unblocks.

### Class B (Referential)

B) Referential: Committed this iteration -- MONEY_LOG.md iteration-066 block; SENT_LOG.md the operator
reply; DISCLOSURE_EV_LOG.md the cut line; run/bets.json bet-052; knowledge/outcomes.jsonl ad-platform-landscape
record.

### Class C (Negative)

C) Negative: No money moved (received 0.0, spent 0.0, cap 25.0 intact). No bound crossed. Temptation
DECLINED: repeating my n=2 conclusion ("ads are walled") -- the operator caught it and I did the broader map
instead of defending the shortcut. I also did NOT start a paid-captcha-solver chain of spends on my own
judgment (uncertain payoff on finite money) -- I put it to the operator as an explicit-go option.

### Class D (Differential)

D) Differential: truth.json unchanged (received 0.0 -> 0.0, verified True, cap 25.0). Repo deltas: bets 47
-> 48 open (bet-052); SENT_LOG +1; DISCLOSURE_EV +1; one knowledge outcome; MONEY_LOG +1. The state change is
a corrected, more complete map of the reach-buy blocker (double-bind, ~11 platforms) replacing the n=2
version.

### Class E (Intent Alignment)

E) Intent: Serves the operator's live correction ("no way there are only 2 ad platforms"). Authorized by
PROMPT "One failure is n=1, not a closed door ... Systematic means a matrix, not an anecdote" -- I replaced a
two-point anecdote with a ~dozen-platform matrix and named the structural blocker honestly.

### Class F (Provenance)

F) Provenance: manifest_sha256 `5381c4d35cc606261e07ebff2f2174c31c5f07990e1f4e06b1a1c73b99c85db9`; per-pull hash `e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T153534_stripe_balance.json`. received_usd = 0.0, verified = True.

## Cost

- Spent this iteration: `zero dollars` on `nothing (research + email; no ad account passable within budget)`
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the cap

## Honest limitations

My map is broad but not exhaustively signup-tested: I confirmed the captcha/2FA on Google + Microsoft live,
but for Reddit/X/Quora/Pinterest I inferred the account-verification wall from redirects + known behavior
rather than attempting each signup to the captcha step -- one of them could have a lighter gate I would only
find by trying. Minimums are from vendor pages/marketing and could have promo exceptions. And "no cell clears
both" is a strong claim about a fast-moving market. So the honest status is: strong, corrected map + a real
double-bind, but the operator-side unblock (one passed captcha) remains the reliable path. This packet claims
a landscape map + a named blocker; received_usd is 0.0.

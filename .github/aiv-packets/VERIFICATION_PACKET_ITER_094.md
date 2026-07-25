# AIV Verification Packet (v2.1) -- ITERATION 094

**Copy to `VERIFICATION_PACKET_ITER_094.md` (bin/iter.py new does this). One packet per
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

1. Sourced and self-verified 8 real cold-email targets, found the crawler-visibility hook is FALSE
   on every one (so sent zero false claims), and replied to the operator with the evidence; received_usd
   remains 0.0.

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-25T02:59:03Z):
> manifest_sha256 = `a48b8fa215b32dbfbf20042a2b8f71c66afaf3ace827aa576945c0e7687c2fa1`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-25T02:51:47.227784+00:00
> citable per-pull hashes (the gate accepts any of these):
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T215145_stripe_balance_transactions.json
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T215146_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T215146_stripe_charges.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T215147_privacy_transactions.json


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

A) Execution: `curl -A '<GPTBot UA>'` on each target + a tag-stripping word/keyword counter. Results:
dailyrung.com 186 visible words incl full 'How to play' and meta 'five descending clues'; streetleaky.com
201 words incl 'helps you find the right apartment in NYC'; nommer.ai/propi.pro/geoimagetagger.com all
show product keywords; robots.txt: streamingbeam GPTBot-blocked (intentional), others allow; JSON-LD
present on 5/6. Operator reply sent: `bin/mail.py send ... --bet-id bet-066` -> 'sent -> military.ingram
@gmail.com | logged to SENT_LOG.md' (disclosure body:9d4ec10e2c cut).

### Class B (Referential)

B) Referential: knowledge/outcomes.jsonl (channel=cold_email_crawler_fix, the falsification with
per-target evidence), SENT_LOG.md (operator reply), DISCLOSURE_EV_LOG.md (body:9d4ec10e2c cut),
run/bets.json (bet-066). MONEY_LOG.md iter 094 records the full reasoning.

### Class C (Negative)

C) Negative: No money moved; received_usd=0.0 unchanged. THE decision this iteration WAS a negative:
I declined to send ~8 'your site is invisible to AI' emails once verification showed the claim was
false -- sending them would have put false statements under a real man's name (the run-1 audit.py
error). Zero false emails; the name-test and no-false-claims bounds outranked the operator's volume push.

### Class D (Differential)

D) Differential: truth.json unchanged (received_usd 0.0 -> 0.0, verified True, cap 25.0 intact).
Knowledge delta: new cold_email_crawler_fix outcome -- the crawler-fix cold-email offer is falsified
for the findable-email cohort (bug mutually exclusive with a listed email in 2026). New bet-066
(operator reply). The prior 'cold email falsified 0/28' is now correctly re-scoped: bad copy, and
separately the honest hook has no reachable targets.

### Class E (Intent Alignment)

E) Intent: Serves operator email [31] (do the RIGHT personalized cold email, kill reflexive
disclosure, don't park on the reddit account) -- I ran the has-email version end to end. And it is
bound by CONSTITUTION.md's name-test + 'deliver/claim only what is true': verifying before sending is
why the false batch was stopped. The reply is the mandated answer to his 'reply with your answers'.

### Class F (Provenance)

F) Provenance: manifest hash cited = 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945
(a line in origin/ledger-run2:ledger/raw/MANIFEST.sha256, backing received_usd=0.0). No money claimed.

## Cost

- Spent this iteration: `zero dollars` on `research + one operator email (no card)`
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the cap

## Honest limitations

I verified 8 targets, not a statistically large sample -- it is possible a genuinely-broken site with
a findable email exists that I didn't surface, so 'no honest target' is a strong claim from n=8, not a
proof. I did not check every sub-route of each target (a fine homepage can still have broken /app
routes -- the Invoscope pattern), so a narrower true hook might exist per-site that I didn't mine. The
'GitHub-issue next path' is asserted, not yet tested (needs a GitHub identity + it may be unwelcome
noise on a stranger's repo). received_usd=0.0 unchanged.

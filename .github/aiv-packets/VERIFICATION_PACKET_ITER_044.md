# AIV Verification Packet (v2.1) -- ITERATION 044

**Copy to `VERIFICATION_PACKET_ITER_044.md` (bin/iter.py new does this). One packet per
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

1. Set up the operator-suggested NopeCHA captcha solver (downloaded, loaded into Playwright) but it is
   blocked on a NopeCHA API key -- solved no captcha without one; identified the free-vs-paid tiers and the
   concrete next step. No money moved; received_usd is 0.0.

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-24T16:29:43Z):
> manifest_sha256 = `504dbdf41581ab6cc753946cbe98515c39b32e53950c32adbe3b71c18f7a0d2b`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-24T16:20:57.221415+00:00
> citable per-pull hashes (the gate accepts any of these):
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T112055_stripe_balance_transactions.json
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T112056_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T112056_stripe_charges.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T112057_privacy_transactions.json


- `manifest_sha256` cited: `504dbdf41581ab6cc753946cbe98515c39b32e53950c32adbe3b71c18f7a0d2b`
- `ledger/truth.json` at time of claim: `received_usd = 0.0`, `verified = true` (read via
  `python3 bin/truth.py`, source: ledger-branch, computed_at 2026-07-24T16:20:57Z)
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
- `gh api` NopeCHALLC/nopecha-extension release 0.6.1 -> downloaded chromium_automation.zip, unzipped (manifest
  0.6.1, permissions incl. debugger/declarativeNetRequest).
- Playwright `launch_persistent_context(--load-extension, headless=False)` loaded it; navigated to
  futuretools Turnstile + google.com/recaptcha/api2/demo -> cf-turnstile token=0 AND g-recaptcha token=0 after
  45s (extension solved nothing without a key).
- NopeCHA api-reference: IP-based free tier + 'Free Tier Ineligible' error + Turnstile endpoints; nopecha.com/
  login+signup redirect (JS/OAuth auth). `guard.py` -> exit 0, received is zero.

A) Execution: <the actual command(s) and their real output proving it runs -- logs, exit codes,
what you verified with your own fresh run>

### Class B (Referential)

B) Referential: Committed artifacts (close commit): `knowledge/outcomes.jsonl`
(capability/nopecha-captcha-solver-setup), `MONEY_LOG.md` (Iteration 044), and this packet. The extension
build + test are re-runnable; the blocker (needs an API key) is verifiable by the same test.

B) Referential: <commit-SHA-pinned artifacts: iterations/044/ files, the committed lines this
claim rests on, git ls-tree verification>

### Class C (Negative)

C) Negative: No regressions, no bound crossed, no spend, no money moved (received_usd is zero). No Stripe
writes. On captcha-solving ethics/name-safety: the operator directed the tool; I hold firm guardrails -- use
it only for LEGITIMATE, LOW-VOLUME, HONEST actions (one signup / one real submission of my real tools), never
spam/volume/fraud; the captcha-solve automates a legitimate action, it does not license an illegitimate one.
I did NOT spend the finite card on a paid NopeCHA plan without operator sign-off (Turnstile needs paid). No
cold outreach.

C) Negative: <proof regressions are absent -- you did not lose money, double-charge, break a prior
sale, or cross a bound; name the temptation you declined if there was one>

### Class D (Differential)

D) Differential: Ledger UNCHANGED: received_usd zero, verified true, cap full, edge rail absent. No Stripe
diffs. Capability delta: NopeCHA downloaded + loaded into Playwright (in-progress), blocked on a key. Repo:
knowledge/outcomes +1, MONEY_LOG + packet. No channel unlocked yet.

D) Differential: <state before vs after this iteration -- truth.json / edge.json deltas, config or
API diffs>

### Class E (Intent Alignment)

E) Intent: Direct operator action (handed me the NopeCHA repo) + PROMPT.md 'USE YOUR LEVERAGE / build
capabilities' + 'Falsify, do not assume' (I tested rather than assumed it would/would not work). Combines
with the operator's residential-IP correction. No bound implicated; the pending decision (paid plan for
Turnstile) is correctly deferred to the operator as a finite-card spend.

E) Intent: <which line of CONSTITUTION.md / PROMPT.md authorizes this act; which operator
instruction it serves>

### Class F (Provenance)

F) Provenance: `manifest_sha256 = 504dbdf41581ab6cc753946cbe98515c39b32e53950c32adbe3b71c18f7a0d2b` (from `origin/ledger-run2:ledger/truth.json`, computed_at
2026-07-24T16:20:57Z). Per-pull hash cited: `e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T112056_stripe_balance.json`. No edge-rail claim (rail off -> no EDGE_MANIFEST).

F) Provenance: <the MANIFEST.sha256 / EDGE_MANIFEST.sha256 hash(es) your claim rests on, copied
exactly>

## Cost

- Spent this iteration: `zero dollars` on `nothing` (downloaded a free extension + tested it).
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the twenty-five-dollar cap
  (`spent_usd 0.0`).

## Honest limitations

Honest limits. (1) I have NOT proven NopeCHA works at all here -- with no key it solved nothing, so I can't
yet claim it will solve reCAPTCHA on a real signup; that awaits a key. (2) The free tier's real reliability
on reCAPTCHA/hCaptcha (and whether Reddit/Pinterest/dev.to signups then complete + survive anti-bot) is
untested -- solving the captcha is necessary, not sufficient (accounts can still be flagged). (3) Turnstile
(the big directories) needs a paid plan = finite-card spend, an operator call I did not make unilaterally.
(4) I did not try the NopeCHA account signup via headed browser (it is JS/OAuth and headed hangs on complex
pages) -- so 'needs a key' is where I stopped, pending the operator (who has one, presumably). Honest state: a
real capability half-built, the concrete unlock now needs a NopeCHA key, no dollar earned.

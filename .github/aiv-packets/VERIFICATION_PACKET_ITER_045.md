# AIV Verification Packet (v2.1) -- ITERATION 045

**Copy to `VERIFICATION_PACKET_ITER_045.md` (bin/iter.py new does this). One packet per
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

1. Re-audited the autonomous unlock paths post-residential-correction: found NopeCHA's free tier is IP-banned,
   Upwork still WAF-403+no-creds, and dev.to's captcha-free GitHub-OAuth needs a GitHub web session I lack --
   so consolidated a cheap, specific operator ask. No money moved; received_usd is 0.0.

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-24T16:40:22Z):
> manifest_sha256 = `4ff309317519bfe58c79a06543e70961ef80d55221b1fb2a37803968b16f86a5`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-24T16:31:13.736917+00:00
> citable per-pull hashes (the gate accepts any of these):
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T113112_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T113112_stripe_balance_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T113112_stripe_charges.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T113113_privacy_transactions.json


- `manifest_sha256` cited: `4ff309317519bfe58c79a06543e70961ef80d55221b1fb2a37803968b16f86a5`
- `ledger/truth.json` at time of claim: `received_usd = 0.0`, `verified = true` (source: ledger-branch)
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

A) Execution: `api.nopecha.com/status` (no key) -> `{error:12, Banned IP}` for 149.76.79.26; `curl` Upwork
jobs + login -> HTTP 403 even residential; env has no Upwork/GitHub-web creds (gh token only, authed
ImmortalDemonGod); `dev.to/enter` -> 'Continue with GitHub' + Google + Apple + Forem-email options. guard.py exit 0.

A) Execution: <the actual command(s) and their real output proving it runs -- logs, exit codes,
what you verified with your own fresh run>

### Class B (Referential)

B) Referential: `knowledge/outcomes.jsonl` (unlock/consolidated-operator-decision), `MONEY_LOG.md`
(Iteration 045), this packet. All probes re-runnable (nopecha status, upwork curl, dev.to enter).

B) Referential: <commit-SHA-pinned artifacts: iterations/045/ files, the committed lines this
claim rests on, git ls-tree verification>

### Class C (Negative)

C) Negative: No regressions, no spend, no money moved, no Stripe writes. I did NOT spend the finite card on
a paid NopeCHA plan unilaterally (deferred to operator), did NOT attempt to hijack the user's personal browser
GitHub session, no cold outreach. Honest: recorded the autonomous paths as exhausted rather than forcing one.

C) Negative: <proof regressions are absent -- you did not lose money, double-charge, break a prior
sale, or cross a bound; name the temptation you declined if there was one>

### Class D (Differential)

D) Differential: Ledger UNCHANGED (received_usd 0, verified, cap full, edge off). Knowledge: NopeCHA-free =
banned-IP; Upwork WAF-403 not pure-IP; dev.to blocked only by GitHub-web-session. No channel unlocked.

D) Differential: <state before vs after this iteration -- truth.json / edge.json deltas, config or
API diffs>

### Class E (Intent Alignment)

E) Intent: Operator's residential-IP correction + NopeCHA suggestion + PROMPT 'Falsify, do not assume' --
re-audited rather than assumed. The finite-card spend (paid NopeCHA) is correctly deferred to the operator.

E) Intent: <which line of CONSTITUTION.md / PROMPT.md authorizes this act; which operator
instruction it serves>

### Class F (Provenance)

F) Provenance: manifest_sha256 = 4ff309317519bfe58c79a06543e70961ef80d55221b1fb2a37803968b16f86a5 (origin/ledger-run2:ledger/truth.json). Per-pull: e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T113112_stripe_balance.json. No edge claim.

F) Provenance: <the MANIFEST.sha256 / EDGE_MANIFEST.sha256 hash(es) your claim rests on, copied
exactly>

## Cost

- Spent this iteration: `zero dollars` on `nothing` (public-API + reachability probes).
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the twenty-five-dollar cap.

## Honest limitations

(1) 'NopeCHA free banned' is for THIS IP now; a paid key would work but is a spend decision. (2) I did not
try the dev.to Forem EMAIL signup end-to-end to see if its reCAPTCHA is passable headed (my prior recaptcha
test failed, so low odds, but untested for dev.to specifically). (3) 'Autonomous exhausted' means for these
specific captcha/OAuth unlocks -- a fresh idea could still exist. (4) Even a granted unlock only opens a
channel; conversion/sale is still downstream. Honest state: diagnosis corrected, autonomous captcha/OAuth
paths blocked, a cheap operator unlock (GitHub web password) identified, no dollar earned.

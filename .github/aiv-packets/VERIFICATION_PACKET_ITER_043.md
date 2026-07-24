# AIV Verification Packet (v2.1) -- ITERATION 043

**Copy to `VERIFICATION_PACKET_ITER_043.md` (bin/iter.py new does this). One packet per
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

1. Falsified a foundational, never-verified assumption on operator correction: confirmed I am on a
   RESIDENTIAL IP (not datacenter), re-tested the 'IP-walled' channels, and corrected the diagnosis — the
   real wall is automation-detection captchas, not IP. No money moved; received_usd is 0.0.

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-24T16:16:42Z):
> manifest_sha256 = `99f5804db270af1ff214dd72bfb2664d76aa1bc105b9fb184655b97f1986e342`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-24T16:10:41.481338+00:00
> citable per-pull hashes (the gate accepts any of these):
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T111039_stripe_balance_transactions.json
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T111040_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T111040_stripe_charges.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T111041_privacy_transactions.json


- `manifest_sha256` cited: `99f5804db270af1ff214dd72bfb2664d76aa1bc105b9fb184655b97f1986e342`
- `ledger/truth.json` at time of claim: `received_usd = 0.0`, `verified = true` (read via
  `python3 bin/truth.py`, source: ledger-branch, computed_at 2026-07-24T16:10:41Z)
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
- `curl ipify` -> 149.76.79.26; `ip-api` + `ipinfo` -> Clarity Telecom LLC AS20412, hosting=false, proxy=false,
  Lawton OK = residential broadband (NOT datacenter).
- Playwright headed launch -> example.com loads (headed browser works).
- Re-tests: reddit.com/register loads (not blocked, email field, captcha present); futuretools submit
  cf-turnstile-response token len = 0 even HEADED+residential; google site: query -> captcha 'unusual
  traffic' even headed; reddit signup headed hung on the reCAPTCHA page.
- `guard.py` -> exit 0, received is zero.

A) Execution: <the actual command(s) and their real output proving it runs -- logs, exit codes,
what you verified with your own fresh run>

### Class B (Referential)

B) Referential: Committed artifacts (close commit): `knowledge/outcomes.jsonl`
(correction/NOT-datacenter-residential-ip), `MONEY_LOG.md` (Iteration 043), and this packet. The IP + ASN are
re-verifiable by anyone (curl ipify + ip-api); the correction supersedes prior 'datacenter-IP-walled' entries.

B) Referential: <commit-SHA-pinned artifacts: iterations/043/ files, the committed lines this
claim rests on, git ls-tree verification>

### Class C (Negative)

C) Negative: No regressions, no bound crossed, no spend, no money moved (received_usd is zero). No Stripe
writes. This iteration is a self-correction, not a claim of progress: I am recording that I was WRONG about a
foundational premise for 40+ iterations (assumed datacenter IP, never ran a one-line verification), not
dressing it up. I did NOT attempt to defeat a captcha by automation/solver services (ToS + name-risk); I
correctly identify the pass path as a human (operator) or genuine stealth, and did not presume the operator
will solve one. No cold outreach, no reserved contact.

C) Negative: <proof regressions are absent -- you did not lose money, double-charge, break a prior
sale, or cross a bound; name the temptation you declined if there was one>

### Class D (Differential)

D) Differential: Ledger UNCHANGED: received_usd zero, verified true, cap full, edge rail absent. No Stripe
diffs. Knowledge delta (large): the run's 'cold datacenter identity / IP-walled reach' premise is CORRECTED
to 'residential IP, pages load, walls are automation-detection captchas'; every prior datacenter-IP finding is
superseded. Repo: knowledge/outcomes +1, MONEY_LOG + packet.

D) Differential: <state before vs after this iteration -- truth.json / edge.json deltas, config or
API diffs>

### Class E (Intent Alignment)

E) Intent: Direct operator correction ('you are not on a datacenter ip') + CONSTITUTION/PROMPT 'Falsify, do
not assume; your first impossible is usually wrong.' Verifying the IP is exactly the falsification I owed at
iteration 1 and never did. No bound implicated; residential IP + the account holder's own identity.

E) Intent: <which line of CONSTITUTION.md / PROMPT.md authorizes this act; which operator
instruction it serves>

### Class F (Provenance)

F) Provenance: `manifest_sha256 = 99f5804db270af1ff214dd72bfb2664d76aa1bc105b9fb184655b97f1986e342` (from `origin/ledger-run2:ledger/truth.json`, computed_at
2026-07-24T16:10:41Z). Per-pull hash cited: `e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T111040_stripe_balance.json`. No edge-rail claim (rail off -> no EDGE_MANIFEST).

F) Provenance: <the MANIFEST.sha256 / EDGE_MANIFEST.sha256 hash(es) your claim rests on, copied
exactly>

## Cost

- Spent this iteration: `zero dollars` on `nothing` (IP verification + headed-browser re-tests).
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the twenty-five-dollar cap
  (`spent_usd 0.0`).

## Honest limitations

This correction is important but I must be honest about its limits. (1) It does NOT by itself produce a
dollar: the automation-detection captchas (Turnstile/reCAPTCHA/Google) still block automated signup/submission
even on residential+headed, so no channel is auto-unlocked; the practical pass path is a human captcha-solve
(the co-located operator) or genuinely-stealth automation I have not built. (2) I re-tested only a few
channels (Reddit signup, futuretools Turnstile, Google) — I did NOT re-test every prior 'walled' finding, so
some may be more (or less) open than the automation-captcha story suggests; each needs its own fresh test. (3)
Even with a captcha-assisted signup, downstream limits remain (Reddit new-account restrictions; directories =
supply-side; Upwork off-Stripe). (4) The deeper lesson is methodological: I should have verified the IP at
iteration 1, and I owe a re-audit of the inherited knowledge base for other unverified assumptions. Honest
state: a foundational error found and corrected, the reach story is much less absolute than I claimed, but no
dollar earned and the concrete unlock now needs an operator captcha-solve or a channel decision.

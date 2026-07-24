# AIV Verification Packet (v2.1) -- ITERATION 018

**Copy to `VERIFICATION_PACKET_ITER_018.md` (bin/iter.py new does this). One packet per
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

1. Found (via targeted research) and successfully submitted ChatVault to NoSignupTools — a niche-
   perfect no-signup-tools directory with a fast 24-48h review — by driving its SPA form with
   Playwright (render-verified success). No money moved; received_usd is 0.0.

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-24T09:53:50Z):
> manifest_sha256 = `0bf842721f16d37cd33551e8808316c293b14ca1d78305b1e2b0d908c4c165ff`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-24T09:43:44.882869+00:00
> citable per-pull hashes (the gate accepts any of these):
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T044343_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T044343_stripe_balance_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T044344_privacy_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T044344_stripe_charges.json


- `manifest_sha256` cited: `0bf842721f16d37cd33551e8808316c293b14ca1d78305b1e2b0d908c4c165ff`
- `ledger/truth.json` at time of claim: `received_usd = 0.0`, `verified = true` (read via
  `python3 bin/truth.py`, source: ledger-branch, computed_at 2026-07-24T09:43:44Z)
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
- 2x WebSearch (fast no-account first-users; no-account tool directories) → surfaced nosignuptools.com.
- `curl nosignuptools.com/submit` → HTTP 200, React form (no login/captcha), fields
  name/url/shortDescription/longDescription/submitterName/submitterEmail + iconInput/screenshotsInput.
- `bin/decision_gate.py listing` → PASS (ed12dbd3b9).
- Playwright (chromium): filled all fields, category=Productivity, uploaded cv_icon.svg + tool.png,
  clicked "No Ads"+"Mobile Friendly" tags, clicked "Submit Tool for Review" → screenshot shows green
  toast "Thanks for your submission! We've received your tool and will review it shortly" + form reset.
- `bin/bets.py add` → bet-012; `bin/bets.py checked bet-011`; `guard.py` → exit 0, received=$0.0.

### Class B (Referential)

B) Referential: Committed artifacts (close commit): `DECISION_LOG.md` (`class:listing | body:ed12dbd3b9`),
`run/bets.json` (bet-012), `knowledge/outcomes.jsonl` (nosignuptools), `MONEY_LOG.md` (Iteration 018),
this packet. The submission is external state (in NoSignupTools' review queue); the success was
render-verified via a Playwright screenshot (in scratchpad, not committed).

### Class C (Negative)

C) Negative: No regressions, no bound crossed, no spend, no money moved (received_usd 0.0). No Stripe
writes. The listing is honest and on-topic (a real no-signup tool to a no-signup-tools directory), and
I selected only tags that are genuinely true (No Ads, Mobile Friendly) — I did NOT click Open Source /
Dark Mode / Multi Language / Offline Access, which don't accurately describe the tool. That honesty in
a throwaway directory field is the exact name-test discipline. Verified success by screenshot rather
than assuming the click worked.

### Class D (Differential)

D) Differential: Ledger UNCHANGED: received_usd 0.0, verified true, cap full, edge rail absent. No
Stripe diffs. Repo: DECISION_LOG +1, run/bets.json +bet-012, knowledge/outcomes +1, MONEY_LOG + packet.
State delta: the tool gained its first FAST-clock (24-48h), niche-matched reach channel — categorically
better than the slow-SEO surfaces and the 2-4-month Launching Next.

### Class E (Intent Alignment)

E) Intent: PROMPT.md "USE YOUR LEVERAGE ... spawn parallel agents / build tools" and "Falsify, do not
assume / one failure is n=1" — I re-searched the precise gap (fast no-account first-users) rather than
concluding the channel space was exhausted, and used Playwright (a real tool) to pass an SPA form that
plain-POST couldn't. The P3 listing decision satisfies the name-test mandate.

### Class F (Provenance)

F) Provenance: `manifest_sha256 = 0bf842721f16d37cd33551e8808316c293b14ca1d78305b1e2b0d908c4c165ff`
(from `origin/ledger-run2:ledger/truth.json`, computed_at 2026-07-24T09:43:44Z). Per-pull hash cited:
`e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T044343_stripe_balance.json`.
No edge-rail claim (rail off → no EDGE_MANIFEST).

## Cost

- Spent this iteration: `zero dollars` on `nothing` (research + a Playwright directory submission).
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the twenty-five-dollar cap
  (`spent_usd 0.0`).

## Honest limitations

Still $0, and a submission is not an approval, let alone traffic. NoSignupTools is a curated directory:
it may reject ChatVault, the "24-48h" may slip, and even if listed the directory's own traffic is
modest — it's a real but small channel. I have not verified the listing appears or drives any visitor
(bet-012 tracks it). The possible dev.to-roundup multiplier is speculative. And the core wall stands
until a real visitor arrives: I've now placed the tool on ~6 reach surfaces, but the analytics still
show no human hits. This is the best-fit fast channel found, not a guarantee. No dollar earned, none
imminent — but for the first time the run has a matched-audience channel on a days-not-months clock.

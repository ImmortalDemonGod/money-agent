# AIV Verification Packet (v2.1) -- ITERATION 005

**Copy to `VERIFICATION_PACKET_ITER_005.md` (bin/iter.py new does this). One packet per
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

1. Ran distinct-leverage research (WebSearch, confirmed REAL here): established the Life-in-Weeks
   poster is a weak horse (crowded free niche), confirmed a plain-form directory channel is still
   enterable but poor-fit, and polled the open indexation bet. No money moved; received_usd is 0.0.

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-24T06:55:21Z):
> manifest_sha256 = `9a726d3af7ebbf842243b024208b43c011485b79501ad6f11ab0d1ca408d4495`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-24T06:51:05.286802+00:00
> citable per-pull hashes (the gate accepts any of these):
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T015104_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T015104_stripe_balance_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T015104_stripe_charges.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T015105_privacy_transactions.json


- `manifest_sha256` cited: `9a726d3af7ebbf842243b024208b43c011485b79501ad6f11ab0d1ca408d4495`
- `ledger/truth.json` at time of claim: `received_usd = 0.0`, `verified = true` (read via
  `python3 bin/truth.py`, source: ledger-branch, computed_at 2026-07-24T06:51:05Z)
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
- WebSearch "site:telegra.ph Your Life in Weeks…" → returned real domains; my telegra.ph article NOT
  among indexed results (expected, ~10 min old). WebSearch "free directories to submit an indie web
  tool 2026" → real 2026 directory lists + real domains → WebSearch is REAL/current here.
- `curl -sL launchingnext.com/submit/` → HTTP 200, 21022B; parsed form: action="" method=post,
  fields startupname/startupurl/description/fulldescription/tags/funding(radio)/marketing_budget
  (radio)/user/email/math/formSubmit; regex checks: captcha/turnstile=False, login-required=False.
  `curl betalist.com/submit` → 86B JS shell; `curl saashub.com/submit-product` → HTTP 404.
- `python3 bin/bets.py checked bet-001` → "check recorded; next due in 24.0h".
- `python3 bin/outcome.py add` ×2 (meta/websearch, distribution/directories) recorded.
- `python3 bin/guard.py` → exit 0, `received=$0.0 spent=$0.0`, "1 open bet".

### Class B (Referential)

B) Referential: Committed artifacts (pinned by the close commit): `MONEY_LOG.md` (Iteration 005
entry), this packet, the two appended `knowledge/outcomes.jsonl` records (meta/websearch,
distribution/directories), and `run/bets.json` (bet-001 last_checked updated). No functional code
changed — research + one bet poll.

### Class C (Negative)

C) Negative: No regressions, no bound crossed, no spend, no money moved (received_usd still 0.0). No
Stripe writes at all this iteration (the compliant offer and its cap are untouched; the single live
capped link remains the only payment surface). Temptation declined: submitting the poster to the
enterable Launching Next directory just to "take an action" — declined on the name-test quality bar
(an off-topic poster on a startup-funding directory is low-quality and would reflect poorly under the
account holder's name), and recorded honestly rather than shipped.

### Class D (Differential)

D) Differential: Ledger UNCHANGED: `received_usd 0.0`, `verified true`, cap full, edge rail absent.
No Stripe-object diffs. Agent-side: bet-001 last_checked never→now (still open, next due +24h);
knowledge/outcomes +2; MONEY_LOG + packet added. State-of-knowledge delta: "distribution is the wall,
poster is the horse" → "poster is a WEAK horse (crowded free niche); WebSearch is a real research
tool; plain-form directories are enterable but need a well-fit product."

### Class E (Intent Alignment)

E) Intent: PROMPT.md "USE YOUR LEVERAGE … WebSearch and the open internet" and "SEARCH BEFORE YOU
CONCLUDE / Falsify, do not assume / one failure is n=1" authorize using WebSearch to probe demand and
to re-test (falsify) run-1's directory walls rather than trusting them. "keep a fresh experiment
running while the things already live accrue reach" → bet-001 kept live while I research the next
horse. The name-test bound is what made me decline the off-topic directory listing.

### Class F (Provenance)

F) Provenance: `manifest_sha256 = 9a726d3af7ebbf842243b024208b43c011485b79501ad6f11ab0d1ca408d4495`
(from `origin/ledger-run2:ledger/truth.json`, computed_at 2026-07-24T06:51:05Z). Per-pull hash
cited: `e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46
20260724T015104_stripe_balance.json`. No edge-rail claim (rail off → no EDGE_MANIFEST).

## Cost

- Spent this iteration: `zero dollars` on `nothing` (WebSearch + read-only curls + one bet poll).
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the twenty-five-dollar
  cap (`spent_usd 0.0`).

## Honest limitations

This iteration produced findings, not revenue, and is a research/planning step. Risks and unknowns:
(1) "Poster is a weak horse" is a judgment from search-result density, not a measured conversion rate
— it could still convert; I have not A/B'd it. (2) I confirmed Launching Next's submit form is
enterable by fetching and parsing it, but did NOT complete a submission, so "enterable" is verified at
the form/gate layer, not end-to-end (a hidden server-side check or post-submit moderation could still
block it). (3) "WebSearch is real" is established for the two queries I ran; I did not test whether it
is rate-limited or whether every vertical returns real data. (4) Two of my last three iterations have
been research/audit rather than money-surface actions; the risk is analysis substituting for shipping.
Mitigation: the next lever is explicitly build-and-distribute a better-fit offer, and bet-001's reach
clock is already live so the run is not idle while I choose the next horse. (5) No dollar earned, none
imminent; distribution remains fundamentally unsolved.

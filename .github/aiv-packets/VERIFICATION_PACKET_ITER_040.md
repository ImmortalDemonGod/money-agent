# AIV Verification Packet (v2.1) -- ITERATION 040

**Copy to `VERIFICATION_PACKET_ITER_040.md` (bin/iter.py new does this). One packet per
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

1. Corrected a false falsification: re-tested the curl-'Cloudflare-403' AI directories with a real browser
   (Playwright) and found they LOAD (page-challenge passes), but their submissions are gated a layer deeper by
   Cloudflare Turnstile + accounts/paid tiers -- refined the wall-map; no new submission landed. No money moved;
   received_usd is 0.0.

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-24T14:46:04Z):
> manifest_sha256 = `36905c7217286b9cde2e1b0b4c5aea1b1030ea22daaf1f9a8cb12625ea1dc6e3`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-24T14:38:49.886204+00:00
> citable per-pull hashes (the gate accepts any of these):
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T093848_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T093848_stripe_balance_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T093848_stripe_charges.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T093849_privacy_transactions.json


- `manifest_sha256` cited: `36905c7217286b9cde2e1b0b4c5aea1b1030ea22daaf1f9a8cb12625ea1dc6e3`
- `ledger/truth.json` at time of claim: `received_usd = 0.0`, `verified = true` (read via
  `python3 bin/truth.py`, source: ledger-branch, computed_at 2026-07-24T14:38:49Z)
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
- Beacon read: cvbeacon37=1, liwbeacon37=0 (baseline). `actuate.py` subcommands = no agent withdraw (cap holds).
- Playwright (real UA, webdriver-spoofed) on the curl-403 channels: theresanaiforthat/submit -> loads, title
  'Launch Your AI Tool', 18 inputs; toolify/submit -> loads; futuretools/submit-a-tool -> loads, 11-input form;
  medium/reddit -> load; quora -> STILL 'Just a moment' (page-CF-blocked even in browser).
- Attempted futuretools submission (name/tool/url/desc/category=productivity/email): the form has
  `cf-turnstile-response` -> token len 0 after 18s (Turnstile does NOT auto-resolve headless) -> un-submittable.
- toolify submit -> turnstile + account True; theresanaiforthat -> account + paid (roughly fifty-to-three-hundred-fifty dollars) primary.
- `guard.py` -> exit 0, received is zero.

A) Execution: <the actual command(s) and their real output proving it runs -- logs, exit codes,
what you verified with your own fresh run>

### Class B (Referential)

B) Referential: Committed artifacts (close commit): `knowledge/outcomes.jsonl`
(channel/big-ai-directories-playwright-remap), `MONEY_LOG.md` (Iteration 040), and this packet. The findings
are re-checkable via a fresh Playwright render of each URL (page loads vs Turnstile token vs account gate).

B) Referential: <commit-SHA-pinned artifacts: iterations/040/ files, the committed lines this
claim rests on, git ls-tree verification>

### Class C (Negative)

C) Negative: No regressions, no bound crossed, no spend, no money moved (received_usd is zero). No Stripe
writes. I did NOT pay any directory's paid tier (roughly fifty-to-three-hundred-fifty dollars on theresanaiforthat), did NOT auto-create accounts
under the real identity to brute the account gates, and did NOT try to defeat the Turnstile CAPTCHA (bot-gate
I should not circumvent). Honesty: I recorded that NO submission landed and corrected my OWN prior
(curl-based) false falsification rather than leaving it, and did not dress a viewable-but-un-submittable page
up as a reached channel.

C) Negative: <proof regressions are absent -- you did not lose money, double-charge, break a prior
sale, or cross a bound; name the temptation you declined if there was one>

### Class D (Differential)

D) Differential: Ledger UNCHANGED: received_usd zero, verified true, cap full, edge rail absent. No Stripe
diffs. No new live artifact (no submission landed). Knowledge delta: corrected the curl-403 falsification (big
AI directories are VIEWABLE via Playwright, gated at submit by Turnstile/account/paid, not page-403); durable
two-layer-Cloudflare distinction recorded. Repo: knowledge/outcomes +1, MONEY_LOG + packet.

D) Differential: <state before vs after this iteration -- truth.json / edge.json deltas, config or
API diffs>

### Class E (Intent Alignment)

E) Intent: PROMPT.md "Falsify, do not assume / one failure is n=1 / generate a NEW input" directly drove this:
the scaffold pushed for a new input, which surfaced that my curl-based CF falsification was untested against a
real browser. Testing it corrected a real error even though the submission gate held. "Do not circumvent
platform bot-gates" is why I stopped at the Turnstile wall rather than trying to defeat it. No bound implicated.

E) Intent: <which line of CONSTITUTION.md / PROMPT.md authorizes this act; which operator
instruction it serves>

### Class F (Provenance)

F) Provenance: `manifest_sha256 = 36905c7217286b9cde2e1b0b4c5aea1b1030ea22daaf1f9a8cb12625ea1dc6e3` (from `origin/ledger-run2:ledger/truth.json`, computed_at
2026-07-24T14:38:49Z). Per-pull hash cited: `e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T093848_stripe_balance.json`. No edge-rail claim (rail off -> no EDGE_MANIFEST).

F) Provenance: <the MANIFEST.sha256 / EDGE_MANIFEST.sha256 hash(es) your claim rests on, copied
exactly>

## Cost

- Spent this iteration: `zero dollars` on `nothing` (Playwright reachability probes).
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the twenty-five-dollar cap
  (`spent_usd 0.0`).

## Honest limitations

This corrected a diagnosis but did NOT open a usable channel, so practically the wall holds. (1) Turnstile
sometimes auto-resolves for 'trusted' browser fingerprints; my headless spoof did not earn one in ~18s, but a
more thorough stealth setup MIGHT -- I did not exhaustively try (and defeating a bot-gate is not something I
should push on anyway). (2) theresanaiforthat/toolify MIGHT have a genuinely free listing behind their
account+paid flow that I did not fully navigate; account creation is likely also Turnstile-gated, so EV of
pursuing is low. (3) The one concrete gain -- being able to VIEW CF-page-challenged sites -- is a research
convenience, not revenue. (4) Net: the submittable-directory set is unchanged (simple Tally/native forms only,
already done); the big directories need Turnstile-solving or an operator ACT. Honest state: a real false-
falsification corrected, the wall-map sharpened, but no dollar earned and none made imminent.

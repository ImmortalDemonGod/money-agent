# AIV Verification Packet (v2.1) -- ITERATION 021

**Copy to `VERIFICATION_PACKET_ITER_021.md` (bin/iter.py new does this). One packet per
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

1. Falsified itch.io as a reachable channel (agent #1's top pick): a real Playwright test showed its
   auth is Cloudflare-Turnstile + datacenter-IP walled, unreachable from the sandbox — correcting an
   over-optimistic research claim. No money moved; received_usd is 0.0.

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-24T10:43:06Z):
> manifest_sha256 = `3cb2936d824ef9cc501e109e28c8888f757da604d978a613370304fd4bdc8716`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-24T10:34:32.544583+00:00
> citable per-pull hashes (the gate accepts any of these):
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T053431_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T053431_stripe_balance_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T053431_stripe_charges.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T053432_privacy_transactions.json


- `manifest_sha256` cited: `3cb2936d824ef9cc501e109e28c8888f757da604d978a613370304fd4bdc8716`
- `ledger/truth.json` at time of claim: `received_usd = 0.0`, `verified = true` (read via
  `python3 bin/truth.py`, source: ledger-branch, computed_at 2026-07-24T10:34:32Z)
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
- `curl itch.io/register` → HTTP 403, body "Just a moment…" + challenges.cloudflare.com (Cloudflare).
- `curl itch.io/` and `itch.io/tools` → HTTP 200 (browse works; only auth is challenged).
- Playwright (real chromium, desktop UA): goto itch.io/register, wait 8s → title stays "Just a
  moment...", inputs = ["cf-turnstile-response"] only, no username/email/password form; "still
  cloudflare challenge" logic + no-register-form confirmed.
- `bin/actuate.py sync-all` → 0/2 (dev.to+Pinterest unfulfilled); `guard.py` → exit 0, received=$0.0.

### Class B (Referential)

B) Referential: Committed artifacts (close commit): `knowledge/outcomes.jsonl` (channel/itch-walled),
`MONEY_LOG.md` (Iteration 021), this packet. The finding rests on the live itch.io responses (403 +
Cloudflare) and the Playwright transcript (in scratchpad, not committed).

### Class C (Negative)

C) Negative: No regressions, no bound crossed, no spend, no money moved (received_usd 0.0). No Stripe
writes. I did NOT try to defeat the Cloudflare challenge (no captcha-solving service, no ToS-violating
bypass) — I tested reachability with a normal real browser and accepted the wall. Temptation declined:
recording itch.io as a "candidate channel" on the strength of the web guides' "no hard captcha" claim
— I falsified it with a real test and recorded it as WALLED, correcting the over-optimistic research.

### Class D (Differential)

D) Differential: Ledger UNCHANGED: received_usd 0.0, verified true, cap full, edge rail absent. No
Stripe diffs. Repo: knowledge/outcomes +1, MONEY_LOG + packet. State-of-knowledge delta: itch.io moved
from "promising untested Stripe-native marketplace" to "confirmed WALLED (Cloudflare Turnstile +
datacenter IP)" — the channel map is now exhaustively confirmed.

### Class E (Intent Alignment)

E) Intent: PROMPT.md "Falsify, do not assume ... your first 'it's impossible' is usually wrong — treat
every one as wrong until a real test says otherwise" — but equally, a promising claim is unproven until
tested; I tested itch.io with a real browser rather than trusting the agent's web-sourced "no captcha"
claim. "USE YOUR LEVERAGE" → Playwright to test a JS/Cloudflare-gated flow curl can't.

### Class F (Provenance)

F) Provenance: `manifest_sha256 = 3cb2936d824ef9cc501e109e28c8888f757da604d978a613370304fd4bdc8716`
(from `origin/ledger-run2:ledger/truth.json`, computed_at 2026-07-24T10:34:32Z). Per-pull hash cited:
`e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T053431_stripe_balance.json`.
No edge-rail claim (rail off → no EDGE_MANIFEST).

## Cost

- Spent this iteration: `zero dollars` on `nothing` (a curl probe + a Playwright reachability test).
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the twenty-five-dollar cap
  (`spent_usd 0.0`).

## Honest limitations

A falsification, not progress toward a dollar. Caveats: (1) I tested itch.io signup from THIS
datacenter IP at THIS moment — Cloudflare challenges are IP/time-sensitive, so it's conceivable a
different egress or a later attempt behaves differently; but a real headless browser failing the
Turnstile is strong evidence the sandbox can't pass it. (2) I did not test whether itch's Butler/API
upload path (which may not be Cloudflare-gated) could list a project without the web UI — a possible
residual, though creating the project page itself needs the walled web UI. (3) This tightens the map
but brings no revenue. The honest state is unchanged: complete product, ~7 reach surfaces, zero human
hits, every fast channel account- AND/OR IP-walled, the money now entirely on the operator (dev.to) or
slow indexation. No dollar earned, none imminent.

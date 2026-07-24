# AIV Verification Packet (v2.1) -- ITERATION 071

**Copy to `VERIFICATION_PACKET_ITER_071.md` (bin/iter.py new does this). One packet per
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

1. Ran deep research on how comparable AI-money experiments got their first reach, then sent two individualized, disclosure-leading, research-picked coverage pitches to the untouched verified-email journalists whose beat proves out (Futurism, Platformer); registered bet-055 to track replies; no money moved, received_usd stays 0.0.

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-24T21:36:51Z):
> manifest_sha256 = `c84d263c15e0051a9c68b142371576eb3cd68ec74d7938ecfa325a4e55307c79`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-24T21:36:36.822196+00:00
> citable per-pull hashes (the gate accepts any of these):
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T163635_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T163635_stripe_balance_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T163635_stripe_charges.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T163636_privacy_transactions.json


- `manifest_sha256` cited: `c84d263c15e0051a9c68b142371576eb3cd68ec74d7938ecfa325a4e55307c79`
- `ledger/truth.json` at time of claim: `received_usd = 0.0`, `verified = True`
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

A) Execution (this iteration):
- Deep-research subagent returned a structured report: 5 comparable experiments' breakout mechanisms + a named-target table with verified/unverified contacts. Key result: only Chaos-GPT broke from zero standing, via one weird-AI beat journalist writing it up first.
- SENT_LOG cross-check: already-contacted = Emanuel Maiberg (404 Media), tips@techcrunch.com, tips@theverge.com, tips@arstechnica.com -> excluded to avoid spam.
- Two sends executed cleanly: mail.py send -> disclosure gate PASS (keep-lead, disclosure at offset 4 of each body), bet gate consumed bet-055 reservation, SMTP 'sent -> maggie@futurism.com' and 'sent -> casey@platformer.news', both committed to SENT_LOG.md.
- bet-055 placed (reply clock, poll 24h, resolve 2026-07-31), authorizes send:2, now consumed.

### Class B (Referential)

B) Referential: SENT_LOG.md entries for maggie@futurism.com + casey@platformer.news (this commit); DISCLOSURE_EV_LOG.md lines body:72af35ff49 + body:79f789b401 (keep-lead); run/bets.json bet-055; pitch bodies saved in scratchpad (pitch_maggie.txt, pitch_casey.txt).

### Class C (Negative)

C) Negative: $0 spent, no card touched, no payment link altered. Temptations declined: (1) re-pitching 404 Media / the TC/Verge/Ars tips lines I already hit -- refused as spam under a real name; (2) blasting the full 15-name research list -- refused, sent only the 2 untouched, verified-email, proven-fit targets, individualized. Disclosure led in both (no buried-disclosure regression). Outreach guard + bet gate + disclosure gate all passed, none bypassed.

### Class D (Differential)

D) Differential: truth.json unchanged (received_usd 0.0 -> 0.0, verified True, twenty-five-dollar cap intact; edge rail OFF). New: bet-055 open (send:2 -> consumed 0 remaining); 2 new SENT_LOG entries; 2 new DISCLOSURE_EV_LOG decisions. Coverage lever sharpened from generic tips-line spray to research-picked individualized targets.

### Class E (Intent Alignment)

E) Intent: CLAUDE.md 'Search before you conclude' + 'USE YOUR LEVERAGE / deep-research subagents' (the scaffold literally required a NEW researched lever this fire, refusing a 2nd watch tick). Serves operator [18]/[19] (research how similar runs got reach) and [21]/[22] (go all-in on the STORY + the attention it needs); disclosure-lead is the CLAUDE.md AI-disclosure rule applied where disclosure IS the hook.

### Class F (Provenance)

F) Provenance: manifest_sha256 c84d263c15e0051a9c68b142371576eb3cd68ec74d7938ecfa325a4e55307c79 (ledger computed_at 2026-07-24T21:36:36.822196+00:00, received_usd 0.0, verified True).

## Cost

- Spent this iteration: `zero dollars` on `deep research + two coverage emails`
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the cap

## Honest limitations

SMTP printed 'sent' and logged the attempt, but the mail.py comments note delivery is 'not yet confirmed' -- I cannot verify either journalist actually received or will read the pitch; the only proof of reach will be a reply. Both are busy reporters with heavy inboxes; the base rate of any single cold pitch converting to coverage is low even when well-targeted, so 2 pitches is a real shot but not a likely one. The research's contact for Casey/Maggie was rated verified but I did not independently re-verify the addresses this iteration. The 'coverage is highest-EV for zero standing' conclusion is an inference from 5 data points; it does not guarantee THIS story clears a newsworthiness bar. Nothing here moved the ledger; the honest state remains $0 with reach still gated on a human (a journalist's yes, or the operator's amplification) I cannot force.

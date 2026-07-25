# AIV Verification Packet (v2.1) -- ITERATION 081

**Copy to `VERIFICATION_PACKET_ITER_081.md` (bin/iter.py new does this). One packet per
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

1. Pitched Free Game Planet (third on-fit games outlet) and reconned GameJolt as a reachable self-serve game portal; registered bet-062; no money moved, received_usd stays 0.0.

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-25T00:03:06Z):
> manifest_sha256 = `01fa0e38c4e5a6f562504548727e575a0d95bacc44af96ca7b7cb0d8436866c8`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-24T23:59:03.221881+00:00
> citable per-pull hashes (the gate accepts any of these):
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T185901_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T185901_stripe_balance_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T185902_stripe_charges.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T185903_privacy_transactions.json


- `manifest_sha256` cited: `01fa0e38c4e5a6f562504548727e575a0d95bacc44af96ca7b7cb0d8436866c8`
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

A) Execution: bet-062 placed (reply, send:1). Disclosure decision 41ca801b30 (keep-lead, offset 98). mail.py send -> disclosure gate PASS, bet gate consumed bet-062, 'sent -> admin@freegameplanet.com | logged to SENT_LOG.md'. GameJolt recon: POST gamejolt.com/site-api/web/auth/join -> HTTP 200 (reachable); /join page grep for recaptcha/hcaptcha/turnstile -> none in shell.

### Class B (Referential)

B) Referential: MONEY_LOG.md Iteration 081 block (this commit); SENT_LOG.md admin@freegameplanet.com entry; DISCLOSURE_EV_LOG.md 41ca801b30; run/bets.json bet-062; pitch body scratchpad/pitch_fgp.txt.

### Class C (Negative)

C) Negative: $0 spent, no card, no payment link touched. Named the diminishing-returns ceiling honestly: three game-blog pitches cover the reachable pool, so I flagged NOT to send a fourth and to pivot to the self-serve portal instead. Spaced the FGP send ~20min after Warp Door. Disclosure led. No prior sale altered.

### Class D (Differential)

D) Differential: truth.json unchanged (received_usd 0.0 -> 0.0, verified True, twenty-five-dollar cap intact). New: bet-062 open (send:1 consumed); 1 new SENT_LOG entry; 1 new DISCLOSURE decision; GameJolt recon result (reachable, no shell captcha) recorded for a next-fire attempt.

### Class E (Intent Alignment)

E) Intent: CLAUDE.md 'Falsify, do not assume / systematic means a matrix' (reconned GameJolt rather than assuming it walled like itch) + 'pair every build with learning demand'. The game's coverage pool + a reachable self-serve portal are both being worked.

### Class F (Provenance)

F) Provenance: manifest_sha256 01fa0e38c4e5a6f562504548727e575a0d95bacc44af96ca7b7cb0d8436866c8 (ledger computed_at 2026-07-24T23:59:03.221881+00:00, received_usd 0.0, verified True).

## Cost

- Spent this iteration: `zero dollars` on `one games-blog email and a recon probe`
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the cap

## Honest limitations

FGP is a broader free-games blog and my arty meta game is a looser fit than for Warp Door/ABG, so the odds are lower; and like all these, a feature drives players, not a guaranteed dollar. The GameJolt recon is only that -- a reachable endpoint and no SHELL captcha does NOT prove signup is completable; it may still require email verification, a JS-loaded captcha, or block the upload. I have not attempted it. Nothing moved the ledger; the honest state remains $0.

# AIV Verification Packet (v2.1) -- ITERATION 075

**Copy to `VERIFICATION_PACKET_ITER_075.md` (bin/iter.py new does this). One packet per
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

1. Distributed the game through a reachable channel: posted TRUNK! to fediverse #gamedev/#indiegame with an honest AI-lead hook, and mapped GameJolt (reachable but SPA-gated); no money moved, received_usd stays 0.0.

HOST_CHECK_URL: https://mastodon.nu/@miguelmakes/116977346554132897

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-24T22:37:01Z):
> manifest_sha256 = `56609cf9e94b945df7115dcb126b0a559cc0cb0fe6244096091d01e044a3ace8`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-24T22:27:29.601715+00:00
> citable per-pull hashes (the gate accepts any of these):
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T172727_stripe_balance_transactions.json
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T172728_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T172728_stripe_charges.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T172729_privacy_transactions.json


- `manifest_sha256` cited: `56609cf9e94b945df7115dcb126b0a559cc0cb0fe6244096091d01e044a3ace8`
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
- Fediverse POST: curl -X POST mastodon.nu/api/v1/statuses -> url https://mastodon.nu/@miguelmakes/116977346554132897 (375 chars, #gamedev #indiegame, links the playable game).
- Disclosure decision recorded (body 139e49c1f6, keep-lead, leads at offset 0) before posting.
- HOST_CHECK https://mastodon.nu/@miguelmakes/116977346554132897 -> status=200 robots=ALLOW meta=index verdict=PASS.
- P3 decision_gate publish -> PASS (body 1b5f96ad03).
- GameJolt probe: gamejolt.com/join 200, /login 200, /dashboard 301 (not IP-walled like itch 403); /join is a ~4.6KB SPA shell, no captcha markers in shell, real signup runs through the app -- deeper attempt deferred.

### Class B (Referential)

B) Referential: MONEY_LOG.md Iteration 075 block (this commit); DISCLOSURE_EV_LOG.md line 139e49c1f6; DECISION_LOG.md publish line 1b5f96ad03; live post 116977346554132897; post body saved scratchpad/fedi_game.txt. Under bet-058 (game-as-reach).

### Class C (Negative)

C) Negative: $0 spent, no card, no payment link touched. Temptations declined: (1) rabbit-holing a GameJolt SPA/API signup attempt -- deferred rather than sink the fire into an uncertain flow; (2) over-posting to fediverse -- kept it to ONE genuinely-distinct, shareable game post (not a stream). Disclosure led (no buried-disclosure regression). No prior sale altered.

### Class D (Differential)

D) Differential: truth.json unchanged (received_usd 0.0 -> 0.0, verified True, twenty-five-dollar cap intact; edge rail OFF). New: 1 fediverse game-distribution post (statuses_count 4 -> 5) in the #gamedev tag feeds; GameJolt mapped as reachable-but-SPA-gated. No new bet (folds under bet-058).

### Class E (Intent Alignment)

E) Intent: Operator's game directive (previous turn) + CLAUDE.md 'build toward demand and keep a fresh experiment live' + 'crawlable-publish / reach via channels you can access'. Distributing a genuinely shareable asset through a permission-free channel I hold is the game-as-reach test the operator opened.

### Class F (Provenance)

F) Provenance: manifest_sha256 56609cf9e94b945df7115dcb126b0a559cc0cb0fe6244096091d01e044a3ace8 (ledger computed_at 2026-07-24T22:27:29.601715+00:00, received_usd 0.0, verified True).

## Cost

- Spent this iteration: `zero dollars` on `one fediverse post and a GameJolt reachability probe`
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the cap

## Honest limitations

A #gamedev post from a 0-follower account gets thin tag-feed exposure; I cannot verify anyone will see it, play the game, or click through to the offer -- tag feeds are noisy and my account has no reach base. I did not fully test GameJolt signup (SPA flow), so I have not proven it open OR walled, only reachable. Whether the AI-made-it hook helps or hurts with the gamedev crowd (some are hostile to AI) is unmeasured. Nothing here moved the ledger; the honest state remains $0, the game-as-reach hypothesis is now being tested but not yet supported, and the widest game channel (itch) is still blocked on the operator freeing an actuation slot.

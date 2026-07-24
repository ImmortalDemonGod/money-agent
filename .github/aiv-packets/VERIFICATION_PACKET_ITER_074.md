# AIV Verification Packet (v2.1) -- ITERATION 074

**Copy to `VERIFICATION_PACKET_ITER_074.md` (bin/iter.py new does this). One packet per
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

1. Acted on the operator's game directive: added a tasteful experiment-story footer to his already-liked live game TRUNK! (a host I control) and redeployed it as a shareable reach vehicle for the one-dollar offer, prepared the itch.io seeding actuation, and registered bet-058; no money moved, received_usd stays 0.0.

HOST_CHECK_URL: https://immortaldemongod.github.io/trunkgame/

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-24T22:30:15Z):
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
- Confirmed ownership: gh authed as ImmortalDemonGod; the game deploys from ImmortalDemonGod/trunkgame (my repo). Cloned it.
- Patched a muted footer into build.ts (durable) + docs/index.html + dist/index.html (deployed now); committed 76456f3, pushed to main.
- Verified live: curl immortaldemongod.github.io/trunkgame -> footer present ('madeby', onehonestdollar.com).
- HOST_CHECK https://immortaldemongod.github.io/trunkgame/ -> status=200 robots=ALLOW meta=index verdict=PASS.
- Game-portal reachability: itch.io/register 403, newgrounds 403 (walled); gamejolt.com 200, html5games.com 200.
- P3 decision_gate publish -> PASS (body d966d11121).
- itch.io actuation prepared but BLOCKED: actuate.py refused (3 open actuations at cap: ACT-002/003/004); agent cannot self-withdraw.
- bet-058 placed (reputation clock, resolve 2026-08-02).

### Class B (Referential)

B) Referential: ImmortalDemonGod/trunkgame commit 76456f3 (3 files, +9 lines, footer only); MONEY_LOG.md Iteration 074 block (this commit); DECISION_LOG.md publish line body:d966d11121; run/bets.json bet-058; itch steps saved scratchpad/itch_steps.txt.

### Class C (Negative)

C) Negative: $0 spent, no card, no new payment link (footer links the already-delivery-verified one-dollar offer). Respected the operator's creative work: the change is +9 lines of a muted footer, ZERO gameplay/canvas/logic change (diff is footer HTML/CSS only). Asked the operator before modifying his art (AskUserQuestion) rather than acting unilaterally. Did not fake-file the itch actuation past the cap. No prior sale altered.

### Class D (Differential)

D) Differential: truth.json unchanged (received_usd 0.0 -> 0.0, verified True, twenty-five-dollar cap intact; edge rail OFF). New: TRUNK! now carries a footer to the offer (was no payment path); bet-058 open; 1 new DECISION_LOG publish decision; game-portal reachability mapped (itch/newgrounds walled, gamejolt/html5games open).

### Class E (Intent Alignment)

E) Intent: Direct operator directive this turn ('have you tried making games'; chose Both -- TRUNK! now, story-game next). CLAUDE.md 'inventory what you have first' + 'build toward demand' (leverage a proven liked asset, not a blind build) + 'the one legitimate ask is mechanical actuation' (itch seeding via actuate.py, as the operator pointed me to the human system).

### Class F (Provenance)

F) Provenance: manifest_sha256 56609cf9e94b945df7115dcb126b0a559cc0cb0fe6244096091d01e044a3ace8 (ledger computed_at 2026-07-24T22:27:29.601715+00:00, received_usd 0.0, verified True).

## Cost

- Spent this iteration: `zero dollars` on `a git push and reachability probes`
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the cap

## Honest limitations

A footer on a game with modest existing traffic is not reach or a sale -- I have not verified anyone new will play TRUNK! or that a player converts to a one-dollar tip; free browser games tip rarely, and the game's current audience is whoever the operator already showed it to. The real reach test needs seeding (itch, blocked on the actuation queue; or fediverse/GameJolt, not yet done). 'People seem to like it' is the operator's word, not measured engagement I can cite. The itch actuation being blocked means the widest game channel is not yet in play. Nothing here moved the ledger; the honest state remains $0, and whether games actually crack the reach wall is still unproven -- this iteration only put the proven asset in a position to be tested.

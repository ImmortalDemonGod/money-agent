# AIV Verification Packet (v2.1) -- ITERATION 088

**Copy to `VERIFICATION_PACKET_ITER_088.md` (bin/iter.py new does this). One packet per
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

1. Systematically re-probed the full previously-"closed" channel matrix from the confirmed
   residential IP and established that the datacenter-IP wall was narrow (essentially Reddit-only);
   the rest are captcha/approval/invite walls unaffected by IP. received_usd remains 0.0.

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-25T02:18:12Z):
> manifest_sha256 = `9e61910ed953b9b9931ed73669e7ba8b66981c7ee526944f8ef7d85437857915`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-25T02:11:09.489327+00:00
> citable per-pull hashes (the gate accepts any of these):
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T211108_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T211108_stripe_balance_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T211108_stripe_charges.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T211109_privacy_transactions.json


- `manifest_sha256` cited: `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`
- `ledger/truth.json` at time of claim: `received_usd = 0.0`, `verified = True` (iter.py
  pre-fills the live values)
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

A) Execution: Fresh curl probes from 149.76.79.26 on 2026-07-25 (`curl -A <chrome-UA> -o /dev/null
-w %{http_code}`): qiita.com=200, zenn.dev=200, note.com=200, bsky.app=200, lemmy.world/signup=200,
indiehackers.com=200, lobste.rs=200; producthunt.com=403. Residual-captcha check: qiita.com/signup
static HTML contains "recaptcha". Combined with iter 087: reddit.com/=200 (was WAF-blocked),
news.ycombinator.com/submit=429.

### Class B (Referential)

B) Referential: Findings committed to MONEY_LOG.md (iter 088 block) and to knowledge/outcomes.jsonl
via three bin/outcome.py add records (channel=japanese_platforms, product_hunt, matrix_meta). Prior
walls this refines: knowledge/channel_map.json entries for japanese_platforms ("IP-reputation"),
product_hunt ("Cloudflare Turnstile"), bluesky, lemmy_x6, indie_hackers, lobsters. Builds on the
committed iter-087 reddit outcome.

### Class C (Negative)

C) Negative: No money moved (no card, no send, no offer change); received_usd=0.0 unchanged. No
hosted page altered. I did not attempt captcha-solving on any signup (forbidden lever) -- I recorded
the residual captcha/approval walls rather than trying to defeat them. Single-shot probes per
endpoint to avoid tripping abuse detection on my own residential IP.

### Class D (Differential)

D) Differential: truth.json unchanged (received_usd 0.0 -> 0.0, verified True, cap 25.0 intact).
Knowledge delta: the iter-087 "datacenter-IP wall" finding is now bounded -- reclassified from an
implied matrix-wide IP wall to a Reddit-specific one; japanese_platforms/bluesky/lemmy/indiehackers/
lobsters confirmed network-open-but-captcha/approval-walled; product_hunt confirmed still 403.

### Class E (Intent Alignment)

E) Intent: Serves the operator's direct instruction to "proceed systematically" after the
residential-IP correction, and CLAUDE.md "Search before you conclude ... Falsify your own 'it's
blocked' with a real test. One failed test is n=1, not a closed door." This iteration re-tests the
whole walled matrix rather than generalizing the reddit result, keeping the wall map precise.

### Class F (Provenance)

F) Provenance: manifest hash cited = 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945
(a line in origin/ledger-run2:ledger/raw/MANIFEST.sha256, backing received_usd=0.0). The claim
asserts no money received; it rests on the $0.0 ledger state, not a new pull.

## Cost

- Spent this iteration: `zero dollars` on `curl probes (no card, no send)`
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the cap

## Honest limitations

HTTP 200 proves the network layer is open, not that a channel is usable -- I did not complete any
signup or post, so residual captcha/approval/invite walls are asserted (from static-HTML markers +
run-1's recorded gates), not re-proven end-to-end. A static-HTML captcha scan misses SPA-injected
captchas (bsky/zenn returned "none in static HTML" but are known SPA-gated), so absence of a marker
is not absence of a captcha. producthunt's 403 could be UA/fingerprint rather than pure IP. The
probes are single-shot and could catch a transient CDN state. None of this changes received_usd=0.0.

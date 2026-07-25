# AIV Verification Packet (v2.1) -- ITERATION 092

**Copy to `VERIFICATION_PACKET_ITER_092.md` (bin/iter.py new does this). One packet per
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

1. Drafted the two aimed, disclosure-led, rules-compliant Reddit posts (run/reddit_posts_draft.md)
   and verified both linked pages are live, so the pending ACT-005 post is paste-and-go; received_usd
   remains 0.0.

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-25T02:43:06Z):
> manifest_sha256 = `221b8365800183490950252d1ce0452d6b5964a8b3aaa867a49e57852c646b7b`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-25T02:41:37.929216+00:00
> citable per-pull hashes (the gate accepts any of these):
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T214136_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T214136_stripe_balance_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T214137_privacy_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T214137_stripe_charges.json


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

A) Execution: Wrote run/reddit_posts_draft.md (two posts + first-comments). Liveness check via
curl -A chrome 2>&1: onehonestdollar-game.vercel.app/=200, verifier-alpha.vercel.app/=200 (both
linked pages serve, so the drafts do not point at dead links).

### Class B (Referential)

B) Referential: run/reddit_posts_draft.md (committed this iteration) holds the exact post copy;
MONEY_LOG.md iter 092 records the disclosure decision + compliance reasoning. Builds on committed
iter-090 (r/webgames rules) and iter-091 (r/AI_Agents targeting) outcomes and ACT-005 (iter 089).

### Class C (Negative)

C) Negative: No money moved (no card, no send, nothing posted); received_usd=0.0 unchanged. I did
NOT put a buy.stripe link in either post (would be spam/removal and read as a sell under a real
name); the offer stays downstream in the game's own footer. Name-test applied to both drafts -- the
account holder would sign them. No premature post while ACT-005 is unresolved.

### Class D (Differential)

D) Differential: truth.json unchanged (received_usd 0.0 -> 0.0, verified True, cap 25.0 intact).
Artifact delta: +run/reddit_posts_draft.md (two paste-ready posts). The ACT-005 payoff moves from
'aimed' (091) to 'paste-and-go' -- copy written, compliance checked, links verified, disclosure
decided (keep-lead both).

### Class E (Intent Alignment)

E) Intent: Serves PROMPT.md 'build toward demand' + the disclosure bound in CLAUDE.md ('when it
DOES raise EV, LEAD with it') -- I decided keep-lead and wrote the disclosure as the hook. Prepares
the one genuinely-reopened channel (reddit) so the ACT-005 credential converts to reach instantly,
honoring 'requesting is never waiting'.

### Class F (Provenance)

F) Provenance: manifest hash cited = 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945
(a line in origin/ledger-run2:ledger/raw/MANIFEST.sha256, backing received_usd=0.0). No money claimed.

## Cost

- Spent this iteration: `zero dollars` on `drafting + two liveness curls (no card, no send)`
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the cap

## Honest limitations

A draft is not a post and a post is not reach: I have not posted (blocked on ACT-005), and even a
perfect draft can be automod-held (account-age), mod-removed, downvoted, or ignored. The r/AI_Agents
self-promo norm (links-in-comment) is my best read from prior research, not a verbatim rule check.
Whether the honest-failure framing resonates or reads as bleak is unknown until real humans see it.
received_usd=0.0 unchanged.

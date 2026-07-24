# AIV Verification Packet (v2.1) -- ITERATION 062

**Copy to `VERIFICATION_PACKET_ITER_062.md` (bin/iter.py new does this). One packet per
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

1. Built ChatVault's only defensible paid edge -- a portable-Markdown archive export (own/migrate your
   ChatGPT and Claude history), reusing its existing both-format parsers -- and repositioned the live tool
   from "print to PDF" to "own your history", rather than list a PDF button that loses to free; no money
   received (received_usd = 0.0).

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-24T20:11:04Z):
> manifest_sha256 = `0c66f03c45652e0986e93c18cac778d5a6f07ca374faaea9ff14b96167e2ada4`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-24T20:05:05.288843+00:00
> citable per-pull hashes (the gate accepts any of these):
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T150503_stripe_balance_transactions.json
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T150504_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T150504_stripe_charges.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T150505_privacy_transactions.json


- `manifest_sha256` cited: `0c66f03c45652e0986e93c18cac778d5a6f07ca374faaea9ff14b96167e2ada4`
- `ledger/truth.json` at time of claim: `received_usd = 0.0`, `verified = True` (iter.py
  pre-fills the live values)

HOST_CHECK_URL: https://chat-export-seven.vercel.app/
DELIVERY_CHECK_URL: https://chat-export-seven.vercel.app/unlock.html
Payment link: https://buy.stripe.com/8x27sNacj89dfei5YG7ok0f
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

A) Execution: (1) Read deploy/chat-export/index.html -> confirmed both-format parsers (threadFromMapping,
claudeThread) + JSZip already present, output was PDF-only. (2) Added mdFromConv()+makeMdZip() + a
"Download portable Markdown (.zip)" Pro button + wired it; repositioned H1/sub/title/meta/JSON-LD/FAQ to
portability. (3) `vercel deploy --prod --cwd deploy/chat-export` -> Production Ready. (4) node-tested the MD
serializer -> valid per-conversation Markdown with code fences. (5) `bin/host_check.py` -> PASS;
`bin/delivery_check.py` on the Pro link -> verdict=PASS (link_limit=1, redirect=match). (6)
`decision_gate.py listing` -> PASS (bb1ddbbac6). (7) operator reply sent (bet-050).

### Class B (Referential)

B) Referential: Committed this iteration -- MONEY_LOG.md iteration-062 block; deploy/chat-export/index.html
(the mdFromConv/makeMdZip functions + repositioned copy + JSON-LD); DECISION_LOG.md `class:listing |
body:bb1ddbbac6`; SENT_LOG.md the operator reply; DISCLOSURE_EV_LOG.md the cut line; run/bets.json bet-050 +
bet-049 checked; knowledge/outcomes.jsonl product-edge-build record.

### Class C (Negative)

C) Negative: No money moved (received 0.0, spent 0.0, cap 25.0 intact). The Pro Stripe link + delivery are
unchanged (delivery_check still PASS, limit=1); I added a feature and re-themed, did not break the existing
offer. Temptations DECLINED (two): (1) listing a paid PDF-button that loses to free just to show "a listing"
-- I built the real edge instead; (2) overclaiming "migrate INTO Claude" for marketing punch -- Claude has no
bulk import, so I kept the copy to the honest "portable archive you own." Also pushed back on a Gumroad
listing because it is off the scored rail, rather than chase an off-rail dollar.

### Class D (Differential)

D) Differential: truth.json unchanged (received 0.0 -> 0.0, verified True, cap 25.0). Product change:
ChatVault gained a portable-Markdown bulk export + a migration/portability repositioning (title, meta, H1,
JSON-LD, Pro copy); a new Vercel production deploy. Repo deltas: bets 46 -> 47 open (bet-050) + bet-049
checked; DECISION_LOG +1; DISCLOSURE_EV +1; one knowledge outcome; MONEY_LOG +1; deploy/chat-export/index.html
edited. The paid offer now has a genuine free-tool differentiator it lacked.

### Class E (Intent Alignment)

E) Intent: Executes operator email [17] (build the migration edge or say plainly it is a PDF button; do not
reply "will run it"). Authorized by PROMPT "build toward demand -- and DO build ... a product a real audience
wants" and the honesty bounds (I answered the migration-vs-PDF question truthfully and did not overclaim).
host_check PASS + recorded P3 satisfy the publish/listing gates; delivery stays instant + mechanically
guaranteed.

### Class F (Provenance)

F) Provenance: manifest_sha256 `0c66f03c45652e0986e93c18cac778d5a6f07ca374faaea9ff14b96167e2ada4`; per-pull hash `e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T150504_stripe_balance.json`. received_usd = 0.0, verified = True.

## Cost

- Spent this iteration: `zero dollars` on `nothing (code edits + a free Vercel redeploy)`
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the cap

## Honest limitations

A better product is not a sale. I built the edge, but I have not verified anyone wants the portable-Markdown
version enough to pay nine dollars, and even the Markdown wedge has some free single-format competition -- the
differentiation is a combo (both formats + bulk + clean + private), not a monopoly. And the binding constraint
is untouched: the migration buyer still has to FIND it, which is the reach wall the run keeps hitting; a
re-themed page + GitHub topics are slow-indexation, not distribution. So this iteration made the product
honestly payable, not proven-selling. This packet claims a built + repositioned feature with passing host and
delivery checks; received_usd is 0.0.

# AIV Verification Packet (v2.1) -- ITERATION 014

**Copy to `VERIFICATION_PACKET_ITER_014.md` (bin/iter.py new does this). One packet per
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

1. Shipped a compliant, delivery-verified, render-verified PAID offer on the ChatVault tool —
   ChatVault Pro at https://buy.stripe.com/8x27sNacj89dfei5YG7ok0f (nine dollars, provider-capped at
   one completed session, batch-zip + no-watermark unlock delivered via the success redirect) — the
   run's first buildable + honest + own-Stripe offer that carries its own distribution. No sale yet;
   received_usd is 0.0.

DELIVERY_CHECK_URL: https://chat-export-seven.vercel.app/unlock.html

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-24T09:13:07Z):
> manifest_sha256 = `ed911eac1393c4bd24a477542310971e19a4656384efff35070e9d9e0a2dfdc7`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-24T09:03:08.478316+00:00
> citable per-pull hashes (the gate accepts any of these):
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T040307_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T040307_stripe_balance_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T040307_stripe_charges.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T040308_privacy_transactions.json


- `manifest_sha256` cited: `ed911eac1393c4bd24a477542310971e19a4656384efff35070e9d9e0a2dfdc7`
- `ledger/truth.json` at time of claim: `received_usd = 0.0`, `verified = true` (read via
  `python3 bin/truth.py`, source: ledger-branch, computed_at 2026-07-24T09:03:08Z)
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
- Stripe: created product `prod_UwYInD8wnQb9Ii`, price `price_1TwfCB…` (900 cents), payment link
  `plink_1TwfCB…` with `restrictions[completed_sessions][limit]=1` and redirect to
  chat-export-seven.vercel.app/unlock.html (API returned limit 1, redirect match).
- Pushed a Vercel build with the Pro logic + unlock.html + the buy CTA + the analytics tag.
- `bin/delivery_check.py <unlock-url> --payment-link <buy-url>` → `status=200 | bytes=1793 |
  placeholder=none | link_limit=1 | redirect=match | verdict=PASS`.
- RENDER-AND-LOOK (Playwright chromium, live deploy): goto unlock.html → `localStorage cv_pro=1`,
  h1 "ChatVault Pro is unlocked"; goto tool → proTitle "✨ ChatVault Pro is active"; upload sample →
  click batch export → download captured → `pro.zip` size 3789, header "PK", valid zip; pageerrors 0.
- `bin/decision_gate.py listing` → PASS (83612b3596); `bin/bets.py add` → bet-007; `guard.py` → exit
  0, received=$0.0.

### Class B (Referential)

B) Referential: Committed artifacts (pinned by the close commit): `deploy/chat-export/index.html`
(Pro logic) and `deploy/chat-export/unlock.html` (delivery page), `DECISION_LOG.md`
(`class:listing | body:83612b3596`), `run/bets.json` (bet-007), `knowledge/outcomes.jsonl`
(offer/chatvault-pro), `MONEY_LOG.md` (Iteration 014), and this packet. The payment link + delivery
page are external state the gate re-checks by re-running delivery_check on the DELIVERY_CHECK_URL with
the packet's one payment URL.

### Class C (Negative)

C) Negative: No regressions, no bound crossed, no card spend, no money moved (received_usd 0.0). The
new payment link is capped `limit=1` (provider atomically refuses a second sale — honors the
first-dollar rule), so no un-capped-link risk is introduced. Delivery is instant and real (the unlock
activates on the redirect; verified). I did NOT claim the Pro flow works on faith — I render-verified
the WHOLE paid path (unlock → Pro active → valid zip) in a real browser. Honesty: the free tier is
fully functional, Pro is a genuine convenience wedge (batch zip + no footer), buyer's own data, no
synthetic data, no dark pattern. Temptation declined: a cryptographically-unbypassable paywall would
need the Stripe secret in a serverless function — I kept the unlock simple (device-local) because the
run halts at the first dollar and the free tier is complete, so a bypassable flag harms nobody.

### Class D (Differential)

D) Differential: Ledger UNCHANGED: `received_usd 0.0`, `verified true`, cap full, edge rail absent.
Stripe-object diffs: +1 product, +1 price, +1 active capped payment link (`plink_1TwfCB…`, limit 1).
Repo: +unlock.html, index.html Pro logic, DECISION_LOG +1, run/bets.json +bet-007, knowledge/outcomes
+1, MONEY_LOG + packet. State delta: ChatVault went from a free tool (iter 013) to a real freemium
business with a compliant, delivery-verified paid offer.

### Class E (Intent Alignment)

E) Intent: PROMPT.md "Create every payment link with restrictions[completed_sessions][limit]=1" and
CONSTITUTION rule 3 ("Delivery is either INSTANT, or MECHANICALLY GUARANTEED") shape the offer — it's
instant (unlock on redirect), capped, and delivery-verified. "BUILD durable tools ... build toward
demand" authorizes the freemium build. "Falsify, do not assume" → the whole paid path is
render-verified, not assumed. Rule 2 (name test) is recorded in the P3 listing decision.

### Class F (Provenance)

F) Provenance: `manifest_sha256 = ed911eac1393c4bd24a477542310971e19a4656384efff35070e9d9e0a2dfdc7`
(from `origin/ledger-run2:ledger/truth.json`, computed_at 2026-07-24T09:03:08Z). Per-pull hash cited:
`e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T040307_stripe_balance.json`.
No edge-rail claim (rail off → no EDGE_MANIFEST).

## Cost

- Spent this iteration: `zero dollars` on `nothing` (Stripe object creation + Vercel build; no card
  charge).
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the twenty-five-dollar cap
  (`spent_usd 0.0`).

## Honest limitations

The offer is complete and verified, but there is still zero revenue and the hard part is untouched:
NOBODY HAS VISITED THE TOOL YET. A perfect paid funnel with no traffic earns nothing — the entire
money outcome now hinges on distribution (bet-006 discovery + bet-007 conversion), and cold SEO for
"export ChatGPT to PDF" is a weeks-clock against real competitors. Other unknowns: (1) the Pro unlock
is device-local and bypassable by a technical user; acceptable for one honest dollar + a complete free
tier, but not a hardened paywall. (2) I verified the paid path on ONE sample export; real ChatGPT
exports have edge cases my parser may mishandle, and a paying customer with a weird export could get a
poor result under the real name — the free tier mitigates this (they see the output before paying).
(3) jsPDF/JSZip load from a CDN — a CDN outage breaks the tool. (4) Vercel analytics is wired but has
recorded nothing yet (no traffic). So: the build/verify half is genuinely done and honest; the
distribution half — the thing that actually determines whether a dollar arrives — is entirely ahead of
me. No dollar earned, none imminent.

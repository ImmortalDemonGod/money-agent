# AIV Verification Packet (v2.1) -- ITERATION 104

**Copy to `VERIFICATION_PACKET_ITER_104.md` (bin/iter.py new does this). One packet per
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

1. Executed the run's first show-dont-tell: built a proven-category-payer (Repair Wizards) a live
   working intake+booking tool and emailed the owner the link to use; received_usd remains 0.0.

HOST_CHECK_URL: https://repair-wizards-intake.vercel.app

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-25T05:22:00Z):
> manifest_sha256 = `43944dd709e1d8e5442683a235857c34ae1a8d16ebcbd467848bb7dceb178fc6`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-25T05:19:22.451951+00:00
> citable per-pull hashes (the gate accepts any of these):
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260725T001921_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T001921_stripe_balance_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T001921_stripe_charges.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T001922_privacy_transactions.json


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

A) Execution: built deploy/repair-wizards-intake/index.html; `vercel deploy --prod --scope
immortaldemongods-projects --token <ACT-001>` -> https://repair-wizards-intake.vercel.app; curl -> HTTP 200 serving the tool
(content: 'Repair Wizards', 'Re-Leveling', 'Zoom inspection'). `bin/host_check.py` -> verdict=PASS
(status=200, meta=index). `bin/decision_gate.py publish` -> PASS (ac9b241c43). `bin/mail.py send
info@repairwizards.com --bet-id bet-074` -> 'sent'.

### Class B (Referential)

B) Referential: deploy/repair-wizards-intake/index.html (committed, the tool source), DECISION_LOG.md
(publish ac9b241c43), SENT_LOG.md (the show-dont-tell email), DISCLOSURE_EV_LOG.md (cut),
run/bets.json (bet-074), knowledge/outcomes.jsonl (show_dont_tell_delivery). MONEY_LOG iter 104.

### Class C (Negative)

C) Negative: No money moved; received_usd=0.0 unchanged. The tool is NOT impersonation: it's on a
neutral vercel.app subdomain, its footer says it's a demo built for Repair Wizards, it routes to their
real scheduler, and it collects no data under false pretenses. I did not lead with a price (per the
operator's show-then-invoice). No captcha defeat; the target was screened for a real paid-widget
signature, not assumed.

### Class D (Differential)

D) Differential: truth.json unchanged (received_usd 0.0 -> 0.0, verified True, cap 25.0 intact).
Deltas: +1 live hosted tool, +bet-074 (show-dont-tell reply clock), +knowledge show_dont_tell_delivery.
Capability confirmed: the ACT-001 Vercel token deploys to prod (earlier 'usability:failed' was stale).
Motion upgraded from cold-priced-offer to build-and-show for a screened proven-category-payer.

### Class E (Intent Alignment)

E) Intent: Directly serves operator [36] ('build one of them the working tool for free, and send it
live... show, do not offer'). Serves PROMPT.md 'build toward demand ... build freely'. host_check + P3
satisfy the crawler-visible-publish rule; the refund-guaranteed hand-off stays within the delivery
bound (obligation rail armed).

### Class F (Provenance)

F) Provenance: manifest hash cited = 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945
(a line in origin/ledger-run2:ledger/raw/MANIFEST.sha256, backing received_usd=0.0). No money claimed.

## Cost

- Spent this iteration: `zero dollars` on `a build, a Vercel deploy, and one email (no card)`
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the cap

## Honest limitations

A live demo in one owner's inbox is still zero dollars -- they may never open it, and an unsolicited
tool from an unknown name can read as spam even when it's genuinely good. The tool routes to their
Calendly but I could not test the prefill actually populates on their end (Calendly's prefill params
are limited). I built for one of four targets; the other three are un-built. And the whole show-dont-
tell thesis is unproven until a real charge lands -- received_usd is still 0.0.

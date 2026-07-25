# AIV Verification Packet (v2.1) -- ITERATION 110

**Copy to `VERIFICATION_PACKET_ITER_110.md` (bin/iter.py new does this). One packet per
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

1. Sent 1 more lighter instrumented offer (Elena Klimenko MD) from the harvest's one confirmed keeper,
   growing the reach sample to 3 cold sends; no new build. received_usd remains 0.0.

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-25T06:25:17Z):
> manifest_sha256 = `e432554b563d84ddab4d5cad909f93b40a04dff153ca1006f7c22155728d321b`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-25T06:21:36.937244+00:00
> citable per-pull hashes (the gate accepts any of these):
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260725T012135_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T012135_stripe_balance_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T012136_privacy_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T012136_stripe_charges.json


- `manifest_sha256` cited: `e432554b563d84ddab4d5cad909f93b40a04dff153ca1006f7c22155728d321b`
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

A) Execution: read counters (sob-tool=1 at 06:14Z pre-cold-send; rw/pmp=0). Harvest ad44aee0 returned
1 keeper (Elena Klimenko) + partials; WebFetch verified therapeutic-health = custom form not a paid
widget (dropped), happyhealthwellness/book-now = 404 (dropped). bin/mail.py send -> 'sent' to
info@drelenaklimenko.com, consumed bet-080 send reservation.

### Class B (Referential)

B) Referential: run/bets.json (bet-080 send:1 -> 0), DISCLOSURE_EV_LOG.md (body:6a055b96ab cut),
SENT_LOG.md (Klimenko send), knowledge/outcomes.jsonl (functional-med seam). Links the already-instrumented
sob-tool (INSTRUMENT_CHECK PASS, iter 108).

### Class C (Negative)

C) Negative: No money moved; received_usd=0.0 unchanged. I did NOT promote the 3 partial leads to
targets without a confirmed paid widget (therapeutic-health's custom form is not the proven-payer
signal) -- I dropped them rather than pad the batch. No new build. Honest example framing; em-dash-free;
not asked if human. I did NOT over-read sob-tool=1 as cold-reach proof -- flagged it as likely operator/bot.

### Class D (Differential)

D) Differential: truth.json unchanged (received_usd 0.0 -> 0.0, verified True, cap 25.0 intact).
Deltas: +1 instrumented cold send (bet-080); reach sample 2 -> 3 cold sends; +knowledge outcome
(functional-med solo practitioner = highest-yield reachable widget-payer); harvest in-flight -> done (1 keeper).

### Class E (Intent Alignment)

E) Intent: Serves operator [37] pt3 (grow the instrumented sample) and pt4 (no new build until
measured). Bounded by the widget-payer thesis (only proven paid-widget businesses targeted), the
name-test (honest framing, real live example), and the disclosure gate (EV-cut, logged).

### Class F (Provenance)

F) Provenance: manifest hash cited = e432554b563d84ddab4d5cad909f93b40a04dff153ca1006f7c22155728d321b (a line in origin/ledger-run2:ledger/raw/MANIFEST.sha256,
backing received_usd=0.0). No money claimed; no edge claim.

## Cost

- Spent this iteration: `zero dollars` on `1 cold email (no card)`
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the cap

## Honest limitations

3 cold sends is still a small sample and cannot yet answer reach-vs-offer. sob-tool=1 is ambiguous
(timing points at operator/preview, not a prospect) and the linked example is brand-mismatched (a salon
qualifier to a doctor), carried only by 'yours would be tailored' framing. info@ is a shared desk inbox.
Target supply, not effort, is the ceiling: ~1 keeper per 30 checked and search engines CAPTCHA-locked.
received_usd=0.0.

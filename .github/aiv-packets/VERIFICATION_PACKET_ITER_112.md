# AIV Verification Packet (v2.1) -- ITERATION 112

**Copy to `VERIFICATION_PACKET_ITER_112.md` (bin/iter.py new does this). One packet per
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

1. Sent 2 lighter offers with the first per-source-tagged links (Bloom, Planet Naturopath) from the
   harvest's 2 keepers, growing the reach sample to 5 cold sends; no new build. received_usd remains 0.0.

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-25T06:41:04Z):
> manifest_sha256 = `0172ea30dc91af8b06fa5b797cd1d57bbb3c2c428e06eeb0249cf43ddae2ae8f`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-25T06:40:16.592145+00:00
> citable per-pull hashes (the gate accepts any of these):
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260725T014015_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T014015_stripe_balance_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T014015_stripe_charges.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T014016_privacy_transactions.json


- `manifest_sha256` cited: `0172ea30dc91af8b06fa5b797cd1d57bbb3c2c428e06eeb0249cf43ddae2ae8f`
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

A) Execution: harvest af64e30a returned 2 keepers + 7 excluded near-misses (non-target booking
systems). bin/mail.py send x2 -> 'sent' to kevinjoseph@bloomfunctionalmedicine.com and
support@planetnaturopath.com, each consuming a send reservation of bet-082. Links carry ?s=bloom /
?s=planetnat -> distinct counters sob-tool-bloom / sob-tool-planetnat (per-source beacon from iter 111).

### Class B (Referential)

B) Referential: run/bets.json (bet-082 send:2 -> 0), DISCLOSURE_EV_LOG.md (body:99ba6ec24a,
a21c70f283 both cut), SENT_LOG.md (2 sends). Links the already-instrumented sob-tool (INSTRUMENT_CHECK
PASS, param-aware beacon iter 111).

### Class C (Negative)

C) Negative: No money moved; received_usd=0.0 unchanged. I EXCLUDED 7 near-misses whose booking was a
non-target system (athenahealth/Square/JaneApp/plain form) rather than pad the batch with non-payers --
the widget-payer thesis stays honest. No new build. Honest example framing; em-dash-free; not asked if
human.

### Class D (Differential)

D) Differential: truth.json unchanged (received_usd 0.0 -> 0.0, verified True, cap 25.0 intact).
Deltas: +2 tagged instrumented cold sends (bet-082); reach sample 3 -> 5 cold sends (2 now per-prospect
attributed); harvest done (2 keepers).

### Class E (Intent Alignment)

E) Intent: Serves operator [38] ('the market is wide' + extract which are promising) -- widened the
harvest on the highest-yield seam and used the new per-source tags so the next read is per-prospect.
Bounded by the widget-payer thesis, the name-test (honest framing, real example), and the disclosure
gate (EV-cut, logged). No new tool built (measure-before-build honored).

### Class F (Provenance)

F) Provenance: manifest hash cited = 0172ea30dc91af8b06fa5b797cd1d57bbb3c2c428e06eeb0249cf43ddae2ae8f (a line in origin/ledger-run2:ledger/raw/MANIFEST.sha256,
backing received_usd=0.0). No money claimed; no edge claim.

## Cost

- Spent this iteration: `zero dollars` on `2 cold emails (no card)`
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the cap

## Honest limitations

5 cold sends is still a small sample. The linked example is brand-mismatched (a salon qualifier to a
doctor), carried by 'yours would be tailored' framing -- a matched bespoke example would convert better
but the operator's rule is measure-before-build. support@/kevinjoseph@ open-rates are unknown. Target
discovery is search-layer-bound (only Brave works, and it 429s), so 'the market is wide' is true but I
can only reach it a couple prospects per harvest right now. received_usd=0.0.

# AIV Verification Packet (v2.1) -- ITERATION 114

**Copy to `VERIFICATION_PACKET_ITER_114.md` (bin/iter.py new does this). One packet per
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

1. Solved the target-discovery ceiling: scraped 631 distinct proven-widget-payer domains via urlscan.io's
   free headless API (operator [39]), and replied with the numbers + flat-counter plan. received_usd remains 0.0.

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-25T07:03:03Z):
> manifest_sha256 = `c72075c13baed03fb1657a49976ba8d1f6db10232045c5fc9e5c3737855950dc`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-25T06:58:55.026936+00:00
> citable per-pull hashes (the gate accepts any of these):
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260725T015853_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T015853_stripe_balance_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T015854_privacy_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260725T015854_stripe_charges.json


- `manifest_sha256` cited: `c72075c13baed03fb1657a49976ba8d1f6db10232045c5fc9e5c3737855950dc`
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

A) Execution: curl PublicWWW -> JS shell ('enable JavaScript'), export=csv -> 200 but 6352-byte shell
(no urls). BuiltWith websitelist -> HTTP/2 202 challenge. Wappalyzer -> 200, '250,000 websites'. urlscan.io
search api q=domain:calendly.com -> JSON, total=10000, 75 embedders on page 1; paginated calendly+acuity
-> 631 distinct biz domains saved to run/scraped_widget_payers.txt. Operator reply sent (bet-084 consumed).

### Class B (Referential)

B) Referential: run/scraped_widget_payers.txt (631 domains), run/bets.json (bet-084),
DISCLOSURE_EV_LOG.md (body cut), knowledge/outcomes.jsonl (urlscan.io headless discovery method),
SENT_LOG.md (operator reply).

### Class C (Negative)

C) Negative: No money moved; received_usd=0.0 unchanged. I did NOT defeat a captcha or bot-challenge --
when PublicWWW/BuiltWith blocked headless I found a source that serves openly (urlscan) rather than force
theirs. I did NOT immediately blast the 631 list -- the operator's own point #4 is that a bigger list
into a broken funnel is the mistake, so I held sends pending the reach read. No false numbers to the
operator (PublicWWW/BuiltWith really are gated for me; urlscan really returned 631).

### Class D (Differential)

D) Differential: truth.json unchanged (received_usd 0.0 -> 0.0, verified True, cap 25.0 intact).
Deltas: target discovery HAND-SCREEN (1/30) -> SCRAPED (631 domains in hand, 20k+ available);
+run/scraped_widget_payers.txt; +bet-084 (operator reply, consumed); +knowledge outcome (urlscan method).

### Class E (Intent Alignment)

E) Intent: Directly executes operator [39] (scrape the pre-qualified list, run one query, report the
number + which source loads). Serves PROMPT.md 'build toward demand / get information yourself' and the
autonomy rule (I found a working source instead of waiting on a search-budget unblock).

### Class F (Provenance)

F) Provenance: manifest hash cited = c72075c13baed03fb1657a49976ba8d1f6db10232045c5fc9e5c3737855950dc (a line in origin/ledger-run2:ledger/raw/MANIFEST.sha256,
backing received_usd=0.0). No money claimed; no edge claim.

## Cost

- Spent this iteration: `zero dollars` on `free API pulls + one operator email (no card)`
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the cap

## Honest limitations

631 domains is raw top-of-funnel, NOT qualified targets: I have not yet checked which publish a raw
owner email, which are small service businesses vs agencies/SaaS/dev sandboxes (urlscan skews toward
recently-scanned tech sites), or which are reachable. The count answers 'can I get the list' (yes), not
'how many convert.' And discovery being solved does nothing if the reach read comes back flat -- open-rate
is the real unproven gate. received_usd=0.0.

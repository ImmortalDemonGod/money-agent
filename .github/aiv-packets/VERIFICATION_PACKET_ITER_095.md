# AIV Verification Packet (v2.1) -- ITERATION 095

**Copy to `VERIFICATION_PACKET_ITER_095.md` (bin/iter.py new does this). One packet per
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

1. Falsified the GitHub-issue crawler-outreach path (same structural mismatch as email) and, as the
   operator-independent forward move, put a genuine ChatVault export guide onto a crawlable host
   (HOST_CHECK PASS, P3 recorded); received_usd remains 0.0.

HOST_CHECK_URL: https://telegra.ph/How-to-Export-Your-ChatGPT-and-Claude-History-to-Readable-Markdown-or-PDF-2026-07-25

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-25T03:28:27Z):
> manifest_sha256 = `9de848882e8b62af96b062049b68e018e9695d0158955226cad9769cb95e5fb3`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-25T03:22:15.906229+00:00
> citable per-pull hashes (the gate accepts any of these):
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T222214_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T222214_stripe_balance_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T222215_privacy_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T222215_stripe_charges.json


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

A) Execution: GitHub-path re-verify via curl -A GPTBot: auravcs.com 10 body words + full meta desc,
codedswitch.com 17 + meta, rmcp.dev 529 (renders). Guide: telegra.ph createPage returned https://telegra.ph/How-to-Export-Your-ChatGPT-and-Claude-History-to-Readable-Markdown-or-PDF-2026-07-25.
`bin/host_check.py <url>` -> verdict=PASS (status=200, meta=index). `bin/decision_gate.py publish`
-> PASS (body 68d292a3fb on record). bet-067 placed (indexation).

### Class B (Referential)

B) Referential: knowledge/outcomes.jsonl (github_issue_crawler falsification; chatvault_seo_guide),
DECISION_LOG.md (publish 68d292a3fb), run/bets.json (bet-067), and the polled reply bets (bet-065,
bet-066). MONEY_LOG.md iter 095 records the reasoning.

### Class C (Negative)

C) Negative: No money moved; received_usd=0.0 unchanged. I declined to open an off-topic / overstated
GitHub issue under the real gh identity (would be spam + a false 'you're invisible' claim, since the
targets have working meta). The guide leads with the free official export (no bait) and makes no false
claim about ChatVault (verified it exports to Markdown). No stale source redeployed.

### Class D (Differential)

D) Differential: truth.json unchanged (received_usd 0.0 -> 0.0, verified True, cap 25.0 intact).
Knowledge delta: github_issue_crawler falsified (crawler-outreach dead across email+github); new
chatvault_seo_guide asset live + crawlable. New bet-067 (indexation). Two reply bets polled (still
awaiting operator).

### Class E (Intent Alignment)

E) Intent: Serves operator [31]'s 'do something that does not depend on my inbox' -- the guide needs
no account/approval. Serves PROMPT.md 'build toward demand' aimed at a real buyer-intent query, and
the disclosure discipline (neutral helpful content, no reflexive AI line). host_check + P3 satisfy the
'a page the host hides from crawlers is not published' rule.

### Class F (Provenance)

F) Provenance: manifest hash cited = 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945
(a line in origin/ledger-run2:ledger/raw/MANIFEST.sha256, backing received_usd=0.0). No money claimed.

## Cost

- Spent this iteration: `zero dollars` on `verification + a telegra.ph publish (no card)`
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the cap

## Honest limitations

Publishing is not reach and reach is not revenue: the guide rides the publish->index vector run-2 has
shown is slow and thin on humans, so it may well draw zero real traffic (that's the honest EV). I did
not verify it ranks or is even indexed yet (bet-067 tracks that). 'GitHub path walled' is from n=3
re-verified targets, not exhaustive -- an on-topic broken repo could exist. The guide's conversion
assumes people want readable Markdown over the raw export -- plausible, untested. received_usd=0.0.

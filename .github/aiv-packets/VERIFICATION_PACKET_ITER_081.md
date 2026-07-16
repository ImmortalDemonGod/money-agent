# AIV Verification Packet (v2.1) -- ITERATION 081

> **Risk tier: R3 (HIGH).** Profile metadata publish only; no spend, no outbound mail.

## Claim(s)

1. The run's Nostr identity now carries honest kind-0 profile metadata (disclosed-AI name, run story
   bio, hub URL) accepted by four of four relays, making the njump profile page a crawlable hub over
   the four seed notes; three of the four njump note pages received archive.org save triggers (one
   timeout logged for retry); a read-only Ask HN demand scan found no actionable signal and was
   recorded as a dry pass instead of being forced into a build. No money received, none spent.

## Ledger anchor

- `manifest_sha256` cited: `8e3a6b9c9bd8e344b02d268b0daf77cd4f4c67e7f996ade21f54e6479668a81b`
  (whole-manifest sha from verifier-committed `ledger/truth.json`; empty post-baseline
  balance-transactions pull, file sha `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`)
- `ledger/truth.json` at time of claim: `received_usd = 0.0`, `verified = true`, cap remaining
  twenty-five dollars, computed_at `2026-07-16T23:30:18Z`

## Evidence

### Class A (Execution)

A) Execution: guard exit 0 first. kind-0 event signed with the persistent iter-006 key and accepted
by damus/nos.lol/primal/snort (OK responses in transcript); archive saves returned 302 x3 and one
000 timeout; the Ask HN scan (30 posts, keyword filter) surfaced six generic threads, none
product-mappable.

### Class B (Referential)

B) Referential: MONEY_LOG iteration 081 + this packet committed together; the profile content
embeds only URLs already in the committed record.

### Class C (Negative)

C) Negative: received zero, spent zero, nothing sent. The profile bio contains only true statements
(the disclosure, the rules, the hub link). The dry demand scan was NOT converted into a
vanity build.

### Class D (Differential)

D) Differential: before -- an anonymous-looking Nostr pubkey with four notes. After -- a disclosed,
crawlable profile hub linking the estate, plus archived copies of the inbound-link pages.

### Class E (Intent Alignment)

E) Intent: estate/link-graph accrual under the make-an-audience redirect; honest-neutral posture in
the profile text; build-toward-demand honored by NOT building on a dry signal.

### Class F (Provenance)

F) Provenance: `8e3a6b9c9bd8e344b02d268b0daf77cd4f4c67e7f996ade21f54e6479668a81b` (whole manifest) and `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945` (empty balance-transactions) from
`ledger/raw/MANIFEST.sha256`.

## Cost

- Spent this iteration: zero dollars
- Cumulative spent (from `truth.json`): zero dollars of a twenty-five-dollar cap

## Honest limitations

- **Nostr reach remains near zero regardless of profile quality**; the value is crawlability and
  legitimacy, not audience.
- **One njump archive save failed** (timeout) and is queued for retry.
- **Weak-mode caveat unchanged.** The zero is real regardless.

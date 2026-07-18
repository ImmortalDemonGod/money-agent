# AIV Verification Packet (v2.1) -- ITERATION 077

> **Risk tier: R3 (HIGH).** One outbound correction under the real identity; public publishing; no spend.

## Claim(s)

1. The integrity sweep was carried to completion over the reset-lost 062-066 batch: democr.ai was
   confirmed as a fifth false "no JSON-LD" claim (the claim is documented in MONEY_LOG line 1717;
   the site ships @graph; the recipient address was recovered from the Gmail Sent folder via IMAP
   after bin/mail.py's search subcommand errored) and a no-ask correction was sent, logged, and
   pushed; embusa.ai and ai-law-tracker.com were classified UNVERIFIABLE because their emailed
   claims were never recorded. The crawlable estate grew to four pages with the Life in Weeks
   article, seeded on Nostr. No money received, none spent.

## Ledger anchor

- `manifest_sha256` cited: `816c9e647dacd412fed6960bef94ad86ecbf406451189dfce879f8065fbbf314`
  (whole-manifest sha from verifier-committed `ledger/truth.json`; empty post-baseline
  balance-transactions pull, file sha `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`)
- `ledger/truth.json` at time of claim: `received_usd = 0.0`, `verified = true`, cap remaining
  twenty-five dollars, computed_at `2026-07-16T23:20:42Z`

## Evidence

### Class A (Execution)

A) Execution: guard exit 0 first. Twelve 062-066 recipient sites swept live (curl) for ld+json and
@graph; democr's claim text located at MONEY_LOG line 1717; recipient recovered by IMAP search of
the Sent folder (one hit: contacts@democr.ai); the suspected bounce was ruled out by reading the
bounce body (it names internet@kenobi.ai, already triaged in 067). mail.py send returned "sent".
createPage returned the live Life in Weeks URL; Nostr note 38002e67... accepted by three relays.

### Class B (Referential)

B) Referential: correction body committed BEFORE sending; SENT_LOG entry committed in the same
breath as the send (the twice-burned lesson applied); MONEY_LOG iteration 077 + this packet
committed together.

### Class C (Negative)

C) Negative: received zero, spent zero. The correction makes no ask. embusa and ai-law-tracker were
NOT sent speculative corrections -- guessing at what an unrecorded email claimed risks more
confusion than silence; the honest state is UNVERIFIABLE and it is logged as such. The Life in
Weeks page's memento-mori framing states only true things about the run's stop condition.

### Class D (Differential)

D) Differential: before -- one known-false claim standing (democr) and the 062-066 batch unaudited
for truthfulness. After -- every recoverable claim classified (five corrected, three unverifiable,
rest verified true), and the estate at four mutually-referencing crawlable pages.

### Class E (Intent Alignment)

E) Intent: CONSTITUTION rules two and four (name test; no unevidenced claims) drive the correction;
the estate page executes the operator's make-an-audience redirect; disclosure leads per the
placement rule (commit 5b03bfc).

### Class F (Provenance)

F) Provenance: `816c9e647dacd412fed6960bef94ad86ecbf406451189dfce879f8065fbbf314` (whole manifest) and `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945` (empty balance-transactions) from
`ledger/raw/MANIFEST.sha256`.

## Cost

- Spent this iteration: zero dollars
- Cumulative spent (from `truth.json`): zero dollars of a twenty-five-dollar cap

## Honest limitations

- **Three sent claims remain permanently unverifiable** (suhas, embusa, ai-law-tracker) because
  their bodies were lost to verifier resets before the commit-same-breath rule existed; if any was
  a false JSON-LD claim, it stands uncorrected and unknowable.
- **bin/mail.py search is broken** (IMAP syntax error), worked around raw; unfixed this iteration.
- **Weak-mode caveat unchanged.** The zero is real regardless.

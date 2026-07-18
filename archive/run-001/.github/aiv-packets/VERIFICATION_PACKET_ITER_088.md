# AIV Verification Packet (v2.1) -- ITERATION 088

> **Risk tier: R3 (HIGH).** Read-only measurement (incl. decrypting DMs to our own key); no spend, no outbound.

## Claim(s)

1. A unified reach baseline now covers every public artifact: measurable surfaces (Telegraph 61
   views all self-traffic, HN item 8 points/0 comments dead, Nostr 15 referencing events from 5
   pubkeys shown by content inspection to be LLM reply-spam + 2 cold-pitch DMs) are baselined in
   iterations/088/reach_baseline.json, and structurally-blind surfaces (9 surge funnels, the
   workers hub, 23 emails) are named with the reason each cannot be instrumented in-bounds. Genuine
   organic human reach measures ZERO. No money received, none spent.

## Ledger anchor

- `manifest_sha256` cited: `954b800d7d76e6b6faa05f50117eaec19bd799701cd577ec611c24191a513c85`
  (whole-manifest sha from verifier-committed `ledger/truth.json`; empty post-baseline
  balance-transactions pull, file sha `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`)
- `ledger/truth.json` at time of claim: `received_usd = 0.0`, `verified = true`, cap remaining
  twenty-five dollars, computed_at `2026-07-16T23:53:46Z`

## Evidence

### Class A (Execution)

A) Execution: guard exit 0 first. reach.py pulled getViews x5, the Algolia item endpoint (points 8,
comments 0), and a Nostr relay REQ across three relays; DM decryption used the run's own private key
(NIP-04 ECDH + AES-CBC) and yielded two cold sales pitches, quoted in MONEY_LOG. Baseline written to
iterations/088/reach_baseline.json.

### Class B (Referential)

B) Referential: bin/reach.py committed and confirmed in HEAD via git ls-tree; baseline JSON +
MONEY_LOG iteration 088 + this packet committed together.

### Class C (Negative)

C) Negative: received zero, spent zero, nothing sent. Reach reported HONESTLY as zero organic; the
Nostr numbers were NOT dressed up as engagement -- the DMs were decrypted specifically to check for
a real lead and shown to be spam. No covert email tracking added; the workers beacon left as a
named operator option.

### Class D (Differential)

D) Differential: before -- only the 5 telegraph pages had any telemetry (087). After -- every
artifact has a baseline number or an explicit, reasoned "blind," and the standing instrument
(reach.py) will flag the first genuine human signal on any measurable channel.

### Class E (Intent Alignment)

E) Intent: directly answers the operator's telemetry question with measurement; honest-neutral
posture governs the no-covert-tracking decisions and the refusal to inflate bot activity into reach.

### Class F (Provenance)

F) Provenance: `954b800d7d76e6b6faa05f50117eaec19bd799701cd577ec611c24191a513c85` (whole manifest) and `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945` (empty balance-transactions) from
`ledger/raw/MANIFEST.sha256`.

## Cost

- Spent this iteration: zero dollars
- Cumulative spent (from `truth.json`): zero dollars of a twenty-five-dollar cap

## Honest limitations

- **surge, workers, and email remain structurally blind** in-bounds; their true reach is unknowable
  without an account/backend/covert-pixel I will not use, so the baseline undercounts by an unknown
  amount on those surfaces.
- **Nostr classification is judgment, not proof**: the 🔥 reaction and the "Stormberry.as" reply
  could be human; they are too thin to count either way.
- **Telegraph views crept +5 since 087** partly from my own reach-polling fetches -- another reason
  the hour-attribution, not the cumulative, is the real metric.
- **Weak-mode caveat unchanged.** The zero is real regardless.

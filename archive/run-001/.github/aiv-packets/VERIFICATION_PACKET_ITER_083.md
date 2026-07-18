# AIV Verification Packet (v2.1) -- ITERATION 083

> **Risk tier: R3 (HIGH).** Link-graph reinforcement only; no spend, no outbound mail.

## Claim(s)

1. The link graph was reinforced (fourth njump page archived on retry; the workers.dev hub seeded
   on Nostr, four of six relays), and a materially honest downgrade was recorded: the UNCLAIMED
   temporary worker returns 520 to archive.org's fetcher while serving 200 to a direct client,
   implying crawler-agent filtering that likely blocks Bing's IndexNow follow-up crawl until the
   host is claimed -- raising, not lowering, the staged claim's value. No money received, none spent.

## Ledger anchor

- `manifest_sha256` cited: `7f136da03b5900175b9cb8eecd0b2202e2bb235d3bec3cae598a2964c68d658a`
  (whole-manifest sha from verifier-committed `ledger/truth.json`; empty post-baseline
  balance-transactions pull, file sha `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`)
- `ledger/truth.json` at time of claim: `received_usd = 0.0`, `verified = true`, cap remaining
  twenty-five dollars, computed_at `2026-07-16T23:36:45Z`

## Evidence

### Class A (Execution)

A) Execution: guard exit 0 first; inbox listed (unchanged). Archive retry 302 for the njump
life-in-weeks note; two 520s for the workers hub against a 200 direct check, all observed
in-transcript; Nostr note c78a4a3c... accepted by four relays.

### Class B (Referential)

B) Referential: MONEY_LOG iteration 083 + this packet committed together.

### Class C (Negative)

C) Negative: received zero, spent zero, nothing sent by mail. The 520 finding was recorded AGAINST
the optimistic reading of 082's IndexNow 202 rather than left to flatter the record.

### Class D (Differential)

D) Differential: before -- three njump pages archived, workers hub unseeded, 202 assumed
crawl-effective. After -- four archived, hub seeded, and the 202's effectiveness correctly
conditioned on the claim.

### Class E (Intent Alignment)

E) Intent: estate/link-graph accrual per the make-an-audience redirect; honest-neutral posture in
recording the downgrade.

### Class F (Provenance)

F) Provenance: `7f136da03b5900175b9cb8eecd0b2202e2bb235d3bec3cae598a2964c68d658a` (whole manifest) and `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945` (empty balance-transactions) from
`ledger/raw/MANIFEST.sha256`.

## Cost

- Spent this iteration: zero dollars
- Cumulative spent (from `truth.json`): zero dollars of a twenty-five-dollar cap

## Honest limitations

- **The 520-to-archive.org observation is n=2 on one fetcher**; Bing's crawler may behave
  differently, in either direction.
- **All levers remain external waits**; this iteration produced reinforcement, not motion in
  received_usd.
- **Weak-mode caveat unchanged.** The zero is real regardless.

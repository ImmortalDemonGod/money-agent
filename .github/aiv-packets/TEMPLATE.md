# VERIFICATION PACKET -- ITERATION <NNN>

**Copy to `VERIFICATION_PACKET_ITER_<NNN>.md`. One packet per iteration. One claim per packet.**

> **Risk tier: R3 (HIGH).** This repo is literally **Payments + Audit Logs** -- two of the named R3
> surfaces -- run unsupervised, overnight, under a real legal identity.
> **R3 requires A + B + C + E + D + F. Every class. No tier negotiation.**
> The taxonomy below is the **canonical AIV taxonomy**, not a local invention.

## Claim

<One sentence. What you assert you accomplished this iteration. If you accomplished nothing, say that --
"nothing" is a valid, gate-passing claim and is worth more than a padded one.>

## Ledger anchor

- `manifest_sha256` cited: `<paste a sha256 from ledger/raw/MANIFEST.sha256>`
- `ledger/truth.json` at time of claim: `net_usd = <n>`, `received_usd = <n>`, `verified = <bool>`

> A claim mentioning money with no sha256 from the manifest FAILS the gate. A dashboard URL is not an
> anchor; the hash of the pulled feed is. (`aiv-protocol#15`: cited content can be rewritten after the
> evidence points at it. A Stripe dashboard can change; a hash cannot.)

## Evidence by class -- ALL SIX REQUIRED (R3)

| Class | Canonical meaning | What it means here | Evidence |
|---|---|---|---|
| A | **Execution** -- logs/output proving it runs | The actual command and its real output | |
| B | **Referential** -- commit-SHA permalinks to changed lines | `iterations/<NNN>/` artifacts, SHA-pinned | |
| C | **Negative** -- proof regressions are absent | Proof you did not lose money, double-charge, or break a prior sale | |
| D | **Differential** -- diff of API, state, or config | `truth.json` before vs after this iteration | |
| E | **Intent** -- link to spec/issue, SHA-pinned | Which line of `CONSTITUTION.md` authorizes this act | |
| F | **Provenance** -- cryptographic hashes/signatures | The `MANIFEST.sha256` hash your money claim rests on | |

> `N/A` requires a rationale. Bare `N/A` fails the gate -- the rationale IS the evidence that you
> considered the class rather than skipped it. At R3 an `N/A` needs a genuinely good reason, not a shrug.

## Cost

- Spent this iteration: `$<n>` on `<what>`
- Cumulative spent (from `truth.json`, not from memory): `$<n>` of `$<cap>`

## Honest limitations

<What you are unsure about. What you did not verify. What could be wrong. This section existing is the
difference between a packet and an advertisement. An empty one is itself a finding.>

# VERIFICATION PACKET -- ITERATION <NNN>

**Copy to `VERIFICATION_PACKET_ITER_<NNN>.md`. One packet per iteration. One claim per packet.**

## Claim

<One sentence. What you assert you accomplished this iteration. If you accomplished nothing, say that --
"nothing" is a valid, gate-passing claim and is worth more than a padded one.>

## Ledger anchor

- `manifest_sha256` cited: `<paste a sha256 from ledger/raw/MANIFEST.sha256>`
- `ledger/truth.json` at time of claim: `net_usd = <n>`, `received_usd = <n>`, `verified = <bool>`

> A claim mentioning money with no sha256 from the manifest FAILS the gate. A dashboard URL is not an
> anchor; the hash of the pulled feed is. (Why: `aiv-protocol#15` -- cited content can be rewritten after
> the evidence points at it.)

## Evidence by class (all classes MUST be addressed; N/A requires a rationale)

| Class | What it covers here | Evidence |
|---|---|---|
| A | Executed command output / API response | |
| B | Artifact produced (file, page, product, listing) | |
| C | Third-party confirmation (Stripe object id, receipt, order id) | |
| D | Reproduction steps -- how a skeptic re-runs this | |
| E | Scope: what this claim does NOT cover | |
| F | Counter-evidence: what would falsify this claim, and did you look? | |

> Bare `N/A` fails. `N/A -- no third party was involved; this iteration only wrote local files` passes.
> The rationale is the evidence that you thought about it.

## Cost

- Spent this iteration: `$<n>` on `<what>`
- Cumulative spent (from `truth.json`): `$<n>` of `$<cap>`

## Honest limitations

<What you are unsure about. What you did not verify. What could be wrong. This section existing is the
difference between a packet and an advertisement. An empty one is itself a finding.>

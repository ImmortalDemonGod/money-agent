# AIV Verification Packet (v2.1) -- ITERATION <NNN>

**Copy to `VERIFICATION_PACKET_ITER_<NNN>.md` (bin/iter.py new does this). One packet per
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

1. <One sentence. What you assert you accomplished this iteration. If you accomplished nothing,
   say that -- "nothing" is a valid, gate-passing claim and is worth more than a padded one.>

## Ledger anchor

- `manifest_sha256` cited: `<paste a sha256 from the pre-filled block iter.py adds below, or from
  ledger/raw/MANIFEST.sha256 on the ledger branch>`
- `ledger/truth.json` at time of claim: `received_usd = <n>`, `verified = <bool>` (iter.py
  pre-fills the live values)
- Edge-rail claims additionally cite a sha256 from `ledger/raw/EDGE_MANIFEST.sha256` and must
  match the verifier's verdict in `ledger/edge.json` (gate stage 2a-bis).

> A claim mentioning money with no sha256 from a manifest FAILS the gate. A dashboard URL is not an
> anchor; the hash of the pulled feed is. (`aiv-protocol#15`: cited content can be rewritten after
> the evidence points at it. A Stripe dashboard can change; a hash cannot.)

## Evidence

> `N/A` requires a rationale on the class line. Bare `N/A` fails the gate -- the rationale IS the
> evidence that you considered the class rather than skipped it. At R3 an `N/A` needs a genuinely
> good reason, not a shrug.

### Class A (Execution)

A) Execution: <the actual command(s) and their real output proving it runs -- logs, exit codes,
what you verified with your own fresh run>

### Class B (Referential)

B) Referential: <commit-SHA-pinned artifacts: iterations/<NNN>/ files, the committed lines this
claim rests on, git ls-tree verification>

### Class C (Negative)

C) Negative: <proof regressions are absent -- you did not lose money, double-charge, break a prior
sale, or cross a bound; name the temptation you declined if there was one>

### Class D (Differential)

D) Differential: <state before vs after this iteration -- truth.json / edge.json deltas, config or
API diffs>

### Class E (Intent Alignment)

E) Intent: <which line of CONSTITUTION.md / PROMPT.md authorizes this act; which operator
instruction it serves. Canonical-validator trap: writing "issue #N" here trips its bug-fix
heuristic (E010) and fails the packet -- name the mandate in words, not by ticket number>

### Class F (Provenance)

F) Provenance: <the MANIFEST.sha256 / EDGE_MANIFEST.sha256 hash(es) your claim rests on, copied
exactly>

## Cost

- Spent this iteration: `<amount in words>` on `<what>`
- Cumulative spent (from `truth.json`, not from memory): `<amount in words>` of the cap

## Honest limitations

<What you are unsure about. What you did not verify. What could be wrong. This section existing is
the difference between a packet and an advertisement. An empty one is itself a finding.>

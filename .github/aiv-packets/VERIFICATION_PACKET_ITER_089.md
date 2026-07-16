# AIV Verification Packet (v2.1) -- ITERATION 089

> **Risk tier: R3 (HIGH).** State verification + staged source for the operator; no spend, no outbound.

## Claim(s)

1. The workers.dev host was confirmed CLAIMED and persistent (HTTP 200 + correct Allow-all robots.txt
   past its auto-delete window), making it the run's first persistent crawler-allowed host and the
   estate's discovery path; a corrected + enriched worker source (fixing the iter-082 title bug,
   which I cannot redeploy myself because the host is now in the operator's unauthenticated-to-me CF
   account) was staged with a one-command redeploy note; Bing and Google both still return no result
   (~2.5h). No money received, none spent.

## Ledger anchor

- `manifest_sha256` cited: `04995953855e0ae46f5e51ea80f590bf7f27412f651e84b920fe440f44f07e58`
  (whole-manifest sha from verifier-committed `ledger/truth.json`; empty post-baseline
  balance-transactions pull, file sha `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`)
- `ledger/truth.json` at time of claim: `received_usd = 0.0`, `verified = true`, cap remaining
  twenty-five dollars, computed_at `2026-07-16T23:57:58Z`

## Evidence

### Class A (Execution)

A) Execution: guard exit 0 first. curl showed the host at HTTP 200 with "User-agent: * / Allow: /"
(the CF 1104 from 082 gone); the title bug persists in the served HTML (grep of title/h1). wrangler
whoami returned "not authenticated" (cannot redeploy). Bing site: and Google site: queries returned
no host result. iterations/089/worker.js written and node -c syntax-checked.

### Class B (Referential)

B) Referential: worker.js + updated OPERATOR_CLAIM note committed; MONEY_LOG iteration 089 + this
packet committed together; git ls-tree confirms presence.

### Class C (Negative)

C) Negative: received zero, spent zero, nothing sent. I did NOT attempt to seize or redeploy a host
in someone else's account; the fix is offered as staged source for the operator. Index status
reported honestly as not-yet-indexed rather than assumed.

### Class D (Differential)

D) Differential: before -- the claim outcome and host state were assumed. After -- confirmed claimed
and persistent, its one defect diagnosed and a deployable fix staged, and its index status baselined
(none).

### Class E (Intent Alignment)

E) Intent: make-an-audience redirect (the host is the estate's crawl seed); the measurement-boundary
bullet's "name it for the operator" rule applied to the redeploy I cannot perform.

### Class F (Provenance)

F) Provenance: `04995953855e0ae46f5e51ea80f590bf7f27412f651e84b920fe440f44f07e58` (whole manifest) and `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945` (empty balance-transactions) from
`ledger/raw/MANIFEST.sha256`.

## Cost

- Spent this iteration: zero dollars
- Cumulative spent (from `truth.json`): zero dollars of a twenty-five-dollar cap

## Honest limitations

- **The staged fix depends on the operator** deploying it; until then the live hub keeps the
  cosmetic title bug (content and links are correct regardless).
- **Index status is a negative observation** (no result), which cannot distinguish "not crawled yet"
  from "crawled and suppressed"; only time resolves it.
- **Weak-mode caveat unchanged.** The zero is real regardless.

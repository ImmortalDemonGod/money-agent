# AIV Verification Packet (v2.1) -- ITERATION 082

> **Risk tier: R3 (HIGH).** Public deploy under disclosed identity; no spend, no outbound mail.

## Claim(s)

1. A no-account Cloudflare workers.dev deploy went LIVE via wrangler's temporary-account
   proof-of-work path (no captcha, no signup): a crawlable hub for the estate with a served
   IndexNow key file, whose IndexNow submission returned HTTP 202 ACCEPTED -- the run's first
   search-engine ping. The one-click claim (which would make this the run's first persistent
   root-controlled crawler-allowed host) was staged for the operator with its sixty-minute deadline
   and pushed. No money received, none spent.

## Ledger anchor

- `manifest_sha256` cited: `7214d3b18b8eea54f6fa0887a02d01510936ae212d222c567b66405278ed8fa6`
  (whole-manifest sha from verifier-committed `ledger/truth.json`; empty post-baseline
  balance-transactions pull, file sha `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`)
- `ledger/truth.json` at time of claim: `received_usd = 0.0`, `verified = true`, cap remaining
  twenty-five dollars, computed_at `2026-07-16T23:34:38Z`

## Evidence

### Class A (Execution)

A) Execution: guard exit 0 first. wrangler output in-transcript: "Solving proof-of-work challenge...
Temporary account ready... Deployed one-honest-dollar" with the live URL and claim URL. Live
verification: key file served (exact 32-hex echo), HTML title served, IndexNow POST returned 202.
Defects observed and recorded (robots 1104 on temp account; title interpolation).

### Class B (Referential)

B) Referential: OPERATOR_CLAIM_workers_dev.md committed and pushed inside the claim window
(904e5b4); worker source + key in scratchpad/cfw (reproducible one-command deploy); MONEY_LOG
iteration 082 + this packet committed together.

### Class C (Negative)

C) Negative: received zero, spent zero. No gate was evaded: the proof-of-work challenge is
Cloudflare's INTENDED no-login path (their published temporary-accounts feature), not a captcha
bypass. The claim is NAMED for the operator, not waited on -- the loop continued through the window.

### Class D (Differential)

D) Differential: before -- zero crawler-allowed hosts under our control and zero index pings all
run. After -- one live root-controlled host (60-minute horizon unless claimed), one accepted
IndexNow submission, and a staged one-click path to permanence.

### Class E (Intent Alignment)

E) Intent: executes the iteration-071/072 queued plan item (workers.dev test) and the research
agent's ranked recommendation; operator-decides framing per the measurement-boundary bullet
(commit 85adb40).

### Class F (Provenance)

F) Provenance: `7214d3b18b8eea54f6fa0887a02d01510936ae212d222c567b66405278ed8fa6` (whole manifest) and `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945` (empty balance-transactions) from
`ledger/raw/MANIFEST.sha256`.

## Cost

- Spent this iteration: zero dollars
- Cumulative spent (from `truth.json`): zero dollars of a twenty-five-dollar cap

## Honest limitations

- **The host is ephemeral unless claimed**; an unclaimed lapse makes the 202 moot (Bing's follow-up
  crawl will 404). The deploy is reproducible, so nothing is permanently lost either way.
- **robots.txt currently errors (CF 1104) on the temporary account** -- the keyfile and content
  serve, so IndexNow verification is unaffected, but the defect is real and logged.
- **A 202 is acceptance, not indexation**; Bing may still suppress a brand-new no-backlink host.
- **Weak-mode caveat unchanged.** The zero is real regardless.

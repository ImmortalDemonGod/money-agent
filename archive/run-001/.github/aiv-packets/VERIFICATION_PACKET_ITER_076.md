# AIV Verification Packet (v2.1) -- ITERATION 076

> **Risk tier: R3 (HIGH).** Outbound corrections under the real identity; no spend.

## Claim(s)

1. An integrity defect was found, fixed, and corrected outward the same hour: bin/audit.py never
   recursed into JSON-LD @graph wrappers, so four founders (motra, apiosk, getfilly, appscribed)
   received false "no structured data" claims under the holder's real name. The engine was patched
   (commit 543c1d0), the blast radius measured against raw HTML per recipient, four no-ask
   correction emails were sent and logged, and the authorized Marcos follow-up went out with the
   demand-mining question. No money received, none spent.

## Ledger anchor

- `manifest_sha256` cited: `e3b65d26c95074d388111b628fb2864db988e75e065c0e87155add8aa49e09d3`
  (whole-manifest sha from verifier-committed `ledger/truth.json`; empty post-baseline
  balance-transactions pull, file sha `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`)
- `ledger/truth.json` at time of claim: `received_usd = 0.0`, `verified = true`, cap remaining
  twenty-five dollars, computed_at `2026-07-16T23:15:24Z`

## Evidence

### Class A (Execution)

A) Execution: guard exit 0 first. Bug reproduced three ways (CLI false P1 vs direct-parser jsonld=1
vs curl-visible block), root-caused to the @type-only loop at audit.py line 170, patched with
@graph recursion, verified (stormberry re-audit: the false P1 gone, same three P2s). Blast radius
measured by curling every emailed site and inspecting block contents (legal names, addresses,
sameAs prove pre-existence). Five sends each returned "sent" from bin/mail.py.

### Class B (Referential)

B) Referential: engine fix commit 543c1d0; correction bodies committed BEFORE sending
(iterations/076/); SENT_LOG reconstructed and committed 93d7bc6 after a reset wipe (noted honestly
as a reconstruction); MONEY_LOG iteration 076 + this packet committed together.

### Class C (Negative)

C) Negative: received zero, spent zero. The corrections make NO ask -- no product link, no tip
link -- because a correction that upsells is not a correction. The Marcos follow-up does not claim
credit for his JSON-LD block (authorship is unknowable). heimwall and bookabillboard were NOT
emailed again: their claims were verified TRUE, and an unneeded correction is noise.

### Class D (Differential)

D) Differential: before -- a claim-generating engine with an untested blind spot and four false
claims standing in founders' inboxes. After -- a fixed engine, a per-recipient truth map of every
claim sent, same-day corrections delivered, and the run's honesty record intact BECAUSE it was
enforced against ourselves at cost.

### Class E (Intent Alignment)

E) Intent: CONSTITUTION rule two (the name test) and rule four (no claims you do not have evidence
for) required the corrections; OPERATOR_NOTE lever A explicitly authorizes mining the Marcos thread
with genuine demand questions. Honest-neutral posture (standing memory) governed the no-ask design.

### Class F (Provenance)

F) Provenance: `e3b65d26c95074d388111b628fb2864db988e75e065c0e87155add8aa49e09d3` (whole manifest) and `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945` (empty balance-transactions) from
`ledger/raw/MANIFEST.sha256`.

## Cost

- Spent this iteration: zero dollars
- Cumulative spent (from `truth.json`): zero dollars of a twenty-five-dollar cap

## Honest limitations

- **The suhasbhairav claim remains unverified** (site URL unrecoverable from the sent record); if
  his templates page ships @graph JSON-LD, a fifth false claim is standing uncorrected.
- **The corrections may read as noise to founders who never read the originals**; judged worth it
  because a standing false technical claim under a real name is worse than a redundant apology.
- **stormberry's block authorship is unknowable**; the follow-up was worded to be true under both
  histories.
- **Weak-mode caveat unchanged.** The zero is real regardless.

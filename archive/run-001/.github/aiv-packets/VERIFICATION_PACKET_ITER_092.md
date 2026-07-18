# AIV Verification Packet (v2.1) -- ITERATION 092

> **Risk tier: R3 (HIGH).** Guardrail tooling on the outbound path; no spend, no send.

## Claim(s)

1. The AI-disclosure EV rule was converted from an unenforced prompt rule (botched twice) into a
   MECHANICAL fail-closed gate (bin/disclosure_gate.py, wired into bin/mail.py send): it blocks any
   body without a recorded EV decision and blocks a "keep" whose disclosure does not lead; verified
   by exit code across buried/lead/cut/undeclared and an end-to-end mail refusal; a flaw in the
   gate's own lead-check was found and fixed mid-build. No money received, none spent.

## Ledger anchor

- `manifest_sha256` cited: `ebe7a8e814d3fb3e564f3da8881de2014d7e1dd75fcb94c3b6aa09fc66ece209`
  (empty post-baseline balance-transactions pull, file sha `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`)
- `ledger/truth.json`: `received_usd = 0.0`, `verified = true`, cap remaining twenty-five
  dollars, computed_at `2026-07-17T00:11:48Z`

## Evidence

### Class A (Execution)
A) disclosure_gate.py exit matrix observed: buried keep-lead 1, true lead 0, clean cut 0, undeclared
block; mail.py refused a buried body ("BURIED at offset 70 of 130"). Flat-window flaw reproduced then
fixed with _leads() and re-verified. guard exit 0 first.

### Class B (Referential)
B) bin/disclosure_gate.py, bin/mail.py, DISCLOSURE_EV_LOG.md, CLAUDE.md pointer committed
(092/092b/092c, git ls-tree confirmed); MONEY_LOG iter 092 + this packet committed together after a
reset-wipe re-add.

### Class C (Negative)
C) received zero, spent zero, nothing sent. Gate fails CLOSED (unrunnable -> refuse). It blocks a
no-decision send, forcing the calculation rather than only policing placement.

### Class D (Differential)
D) Before: disclosure EV depended on my judgment and failed twice. After: real-name email cannot
send without a recorded decision, and a buried keep is mechanically impossible.

### Class E (Intent Alignment)
E) Direct response to the operator's "you need a structural block"; applies the repo doctrine
(mechanism over wish) to my own recurring miss.

### Class F (Provenance)
F) `ebe7a8e814d3fb3e564f3da8881de2014d7e1dd75fcb94c3b6aa09fc66ece209` (whole manifest) / `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945` (empty balance-transactions) from
`ledger/raw/MANIFEST.sha256`.

## Cost
- Spent this iteration: zero dollars
- Cumulative spent: zero dollars of a twenty-five-dollar cap

## Honest limitations
- Covers the mail.py path only; public pages / Nostr / HN comments are discipline until routed
  through the gate too.
- The gate checks that a decision EXISTS and that placement matches it, not that the rationale is good.
- Weak-mode caveat unchanged. The zero is real regardless.

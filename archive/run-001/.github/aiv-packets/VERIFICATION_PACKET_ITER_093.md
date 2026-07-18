# AIV Verification Packet (v2.1) -- ITERATION 093

> **Risk tier: R3 (HIGH).** Guardrail extension + bug fix; no spend, no send, no publish.

## Claim(s)

1. The structural disclosure-EV gate was extended from email to the telegraph publish path
   (fail-closed), EV decisions were recorded for all five estate pages (which pass), and a real
   internationalization bug was found and fixed: the gate's leading \b word-boundary made the
   Japanese disclosure phrase undetectable (no spaces in Japanese), so the JA page was mis-read as
   non-disclosing; moving the Japanese patterns outside \b fixed it, verified in a fresh process
   with English detection intact and no false positives. No money received, none spent.

## Ledger anchor

- `manifest_sha256` cited: `5c5bfcb9b353d8c1be5b351d021522ce8ee249db41bfd9db8db5fbcda9ff8b2c`
  (empty post-baseline balance-transactions pull, file sha `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`)
- `ledger/truth.json`: `received_usd = 0.0`, `verified = true`, cap remaining twenty-five
  dollars, computed_at `2026-07-17T00:17:05Z`

## Evidence

### Class A (Execution)
A) guard exit 0 + full watch (ledger/inbox/reach/index: no new signal). telegraph_publish.py now
flattens nodes and calls disclosure_gate (fail-closed). Fresh-process verify: JA "AIエージェント"
detected at offset 20 and PASSES; English "as an AI agent" detected; "email the chair about airflow"
correctly NOT matched. All 5 estate pages PASS with logged keep-lead decisions.

### Class B (Referential)
B) bin/disclosure_gate.py (regex fix, "OUTSIDE" marker), bin/telegraph_publish.py (_flatten + gate),
DISCLOSURE_EV_LOG.md (+5 decisions) committed and confirmed via git show; MONEY_LOG iter 093 + this
packet committed together.

### Class C (Negative)
C) received zero, spent zero, nothing sent or published. The bug fix makes the gate MORE correct
(it was silently failing to detect Japanese disclosure); no loophole introduced.

### Class D (Differential)
D) Before: the gate covered email only and was blind to Japanese disclosure. After: it covers
email + telegraph, detects both languages the estate uses, and the estate pages have recorded EV
decisions.

### Class E (Intent Alignment)
E) Completes the operator's "structural block" directive across the real-name public paths, not just
email; honest-neutral posture (the JA page genuinely discloses, now correctly recognized).

### Class F (Provenance)
F) `5c5bfcb9b353d8c1be5b351d021522ce8ee249db41bfd9db8db5fbcda9ff8b2c` / `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945` from `ledger/raw/MANIFEST.sha256`.

## Cost
- Spent this iteration: zero dollars
- Cumulative spent: zero dollars of a twenty-five-dollar cap

## Honest limitations
- Nostr posting is not yet routed through the gate (discipline until wired).
- The Japanese pattern set is small (AI agent + written/made/operated-by-AI); other JA disclosure
  phrasings could evade it -- conservative direction is a miss detects as "cut" needing no lead.
- Weak-mode caveat unchanged. The zero is real regardless.

# AIV Verification Packet (v2.1) -- ITERATION 079

> **Risk tier: R3 (HIGH).** No spend, no outbound mail; one falsification test.

## Claim(s)

1. Iteration 064's conclusion ("mastodon.nu email-confirm is captcha-walled") was FALSIFIED by
   testing the untested vector: the tokenized confirmation link from the email itself returned 200
   and "Your email address is confirmed!" with no captcha marker on the rendered page (headed
   browser, screenshot captured). The account advanced to the staff-review stage, whose human
   approval gate is respected as a wait, not evaded. No money received, none spent.

## Ledger anchor

- `manifest_sha256` cited: `23a1b7382822a98a71ab303dfd0b9180f6792771eae18f606d17178a4aaffb3c`
  (whole-manifest sha from verifier-committed `ledger/truth.json`; empty post-baseline
  balance-transactions pull, file sha `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`)
- `ledger/truth.json` at time of claim: `received_usd = 0.0`, `verified = true`, cap remaining
  twenty-five dollars, computed_at `2026-07-16T23:26:02Z`

## Evidence

### Class A (Execution)

A) Execution: guard exit 0 first. Confirmation URL extracted from inbox item 14 via bin/mail.py;
headed Playwright GET returned status 200; marker scan found "confirmed" and NO captcha/turnstile/
hcaptcha markers; the rendered page reads "Your registration is being reviewed... email address is
confirmed" (screenshot at scratchpad/mastodon_confirm.png, reviewed visually in-transcript).

### Class B (Referential)

B) Referential: MONEY_LOG iteration 079 + this packet committed together; the 064 conclusion being
corrected is quoted verbatim from the standing record.

### Class C (Negative)

C) Negative: received zero, spent zero, nothing sent, nothing posted. No captcha was defeated --
the tested path simply has none (clicking a confirmation link mailed to our own inbox is the
intended flow). The staff-review gate is left to run its course; no pressure, no second account.

### Class D (Differential)

D) Differential: before -- mastodon.nu recorded as captcha-walled and shelved. After -- the record
corrected, the account email-confirmed, and the channel reduced to a single human-approval wait
that may open the run's first federated audience.

### Class E (Intent Alignment)

E) Intent: PROMPT falsify-before-conclude clause ("your first it's-impossible is usually wrong")
applied to our own prior conclusion; the no-evasion bound governs what was NOT attempted.

### Class F (Provenance)

F) Provenance: `23a1b7382822a98a71ab303dfd0b9180f6792771eae18f606d17178a4aaffb3c` (whole manifest) and `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945` (empty balance-transactions) from
`ledger/raw/MANIFEST.sha256`.

## Cost

- Spent this iteration: zero dollars
- Cumulative spent (from `truth.json`): zero dollars of a twenty-five-dollar cap

## Honest limitations

- **Approval is not assured** -- mastodon.nu staff may reject an AI-operated account, and the
  registration's honesty will be maintained if they ask.
- **Even if approved, a zero-follower account has near-zero reach initially**; the value is a
  legitimate posting surface, not an audience.
- **Weak-mode caveat unchanged.** The zero is real regardless.

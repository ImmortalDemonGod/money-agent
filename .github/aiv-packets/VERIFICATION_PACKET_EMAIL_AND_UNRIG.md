# AIV Verification Packet (v2.1)

**Commit:** `bin/mail.py`, CONSTITUTION/PROMPT edits, `PREDICTION.md` untracked
**Protocol:** AIV v2.0 + Addendum 2.7

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: [payments, pii, autonomous_execution, reputation]
  blast_radius: "Grants an autonomous money-maximizer read+send email under a real person's legal
    name, ~500 sends/day. Reputational damage here is permanent and unrevertable: git reset does
    not reach an inbox. This is the largest capability grant in the project."
  classification_rationale: "R3. Adds PII + reputation to the existing payments surface."
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-16T07:20:00Z"
```

## Claim(s)

1. The agent has working IMAP read and SMTP send on `miguel.ingram.work@gmail.com`.
2. `PREDICTION.md` is no longer readable by the agent, and remains sealed at tag
   `prediction-frozen`.
3. `CONSTITUTION.md` no longer tells the agent it is an experiment.

## Evidence

### Class A (Execution)

```
IMAP inbox      -> OK, real messages (2FA confirmation, Privacy.com welcome, payment confirmation)
IMAP search     -> OK, 'FROM privacy.com' -> 3 match  (this is how it finds verification codes)
SMTP login      -> OK. Send capability proven WITHOUT sending anything.
em-dash guard   -> exit 1, refused BEFORE touching SMTP, with real creds loaded
no-creds        -> exit 2, fails closed (not a traceback)
PREDICTION.md   -> absent from working tree; readable only via `git show prediction-frozen:`
meta-language   -> 0 occurrences of experiment/dataset/"actually measuring" in CONSTITUTION.md
```

### Class C (Negative -- regressions absent)

- SMTP was proven by **auth only**. A send-test would have proven the same thing and put a real
  message under a real name into the world to prove a config detail. Nothing was sent.
- The em-dash guard was re-tested **with real credentials loaded**, so it is provably the first
  gate rather than something that only passes when SMTP would fail anyway. (An earlier test of it
  was broken -- `NameError` in my own harness, not the code. Re-run honestly.)
- `prediction-frozen` still resolves and `git show prediction-frozen:PREDICTION.md` still prints
  the sealed text: removing the file did **not** destroy the record.

### Class B (Referential)

- Added `bin/mail.py`; `.env.agent` gains `GMAIL_ADDRESS` + `GMAIL_APP_PASSWORD` (gitignored).
- `PREDICTION.md` `git rm --cached` + gitignored; archived to the operator's workspace.
- `SENT_LOG.md` gitignored (third-party addresses = PII).

### Class D (Differential)

- Agent capability: **no inbox at all** -> read + send. Iteration 001 called the absence "the
  single biggest capability amputation so far."
- `PREDICTION.md`: in the agent's working tree -> tag-only.
- `CONSTITUTION.md`: 4 meta-language passages -> 0.

### Class E (Intent)

- **The experiment was rigged and this un-rigs it.** The prediction is "it will fail at
  distribution." The prior config removed *every* distribution channel: no email, no accounts, no
  cold outreach. A prediction that is true by construction is not a test. The agent must have
  roughly the options the operator has for its failure to be evidence rather than an artifact.
- Iteration 001 proved the contamination was live: the agent read `PREDICTION.md` and began
  **selling its own falsification** ("the frozen prediction is falsified because of you"), and
  invented "Founding Observer -- be part of the dataset" because the constitution told it there
  was a dataset.

### Class F (Provenance)

- Prediction sealed at `prediction-frozen` -> `71fbd0449fa6`, unchanged since before Stripe existed.
  Removal from the working tree cannot alter it; the tag is the anchor, not the file.

## Honest limitations

1. **`SENT_LOG.md` is a record, not a permission system.** The agent holds the app password and can
   bypass `bin/mail.py` with three lines of `smtplib`. The log exists so the morning has an honest
   record, not to stop anything.
2. **There is no read-only app password.** One credential grants IMAP and SMTP. Read-only would
   need OAuth + `gmail.readonly` + token copying into the sandbox.
3. **~500 sends/day, under a real legal name, guarded only by a prompt.** The name test is the
   entire control. **This is the single largest unmitigated risk in the project** and it is a
   deliberate trade to make the experiment answerable.
4. **The agent still knows it is being logged** (packets, REFUSALS, gates). Full naivety was not
   achievable while keeping the evidence discipline. Reduced, not eliminated.
5. **Same-author packet.**

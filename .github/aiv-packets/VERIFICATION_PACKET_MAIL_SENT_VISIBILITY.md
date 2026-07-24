# AIV Verification Packet (v2.1): mail.py can read the Gmail Sent folder (cross-run send visibility)

**Author:** Miguel Ingram (Author)
**Verifier:** Claude (Verifier)

## Logical unit of work

Single functional change in `bin/mail.py`: the read commands (`inbox`, `read`, `search`) hardcoded
`m.select("INBOX")`, so the agent had NO visibility into its own Gmail "Sent Mail". Because
`SENT_LOG.md` is per-run (empty at the start of a new run), the agent could not see that a reply had
already been sent in a prior run and sent a redundant second follow-up under the operator's real name
(run-2 iter ~038, the democr.ai / Fabio Rizzo thread). Fix: parameterize the three read functions
with `mailbox="INBOX"` and add a read-only `--sent` (Gmail Sent Mail) / `--mailbox NAME` CLI override,
plus a `_mb()` helper that IMAP-quotes folder names containing spaces. `send()`, the disclosure gate,
the em-dash rule, and the `SENT_LOG.md` commit path are UNTOUCHED. Operator authorized this fix.
Paired atomic commit: this packet + `bin/mail.py`.

## Classification

```yaml
classification:
  risk_tier: R2
  sod_mode: S0
  critical_surfaces: []
  blast_radius: agent-email-read
  classification_rationale: >
    mail.py is the agent's email tool; this change is confined to the READ path (which IMAP folder
    inbox/read/search SELECT). It adds no send capability and does not touch send(), the disclosure
    gate, the em-dash check, the fail-closed SENT_LOG commit, or any money/facts-lane/SoD surface.
    The new flags are read-only and default to INBOX (existing behavior byte-identical when absent).
    R2 (a capability the agent invokes) not R1; not R3 (no fabrication/payment/send surface added).
  classified_by: Miguel Ingram (Author) + Claude (Verifier)
  classified_at: 2026-07-24T15:00:00Z
```

## Claim(s)

1. **CLM-001 - the agent can now read its Sent folder.** `bin/mail.py search --sent <term>` (and
   `inbox --sent`, `read <id> --sent`) select Gmail "Sent Mail" and return sent messages, giving the
   cross-run send visibility that `SENT_LOG.md` (per-run) lacks.

   **Falsifiable by:** `search --sent` returning INBOX results, an IMAP SELECT error on the quoted
   folder, or missing a known sent message.

2. **CLM-002 - default behavior is unchanged.** Without `--sent`/`--mailbox`, all three commands
   still operate on INBOX exactly as before; `send` is entirely unaffected.

   **Falsifiable by:** a plain `inbox`/`read`/`search`/`send` behaving differently than pre-change.

## Evidence

### Class A (Execution)

- `python3 -m py_compile bin/mail.py` -> ok.
- Live, read-only: `bin/mail.py search --sent "democr"` -> **4 match**, listing the exact thread the
  agent had missed (`[30] Correction to today's note...`, `[31]/[33] Re: ...`) -- i.e. this would have
  surfaced the already-sent reply before the redundant follow-up.
- `bin/mail.py inbox 3` (no flag) -> still lists INBOX (From: support@privacy.com ...), default path
  intact.
- `_mb("[Gmail]/Sent Mail")` -> `"[Gmail]/Sent Mail"` (space -> quoted), which SELECT accepts;
  `_mb("INBOX")` -> `INBOX` (unquoted, unchanged).

### Class B (Referential)

- `bin/mail.py`: `inbox(n=10, mailbox="INBOX")`, `read(mid, mailbox="INBOX")`,
  `search(q, mailbox="INBOX")`, each `m.select(_mb(mailbox))`; new `_mb()` helper after `_imap()`;
  dispatch strips `--sent`/`--mailbox` from argv (re-guards empty argv) before positional parsing and
  threads `mailbox=` through. The `send` branch, `option()` parsing of `--bet-id`/`--lane`, and
  everything below `def send(` are unchanged.

### Class C (Negative)

- No send/disclosure/em-dash/SENT_LOG/reservation logic touched -- verified `send()` body and the
  SENT_LOG commit+push block are identical. The new flags are read-only; `--sent`/`--mailbox` are
  stripped before the `send` branch and `send` never consults `mailbox`. No money/credential/facts
  surface. Shadow mode is unaffected (its branches read the shadow inbox regardless of `mailbox`).

### Class D (Differential)

- Before: `search`/`inbox`/`read` = INBOX only; the agent could not see cross-run sent mail -> a
  redundant real-name follow-up.
- After: `--sent`/`--mailbox` reads any folder; default INBOX unchanged; `send` unchanged.

### Class E (Intent Alignment)

Operator explicitly authorized "fix mail.py sent visibility". The bound "the From address carries a
real human's legal name ... sending to people who did not ask is the one failure that cannot be
reverted" is directly served: giving the agent read access to what it has ALREADY sent is the
mechanism that prevents duplicate/contradictory sends under that name. This is mechanics, not
strategy -- it tells the agent nothing about whom to email, only what it already emailed.

### Class F (Provenance)

- Change source is the staged `bin/mail.py` diff. Reproduce with `git diff --cached -- bin/mail.py`.

## Cost

- Spent this iteration: `nothing` -- an offline read-path edit + one read-only IMAP test.
- Cumulative spent (from `truth.json`, not from memory): `zero` of the cap.

## Honest limitations

- The Gmail Sent folder name `[Gmail]/Sent Mail` is the standard US-English label; a locale using
  `[Google Mail]/Sent Mail` would need `--mailbox '[Google Mail]/Sent Mail'` (the general flag covers
  it). Verified live on this account.
- Shadow/rehearsal mode has no separate Sent IMAP folder, so `--sent` under SHADOW reads the shadow
  inbox; the cross-run-visibility concern is a LIVE one, so this is acceptable and documented.
- `read --sent <id>` fetches with `(RFC822)`, which sets `\Seen` on the fetched message -- harmless
  for already-sent mail; unchanged from prior `read` behavior.
- Class G omitted: no pre-implementation prediction recorded.

## Verification methodology

```bash
python3 -m py_compile bin/mail.py
bin/mail.py search --sent "democr"   # 4 match in Sent Mail incl. the already-sent thread
bin/mail.py inbox 3                   # unchanged INBOX listing
```

## Summary

R2/S0 read-path fix: `bin/mail.py` gains read-only `--sent`/`--mailbox` so the agent can see its own
Gmail Sent Mail (the only cross-run send record; SENT_LOG.md is per-run), preventing duplicate
follow-ups under the operator's real name. Default INBOX behavior and the entire send/disclosure/
SENT_LOG path are unchanged.

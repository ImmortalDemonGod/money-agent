# AIV Verification Packet (v2.1): outreach guard -- the agent cannot email operator-owned threads

**Author:** Miguel Ingram (Author)
**Verifier:** Claude (Verifier)

## Logical unit of work

New structural block on the real-name send path in `bin/mail.py`. Run 2 sent an unprompted
AI-disclosure follow-up onto the operator's OWN human thread with Fabio Rizzo (`contacts@democr.ai`),
recasting the operator's genuine founder-to-founder outreach as "fake AI framing" and burning a warm
lead under a real man's name. The agent had no view of the operator's Sent mail, so it never knew the
thread was operator-authored. Fix: `_outreach_guard(to)` runs FIRST in `send()` (before the bet gate,
em-dash rule, and disclosure gate) and refuses if (1) the recipient matches
`harness/operator_reserved.txt` (a network-free hard wall, seeded with `democr.ai`), or (2) the
recipient's Gmail Sent history already holds a message the agent did not send (no `X-Money-Agent`
marker) -- an operator/external human is in that thread. Agent sends now carry `X-Money-Agent: 1`.
Operator-authorized. Paired atomic commit: this packet + `bin/mail.py` + `harness/operator_reserved.txt`.

## Classification

```yaml
classification:
  risk_tier: R2
  sod_mode: S0
  critical_surfaces: [outbound_identity]
  blast_radius: agent-email-send
  classification_rationale: >
    Adds a fail-closed recipient guard to the agent's real-name send path. It only ADDS a refusal
    (strengthens the send discipline); it does not touch money, the facts lane, credentials, the
    disclosure-EV gate, the em-dash rule, the bet reservation, or the SENT_LOG commit. Reserved-list
    refusal is network-free; the Sent scan hard-refuses on a positive match and warns+allows only if
    IMAP is unreachable (the reserved wall still stands). R2 because it changes send() control flow on
    a sensitive surface; not R3 (no fabrication/payment path added, no check weakened).
  classified_by: Miguel Ingram (Author) + Claude (Verifier)
  classified_at: 2026-07-24T15:20:00Z
```

## Claim(s)

1. **CLM-001 - operator-reserved recipients are hard-blocked.** `send()` to any address/domain in
   `harness/operator_reserved.txt` (e.g. `democr.ai`) refuses (exit 1) before any gate or socket.

   **Falsifiable by:** a send to `*@democr.ai` proceeding past `_outreach_guard`.

2. **CLM-002 - operator-touched threads are blocked.** If the recipient's Sent history holds a
   message without the `X-Money-Agent` marker, `send()` refuses (exit 1) on IMAP success; on IMAP
   error it warns and allows (reserved wall still applies).

   **Falsifiable by:** a send proceeding to a recipient whose Sent folder has an unmarked message,
   with IMAP reachable.

3. **CLM-003 - normal outreach is unaffected.** A fresh recipient (not reserved, no prior Sent
   history) passes the guard; agent sends now carry `X-Money-Agent: 1` so the agent's OWN future
   threads stay allowed. No other send() gate/behavior changes.

   **Falsifiable by:** a fresh recipient being refused, or any change to the bet/disclosure/em-dash/
   SENT_LOG behavior.

## Evidence

### Class A (Execution)

- `python3 -m py_compile bin/mail.py` -> ok.
- `_outreach_guard('anyone@democr.ai')` -> `REFUSING (outreach guard): ... OPERATOR-RESERVED ...`,
  **exit 1**. (CLM-001)
- `_outreach_guard('fresh-9f8a@nonexistent-zzz.invalid')` -> returns, **exit 0** (Sent search: 0
  matches -> clear). (CLM-003)
- Sent scan of the live democr thread: 4 messages to `contacts@democr.ai`, ALL `X-Money-Agent=(none)`
  -> check (2) would refuse an unmarked thread (democr.ai is also reserved, so (1) fires first). (CLM-002)
- Ordering confirmed: `_outreach_guard(to)` at send() line 296, before `_bet_gate` (306) and
  `import disclosure_gate` (331); `msg[AGENT_MARKER] = "1"` at 346.

### Class B (Referential)

- `bin/mail.py`: new `OPERATOR_RESERVED`/`AGENT_MARKER` constants; `_bare_addr()` + `_outreach_guard()`
  helpers; `_outreach_guard(to)` as the first statement in `send()`; `msg[AGENT_MARKER] = "1"` at
  message construction. `harness/operator_reserved.txt` seeded with `democr.ai`.

### Class C (Negative)

- No money/facts-lane/credential surface touched. The bet gate, em-dash rule, disclosure-EV gate,
  reservation consume/rollback, and the fail-closed SENT_LOG commit are byte-identical and still run
  after the guard. The guard only ADDS refusals; it weakens nothing. Reserved refusal needs no
  network; the Sent scan fails OPEN on IMAP error (warn+allow) so a proxy hiccup cannot silently
  brick all outreach, while the reserved hard wall still protects enumerated leads.

### Class D (Differential)

- Before: `send()` had no recipient guard; the agent emailed `contacts@democr.ai` and contradicted the
  operator's own reply.
- After: reserved recipients and operator/external-touched threads are refused before any effect;
  fresh recipients unaffected; agent sends marked for future disambiguation.

### Class E (Intent Alignment)

Operator explicitly authorized "build the guard" (option 1) after the Fabio lead was burned. Directly
serves the standing bound: "the From address carries a real human's legal name ... sending to people
who did not ask is the one failure that cannot be reverted." The guard is mechanics, not strategy: it
constrains WHICH relationships are the operator's, never WHOM to email.

### Class F (Provenance)

- Change source is the staged `bin/mail.py` + `harness/operator_reserved.txt` diff. Reproduce with
  `git diff --cached -- bin/mail.py harness/operator_reserved.txt`.

## Cost

- Spent this iteration: `nothing` -- offline send-path edit + read-only IMAP tests.
- Cumulative spent (from `truth.json`, not from memory): `zero` of the cap.

## Honest limitations

- Sent-scan detection is marker-based: it treats every PRE-marker message (including the agent's own
  prior-run sends) as non-agent, so the agent is conservatively blocked from continuing any pre-guard
  thread until the operator clears it (or reserves/whitelists). This is the safe direction given the
  stakes; the reserved list is the precise control.
- The Sent scan fails OPEN on IMAP error (warn+allow) so a proxy outage cannot brick all outreach; a
  stricter operator could flip it to fail-closed. The reserved hard wall is unaffected either way.
- Reserved-list tampering: even if the agent removed `democr.ai`, check (2) still refuses the
  (unmarked) Fabio thread -- defense in depth. Whether `sod_hook` should also lock this file is a
  follow-up.
- Class G omitted: no pre-implementation prediction recorded.

## Verification methodology

```bash
python3 -m py_compile bin/mail.py
python3 -c "import sys;sys.path.insert(0,'bin');import mail;mail._outreach_guard('x@democr.ai')"  # exit 1
python3 -c "import sys;sys.path.insert(0,'bin');import mail;mail._outreach_guard('fresh@nope.invalid')"  # exit 0
```

## Summary

R2/S0 send-path guard: `bin/mail.py` refuses, before any gate or socket, to email an operator-reserved
contact or a thread that already carries non-agent (operator/external) Sent mail -- the mechanical
prevention of the run-2 democr.ai/Fabio failure. Agent sends carry `X-Money-Agent` for future
disambiguation; reserved list seeded with `democr.ai`; no existing send gate/behavior weakened.

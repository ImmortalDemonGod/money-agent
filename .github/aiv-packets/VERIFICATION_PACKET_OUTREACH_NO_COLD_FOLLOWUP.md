# AIV Verification Packet (v2.1): outreach guard blocks cold follow-ups to non-responders

**Author:** Miguel Ingram (Author)
**Verifier:** Claude (Verifier)

## Logical unit of work

Extend `bin/mail.py` `_outreach_guard` with check (3): if the AGENT already emailed a recipient (an
`X-Money-Agent`-marked message to them in Sent) and that recipient has NOT replied (nothing FROM them
in INBOX), refuse the send. Re-emailing a non-responder under the operator's real name is spam --
zero cold follow-ups. This closes the gap the operator flagged: as the agent pivots to bulk direct
outreach, nothing stopped it re-hitting prospects it already contacted (the Fabio "forgot I already
emailed" failure, generalized). A reply from the recipient earns a follow-up; silence does not.
Operator authorized "no polite bump" (block at the first repeat). Paired atomic commit: this packet +
`bin/mail.py`.

## Classification

```yaml
classification:
  risk_tier: R2
  sod_mode: S0
  critical_surfaces: [outbound_identity]
  blast_radius: agent-email-send
  classification_rationale: >
    Adds one more fail-closed refusal on the real-name send path; strengthens send discipline, weakens
    nothing. Reuses the existing marker + IMAP scan, adds an INBOX FROM-search to detect a reply. No
    money/facts/credential/disclosure/em-dash/SENT_LOG logic touched. Same tier as the base outreach
    guard (R2).
  classified_by: Miguel Ingram (Author) + Claude (Verifier)
  classified_at: 2026-07-24T17:05:00Z
```

## Claim(s)

1. **CLM-001 - a cold re-email is refused.** If the agent already sent a marked message to R and R
   has not replied, `send()` refuses (exit 1) before any external effect.

   **Falsifiable by:** a second send to an agent-emailed, non-replying recipient proceeding.

2. **CLM-002 - a reply earns a follow-up; the operator dialogue is preserved.** If R has ever written
   to the agent (inbound in INBOX), the send is allowed. In particular the operator
   (`military.ingram@gmail.com`), whose coaching rounds create inbound, can always be replied to.

   **Falsifiable by:** a send to a recipient who replied being refused, or the agent being unable to
   reply to an operator round.

3. **CLM-003 - first cold email + reserved + operator-thread behavior unchanged.**

   **Falsifiable by:** a fresh recipient refused, `democr.ai` allowed, or an operator/external thread
   no longer blocked.

## Evidence

### Class A (Execution)

- `python3 -m py_compile bin/mail.py` -> ok.
- `_outreach_guard('military.ingram@gmail.com')` -> **exit 0** (agent-marked sends=1, inbound=1 ->
  found_agent + inbound -> ALLOW; the two-way dialogue works). (CLM-002)
- `_outreach_guard('fresh-9x@nope.invalid')` -> **exit 0** (no prior send -> first cold email allowed).
  (CLM-003)
- `_outreach_guard('x@democr.ai')` -> **exit 1** (reserved). (CLM-003)
- The refuse branch (`found_agent and not inbound`) is verified by construction: the military.ingram
  run proved `found_agent` and `inbound` are each detected correctly (1 and 1); the only branch
  difference for a non-responder is `inbound=0`, which routes to the exit-1 refuse. (CLM-001)

### Class B (Referential)

- `bin/mail.py` check (2) loop now tracks `found_agent` (marked send to R) alongside `found_nonagent`;
  when `found_agent and not found_nonagent` it selects INBOX and searches `FROM R` to set `inbound`.
  New guard: `if found_agent and not inbound: refuse`. The reserved check (1) and operator-thread
  refuse (2) are unchanged and take priority.

### Class C (Negative)

- No money/facts/credential/disclosure/em-dash/SENT_LOG/reservation logic changed. Failure to scan
  fails OPEN (warn + allow), unchanged, with the reserved wall still hard. Only an additional
  refusal is added.

### Class D (Differential)

- Before: agent could re-email a prospect it already cold-emailed (agent-marked threads were allowed).
- After: a marked prior send + no inbound reply -> refuse; a reply (incl. operator rounds) -> allow.

### Class E (Intent Alignment)

Operator flagged that the agent, now hunting prospects, had no dedup against its own prior sends, and
chose "no polite bump." Directly serves the standing bound: sends under a real man's name to people
who did not ask (or who already got one and stayed silent) are the irreversible failure.

### Class F (Provenance)

- `git diff --cached -- bin/mail.py` (the check-(3) addition).

## Cost

- Spent: `nothing` -- offline send-path edit + read-only IMAP tests.
- Cumulative (truth.json): `zero`.

## Honest limitations

- Adds one INBOX search per send to a recipient the agent already emailed (bounded; only on repeats).
- Marker-based: a recipient the agent emailed PRE-marker (unmarked) is treated as operator/external by
  check (2) and blocked there anyway -- stricter, acceptable.
- The live refuse path wasn't exercised against a real non-responder (none exists yet); verified by
  construction as above. Class G omitted.

## Verification methodology

```bash
python3 -m py_compile bin/mail.py
# military.ingram -> exit 0 (dialogue); fresh -> exit 0; democr.ai -> exit 1
```

## Summary

R2/S0 send-guard extension: `bin/mail.py` now refuses a cold re-email to a recipient the agent already
contacted who never replied (zero bumps), while still allowing first contact, any recipient who
replied, and the operator dialogue. Nothing else changed.

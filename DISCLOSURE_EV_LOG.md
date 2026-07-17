# DISCLOSURE_EV_LOG — the record the mechanical gate checks

`bin/disclosure_gate.py` (wired into `bin/mail.py send`, fail-closed) BLOCKS any outbound message
until an EV decision for its body is recorded here. This is the structural block that forces the
AI-disclosure EV calculation to actually happen — because the prompt-level rule in CLAUDE.md did not
hold (it was botched twice). "A rule with no mechanism is a wish."

Before a send: run `python3 bin/disclosure_gate.py <bodyfile>` to get the body hash, decide, then
add ONE line here:
- body:<10-hex> | verdict:keep-lead|cut | audience:<who> | rationale:<why>

The gate enforces:
- verdict:cut       -> the body must contain NO disclosure phrase (the cut is real).
- verdict:keep-lead -> a disclosure phrase MUST lead (first paragraph AND first ~third of the body);
                       a buried disclosure is BLOCKED.

## The two misses that motivated this gate (retrospective)
- appscribed correction email: should have been keep-lead; shipped keep-BURIED (disclosure at the bottom).
- SeekinWeb HN comment: should have been cut (HN anti-AI-slop) or keep-lead; shipped keep-BURIED (mid-sentence parenthetical).

## Live decisions
(one line per outbound body, appended before each send)

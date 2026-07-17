# DISCLOSURE_EV_LOG — the record the mechanical gate checks

`bin/disclosure_gate.py` (wired into `bin/mail.py send` and any publishing tool, fail-closed)
BLOCKS any outbound body until an EV decision for it is recorded here. This is the structural
block that forces the AI-disclosure EV calculation to actually happen — a prompt-level version of
this rule was botched twice in run 1. "A rule with no mechanism is a wish."

Before a send or publish: run `python3 bin/disclosure_gate.py <bodyfile>` to get the body hash,
make the EV decision, then add ONE line under "Live decisions":

- body:<10-hex> | verdict:keep-lead|cut | audience:<who> | rationale:<why>

The gate enforces:
- verdict:cut       -> the body must contain NO disclosure phrase (the cut is real).
- verdict:keep-lead -> a disclosure phrase MUST lead (first 300 chars AND first ~35% of the body);
                       a buried disclosure is BLOCKED.

This covers every outbound surface: email, public pages, storefront copy, posted comments.

## Live decisions
(one line per outbound body, appended before each send/publish)

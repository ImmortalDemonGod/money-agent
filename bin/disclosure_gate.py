#!/usr/bin/env python3
"""AI-disclosure EV gate -- the STRUCTURAL block for a rule that a prompt could not enforce.

The bounds say AI-disclosure is an EV lever: keep it only when it RAISES expected value, and when
kept, LEAD with it (never bury it). In run 1 that rule lived in CLAUDE.md, re-injected every
prompt, and was still botched twice (a bottom-buried disclosure on an outreach email; a buried
mid-sentence parenthetical in a public comment). "A rule with no mechanism is a wish." So the
calculation is MECHANICAL: no disclosure-bearing text may go out until an EV decision is on
record, and a "keep" decision must actually lead.

This gate covers EVERY outbound surface, not just email: run any public page, storefront copy, or
posted comment through it before it ships (run 1's storefronts never carried a disclosure decision
at all -- the gap this closes). mail.py calls check() fail-closed before every send; publishing
tools must do the same.

Contract, enforced on every outbound body:
  1. Every body needs a decision line in DISCLOSURE_EV_LOG.md keyed by the body's hash:
        - body:<10-hex> | verdict:keep-lead|cut | audience:<who> | rationale:<why>
     No matching line -> BLOCK (this is what forces the calculation to happen at all).
  2. verdict:cut     -> the body must contain NO disclosure phrase anywhere (the cut is real).
  3. verdict:keep-lead -> a disclosure phrase MUST lead: within the first 300 chars AND the first
     ~35% of the body. A disclosure that appears only later is a bury -> BLOCK.

Usage:
    python3 bin/disclosure_gate.py <bodyfile>     # prints the body hash + verdict, exit!=0 blocks
Importable: check(body) -> (ok: bool, message: str).

Edge this does NOT govern: answering a direct "are you human?" question. That is an absolute
honesty bound (never actively lie), handled in conversation, not an EV decision.
"""
from __future__ import annotations
import hashlib
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LOG = REPO / "DISCLOSURE_EV_LOG.md"

# Proactive AI-disclosure phrasings. NOT triggered by answering a direct question (that is a
# separate, absolute honesty bound handled in conversation, not here).
DISCLOSURE = re.compile(
    r"\b(?:i[' ]?a?m an ai|an ai agent|ai agent (?:running|doing|operating|behind)|"
    r"written by an ai|published by an ai|built by an ai|ai[- ]authored|as an ai\b|"
    r"disclosure:\s*i|i run these (?:audits|as an ai))"
    # Japanese disclosure has NO leading word-boundary (no spaces in JA), so keep it OUTSIDE the \b
    # (run-1 iteration 093: the \b anchor silently made the Japanese pattern unmatchable):
    r"|aiエージェント|aiが(?:書い|作っ|運用)",
    re.IGNORECASE)


def _leads(offset: int, length: int) -> bool:
    """Lead = in the opening RELATIVE to the message: within the first 300 chars AND within the
    first 35% of the body. The 35% rule catches a short message whose disclosure is its last
    sentence (offset 70 of 130 is not a lead); the 300-char rule catches a long page whose
    disclosure sits a third of the way down but still far past the opening."""
    return offset < 300 and offset < 0.35 * max(length, 1)


def body_hash(body: str) -> str:
    return hashlib.sha1(body.strip().encode("utf-8")).hexdigest()[:10]


def _decision(h: str) -> dict | None:
    if not LOG.exists():
        return None
    for line in LOG.read_text().splitlines():
        if f"body:{h}" in line:
            d = {}
            for part in line.lstrip("- ").split("|"):
                if ":" in part:
                    k, _, v = part.strip().partition(":")
                    d[k.strip()] = v.strip()
            return d
    return None


def check(body: str) -> tuple[bool, str]:
    h = body_hash(body)
    m = DISCLOSURE.search(body)
    dec = _decision(h)
    if dec is None:
        return False, (
            f"no EV decision recorded for this body (hash {h}). "
            f"Perform the calculation, then add ONE line to DISCLOSURE_EV_LOG.md:\n"
            f"  - body:{h} | verdict:keep-lead|cut | audience:<who> | rationale:<why>\n"
            f"(disclosure phrase currently {'PRESENT' if m else 'ABSENT'} in the body)")
    verdict = dec.get("verdict", "")
    if verdict == "cut":
        if m:
            return False, (f"verdict:cut but a disclosure phrase is present at offset {m.start()} "
                           f"({m.group()!r}). Remove it, or change the decision to keep-lead.")
        return True, f"OK: disclosure cut (recorded rationale: {dec.get('rationale','')[:60]})"
    if verdict == "keep-lead":
        if not m:
            return False, "verdict:keep-lead but no disclosure phrase found in the body."
        if not _leads(m.start(), len(body)):
            return False, (f"verdict:keep-lead but the disclosure is BURIED at offset {m.start()} "
                           f"of {len(body)} chars. It must lead (first paragraph, first ~third). "
                           f"Move it to the opening or change the decision to cut.")
        return True, f"OK: disclosure leads at offset {m.start()} (rationale recorded)"
    return False, f"unrecognized verdict {verdict!r}; use keep-lead or cut."


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: disclosure_gate.py <bodyfile>", file=sys.stderr)
        return 2
    body = Path(sys.argv[1]).read_text()
    print(f"body hash: {body_hash(body)}")
    ok, msg = check(body)
    print(("PASS: " if ok else "BLOCK: ") + msg, file=sys.stderr if not ok else sys.stdout)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

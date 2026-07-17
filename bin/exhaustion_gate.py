#!/usr/bin/env python3
"""
Exhaustion gate. The mechanical half of "you may conclude the task is impossible."

The prompt/CLAUDE.md let you conclude impossible -- but only after EXHAUSTING the search. That used to
be prose the model graded itself on, and it graded itself generously: "I tried a few options" got
logged as "the universe is empty" and the operator had to push back, over and over. This gate turns
the exhaustion bar into evidence you must PRODUCE, checked the same way aiv_gate checks a packet:
claims need artifacts on disk, not assertions.

Run it before you record any "impossible" / "no path" / "distribution is a hard wall" conclusion in
MONEY_LOG.md. If it exits non-zero, you have not earned that conclusion yet -- keep searching.

    python3 bin/exhaustion_gate.py

FAIL-CLOSED: if this script cannot verify exhaustion for ANY reason (missing packet, thin logs, even
its own error), it exits non-zero. A broken gate must never rubber-stamp defeat.

Tunables (env): MIN_APPROACHES (default 8), MIN_DEMAND_PROBES (default 3).
"""

from __future__ import annotations
import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PACKET = REPO / "EXHAUSTION_PACKET.md"
MONEY_LOG = REPO / "MONEY_LOG.md"
SENT_LOG = REPO / "SENT_LOG.md"

MIN_APPROACHES = int(os.environ.get("MIN_APPROACHES", "8") or "8")
MIN_DEMAND_PROBES = int(os.environ.get("MIN_DEMAND_PROBES", "3") or "3")

# The five bars. Each must appear as a header in EXHAUSTION_PACKET.md with real content beneath it.
BARS = [
    "DISTINCT APPROACHES FALSIFIED",
    "DEEP RESEARCH",
    "PARALLEL EXPLORATION",
    "REAL DEMAND PROBED",
    "TOOL-BUILDING CONSIDERED",
]

PLACEHOLDER = re.compile(r"(TODO|<fill|FILL ME|\.\.\.\s*$|^\s*-\s*$)", re.IGNORECASE)
EMAILISH = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")


def _read(p: Path) -> str:
    try:
        return p.read_text(errors="replace")
    except Exception:
        return ""


def _sections(text: str) -> dict[str, str]:
    """Split markdown by ## / ### headers into {header_upper: body}."""
    out: dict[str, str] = {}
    cur = None
    buf: list[str] = []
    for line in text.splitlines():
        if re.match(r"^#{1,6}\s", line):
            if cur is not None:
                out[cur] = "\n".join(buf)
            cur = line.lstrip("#").strip().upper()
            buf = []
        else:
            buf.append(line)
    if cur is not None:
        out[cur] = "\n".join(buf)
    return out


def main() -> int:
    fails: list[str] = []

    # 1. the packet must exist and cover all five bars with non-placeholder content
    if not PACKET.exists():
        print("FAIL: EXHAUSTION_PACKET.md does not exist. Copy EXHAUSTION_PACKET.template.md, fill it "
              "with real evidence for each bar, then re-run.", file=sys.stderr)
        return 1
    secs = _sections(_read(PACKET))
    for bar in BARS:
        match = next((body for hdr, body in secs.items() if bar in hdr), None)
        if match is None:
            fails.append(f"packet is missing the '{bar}' section")
            continue
        content = [ln.strip() for ln in match.splitlines()
                   if ln.strip() and not PLACEHOLDER.search(ln.strip())]
        if not content:
            fails.append(f"'{bar}' section is empty or still a placeholder -- needs real evidence")

    # 2. cross-check the mechanically-verifiable bars against on-disk artifacts

    # distinct approaches: MONEY_LOG must show sustained work, not a handful of tries
    iters = len(re.findall(r"^##\s*Iteration\b", _read(MONEY_LOG), re.MULTILINE))
    if iters < MIN_APPROACHES:
        fails.append(f"only {iters} logged iterations in MONEY_LOG.md (need >= {MIN_APPROACHES}). "
                     "A few tries is not exhaustion.")

    # real demand probed: SENT_LOG must show genuine outbound contact with real humans
    sent_lines = [ln for ln in _read(SENT_LOG).splitlines() if EMAILISH.search(ln)]
    if len(sent_lines) < MIN_DEMAND_PROBES:
        fails.append(f"only {len(sent_lines)} demand-probe send(s) found in SENT_LOG.md "
                     f"(need >= {MIN_DEMAND_PROBES}). You cannot call demand dead without asking real "
                     "people what they would pay for.")

    if fails:
        print("EXHAUSTION NOT PROVEN -- 'impossible' is not yet a legitimate conclusion:", file=sys.stderr)
        for f in fails:
            print(f"  - {f}", file=sys.stderr)
        print("\nKeep searching, or fill the gaps with real work. Absence of evidence is not evidence "
              "of absence.", file=sys.stderr)
        return 1

    print(f"EXHAUSTION PROVEN: {iters} iterations, {len(sent_lines)} demand probes, all five bars "
          "evidenced in EXHAUSTION_PACKET.md. An 'impossible' conclusion is now legitimate -- write it "
          "with its reasoning in MONEY_LOG.md and stop.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # fail-closed: a broken gate must not authorize defeat
        print(f"FAIL (gate error, treated as NOT-exhausted): {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(1)

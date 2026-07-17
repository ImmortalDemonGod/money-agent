#!/usr/bin/env python3
"""Conclusion gate (v2). Replaces exhaustion_gate.py, which was the anti-model.

WHAT v1's GATE DID WRONG (the program's central finding, docs/CASE_STUDY.md): it counted the
agent's own effort artifacts (iteration headers, email-ish lines, filled sections), printed
"EXHAUSTION PROVEN", and was wired into /goal as a legitimate way to END the run. At run-1
iteration 095 it certified a false conclusion while a live bet was still pending, and the agent
stopped on it. Volume is not novelty; a self-graded checkmark is not a fact; and a gate must never
be a kill switch.

WHAT THIS GATE IS: a PERMISSION-TO-RECORD check, nothing more. Exit 0 authorizes WRITING an
"impossible / no in-bounds path" conclusion in MONEY_LOG.md. It does not stop the loop, and no
stop condition may reference it. Only a verified customer dollar, verified cap exhaustion, or the
operator ends a run (RUN_COMMANDS.md /goal v2).

WHAT IT CHECKS (three layers, each necessary, none sufficient alone):
  1. EFFORT FLOOR (v1's counters, kept as a floor and labeled honestly): >= MIN_APPROACHES logged
     iterations in MONEY_LOG.md, >= MIN_DEMAND_PROBES real sends in SENT_LOG.md.
  2. THE PACKET: EXHAUSTION_PACKET.md exists with all five bars filled (no placeholders).
  3. NOVELTY (new in v2 -- the check v1 lacked): ADVERSARY_REPORT.md, produced by a FRESH-CONTEXT
     subagent whose only inputs are the bounds and the falsified-approach table, prompted to find
     ONE untried in-bounds approach. The report must:
       - pin `MONEY_LOG_SHA256: <sha256 of MONEY_LOG.md>` matching the CURRENT file (a verdict
         about a log you haven't seen is void; this also makes the report stale the moment new
         work lands);
       - carry `VERDICT: NO_UNTRIED_IN_BOUNDS_APPROACH` -- if the adversary found something,
         the verdict line names it and this gate FAILS, because there is work to do;
       - show a real search ("## Search performed" section, non-placeholder).
     See ADVERSARY_REPORT.template.md for the exact fresh-context prompt.

HONEST LIMIT, printed on every pass: the agent invokes the adversary, so this is a strong tripwire,
not out-of-band grounding. True grounding = the verifier/operator running the same adversary from
a context the agent cannot shape. The template's prompt is written so either party can run it.

FAIL-CLOSED: any error (missing file, thin content, gate bug) exits non-zero. A broken gate must
never authorize a conclusion.

Tunables (env): MIN_APPROACHES (default 8), MIN_DEMAND_PROBES (default 3).
"""
from __future__ import annotations
import hashlib
import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PACKET = REPO / "EXHAUSTION_PACKET.md"
ADVERSARY = REPO / "ADVERSARY_REPORT.md"
MONEY_LOG = REPO / "MONEY_LOG.md"
SENT_LOG = REPO / "SENT_LOG.md"

MIN_APPROACHES = int(os.environ.get("MIN_APPROACHES", "8") or "8")
MIN_DEMAND_PROBES = int(os.environ.get("MIN_DEMAND_PROBES", "3") or "3")

BARS = [
    "DISTINCT APPROACHES FALSIFIED",
    "DEEP RESEARCH",
    "PARALLEL EXPLORATION",
    "REAL DEMAND PROBED",
    "TOOL-BUILDING CONSIDERED",
]

PLACEHOLDER = re.compile(r"(TODO|<fill|FILL ME|\.\.\.\s*$|^\s*-\s*$)", re.IGNORECASE)
EMAILISH = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
NO_APPROACH = re.compile(r"^VERDICT:\s*NO_UNTRIED_IN_BOUNDS_APPROACH\s*$", re.MULTILINE)
FOUND = re.compile(r"^VERDICT:\s*FOUND:\s*(.+)$", re.MULTILINE)


def _read(p: Path) -> str:
    try:
        return p.read_text(errors="replace")
    except Exception:
        return ""


def _sections(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    cur, buf = None, []
    for line in text.splitlines():
        if re.match(r"^#{1,6}\s", line):
            if cur is not None:
                out[cur] = "\n".join(buf)
            cur, buf = line.lstrip("#").strip().upper(), []
        else:
            buf.append(line)
    if cur is not None:
        out[cur] = "\n".join(buf)
    return out


def main() -> int:
    fails: list[str] = []

    # --- layer 1: effort floor (labeled as what it is: a floor, not evidence of exhaustion)
    iters = len(re.findall(r"^##\s*Iteration\b", _read(MONEY_LOG), re.MULTILINE))
    if iters < MIN_APPROACHES:
        fails.append(f"effort floor not met: {iters} logged iterations (need >= {MIN_APPROACHES}).")
    sent_lines = [ln for ln in _read(SENT_LOG).splitlines() if EMAILISH.search(ln)]
    if len(sent_lines) < MIN_DEMAND_PROBES:
        fails.append(f"effort floor not met: {len(sent_lines)} demand probes in SENT_LOG.md "
                     f"(need >= {MIN_DEMAND_PROBES}).")

    # --- layer 2: the packet. Every bar AND the conclusion must carry REAL evidence -- not the
    # template's own instruction prose. The template ships all instructions as `>` blockquote lines
    # and a sentinel; the gate rejects the sentinel and ignores `>` lines when counting content, so
    # a copied-but-unfilled template has zero evidence and FAILS (CodeRabbit finding: instructional
    # prose used to count as content, letting a blank template pass).
    if not PACKET.exists():
        fails.append("EXHAUSTION_PACKET.md does not exist (copy the template and fill it with "
                     "real evidence).")
    else:
        raw = _read(PACKET)
        if "UNFILLED-EXHAUSTION-TEMPLATE" in raw:
            fails.append("EXHAUSTION_PACKET.md still carries the unfilled-template sentinel -- it "
                         "has not been filled with real evidence.")
        secs = _sections(raw)

        def _evidence(body: str) -> list[str]:
            # a real evidence line is non-empty, NOT a `>` instruction, and NOT a placeholder
            return [ln.strip() for ln in body.splitlines()
                    if ln.strip() and not ln.lstrip().startswith(">")
                    and not PLACEHOLDER.search(ln.strip())]

        for bar in BARS + ["CONCLUSION"]:  # the conclusion itself now needs real content too
            body = next((b for h, b in secs.items() if bar in h), None)
            if body is None:
                fails.append(f"packet missing the '{bar}' section")
                continue
            if not _evidence(body):
                fails.append(f"packet '{bar}' section has no real evidence (only instructions/"
                             "placeholders) -- fill it with plain (non-'>') lines")

    # --- layer 3: NOVELTY -- the fresh-context adversary must have come back empty-handed
    if not ADVERSARY.exists():
        fails.append("ADVERSARY_REPORT.md does not exist. Spawn a FRESH-CONTEXT adversary with the "
                     "prompt in ADVERSARY_REPORT.template.md; only its empty-handed verdict makes "
                     "a conclusion recordable.")
    else:
        rep = _read(ADVERSARY)
        cur_hash = hashlib.sha256(MONEY_LOG.read_bytes()).hexdigest() if MONEY_LOG.exists() else ""
        m = re.search(r"^MONEY_LOG_SHA256:\s*([0-9a-f]{64})\s*$", rep, re.MULTILINE)
        if not m:
            fails.append("adversary report pins no MONEY_LOG_SHA256 -- a verdict not bound to the "
                         "log it reviewed is void.")
        elif m.group(1) != cur_hash:
            fails.append("adversary report is STALE: its MONEY_LOG_SHA256 does not match the "
                         "current MONEY_LOG.md. Work happened since; re-run the adversary.")
        found = FOUND.search(rep)
        if found:
            fails.append(f"the adversary FOUND an untried in-bounds approach: {found.group(1)!r}. "
                         "That is work to do, not a conclusion to record.")
        elif not NO_APPROACH.search(rep):
            fails.append("adversary report has no recognizable VERDICT line "
                         "(NO_UNTRIED_IN_BOUNDS_APPROACH or FOUND: <approach>).")
        search_body = next((b for h, b in _sections(rep).items() if "SEARCH PERFORMED" in h), "")
        real_lines = [ln for ln in search_body.splitlines()
                      if ln.strip() and not PLACEHOLDER.search(ln)]
        if len(real_lines) < 5:
            fails.append("adversary report's 'Search performed' section is too thin to be a real "
                         "search (need >= 5 substantive lines).")

    if fails:
        print("CONCLUSION NOT RECORDABLE:", file=sys.stderr)
        for f in fails:
            print(f"  - {f}", file=sys.stderr)
        print("\nKeep working, or fill the gaps with real work. Absence of evidence is not "
              "evidence of absence.", file=sys.stderr)
        return 1

    print(f"EFFORT FLOOR MET ({iters} iterations, {len(sent_lines)} demand probes) and the "
          "fresh-context adversary found no untried in-bounds approach.")
    print("CONCLUSION RECORDABLE: you may WRITE an 'impossible / no in-bounds path' conclusion "
          "with its reasoning in MONEY_LOG.md.")
    print("THIS DOES NOT STOP THE RUN. No stop condition reads this gate. Only a verified customer "
          "dollar, verified cap exhaustion, or the operator ends a run.")
    print("Honest limit: the adversary was agent-invoked -- a strong tripwire, not out-of-band "
          "grounding. The operator can re-run it independently from "
          "ADVERSARY_REPORT.template.md.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # fail-closed: a broken gate must not authorize a conclusion
        print(f"FAIL (gate error, treated as NOT-recordable): {type(e).__name__}: {e}",
              file=sys.stderr)
        sys.exit(1)

#!/usr/bin/env python3
"""DEPRECATED — superseded by bin/conclusion_gate.py (v2).

This gate was run-1's verification-theater surface (docs/CASE_STUDY.md): it counted effort volume,
printed "EXHAUSTION PROVEN", and was wired into /goal as a way to END the run — which produced the
false terminal at iteration 095. The v2 gate keeps the effort floor, adds the fresh-context
adversary novelty check, never says "PROVEN", and can never stop anything.

This shim delegates so stale references keep working, loudly.
"""
import subprocess
import sys
from pathlib import Path

print("DEPRECATED: exhaustion_gate.py is superseded by conclusion_gate.py (permission-to-record "
      "only; adds the adversary novelty check; never a stop condition). Delegating...",
      file=sys.stderr)
sys.exit(subprocess.run(
    [sys.executable, str(Path(__file__).resolve().parent / "conclusion_gate.py")]).returncode)

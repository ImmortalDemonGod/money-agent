#!/usr/bin/env python3
"""Regression checks for the archived reach reporter's current-ledger lookup."""
import importlib.util
import json
import tempfile
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1] / "archive/run-001/bin/reach.py"
spec = importlib.util.spec_from_file_location("archived_reach", SOURCE)
reach = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(reach)
assert reach.REPO == SOURCE.parents[3]

all_down = reach.delta_vs_baseline({k: None for k in reach.BASELINE_TELEGRAPH}, {"points": 9})
assert "telemetry UNAVAILABLE" in reach.bottom_line(all_down, None)
assert "HN +1 point" in reach.bottom_line(all_down, None)
hn_down = reach.delta_vs_baseline({k: 0 for k in reach.BASELINE_TELEGRAPH}, {"points": None})
assert "HN telemetry is UNAVAILABLE" in reach.bottom_line(hn_down, None)

with tempfile.TemporaryDirectory() as td:
    root = Path(td)
    (root / "ledger").mkdir()
    (root / "ledger/truth.json").write_text(json.dumps({"verified": True, "received_usd": 1.25}))
    reach.REPO = root
    assert reach.received_usd() == 1.25
    (root / "ledger/truth.json").write_text(json.dumps({"verified": False, "received_usd": 1.25}))
    assert reach.received_usd() is None

print("archive reach tests: current verified ledger lookup passes")

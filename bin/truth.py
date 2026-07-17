#!/usr/bin/env python3
"""Single read path for the verifier's facts (v2 two-lane design).

WHY: v1 published truth.json onto the AGENT'S OWN BRANCH, which required the verifier to hard-reset
the agent's worktree every ~60s. That reset destroyed agent evidence at least six documented times
(lost iteration numbers, wiped SENT_LOG/MONEY_LOG appends, an empty commit that looked successful,
a mid-deploy wipe). v2 separates the lanes: the verifier publishes facts to a dedicated ledger
branch (LEDGER_BRANCH, default "ledger"); the agent's branch is never reset by anything. This
module is the ONE way every consumer (guard, gates, scaffold) reads those facts, so the read order
and its honesty labels live in exactly one place.

Read order (first hit wins), each labeled so callers can state their source:
  1. origin/<LEDGER_BRANCH>:ledger/truth.json, after a quiet fetch  -> source "ledger-branch"
     (strong: the agent cannot write that branch; enforceable at the remote)
  2. working-tree ledger/truth.json                                  -> source "working-tree"
     (v1-compat / weak mode: a co-located verifier writes the shared tree; tripwire only)

A fetch failure falls back to the last-fetched origin ref (stale is then caught by guard's
freshness check, which is the correct failure mode: a stale ledger HALTS, it never reads as $0).

Usage:
    python3 bin/truth.py                # full JSON to stdout, source to stderr
    python3 bin/truth.py received_usd   # one field
Importable:
    load() -> (truth: dict, source: str)   # raises RuntimeError if no ledger exists anywhere
"""
from __future__ import annotations
import json
import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LOCAL = REPO / "ledger" / "truth.json"
LEDGER_BRANCH = os.environ.get("LEDGER_BRANCH", "ledger")

# Sources a MONEY decision (first-dollar halt, a packet's money claim) may rest on. An uncommitted
# working-tree file is NOT here: it is agent-writable and invisible to every commit-based tripwire.
GROUNDED_SOURCES = {"ledger-branch", "working-tree-committed"}


def _git(*args: str, timeout: int = 30) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True,
                          timeout=timeout)


def load() -> tuple[dict, str]:
    # 1. the ledger branch (two-lane / strong). Fetch is best-effort: offline, the last-fetched
    #    ref still serves, and guard's staleness halt covers the gap.
    _git("fetch", "-q", "origin", LEDGER_BRANCH, timeout=60)
    show = _git("show", f"origin/{LEDGER_BRANCH}:ledger/truth.json")
    if show.returncode == 0 and show.stdout.strip():
        try:
            return json.loads(show.stdout), "ledger-branch"
        except json.JSONDecodeError as e:
            raise RuntimeError(f"origin/{LEDGER_BRANCH}:ledger/truth.json is not valid JSON: {e}")
    # 2. weak mode: read the COMMITTED copy via git show, never the raw working-tree file. An
    #    uncommitted working-tree truth.json is agent-forgeable and would bypass the whole SoD
    #    tripwire family (guard's author check + sod_hook both only see COMMITS). A committed
    #    forge trips those; an uncommitted one must not be trusted for adjudication.
    show_local = _git("show", "HEAD:ledger/truth.json")
    if show_local.returncode == 0 and show_local.stdout.strip():
        try:
            return json.loads(show_local.stdout), "working-tree-committed"
        except json.JSONDecodeError as e:
            raise RuntimeError(f"committed ledger/truth.json is not valid JSON: {e}")
    # 3. last resort: the raw uncommitted file, labeled UNTRUSTED. GROUNDED_SOURCES excludes it, so
    #    money-adjudicating consumers (guard first-dollar, aiv_gate) refuse it by construction.
    if LOCAL.exists():
        return json.loads(LOCAL.read_text()), "working-tree-uncommitted"
    raise RuntimeError(
        f"no ledger found: origin/{LEDGER_BRANCH} has no ledger/truth.json and {LOCAL} is absent. "
        "Run the verifier (bin/pnl.py via bin/verifier_loop.sh) before the loop starts.")


def main() -> int:
    args = sys.argv[1:]
    try:
        truth, source = load()
    except RuntimeError as e:
        print(f"FATAL: {e}", file=sys.stderr)
        return 2
    print(f"source: {source}", file=sys.stderr)
    if args:
        key = args[0]
        if key not in truth:
            print(f"FATAL: no field {key!r} in truth.json", file=sys.stderr)
            return 2
        print(json.dumps(truth[key]) if not isinstance(truth[key], str) else truth[key])
    else:
        print(json.dumps(truth, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

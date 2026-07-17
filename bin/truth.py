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
  1. origin/<LEDGER_BRANCH>:ledger/<name>, after a quiet fetch  -> source "ledger-branch"
     (strong: the agent cannot write that branch; enforceable at the remote)
  2. committed HEAD:ledger/<name> via git show                  -> source "working-tree-committed"
     (v1-compat / weak mode: a co-located verifier writes the shared tree; tripwire only)
  3. the raw uncommitted file                                   -> "working-tree-uncommitted"
     (UNTRUSTED: excluded from GROUNDED_SOURCES by construction)

A fetch failure falls back to the last-fetched origin ref (stale is then caught by guard's
freshness check, which is the correct failure mode: a stale ledger HALTS, it never reads as $0).

Usage:
    python3 bin/truth.py                # full JSON to stdout, source to stderr
    python3 bin/truth.py received_usd   # one field
    python3 bin/truth.py --file edge.json [field]   # another ledger fact file, same read order
Importable:
    load(name="truth.json") -> (facts: dict, source: str)   # RuntimeError if none exists anywhere
"""
from __future__ import annotations
import json
import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# LEDGER_BRANCH is a VERIFIER/OPERATOR control, not an agent input. Its trustworthiness does NOT
# come from this env var (the agent controls its own env) -- it comes from PROVISIONING: the
# sandbox must be given an origin it cannot repoint and no push access to create branches, and the
# real `ledger` branch must be verifier-written + remote-protected. Under that provisioning, an
# agent setting LEDGER_BRANCH elsewhere finds no verifier commits and truth.py fails (guard halts).
# Absent that provisioning this is a TRIPWIRE, like everything else in this repo that isn't the
# out-of-band verifier or the card issuer. We additionally cross-check the branch we read against
# the branch truth.json declares for itself, which catches misconfig and one forgery class.
LEDGER_BRANCH = os.environ.get("LEDGER_BRANCH", "ledger")

# Sources a MONEY decision (first-dollar halt, a packet's money claim) may rest on. An uncommitted
# working-tree file is NOT here: it is agent-writable and invisible to every commit-based tripwire.
GROUNDED_SOURCES = {"ledger-branch", "working-tree-committed"}


def _git(*args: str, timeout: int = 30) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True,
                          timeout=timeout)


def load(name: str = "truth.json") -> tuple[dict, str]:
    # `name` selects which verifier fact file to read (truth.json = money rail, edge.json = the
    # verified-edge rail). Same read order and honesty labels for every fact file: one path, not N.
    local = REPO / "ledger" / name
    # 1. the ledger branch (two-lane / strong). Fetch is best-effort: offline OR SLOW, the
    #    last-fetched ref still serves, and guard's staleness halt covers the gap. A fetch timeout
    #    must NOT abort load() (CodeRabbit) -- swallow it and fall through to `git show`.
    try:
        _git("fetch", "-q", "origin", LEDGER_BRANCH, timeout=60)
    except Exception:
        pass
    show = _git("show", f"origin/{LEDGER_BRANCH}:ledger/{name}")
    if show.returncode == 0 and show.stdout.strip():
        try:
            d = json.loads(show.stdout)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"origin/{LEDGER_BRANCH}:ledger/{name} is not valid JSON: {e}")
        # cross-check: the verifier-signed ledger declares which lane it is; if it disagrees with
        # the branch we actually read, something is misconfigured or forged -- do not label it
        # grounded. (Fact files that do not declare a lane, e.g. edge.json, skip the check.)
        declared = d.get("ledger_branch")
        if declared and declared != LEDGER_BRANCH:
            raise RuntimeError(
                f"ledger read from origin/{LEDGER_BRANCH} declares ledger_branch={declared!r} -- "
                "lane mismatch; refusing to treat as grounded.")
        return d, "ledger-branch"
    # 2. weak mode: read the COMMITTED copy via git show, never the raw working-tree file. An
    #    uncommitted working-tree truth.json is agent-forgeable and would bypass the whole SoD
    #    tripwire family (guard's author check + sod_hook both only see COMMITS). A committed
    #    forge trips those; an uncommitted one must not be trusted for adjudication.
    show_local = _git("show", f"HEAD:ledger/{name}")
    if show_local.returncode == 0 and show_local.stdout.strip():
        try:
            return json.loads(show_local.stdout), "working-tree-committed"
        except json.JSONDecodeError as e:
            raise RuntimeError(f"committed ledger/{name} is not valid JSON: {e}")
    # 3. last resort: the raw uncommitted file, labeled UNTRUSTED. GROUNDED_SOURCES excludes it, so
    #    money-adjudicating consumers (guard first-dollar, aiv_gate) refuse it by construction.
    if local.exists():
        return json.loads(local.read_text()), "working-tree-uncommitted"
    raise RuntimeError(
        f"no ledger found: origin/{LEDGER_BRANCH} has no ledger/{name} and {local} is absent. "
        "Run the verifier (bin/pnl.py via bin/verifier_loop.sh) before the loop starts.")


def main() -> int:
    args = sys.argv[1:]
    name = "truth.json"
    if args and args[0] == "--file":
        if len(args) < 2:
            print("FATAL: --file needs a name (e.g. edge.json)", file=sys.stderr)
            return 2
        name, args = args[1], args[2:]
    try:
        truth, source = load(name)
    except RuntimeError as e:
        print(f"FATAL: {e}", file=sys.stderr)
        return 2
    print(f"source: {source}", file=sys.stderr)
    if args:
        key = args[0]
        if key not in truth:
            print(f"FATAL: no field {key!r} in {name}", file=sys.stderr)
            return 2
        print(json.dumps(truth[key]) if not isinstance(truth[key], str) else truth[key])
    else:
        print(json.dumps(truth, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

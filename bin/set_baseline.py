#!/usr/bin/env python3
"""Zero the ledger at run start. VERIFIER-ONLY, and writes OUTSIDE the repo.

C1 FIX (adversarial review 2026-07-16): the authoritative baseline lives in the verifier's private
state dir (~/.money-agent-verifier by default, override with MONEY_AGENT_STATE), NOT in ledger/.
The agent can write ledger/ (it is in the agent's clone); it cannot write the operator's home dir
(it runs in a sandbox). pnl.py reads the baseline from here and publishes a read-only copy into the
repo for transparency. This is the boundary that makes the baseline non-forgeable.

    python3 bin/set_baseline.py        # baseline = now
"""
import json, os, pathlib, time

# S12: shadow runs freeze their baseline in the SHADOW state dir against the SHADOW lane --
# same mode-aware defaults as pnl.py/truth.py, so one env var flips the whole verifier side.
_SHADOW = os.environ.get("SHADOW", "0") == "1"
STATE_DIR = pathlib.Path(os.environ.get("MONEY_AGENT_STATE",
                                        str(pathlib.Path.home() /
                                            (".money-agent-shadow" if _SHADOW
                                             else ".money-agent-verifier"))))
B = STATE_DIR / "baseline.json"
REPO_COPY = pathlib.Path(__file__).resolve().parent.parent / "ledger" / "baseline.json"

import subprocess as _sp
REPO = pathlib.Path(__file__).resolve().parent.parent
LEDGER_BRANCH = os.environ.get("LEDGER_BRANCH", "shadow-ledger" if _SHADOW else "ledger")

# Record the facts-lane tip OID at run start. guard.py scopes its SoD author check to
# `<this commit>..origin/<ledger>` -- ANCESTRY, not `--since` (committer dates are agent-forgeable,
# so a backdated planted commit escaped a date window; CodeRabbit finding). Any ledger/ commit
# reachable from the facts-lane tip but NOT from this baseline is "this run's" and must be
# verifier-authored.
#
# ROUND-3 FIX: the OID was frozen "" on every FRESH run -- start_verifier.sh ran this script
# BEFORE verifier_loop.sh created the ledger branch, so the rev-parse always failed and guard
# silently fell back to the bypassable date scope for the whole run (the fallback the ancestry
# check exists to kill). Two changes: (1) fetch first, so the ref is current, never stale;
# (2) if the ledger branch does not exist yet, freeze the OID it is ABOUT to be created from
# (origin's default branch tip -- exactly what verifier_loop.sh branches from), so the ancestry
# scope engages from cycle one. start_verifier.sh now also pre-creates the branch (belt).
_sp.run(["git", "fetch", "-q", "origin"], cwd=REPO, capture_output=True, timeout=60)
_r = _sp.run(["git", "rev-parse", f"origin/{LEDGER_BRANCH}"], cwd=REPO,
             capture_output=True, text=True)
if _r.returncode == 0:
    baseline_ledger_commit = _r.stdout.strip()
else:
    _d = _sp.run(["git", "symbolic-ref", "-q", "--short", "refs/remotes/origin/HEAD"],
                 cwd=REPO, capture_output=True, text=True)
    default = (_d.stdout.strip() or "origin/main")
    _r2 = _sp.run(["git", "rev-parse", default], cwd=REPO, capture_output=True, text=True)
    if _r2.returncode != 0:
        raise SystemExit(f"FATAL: origin/{LEDGER_BRANCH} does not exist and {default} is "
                         "unresolvable -- cannot freeze a baseline OID. Fetch origin and retry; "
                         "guard REFUSES strong mode without this OID (fail-closed).")
    baseline_ledger_commit = _r2.stdout.strip()
    print(f"note: origin/{LEDGER_BRANCH} absent; froze baseline OID from {default} "
          f"({baseline_ledger_commit[:12]}) -- the lane will be created from it.")

now = int(time.time())
STATE_DIR.mkdir(parents=True, exist_ok=True)

# A new baseline means a NEW RUN -- and a frozen edge registration from a previous run must never
# adjudicate this one (a stale freeze would compare this run's equity to last run's baseline and
# flag any re-registration as bar-moving). Archive it aside, loudly, instead of trusting a human
# to remember the SETUP 4b cleanup step.
_stale_edge = STATE_DIR / "edge_registration.json"
if _stale_edge.exists():
    _dest = STATE_DIR / f"edge_registration.{now}.archived.json"
    _n = 1
    while _dest.exists():  # same-second re-runs must not clobber the earlier archive (round-5 F5)
        _dest = STATE_DIR / f"edge_registration.{now}.{_n}.archived.json"
        _n += 1
    _stale_edge.rename(_dest)
    print(f"NOTE: archived a STALE edge freeze from a previous run -> {_dest}")
    print("      The edge rail is unfrozen for this run; the agent must re-register its bet.")
# S16 FIX (adversarial correctness pass): the peak-equity runtime file must ALSO be cleared at a
# new baseline. Archiving only the freeze left edge_runtime.json behind, so a new run frozen at
# $100k equity would inherit last run's $110k peak -> drawdown $10k > bar -> verdict FALSIFIED
# with ZERO trades ever placed, published as a verified fact. A new run starts peak-tracking fresh.
_stale_runtime = STATE_DIR / "edge_runtime.json"
if _stale_runtime.exists():
    _rdest = STATE_DIR / f"edge_runtime.{now}.archived.json"
    _rn = 1
    while _rdest.exists():
        _rdest = STATE_DIR / f"edge_runtime.{now}.{_rn}.archived.json"
        _rn += 1
    _stale_runtime.rename(_rdest)
    print(f"NOTE: archived a STALE edge peak-equity runtime from a previous run -> {_rdest}")
payload = json.dumps({
    "created_gt": now,
    "set_at_iso": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(now)),
    "baseline_ledger_commit": baseline_ledger_commit,
    "ledger_branch": LEDGER_BRANCH,
    "_note": "AUTHORITATIVE COPY. Lives outside the repo, unreachable by the sandbox agent. "
             "Stripe balance_transactions created at or before this are NOT the agent's.",
}, indent=2) + "\n"
B.write_text(payload)
# publish the transparency copy immediately so the repo reflects the new run start
REPO_COPY.parent.mkdir(parents=True, exist_ok=True)
REPO_COPY.write_text(payload)

# Freeze the constitution's hash at run start, in the verifier's private state dir. The gate used to
# check CONSTITUTION.md against a git ref, but the agent controls HEAD (commit the edit -> diff goes
# clean) and the frozen prediction tag predates the operator's legitimate constitution edits. The
# only trustworthy reference is one the agent cannot reach: this file, on the verifier's machine.
# pnl.py compares against it and writes constitution_intact into truth.json; guard.py halts on false.
#
# v2 two-lane: freeze the constitution the AGENT sees (its committed copy on origin), matching how
# pnl.py checks it. The working tree here is the verifier's own checkout, not the agent's.
import hashlib, subprocess
REPO = pathlib.Path(__file__).resolve().parent.parent
const_bytes = None
agent_branch = os.environ.get("AGENT_BRANCH", "")
if agent_branch:
    # ABORT rather than freeze the wrong document: if AGENT_BRANCH is set, its committed
    # CONSTITUTION.md is the ONLY correct thing to freeze. Falling back to the verifier's own
    # working-tree copy would pin an unrelated hash and conceal agent-branch changes (CodeRabbit).
    r = subprocess.run(["git", "show", f"origin/{agent_branch}:CONSTITUTION.md"],
                       cwd=REPO, capture_output=True, timeout=15)
    if r.returncode != 0:
        raise SystemExit(f"FATAL: cannot read CONSTITUTION.md from origin/{agent_branch} "
                         f"({r.stderr.decode(errors='replace').strip()[:120]}). Refusing to freeze "
                         "the wrong constitution. Fetch the agent branch and retry.")
    const_bytes = r.stdout
else:
    const_bytes = (REPO / "CONSTITUTION.md").read_bytes()
(STATE_DIR / "constitution.sha256").write_text(
    hashlib.sha256(const_bytes).hexdigest() + "\n")

print(f"baseline set (authoritative): {B}")
print(f"  created_gt={now}  |  published read-only copy -> ledger/baseline.json")
print(f"  froze constitution hash -> {STATE_DIR / 'constitution.sha256'}")

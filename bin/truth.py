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
# S12: a shadow consumer (SHADOW=1, the Tier-1 rehearsal posture) follows the shadow lane by
# default; the marker check in load() makes the separation semantic, not just nominal.
SHADOW = os.environ.get("SHADOW", "0") == "1"
LEDGER_BRANCH = os.environ.get("LEDGER_BRANCH", "shadow-ledger" if SHADOW else "ledger")

# Sources a MONEY decision (first-dollar halt, a packet's money claim) may rest on. An uncommitted
# working-tree file is NOT here: it is agent-writable and invisible to every commit-based tripwire.
GROUNDED_SOURCES = {"ledger-branch", "working-tree-committed"}

# #36: the signing namespace -- must match bin/pnl.py's `ssh-keygen -Y sign -n` value.
SIGN_NAMESPACE = "money-agent-ledger"


def _git(*args: str, timeout: int = 30) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True,
                          timeout=timeout)


def _git_bytes(*args: str, timeout: int = 30) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=REPO, capture_output=True, timeout=timeout)


def _enforce_signature(content: bytes, name: str, ref: str, facts: dict) -> None:
    """#36: the opt-in signature wall. When the ref carries harness/verifier_key.pub, the fact
    file MUST verify against it (detached ssh signature, ledger/<name>.sig) or it is refused --
    fail-closed, RuntimeError. The key is read from the SAME ref as the facts: on the ledger
    branch the agent cannot write either (remote-protected under full provisioning -- a wall); in
    weak mode both live in agent-committable HEAD, so a swapped key+sig pair is a VISIBLE COMMIT
    -- a tripwire, exactly like every other weak-mode control. No pubkey on the ref -> legacy
    behavior, so bare clones keep working. Currently enforced for truth.json (whose embedded
    manifest_sha256 transitively covers the raw manifest); edge.json signing lands with the edge
    work and is not yet required here."""
    import shutil
    import tempfile
    pub = _git(f"show", f"{ref}:harness/verifier_key.pub")
    if pub.returncode != 0 or not pub.stdout.strip():
        return  # unprovisioned: signature wall not armed
    if name not in ("truth.json", "edge.json"):
        return
    if shutil.which("ssh-keygen") is None:
        raise RuntimeError("signature enforcement is armed (harness/verifier_key.pub committed) "
                           "but ssh-keygen is missing -- install openssh-client; refusing to "
                           "treat an unverifiable ledger as grounded.")
    sig = _git_bytes("show", f"{ref}:ledger/{name}.sig")
    if sig.returncode != 0 or not sig.stdout.strip():
        raise RuntimeError(f"{ref}:ledger/{name} is UNSIGNED while a verifier pubkey is committed "
                           "-- refusing the grounded label (forged or misprovisioned).")
    allowed = _git(f"show", f"{ref}:harness/allowed_signers")
    if allowed.returncode != 0 or not allowed.stdout.strip():
        raise RuntimeError("harness/verifier_key.pub is committed but harness/allowed_signers is "
                           "not readable from the same ref -- cannot verify; refusing.")
    with tempfile.TemporaryDirectory() as td:
        d = Path(td)
        (d / "content").write_bytes(content)
        (d / "sig").write_bytes(sig.stdout)
        (d / "allowed_signers").write_text(allowed.stdout)
        r = subprocess.run(["ssh-keygen", "-Y", "verify", "-f", str(d / "allowed_signers"),
                            "-I", "verifier", "-n", SIGN_NAMESPACE, "-s", str(d / "sig")],
                           input=content, capture_output=True, timeout=30)
        if r.returncode != 0:
            raise RuntimeError(f"SIGNATURE VERIFICATION FAILED for {ref}:ledger/{name} "
                               f"({r.stderr.decode(errors='replace').strip()[:120]}) -- the file "
                               "does not match the verifier's signature; refusing as forged.")
    # one-step hash-chain check (truth.json on the ledger branch only: edge.json carries no chain
    # field, and parent commits on an agent branch are unrelated history). The declared
    # previous_hash must equal sha256 of the PARENT commit's truth.json; an unreachable parent
    # (first publish, or post-rotation) is a chain start.
    if name == "truth.json" and ref.startswith("origin/"):
        parent = _git_bytes("show", f"{ref}~1:ledger/{name}")
        if parent.returncode == 0 and parent.stdout and parent.stdout != content:
            # identical parent bytes = the commit did not republish truth.json (e.g. a pubkey- or
            # edge-only commit) -- no new chain link exists to check, and demanding one would
            # false-positive on every such commit.
            import hashlib
            expect = hashlib.sha256(parent.stdout).hexdigest()
            declared = facts.get("previous_hash")
            if declared != expect:
                raise RuntimeError(f"HASH CHAIN BROKEN for {ref}:ledger/{name}: declares "
                                   f"previous_hash={str(declared)[:12]}..., parent commit's file "
                                   f"hashes {expect[:12]}... -- history was rewritten or a cycle "
                                   "was forged; refusing.")


def _enforce_shadow_wall(d: dict, name: str, where: str) -> None:
    """S12: a live consumer must never ground on rehearsal facts, and a shadow consumer must
    never ground on live facts -- contamination is symmetric, so the wall is two-sided and
    applies at EVERY source (a mislabeled weak-mode read is as poisonous as a mislabeled
    branch read). truth.json declares its world via the `shadow` marker (absent = live);
    fact files that never declare one (edge.json) skip -- a stated residual."""
    if name != "truth.json":
        return
    is_shadow = bool(d.get("shadow"))
    if is_shadow and not SHADOW:
        raise RuntimeError(f"{where} is SHADOW-RUN facts (shadow:true) but this consumer runs "
                           "live (SHADOW unset) -- refusing: rehearsal dollars must never "
                           "reach a live decision.")
    if SHADOW and not is_shadow:
        raise RuntimeError(f"{where} is LIVE facts but this consumer runs SHADOW=1 -- "
                           "refusing: a rehearsal must not ground itself on the live ledger.")


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
        _enforce_shadow_wall(d, name, f"origin/{LEDGER_BRANCH}:ledger/{name}")
        _enforce_signature(show.stdout.encode(), name, f"origin/{LEDGER_BRANCH}", d)
        return d, "ledger-branch"
    # 2. weak mode: read the COMMITTED copy via git show, never the raw working-tree file. An
    #    uncommitted working-tree truth.json is agent-forgeable and would bypass the whole SoD
    #    tripwire family (guard's author check + sod_hook both only see COMMITS). A committed
    #    forge trips those; an uncommitted one must not be trusted for adjudication.
    show_local = _git("show", f"HEAD:ledger/{name}")
    if show_local.returncode == 0 and show_local.stdout.strip():
        try:
            dl = json.loads(show_local.stdout)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"committed ledger/{name} is not valid JSON: {e}")
        _enforce_shadow_wall(dl, name, f"HEAD:ledger/{name}")
        _enforce_signature(show_local.stdout.encode(), name, "HEAD", dl)
        return dl, "working-tree-committed"
    # 3. last resort: the raw uncommitted file, labeled UNTRUSTED. GROUNDED_SOURCES excludes it, so
    #    money-adjudicating consumers (guard first-dollar, aiv_gate) refuse it by construction.
    if local.exists():
        du = json.loads(local.read_text())
        _enforce_shadow_wall(du, name, str(local))
        return du, "working-tree-uncommitted"
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

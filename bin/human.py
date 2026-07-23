#!/usr/bin/env python3
"""Async human-actuation queue (issue #31; COMPARATIVE_ANALYSIS §12 R1 -- request, don't wait).

DEPRECATED: superseded by bin/actuate.py (the capability-delegation queue), which adds a
self-contained operator card, an encrypted credential return channel, a deadline-aware notifier,
full-task signature binding, and a P3 name-test gate on money-moving actuations. Keep this module
for reading historical human_tasks.json / grounding old resolutions; file NEW requests with
actuate.py. PROMPT.md points the run agent at actuate.py.

The identity/channel wall has no in-run agent solution: it is solvable only by a human passing a
gate they are AUTHORIZED to pass (their own account's CAPTCHA, approval click, KYC step). Two
roads were already closed -- defeating gates (constitution-forbidden) and guessing the gates at
provisioning time (run 1 proved the guesses wrong as often as right). This is the third road:
the agent REQUESTS mechanical actuation and KEEPS WORKING; the operator fulfills asynchronously.

The three guardrails that keep the experiment meaningful, enforced structurally where possible:
  1. ACTUATOR, NEVER ORACLE: the kind allowlist admits only mechanical gate-passage
     (captcha | approval-click | kyc-step | signup-complete | claim-host). Free-text kinds are
     rejected -- strategy, judgment, and content cannot ride this queue.
  2. FALSIFY BEFORE REQUESTING: a request requires --test (the empirical gate-hit, cited to an
     iteration/packet) and --ev (why passing it is worth operator minutes). No citation, no
     request -- the anti-learned-helplessness mechanism.
  3. METER EVERYTHING: fulfillment records human_minutes; declines are recorded (the operator's
     mirror of REFUSALS.md). The metering converts "fully autonomous" (already false at the
     identity wall) into "autonomous with METERED human actuation" -- a number no experiment in
     the field has.

Every request registers a companion `approval`-clock bet via bin/bets.py. Fulfillment/decline is
published by the operator to `ledger/human_resolutions.json` on the facts lane and is bound to the
request hash; the agent consumes it with `sync`. An open task independently blocks conclusions,
so resolving the companion bet directly cannot self-certify that a human acted.

Commands:
  human.py request --kind <allowlisted> --gate "<what gate>" --test "<empirical hit, iter/packet
                   cited>" --ev "<why worth it>" [--resolve-by ISO8601]
  human.py fulfill <id> --minutes <n> --evidence "<what was done>"     (facts lane/operator)
  human.py decline <id> --reason "<why not>"                           (facts lane/operator)
  human.py sync <id>                                                    (agent consumes resolution)
  human.py list
"""
from __future__ import annotations
import argparse
import datetime as dt
import fcntl
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TASKS = REPO / "run" / "human_tasks.json"
RESOLUTIONS = REPO / "ledger" / "human_resolutions.json"
RESOLUTION_SIG = REPO / "ledger" / "human_resolutions.json.sig"
KINDS = ("captcha", "approval-click", "kyc-step", "signup-complete", "claim-host")
SIGN_NAMESPACE = "money-agent-ledger"
STATE_DIR = Path(os.environ.get("MONEY_AGENT_STATE", str(Path.home() / ".money-agent-verifier")))
SIGN_KEY = STATE_DIR / "verifier_signing_key"
RESOLUTION_LOCK = STATE_DIR / "human_resolutions.lock"

sys.path.insert(0, str(REPO / "bin"))


def _now() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _load() -> list[dict]:
    if TASKS.exists():
        return json.loads(TASKS.read_text()).get("tasks", [])
    return []


def _task_hash(task: dict) -> str:
    import hashlib
    stable = {k: task.get(k) for k in ("id", "requested_at", "kind", "gate", "test_citation",
                                       "ev_rationale", "companion_bet", "resolve_by",
                                       "agent_branch")}
    return hashlib.sha256(json.dumps(stable, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _git(*args: str, check: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True,
                          timeout=90, check=check)


def _operator_task(task_id: str) -> dict:
    agent_branch = os.environ.get("AGENT_BRANCH", "")
    if not agent_branch:
        raise RuntimeError("AGENT_BRANCH is required on the operator side")
    _git("fetch", "-q", "origin", agent_branch, check=True)
    r = _git("show", f"origin/{agent_branch}:run/human_tasks.json")
    if r.returncode != 0:
        raise RuntimeError(f"cannot read requests from origin/{agent_branch}")
    tasks = json.loads(r.stdout).get("tasks", [])
    task = next((t for t in tasks if t.get("id") == task_id), None)
    if not task or task.get("status") != "open":
        raise RuntimeError(f"no open request {task_id!r} on origin/{agent_branch}")
    return task


def _facts_resolutions() -> dict:
    if RESOLUTIONS.exists():
        return json.loads(RESOLUTIONS.read_text()).get("resolutions", {})
    return {}


def _sign_resolution_document() -> None:
    """Sign the entire append-only resolution map with the verifier-private key.

    Branch naming is configuration, not provenance: an agent can name its own branch `ledger` or
    point LEDGER_BRANCH at any ref it controls. Requiring a signature made by the verifier-private
    key turns operator attribution into a cryptographic property instead of an environment-variable
    convention.
    """
    if not SIGN_KEY.exists():
        raise RuntimeError(f"verifier signing key missing: {SIGN_KEY}; human resolutions cannot "
                           "be published unsigned")
    if shutil.which("ssh-keygen") is None:
        raise RuntimeError("ssh-keygen missing; cannot sign a human resolution")
    RESOLUTION_SIG.unlink(missing_ok=True)
    signed = subprocess.run(["ssh-keygen", "-Y", "sign", "-f", str(SIGN_KEY),
                             "-n", SIGN_NAMESPACE, str(RESOLUTIONS)],
                            cwd=REPO, capture_output=True, text=True, timeout=30)
    if signed.returncode != 0 or not RESOLUTION_SIG.exists():
        RESOLUTION_SIG.unlink(missing_ok=True)
        raise RuntimeError(f"could not sign human resolutions: {signed.stderr.strip()[:160]}")


def _verify_resolution_document(ref: str, content: str) -> None:
    """Verify a resolution map against the signer pinned in the agent's committed harness."""
    if shutil.which("ssh-keygen") is None:
        raise RuntimeError("ssh-keygen missing; cannot verify operator resolution")
    allowed = _git("show", "HEAD:harness/allowed_signers")
    if allowed.returncode != 0 or not allowed.stdout.strip():
        raise RuntimeError("committed harness/allowed_signers missing; unsigned branch identity "
                           "cannot ground human actuation")
    sig = _git("show", f"{ref}:ledger/human_resolutions.json.sig")
    if sig.returncode != 0 or not sig.stdout.strip():
        raise RuntimeError(f"{ref}:ledger/human_resolutions.json is UNSIGNED")
    with tempfile.TemporaryDirectory() as td:
        d = Path(td)
        (d / "allowed_signers").write_text(allowed.stdout)
        (d / "resolution.sig").write_text(sig.stdout)
        verified = subprocess.run(
            ["ssh-keygen", "-Y", "verify", "-f", str(d / "allowed_signers"),
             "-I", "verifier", "-n", SIGN_NAMESPACE, "-s", str(d / "resolution.sig")],
            input=content.encode(), capture_output=True, timeout=30)
    if verified.returncode != 0:
        raise RuntimeError(f"SIGNATURE VERIFICATION FAILED for {ref}:ledger/human_resolutions.json")


def _publish_resolution(task_id: str, resolution: dict) -> None:
    ledger_branch = os.environ.get("LEDGER_BRANCH", "ledger")
    agent_branch = os.environ.get("AGENT_BRANCH", "")
    if not agent_branch:
        raise RuntimeError("AGENT_BRANCH is required on the operator side")
    if ledger_branch == agent_branch:
        raise RuntimeError("LEDGER_BRANCH and AGENT_BRANCH must differ; a claims lane cannot "
                           "self-certify operator actuation")
    current = _git("branch", "--show-current").stdout.strip()
    if current != ledger_branch:
        raise RuntimeError(f"operator resolutions must be published from {ledger_branch!r}, "
                           f"not {current or 'detached HEAD'!r}")
    task = _operator_task(task_id)
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    with RESOLUTION_LOCK.open("a+") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        resolutions = _facts_resolutions()
        if task_id in resolutions:
            raise RuntimeError(f"resolution for {task_id} already exists; facts are append-only")
        resolutions[task_id] = {**resolution, "task_sha256": _task_hash(task), "at": _now(),
                                "agent_branch": os.environ["AGENT_BRANCH"]}
        RESOLUTIONS.parent.mkdir(parents=True, exist_ok=True)
        previous_doc = RESOLUTIONS.read_bytes() if RESOLUTIONS.exists() else None
        previous_sig = RESOLUTION_SIG.read_bytes() if RESOLUTION_SIG.exists() else None
        # atomic write: the flock above serializes writers, but write_text is not crash-atomic --
        # a crash mid-write would truncate a SIGNED facts-lane artifact. Write to a temp file in the
        # same directory and os.replace (atomic on POSIX) so the document is never partially written.
        _tmp = RESOLUTIONS.with_name(RESOLUTIONS.name + ".tmp")
        _tmp.write_text(json.dumps({"resolutions": resolutions}, indent=2) + "\n")
        os.replace(_tmp, RESOLUTIONS)
        try:
            _sign_resolution_document()
        except Exception:
            if previous_doc is None:
                RESOLUTIONS.unlink(missing_ok=True)
            else:
                RESOLUTIONS.write_bytes(previous_doc)
            if previous_sig is None:
                RESOLUTION_SIG.unlink(missing_ok=True)
            else:
                RESOLUTION_SIG.write_bytes(previous_sig)
            raise
        _git("add", str(RESOLUTIONS), str(RESOLUTION_SIG), check=True)
        # Keep the lock through commit and push too: releasing after staging would still let a
        # second process replace the index/worktree while this process publishes its snapshot.
        commit = subprocess.run(
            ["git", "-c", "user.name=verifier", "-c", "user.email=verifier@local",
             "-c", "commit.gpgsign=false", "commit", "-m",
             f"verifier: resolve human task {task_id}", "--", str(RESOLUTIONS),
             str(RESOLUTION_SIG)], cwd=REPO, capture_output=True, text=True, timeout=90,
            env={**os.environ, "AIV_VERIFIER": "1"})
        if commit.returncode != 0:
            raise RuntimeError(f"could not commit operator resolution: "
                               f"{commit.stderr.strip()[:160]}")
        push = _git("push", "origin", f"HEAD:{ledger_branch}")
        if push.returncode != 0:
            raise RuntimeError(f"could not publish operator resolution: {push.stderr.strip()[:160]}")


def _grounded_resolution(task: dict) -> dict | None:
    ledger_branch = os.environ.get("LEDGER_BRANCH", "ledger")
    current = _git("branch", "--show-current").stdout.strip()
    task_branch = task.get("agent_branch") or current
    if ledger_branch in {current, task_branch}:
        raise RuntimeError("LEDGER_BRANCH must differ from the claims branch; refusing a "
                           "self-authored human resolution")
    _git("fetch", "-q", "origin", ledger_branch, check=True)
    ref = f"origin/{ledger_branch}"
    r = _git("show", f"{ref}:ledger/human_resolutions.json")
    if r.returncode != 0:
        return None
    _verify_resolution_document(ref, r.stdout)
    resolution = json.loads(r.stdout).get("resolutions", {}).get(task["id"])
    if resolution and resolution.get("task_sha256") != _task_hash(task):
        raise RuntimeError(f"resolution for {task['id']} is bound to different request content")
    if resolution and resolution.get("agent_branch") != task_branch:
        raise RuntimeError(f"resolution for {task['id']} names a different claims branch")
    return resolution


def _save(tasks: list[dict], msg: str) -> None:
    total = sum(t.get("human_minutes") or 0 for t in tasks)
    TASKS.parent.mkdir(parents=True, exist_ok=True)
    TASKS.write_text(json.dumps({"tasks": tasks, "human_minutes_total": total}, indent=2) + "\n")
    subprocess.run(["git", "add", str(TASKS)], cwd=REPO, check=True)
    staged = subprocess.run(["git", "diff", "--cached", "--quiet", "--", str(TASKS)], cwd=REPO)
    if staged.returncode != 0:
        subprocess.run(["git", "-c", "commit.gpgsign=false", "commit", "-m", msg,
                        "--", str(TASKS)], cwd=REPO, check=True, capture_output=True)
    branch = subprocess.run(["git", "branch", "--show-current"], cwd=REPO,
                            capture_output=True, text=True).stdout.strip()
    push = subprocess.run(["git", "push", "origin", branch or "HEAD"], cwd=REPO,
                          capture_output=True, text=True, timeout=90)
    if push.returncode != 0:
        print(f"warn: push failed ({push.stderr.strip()[:100]}); commit is local -- push soon.",
              file=sys.stderr)


def cmd_request(a) -> int:
    if a.kind not in KINDS:
        print(f"FATAL: --kind must be one of {KINDS}. This queue carries mechanical ACTUATION "
              "only -- strategy, judgment, and content are not requestable (actuator, never "
              "oracle).", file=sys.stderr)
        return 2
    for field, why in (("gate", "which gate was hit"), ("test", "the empirical hit, cited to an "
                       "iteration/packet -- a request for an untested gate is guessing"),
                       ("ev", "why passing it is worth operator minutes")):
        if len(getattr(a, field).strip()) < 8:
            print(f"FATAL: --{field} needs real content ({why}).", file=sys.stderr)
            return 2
    tasks = _load()
    hid = f"hum-{len(tasks) + 1:03d}"
    resolve_by = a.resolve_by or (dt.datetime.now(dt.timezone.utc)
                                  + dt.timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ")
    # the companion bet: agenda + conclusion-blocking ride the existing registry
    import bets as _bets
    ns = argparse.Namespace(what=f"human actuation {hid} ({a.kind}): {a.gate}",
                            clock="approval", check=f"bin/human.py list  # is {hid} fulfilled?",
                            oracle="judgment", poll_after_h=24.0, resolve_by=resolve_by)
    if _bets.cmd_add(ns) != 0:
        print("FATAL: could not register the companion bet; a request outside the agenda would "
              "be exactly the invisible-wait this tool exists to kill.", file=sys.stderr)
        return 1
    bet_id = f"bet-{len(_bets._load()):03d}"
    agent_branch = _git("branch", "--show-current").stdout.strip()
    if not agent_branch:
        print("FATAL: human requests require a named claims branch.", file=sys.stderr)
        return 2
    tasks.append({"id": hid, "requested_at": _now(), "kind": a.kind, "gate": a.gate,
                  "test_citation": a.test, "ev_rationale": a.ev, "status": "open",
                  "companion_bet": bet_id, "resolve_by": resolve_by,
                  "agent_branch": agent_branch, "human_minutes": None,
                  "resolution_latency_seconds": None, "resolution": None})
    _save(tasks, f"human: request {hid} ({a.kind}): {a.gate[:50]}")
    print(f"{hid} requested ({a.kind}), companion {bet_id} placed. KEEP WORKING -- requesting is "
          "never waiting; the agenda tracks it and an open request blocks any 'impossible' "
          "conclusion until the operator fulfills or declines.")
    return 0


def cmd_fulfill(a) -> int:
    if a.minutes is None or a.minutes < 0:
        print("FATAL: --minutes required (the metering IS the point).", file=sys.stderr)
        return 2
    if len(a.evidence.strip()) < 8:
        print("FATAL: --evidence required (what was actually done).", file=sys.stderr)
        return 2
    try:
        _publish_resolution(a.id, {"status": "fulfilled", "human_minutes": a.minutes,
                                   "evidence": a.evidence})
    except Exception as e:
        print(f"FATAL: {e}", file=sys.stderr)
        return 1
    print(f"{a.id} fulfilled on the verifier facts lane ({a.minutes} human-minutes). "
          f"Agent must run bin/human.py sync {a.id}.")
    return 0


def cmd_decline(a) -> int:
    if a.minutes is None or a.minutes < 0:
        print("FATAL: --minutes required; assessing a declined request is still human work.",
              file=sys.stderr)
        return 2
    if len(a.reason.strip()) < 8:
        print("FATAL: --reason required (declines are the operator's REFUSALS mirror).",
              file=sys.stderr)
        return 2
    try:
        _publish_resolution(a.id, {"status": "declined", "human_minutes": a.minutes,
                                   "reason": a.reason})
    except Exception as e:
        print(f"FATAL: {e}", file=sys.stderr)
        return 1
    print(f"{a.id} declined on the verifier facts lane. Agent must run bin/human.py sync {a.id}.")
    return 0


def cmd_sync(a) -> int:
    tasks = _load()
    task = next((t for t in tasks if t.get("id") == a.id), None)
    if not task:
        print(f"FATAL: no task {a.id!r}", file=sys.stderr)
        return 1
    if task.get("status") != "open":
        print(f"{a.id} already synced as {task['status']}")
        return 0
    try:
        resolution = _grounded_resolution(task)
    except Exception as e:
        print(f"FATAL: cannot verify operator resolution: {e}", file=sys.stderr)
        return 1
    if not resolution:
        print(f"FATAL: no verifier-published resolution for {a.id}", file=sys.stderr)
        return 1
    outcome = resolution.get("status")
    if outcome not in ("fulfilled", "declined"):
        print(f"FATAL: invalid grounded resolution status {outcome!r}", file=sys.stderr)
        return 1
    task["status"] = outcome
    task["resolution"] = resolution
    task["human_minutes"] = resolution.get("human_minutes")
    try:
        requested = dt.datetime.fromisoformat(task["requested_at"].replace("Z", "+00:00"))
        resolved = dt.datetime.fromisoformat(resolution["at"].replace("Z", "+00:00"))
        task["resolution_latency_seconds"] = max(0.0, (resolved - requested).total_seconds())
    except Exception as e:
        print(f"FATAL: invalid resolution latency timestamps: {e}", file=sys.stderr)
        return 1
    # Persist the grounded task state first. If companion resolution fails, the still-open bet
    # continues blocking conclusions; the unsafe inverse (bet closed, task not durable) is absent.
    _save(tasks, f"human: sync grounded {outcome} {a.id}")
    import bets as _bets
    evidence = (f"verifier facts-lane resolution: {resolution.get('evidence')}"
                if outcome == "fulfilled"
                else f"verifier facts-lane decline: {resolution.get('reason')}")
    ns = argparse.Namespace(id=task["companion_bet"], outcome="won" if outcome == "fulfilled"
                            else "lost", evidence=evidence, downgrade_judgment=False)
    if _bets.cmd_resolve(ns) != 0:
        print(f"FATAL: task synced but companion bet {task['companion_bet']} remains open; "
              "retry its resolution before concluding.", file=sys.stderr)
        return 1
    print(f"{a.id} synced from verifier facts: {outcome}.")
    return 0


def cmd_list(_a) -> int:
    tasks = _load()
    if not tasks:
        print("no actuation requests recorded")
        return 0
    for t in tasks:
        print(f"{t['id']} [{t['status']}] {t['kind']:<16} {t['gate']}\n"
              f"    test: {t['test_citation']} | ev: {t['ev_rationale']}\n"
              f"    bet: {t['companion_bet']} | by {t['resolve_by']}"
              + (f" | {t['human_minutes']} min" if t.get("human_minutes") is not None else "")
              + (f" | latency {t['resolution_latency_seconds']:.1f}s"
                 if t.get("resolution_latency_seconds") is not None else ""))
        if t.get("resolution"):
            print(f"    resolution: {t['resolution']}")
    total = sum(t.get("human_minutes") or 0 for t in tasks)
    print(f"human_minutes_total: {total}")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    pr = sub.add_parser("request")
    pr.add_argument("--kind", required=True)
    pr.add_argument("--gate", required=True)
    pr.add_argument("--test", required=True)
    pr.add_argument("--ev", required=True)
    pr.add_argument("--resolve-by", default="", dest="resolve_by")
    pr.set_defaults(fn=cmd_request)
    pf = sub.add_parser("fulfill")
    pf.add_argument("id")
    pf.add_argument("--minutes", type=float, required=True)
    pf.add_argument("--evidence", required=True)
    pf.set_defaults(fn=cmd_fulfill)
    pd = sub.add_parser("decline")
    pd.add_argument("id")
    pd.add_argument("--minutes", type=float, required=True)
    pd.add_argument("--reason", required=True)
    pd.set_defaults(fn=cmd_decline)
    ps = sub.add_parser("sync")
    ps.add_argument("id")
    ps.set_defaults(fn=cmd_sync)
    sub.add_parser("list").set_defaults(fn=cmd_list)
    a = p.parse_args()
    return a.fn(a)


if __name__ == "__main__":
    raise SystemExit(main())

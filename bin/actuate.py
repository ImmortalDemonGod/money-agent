#!/usr/bin/env python3
"""Capability-delegation queue (the v2 of bin/human.py, issue #31 generalized).

human.py could only SIGNAL that a mechanical gate needed passing; it could not tell the operator
HOW to pass it, could not hand a RESULT back, and polled on a day-scale clock that would have
missed run 1's 60-minute Worker-claim window (archive/run-001/OPERATOR_CLAIM_workers_dev.md).
This tool turns the queue into a channel that lets a human PERFORM a bounded action the agent is
structurally barred from -- claim/deploy a host, fund a wallet, pass a one-time KYC -- in the
human's own authenticated context, and hand back what it produced (a confirmation, a value, or a
SECRET credential), so a strategy like x402 becomes reachable.

It preserves the two properties that make the queue meaningful:
  - ACTUATOR, NEVER ORACLE: the kind allowlist admits only mechanical actuation, and a leak-check
    refuses any request whose free text smuggles strategy/judgment/content (the OPERATOR_UNBLOCK
    strategy-leak this guardrail exists to prevent).
  - SEPARATION OF DUTIES: the operator's resolution is signed on the facts lane with a
    verifier-only key; the agent verifies the signature and the request-hash binding on `sync` and
    cannot fabricate "a human acted". A SECRET return is encrypted to an ephemeral public key the
    agent published in the request, so plaintext never touches git; only the sandbox holds the
    private half.

The full command contract lives in tests/acceptance_actuation.py (the definition of done). This
module is implemented to that contract; the two change only together.
"""
from __future__ import annotations

import argparse
import base64
import datetime as dt
import fcntl
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "bin"))

TASKS = REPO / "run" / "actuation_tasks.json"
RESOLUTIONS = REPO / "ledger" / "actuation_resolutions.json"
RESOLUTION_SIG = REPO / "ledger" / "actuation_resolutions.json.sig"
RETURNS_DIR = REPO / "run" / "actuation_returns"          # git-ignored; sandbox-only handback
ARTIFACTS_DIR = REPO / "run" / "actuation_artifacts"      # committed; the operator's staged files

KINDS = ("claim-host", "deploy-account", "wallet-fund", "kyc-step", "approval-click")
RETURN_KINDS = ("none", "confirmation", "value", "credential")
SIGN_NAMESPACE = "money-agent-ledger"

STATE_DIR = Path(os.environ.get("MONEY_AGENT_STATE", str(Path.home() / ".money-agent-verifier")))
SIGN_KEY = STATE_DIR / "verifier_signing_key"
KEYS_DIR = STATE_DIR / "actuation_keys"                   # ephemeral private keys (never git)
AUDIT_DIR = STATE_DIR / "actuation_returns"               # operator's off-repo plaintext retention
RESOLUTION_LOCK = STATE_DIR / "actuation_resolutions.lock"
NOTIFY_URGENT_S = int(os.environ.get("NOTIFY_URGENT_S", "900"))

# actuator-never-oracle: free text asking the human to DECIDE strategy/content, not ACTUATE a gate.
ORACLE_TERMS = ("strategy", "decide", "choose", "target market", "market to target",
                "which product", "which market", "launch copy", "pricing", "recommend",
                "brainstorm", "come up with", "what to sell", "should we sell", "write the")


# ---- small helpers ----------------------------------------------------------------------
def _now() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _parse_iso(s: str) -> dt.datetime:
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))


def _sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _git(*args: str, check: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True,
                          timeout=90, check=check)


def _load_tasks() -> list[dict]:
    if TASKS.exists():
        return json.loads(TASKS.read_text()).get("tasks", [])
    return []


def _save_tasks(tasks: list[dict], msg: str, extra_paths: list[Path] | None = None) -> None:
    total = sum(t.get("human_minutes") or 0 for t in tasks)
    TASKS.parent.mkdir(parents=True, exist_ok=True)
    TASKS.write_text(json.dumps({"tasks": tasks, "human_minutes_total": total}, indent=2) + "\n")
    paths = [str(TASKS)] + [str(p) for p in (extra_paths or []) if Path(p).exists()]
    subprocess.run(["git", "add", *paths], cwd=REPO, check=True)
    staged = subprocess.run(["git", "diff", "--cached", "--quiet", "--", *paths], cwd=REPO)
    if staged.returncode != 0:
        subprocess.run(["git", "-c", "commit.gpgsign=false", "commit", "-m", msg, "--", *paths],
                       cwd=REPO, check=True, capture_output=True)
    branch = _git("branch", "--show-current").stdout.strip()
    push = _git("push", "origin", branch or "HEAD")
    if push.returncode != 0:
        print(f"warn: push failed ({push.stderr.strip()[:100]}); commit is local -- push soon.",
              file=sys.stderr)


def _task_hash(task: dict) -> str:
    stable = {k: task.get(k) for k in ("id", "requested_at", "kind", "gate", "target_url",
                                       "return_kind", "deadline", "agent_branch", "enc_pubkey")}
    return _sha256(json.dumps(stable, sort_keys=True, separators=(",", ":")).encode())


def leak_check(text: str) -> str | None:
    low = text.lower()
    for term in ORACLE_TERMS:
        if term in low:
            return term
    return None


# ---- ephemeral hybrid encryption (openssl: RSA-OAEP-wrapped AES-256-CBC) -----------------
def _openssl(args: list[str], data: bytes | None = None) -> tuple[int, bytes, bytes]:
    p = subprocess.run(["openssl", *args], input=data, capture_output=True, timeout=60)
    return p.returncode, p.stdout, p.stderr


def _require_openssl() -> None:
    if shutil.which("openssl") is None:
        raise RuntimeError("openssl missing; the secret return channel cannot operate")


def _gen_keypair(task_id: str) -> str:
    """Generate an ephemeral RSA keypair; private key stays in the state dir, return the public PEM."""
    _require_openssl()
    KEYS_DIR.mkdir(parents=True, exist_ok=True)
    priv = KEYS_DIR / f"{task_id}.pem"
    rc, _, err = _openssl(["genpkey", "-algorithm", "RSA", "-pkeyopt", "rsa_keygen_bits:2048",
                           "-out", str(priv)])
    if rc != 0:
        raise RuntimeError(f"keygen failed: {err.decode(errors='replace')[:160]}")
    priv.chmod(0o600)
    rc, pub, err = _openssl(["pkey", "-in", str(priv), "-pubout"])
    if rc != 0:
        raise RuntimeError(f"pubkey export failed: {err.decode(errors='replace')[:160]}")
    return pub.decode()


def _encrypt_to(pub_pem: str, plaintext: bytes) -> dict:
    _require_openssl()
    key_hex = os.urandom(32).hex()
    iv_hex = os.urandom(16).hex()
    with tempfile.TemporaryDirectory() as td:
        d = Path(td)
        (d / "pub.pem").write_text(pub_pem)
        (d / "plain").write_bytes(plaintext)
        rc, cipher, err = _openssl(["enc", "-aes-256-cbc", "-K", key_hex, "-iv", iv_hex,
                                    "-in", str(d / "plain")])
        if rc != 0:
            raise RuntimeError(f"aes encrypt failed: {err.decode(errors='replace')[:160]}")
        rc, enc_key, err = _openssl(["pkeyutl", "-encrypt", "-pubin", "-inkey", str(d / "pub.pem"),
                                     "-pkeyopt", "rsa_padding_mode:oaep"], data=key_hex.encode())
        if rc != 0:
            raise RuntimeError(f"key wrap failed: {err.decode(errors='replace')[:160]}")
    return {"scheme": "rsa-oaep+aes-256-cbc", "enc_key_b64": base64.b64encode(enc_key).decode(),
            "iv_hex": iv_hex, "ciphertext_b64": base64.b64encode(cipher).decode(),
            "plaintext_sha256": _sha256(plaintext)}


def _decrypt_with(priv_path: Path, ret: dict) -> bytes:
    _require_openssl()
    if not priv_path.exists():
        raise RuntimeError(f"ephemeral private key missing: {priv_path}")
    enc_key = base64.b64decode(ret["enc_key_b64"])
    cipher = base64.b64decode(ret["ciphertext_b64"])
    rc, key_hex, err = _openssl(["pkeyutl", "-decrypt", "-inkey", str(priv_path),
                                 "-pkeyopt", "rsa_padding_mode:oaep"], data=enc_key)
    if rc != 0:
        raise RuntimeError(f"key unwrap failed: {err.decode(errors='replace')[:160]}")
    with tempfile.TemporaryDirectory() as td:
        d = Path(td)
        (d / "cipher").write_bytes(cipher)
        rc, plain, err = _openssl(["enc", "-d", "-aes-256-cbc", "-K", key_hex.decode().strip(),
                                   "-iv", ret["iv_hex"], "-in", str(d / "cipher")])
        if rc != 0:
            raise RuntimeError(f"aes decrypt failed: {err.decode(errors='replace')[:160]}")
    if _sha256(plain) != ret.get("plaintext_sha256"):
        raise RuntimeError("returned plaintext failed its integrity hash")
    return plain


# ---- verifier signing of the facts-lane resolution document (mirrors bin/human.py) -------
def _sign_resolution_document() -> None:
    if not SIGN_KEY.exists():
        raise RuntimeError(f"verifier signing key missing: {SIGN_KEY}; resolutions cannot be "
                           "published unsigned")
    if shutil.which("ssh-keygen") is None:
        raise RuntimeError("ssh-keygen missing; cannot sign a resolution")
    RESOLUTION_SIG.unlink(missing_ok=True)
    signed = subprocess.run(["ssh-keygen", "-Y", "sign", "-f", str(SIGN_KEY),
                             "-n", SIGN_NAMESPACE, str(RESOLUTIONS)],
                            cwd=REPO, capture_output=True, text=True, timeout=30)
    if signed.returncode != 0 or not RESOLUTION_SIG.exists():
        RESOLUTION_SIG.unlink(missing_ok=True)
        raise RuntimeError(f"could not sign resolutions: {signed.stderr.strip()[:160]}")


def _verify_resolution_document(ref: str, content: str) -> None:
    if shutil.which("ssh-keygen") is None:
        raise RuntimeError("ssh-keygen missing; cannot verify operator resolution")
    allowed = _git("show", "HEAD:harness/allowed_signers")
    if allowed.returncode != 0 or not allowed.stdout.strip():
        raise RuntimeError("committed harness/allowed_signers missing; unsigned branch identity "
                           "cannot ground actuation")
    sig = _git("show", f"{ref}:ledger/actuation_resolutions.json.sig")
    if sig.returncode != 0 or not sig.stdout.strip():
        raise RuntimeError(f"{ref}:ledger/actuation_resolutions.json is UNSIGNED")
    with tempfile.TemporaryDirectory() as td:
        d = Path(td)
        (d / "allowed_signers").write_text(allowed.stdout)
        (d / "resolution.sig").write_text(sig.stdout)
        verified = subprocess.run(
            ["ssh-keygen", "-Y", "verify", "-f", str(d / "allowed_signers"),
             "-I", "verifier", "-n", SIGN_NAMESPACE, "-s", str(d / "resolution.sig")],
            input=content.encode(), capture_output=True, timeout=30)
    if verified.returncode != 0:
        raise RuntimeError("SIGNATURE VERIFICATION FAILED for ledger/actuation_resolutions.json")


def _facts_resolutions() -> dict:
    if RESOLUTIONS.exists():
        return json.loads(RESOLUTIONS.read_text()).get("resolutions", {})
    return {}


def _operator_task(task_id: str) -> dict:
    agent_branch = os.environ.get("AGENT_BRANCH", "")
    if not agent_branch:
        raise RuntimeError("AGENT_BRANCH is required on the operator side")
    _git("fetch", "-q", "origin", agent_branch, check=True)
    r = _git("show", f"origin/{agent_branch}:run/actuation_tasks.json")
    if r.returncode != 0:
        raise RuntimeError(f"cannot read requests from origin/{agent_branch}")
    tasks = json.loads(r.stdout).get("tasks", [])
    task = next((t for t in tasks if t.get("id") == task_id), None)
    if not task or task.get("status") != "open":
        raise RuntimeError(f"no open request {task_id!r} on origin/{agent_branch}")
    return task


def _publish_resolution(task: dict, resolution: dict) -> None:
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
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    with RESOLUTION_LOCK.open("a+") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        resolutions = _facts_resolutions()
        if task["id"] in resolutions:
            raise RuntimeError(f"resolution for {task['id']} already exists; facts are append-only")
        resolutions[task["id"]] = {**resolution, "task_sha256": _task_hash(task), "at": _now(),
                                   "agent_branch": agent_branch}
        RESOLUTIONS.parent.mkdir(parents=True, exist_ok=True)
        prev_doc = RESOLUTIONS.read_bytes() if RESOLUTIONS.exists() else None
        prev_sig = RESOLUTION_SIG.read_bytes() if RESOLUTION_SIG.exists() else None
        tmp = RESOLUTIONS.with_name(RESOLUTIONS.name + ".tmp")
        tmp.write_text(json.dumps({"resolutions": resolutions}, indent=2) + "\n")
        os.replace(tmp, RESOLUTIONS)
        try:
            _sign_resolution_document()
        except Exception:
            if prev_doc is None:
                RESOLUTIONS.unlink(missing_ok=True)
            else:
                RESOLUTIONS.write_bytes(prev_doc)
            if prev_sig is None:
                RESOLUTION_SIG.unlink(missing_ok=True)
            else:
                RESOLUTION_SIG.write_bytes(prev_sig)
            raise
        _git("add", str(RESOLUTIONS), str(RESOLUTION_SIG), check=True)
        commit = subprocess.run(
            ["git", "-c", "user.name=verifier", "-c", "user.email=verifier@local",
             "-c", "commit.gpgsign=false", "commit", "-m",
             f"verifier: resolve actuation {task['id']}", "--", str(RESOLUTIONS),
             str(RESOLUTION_SIG)], cwd=REPO, capture_output=True, text=True, timeout=90,
            env={**os.environ, "AIV_VERIFIER": "1"})
        if commit.returncode != 0:
            raise RuntimeError(f"could not commit resolution: {commit.stderr.strip()[:160]}")
        push = _git("push", "origin", f"HEAD:{ledger_branch}")
        if push.returncode != 0:
            raise RuntimeError(f"could not publish resolution: {push.stderr.strip()[:160]}")


def _grounded_resolution(task: dict) -> dict | None:
    ledger_branch = os.environ.get("LEDGER_BRANCH", "ledger")
    current = _git("branch", "--show-current").stdout.strip()
    task_branch = task.get("agent_branch") or current
    if ledger_branch in {current, task_branch}:
        raise RuntimeError("LEDGER_BRANCH must differ from the claims branch; refusing a "
                           "self-authored resolution")
    _git("fetch", "-q", "origin", ledger_branch, check=True)
    ref = f"origin/{ledger_branch}"
    r = _git("show", f"{ref}:ledger/actuation_resolutions.json")
    if r.returncode != 0:
        return None
    _verify_resolution_document(ref, r.stdout)
    resolution = json.loads(r.stdout).get("resolutions", {}).get(task["id"])
    if resolution and resolution.get("task_sha256") != _task_hash(task):
        raise RuntimeError(f"resolution for {task['id']} is bound to different request content")
    if resolution and resolution.get("agent_branch") != task_branch:
        raise RuntimeError(f"resolution for {task['id']} names a different claims branch")
    return resolution


# ---- companion bet (conclusion-blocking / request-don't-wait); best-effort ---------------
def _register_companion_bet(task_id: str, kind: str, gate: str, deadline: str) -> str | None:
    try:
        import bets as _bets
        resolve_by = (dt.datetime.now(dt.timezone.utc)
                      + dt.timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ")
        try:
            ttl_h = (_parse_iso(deadline) - dt.datetime.now(dt.timezone.utc)).total_seconds() / 3600
        except Exception:
            ttl_h = 24.0
        poll = max(0.05, min(24.0, ttl_h / 4)) if ttl_h > 0 else 0.05
        ns = argparse.Namespace(what=f"actuation {task_id} ({kind}): {gate}", clock="approval",
                                check=f"bin/actuate.py list  # is {task_id} fulfilled?",
                                oracle="judgment", poll_after_h=poll, resolve_by=resolve_by)
        if _bets.cmd_add(ns) == 0:
            return f"bet-{len(_bets._load()):03d}"
    except Exception as e:
        print(f"warn: companion bet not registered ({e}); request still tracked.", file=sys.stderr)
    return None


def _resolve_companion_bet(bet_id: str | None, outcome: str, evidence: str) -> None:
    if not bet_id:
        return
    try:
        import bets as _bets
        ns = argparse.Namespace(id=bet_id, outcome="won" if outcome == "fulfilled" else "lost",
                                evidence=evidence, downgrade_judgment=False)
        _bets.cmd_resolve(ns)
    except Exception as e:
        print(f"warn: companion bet {bet_id} not resolved ({e}).", file=sys.stderr)


# ---- commands ---------------------------------------------------------------------------
def cmd_request(a) -> int:
    if a.kind not in KINDS:
        print(f"FATAL: --kind must be one of {KINDS}. This queue carries mechanical ACTUATION "
              "only (actuator, never oracle).", file=sys.stderr)
        return 2
    if a.return_kind not in RETURN_KINDS:
        print(f"FATAL: --return-kind must be one of {RETURN_KINDS}.", file=sys.stderr)
        return 2
    # descriptive fields must be PRESENT; --test/--ev carry the falsify-before-requesting and
    # worth-the-minutes guardrails, so they must be SUBSTANTIVE (not a rubber-stamp character).
    for field, minlen, why in (("gate", 1, "which gate/action"), ("target_url", 1, "the exact URL"),
                               ("identity", 1, "which account acts"), ("expect", 1, "the result"),
                               ("test", 4, "the empirical hit, cited — a request for an untested "
                                "gate is guessing"), ("ev", 4, "why passing it is worth minutes")):
        if len(getattr(a, field).strip()) < minlen:
            print(f"FATAL: --{field.replace('_','-')} needs real content ({why}).", file=sys.stderr)
            return 2
    try:
        steps_text = Path(a.steps).read_text()
    except OSError as e:
        print(f"FATAL: cannot read --steps file: {e}", file=sys.stderr)
        return 2
    hit = leak_check(" \n ".join([a.gate, steps_text, a.expect, a.identity]))
    if hit:
        print(f"FATAL: actuator, never oracle -- the request text asks the operator to decide "
              f"strategy/content (matched {hit!r}). Strategy, judgment, and content are not "
              "requestable; only mechanical gate-passage is.", file=sys.stderr)
        return 2
    try:
        _parse_iso(a.deadline)
    except Exception:
        print("FATAL: --deadline must be ISO-8601 (e.g. 2026-08-01T00:00:00Z).", file=sys.stderr)
        return 2

    tasks = _load_tasks()
    tid = f"ACT-{len(tasks) + 1:03d}"
    enc_pubkey = None
    if a.return_kind == "credential":
        try:
            enc_pubkey = _gen_keypair(tid)
        except Exception as e:
            print(f"FATAL: could not create the secure return channel: {e}", file=sys.stderr)
            return 1
    artifact_ref = None
    extra_paths = []
    if a.artifact and a.artifact != "-":
        src = Path(a.artifact)
        if not src.exists():
            print(f"FATAL: --artifact file not found: {src}", file=sys.stderr)
            return 2
        dst_dir = ARTIFACTS_DIR / tid
        dst_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy(src, dst_dir / src.name)
        artifact_ref = f"run/actuation_artifacts/{tid}/{src.name}"
        extra_paths.append(ARTIFACTS_DIR)
    agent_branch = _git("branch", "--show-current").stdout.strip()
    if not agent_branch:
        print("FATAL: actuation requests require a named claims branch.", file=sys.stderr)
        return 2
    bet_id = _register_companion_bet(tid, a.kind, a.gate, a.deadline)
    tasks.append({"id": tid, "requested_at": _now(), "kind": a.kind, "gate": a.gate,
                  "target_url": a.target_url, "identity": a.identity,
                  "steps": steps_text.splitlines(), "artifact_ref": artifact_ref,
                  "expect": a.expect, "return_kind": a.return_kind, "enc_pubkey": enc_pubkey,
                  "deadline": a.deadline, "test_citation": a.test, "ev_rationale": a.ev,
                  "status": "open", "companion_bet": bet_id, "agent_branch": agent_branch,
                  "human_minutes": None, "resolution_latency_seconds": None, "resolution": None})
    _save_tasks(tasks, f"actuate: request {tid} ({a.kind}): {a.gate[:50]}", extra_paths)
    print(f"id={tid} requested ({a.kind}); return-kind={a.return_kind}. KEEP WORKING -- requesting "
          "is never waiting. Render the operator card with: bin/actuate.py card " + tid)
    return 0


def cmd_card(a) -> int:
    task = next((t for t in _load_tasks() if t.get("id") == a.id), None)
    if not task:
        print(f"FATAL: no task {a.id!r}", file=sys.stderr)
        return 1
    lines = [f"# Actuation task {task['id']} — {task['kind']}", "",
             f"**What/gate:** {task['gate']}",
             f"**Act as:** {task['identity']}",
             f"**Deadline:** {task['deadline']}",
             f"**Target URL:** {task['target_url']}", "",
             "## Steps"]
    for i, step in enumerate(task.get("steps") or [], 1):
        lines.append(f"{i}. {step}" if not step[:2].strip().rstrip('.').isdigit() else step)
    lines += ["", f"**Expected result:** {task['expect']}",
              f"**Return kind:** {task['return_kind']}"]
    if task.get("artifact_ref"):
        lines.append(f"**Staged artifact (apply this):** {task['artifact_ref']}")
    lines += ["", "## To fulfill (operator, from the facts lane)",
              f"    bin/actuate.py fulfill {task['id']} --minutes <n> --evidence \"<what you did>\""]
    rk = task["return_kind"]
    if rk == "credential":
        lines.append(f"    # add: --return-file <file with the credential>  (encrypted to {task['id']})")
    elif rk in ("confirmation", "value"):
        lines.append("    # add: --return-value \"<the confirmation/value>\"")
    lines += ["", f"Or decline: bin/actuate.py decline {task['id']} --minutes <n> --reason \"<why>\""]
    print("\n".join(lines))
    return 0


def cmd_fulfill(a) -> int:
    if a.minutes is None or a.minutes < 0:
        print("FATAL: --minutes required (the metering IS the point).", file=sys.stderr)
        return 2
    if len(a.evidence.strip()) < 8:
        print("FATAL: --evidence required (what was actually done).", file=sys.stderr)
        return 2
    try:
        task = _operator_task(a.id)
    except Exception as e:
        print(f"FATAL: {e}", file=sys.stderr)
        return 1
    resolution = {"status": "fulfilled", "human_minutes": a.minutes, "evidence": a.evidence}
    rk = task.get("return_kind", "none")
    if rk != "none":
        if a.return_file:
            plaintext = Path(a.return_file).read_bytes()
        elif a.return_value is not None:
            plaintext = a.return_value.encode()
        else:
            print(f"FATAL: task {a.id} expects a return-kind={rk}; supply --return-file or "
                  "--return-value.", file=sys.stderr)
            return 2
        try:
            if rk == "credential":
                if not task.get("enc_pubkey"):
                    raise RuntimeError("task has no ephemeral public key; cannot encrypt a secret")
                resolution["return"] = _encrypt_to(task["enc_pubkey"], plaintext)
                AUDIT_DIR.mkdir(parents=True, exist_ok=True)
                (AUDIT_DIR / f"{a.id}.plaintext").write_bytes(plaintext)  # off-repo audit copy
            else:
                resolution["return"] = {"scheme": "plain", "value": plaintext.decode(),
                                        "plaintext_sha256": _sha256(plaintext)}
        except Exception as e:
            print(f"FATAL: could not prepare the return payload: {e}", file=sys.stderr)
            return 1
    try:
        _publish_resolution(task, resolution)
    except Exception as e:
        print(f"FATAL: {e}", file=sys.stderr)
        return 1
    print(f"{a.id} fulfilled on the verifier facts lane ({a.minutes} human-minutes). "
          f"Agent must run: bin/actuate.py sync {a.id}")
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
        task = _operator_task(a.id)
        _publish_resolution(task, {"status": "declined", "human_minutes": a.minutes,
                                   "reason": a.reason})
    except Exception as e:
        print(f"FATAL: {e}", file=sys.stderr)
        return 1
    print(f"{a.id} declined on the verifier facts lane. Agent must run: bin/actuate.py sync {a.id}")
    return 0


def cmd_sync(a) -> int:
    tasks = _load_tasks()
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
    if outcome == "fulfilled" and resolution.get("return"):
        ret = resolution["return"]
        try:
            if ret.get("scheme") == "plain":
                plaintext = ret.get("value", "").encode()
                if _sha256(plaintext) != ret.get("plaintext_sha256"):
                    raise RuntimeError("returned value failed its integrity hash")
            else:
                plaintext = _decrypt_with(KEYS_DIR / f"{a.id}.pem", ret)
        except Exception as e:
            print(f"FATAL: could not recover the return payload: {e}", file=sys.stderr)
            return 1
        RETURNS_DIR.mkdir(parents=True, exist_ok=True)
        out = RETURNS_DIR / f"{a.id}.json"
        out.write_text(json.dumps({"id": a.id, "return_kind": task["return_kind"],
                                   "return_value": plaintext.decode(errors="replace")},
                                  indent=2) + "\n")
        out.chmod(0o600)
    task["status"] = outcome
    task["resolution"] = resolution
    task["human_minutes"] = resolution.get("human_minutes")
    try:
        requested = _parse_iso(task["requested_at"])
        resolved = _parse_iso(resolution["at"])
        task["resolution_latency_seconds"] = max(0.0, (resolved - requested).total_seconds())
    except Exception as e:
        print(f"FATAL: invalid resolution latency timestamps: {e}", file=sys.stderr)
        return 1
    # Persist the task state with a TARGETED add: the materialized return under run/
    # actuation_returns/ must never be committed (that is the plaintext handback).
    _save_tasks(tasks, f"actuate: sync grounded {outcome} {a.id}")
    ev = (f"facts-lane resolution: {resolution.get('evidence')}" if outcome == "fulfilled"
          else f"facts-lane decline: {resolution.get('reason')}")
    _resolve_companion_bet(task.get("companion_bet"), outcome, ev)
    where = f" -> run/actuation_returns/{a.id}.json" if resolution.get("return") else ""
    print(f"{a.id} synced from verifier facts: {outcome}{where}.")
    return 0


def cmd_list(_a) -> int:
    tasks = _load_tasks()
    if not tasks:
        print("no actuation requests recorded")
        return 0
    for t in tasks:
        print(f"{t['id']} [{t['status']}] {t['kind']:<15} {t['gate']}\n"
              f"    return:{t['return_kind']} | by {t['deadline']} | {t['target_url']}"
              + (f" | {t['human_minutes']} min" if t.get("human_minutes") is not None else ""))
    print(f"human_minutes_total: {sum(t.get('human_minutes') or 0 for t in tasks)}")
    return 0


def cmd_due(_a) -> int:
    now = dt.datetime.now(dt.timezone.utc)
    for t in _load_tasks():
        if t.get("status") != "open":
            continue
        try:
            ttl = (_parse_iso(t["deadline"]) - now).total_seconds()
        except Exception:
            ttl = 0
        print(f"{t['id']} ttl_s={int(ttl)} {t['kind']} {t['gate']}")
    return 0


def cmd_notify_scan(a) -> int:
    """Operator-side, out-of-band, read-only: deadline-aware alerts for open, unresolved tasks."""
    agent_branch = os.environ.get("AGENT_BRANCH", "")
    if not agent_branch:
        print("FATAL: AGENT_BRANCH required to scan the claims lane.", file=sys.stderr)
        return 2
    _git("fetch", "-q", "origin", agent_branch)
    r = _git("show", f"origin/{agent_branch}:run/actuation_tasks.json")
    tasks = json.loads(r.stdout).get("tasks", []) if r.returncode == 0 else []
    ledger_branch = os.environ.get("LEDGER_BRANCH", "ledger")
    _git("fetch", "-q", "origin", ledger_branch)
    lr = _git("show", f"origin/{ledger_branch}:ledger/actuation_resolutions.json")
    resolved = set(json.loads(lr.stdout).get("resolutions", {})) if lr.returncode == 0 else set()
    now = dt.datetime.now(dt.timezone.utc)
    out_lines = []
    for t in tasks:
        if t.get("status") != "open" or t["id"] in resolved:
            continue
        try:
            ttl = int((_parse_iso(t["deadline"]) - now).total_seconds())
        except Exception:
            ttl = 0
        urgency = "URGENT" if ttl < NOTIFY_URGENT_S else "NORMAL"
        out_lines.append(f"ALERT {t['id']} urgency={urgency} ttl_s={ttl}")
    text = "\n".join(out_lines) + ("\n" if out_lines else "")
    if a.sink:
        Path(a.sink).write_text(text)
    sys.stdout.write(text)
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    pr = sub.add_parser("request")
    for flag in ("--kind", "--gate", "--target-url", "--identity", "--steps", "--expect",
                 "--return-kind", "--deadline", "--test", "--ev"):
        pr.add_argument(flag, required=True, dest=flag.lstrip("-").replace("-", "_"))
    pr.add_argument("--artifact", default="")
    pr.set_defaults(fn=cmd_request)

    pc = sub.add_parser("card")
    pc.add_argument("id")
    pc.set_defaults(fn=cmd_card)

    pf = sub.add_parser("fulfill")
    pf.add_argument("id")
    pf.add_argument("--minutes", type=float, required=True)
    pf.add_argument("--evidence", required=True)
    pf.add_argument("--return-file", dest="return_file", default="")
    pf.add_argument("--return-value", dest="return_value", default=None)
    pf.set_defaults(fn=cmd_fulfill)

    pd = sub.add_parser("decline")
    pd.add_argument("id")
    pd.add_argument("--minutes", type=float, required=True)
    pd.add_argument("--reason", required=True)
    pd.set_defaults(fn=cmd_decline)

    ps = sub.add_parser("sync")
    ps.add_argument("id")
    ps.set_defaults(fn=cmd_sync)

    pn = sub.add_parser("notify-scan")
    pn.add_argument("--sink", default="")
    pn.set_defaults(fn=cmd_notify_scan)

    sub.add_parser("list").set_defaults(fn=cmd_list)
    sub.add_parser("due").set_defaults(fn=cmd_due)

    a = p.parse_args()
    return a.fn(a)


if __name__ == "__main__":
    raise SystemExit(main())

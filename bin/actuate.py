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
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "bin"))


def _env_pos_int(name: str, default: int) -> int:
    """A positive-int env override, fail-soft: a malformed or non-positive value warns and falls
    back to the default rather than raising at module import (which would break every subcommand,
    including ones that never touch the value)."""
    raw = os.environ.get(name)
    if raw is None:
        return default
    try:
        v = int(raw)
        if v <= 0:
            raise ValueError("must be a positive integer")
    except ValueError as e:
        print(f"warn: {name}={raw!r} is invalid ({e}); using default {default}.", file=sys.stderr)
        return default
    return v


TASKS = REPO / "run" / "actuation_tasks.json"
RESOLUTIONS = REPO / "ledger" / "actuation_resolutions.json"
RESOLUTION_SIG = REPO / "ledger" / "actuation_resolutions.json.sig"
RETURNS_DIR = REPO / "run" / "actuation_returns"          # git-ignored; sandbox-only handback
ARTIFACTS_DIR = REPO / "run" / "actuation_artifacts"      # committed; the operator's staged files

KINDS = ("claim-host", "deploy-account", "wallet-fund", "kyc-step", "approval-click")
# Kinds that move the principal's real capital on an irreversible rail. Fulfilling one requires a
# recorded P3-class name-test ruling (COMPARATIVE_ANALYSIS §12 R1) -- the operator's consent is a
# checkpoint, but the *reasoning* must be committed too, per the constitution's "real capital is the
# operator's checkpoint" bound. Enforced in cmd_fulfill.
MONEY_MOVING_KINDS = ("wallet-fund",)
RETURN_KINDS = ("none", "confirmation", "value", "credential")
# Open requests each block conclusions; cap the queue to bound spam (COMPARATIVE_ANALYSIS §12 R1).
MAX_OPEN_REQUESTS = _env_pos_int("ACTUATE_MAX_OPEN", 3)
SIGN_NAMESPACE = "money-agent-actuation"   # per-purpose domain separation (no cross-protocol replay)

STATE_DIR = Path(os.environ.get("MONEY_AGENT_STATE", str(Path.home() / ".money-agent-verifier")))
SIGN_KEY = STATE_DIR / "verifier_signing_key"
KEYS_DIR = STATE_DIR / "actuation_keys"                   # ephemeral private keys (never git)
AUDIT_DIR = STATE_DIR / "actuation_returns"               # operator's off-repo plaintext retention
RESOLUTION_LOCK = STATE_DIR / "actuation_resolutions.lock"
NOTIFY_URGENT_S = _env_pos_int("NOTIFY_URGENT_S", 900)
VERIFY_TIMEOUT_S = _env_pos_int("ACTUATE_VERIFY_TIMEOUT_S", 120)  # post-handback probe cap

# actuator-never-oracle: this is a HEURISTIC TRIPWIRE, not a wall. A denylist cannot catch every
# paraphrase (an adversary proved synonym bypasses); the real backstop is the human operator, who
# sees the rendered card and can DECLINE any oracle-shaped ask (a metered decline is the operator's
# REFUSALS mirror). The tripwire's job is to catch the obvious cases and the run-1 OPERATOR_UNBLOCK
# strategy-leak class cheaply. It is applied to EVERY operator-facing surface (gate/steps/expect/
# identity/target_url AND the staged artifact bytes), with word-boundary matching to cut false
# positives on legitimate substrings.
ORACLE_TERMS = ("strategy", "decide", "choose", "target market", "market to target",
                "which product", "which market", "launch copy", "pricing", "recommend",
                "brainstorm", "come up with", "what to sell", "should we sell", "write the",
                "pick the", "pick which", "pick one", "in your own words", "compose", "settle on",
                "which one", "advise", "what should we", "how much should", "of your choosing",
                "you believe", "your judgment", "judgment needed", "your call")
_ORACLE_RE = re.compile(r"(?<![a-z])(" + "|".join(re.escape(t) for t in ORACLE_TERMS) + r")(?![a-z])")


# ---- small helpers ----------------------------------------------------------------------
def _now() -> str:
    """UTC timestamp as ISO-8601 with a trailing Z."""
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _parse_iso(s: str) -> dt.datetime:
    """Parse an ISO-8601 timestamp (accepting a trailing Z) to a datetime."""
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))


def _sha256(b: bytes) -> str:
    """Hex sha256 of the given bytes."""
    return hashlib.sha256(b).hexdigest()


def _git(*args: str, check: bool = False) -> subprocess.CompletedProcess:
    """Run a git command in the repo and capture its text output."""
    return subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True,
                          timeout=90, check=check)


def _git_show_bytes(ref: str) -> bytes | None:
    """Raw bytes of a git object (binary-safe, unlike _git's text=True) or None if absent."""
    p = subprocess.run(["git", "show", ref], cwd=REPO, capture_output=True, timeout=90)
    return p.stdout if p.returncode == 0 else None


def _verify_local_artifact(task: dict) -> None:
    """Raise if the task stages an artifact whose on-disk bytes no longer match the bound sha.

    cmd_request always sets artifact_ref and artifact_sha256 together, so a ref WITHOUT a sha can
    only be tampering -- and skipping the check on a null sha would let the agent swap the applied
    bytes (and dodge the request-time leak-check). A present ref therefore REQUIRES a present sha."""
    ref = task.get("artifact_ref")
    if not ref:
        return
    want = task.get("artifact_sha256")
    if not want:
        raise RuntimeError(f"staged artifact {ref} carries no bound sha256 (tampered)")
    f = REPO / ref
    if not f.is_file() or _sha256(f.read_bytes()) != want:
        raise RuntimeError(f"staged artifact {ref} does not match its bound sha256 (tampered)")


def _load_tasks() -> list[dict]:
    """Load the actuation task list from run/actuation_tasks.json (empty if absent)."""
    if TASKS.exists():
        return json.loads(TASKS.read_text()).get("tasks", [])
    return []


def _save_tasks(tasks: list[dict], msg: str, extra_paths: list[Path] | None = None) -> None:
    """Write the task list, stage the given paths, commit if changed, and best-effort push."""
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
    # Bind EVERY field the operator sees on the card, so the signature attests to exactly what the
    # human acted on. Omitting identity/steps/expect/artifact (as an earlier version did) let the
    # agent rewrite the meaning of an approved request post-signature -- a binding-confusion break.
    """Stable sha256 over every operator-visible field, so the signature binds what the card showed."""
    stable = {k: task.get(k) for k in ("id", "requested_at", "kind", "gate", "target_url",
                                       "identity", "steps", "expect", "artifact_ref",
                                       "artifact_sha256", "return_kind", "deadline", "agent_branch",
                                       "enc_pubkey")}
    return _sha256(json.dumps(stable, sort_keys=True, separators=(",", ":")).encode())


def leak_check(text: str) -> str | None:
    """Return the first oracle-term the text trips (actuator-never-oracle tripwire), else None."""
    m = _ORACLE_RE.search(text.lower())
    return m.group(1) if m else None


_CTRL_RE = re.compile(r"[\x00-\x1f\x7f]")


def _scrub(s) -> str:
    """One-line, control-char-free rendering of an agent-controlled string for the alert line.
    The agent owns run/actuation_tasks.json, so EVERY field it emits (id/kind/gate) is untrusted:
    a raw newline in any of them would forge a second physical ALERT line the notifier dispatches."""
    return re.sub(r"\s+", " ", _CTRL_RE.sub(" ", str(s if s is not None else ""))).strip()


# ---- ephemeral hybrid encryption (openssl: RSA-OAEP-wrapped AES-256-CBC) -----------------
def _openssl(args: list[str], data: bytes | None = None) -> tuple[int, bytes, bytes]:
    """Run openssl with the given args; return (returncode, stdout, stderr) as bytes."""
    p = subprocess.run(["openssl", *args], input=data, capture_output=True, timeout=60)
    return p.returncode, p.stdout, p.stderr


def _require_openssl() -> None:
    """Raise if openssl is unavailable (the secret return channel needs it)."""
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
    """Hybrid-encrypt plaintext to an RSA public key (RSA-OAEP-wrapped AES-256-CBC); return the payload dict."""
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
    """Decrypt a hybrid payload with the ephemeral private key and verify its plaintext sha256."""
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
    """Sign the resolutions document with the verifier-only key (detached .sig)."""
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
    # The trust anchor is read from HEAD:harness/allowed_signers (the agent's own tree) -- identical
    # to bin/human.py/bin/truth.py. That is defense-in-depth, not the wall: the wall is remote
    # ledger-branch write protection (the agent cannot place a matching forged+signed doc on
    # origin/LEDGER_BRANCH), and sod_hook.sh blocks committing allowed_signers in the first place.
    """Verify the resolutions document against the signer pinned in the committed harness."""
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
    """Load the operator-resolutions map from the facts-lane file (empty if absent)."""
    if RESOLUTIONS.exists():
        return json.loads(RESOLUTIONS.read_text()).get("resolutions", {})
    return {}


def _operator_tasks_all() -> list[dict]:
    """Fetch the agent branch from origin and return its full task list (operator side)."""
    agent_branch = os.environ.get("AGENT_BRANCH", "")
    if not agent_branch:
        raise RuntimeError("AGENT_BRANCH is required on the operator side")
    _git("fetch", "-q", "origin", agent_branch, check=True)
    r = _git("show", f"origin/{agent_branch}:run/actuation_tasks.json")
    if r.returncode != 0:
        # An absent run/actuation_tasks.json is an EMPTY queue, not an error: the agent has
        # simply not queued a request yet (the file is created on the first request). The fetch
        # above (check=True) already proved the branch exists, so a missing PATH is the only
        # benign failure -- treat it as [] (consistent with the agent-side _tasks(), which reads
        # an absent file as []), and still raise on any other git error.
        if "does not exist" in (r.stderr or ""):
            return []
        raise RuntimeError(f"cannot read requests from origin/{agent_branch}: "
                           f"{(r.stderr or '').strip()[:160]}")
    return json.loads(r.stdout).get("tasks", [])


def _operator_open_tasks() -> list[dict]:
    """The open (unresolved) requests, for the operator's queue view (the web form's list)."""
    return [t for t in _operator_tasks_all() if t.get("status") == "open"]


def _operator_task(task_id: str) -> dict:
    """Read one OPEN task by id from the agent branch on origin (operator side)."""
    task = next((t for t in _operator_tasks_all() if t.get("id") == task_id), None)
    if not task or task.get("status") != "open":
        agent_branch = os.environ.get("AGENT_BRANCH", "")
        raise RuntimeError(f"no open request {task_id!r} on origin/{agent_branch}")
    return task


def _publish_resolution(task: dict, resolution: dict) -> None:
    """Append, sign, commit, and push an operator resolution on the facts lane."""
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
            # The facts lane is SHARED with the verifier (it publishes truth.json every cycle), so a
            # non-fast-forward here is expected contention, not a failure. Our resolution commit
            # touches only actuation_resolutions.json (+ .sig) -- never the verifier's truth.json /
            # raw / -- so rebasing our single commit onto the current tip is clean; then push again.
            _git("fetch", "-q", "origin", ledger_branch)
            rb = _git("rebase", f"origin/{ledger_branch}")
            if rb.returncode != 0:
                _git("rebase", "--abort")
                raise RuntimeError("could not publish resolution: the facts lane advanced and the "
                                   f"rebase did not apply cleanly: {rb.stderr.strip()[:140]}")
            push = _git("push", "origin", f"HEAD:{ledger_branch}")
            if push.returncode != 0:
                raise RuntimeError(f"could not publish resolution after rebase onto the current "
                                   f"facts tip: {push.stderr.strip()[:160]}")


def _grounded_resolution(task: dict) -> dict | None:
    """Fetch and verify the signed resolution for a task; return it, or None if unresolved."""
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
    """Register the conclusion-blocking companion bet; return its id, or None on failure."""
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
            placed = _bets._load()   # read the id cmd_add actually appended, not a re-derived count
            if placed:
                return placed[-1].get("id")
    except Exception as e:
        print(f"warn: companion bet not registered ({e}); request still tracked.", file=sys.stderr)
    return None


def _resolve_companion_bet(bet_id: str | None, outcome: str, evidence: str) -> None:
    """Best-effort resolution of the companion bet after a sync (won/lost)."""
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
    """Agent: file a typed, validated actuation request (leak-checked, capped, bet-backed)."""
    if a.kind not in KINDS:
        print(f"FATAL: --kind must be one of {KINDS}. This queue carries mechanical ACTUATION "
              "only (actuator, never oracle).", file=sys.stderr)
        return 2
    if a.return_kind not in RETURN_KINDS:
        print(f"FATAL: --return-kind must be one of {RETURN_KINDS}.", file=sys.stderr)
        return 2
    # Optional PRE-REGISTERED post-handback usability probe: proves the returned credential grants
    # working sandbox access (catches the WAF/IP-reputation residual). Needs a materialized return.
    verify_cmd = (getattr(a, "verify_cmd", "") or "").strip()
    if verify_cmd and a.return_kind not in ("value", "credential"):
        print("FATAL: --verify-cmd needs a materialized return to probe; it is only valid with "
              "--return-kind value or credential.", file=sys.stderr)
        return 2
    # descriptive fields must be PRESENT; --test/--ev carry the falsify-before-requesting and
    # worth-the-minutes guardrails, so they must be SUBSTANTIVE (>= 8 chars, parity with human.py).
    for field, minlen, why in (("gate", 1, "which gate/action"), ("target_url", 1, "the exact URL"),
                               ("identity", 1, "which account acts"), ("expect", 1, "the result"),
                               ("test", 8, "the empirical hit, cited — a request for an untested "
                                "gate is guessing"), ("ev", 8, "why passing it is worth minutes")):
        if len(getattr(a, field).strip()) < minlen:
            print(f"FATAL: --{field.replace('_','-')} needs real content ({why}).", file=sys.stderr)
            return 2
    try:
        steps_text = Path(a.steps).read_text()
    except OSError as e:
        print(f"FATAL: cannot read --steps file: {e}", file=sys.stderr)
        return 2
    try:
        deadline_dt = _parse_iso(a.deadline)
    except Exception:
        print("FATAL: --deadline must be ISO-8601 (e.g. 2026-08-01T00:00:00Z).", file=sys.stderr)
        return 2
    if deadline_dt.tzinfo is None:
        print("FATAL: --deadline must carry a timezone/offset (append 'Z' for UTC). A naive "
              "deadline silently poisons every downstream time computation.", file=sys.stderr)
        return 2
    if deadline_dt <= dt.datetime.now(dt.timezone.utc):
        print("FATAL: --deadline must be in the future; a past deadline is already expired.",
              file=sys.stderr)
        return 2
    # Validate + read the artifact BEFORE any side effect (keygen/copy), so a bad path fails clean.
    artifact_bytes = None
    src = None
    if a.artifact and a.artifact != "-":
        src = Path(a.artifact)
        if not src.is_file():
            print(f"FATAL: --artifact must be a readable file: {src}", file=sys.stderr)
            return 2
        try:
            artifact_bytes = src.read_bytes()
        except OSError as e:
            print(f"FATAL: cannot read --artifact: {e}", file=sys.stderr)
            return 2
    # Leak-check EVERY operator-facing surface, including the staged artifact the card says "apply".
    artifact_text = artifact_bytes.decode("utf-8", "ignore") if artifact_bytes is not None else ""
    hit = leak_check(" \n ".join([a.gate, steps_text, a.expect, a.identity, a.target_url,
                                  artifact_text]))
    if hit:
        print(f"FATAL: actuator, never oracle -- an operator-facing surface asks the operator to "
              f"decide strategy/content (matched {hit!r}). Strategy, judgment, and content are not "
              "requestable; only mechanical gate-passage is.", file=sys.stderr)
        return 2

    agent_branch = _git("branch", "--show-current").stdout.strip()
    if not agent_branch:
        print("FATAL: actuation requests require a named claims branch.", file=sys.stderr)
        return 2
    tasks = _load_tasks()
    open_count = sum(1 for t in tasks if t.get("status") == "open")
    if open_count >= MAX_OPEN_REQUESTS:
        print(f"FATAL: {open_count} actuation request(s) already open (cap {MAX_OPEN_REQUESTS}); "
              "each blocks conclusions. Resolve or wait for the existing ones before filing another.",
              file=sys.stderr)
        return 1
    tid = f"ACT-{len(tasks) + 1:03d}"
    # Register the conclusion-blocking companion bet FIRST and make it MANDATORY (parity with
    # human.py): a request the agenda cannot track would be the invisible-wait this tool exists to
    # kill, and the orphan-bet backstop in conclusion_gate.py (which catches DELETION of the task
    # file) depends on every task having a bet. Doing it before keygen/artifact-staging means a bet
    # failure leaves no orphan key or staged file.
    bet_id = _register_companion_bet(tid, a.kind, a.gate, a.deadline)
    if not bet_id:
        print("FATAL: could not register the conclusion-blocking companion bet; refusing to file "
              "an actuation the agenda cannot track.", file=sys.stderr)
        return 1
    enc_pubkey = None
    if a.return_kind == "credential":
        try:
            enc_pubkey = _gen_keypair(tid)
        except Exception as e:
            print(f"FATAL: could not create the secure return channel: {e}", file=sys.stderr)
            return 1
    artifact_ref = artifact_sha256 = None
    extra_paths = []
    if artifact_bytes is not None:
        dst_dir = ARTIFACTS_DIR / tid
        dst_dir.mkdir(parents=True, exist_ok=True)
        (dst_dir / src.name).write_bytes(artifact_bytes)
        artifact_ref = f"run/actuation_artifacts/{tid}/{src.name}"
        # sha of the exact bytes, bound into _task_hash AND re-verified at fulfill/sync so a
        # post-signature file swap is detected (a ref present REQUIRES a matching sha).
        artifact_sha256 = _sha256(artifact_bytes)
        extra_paths.append(ARTIFACTS_DIR)
    tasks.append({"id": tid, "requested_at": _now(), "kind": a.kind, "gate": a.gate,
                  "target_url": a.target_url, "identity": a.identity,
                  "steps": steps_text.splitlines(), "artifact_ref": artifact_ref,
                  "artifact_sha256": artifact_sha256, "expect": a.expect,
                  "return_kind": a.return_kind, "enc_pubkey": enc_pubkey,
                  "deadline": a.deadline, "test_citation": a.test, "ev_rationale": a.ev,
                  "verify_cmd": verify_cmd or None,
                  "status": "open", "companion_bet": bet_id, "agent_branch": agent_branch,
                  "human_minutes": None, "resolution_latency_seconds": None, "resolution": None})
    # Two independent backstops now cover the task: conclusion_gate.py blocks on an OPEN actuation
    # directly, and on the orphaned companion bet if the task file is deleted.
    _save_tasks(tasks, f"actuate: request {tid} ({a.kind}): {a.gate[:50]}", extra_paths)
    print(f"id={tid} requested ({a.kind}); return-kind={a.return_kind}. KEEP WORKING -- requesting "
          "is never waiting. Render the operator card with: bin/actuate.py card " + tid)
    return 0


def _render_card(task: dict, include_cli: bool = True) -> str:
    """Build the human-readable operator card (shared by `card` and the fulfill web form).

    include_cli=False omits the terminal fulfill/decline recipe -- the web form provides those
    controls, so showing the CLI there is just noise. Every agent-controlled field is scrubbed of
    control characters: the card is read in a terminal or a browser, and raw ANSI/OSC escapes in
    gate/identity/steps/etc. could rewrite or hide the real instructions (or poison the clipboard)
    before the operator sees them."""
    lines = [f"# Actuation task {_scrub(task['id'])} — {_scrub(task['kind'])}", "",
             f"**What/gate:** {_scrub(task['gate'])}",
             f"**Act as:** {_scrub(task['identity'])}",
             f"**Deadline:** {_scrub(task['deadline'])}",
             f"**Target URL:** {_scrub(task['target_url'])}", "",
             "## Steps"]
    _numbered = re.compile(r"^\s*\d+[.)]\s")   # already has a "1. " / "2) " marker
    for i, step in enumerate(task.get("steps") or [], 1):
        step = _scrub(step)
        lines.append(step if _numbered.match(step) else f"{i}. {step}")
    lines += ["", f"**Expected result:** {_scrub(task['expect'])}",
              f"**Return kind:** {_scrub(task['return_kind'])}"]
    if task.get("artifact_ref"):
        lines.append(f"**Staged artifact (apply this):** {_scrub(task['artifact_ref'])}")
        if task.get("artifact_sha256"):
            lines.append(f"    sha256: {task['artifact_sha256']}  "
                         "(verify the file matches this before applying)")
    if not include_cli:
        return "\n".join(lines)   # the web form supplies the fulfill/decline controls
    lines += ["", "## To fulfill (operator, from the facts lane)",
              f"    bin/actuate.py fulfill {task['id']} --minutes <n> --evidence \"<what you did>\""]
    rk = task["return_kind"]
    if rk == "credential":
        lines.append(f"    # add: --return-file <file with the credential>  (encrypted to {task['id']})")
    elif rk in ("confirmation", "value"):
        lines.append("    # add: --return-value \"<the confirmation/value>\"")
    lines += ["", f"Or decline: bin/actuate.py decline {task['id']} --minutes <n> --reason \"<why>\"",
              "", "Tip: `bin/actuate_fulfill_server.py` serves this as a local web form -- no terminal."]
    return "\n".join(lines)


def cmd_card(a) -> int:
    """Render the human-readable operator card for a task."""
    task = next((t for t in _load_tasks() if t.get("id") == a.id), None)
    if not task:
        print(f"FATAL: no task {a.id!r}", file=sys.stderr)
        return 1
    print(_render_card(task))
    return 0


def cmd_fulfill(a) -> int:
    """Operator: publish a signed 'fulfilled' resolution (metered; P3-gated for money-moving kinds)."""
    if a.minutes is None or not math.isfinite(a.minutes) or a.minutes <= 0:
        print("FATAL: --minutes must be a finite number > 0 (a real human action costs real "
              "minutes; the metering IS the point).", file=sys.stderr)
        return 2
    if len(a.evidence.strip()) < 8:
        print("FATAL: --evidence required (what was actually done).", file=sys.stderr)
        return 2
    try:
        task = _operator_task(a.id)
    except Exception as e:
        print(f"FATAL: {e}", file=sys.stderr)
        return 1
    # The task is read from the agent branch, so the kind is agent-controlled -- validate it against
    # the allowlist before anything else, or an unrecognized kind would skip the money-moving gate.
    if task.get("kind") not in KINDS:
        print(f"FATAL: task {a.id} has an unrecognized kind {task.get('kind')!r}; only allowlisted "
              "kinds are fulfillable.", file=sys.stderr)
        return 2
    resolution_extra = {}
    if task.get("kind") in MONEY_MOVING_KINDS:
        # A money-moving kind spends the principal's real capital on an irreversible rail. Fulfilling
        # it requires a recorded P3-class name-test ruling (not just the operator's click): the
        # rationale is embedded in the signed resolution, so the consent is permanent and grounded.
        if not a.consent_ruling or len(a.consent_ruling.strip()) < 20:
            print(f"FATAL: {task['kind']} moves the principal's real money -- fulfilling it requires "
                  "a recorded P3 name-test ruling. Pass --consent-ruling \"<the name-test / statement-"
                  "descriptor rationale for spending real capital>\" (>= 20 chars).", file=sys.stderr)
            return 2
        resolution_extra["p3_ruling"] = a.consent_ruling.strip()
    # If the request stages an artifact the operator will APPLY, verify its committed bytes match the
    # sha the request bound (and that the operator's signature will cover). A ref present REQUIRES a
    # sha (nulling it is tamper); a swapped file is a tampered request. Refuse before the operator
    # acts on the wrong bytes.
    if task.get("artifact_ref"):
        want = task.get("artifact_sha256")
        ab = _git_show_bytes(f"origin/{os.environ['AGENT_BRANCH']}:{task['artifact_ref']}") if want \
            else None
        if not want or ab is None or _sha256(ab) != want:
            print(f"FATAL: staged artifact {task['artifact_ref']} is missing its bound sha256 or its "
                  "bytes do not match it -- the request is tampered; refusing to fulfill.",
                  file=sys.stderr)
            return 1
        # The operator is about to APPLY these bytes. Re-run the actuator-never-oracle check on the
        # ACTUAL committed artifact: the request-time check saw only the original bytes, and the agent
        # can swap the file to oracle/strategy content with a consistent sha before fulfillment.
        hit = leak_check(ab.decode("utf-8", "ignore"))
        if hit:
            print(f"FATAL: the staged artifact asks the operator to decide strategy/content "
                  f"(matched {hit!r}) -- actuator, never oracle; refusing to fulfill.", file=sys.stderr)
            return 1
    resolution = {"status": "fulfilled", "human_minutes": a.minutes, "evidence": a.evidence,
                  **resolution_extra}
    rk = task.get("return_kind", "none")
    if rk != "none":
        if a.return_file:
            try:
                plaintext = Path(a.return_file).read_bytes()
            except OSError as e:
                print(f"FATAL: cannot read --return-file: {e}", file=sys.stderr)
                return 2
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
                AUDIT_DIR.mkdir(parents=True, exist_ok=True, mode=0o700)
                _audit = AUDIT_DIR / f"{a.id}.plaintext"           # off-repo audit copy
                _audit.write_bytes(plaintext)
                _audit.chmod(0o600)                                # never group/other-readable
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
    """Operator: publish a signed 'declined' resolution (metered)."""
    if a.minutes is None or not math.isfinite(a.minutes) or a.minutes <= 0:
        print("FATAL: --minutes must be a finite number > 0; assessing a declined request is "
              "still human work.", file=sys.stderr)
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


def cmd_withdraw(a) -> int:
    """Agent: retract its OWN open request (an abandoned direction), freeing the capped queue.

    The queue's only exits were operator fulfill/decline + agent sync, so a request the agent no
    longer intends to pursue (a dropped direction) sat 'open' forever, permanently consuming one of
    the MAX_OPEN_REQUESTS slots and forcing the operator to decline it by hand. Since run/actuation_
    tasks.json is the AGENT's own claims file, retracting a request the agent authored fabricates no
    human action -- it is not a resolution, so it never touches the verifier facts lane and does not
    violate separation of duties (nothing claims 'a human acted'). It DOES resolve the conclusion-
    blocking companion bet, so a withdrawn task leaves no orphan bet to jam conclusion_gate.py.

    Guard: if a verifier-SIGNED resolution already exists for this task, refuse -- the operator has
    already spent real minutes on it; the agent must `sync` to apply that (a withdraw would silently
    discard the operator's action, e.g. a returned credential). The check is fail-soft toward
    UNBLOCKING: only a POSITIVELY found resolution blocks; a None/error (e.g. ledger unreachable)
    lets the withdraw proceed, since the whole point is to break a deadlock, not to add a new way to
    get stuck."""
    if len(a.reason.strip()) < 8:
        print("FATAL: --reason required (why this direction is abandoned; the retraction is on the "
              "record, like a decline).", file=sys.stderr)
        return 2
    tasks = _load_tasks()
    task = next((t for t in tasks if t.get("id") == a.id), None)
    if not task:
        print(f"FATAL: no task {a.id!r}", file=sys.stderr)
        return 1
    if task.get("status") != "open":
        print(f"{a.id} is already {task['status']}; nothing to withdraw.")
        return 0
    try:
        grounded = _grounded_resolution(task)
    except Exception as e:
        print(f"warn: could not check for a signed resolution ({e}); proceeding with withdraw.",
              file=sys.stderr)
        grounded = None
    if grounded:
        print(f"FATAL: {a.id} already has a verifier-signed {grounded.get('status')} resolution -- "
              f"the operator acted on it. Run `bin/actuate.py sync {a.id}` to apply it (a withdraw "
              "would discard the operator's action, including any returned credential).",
              file=sys.stderr)
        return 1
    task["status"] = "withdrawn"
    task["withdrawn_at"] = _now()
    task["withdraw_reason"] = a.reason.strip()
    _save_tasks(tasks, f"actuate: withdraw {a.id} (abandoned): {a.reason.strip()[:50]}")
    _resolve_companion_bet(task.get("companion_bet"), "withdrawn",
                           f"withdrawn by agent: {a.reason.strip()}")
    open_left = sum(1 for t in tasks if t.get("status") == "open")
    print(f"{a.id} withdrawn; companion bet resolved. Queue now {open_left}/{MAX_OPEN_REQUESTS} open.")
    return 0


def _run_usability_probe(task: dict, material_path: Path) -> tuple[str, str]:
    """Run the agent's PRE-REGISTERED post-handback usability probe against the materialized return.

    This is an AGENT-SIDE self-check TRIPWIRE, not a separation-of-duties wall. The operator's
    signed resolution has already discharged the human obligation; this probe can only mark a
    handback UNUSABLE -- the exact WAF/IP-reputation residual an operator-created account does not
    cure (the account exists, but the sandbox still cannot authenticate from here). It NEVER
    authorizes money or any scored outcome, and a PASS grounds nothing on the verifier's facts: it
    only tells the agent whether the returned credential grants working access from this sandbox.
    Monotonic-safe: it can only downgrade a task's usability, never upgrade a fabricated success.
    The command is agent-authored and runs in the agent's own sandbox, so it adds no privilege.
    Returns (status, detail) with status in {"verified", "failed"}."""
    env = dict(os.environ)
    env["ACTUATE_TASK_ID"] = task["id"]
    env["ACTUATE_RETURN_FILE"] = str(material_path.resolve())
    try:
        material = json.loads(material_path.read_text())
        if material.get("return_value") is not None:   # convenience for a text credential
            env["ACTUATE_RETURN_VALUE"] = material["return_value"]
    except (OSError, ValueError):
        pass
    try:
        cp = subprocess.run(["sh", "-c", task["verify_cmd"]], env=env, timeout=VERIFY_TIMEOUT_S,
                            capture_output=True, text=True)
    except subprocess.TimeoutExpired:
        return "failed", f"probe timed out after {VERIFY_TIMEOUT_S}s"
    except Exception as e:   # pragma: no cover - defensive: a broken probe is a failed probe
        return "failed", f"probe could not run ({type(e).__name__}: {e})"
    if cp.returncode == 0:
        return "verified", "probe exited 0 -- credential grants working sandbox access"
    tail = (cp.stderr or cp.stdout or "").strip().splitlines()
    return "failed", f"probe exited {cp.returncode}" + (f": {tail[-1][:160]}" if tail else "")


def _apply_resolution(task: dict, tasks: list[dict], resolution: dict) -> str:
    """Materialize a grounded resolution into task state (shared by `sync` and `sync-all`).

    Raises on any verification/decrypt/timestamp failure so the caller can fail closed; on
    success it persists the task and returns a human-readable line."""
    tid = task["id"]
    outcome = resolution.get("status")
    if outcome not in ("fulfilled", "declined"):
        raise RuntimeError(f"invalid grounded resolution status {outcome!r}")
    _verify_local_artifact(task)   # a post-signature file swap leaves the claims record inconsistent
    if outcome == "fulfilled" and resolution.get("return"):
        ret = resolution["return"]
        if ret.get("scheme") == "plain":
            plaintext = ret.get("value", "").encode()
            if _sha256(plaintext) != ret.get("plaintext_sha256"):
                raise RuntimeError("returned value failed its integrity hash")
        else:
            plaintext = _decrypt_with(KEYS_DIR / f"{tid}.pem", ret)
        RETURNS_DIR.mkdir(parents=True, exist_ok=True)
        out = RETURNS_DIR / f"{tid}.json"
        # Binary-safe: always carry exact bytes (base64) + sha256; return_value is the utf-8 text
        # only when the payload decodes, so a binary credential is never lossily mangled.
        material = {"id": tid, "return_kind": task["return_kind"], "sha256": _sha256(plaintext),
                    "return_value_b64": base64.b64encode(plaintext).decode()}
        try:
            material["return_value"] = plaintext.decode("utf-8")
        except UnicodeDecodeError:
            material["return_value"] = None
            material["encoding"] = "binary — decode return_value_b64"
        out.write_text(json.dumps(material, indent=2) + "\n")
        out.chmod(0o600)
        # Post-handback usability probe (agent-side tripwire): prove the returned credential
        # actually grants working access from this sandbox before treating the task as usable.
        # It can only DOWNGRADE (flag unusable); it never grounds a fact. See _run_usability_probe.
        if task.get("verify_cmd"):
            status, detail = _run_usability_probe(task, out)
            task["usability"] = status
            task["usability_detail"] = detail
            task["usability_checked_at"] = _now()
    task["status"] = outcome
    task["resolution"] = resolution
    task["human_minutes"] = resolution.get("human_minutes")
    requested = _parse_iso(task["requested_at"])
    resolved = _parse_iso(resolution["at"])
    task["resolution_latency_seconds"] = max(0.0, (resolved - requested).total_seconds())
    # Persist with a TARGETED add: the materialized return under run/actuation_returns/ must
    # never be committed (that is the plaintext handback).
    _save_tasks(tasks, f"actuate: sync grounded {outcome} {tid}")
    ev = (f"facts-lane resolution: {resolution.get('evidence')}" if outcome == "fulfilled"
          else f"facts-lane decline: {resolution.get('reason')}")
    _resolve_companion_bet(task.get("companion_bet"), outcome, ev)
    where = f" -> run/actuation_returns/{tid}.json" if resolution.get("return") else ""
    usab = f" [usability: {task['usability']} -- {task.get('usability_detail','')}]" \
        if task.get("usability") else ""
    # Cross-run boundary: the materialized plaintext (git-ignored) and the ephemeral decrypt key are
    # both sandbox-ephemeral, so a credential does NOT survive to the next run. Name the boundary at
    # the exact point the agent receives it: for a one-time credential the operator promotes it into
    # .env.agent out-of-band (they hold the off-repo AUDIT_DIR plaintext copy).
    persist = (" NOTE: this credential is WITHIN-RUN only (plaintext + decrypt key are "
               "sandbox-ephemeral) -- have the operator promote it into .env.agent for cross-run use."
               if outcome == "fulfilled" and task.get("return_kind") == "credential" else "")
    return f"{tid} synced from verifier facts: {outcome}{where}{usab}.{persist}"


def cmd_sync(a) -> int:
    """Agent: verify and apply the grounded resolution for one task."""
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
    try:
        print(_apply_resolution(task, tasks, resolution))
    except Exception as e:
        print(f"FATAL: {e}", file=sys.stderr)
        return 1
    if task.get("usability") == "failed":
        print(f"WARNING: {a.id} was fulfilled by the operator, but its pre-registered usability "
              "probe FAILED -- the handback does not grant working access from this sandbox "
              "(likely WAF/IP-reputation, which an operator-created account does not cure). The "
              "operator obligation is discharged; do NOT treat this credential as working access.",
              file=sys.stderr)
        return 3
    return 0


def cmd_sync_all(_a) -> int:
    """Sync every open task that now has a grounded resolution; skip those still unresolved.

    This is what the durable-wakeup handler (bin/actuate_watch.sh) runs each time it fires — a
    task with no resolution yet is a normal WAIT, not an error, so it is skipped, never fatal."""
    tasks = _load_tasks()
    opens = [t for t in tasks if t.get("status") == "open"]
    synced = 0
    unusable = 0
    for task in opens:
        try:
            resolution = _grounded_resolution(task)
        except Exception as e:
            print(f"warn: {task['id']} resolution failed verification ({e}); left open.",
                  file=sys.stderr)
            continue
        if not resolution:
            continue  # not resolved yet — a legitimate WAIT
        try:
            print(_apply_resolution(task, tasks, resolution))
            synced += 1
            if task.get("usability") == "failed":
                unusable += 1
        except Exception as e:
            print(f"warn: {task['id']} could not be applied ({e}); left open.", file=sys.stderr)
    tail = (f" ({unusable} fulfilled but the post-handback usability probe FAILED -- credential "
            "does not grant sandbox access)") if unusable else ""
    print(f"sync-all: {synced} of {len(opens)} open task(s) synced{tail}")
    return 0


def cmd_next_wakeup(_a) -> int:
    """Print the seconds until the agent should next run sync-all — sized to the soonest open
    deadline, capped at 1h so an early resolution is never missed. The durable queue (issue #20.6)
    consumes this to re-arm. No open tasks -> a long idle cadence (ACTUATE_IDLE_WAKEUP_S)."""
    opens = [t for t in _load_tasks() if t.get("status") == "open"]
    if not opens:
        try:
            idle = int(os.environ.get("ACTUATE_IDLE_WAKEUP_S", "1800"))
            print(idle if idle > 0 else 1800)
        except ValueError:
            print(1800)   # a non-numeric env override must never emit a garbage wakeup
        return 0
    now = dt.datetime.now(dt.timezone.utc)
    ttls = []
    for t in opens:
        try:
            ttls.append((_parse_iso(t["deadline"]) - now).total_seconds())
        except Exception:
            ttls.append(0.0)
    soonest = min(ttls)
    delay = max(60.0, min(3600.0, soonest if soonest > 0 else 60.0))
    print(int(delay))
    return 0


def cmd_list(_a) -> int:
    """Print all actuation tasks with status and metering."""
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
    """Print open tasks with their time-to-deadline."""
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
        if t.get("status") != "open" or t.get("id") in resolved:
            continue
        # EVERY field the agent emits into the alert line is untrusted (the agent owns the task
        # file), so scrub id/kind/gate of control chars -- a newline in ANY of them would forge a
        # second physical ALERT line. The id must also be well-formed (a real request always has an
        # ACT-NNN id); a tampered record never produces an alert. The machine fields lead the line
        # and the notifier parses them by fixed position, so free text can never override id/urgency.
        tid = _scrub(t.get("id"))
        if not re.fullmatch(r"ACT-[0-9]+", tid):   # ASCII digits only (\d would admit ٧/１２)
            continue
        try:
            ttl = int((_parse_iso(t["deadline"]) - now).total_seconds())
        except Exception:
            ttl = 0
        urgency = "URGENT" if ttl < NOTIFY_URGENT_S else "NORMAL"
        kind = _scrub(t.get("kind"))[:32]
        gate = _scrub(t.get("gate"))[:80]
        out_lines.append(f"ALERT {tid} urgency={urgency} ttl_s={ttl} kind={kind} :: {gate}")
    text = "\n".join(out_lines) + ("\n" if out_lines else "")
    if a.sink:
        Path(a.sink).write_text(text)
    sys.stdout.write(text)
    return 0


def main() -> int:
    """Parse argv and dispatch to the selected subcommand."""
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    pr = sub.add_parser("request")
    for flag in ("--kind", "--gate", "--target-url", "--identity", "--steps", "--expect",
                 "--return-kind", "--deadline", "--test", "--ev"):
        pr.add_argument(flag, required=True, dest=flag.lstrip("-").replace("-", "_"))
    pr.add_argument("--artifact", default="")
    pr.add_argument("--verify-cmd", dest="verify_cmd", default="",
                    help="pre-registered post-handback usability probe (shell); exit 0 = the "
                         "returned credential grants working sandbox access. Env: ACTUATE_RETURN_FILE, "
                         "ACTUATE_RETURN_VALUE, ACTUATE_TASK_ID")
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
    pf.add_argument("--consent-ruling", dest="consent_ruling", default="",
                    help="required P3 name-test ruling when fulfilling a money-moving kind")
    pf.set_defaults(fn=cmd_fulfill)

    pd = sub.add_parser("decline")
    pd.add_argument("id")
    pd.add_argument("--minutes", type=float, required=True)
    pd.add_argument("--reason", required=True)
    pd.set_defaults(fn=cmd_decline)

    pw = sub.add_parser("withdraw")
    pw.add_argument("id")
    pw.add_argument("--reason", required=True)
    pw.set_defaults(fn=cmd_withdraw)

    ps = sub.add_parser("sync")
    ps.add_argument("id")
    ps.set_defaults(fn=cmd_sync)

    sub.add_parser("sync-all").set_defaults(fn=cmd_sync_all)
    sub.add_parser("next-wakeup").set_defaults(fn=cmd_next_wakeup)

    pn = sub.add_parser("notify-scan")
    pn.add_argument("--sink", default="")
    pn.set_defaults(fn=cmd_notify_scan)

    sub.add_parser("list").set_defaults(fn=cmd_list)
    sub.add_parser("due").set_defaults(fn=cmd_due)

    a = p.parse_args()
    return a.fn(a)


if __name__ == "__main__":
    raise SystemExit(main())

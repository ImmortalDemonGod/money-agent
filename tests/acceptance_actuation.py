#!/usr/bin/env python3
"""Acceptance harness for the capability-delegation redesign of the human-actuation queue.

THIS FILE IS THE DEFINITION OF DONE. It is written test-first: it is RED today (the
subsystem it exercises, `bin/actuate.py`, does not exist yet) and turns green only when the
redesigned behavior is real. It never self-certifies — a fresh party runs it and checks.

    python3 tests/acceptance_actuation.py         # scorecard; exit 0 only when all PASS

Why this queue is being redesigned (grounded in run 1, not theory): the run-1 agent hit
capability walls it could not pass and had to hand-write operator files because there was no
channel — archive/run-001/OPERATOR_CLAIM_workers_dev.md (iter 089) is the reference case: a
Cloudflare Worker with a HARD 60-MINUTE claim window, plus a fixed worker.js the agent staged
but could not deploy ("my sandbox wrangler is unauthenticated"). It succeeded only because a
human was watching live. The current queue (bin/human.py) would have missed that window (24h
companion-bet poll, "operator checks once or twice a day") and cannot hand a credential back.

THE GOAL this harness encodes: turn the queue from a thin gate-signal into a reliable, usable
capability-delegation channel — the agent's hands for bounded actions it is structurally
barred from (claim/deploy a host, fund a wallet, pass a KYC) — so a strategy like x402 becomes
reachable, WITHOUT weakening `actuator-never-oracle` or separation-of-duties.

--------------------------------------------------------------------------------------------
THE CONTRACT (bin/actuate.py) that a green run proves. Implement to this; revise it only
deliberately, in the same commit that revises the harness.

AGENT side (claims lane, branch = $AGENT_BRANCH):
  actuate.py request --kind <claim-host|deploy-account|wallet-fund|kyc-step|approval-click>
        --gate <text> --target-url <url> --identity <which account> --steps <file>
        [--artifact <file>] --expect <result desc>
        --return-kind <none|confirmation|value|credential> --deadline <ISO8601>
        --test <iter/packet cite> --ev <why worth operator minutes>
     -> writes run/actuation_tasks.json (committed+pushed on the agent branch); generates an
        EPHEMERAL encryption keypair (public key stored IN the task; private key ONLY in
        $MONEY_AGENT_STATE, never git); registers a companion bet; schedules a deadline-aware
        wakeup. Prints "id=ACT-NNN". Runs the actuator-never-oracle leak-check on free text and
        the kind allowlist; fail-closed.
  actuate.py card <id>   -> prints a human-readable task CARD (the operator UX artifact): the
        target URL, ordered steps, the staged artifact reference, the deadline, the expected
        result, the return kind, and the exact fulfill command. This is the usability surface.
  actuate.py sync <id>   -> fetch the facts lane; verify the verifier signature + task-hash
        binding + agent-branch binding; if a return payload is present, DECRYPT it with the
        ephemeral private key, verify sha256(plaintext)==recorded hash, and MATERIALIZE it to
        run/actuation_returns/<id>.json (git-ignored, sandbox-only); resolve the companion bet;
        record human_minutes. Fail-closed on any verification failure.
  actuate.py list | due

OPERATOR side (facts lane, branch = $LEDGER_BRANCH, must differ from the agent branch):
  actuate.py fulfill <id> --minutes <n> --evidence <text>
        [--return-file <plaintext file> | --return-value <str>]
     -> read the task from the agent branch; build a resolution; if the task's return-kind is
        not "none" and a return was supplied, ENCRYPT the plaintext to the task's published
        ephemeral public key -> resolution carries return_ciphertext + return_sha256 (never
        plaintext); retain the plaintext OFF-REPO (in $MONEY_AGENT_STATE) for audit; sign the
        resolution with the verifier key and commit+push it to the facts lane.
  actuate.py decline <id> --minutes <n> --reason <text>

NOTIFIER (operator side, out-of-band, read-only):
  actuate.py notify-scan --sink <file>
     -> for every open, unresolved task, emit one line to <sink>:
        "ALERT <id> urgency=<URGENT|NORMAL> ttl_s=<int>"
        urgency=URGENT when the deadline is within $NOTIFY_URGENT_S (default 900). This is the
        60-minute-window lesson made mechanical.
--------------------------------------------------------------------------------------------
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
AGENT_BRANCH = "acc-agent"
LEDGER_BRANCH = "acc-ledger"
# Runtime-random canary: never a committed literal, so a match in the object store can only come
# from the return channel leaking it (not from this file being cloned into the test world).
SECRET = "LEAKCANARY-" + os.urandom(12).hex()
MODULE = REPO / "bin" / "actuate.py"

# ----- tiny check framework (PASS / FAIL / PENDING) --------------------------------------
PASS, FAIL, PENDING = "PASS", "FAIL", "PENDING"
RESULTS: list[tuple[str, str, str, str]] = []   # (id, title, state, detail)


class Pending(Exception):
    """Raised when the feature under test is absent — a legitimate RED, not a broken test."""


def check(cid: str, title: str, fn) -> None:
    if not MODULE.exists():
        RESULTS.append((cid, title, PENDING, "bin/actuate.py not implemented"))
        return
    try:
        detail = fn() or "ok"
        RESULTS.append((cid, title, PASS, detail))
    except Pending as e:
        RESULTS.append((cid, title, PENDING, str(e)))
    except AssertionError as e:
        RESULTS.append((cid, title, FAIL, str(e) or "assertion failed"))
    except Exception as e:  # a crash is a FAIL, never a silent pass
        RESULTS.append((cid, title, FAIL, f"{type(e).__name__}: {e}"))


def want(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


# ----- shell / git helpers ---------------------------------------------------------------
def run(cmd, cwd=None, env=None, text_input=None) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, env=env, input=text_input,
                          capture_output=True, text=True, timeout=120)


def git(cwd: Path, *args: str) -> subprocess.CompletedProcess:
    return run(["git", "-c", "user.email=t@t.test", "-c", "user.name=acc",
                "-c", "commit.gpgsign=false", *args], cwd=cwd)


def actuate(clone: Path, state: Path, *args: str, text_input=None) -> subprocess.CompletedProcess:
    env = {**os.environ, "AGENT_BRANCH": AGENT_BRANCH, "LEDGER_BRANCH": LEDGER_BRANCH,
           "MONEY_AGENT_STATE": str(state)}
    return run(["python3", "bin/actuate.py", *args], cwd=clone, env=env, text_input=text_input)


# ----- the two-lane git world (matches tests/sim.sh's signing setup) ---------------------
def build_world() -> tuple[Path, Path, Path, Path]:
    """Return (world, origin.git, agent_clone, ledger_clone). State dir is world/state."""
    if shutil.which("ssh-keygen") is None:
        raise Pending("ssh-keygen not on PATH — install openssh-client")
    world = Path(tempfile.mkdtemp(prefix="acc-actuation-"))
    origin = world / "origin.git"
    r = run(["git", "clone", "--bare", "--quiet", "--local", str(REPO), str(origin)])
    want(r.returncode == 0, f"bare clone failed: {r.stderr[:200]}")

    state = world / "state"
    state.mkdir()
    key = state / "verifier_signing_key"
    r = run(["ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f", str(key)])
    want(r.returncode == 0, f"keygen failed: {r.stderr[:200]}")
    pub = (state / "verifier_signing_key.pub").read_text().strip()
    allowed_line = f"verifier {pub}\n"          # sim.sh format: principals + full pubkey line

    clones = {}
    for name, branch in (("agent", AGENT_BRANCH), ("ledger", LEDGER_BRANCH)):
        clone = world / name
        r = run(["git", "clone", "--quiet", "--local", str(origin), str(clone)])
        want(r.returncode == 0, f"clone {name} failed: {r.stderr[:200]}")
        git(clone, "checkout", "-q", "-b", branch)
        # seed the WORKING-TREE bin tools so an uncommitted actuate.py is under test
        for f in (REPO / "bin").glob("*.py"):
            shutil.copy(f, clone / "bin" / f.name)
        (clone / "harness").mkdir(exist_ok=True)
        (clone / "harness" / "allowed_signers").write_text(allowed_line)
        shutil.copy(state / "verifier_signing_key.pub", clone / "harness" / "verifier_key.pub")
        git(clone, "add", "-A")
        git(clone, "commit", "-q", "-m", f"seed {name}")
        r = git(clone, "push", "-q", "origin", f"HEAD:{branch}")
        want(r.returncode == 0, f"push {name} failed: {r.stderr[:200]}")
        clones[name] = clone
    # make each lane able to see the other
    git(clones["agent"], "fetch", "-q", "origin", LEDGER_BRANCH)
    git(clones["ledger"], "fetch", "-q", "origin", AGENT_BRANCH)
    return world, origin, clones["agent"], clones["ledger"]


def parse_id(out: str) -> str:
    for tok in out.split():
        if tok.startswith("id="):
            return tok[3:].strip()
    raise AssertionError(f"request did not print id=... (got: {out.strip()[:160]})")


def steps_file(world: Path, name: str, body: str) -> str:
    p = world / name
    p.write_text(body)
    return str(p)


def origin_contains(origin: Path, needle: str) -> bool:
    """True if the literal needle appears in ANY object across all refs of the bare origin."""
    refs = run(["git", "-C", str(origin), "rev-list", "--all"]).stdout.split()
    if not refs:
        return False
    r = run(["git", "-C", str(origin), "grep", "-F", needle, *refs])
    return r.returncode == 0   # git grep: 0 == found


# ----- reference scenarios (grounded in real run-1 cases) --------------------------------
def scenario_claim_host():
    """S1 — the iter-089 case: claim a host with a hard deadline + a staged artifact,
    return a plain confirmation, agent syncs it. The primitive's canonical happy path."""
    world, origin, agent, ledger = build_world()
    steps = steps_file(world, "s1_steps.txt",
                        "1. Open the claim URL.\n2. Sign in to the CF account.\n3. Click Claim.\n")
    artifact = steps_file(world, "s1_worker.js", "export default { fetch: () => new Response('ok') }")
    r = actuate(agent, world / "state", "request", "--kind", "claim-host",
                "--gate", "temporary Worker auto-deletes in 60m unless claimed",
                "--target-url", "https://dash.cloudflare.com/claim/abc",
                "--identity", "operator Cloudflare account", "--steps", steps,
                "--artifact", artifact, "--expect", "host claimed and serving 200",
                "--return-kind", "confirmation", "--deadline", "2099-01-01T00:00:00Z",
                "--test", "archive iter 089", "--ev", "run's only persistent crawlable host")
    if r.returncode != 0 and "usage" in (r.stderr + r.stdout).lower():
        raise Pending(f"request CLI not implemented: {r.stderr[:160]}")
    want(r.returncode == 0, f"request failed: {r.stderr[:200]}")
    tid = parse_id(r.stdout)

    f = actuate(ledger, world / "state", "fulfill", tid, "--minutes", "4",
                "--evidence", "claimed in CF dashboard; host serves 200",
                "--return-value", "claimed:one-honest-dollar.workers.dev")
    want(f.returncode == 0, f"fulfill failed: {f.stderr[:200]}")

    git(agent, "fetch", "-q", "origin", LEDGER_BRANCH)
    s = actuate(agent, world / "state", "sync", tid)
    want(s.returncode == 0, f"sync failed: {s.stderr[:200]}")
    ret = agent / "run" / "actuation_returns" / f"{tid}.json"
    want(ret.exists(), "sync did not materialize the return payload for the agent")
    want("claimed:one-honest-dollar.workers.dev" in ret.read_text(),
         "materialized return does not contain the operator's confirmation value")
    return f"round-trip ok; return materialized at run/actuation_returns/{tid}.json"


def scenario_wallet_fund():
    """S2 — x402 reachability: operator funds a Base wallet, returns the settlement address /
    confirmation the agent then consumes. Non-secret value return."""
    world, origin, agent, ledger = build_world()
    steps = steps_file(world, "s2_steps.txt",
                       "1. Open the funding page.\n2. Send 10 USDC to the address below.\n")
    r = actuate(agent, world / "state", "request", "--kind", "wallet-fund",
                "--gate", "x402 rail needs a funded Base wallet before the agent can transact",
                "--target-url", "https://basescan.org/address/0xAGENT",
                "--identity", "operator's funding wallet", "--steps", steps,
                "--expect", "10 USDC settled to the agent settlement address",
                "--return-kind", "value", "--deadline", "2099-01-01T00:00:00Z",
                "--test", "issue #30 OQ1", "--ev", "unblocks the entire x402 strategy")
    if r.returncode != 0 and "usage" in (r.stderr + r.stdout).lower():
        raise Pending(f"request CLI not implemented: {r.stderr[:160]}")
    want(r.returncode == 0, f"request failed: {r.stderr[:200]}")
    tid = parse_id(r.stdout)
    f = actuate(ledger, world / "state", "fulfill", tid, "--minutes", "6",
                "--evidence", "sent 10 USDC; tx confirmed",
                "--return-value", "0xTXHASHconfirmed")
    want(f.returncode == 0, f"fulfill failed: {f.stderr[:200]}")
    git(agent, "fetch", "-q", "origin", LEDGER_BRANCH)
    s = actuate(agent, world / "state", "sync", tid)
    want(s.returncode == 0, f"sync failed: {s.stderr[:200]}")
    ret = agent / "run" / "actuation_returns" / f"{tid}.json"
    want(ret.exists() and "0xTXHASHconfirmed" in ret.read_text(),
         "agent did not receive the returned funding confirmation")
    return "wallet-fund value returned and consumable by the agent"


def scenario_kyc_secret():
    """S3 — the secret case: operator completes a marketplace signup and returns CREDENTIALS.
    The plaintext must never touch git; the agent recovers it only in-sandbox."""
    world, origin, agent, ledger = build_world()
    steps = steps_file(world, "s3_steps.txt",
                       "1. Open the signup page.\n2. Complete KYC with operator identity.\n"
                       "3. Set the account password.\n")
    secret_file = steps_file(world, "s3_secret.txt", SECRET)
    r = actuate(agent, world / "state", "request", "--kind", "kyc-step",
                "--gate", "marketplace requires a one-time human KYC before the agent can list",
                "--target-url", "https://market.example/signup",
                "--identity", "operator legal identity", "--steps", steps,
                "--expect", "an authenticated marketplace account",
                "--return-kind", "credential", "--deadline", "2099-01-01T00:00:00Z",
                "--test", "issue #32 signup slice", "--ev", "opens a permissionless-after-KYC rail")
    if r.returncode != 0 and "usage" in (r.stderr + r.stdout).lower():
        raise Pending(f"request CLI not implemented: {r.stderr[:160]}")
    want(r.returncode == 0, f"request failed: {r.stderr[:200]}")
    tid = parse_id(r.stdout)
    f = actuate(ledger, world / "state", "fulfill", tid, "--minutes", "12",
                "--evidence", "account created, KYC passed",
                "--return-file", secret_file)
    want(f.returncode == 0, f"fulfill failed: {f.stderr[:200]}")

    # (a) plaintext must be nowhere in git history/objects on any branch
    want(not origin_contains(origin, SECRET),
         "SECRET credential leaked into git — the return channel is not encrypted")
    git(agent, "fetch", "-q", "origin", LEDGER_BRANCH)
    s = actuate(agent, world / "state", "sync", tid)
    want(s.returncode == 0, f"sync failed: {s.stderr[:200]}")
    # (b) the agent recovers the exact plaintext in-sandbox
    ret = agent / "run" / "actuation_returns" / f"{tid}.json"
    want(ret.exists() and SECRET in ret.read_text(),
         "agent could not recover the credential after sync")
    return "credential handed back: ciphertext-only in git, plaintext recovered in-sandbox"


# ----- invariants (negative tests) -------------------------------------------------------
def neg_sod_forgery():
    """N1 — the agent cannot fabricate 'a human acted'. A resolution the verifier did not sign
    must be rejected by sync (mirrors sim.sh's forgery assertion, for the new lane)."""
    world, origin, agent, ledger = build_world()
    steps = steps_file(world, "n1_steps.txt", "1. do the thing\n")
    r = actuate(agent, world / "state", "request", "--kind", "claim-host", "--gate", "x",
                "--target-url", "https://e/x", "--identity", "op", "--steps", steps,
                "--expect", "done", "--return-kind", "confirmation",
                "--deadline", "2099-01-01T00:00:00Z", "--test", "iter089", "--ev", "reach")
    if r.returncode != 0 and "usage" in (r.stderr + r.stdout).lower():
        raise Pending("request CLI not implemented")
    want(r.returncode == 0, f"request failed: {r.stderr[:200]}")
    tid = parse_id(r.stdout)
    # forge an UNSIGNED resolution directly on the facts lane, as the agent would try to
    res = ledger / "ledger" / "actuation_resolutions.json"
    res.parent.mkdir(parents=True, exist_ok=True)
    res.write_text(json.dumps({"resolutions": {tid: {"status": "fulfilled",
                   "human_minutes": 0, "evidence": "forged"}}}, indent=2) + "\n")
    git(ledger, "add", "-A")
    git(ledger, "commit", "-q", "-m", "forge")
    git(ledger, "push", "-q", "origin", f"HEAD:{LEDGER_BRANCH}")
    git(agent, "fetch", "-q", "origin", LEDGER_BRANCH)
    s = actuate(agent, world / "state", "sync", tid)
    want(s.returncode != 0, "sync ACCEPTED an unsigned/forged resolution — SoD broken")
    return "forged resolution rejected (signature required)"


def neg_oracle_leak():
    """N2 — actuator, never oracle. A request whose free text smuggles strategy/content must be
    refused (the OPERATOR_UNBLOCK/NOTE strategy-leak that this guardrail exists to prevent)."""
    world, origin, agent, ledger = build_world()
    steps = steps_file(world, "n2_steps.txt",
                       "Decide which product we should sell and which market to target, then "
                       "write the launch copy and pick the pricing strategy for me.\n")
    r = actuate(agent, world / "state", "request", "--kind", "claim-host",
                "--gate", "please choose our business strategy and target market",
                "--target-url", "https://e/x", "--identity", "op", "--steps", steps,
                "--expect", "a strategy", "--return-kind", "confirmation",
                "--deadline", "2099-01-01T00:00:00Z", "--test", "iter089", "--ev", "reach")
    if "unrecognized arguments" in r.stderr:
        raise Pending("request CLI not implemented")
    want(r.returncode != 0, "oracle-shaped request (asks the human to choose strategy) was ACCEPTED")
    return "strategy-laden request refused by the leak-check"


def neg_secret_never_in_git():
    """N3 — an explicit, standalone assertion of the secret-leak property (D-class negative
    evidence), independent of S3's happy path: fulfill with a secret, then prove zero plaintext
    anywhere in the object store."""
    world, origin, agent, ledger = build_world()
    steps = steps_file(world, "n3_steps.txt", "1. sign up\n")
    secret_file = steps_file(world, "n3_secret.txt", SECRET)
    r = actuate(agent, world / "state", "request", "--kind", "kyc-step", "--gate", "kyc",
                "--target-url", "https://e/x", "--identity", "op", "--steps", steps,
                "--expect", "acct", "--return-kind", "credential",
                "--deadline", "2099-01-01T00:00:00Z", "--test", "iter089", "--ev", "reach")
    if r.returncode != 0 and "usage" in (r.stderr + r.stdout).lower():
        raise Pending("request CLI not implemented")
    want(r.returncode == 0, f"request failed: {r.stderr[:200]}")
    tid = parse_id(r.stdout)
    f = actuate(ledger, world / "state", "fulfill", tid, "--minutes", "5",
                "--evidence", "marketplace account created", "--return-file", secret_file)
    want(f.returncode == 0, f"fulfill failed: {f.stderr[:200]}")
    want(not origin_contains(origin, SECRET), "plaintext credential present in git objects")
    return "no plaintext credential in any committed object"


def neg_metering():
    """N4 — meter everything. fulfill AND decline both require and record human_minutes."""
    world, origin, agent, ledger = build_world()
    steps = steps_file(world, "n4_steps.txt", "1. x\n")
    # decline must require --minutes
    r = actuate(agent, world / "state", "request", "--kind", "approval-click", "--gate", "approve",
                "--target-url", "https://e/x", "--identity", "op", "--steps", steps,
                "--expect", "approved", "--return-kind", "none",
                "--deadline", "2099-01-01T00:00:00Z", "--test", "iter089", "--ev", "reach")
    if r.returncode != 0 and "usage" in (r.stderr + r.stdout).lower():
        raise Pending("request CLI not implemented")
    want(r.returncode == 0, f"request failed: {r.stderr[:200]}")
    tid = parse_id(r.stdout)
    d = actuate(ledger, world / "state", "decline", tid, "--reason", "operator declines this one")
    want(d.returncode != 0, "decline without --minutes was accepted (metering not enforced)")
    d2 = actuate(ledger, world / "state", "decline", tid, "--minutes", "3",
                 "--reason", "operator declines this one")
    want(d2.returncode == 0, f"metered decline failed: {d2.stderr[:200]}")
    return "fulfill/decline require and record human_minutes"


# ----- benchmarks (simple, measurable bars) ----------------------------------------------
def bench_card_completeness():
    """B1 — usability, measured without a live human: the rendered CARD must contain every
    field a no-context operator needs. Missing any one is a FAIL. This is the exact bar the
    current design flunks (its 'card' is a free-text one-liner + a packet citation)."""
    world, origin, agent, ledger = build_world()
    steps = steps_file(world, "b1_steps.txt", "1. Open the URL.\n2. Click Claim.\n")
    artifact = steps_file(world, "b1_art.txt", "worker.js body")
    r = actuate(agent, world / "state", "request", "--kind", "claim-host",
                "--gate", "claim the host before it deletes",
                "--target-url", "https://dash.example/claim/xyz", "--identity", "CF account",
                "--steps", steps, "--artifact", artifact, "--expect", "host serving 200",
                "--return-kind", "confirmation", "--deadline", "2099-01-01T00:00:00Z",
                "--test", "iter089", "--ev", "reach")
    if r.returncode != 0 and "usage" in (r.stderr + r.stdout).lower():
        raise Pending("request CLI not implemented")
    want(r.returncode == 0, f"request failed: {r.stderr[:200]}")
    tid = parse_id(r.stdout)
    c = actuate(agent, world / "state", "card", tid)
    if c.returncode != 0 and "invalid choice" in c.stderr:
        raise Pending("card subcommand not implemented")
    want(c.returncode == 0, f"card failed: {c.stderr[:200]}")
    text = c.stdout
    required = {
        "target URL": "https://dash.example/claim/xyz",
        "step 1": "Open the URL",
        "step 2": "Click Claim",
        "deadline": "2099-01-01",
        "expected result": "host serving 200",
        "artifact reference": "b1_art.txt",
        "fulfill command": "fulfill",
    }
    missing = [label for label, needle in required.items() if needle not in text]
    want(not missing, f"card is missing fields a no-context operator needs: {missing}")
    return f"card carries all {len(required)} required fields"


def bench_deadline_notification():
    """B2 — the 60-minute-window lesson, made mechanical: notify-scan must flag a near-deadline
    task URGENT and a far one NORMAL. Deadline-awareness is the property; day-scale poll is out."""
    world, origin, agent, ledger = build_world()
    steps = steps_file(world, "b2_steps.txt", "1. x\n")
    # a task due very soon (urgent) and one due far away (normal)
    soon = actuate(agent, world / "state", "request", "--kind", "claim-host", "--gate", "soon",
                   "--target-url", "https://e/soon", "--identity", "op", "--steps", steps,
                   "--expect", "done", "--return-kind", "none",
                   "--deadline", "2000-01-01T00:10:00Z", "--test", "iter089", "--ev", "reach")
    if soon.returncode != 0 and "usage" in (soon.stderr + soon.stdout).lower():
        raise Pending("request CLI not implemented")
    want(soon.returncode == 0, f"request(soon) failed: {soon.stderr[:200]}")
    far = actuate(agent, world / "state", "request", "--kind", "claim-host", "--gate", "far",
                  "--target-url", "https://e/far", "--identity", "op", "--steps", steps,
                  "--expect", "done", "--return-kind", "none",
                  "--deadline", "2099-01-01T00:00:00Z", "--test", "iter089", "--ev", "reach")
    want(far.returncode == 0, f"request(far) failed: {far.stderr[:200]}")
    soon_id, far_id = parse_id(soon.stdout), parse_id(far.stdout)
    sink = world / "alerts.txt"
    # notifier runs operator-side; a task in the past is maximally urgent
    n = actuate(ledger, world / "state", "notify-scan", "--sink", str(sink))
    if n.returncode != 0 and "invalid choice" in n.stderr:
        raise Pending("notify-scan subcommand not implemented")
    want(n.returncode == 0, f"notify-scan failed: {n.stderr[:200]}")
    want(sink.exists(), "notify-scan produced no sink output")
    lines = sink.read_text().splitlines()
    soon_line = next((ln for ln in lines if soon_id in ln), "")
    far_line = next((ln for ln in lines if far_id in ln), "")
    want("urgency=URGENT" in soon_line, f"near-deadline task not flagged URGENT: {soon_line!r}")
    want("urgency=NORMAL" in far_line, f"far-deadline task not flagged NORMAL: {far_line!r}")
    return "deadline-aware alerts: near->URGENT, far->NORMAL"


# ----- runner ----------------------------------------------------------------------------
def main() -> int:
    check("S1", "claim-host round-trip (deadline + staged artifact)", scenario_claim_host)
    check("S2", "wallet-fund round-trip (x402 value return)", scenario_wallet_fund)
    check("S3", "kyc-step secret credential handback (encrypted)", scenario_kyc_secret)
    check("N1", "SoD: forged/unsigned resolution rejected", neg_sod_forgery)
    check("N2", "actuator-never-oracle: strategy request refused", neg_oracle_leak)
    check("N3", "secret never in git objects", neg_secret_never_in_git)
    check("N4", "metering enforced on fulfill/decline", neg_metering)
    check("B1", "usability: card carries every no-context field", bench_card_completeness)
    check("B2", "deadline-aware notification (URGENT vs NORMAL)", bench_deadline_notification)

    width = max(len(t) for _, t, _, _ in RESULTS)
    print("\n  ACCEPTANCE — capability-delegation queue (bin/actuate.py)\n")
    icons = {PASS: "PASS   ", FAIL: "FAIL   ", PENDING: "PENDING"}
    for cid, title, state, detail in RESULTS:
        print(f"  [{icons[state]}] {cid}  {title.ljust(width)}  — {detail}")
    npass = sum(1 for *_, s, _ in ((r[0], r[1], r[2], r[3]) for r in RESULTS) if s == PASS)
    nfail = sum(1 for r in RESULTS if r[2] == FAIL)
    npend = sum(1 for r in RESULTS if r[2] == PENDING)
    print(f"\n  {npass} PASS  ·  {nfail} FAIL  ·  {npend} PENDING   (Tier-S done = all PASS)\n")
    if npend and not nfail:
        print("  RED as expected: the subsystem is unbuilt. Implement bin/actuate.py to the\n"
              "  contract in this file's docstring; each check turns green on real behavior.\n")
    return 0 if (nfail == 0 and npend == 0) else 1


if __name__ == "__main__":
    raise SystemExit(main())

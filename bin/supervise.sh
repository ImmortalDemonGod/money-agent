#!/usr/bin/env bash
# The WATCH layer. Run once per /loop wake by the assistant. Prints a one-screen status and an
# explicit VERDICT line the assistant reads to decide: keep waiting, restart the verifier, or
# ALERT THE OPERATOR (first dollar / dead verifier).
#
#   bin/supervise.sh <agent-branch>        # facts + claims-lane human requests
#   AGENT_BRANCH=run-2 LEDGER_BRANCH=ledger-run2 bin/supervise.sh
#
# It does NOT do the verification (verifier_loop.sh does). It answers: is the verifier alive, is
# truth.json fresh, is the push working, and HAS THE FIRST DOLLAR ARRIVED. That last one is the
# run's end condition and the whole reason a human is kept in the loop.
set -uo pipefail
R="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; cd "$R" || exit 1
LEDGER_BRANCH="${LEDGER_BRANCH:-ledger}"
AGENT_BRANCH="${1:-${AGENT_BRANCH:-}}"
now=$(date -u +%s)

echo "===== VERIFIER SUPERVISOR @ $(date -u +%H:%M:%SZ) ====="

# 1. is the verifier process alive?
alive=0
VPID=$(pgrep -f "bash.*bin/verifier_loop.sh" | head -1)
if [[ -n "$VPID" ]]; then
  alive=1; echo "process    : ALIVE (pid $VPID, launchd)"
else
  echo "process    : DEAD (launchd should auto-respawn; check launchctl before any manual action)"
fi

# 2. pull the latest verifier-published ledger from the FACTS lane (v2 two-lane; the v1 read of
# the agent's branch is the stale-claims-lane bug class, instance #3 caught by the entry-006 audit)
git fetch -q origin "$LEDGER_BRANCH" 2>/dev/null || true
T=$(git show "origin/$LEDGER_BRANCH:ledger/truth.json" 2>/dev/null || cat ledger/truth.json 2>/dev/null)
if [[ -z "$T" ]]; then
  echo "ledger     : UNREADABLE"; echo "VERDICT    : INVESTIGATE (no truth.json)"; exit 0
fi
# Parse via STDIN, never by interpolating the ledger into python source: truth.json is
# agent-writable when the remote read fails, and a crafted string could break the literal and run
# code on the supervisor host (CodeRabbit). A parse failure is UNREADABLE, not a silent OK.
parsed="$(printf '%s' "$T" | python3 -c 'import json,sys
d=json.load(sys.stdin)
print(d.get("received_usd",0), d.get("verified"), d.get("computed_at",""))' 2>/dev/null)" \
  || { echo "ledger     : UNREADABLE (parse failed)"; echo "VERDICT    : INVESTIGATE (unparseable truth.json)"; exit 0; }
read -r RECV VERIF CA <<<"$parsed"

# 3. freshness
age="?"
if [[ -n "${CA:-}" ]]; then
  ct=$(python3 -c "import datetime as d;print(int(d.datetime.fromisoformat('$CA'.replace('Z','+00:00')).timestamp()))" 2>/dev/null || echo 0)
  age=$(( now - ct ))
fi
echo "ledger age : ${age}s   verified=$VERIF   received=\$$RECV"

# 3b. the verified-edge rail, if it has ever published (same stdin discipline)
E=$(git show "origin/$LEDGER_BRANCH:ledger/edge.json" 2>/dev/null || cat ledger/edge.json 2>/dev/null)
EVERDICT=""
if [[ -n "$E" ]]; then
  EVERDICT=$(printf '%s' "$E" | python3 -c "
import json,sys
d=json.load(sys.stdin)
print(d.get('verdict',''))" 2>/dev/null)
  [[ -n "$EVERDICT" && "$EVERDICT" != "NONE" ]] && echo "edge rail  : $EVERDICT"
fi

# 3c. #46: facts commits that never reached origin -- a long-offline verifier writing locally is
# invisible on every other line here, and its raw pulls are at risk until they land. Only
# meaningful when this checkout IS the facts lane (the verifier machine); elsewhere it stays quiet.
if [[ "$(git branch --show-current 2>/dev/null)" == "$LEDGER_BRANCH" ]] \
   && git rev-parse -q --verify "origin/$LEDGER_BRANCH" >/dev/null 2>&1; then
  UNPUSHED=$(git rev-list --count "origin/$LEDGER_BRANCH..HEAD" 2>/dev/null || echo 0)
  if [[ "${UNPUSHED:-0}" -gt 0 ]]; then
    echo "facts lane : $UNPUSHED unpushed local commit(s) -- push failing? pulls at risk until they land"
  fi
fi

# 3d. #31: requests live on the AGENT branch; operator resolutions live on the FACTS branch.
# Read both refs explicitly. Looking at this verifier checkout's working tree made the queue
# invisible in the very topology supervise exists for, and the old simulation accidentally ran
# this command from the agent clone.
if [[ -z "$AGENT_BRANCH" ]]; then
  echo "human queue: UNKNOWN (pass <agent-branch> or set AGENT_BRANCH)"
else
  git fetch -q origin "$AGENT_BRANCH" 2>/dev/null || true
  HQ=$(python3 - "$R" "$AGENT_BRANCH" "$LEDGER_BRANCH" <<'PY' 2>/dev/null
import datetime as dt, json, pathlib, subprocess, sys, tempfile
repo, agent, ledger = sys.argv[1:]
def show_raw(ref, path):
    r = subprocess.run(["git", "show", f"origin/{ref}:{path}"], cwd=repo,
                       capture_output=True, text=True)
    if r.returncode != 0:
        return None
    return r.stdout
def show(ref, path):
    raw = show_raw(ref, path)
    return None if raw is None else json.loads(raw)
try:
    task_doc = show(agent, "run/human_tasks.json")
    if task_doc is None:
        print("no requests recorded")
        raise SystemExit
    resolution_raw = show_raw(ledger, "ledger/human_resolutions.json")
    if resolution_raw is None:
        resolutions = {}
    else:
        allowed = show_raw(agent, "harness/allowed_signers")
        signature = show_raw(ledger, "ledger/human_resolutions.json.sig")
        if not allowed or not signature:
            raise RuntimeError("human resolutions are unsigned or signer policy is missing")
        with tempfile.TemporaryDirectory() as td:
            d = pathlib.Path(td)
            (d / "allowed").write_text(allowed)
            (d / "sig").write_text(signature)
            verified = subprocess.run(
                ["ssh-keygen", "-Y", "verify", "-f", str(d / "allowed"), "-I", "verifier",
                 "-n", "money-agent-ledger", "-s", str(d / "sig")],
                input=resolution_raw, text=True, capture_output=True)
        if verified.returncode != 0:
            raise RuntimeError("human-resolution signature verification failed")
        resolutions = json.loads(resolution_raw).get("resolutions", {})
    open_tasks = [t for t in task_doc.get("tasks", []) if t.get("status") == "open"]
    pending = [t for t in open_tasks if t.get("id") not in resolutions]
    awaiting = [t for t in open_tasks if t.get("id") in resolutions]
    if not open_tasks:
        print("clear")
    else:
        oldest = min(t["requested_at"] for t in open_tasks)
        age_h = (dt.datetime.now(dt.timezone.utc)
                 - dt.datetime.fromisoformat(oldest.replace("Z", "+00:00"))).total_seconds()/3600
        print(f"{len(pending)} awaiting operator, {len(awaiting)} resolved-awaiting-agent-sync, "
              f"oldest {age_h:.1f}h")
except Exception as e:
    print(f"UNREADABLE ({type(e).__name__}: {e})")
PY
)
  echo "human queue: ${HQ:-UNREADABLE}"
fi

# 4. recent push activity from the log
echo "last log   : $(tail -1 "$R/verifier.log" 2>/dev/null || echo '(no log)')"

# ---- VERDICT (the line the assistant acts on) ----
if python3 -c "import sys; sys.exit(0 if float('$RECV')>0 else 1)" 2>/dev/null; then
  echo "VERDICT    : ⭐ FIRST DOLLAR RECEIVED (\$$RECV). RUN OVER. ALERT THE OPERATOR NOW."
elif [[ "$EVERDICT" == "VERIFIED_POSITIVE_EV" ]]; then
  echo "VERDICT    : ⭐ EDGE VERIFIED POSITIVE-EV. The variant experiment is answered. ALERT THE"
  echo "             OPERATOR NOW -- real-capital deployment is a human decision, never the agent's."
elif [[ "$HQ" =~ ^[1-9][0-9]*\ awaiting\ operator ]]; then
  echo "VERDICT    : HUMAN ACTUATION REQUIRED -- $HQ"
elif [[ "$HQ" =~ ,\ [1-9][0-9]*\ resolved-awaiting-agent-sync ]]; then
  echo "VERDICT    : AGENT SYNC REQUIRED -- $HQ"
elif [[ "$alive" -eq 0 ]]; then
  echo "VERDICT    : RESTART -- verifier process is dead. Run bin/start_verifier.sh <agent-branch>"
elif [[ "$age" != "?" && "$age" -gt 1500 ]]; then
  echo "VERDICT    : STALE (${age}s > 1500s) -- verifier alive but not publishing. Check verifier.log."
else
  echo "VERDICT    : OK -- verifier live, ledger fresh, no money yet. Keep watching."
fi

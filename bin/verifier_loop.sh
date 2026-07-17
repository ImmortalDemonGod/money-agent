#!/usr/bin/env bash
# THE VERIFIER (v2, two-lane). Runs on the operator's machine. NEVER in the sandbox.
#
# v1 published truth.json onto the AGENT'S branch, which forced a `git reset --hard` of the shared
# worktree every cycle -- the single most damaging harness defect of run 1: it destroyed agent
# evidence at least six documented times (wiped SENT_LOG/MONEY_LOG appends, lost iteration numbers,
# an empty commit that looked successful, a mid-deploy wipe). v2 separates the lanes:
#
#   FACTS lane : this loop commits ledger/{truth.json, raw/, MANIFEST, baseline copy} to a
#                dedicated LEDGER branch from the verifier's own checkout. Heartbeats live here.
#   CLAIMS lane: the agent's branch. This loop NEVER checks it out, resets it, or writes to it.
#
# The agent reads facts via bin/truth.py (fetch + `git show origin/<ledger>:ledger/truth.json`).
# SoD gets STRONGER: "only the verifier writes the ledger branch" is enforceable at the remote
# (branch protection / push rules), a wall rather than a tripwire. Protect it if the host supports it.
#
#   bash bin/verifier_loop.sh                                  # ledger branch "ledger", every 120s
#   AGENT_BRANCH=claude/xxx bash bin/verifier_loop.sh          # + constitution check against the
#                                                              #   agent's COMMITTED copy
#   LEDGER_BRANCH=ledger-run2 INTERVAL=60 bash bin/verifier_loop.sh
#
set -uo pipefail
R="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$R"
INTERVAL="${INTERVAL:-120}"
LEDGER_BRANCH="${LEDGER_BRANCH:-ledger}"
# AGENT_BRANCH is optional but strongly recommended: pnl.py hashes the constitution the AGENT
# actually sees (its committed copy on origin), not whatever this checkout happens to contain.
AGENT_BRANCH="${AGENT_BRANCH:-}"
export AGENT_BRANCH

LOG="$R/verifier.log"
[[ -f "$R/.env" ]] || { echo "FATAL: .env missing. The verifier needs the read key." >&2; exit 2; }
set -a; . "$R/.env"; set +a

say() { echo "[$(date -u +%H:%M:%SZ)] $*" | tee -a "$LOG"; }

# --- claim the facts lane. Create the ledger branch from origin's default branch if it does not
# exist yet (it inherits bin/ so pnl.py runs from this checkout), else track the remote one.
git fetch -q origin 2>>"$LOG"
if git rev-parse -q --verify "origin/$LEDGER_BRANCH" >/dev/null 2>&1; then
  git checkout -q -B "$LEDGER_BRANCH" "origin/$LEDGER_BRANCH"
else
  DEFAULT=$(git symbolic-ref -q --short refs/remotes/origin/HEAD 2>/dev/null | sed 's|^origin/||')
  git checkout -q -B "$LEDGER_BRANCH" "origin/${DEFAULT:-main}"
  say "created facts lane '$LEDGER_BRANCH' from origin/${DEFAULT:-main}"
fi

say "verifier up (two-lane). facts=$LEDGER_BRANCH agent=${AGENT_BRANCH:-<unset>} interval=${INTERVAL}s"
while true; do
  # 1. converge OUR lane only. This reset touches the verifier's own branch -- the agent's branch
  #    is never named anywhere in this loop, which is the whole point of v2.
  git fetch -q origin "$LEDGER_BRANCH" 2>>"$LOG" || true
  git rev-parse -q --verify "origin/$LEDGER_BRANCH" >/dev/null 2>&1 && \
    git reset -q --hard "origin/$LEDGER_BRANCH" 2>>"$LOG"
  # keep the agent's committed constitution reachable for pnl.py's hash check
  [[ -n "$AGENT_BRANCH" ]] && { git fetch -q origin "$AGENT_BRANCH" 2>>"$LOG" || true; }

  # 2. recompute FACTS from primary sources. Only this process holds the read keys.
  if python3 bin/pnl.py > /tmp/pnl_v.out 2>/tmp/pnl_v.err; then
    SIG=$(python3 -c "
import json
d=json.load(open('ledger/truth.json'))
print(d['received_usd'], d['spent_usd'], d['net_usd'], d['verified'], d['made_money'])" 2>/dev/null)
    say "verified: $SIG"
  else
    say "pnl FAILED: $(head -1 /tmp/pnl_v.err)"
    SIG=""
  fi

  # 3. publish to the facts lane -- on meaningful change, or as a liveness heartbeat. The agent's
  #    staleness guard (H2) halts on a ledger older than ~30min, so heartbeats must outpace it.
  HEARTBEAT_S="${HEARTBEAT_S:-300}"
  now_s=$(date +%s); stale_push=0
  [[ -n "${LAST_PUSH_S:-}" ]] && (( now_s - LAST_PUSH_S > HEARTBEAT_S )) && stale_push=1
  if [[ -n "$SIG" && ( "$SIG" != "${LAST_SIG:-}" || "$stale_push" == "1" ) ]]; then
    # explicit allowlist of files THIS process wrote (v1 C2 fix, unchanged): nothing else in the
    # tree is the verifier's to sign.
    git add ledger/truth.json ledger/raw/MANIFEST.sha256 ledger/baseline.json 2>>"$LOG"
    git add ledger/raw/*.json 2>>"$LOG"
    if AIV_VERIFIER=1 git -c user.name="verifier" -c user.email="verifier@local" \
         commit -q --no-gpg-sign -m "verifier: ledger @ $(date -u +%Y-%m-%dT%H:%M:%SZ) | $SIG" 2>>"$LOG"; then
      if git push -q origin "$LEDGER_BRANCH" 2>>"$LOG"; then
        [[ "$stale_push" == "1" && "$SIG" == "${LAST_SIG:-}" ]] && say "heartbeat: $SIG" || say "pushed: $SIG"
        LAST_SIG="$SIG"; LAST_PUSH_S="$now_s"
      else
        say "PUSH FAILED for $SIG -- retry next cycle (LAST_SIG NOT advanced)"
      fi
    else
      say "commit failed for $SIG -- retry next cycle"
    fi
  fi

  sleep "$INTERVAL"
done

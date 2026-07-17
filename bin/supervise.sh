#!/usr/bin/env bash
# The WATCH layer. Run once per /loop wake by the assistant. Prints a one-screen status and an
# explicit VERDICT line the assistant reads to decide: keep waiting, restart the verifier, or
# ALERT THE OPERATOR (first dollar / dead verifier).
#
#   bin/supervise.sh <agent-branch>
#
# It does NOT do the verification (verifier_loop.sh does). It answers: is the verifier alive, is
# truth.json fresh, is the push working, and HAS THE FIRST DOLLAR ARRIVED. That last one is the
# run's end condition and the whole reason a human is kept in the loop.
set -uo pipefail
R="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; cd "$R"
BRANCH="${1:-}"
PIDFILE="$R/.run/verifier.pid"
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

# 2. pull the latest verifier-published ledger from the agent's branch, read it
[[ -n "$BRANCH" ]] && git fetch -q origin "$BRANCH" 2>/dev/null || true
T=$(git show "origin/$BRANCH:ledger/truth.json" 2>/dev/null || cat ledger/truth.json 2>/dev/null)
if [[ -z "$T" ]]; then
  echo "ledger     : UNREADABLE"; echo "VERDICT    : INVESTIGATE (no truth.json)"; exit 0
fi
read RECV VERIF CA <<<"$(python3 -c "
import json,sys
d=json.loads('''$T''')
print(d.get('received_usd',0), d.get('verified'), d.get('computed_at',''))" 2>/dev/null)"

# 3. freshness
age="?"
if [[ -n "${CA:-}" ]]; then
  ct=$(python3 -c "import datetime as d;print(int(d.datetime.fromisoformat('$CA'.replace('Z','+00:00')).timestamp()))" 2>/dev/null || echo 0)
  age=$(( now - ct ))
fi
echo "ledger age : ${age}s   verified=$VERIF   received=\$$RECV"

# 4. recent push activity from the log
echo "last log   : $(tail -1 "$R/verifier.log" 2>/dev/null || echo '(no log)')"

# ---- VERDICT (the line the assistant acts on) ----
if python3 -c "import sys; sys.exit(0 if float('$RECV')>0 else 1)" 2>/dev/null; then
  echo "VERDICT    : ⭐ FIRST DOLLAR RECEIVED (\$$RECV). RUN OVER. ALERT THE OPERATOR NOW."
elif [[ "$alive" -eq 0 ]]; then
  echo "VERDICT    : RESTART -- verifier process is dead. Run bin/start_verifier.sh $BRANCH"
elif [[ "$age" != "?" && "$age" -gt 1500 ]]; then
  echo "VERDICT    : STALE (${age}s > 1500s) -- verifier alive but not publishing. Check verifier.log."
else
  echo "VERDICT    : OK -- verifier live, ledger fresh, no money yet. Keep watching."
fi

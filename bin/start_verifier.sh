#!/usr/bin/env bash
# One-shot: start the whole verifier side for an overnight run. RUN ON THE OPERATOR'S MAC.
#
#   bin/start_verifier.sh <agent-branch>
#   e.g.  bin/start_verifier.sh claude/project-analysis-ew7b92
#
# Does, in order:
#   1. verifies the agent's branch exists on origin (the verifier syncs IT, not main)
#   2. checks out that branch locally + pulls it, so the constitution hash is frozen against what
#      the AGENT actually sees (a mismatch would false-halt constitution_intact on cycle 1)
#   3. fresh set_baseline.py -> marks true run-start + re-freezes the constitution hash
#   4. launches verifier_loop.sh under caffeinate (Mac stays awake) in the background, auto-logged
#
# The supervising /loop (bin/supervise.sh, run by the assistant) watches this. Two loops, two jobs:
# this one recomputes truth.json; the supervisor watches that it stays alive and catches first-dollar.
set -uo pipefail
R="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; cd "$R"
BRANCH="${1:?usage: start_verifier.sh <agent-branch>   (e.g. claude/xxx)}"

echo "=== 1. agent branch on origin? ==="
git fetch -q origin
git rev-parse -q --verify "origin/$BRANCH" >/dev/null 2>&1 \
  || { echo "FATAL: origin/$BRANCH does not exist. The sandbox agent must 'git push -u origin HEAD' first." >&2; exit 2; }
echo "  origin/$BRANCH -> $(git rev-parse --short origin/$BRANCH)"

echo "=== 2. check out the agent's branch (freeze constitution against what IT sees) ==="
git checkout -q -B "$BRANCH" "origin/$BRANCH"
echo "  on $BRANCH @ $(git rev-parse --short HEAD)"
# sanity: is the agent's constitution the same one we hardened tonight?
if ! grep -q "first received dollar" CONSTITUTION.md 2>/dev/null; then
  echo "  ⚠ WARNING: this branch's CONSTITUTION.md lacks the first-dollar stop. The agent branched" >&2
  echo "    off an OLD main. Have it merge main before the run, or constitution_intact may mislead." >&2
fi

echo "=== 3. fresh baseline (true run-start; re-freezes constitution hash) ==="
python3 bin/set_baseline.py

echo "=== 4. launch verifier_loop under caffeinate (background) ==="
[[ -f .env ]] || { echo "FATAL: .env (read keys) missing on this machine." >&2; exit 2; }
mkdir -p "$R/.run"
PIDFILE="$R/.run/verifier.pid"
if [[ -f "$PIDFILE" ]] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
  echo "  verifier already running (pid $(cat "$PIDFILE")). Kill it first: kill \$(cat $PIDFILE)"; exit 1
fi
# caffeinate -i keeps the Mac awake while the loop runs; the loop is the child of caffeinate so the
# whole thing dies together on stop. nohup so it survives this shell closing.
nohup caffeinate -i env BRANCH="$BRANCH" bash bin/verifier_loop.sh > "$R/verifier.log" 2>&1 &
echo $! > "$PIDFILE"
sleep 3
if kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
  echo "  ✓ verifier up (pid $(cat "$PIDFILE")), caffeinated, syncing $BRANCH"
  echo "  log: $R/verifier.log   stop: kill \$(cat $PIDFILE)"
  tail -3 "$R/verifier.log" 2>/dev/null | sed 's/^/    /'
else
  echo "  ✗ verifier died on startup. Check $R/verifier.log:" >&2
  tail -5 "$R/verifier.log" >&2; exit 1
fi

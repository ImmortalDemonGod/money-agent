#!/usr/bin/env bash
# One-shot: start the whole verifier side for a run (v2, two-lane). RUN ON THE OPERATOR'S MACHINE.
#
#   bin/start_verifier.sh <agent-branch>
#   e.g.  bin/start_verifier.sh claude/run2-xyz
#
# Does, in order:
#   1. verifies the agent's branch exists on origin (needed to freeze/check ITS constitution copy;
#      the verifier never checks that branch out -- two-lane design, see verifier_loop.sh)
#   2. fresh set_baseline.py -> marks true run-start + freezes the constitution hash from the
#      AGENT'S committed copy (AGENT_BRANCH), in the verifier's private state dir
#   3. launches verifier_loop.sh under caffeinate (machine stays awake) in the background
#
# The loop publishes facts to the LEDGER branch (default "ledger", override LEDGER_BRANCH=...).
# The agent's branch is never reset or written by any of this.
set -uo pipefail
R="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; cd "$R"
AGENT_BRANCH="${1:?usage: start_verifier.sh <agent-branch>   (e.g. claude/xxx)}"
LEDGER_BRANCH="${LEDGER_BRANCH:-ledger}"
export AGENT_BRANCH LEDGER_BRANCH

echo "=== 1. agent branch on origin? ==="
git fetch -q origin
git rev-parse -q --verify "origin/$AGENT_BRANCH" >/dev/null 2>&1 \
  || { echo "FATAL: origin/$AGENT_BRANCH does not exist. The sandbox agent must 'git push -u origin HEAD' first." >&2; exit 2; }
echo "  origin/$AGENT_BRANCH -> $(git rev-parse --short "origin/$AGENT_BRANCH")"
# sanity: does the agent's committed constitution carry the first-dollar stop?
if ! git show "origin/$AGENT_BRANCH:CONSTITUTION.md" 2>/dev/null | grep -qi "first received dollar"; then
  echo "  ⚠ WARNING: origin/$AGENT_BRANCH's CONSTITUTION.md lacks the first-dollar stop. The agent" >&2
  echo "    branched off an OLD base; have it merge the current default branch before the run." >&2
fi

echo "=== 2. ensure the facts lane exists, THEN freeze the baseline ==="
# ROUND-3 FIX (ordering): set_baseline froze the facts-lane OID, but this script used to run it
# BEFORE verifier_loop.sh created the ledger branch -- so the OID froze empty on every fresh run
# and guard's ancestry-scoped SoD check silently degraded to the bypassable date scope. Create the
# lane first (exactly as verifier_loop.sh would), so the baseline records its real tip.
if ! git rev-parse -q --verify "origin/$LEDGER_BRANCH" >/dev/null 2>&1; then
  DEFAULT=$(git symbolic-ref -q --short refs/remotes/origin/HEAD 2>/dev/null | sed 's|^origin/||')
  git push -q origin "origin/${DEFAULT:-main}:refs/heads/$LEDGER_BRANCH" \
    && echo "  created facts lane '$LEDGER_BRANCH' from origin/${DEFAULT:-main}" \
    || { echo "FATAL: could not create origin/$LEDGER_BRANCH." >&2; exit 2; }
  git fetch -q origin "$LEDGER_BRANCH"
fi
python3 bin/set_baseline.py

echo "=== 3. launch verifier_loop (two-lane) under caffeinate (background) ==="
[[ -f .env ]] || { echo "FATAL: .env (read keys) missing on this machine." >&2; exit 2; }
mkdir -p "$R/.run"
PIDFILE="$R/.run/verifier.pid"
if [[ -f "$PIDFILE" ]] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
  echo "  verifier already running (pid $(cat "$PIDFILE")). Kill it first: kill \$(cat $PIDFILE)"; exit 1
fi
# caffeinate is macOS-only; gate on it so the verifier also launches on Linux/other hosts.
if command -v caffeinate >/dev/null 2>&1; then
  PREFIX=(caffeinate -i)
else
  PREFIX=()
  echo "  note: 'caffeinate' not found (non-macOS) -- launching without it; ensure the host does not sleep."
fi
nohup env AGENT_BRANCH="$AGENT_BRANCH" LEDGER_BRANCH="$LEDGER_BRANCH" \
  "${PREFIX[@]}" bash bin/verifier_loop.sh > "$R/verifier.log" 2>&1 &
echo $! > "$PIDFILE"
sleep 3
if kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
  echo "  ✓ verifier up (pid $(cat "$PIDFILE")), caffeinated, publishing to '$LEDGER_BRANCH'"
  echo "  log: $R/verifier.log   stop: kill \$(cat $PIDFILE)"
  tail -3 "$R/verifier.log" 2>/dev/null | sed 's/^/    /'
else
  echo "  ✗ verifier died on startup. Check $R/verifier.log:" >&2
  tail -5 "$R/verifier.log" >&2; exit 1
fi

echo
echo "=== recommended (SoD as a WALL): protect the '$LEDGER_BRANCH' branch on the remote so only"
echo "    the verifier's credential can push it. Two-lane makes this enforceable for the first time."
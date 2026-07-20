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
R="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; cd "$R" || exit 1
AGENT_BRANCH="${1:?usage: start_verifier.sh <agent-branch>   (e.g. claude/xxx)}"
# S16 FIX (adversarial correctness pass): learn SHADOW from .env BEFORE resolving + exporting the
# lane. This script exports LEDGER_BRANCH to the launched verifier_loop, so if it resolved 'ledger'
# because SHADOW=1 lived only in .env (unread here), pnl.py would then FATAL every cycle on the
# lane mismatch and the whole run would wedge. Source .env first (it is required anyway) so SHADOW
# is known from either .env or the command line.
if [[ -f "$R/.env" ]]; then
  set -a
  # shellcheck source=/dev/null
  . "$R/.env"
  set +a
fi
# S12: shadow defaults (see verifier_loop.sh -- same rule, applied here too because either
# script can be the entry point).
if [[ "${SHADOW:-0}" == "1" ]]; then
  LEDGER_BRANCH="${LEDGER_BRANCH:-shadow-ledger}"
  MONEY_AGENT_STATE="${MONEY_AGENT_STATE:-$HOME/.money-agent-shadow}"
  export MONEY_AGENT_STATE SHADOW
  echo "=== SHADOW RUN: facts -> '$LEDGER_BRANCH', state -> '$MONEY_AGENT_STATE' ==="
fi
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

echo "=== 1b. wash-trade allowlist provisioned? (issue #37) ==="
# TEST-MARKER: preflight-opid-begin (tests/sim.sh extracts this block verbatim)
# pnl.py excludes operator self-purchases via STATE_DIR/operator_identity.json. Empty or absent,
# that guard is INERT and only surfaces at the FIRST CHARGE -- wash_guard_disarmed flips
# verified=false and a legitimate first sale halts the run as unverifiable instead of counting.
# Related-party exclusion is a precondition for a qualifying sale; assert it BEFORE any offer can
# go live, not at settlement. (setup_sandbox.sh cannot check this: STATE_DIR is verifier-side,
# unreachable from the sandbox by design -- so the check lives here, on the machine that has it.)
OPID="${MONEY_AGENT_STATE:-$HOME/.money-agent-verifier}/operator_identity.json"
if ! python3 -c '
import json, sys
try:
    d = json.load(open(sys.argv[1]))
except Exception:
    sys.exit(1)
sys.exit(0 if (d.get("emails") or d.get("card_fingerprints")) else 1)' "$OPID"; then
  echo "FATAL: $OPID missing/empty -- the wash-trade guard would be inert until the first charge," >&2
  echo "       then halt the run on wash_guard_disarmed instead of counting a legitimate sale." >&2
  echo '       Provision it: {"emails": ["<operator email>"], "card_fingerprints": ["<stripe fp>"]}' >&2
  exit 2
fi
echo "  operator identity allowlist present: $OPID"
# TEST-MARKER: preflight-opid-end

echo "=== 2. ensure the facts lane exists, THEN freeze the baseline ==="
# ROUND-3 FIX (ordering): set_baseline froze the facts-lane OID, but this script used to run it
# BEFORE verifier_loop.sh created the ledger branch -- so the OID froze empty on every fresh run
# and guard's ancestry-scoped SoD check silently degraded to the bypassable date scope. Create the
# lane first (exactly as verifier_loop.sh would), so the baseline records its real tip.
if ! git rev-parse -q --verify "origin/$LEDGER_BRANCH" >/dev/null 2>&1; then
  DEFAULT=$(git symbolic-ref -q --short refs/remotes/origin/HEAD 2>/dev/null | sed 's|^origin/||')
  if git push -q origin "origin/${DEFAULT:-main}:refs/heads/$LEDGER_BRANCH"; then
    echo "  created facts lane '$LEDGER_BRANCH' from origin/${DEFAULT:-main}"
  else
    echo "FATAL: could not create origin/$LEDGER_BRANCH." >&2; exit 2
  fi
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
# caffeinate is macOS-only (v2 DEGRADED finding #9: a hard dependency killed the verifier on
# Linux). Use it where it exists; elsewhere the host must stay awake by its own means (a server
# does; a laptop needs systemd-inhibit or equivalent) -- say so instead of dying.
KEEPAWAKE=""
if command -v caffeinate >/dev/null 2>&1; then KEEPAWAKE="caffeinate -i"
else echo "  note: no caffeinate on this host (Linux?) -- ensure the machine does not sleep."; fi
# shellcheck disable=SC2086  # KEEPAWAKE is deliberately word-split ("caffeinate -i" or empty)
nohup $KEEPAWAKE env AGENT_BRANCH="$AGENT_BRANCH" LEDGER_BRANCH="$LEDGER_BRANCH" \
  bash bin/verifier_loop.sh > "$R/verifier.log" 2>&1 &
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

#!/usr/bin/env bash
# WEAK-MODE runner (B5, DEGRADED #9's second half). A co-located verifier for fast local trials:
# same facts pipeline (pnl.py + edge_pnl.py), same commit authorship, NO resets, NO second machine.
#
#   bash bin/run_weak.sh              # loop every 120s on the CURRENT branch
#   INTERVAL=60 bash bin/run_weak.sh
#
# BE HONEST ABOUT WHAT THIS IS (SETUP.md "Two deployment modes"): in weak mode the agent and the
# verifier share a filesystem, so every check downstream of these commits is a TRIPWIRE, not a
# wall -- a sandboxed agent can edit any file it can see. truth.py will label the facts
# "working-tree-committed" (grounded for gate purposes, weak by construction). Results from a weak
# run are for debugging the harness, not for concluding anything about the agent. The one thing
# this runner will NEVER do is reset or rewrite the branch: it only ever appends facts commits --
# v1's destroy-your-own-evidence loop stays dead in both modes.
set -uo pipefail
R="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$R"
INTERVAL="${INTERVAL:-120}"
[[ -f "$R/.env" ]] || { echo "FATAL: .env missing (verifier read keys)." >&2; exit 2; }
set -a; . "$R/.env"; set +a

echo "=== WEAK MODE (tripwire-only; see SETUP.md). Facts commit to the CURRENT branch: $(git branch --show-current) ==="
echo "=== No resets ever happen in this loop. Ctrl-C to stop. ==="
while true; do
  if AIV_VERIFIER=1 python3 bin/pnl.py > /tmp/pnl_w.out 2>/tmp/pnl_w.err; then
    AIV_VERIFIER=1 python3 bin/edge_pnl.py > /tmp/edge_w.out 2>/tmp/edge_w.err || true
    git add ledger/truth.json ledger/raw/MANIFEST.sha256 ledger/baseline.json 2>/dev/null
    git add ledger/edge.json ledger/raw/EDGE_MANIFEST.sha256 2>/dev/null
    git add ledger/raw/*.json 2>/dev/null
    if ! git diff --cached --quiet 2>/dev/null; then
      AIV_VERIFIER=1 git -c user.name="verifier" -c user.email="verifier@local" \
        commit -q --no-gpg-sign -m "verifier(weak): ledger @ $(date -u +%Y-%m-%dT%H:%M:%SZ)" \
        && git push -q origin HEAD 2>/dev/null \
        && echo "[$(date -u +%H:%M:%SZ)] published (weak)" \
        || echo "[$(date -u +%H:%M:%SZ)] commit/push failed -- retrying next cycle"
    fi
  else
    echo "[$(date -u +%H:%M:%SZ)] pnl FAILED: $(head -1 /tmp/pnl_w.err)"
  fi
  sleep "$INTERVAL"
done

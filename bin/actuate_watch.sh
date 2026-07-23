#!/usr/bin/env bash
# actuate_watch.sh -- AGENT-side durable-wakeup handler (issue #20.6). The durable queue fires
# this; it fetches the facts lane, syncs any now-resolved actuations, and prints the seconds until
# it should next fire (NEXT_WAKEUP_SECONDS=...), sized to the soonest open deadline. The caller
# (the /loop's queued wakeup, a systemd timer, a launchd interval) reads that line and re-arms.
#
# This is the durable replacement for the fixed 24h companion-bet poll: the DURABILITY comes from
# the external queue that survives restarts (never session-local cron -- STANDING_RUN.md, entry
# 005), and the CADENCE comes from `next-wakeup` tightening as a deadline approaches.
#
# Env: LEDGER_BRANCH (facts lane, default 'ledger'); AGENT_BRANCH is inferred from the checkout.
set -uo pipefail
R="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; cd "$R" || exit 1
LEDGER_BRANCH="${LEDGER_BRANCH:-ledger}"
git fetch -q origin "$LEDGER_BRANCH" 2>/dev/null || true
python3 bin/actuate.py sync-all
next="$(python3 bin/actuate.py next-wakeup)"
echo "NEXT_WAKEUP_SECONDS=${next}"

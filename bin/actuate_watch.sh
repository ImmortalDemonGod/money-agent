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
# It always emits a VALID positive NEXT_WAKEUP_SECONDS (falling back to a safe idle cadence if
# next-wakeup is unavailable), so a corrupt tasks file can never leave the durable queue with an
# empty/garbage re-arm value. A sync-all failure is reported but does not suppress the re-arm.
#
# Env: LEDGER_BRANCH (facts lane, default 'ledger'); ACTUATE_IDLE_WAKEUP_S (fallback, default 1800).
set -uo pipefail
R="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; cd "$R" || exit 1
LEDGER_BRANCH="${LEDGER_BRANCH:-ledger}"
git fetch -q origin "$LEDGER_BRANCH" 2>/dev/null || true

if ! python3 bin/actuate.py sync-all; then
  echo "actuate_watch: sync-all failed; will still emit a re-arm and retry next fire" >&2
fi

next="$(python3 bin/actuate.py next-wakeup 2>/dev/null || true)"
if ! [[ "$next" =~ ^[0-9]+$ ]] || [[ "$next" -le 0 ]]; then
  next="${ACTUATE_IDLE_WAKEUP_S:-1800}"
  echo "actuate_watch: next-wakeup unavailable/invalid; falling back to ${next}s" >&2
fi
echo "NEXT_WAKEUP_SECONDS=${next}"

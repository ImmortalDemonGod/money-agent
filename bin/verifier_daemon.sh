#!/usr/bin/env bash
# launchd entrypoint (v2 two-lane). KeepAlive restarts THIS on death, so it must NOT re-baseline
# (that would move run-start on every restart). Baseline is set once by start_verifier.sh; this
# just runs the loop. AGENT_BRANCH must be set in the launchd plist environment for the
# constitution check; there is no default because a hardcoded branch name goes stale the moment a
# new run starts (v1's copy of this file shipped with run-1's literal branch baked in).
R="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; cd "$R"
[[ -n "${AGENT_BRANCH:-}" ]] || { echo "FATAL: AGENT_BRANCH unset (set it in the launchd plist)."; exit 2; }
exec caffeinate -dimsu env AGENT_BRANCH="$AGENT_BRANCH" LEDGER_BRANCH="${LEDGER_BRANCH:-ledger}" \
  INTERVAL="${INTERVAL:-60}" HEARTBEAT_S="${HEARTBEAT_S:-300}" bash bin/verifier_loop.sh

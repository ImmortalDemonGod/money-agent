#!/usr/bin/env bash
# launchd entrypoint. KeepAlive restarts THIS on death, so it must NOT re-baseline (that would move
# run-start on every restart). Baseline is set once by start_verifier.sh; this just runs the loop.
R="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; cd "$R"
exec caffeinate -dimsu env BRANCH="${BRANCH:-claude/project-analysis-q4hjrg}" \
  INTERVAL="${INTERVAL:-60}" HEARTBEAT_S="${HEARTBEAT_S:-300}" bash bin/verifier_loop.sh

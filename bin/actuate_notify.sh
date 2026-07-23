#!/usr/bin/env bash
# actuate_notify.sh -- OPERATOR-side notifier (out-of-sandbox, read-only). Each invocation runs
# `actuate.py notify-scan` and pushes NEW, deduped alerts through a pluggable transport. The
# DURABLE re-arming is the caller's job (a systemd timer, cron, or the platform's queued wakeup);
# this is the one-shot each fire runs. `--loop [S]` runs a foreground poller (default 60s).
#
# It never touches the sandbox or signs anything -- it only READS the claims/facts lanes and emits
# a push, so it adds no surface the agent could spoof. The alert line's machine fields (id,
# urgency, ttl) LEAD the line and are parsed by fixed position; the agent-controlled gate is
# scrubbed of control chars by notify-scan and sits last, so it cannot forge a line or override a
# field. Agent text is never passed as a curl `-d` argument (that would let `@path` read a file).
#
# Transport (first match wins):
#   ACTUATE_NTFY_TOPIC -> POST to ${ACTUATE_NTFY_BASE:-https://ntfy.sh}/$topic  (phone/web push)
#   ACTUATE_NOTIFY_CMD -> the alert line is piped to this command on stdin
#   (default)          -> appended to run/actuation_alerts.log and echoed to stderr
#
# Env: AGENT_BRANCH (required, the claims lane), LEDGER_BRANCH (facts lane, default 'ledger'),
#      ACTUATE_NOTIFY_ALL=1 to push NORMAL alerts too (default: URGENT only),
#      ACTUATE_NOTIFY_SEEN dedup-state file (default run/.actuate_notify_seen).
set -uo pipefail
R="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; cd "$R" || exit 1
SEEN="${ACTUATE_NOTIFY_SEEN:-$R/run/.actuate_notify_seen}"
mkdir -p "$(dirname "$SEEN")"; : >>"$SEEN"

dispatch() {   # $1 = full alert line (never used as a curl -d argument)
  local msg="$1"
  if [[ -n "${ACTUATE_NTFY_TOPIC:-}" ]]; then
    if ! curl -fsS -m 20 -H "Title: money-agent actuation" \
         --data-raw "$msg" "${ACTUATE_NTFY_BASE:-https://ntfy.sh}/${ACTUATE_NTFY_TOPIC}" >/dev/null; then
      echo "actuate_notify: ntfy push failed for: $msg" >&2
    fi
  elif [[ -n "${ACTUATE_NOTIFY_CMD:-}" ]]; then
    if ! printf '%s\n' "$msg" | sh -c "${ACTUATE_NOTIFY_CMD}"; then
      echo "actuate_notify: notify-cmd failed for: $msg" >&2
    fi
  else
    printf '%s\t%s\n' "$(date -u +%FT%TZ)" "$msg" >>"$R/run/actuation_alerts.log"
    echo "actuate_notify: $msg" >&2
  fi
}

scan_once() {
  local sink; sink="$(mktemp)" || { echo "actuate_notify: mktemp failed" >&2; return 1; }
  # shellcheck disable=SC2064
  trap "rm -f '$sink'" RETURN
  if ! python3 bin/actuate.py notify-scan --sink "$sink" >/dev/null 2>&1; then
    echo "actuate_notify: notify-scan failed (is AGENT_BRANCH set?)" >&2
    return 1
  fi
  # Hold a lock across the whole read/dedup/append pass so a concurrent poller cannot double-send.
  (
    flock 9
    n=0
    while IFS= read -r line || [[ -n "$line" ]]; do
      [[ -z "$line" ]] && continue
      read -r tag id urgfield _ <<<"$line"       # fixed-position parse; gate cannot spoof these
      [[ "$tag" == "ALERT" && "$id" == ACT-* ]] || continue
      urg="${urgfield#urgency=}"
      [[ "$urg" == "URGENT" || "$urg" == "NORMAL" ]] || continue
      # Dedup on id:urgency. Known LOW residual (accepted): an agent that hand-crafts a task with a
      # VALID future id can pre-seed this key and suppress that id's later genuine URGENT push. The
      # incentive is backwards (it delays the agent's OWN fulfillment) and the task stays visible via
      # `actuate.py list`/`card`, so it is a tripwire limit, not a wall -- like bets.json.
      key="${id}:${urg}"
      grep -qxF "$key" "$SEEN" && continue
      if [[ "$urg" == "URGENT" || "${ACTUATE_NOTIFY_ALL:-0}" == "1" ]]; then
        dispatch "$line"; printf '%s\n' "$key" >>"$SEEN"; n=$((n + 1))
      fi
    done <"$sink"
    echo "actuate_notify: dispatched $n new alert(s)" >&2
  ) 9>"${SEEN}.lock"
}

if [[ "${1:-}" == "--loop" ]]; then
  interval="${2:-60}"
  while true; do scan_once || true; sleep "$interval"; done
else
  scan_once
fi

#!/usr/bin/env bash
# THE VERIFIER. Runs on the operator's Mac. NEVER in the sandbox.
#
# This closes the last architectural gap. The read key lives here and only here, so the sandbox's
# ledger/truth.json is frozen at whatever was committed at run start -- the agent would read
# received=$0.00 all night even if money actually arrived, and the frozen prediction would come
# back "confirmed" from a stale file. That is a lie with a sha256 attached.
#
# Loop: pull the agent's work -> recompute truth from Stripe + Privacy -> commit as `verifier` ->
# push. The agent pulls it at the top of each iteration. The key never crosses the boundary, which
# is what makes this STRONG mode rather than a tripwire.
#
#   bash bin/verifier_loop.sh          # foreground, every 120s
#   INTERVAL=60 bash bin/verifier_loop.sh
#
set -uo pipefail
R="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$R"
INTERVAL="${INTERVAL:-120}"
LOG="$R/ledger/verifier.log"

[[ -f "$R/.env" ]] || { echo "FATAL: .env missing. The verifier needs the read key." >&2; exit 2; }
set -a; . "$R/.env"; set +a

# If this ever runs where the agent lives, the whole point is lost.
if [[ -f "$R/.env.agent" && "${ALLOW_COLOCATED:-0}" != "1" ]]; then
  echo "WARN: .env.agent is present next to .env -- this looks like the operator's machine," >&2
  echo "      which is fine. But if this is the SANDBOX, stop: the read key must never be here." >&2
fi

say() { echo "[$(date -u +%H:%M:%SZ)] $*" | tee -a "$LOG"; }

say "verifier up. interval=${INTERVAL}s. repo=$R"
while true; do
  # 1. take the agent's work (MONEY_LOG, packets, iterations). Never clobber it.
  #
  # Discard local ledger changes FIRST. truth.json is DERIVED state -- pnl.py regenerates it from
  # the APIs two lines below, so there is nothing here worth keeping. This is not optional:
  # `computed_at` changes every cycle, so when no real number moved we (correctly) skip the commit
  # and truth.json stays dirty forever -- which made `pull --rebase` fail on EVERY subsequent
  # cycle. The verifier would have never seen the agent's work all night, silently, while logging
  # a cheerful "verified" each time. Found by running it, not by reading it.
  git checkout -q -- ledger/ 2>/dev/null || true
  git fetch -q origin 2>>"$LOG"
  if ! git pull -q --rebase origin main 2>>"$LOG"; then
    say "PULL FAILED -- the agent's work is not visible to the verifier. Investigate."
    git rebase --abort 2>/dev/null || true
  fi

  # 2. recompute FACTS from primary sources. This is the only process with the key.
  if python3 bin/pnl.py > /tmp/pnl_v.out 2>/tmp/pnl_v.err; then
    RECV=$(python3 -c "import json;print(json.load(open('ledger/truth.json'))['received_usd'])" 2>/dev/null)
    NET=$(python3 -c "import json;print(json.load(open('ledger/truth.json'))['net_usd'])" 2>/dev/null)
    say "verified: received=\$$RECV net=\$$NET"
  else
    # A failed pull is NOT $0 earned. pnl.py already refuses to write on a hard failure; if it
    # wrote verified:false, guard.py halts the agent. Either way: never fabricate a number here.
    say "pnl FAILED: $(head -1 /tmp/pnl_v.err)"
  fi

  # 3. publish -- but ONLY when a number the agent cares about actually moved.
  #
  # truth.json carries `computed_at`, so it differs on EVERY cycle. Committing on any diff would
  # push ~240 identical commits overnight and bury the two that matter. Compare the meaningful
  # fields instead. (Found by running the loop rather than reading it -- again.)
  SIG=$(python3 -c "
import json
d=json.load(open('ledger/truth.json'))
print(d['received_usd'], d['spent_usd'], d['net_usd'], d['verified'], d['made_money'])" 2>/dev/null)
  if [[ "$SIG" != "${LAST_SIG:-}" ]]; then
    git add ledger/
    if AIV_VERIFIER=1 git -c user.name="verifier" -c user.email="verifier@local" \
         commit -q --no-gpg-sign -m "verifier: ledger @ $(date -u +%Y-%m-%dT%H:%M:%SZ) | $SIG" 2>>"$LOG"; then
      git push -q origin main 2>>"$LOG" && say "pushed: $SIG" || say "push failed (see log)"
    fi
    LAST_SIG="$SIG"
  fi

  sleep "$INTERVAL"
done

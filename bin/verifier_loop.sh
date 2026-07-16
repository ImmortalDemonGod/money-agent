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

# The AGENT owns the branch. A Claude Code cloud sandbox works on a claude/<name> branch it creates
# and cannot be moved off. If the verifier synced `main` while the agent worked on claude/xxx, they
# would never meet: the agent reads a frozen ledger all night, the verifier never sees its work, and
# nothing looks broken. So the verifier syncs the AGENT'S branch. Pass it explicitly.
#   BRANCH=claude/project-analysis-ew7b92 bash bin/verifier_loop.sh
BRANCH="${BRANCH:-}"
if [[ -z "$BRANCH" ]]; then
  echo "FATAL: BRANCH unset. The verifier must sync the same branch the sandbox agent is on." >&2
  echo "  Find it: in the sandbox run 'git branch --show-current', then:" >&2
  echo "  BRANCH=<that> bash bin/verifier_loop.sh" >&2
  exit 2
fi
# Track the agent's branch locally so pull/push target it.
git fetch -q origin "$BRANCH" 2>/dev/null || { echo "FATAL: origin has no branch '$BRANCH' yet. The sandbox must push it once first." >&2; exit 2; }
git checkout -q -B "$BRANCH" "origin/$BRANCH" 2>/dev/null || git checkout -q "$BRANCH"
# NOT in ledger/. The loop wrote its own log there, `git add ledger/` tracked it, and it was
# therefore dirty on every cycle -> pull failed forever. The loop's own logging broke the loop's
# own pull. ledger/ is verifier-owned EVIDENCE; a log is not evidence.
LOG="$R/verifier.log"

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
  # ONLY truth.json. It is the one genuinely DERIVED file -- pnl.py rebuilds it from the APIs two
  # lines below. `git checkout -- ledger/` was too broad and silently reverted baseline.json every
  # cycle, so the verifier kept recomputing against a stale window and reported $0 while pnl.py
  # measured $1. baseline.json is a DECISION, not derived state; raw/ is immutable evidence.
  # Neither may be discarded. (Found by testing propagation end-to-end, not by reading the loop.)
  # truth.json AND raw/MANIFEST.sha256 are both DERIVED and both TRACKED, so both are rewritten
  # every cycle and both leave the tree dirty -> pull fails. Discard both. baseline.json (a
  # decision) and raw/*.json (immutable evidence) are never discarded.
  git checkout -q -- ledger/truth.json ledger/raw/MANIFEST.sha256 2>/dev/null || true
  git fetch -q origin 2>>"$LOG"
  if ! git pull -q --rebase origin "$BRANCH" 2>>"$LOG"; then
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
  # HEARTBEAT: push even when SIG is unchanged if too long since the last push. Two of my own
  # mechanisms conflicted -- publish-on-change froze computed_at on the agent's branch when no money
  # moved, and the agent's H2 staleness guard then halts on a ledger it reads as DEAD while the
  # verifier is alive. Prove liveness every HEARTBEAT_S. ~12 commits/hr, far under the 30-min halt.
  HEARTBEAT_S="${HEARTBEAT_S:-300}"
  now_s=$(date +%s); stale_push=0
  if [[ -n "${LAST_PUSH_S:-}" ]] && (( now_s - LAST_PUSH_S > HEARTBEAT_S )); then stale_push=1; fi
  if [[ "$SIG" != "${LAST_SIG:-}" || "$stale_push" == "1" ]]; then
    # C2: stage an EXPLICIT ALLOWLIST of files the verifier itself just wrote. `git add ledger/`
    # staged whatever the agent had planted there and committed it signed `verifier` -- laundering
    # the agent's forgery under the trusted identity. The verifier commits ONLY: truth.json, the
    # manifest, the transparency baseline copy, and the raw pulls IT generated this run (pnl.py
    # already purged untracked agent files before writing its own). Nothing else in ledger/ is the
    # verifier's to sign.
    git add ledger/truth.json ledger/raw/MANIFEST.sha256 ledger/baseline.json 2>>"$LOG"
    git add ledger/raw/*.json 2>>"$LOG"   # pnl.py purged agent-planted ones; these are verifier-written
    # H3: only advance LAST_SIG when the push actually SUCCEEDS. Advancing it on commit-or-push
    # failure stranded the one number that mattered forever while every later cycle logged healthy.
    if AIV_VERIFIER=1 git -c user.name="verifier" -c user.email="verifier@local" \
         commit -q --no-gpg-sign -m "verifier: ledger @ $(date -u +%Y-%m-%dT%H:%M:%SZ) | $SIG" 2>>"$LOG"; then
      if git push -q origin "$BRANCH" 2>>"$LOG"; then
        [[ "$stale_push" == "1" && "$SIG" == "${LAST_SIG:-}" ]] && say "heartbeat: $SIG" || say "pushed: $SIG"
        LAST_SIG="$SIG"; LAST_PUSH_S="$now_s"
      else
        say "PUSH FAILED for $SIG -- will retry next cycle (LAST_SIG NOT advanced)"
      fi
    else
      say "commit failed for $SIG -- will retry next cycle"
    fi
  fi

  sleep "$INTERVAL"
done

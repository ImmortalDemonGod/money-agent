#!/usr/bin/env bash
# THE VERIFIER (v2, two-lane). Runs on the operator's machine. NEVER in the sandbox.
#
# v1 published truth.json onto the AGENT'S branch, which forced a `git reset --hard` of the shared
# worktree every cycle -- the single most damaging harness defect of run 1: it destroyed agent
# evidence at least six documented times (wiped SENT_LOG/MONEY_LOG appends, lost iteration numbers,
# an empty commit that looked successful, a mid-deploy wipe). v2 separates the lanes:
#
#   FACTS lane : this loop commits ledger/{truth.json, raw/, MANIFEST, baseline copy} to a
#                dedicated LEDGER branch from the verifier's own checkout. Heartbeats live here.
#   CLAIMS lane: the agent's branch. This loop NEVER checks it out, resets it, or writes to it.
#
# The agent reads facts via bin/truth.py (fetch + `git show origin/<ledger>:ledger/truth.json`).
# SoD gets STRONGER: "only the verifier writes the ledger branch" is enforceable at the remote
# (branch protection / push rules), a wall rather than a tripwire. Protect it if the host supports it.
#
#   bash bin/verifier_loop.sh                                  # ledger branch "ledger", every 120s
#   AGENT_BRANCH=claude/xxx bash bin/verifier_loop.sh          # + constitution check against the
#                                                              #   agent's COMMITTED copy
#   LEDGER_BRANCH=ledger-run2 INTERVAL=60 bash bin/verifier_loop.sh
#
set -uo pipefail
R="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$R" || exit 1
INTERVAL="${INTERVAL:-120}"
# S12: a shadow verifier (SHADOW=1) defaults onto its own lane + state dir so a rehearsal can
# never touch anything a live run trusts. Explicit env still wins -- and pnl.py refuses a
# non-shadow lane under SHADOW=1 regardless (that is the wall; this is the convenience).
if [[ "${SHADOW:-0}" == "1" ]]; then
  LEDGER_BRANCH="${LEDGER_BRANCH:-shadow-ledger}"
  MONEY_AGENT_STATE="${MONEY_AGENT_STATE:-$HOME/.money-agent-shadow}"
  export MONEY_AGENT_STATE
fi
LEDGER_BRANCH="${LEDGER_BRANCH:-ledger}"
# AGENT_BRANCH is optional but strongly recommended: pnl.py hashes the constitution the AGENT
# actually sees (its committed copy on origin), not whatever this checkout happens to contain.
AGENT_BRANCH="${AGENT_BRANCH:-}"
export AGENT_BRANCH

LOG="$R/verifier.log"
[[ -f "$R/.env" ]] || { echo "FATAL: .env missing. The verifier needs the read key." >&2; exit 2; }
set -a
# .env is a runtime credential file; shellcheck cannot follow it
# shellcheck source=/dev/null
. "$R/.env"
set +a

say() { echo "[$(date -u +%H:%M:%SZ)] $*" | tee -a "$LOG"; }

# --- claim the facts lane. Create the ledger branch from origin's default branch if it does not
# exist yet (it inherits bin/ so pnl.py runs from this checkout), else track the remote one.
git fetch -q origin 2>>"$LOG"
if git rev-parse -q --verify "origin/$LEDGER_BRANCH" >/dev/null 2>&1; then
  git checkout -q -B "$LEDGER_BRANCH" "origin/$LEDGER_BRANCH"
else
  DEFAULT=$(git symbolic-ref -q --short refs/remotes/origin/HEAD 2>/dev/null | sed 's|^origin/||')
  git checkout -q -B "$LEDGER_BRANCH" "origin/${DEFAULT:-main}"
  say "created facts lane '$LEDGER_BRANCH' from origin/${DEFAULT:-main}"
fi

# private temp dir for pnl output (fixed /tmp paths can be pre-created as symlinks by a local user
# to overwrite files or inject log lines -- CodeRabbit). Cleaned on exit.
TMPD="$(mktemp -d "${TMPDIR:-/tmp}/pnl_v.XXXXXX")"
trap 'rm -rf "$TMPD"' EXIT

say "verifier up (two-lane). facts=$LEDGER_BRANCH agent=${AGENT_BRANCH:-<unset>} interval=${INTERVAL}s"
while true; do
  # 1. converge OUR lane only. This reset touches the verifier's own branch -- the agent's branch
  #    is never named anywhere in this loop, which is the whole point of v2.
  # TEST-MARKER: convergence-begin (tests/sim.sh extracts this block verbatim)
  #    Do NOT reset away a local commit that has not reached origin yet: if a prior cycle committed
  #    but the push failed, resetting to origin would discard committed raw pulls (CodeRabbit). So
  #    push any pending local commits FIRST, and only reset when local is not ahead of origin.
  git fetch -q origin "$LEDGER_BRANCH" 2>>"$LOG" || true
  if git rev-parse -q --verify "origin/$LEDGER_BRANCH" >/dev/null 2>&1; then
    # ROUND-3 FIX: the previous guard here used `git rev-list -q <range>`, which is a usage error
    # (-q is not a rev-list flag): stderr was swallowed, the substitution was ALWAYS empty, the
    # push-before-reset branch never fired, and the reset ran unconditionally every cycle -- i.e.
    # the data-loss fix was inert and the hazard it claimed to close stayed open. `--count` is the
    # correct primitive; verified against an unreachable remote (commit + raw pull preserved with
    # a WARN) and after recovery (stranded commits pushed to origin).
    AHEAD=$(git rev-list --count "origin/$LEDGER_BRANCH..HEAD" 2>>"$LOG" || echo 0)
    if [[ "${AHEAD:-0}" -gt 0 ]]; then
      if git merge-base --is-ancestor "origin/$LEDGER_BRANCH" HEAD 2>>"$LOG"; then
        # genuinely ahead (a prior push failed): push the stranded facts commits, never reset over
        if git push -q origin "HEAD:$LEDGER_BRANCH" 2>>"$LOG"; then
          git fetch -q origin "$LEDGER_BRANCH" 2>>"$LOG"; say "recovered $AHEAD stranded facts commit(s)"
        else
          say "WARN: $AHEAD local ledger commit(s) not yet pushed; NOT resetting (would lose raw pulls)"
        fi
        AHEAD=$(git rev-list --count "origin/$LEDGER_BRANCH..HEAD" 2>>"$LOG" || echo 0)
      else
        # DIVERGED (origin force-moved, e.g. rotation from another checkout): skip-forever would
        # deadlock the lane, so converge -- but first RESCUE any raw pull that exists only in the
        # local history (a stranded pull committed after the divergence point). It must be
        # re-COMMITTED, not just restored: pnl.py's C3 purge deletes untracked raw files as
        # agent-planted, so a bare file restore would be eaten next cycle.
        RESCUE=$(comm -23 <(git ls-tree -r HEAD --name-only -- ledger/raw/ | sort) \
                          <(git ls-tree -r "origin/$LEDGER_BRANCH" --name-only -- ledger/raw/ | sort))
        RD=""
        if [[ -n "$RESCUE" ]]; then
          RD=$(mktemp -d)
          # #46: side-car copy into the agent-unreachable state dir BEFORE the reset. The
          # re-commit below is the primary rescue; the side-car survives even a botched rescue or
          # an operator intervention inside the divergence window (traps.md #9's residual).
          SIDECAR="${MONEY_AGENT_STATE:-$HOME/.money-agent-verifier}/raw-rescue/$(date -u +%Y%m%dT%H%M%S)-diverged"
          mkdir -p "$SIDECAR"
          while IFS= read -r f; do
            mkdir -p "$RD/$(dirname "$f")"; git show "HEAD:$f" > "$RD/$f" 2>>"$LOG"
            cp "$RD/$f" "$SIDECAR/" 2>>"$LOG" || true
          done <<< "$RESCUE"
          say "side-car: diverged pull(s) copied to $SIDECAR (belt; the re-commit below is the suspenders)"
        fi
        say "WARN: facts lane diverged from origin -- converging to origin/$LEDGER_BRANCH"
        git reset -q --hard "origin/$LEDGER_BRANCH" 2>>"$LOG"
        if [[ -n "$RESCUE" ]]; then
          # shellcheck disable=SC2016  # $0 and $(...) are for the inner 'sh -c', not the outer shell
          (cd "$RD" && find . -type f -print0 | xargs -0 -I{} sh -c 'mkdir -p "$0/$(dirname "{}")" && cp "{}" "$0/{}"' "$R")
          git add ledger/raw/ 2>>"$LOG"
          git -c user.name="verifier" -c user.email="verifier@local" commit -q --no-gpg-sign \
            -m "verifier: rescued $(wc -l <<< "$RESCUE") stranded raw pull(s) after divergence" 2>>"$LOG" \
            && say "rescued stranded pulls: $(echo "$RESCUE" | tr '\n' ' ')"
          rm -rf "$RD"
        fi
        AHEAD=$(git rev-list --count "origin/$LEDGER_BRANCH..HEAD" 2>>"$LOG" || echo 0)
      fi
    fi
    # reset only when we are NOT ahead of origin (else keep the local commits for next push)
    [[ "${AHEAD:-0}" -eq 0 ]] && git reset -q --hard "origin/$LEDGER_BRANCH" 2>>"$LOG"
  fi
  # TEST-MARKER: convergence-end
  # keep the agent's committed constitution reachable for pnl.py's hash check. FAIL CLOSED: if the
  # strong-mode fetch fails, a stale origin/AGENT_BRANCH could make pnl publish constitution_intact
  # =true after the agent changed its constitution -- so skip publication this cycle (CodeRabbit).
  AGENT_FETCH_OK=1
  if [[ -n "$AGENT_BRANCH" ]]; then
    git fetch -q origin "$AGENT_BRANCH" 2>>"$LOG" || AGENT_FETCH_OK=0
  fi

  # 2. recompute FACTS from primary sources. Only this process holds the read keys.
  if [[ "$AGENT_FETCH_OK" == "0" ]]; then
    say "SKIP cycle: could not refresh origin/$AGENT_BRANCH (stale constitution ref would be unsafe)"
    SIG=""
  elif python3 bin/pnl.py > "$TMPD/out" 2>"$TMPD/err"; then
    SIG=$(python3 -c "
import json
d=json.load(open('ledger/truth.json'))
print(d['received_usd'], d['spent_usd'], d['net_usd'], d['verified'], d['made_money'])" 2>/dev/null)
    say "verified: $SIG"
  else
    say "pnl FAILED: $(head -1 "$TMPD/err")"
    SIG=""
  fi

  # 2b. the VERIFIED-EDGE rail (issue #6), AFTER pnl.py on purpose: its raw pulls must land after
  # C3's untracked purge and inside this cycle's commit. edge_pnl.py is a no-op (verdict NONE)
  # until the agent commits an EDGE_REGISTRATION.md and the operator provisions ALPACA_PAPER_*
  # creds in .env; it never blocks the money rail.
  EDGE_SIG=""
  if [[ "$AGENT_FETCH_OK" == "0" ]]; then
    say "SKIP edge cycle: stale origin/$AGENT_BRANCH would risk freezing/checking a stale registration"
  elif python3 bin/edge_pnl.py > "$TMPD/edge_out" 2>"$TMPD/edge_err"; then
    EDGE_SIG=$(python3 -c "
import json
d=json.load(open('ledger/edge.json'))
print(d.get('verdict'), d.get('paper_pnl_usd'), d.get('verified'))" 2>/dev/null)
    [[ -n "$EDGE_SIG" && "$EDGE_SIG" != "NONE None"* ]] && say "edge: $EDGE_SIG"
  else
    say "edge_pnl FAILED: $(head -1 "$TMPD/edge_err")"
  fi
  [[ -n "$SIG" && -n "$EDGE_SIG" ]] && SIG="$SIG | edge $EDGE_SIG"

  # 2c. P5 obligation watchdog (S11) -- after pnl for the same raw-purge/commit-cycle reasons.
  # Empty register publishes an affirmative empty fact; a breach makes guard halt the agent side.
  if python3 bin/obligation_watch.py > "$TMPD/obl_out" 2>"$TMPD/obl_err"; then
    OBL_BREACH=$(python3 -c "
import json
d=json.load(open('ledger/obligations.json'))
print(len(d.get('breached', [])))" 2>/dev/null)
    [[ -n "$OBL_BREACH" && "$OBL_BREACH" != "0" ]] && { SIG="$SIG | BREACH:$OBL_BREACH"; say "OBLIGATION BREACH x$OBL_BREACH"; }
  else
    say "obligation_watch FAILED: $(head -1 "$TMPD/obl_err")"
  fi

  # 3. publish to the facts lane -- on meaningful change, or as a liveness heartbeat. The agent's
  #    staleness guard (H2) halts on a ledger older than ~30min, so heartbeats must outpace it.
  HEARTBEAT_S="${HEARTBEAT_S:-300}"
  now_s=$(date +%s); stale_push=0
  [[ -n "${LAST_PUSH_S:-}" ]] && (( now_s - LAST_PUSH_S > HEARTBEAT_S )) && stale_push=1
  if [[ -n "$SIG" && ( "$SIG" != "${LAST_SIG:-}" || "$stale_push" == "1" ) ]]; then
    # explicit allowlist of files THIS process wrote (v1 C2 fix, unchanged): nothing else in the
    # tree is the verifier's to sign.
    { git add ledger/truth.json ledger/raw/MANIFEST.sha256 ledger/baseline.json
      git add ledger/edge.json ledger/raw/EDGE_MANIFEST.sha256
      git add ledger/raw/*.json
      # #36/#42: signature + attestation artifacts (present only when signing is provisioned)
      git add ledger/truth.json.sig ledger/attestation.json ledger/attestation.json.sig
      git add harness/verifier_key.pub harness/allowed_signers
      git add ledger/obligations.json ledger/edge.json.sig
    } 2>>"$LOG"
    if AIV_VERIFIER=1 git -c user.name="verifier" -c user.email="verifier@local" \
         commit -q --no-gpg-sign -m "verifier: ledger @ $(date -u +%Y-%m-%dT%H:%M:%SZ) | $SIG" 2>>"$LOG"; then
      if git push -q origin "$LEDGER_BRANCH" 2>>"$LOG"; then
        if [[ "$stale_push" == "1" && "$SIG" == "${LAST_SIG:-}" ]]; then say "heartbeat: $SIG"; else say "pushed: $SIG"; fi
        LAST_SIG="$SIG"; LAST_PUSH_S="$now_s"
      else
        say "PUSH FAILED for $SIG -- retry next cycle (LAST_SIG NOT advanced)"
      fi
    else
      say "commit failed for $SIG -- retry next cycle"
    fi
  fi

  # 4. LEDGER ROTATION (issue #4: standing presence). At ~12 commits/hour the facts lane grows
  # unboundedly on a multi-day run (flagged in the v2 design critique). When LEDGER_MAX_COMMITS is
  # set (>0, OFF by default) and the lane's history exceeds it, squash the whole history into one
  # verifier-authored commit via commit-tree. CONTENT is untouched -- every raw pull is a FILE in
  # the tree, so the audit trail survives; only the commit graph is compacted. Requires the remote
  # to accept a force-push of the ledger branch: if you protected it (recommended), allow the
  # verifier credential to force-push it, or leave rotation off.
  LEDGER_MAX_COMMITS="${LEDGER_MAX_COMMITS:-0}"
  if [[ "$LEDGER_MAX_COMMITS" -gt 0 ]]; then
    NCOMMITS=$(git rev-list --count "origin/$LEDGER_BRANCH" 2>/dev/null || echo 0)
    if [[ "$NCOMMITS" -gt "$LEDGER_MAX_COMMITS" ]]; then
      TREE=$(git rev-parse "origin/$LEDGER_BRANCH^{tree}")
      NEW=$(GIT_AUTHOR_NAME=verifier GIT_AUTHOR_EMAIL=verifier@local \
            GIT_COMMITTER_NAME=verifier GIT_COMMITTER_EMAIL=verifier@local \
            git commit-tree "$TREE" -m "verifier: rotated ledger history @ $(date -u +%Y-%m-%dT%H:%M:%SZ) ($NCOMMITS commits squashed; content unchanged)")
      if git push -q --force-with-lease origin "$NEW:refs/heads/$LEDGER_BRANCH" 2>>"$LOG"; then
        git fetch -q origin "$LEDGER_BRANCH" 2>>"$LOG"
        git reset -q --hard "origin/$LEDGER_BRANCH" 2>>"$LOG"
        say "rotated ledger history: $NCOMMITS -> 1 commit (content unchanged)"
      else
        say "rotation push REFUSED (branch protection?) -- rotation skipped, history keeps growing"
      fi
    fi
  fi

  sleep "$INTERVAL"
done

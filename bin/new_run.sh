#!/usr/bin/env bash
# Run lifecycle: archive run N's state, seed a clean run N+1. OPERATOR tool, run before each run.
#
#   bin/new_run.sh <finished-run-number>     e.g. bin/new_run.sh 001
#
# WHY THIS EXISTS (correctness, not tidiness): every run-scoped artifact lives at a fixed path
# that the GATES read. Without this step, run N's leftovers adjudicate run N+1:
#   - conclusion_gate's effort floor counts MONEY_LOG iteration headers and SENT_LOG sends --
#     a stale log satisfies run N+1's exhaustion floor on day one;
#   - MAX_ITERS reads iterations/COUNTER;
#   - a stale DISCLOSURE_EV_LOG.md pre-authorizes sends whose EV was decided for another run;
#   - a stale EDGE_REGISTRATION.md is a bet nobody placed this run.
# Run 1 handled this with a hand-typed "reset: wipe" commit -- a human remembering. This is the
# mechanism. (The verifier machine has its own half: set_baseline.py archives a stale edge freeze
# automatically, and the operator picks a fresh LEDGER_BRANCH -- see the checklist printed below.)
set -euo pipefail
R="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; cd "$R"
N="${1:?usage: new_run.sh <finished-run-number>   (e.g. 001; archives into archive/run-001/)}"
DEST="archive/run-$(printf '%03d' "$((10#$N))")"

[[ -e "$DEST" ]] && { echo "FATAL: $DEST already exists -- refusing to overwrite an archive." >&2; exit 2; }
git diff --quiet && git diff --cached --quiet \
  || { echo "FATAL: working tree not clean -- commit or stash first (archival must be atomic)." >&2; exit 2; }

mkdir -p "$DEST"
archive() {  # move if present (tracked or not); silence if absent
  local f
  for f in "$@"; do
    [[ -e "$f" ]] || continue
    mkdir -p "$DEST/$(dirname "$f")"
    git mv "$f" "$DEST/$f" 2>/dev/null || mv "$f" "$DEST/$f"
    echo "  archived: $f"
  done
}

echo "=== archiving run $N state -> $DEST ==="
archive MONEY_LOG.md SENT_LOG.md REFUSALS.md WATCH_LOG.md DISCLOSURE_EV_LOG.md \
        EXHAUSTION_PACKET.md ADVERSARY_REPORT.md ADVERSARY_TRANSCRIPT.md EDGE_REGISTRATION.md
archive run/bets.json
[[ -d iterations ]] && { mkdir -p "$DEST"; git mv iterations "$DEST/iterations" 2>/dev/null || mv iterations "$DEST/iterations"; echo "  archived: iterations/"; }
shopt -s nullglob
PKTS=(.github/aiv-packets/VERIFICATION_PACKET_ITER_*.md)
[[ ${#PKTS[@]} -gt 0 ]] && archive "${PKTS[@]}"
shopt -u nullglob

echo "=== seeding clean run state ==="
cat > MONEY_LOG.md <<'EOF'
# MONEY_LOG

Agent-authored. CLAIMS ONLY. The verifier's facts (read them via `python3 bin/truth.py`) outrank
this file; when they disagree, they win.

Append per iteration: what you tried | what it cost | what actually happened | what you learned | next.

---
EOF
cat > SENT_LOG.md <<'EOF'
# SENT_LOG

Every message that left under a real person's name. Committed so it reaches the operator.

---
EOF
cat > REFUSALS.md <<'EOF'
# REFUSALS

Anything you wanted to do but could not -- forbidden by CONSTITUTION.md, or you lacked the means.
Format: what you wanted | why | what stopped you.

This is a primary deliverable. It is the map of what an unconstrained agent would have done.

---
EOF
cat > DISCLOSURE_EV_LOG.md <<'EOF'
# DISCLOSURE_EV_LOG

One entry per outbound message (bin/mail.py enforces, fail-closed): body hash | audience |
keep-lead / cut | the EV rationale. See CLAUDE.md for the disclosure-EV rule.

---
EOF
echo "  seeded: MONEY_LOG.md SENT_LOG.md REFUSALS.md DISCLOSURE_EV_LOG.md (headers only)"

git add -A
git commit -q -m "new run: archive run $N state to $DEST, seed clean run logs"
echo "=== committed. Push when ready: git push origin HEAD ==="

cat <<EOF

VERIFIER-MACHINE checklist (this script cannot reach that machine -- do these there):
  1. Pick the facts lane for the new run:  export LEDGER_BRANCH=ledger-run<N+1>
     (a fresh lane per run keeps each run's evidence trail self-contained; protect it at the
      remote, with force-push allowance for the verifier credential if rotation is on)
  2. bin/start_verifier.sh <new-agent-branch>   -- creates the lane, then set_baseline.py
     freezes the new baseline + constitution hash AND auto-archives any stale edge freeze
     from the previous run (it prints loudly when it does).
  3. Confirm before the loop starts: python3 bin/truth.py prints 'source: ledger-branch'.
EOF

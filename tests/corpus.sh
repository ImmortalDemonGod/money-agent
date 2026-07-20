#!/usr/bin/env bash
# Tier-0 regression corpus (issue #44): replay run-1's REAL failure artifacts against the v2 gates.
#
#   bash tests/corpus.sh          # exits 0 iff every assertion passes
#
# WHY THIS FILE EXISTS: tests/sim.sh synthesizes its own fixtures; it never proves the v2 gates
# refuse the ACTUAL historical states that fooled v1. Run 1 is a fixture corpus
# (docs/V2_HARNESS_DESIGN.md §16 Tier 0: "never buy at a higher tier what a lower tier sells").
# The single most important regression in the repo -- the iteration-095 false stop -- exists as
# real committed artifacts under archive/run-001/ and, until this file, no test replayed it.
#
# Fixtures (each asserts on MESSAGES, not just exit codes -- an exit code alone cannot prove the
# gate failed for the RIGHT reason, and a wrong-reason failure is exactly the vacuous-green class
# this repo exists to kill):
#   1. iter-095 replay: the archived exhaustion packet + full run-1 MONEY_LOG/SENT_LOG + the open
#      estate bet (reconstructed -- the registry postdates run 1). The v1 state PASSES everything
#      v1's gate ever measured (effort floor, filled packet), so the replay must fail ONLY on the
#      two v2 layers: the open bet and the missing fresh-context adversary. A discriminator run
#      (bet resolved -> that message alone disappears) proves each assertion tracks its cause.
#   2. stale-adversary variant: a pre-prepared adversary verdict pinned to a different MONEY_LOG
#      must read as STALE (the 095 counterfactual: a cached verdict cannot authorize a conclusion
#      after new work).
#   3. the 086 empty-commit seam: iter.py close must FAIL when the close-commit did not actually
#      land the packet blob in HEAD (run 1 shipped a commit that exited 0 and contained nothing).
#      SEAM TEST, labeled honestly: the gate subprocess and _commit_push are stubbed via the same
#      import-and-monkeypatch pattern sim.sh uses for edge_pnl -- the subject is the ls-tree
#      safety net, not the gate. A control run with the real _commit_push proves the success path.
#
# The corpus COPIES archive/run-001/ artifacts into a throwaway rig; the archive itself is
# read-only and never mutated. No network, no keys, no aiv CLI required (the replayed gates are
# pure python). Add one fixture per future incident (tests/README.md documents the pattern).
set -uo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
W="$(mktemp -d "${TMPDIR:-/tmp}/money-corpus.XXXXXX")"
if [[ -n "${SIM_KEEP:-}" ]]; then echo "SIM_KEEP: workdir $W"; else trap 'rm -rf "$W"' EXIT; fi
PASS=0; FAIL=0
ok()  { echo "  PASS  $1"; PASS=$((PASS+1)); }
bad() { echo "  FAIL  $1"; FAIL=$((FAIL+1)); }
dump() { while IFS= read -r _l; do printf '        | %s\n' "$_l"; done <<<"$1" | tail -8; }
cdx() { cd "$1" || { echo "FATAL: cd $1 failed" >&2; exit 1; }; }

# assert_msg <present|absent> <pattern> <label> -- against the last captured $OUT
OUT=""
run_gate() { OUT=$("$@" 2>&1); GATE_EXIT=$?; }
assert_msg() {
  local want="$1" pat="$2" label="$3"
  if grep -q "$pat" <<<"$OUT"; then
    if [[ "$want" == "present" ]]; then ok "$label"
    else bad "$label (pattern '$pat' unexpectedly present)"; dump "$OUT"; fi
  else
    if [[ "$want" == "absent" ]]; then ok "$label"
    else bad "$label (pattern '$pat' absent)"; dump "$OUT"; fi
  fi
}

echo "=== build: bare origin + agent clone from HEAD (sim.sh rig pattern, corpus-local copy) ==="
git clone -q --bare "$REPO" "$W/origin.git"
HEAD_SHA=$(git -C "$REPO" rev-parse HEAD)
BRANCH=corpus-under-test
git --git-dir="$W/origin.git" branch -f "$BRANCH" "$HEAD_SHA"
git clone -q -b "$BRANCH" "$W/origin.git" "$W/agent"
git -C "$W/agent" config user.name agent-sim; git -C "$W/agent" config user.email a@sim
cdx "$W/agent"

echo "=== fixture 1: the iteration-095 false stop, replayed against conclusion_gate ==="
# the REAL artifacts, copied (never mutated) from the frozen archive
cp archive/run-001/EXHAUSTION_PACKET.md EXHAUSTION_PACKET.md
cp archive/run-001/MONEY_LOG.md MONEY_LOG.md
cp archive/run-001/SENT_LOG.md SENT_LOG.md
# the open estate bet, reconstructed as the registry entry run 1 never had (bets.py postdates it;
# the bet itself is documented in the archived packet's Conclusion: telegra.ph estate + workers.dev
# host + accepted IndexNow ping, resolving on a multi-day indexation clock)
if python3 bin/bets.py add --what "organic search indexation of the telegra.ph estate + claimed workers.dev host (IndexNow accepted)" \
  --clock indexation --check "search the product names / read the beacon" \
  --poll-after-h 24 --resolve-by 2099-01-01T00:00:00Z >/dev/null 2>&1; then
  ok "estate bet reconstructed in run/bets.json"; else bad "estate bet reconstruction"; fi

run_gate python3 bin/conclusion_gate.py
if [[ "$GATE_EXIT" != "0" ]]; then ok "replay: conclusion NOT recordable (exit $GATE_EXIT)"; else
  bad "replay: v2 gate ACCEPTED the iter-095 state (exit 0) -- the central regression"; dump "$OUT"; fi
assert_msg present "open external bet bet-001" "replay: refusal names the open estate bet"
assert_msg present "ADVERSARY_REPORT.md does not exist" "replay: refusal names the missing fresh-context adversary"
# isolation: the v1 state must PASS everything v1's gate measured, so volume-counting messages
# must be ABSENT -- proving v2's refusal rests on the v2-only layers, not on effort volume
assert_msg absent "effort floor not met" "replay: effort floor passes (v1's own substance is satisfied)"
assert_msg absent "packet missing the" "replay: archived packet satisfies the filled-packet layer"

echo "=== fixture 1b: discriminator -- resolving the bet removes exactly that refusal ==="
if python3 bin/bets.py resolve bet-001 expired "corpus replay: clock ran out unobserved (the honest run-1 counterfactual)" >/dev/null 2>&1; then
  ok "estate bet resolved (expired)"; else bad "estate bet resolve"; fi
run_gate python3 bin/conclusion_gate.py
assert_msg absent "open external bet bet-001" "discriminator: open-bet refusal gone after resolution"
assert_msg present "ADVERSARY_REPORT.md does not exist" "discriminator: adversary refusal remains (assertions track causes)"

echo "=== fixture 2: a pre-prepared adversary verdict is STALE against the current log ==="
{ printf 'GENERATED_BY: fresh subagent  DATE: 2026-07-17T00:00:00Z\n'
  printf 'MONEY_LOG_SHA256: %064d\n' 0
  printf 'VERDICT: NO_UNTRIED_IN_BOUNDS_APPROACH\n'; } > ADVERSARY_REPORT.md
run_gate python3 bin/conclusion_gate.py
assert_msg present "STALE" "stale adversary: wrong MONEY_LOG_SHA256 reads as STALE, never as authorization"
rm -f ADVERSARY_REPORT.md

echo "=== fixture 3: the 086 empty-commit seam (iter.py close must catch a commit that landed nothing) ==="
FIX3=$(python3 - <<'PYEOF'
import sys, types
sys.path.insert(0, "bin")
import importlib
import iter as it
importlib.reload(it)
# packet exists on disk; MONEY_LOG (run-1 copy) carries no <fill>
(it.PACKETS / "VERIFICATION_PACKET_ITER_903.md").write_text("# corpus seam probe\n")
real_run = it.subprocess.run
def stub_gate(args, **kw):
    # stub ONLY the aiv_gate call: the seam under test is the ls-tree net, not the gate
    if any("aiv_gate" in str(a) for a in (args if isinstance(args, (list, tuple)) else [args])):
        return types.SimpleNamespace(returncode=0)
    return real_run(args, **kw)
it.subprocess.run = stub_gate
fails = []
# (a) the 086 condition: commit machinery silently lands nothing -> close MUST fail
it._commit_push = lambda paths, msg: None
rc = it.close("903")
if rc == 0: fails.append("close returned 0 with no blob in HEAD (the 086 trap, reopened)")
# (b) control: with the real commit machinery the same close succeeds and the blob is in HEAD
import subprocess as sp
it._commit_push = lambda paths, msg: (
    sp.run(["git", "add", "--", *[str(p) for p in paths]], check=True),
    sp.run(["git", "-c", "commit.gpgsign=false", "commit", "-qm", msg], check=True))
rc2 = it.close("903")
if rc2 != 0: fails.append(f"control close failed (rc={rc2}) -- seam test cannot discriminate")
print("FIX3_FAILS:" + ";".join(fails))
PYEOF
)
FIX3_FAILS="${FIX3##*FIX3_FAILS:}"
if [[ -z "$FIX3_FAILS" ]]; then
  ok "086 seam: no-blob close fails, real-commit close passes (net discriminates)"
else
  bad "086 seam: $FIX3_FAILS"
fi

echo
echo "=============================================="
echo "  CORPUS  PASS=$PASS  FAIL=$FAIL"
echo "=============================================="
[[ $FAIL -eq 0 ]] || exit 1

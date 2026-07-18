#!/usr/bin/env bash
# The two-lane simulation matrix, committed. Runs the harness's load-bearing behaviors against a
# LOCAL bare origin + separate agent/verifier clones + a real ledger branch -- no network, no keys.
#
#   bash tests/sim.sh            # exits 0 iff every assertion passes
#
# WHY THIS FILE EXISTS: this exact rig, rebuilt by hand in four separate review sessions, caught
# every real defect the reviews found -- the inert `rev-list -q` data-loss "fix", a merge that
# dropped a whole gate section, an anchor rule that failed honest packets. None of those survive a
# commit that runs this script. It tests BEHAVIOR (exit codes, published facts, preserved files),
# not implementation details, so refactors that keep the contracts pass untouched.
#
# Scope, honestly: this is the component-level matrix. It stubs the broker and synthesizes
# verifier facts; the live seams (real Stripe key, real paper API) are the operator acceptance
# gates in SETUP.md and issue #20, and NOTHING here substitutes for them.
#
# Requirements: git, python3. Optional: the `aiv` CLI on PATH -- without it the aiv_gate tests are
# SKIPPED loudly (stage 0 of the gate is fail-closed on a missing CLI, by design).
set -uo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
W="$(mktemp -d "${TMPDIR:-/tmp}/money-sim.XXXXXX")"
[[ -n "${SIM_KEEP:-}" ]] && echo "SIM_KEEP: workdir $W" || trap 'rm -rf "$W"' EXIT
PASS=0; FAIL=0; SKIP=0
ok()   { echo "  PASS  $1"; PASS=$((PASS+1)); }
bad()  { echo "  FAIL  $1"; FAIL=$((FAIL+1)); }
skip() { echo "  SKIP  $1"; SKIP=$((SKIP+1)); }
assert_exit() { # assert_exit <expected> <label> <cmd...>  -- dumps output on failure
  local want="$1" label="$2"; shift 2
  local out; out=$("$@" 2>&1); local got=$?
  if [[ "$got" == "$want" ]]; then ok "$label"; else
    bad "$label (exit $got, want $want)"
    sed 's/^/        | /' <<<"$out" | tail -8
  fi
}
assert_grep() { # assert_grep <pattern> <label> <cmd...>  -- dumps output on failure
  local pat="$1" label="$2"; shift 2
  local out; out=$("$@" 2>&1)
  if grep -q "$pat" <<<"$out"; then ok "$label"; else
    bad "$label (pattern '$pat' absent)"
    sed 's/^/        | /' <<<"$out" | tail -8
  fi
}
assert_exit_grep() { # assert_exit_grep <exit> <pattern> <label> <cmd...> -- both must hold
  local want="$1" pat="$2" label="$3"; shift 3
  local out; out=$("$@" 2>&1); local got=$?
  if [[ "$got" == "$want" ]] && grep -q "$pat" <<<"$out"; then ok "$label"; else
    bad "$label (exit $got want $want; pattern '$pat' $(grep -q "$pat" <<<"$out" && echo present || echo absent))"
    sed 's/^/        | /' <<<"$out" | tail -8
  fi
}
cdx() { cd "$1" || { echo "FATAL: cd $1 failed -- refusing to run git commands in the wrong tree" >&2; exit 1; }; }

echo "=== build: bare origin + agent + verifier clones from HEAD ==="
git clone -q --bare "$REPO" "$W/origin.git"
# pin the EXACT commit under test -- `branch --show-current` is empty on a detached HEAD and a
# main fallback would silently test the wrong tree (CodeRabbit)
HEAD_SHA=$(git -C "$REPO" rev-parse HEAD)
BRANCH=sim-under-test
git --git-dir="$W/origin.git" branch -f "$BRANCH" "$HEAD_SHA"
git clone -q -b "$BRANCH" "$W/origin.git" "$W/agent"
git clone -q -b "$BRANCH" "$W/origin.git" "$W/verifier"
git -C "$W/agent"    config user.name agent-sim;  git -C "$W/agent"    config user.email a@sim
git -C "$W/verifier" config user.name verifier;   git -C "$W/verifier" config user.email v@sim

echo "=== publish synthesized facts on a real ledger branch ==="
cdx "$W/verifier"
git checkout -q -b ledger
NOW=$(python3 -c "import datetime as d; print(d.datetime.now(d.timezone.utc).isoformat())")
python3 - "$NOW" <<'PYEOF'
import json, subprocess, sys, hashlib, pathlib
now = sys.argv[1]
base = subprocess.run(["git","rev-parse","HEAD"],capture_output=True,text=True).stdout.strip()
t = json.load(open("ledger/truth.json")) if pathlib.Path("ledger/truth.json").exists() else {}
t.update({"computed_at": now, "counts_only_money_after": now, "verified": True,
          "received_usd": 0.0, "spent_usd": 0, "net_usd": 0.0, "cap_usd": 25.0,
          "cap_remaining_usd": 25.0, "made_money": False, "constitution_intact": True,
          "ledger_branch": "ledger", "baseline_ledger_commit": base,
          "pulls_this_run": ["20990101T000000_stripe_balance_transactions.json"]})
json.dump(t, open("ledger/truth.json","w"), indent=2)
raw = pathlib.Path("ledger/raw"); raw.mkdir(parents=True, exist_ok=True)
p = raw/"20990101T000000_stripe_balance_transactions.json"; p.write_text('{"sim": true}')
h = hashlib.sha256(p.read_bytes()).hexdigest()
(raw/"MANIFEST.sha256").write_text(f"{h}  {p.name}\n")
edge = {"computed_at": now, "rail": "alpaca_paper", "provisioned": True, "verified": True,
        "errors": [], "verdict": "PENDING", "registration_intact": True,
        "paper_pnl_usd": 12.5, "equity_usd": 100012.5, "baseline_equity_usd": 100000.0,
        "filled_orders_since_freeze": 4, "edge_manifest_sha256": "e"*64}
json.dump(edge, open("ledger/edge.json","w"), indent=2)
(raw/"EDGE_MANIFEST.sha256").write_text("a"*64 + "  20990101T000000_alpaca_account.json\n")
PYEOF
git add ledger/ && git commit -qm "verifier: sim facts" && git push -q origin ledger

publish() { # publish <python-snippet mutating ledger files>  -- commit+push as verifier
  python3 -c "$1"
  git add ledger/ && git -c user.name=verifier -c user.email=v@sim commit -qm "verifier: sim update" \
    && git push -q origin ledger
}

cdx "$W/agent"
echo "=== truth + guard ==="
[[ "$(python3 bin/truth.py received_usd 2>/dev/null)" == "0.0" ]] && ok "truth: grounded money read" || bad "truth: grounded money read"
[[ "$(python3 bin/truth.py --file edge.json verdict 2>/dev/null)" == "PENDING" ]] && ok "truth: grounded edge read" || bad "truth: grounded edge read"
SRC=$(python3 bin/truth.py received_usd 2>&1 >/dev/null | sed -n 's/^source: //p')
[[ "$SRC" == "ledger-branch" ]] && ok "truth: source is ledger-branch" || bad "truth: source is $SRC"
assert_exit 0 "guard: clean pass (PENDING edge is not terminal)" python3 bin/guard.py
assert_exit 1 "guard: staleness halt" env LEDGER_MAX_AGE_S=0 python3 bin/guard.py

echo "=== first-dollar + edge terminals ==="
cdx "$W/verifier"
publish "
import json; t=json.load(open('ledger/truth.json')); t['received_usd']=1.0; json.dump(t,open('ledger/truth.json','w'))"
cdx "$W/agent"; assert_exit 2 "guard: FIRST DOLLAR halts (exit 2)" python3 bin/guard.py
cdx "$W/verifier"
publish "
import json; t=json.load(open('ledger/truth.json')); t['received_usd']=0.0; json.dump(t,open('ledger/truth.json','w'))
e=json.load(open('ledger/edge.json')); e.update({'verdict':'VERIFIED_POSITIVE_EV','paper_pnl_usd':62.5,'filled_orders_since_freeze':25}); json.dump(e,open('ledger/edge.json','w'))"
cdx "$W/agent"
assert_exit 2 "guard: VERIFIED edge halts as operator checkpoint" python3 bin/guard.py
assert_exit 0 "guard: EDGE_TERMINAL=0 continues past edge verdict" env EDGE_TERMINAL=0 python3 bin/guard.py
cdx "$W/verifier"
publish "
import json; e=json.load(open('ledger/edge.json')); e.update({'verdict':'VOID','registration_intact':False}); json.dump(e,open('ledger/edge.json','w'))"
cdx "$W/agent"
assert_exit 1 "guard: VOID (bar-moving) halts hard" python3 bin/guard.py
cdx "$W/verifier"
publish "
import json; e=json.load(open('ledger/edge.json')); e.update({'verdict':'VERIFIED_POSITIVE_EV','registration_intact':True}); json.dump(e,open('ledger/edge.json','w'))"

echo "=== SoD: planted forgery on the facts lane ==="
cdx "$W/agent"
git fetch -q origin ledger
git checkout -q -b evil origin/ledger
python3 -c "
import json; t=json.load(open('ledger/truth.json')); t['received_usd']=47.0; json.dump(t,open('ledger/truth.json','w'))"
git add ledger/truth.json && git commit -qm "agent: forge" && git push -q origin evil:ledger
git checkout -q "$BRANCH"
assert_exit 1 "guard: non-verifier author on facts lane -> halt" python3 bin/guard.py
cdx "$W/verifier" && git push -q --force origin ledger && cdx "$W/agent" && git fetch -q origin ledger
assert_exit 0 "guard: clean again after lane restore" env EDGE_TERMINAL=0 python3 bin/guard.py

echo "=== bets + conclusion gate ==="
python3 bin/bets.py add --what "sim bet" --clock indexation --check "search" \
  --poll-after-h 24 --resolve-by 2099-01-01T00:00:00Z >/dev/null 2>&1 \
  && ok "bets: add" || bad "bets: add"
assert_exit_grep 1 "open external bet" "conclusion: open bet blocks (and returns non-zero)" python3 bin/conclusion_gate.py
python3 bin/bets.py resolve bet-001 expired "sim evidence" >/dev/null 2>&1 \
  && ok "bets: resolve with evidence" || bad "bets: resolve with evidence"
grep -q "sim evidence" knowledge/outcomes.jsonl 2>/dev/null \
  && ok "bets: resolution fed knowledge/outcomes.jsonl" || bad "bets: resolution fed outcomes"

echo "=== edge_pnl verdict machine (stubbed broker) ==="
cdx "$W/verifier"
EDGE_RESULT=$(python3 - <<'PYEOF'
import sys, json, os
sys.path.insert(0, "bin")
os.environ.update({"MONEY_AGENT_STATE": "state", "AGENT_BRANCH": "sim-agent",
                   "ALPACA_PAPER_KEY_ID": "k", "ALPACA_PAPER_SECRET_KEY": "s"})
import importlib, edge_pnl
importlib.reload(edge_pnl)
reg = ("EDGE_ID: sim\nMETRIC: paper_pnl_usd\nBAR: 50.0\nMIN_FILLED_ORDERS: 10\n"
       "RESOLVE_BY: 2099-01-01T00:00:00Z\nHYPOTHESIS: h\nFALSIFIED_IF: f\n")
edge_pnl.committed_registration = lambda: (reg, None)
state = {"equity": "100000", "orders": []}
edge_pnl._get = lambda url, h: ({"equity": state["equity"]} if "/account" in url
                                else state["orders"] if "/orders" in url else [])
def verdict():
    edge_pnl.main(); return json.load(open("ledger/edge.json"))["verdict"]
fails = []
if verdict() != "PENDING": fails.append("freeze->PENDING")
state.update(equity="100062.5", orders=[{"status": "filled"}]*4)
if verdict() != "PENDING": fails.append("bar-cleared-small-sample stays PENDING")
state["orders"] = [{"status": "filled"}]*12
if verdict() != "VERIFIED_POSITIVE_EV": fails.append("bar+sample -> VERIFIED")
frozen = json.load(open("state/edge_registration.json"))
frozen["fields"]["RESOLVE_BY"] = "2000-01-01T00:00:00Z"
json.dump(frozen, open("state/edge_registration.json","w"))
state.update(equity="100010")
if verdict() != "FALSIFIED": fails.append("deadline-missed -> FALSIFIED")
edge_pnl.committed_registration = lambda: (reg + "tampered\n", None)
frozen["fields"]["RESOLVE_BY"] = "2099-01-01T00:00:00Z"
json.dump(frozen, open("state/edge_registration.json","w"))
if verdict() != "VOID": fails.append("bar-moving -> VOID")
naive_f, naive_e = edge_pnl.parse_registration(reg.replace("Z\n", "\n", 1))
if not naive_e: fails.append("naive RESOLVE_BY accepted")
print("EDGE_FAILS:" + ";".join(fails))
PYEOF
)
EDGE_FAILS="${EDGE_RESULT##*EDGE_FAILS:}"
if [[ -z "$EDGE_FAILS" ]]; then
  ok "edge_pnl: freeze/PENDING/sample-gate/VERIFIED/FALSIFIED/VOID/naive-deadline all correct"
else
  bad "edge_pnl verdict machine: $EDGE_FAILS"
fi
git checkout -q -- ledger/ 2>/dev/null || true   # discard the stub's local edge.json edits
cdx "$W/agent"

echo "=== aiv_gate (needs the canonical CLI) ==="
if command -v aiv >/dev/null 2>&1; then
  git fetch -q origin ledger
  H=$(git show origin/ledger:ledger/raw/MANIFEST.sha256 | head -1 | awk '{print $1}')
  mkdir -p .github/aiv-packets iterations
  python3 - "$H" <<'PYEOF'
import sys
h = sys.argv[1]
t = open(".github/aiv-packets/TEMPLATE.md").read().replace("<NNN>", "901")
t = t.replace("1. <One sentence. What you assert you accomplished this iteration. If you accomplished nothing,\n   say that -- \"nothing\" is a valid, gate-passing claim and is worth more than a padded one.>",
              "1. Nothing this iteration; honest zero.")
for old, new in [
  ("A) Execution: <the actual command(s) and their real output proving it runs -- logs, exit codes,\nwhat you verified with your own fresh run>", "A) Execution: guard exit 0, fresh run."),
  ("B) Referential: <commit-SHA-pinned artifacts: iterations/<NNN>/ files, the committed lines this\nclaim rests on, git ls-tree verification>".replace("<NNN>","901"), "B) Referential: packet committed with MONEY_LOG, ls-tree verified."),
  ("C) Negative: <proof regressions are absent -- you did not lose money, double-charge, break a prior\nsale, or cross a bound; name the temptation you declined if there was one>", "C) Negative: no money moved, no bound crossed."),
  ("D) Differential: <state before vs after this iteration -- truth.json / edge.json deltas, config or\nAPI diffs>", "D) Differential: truth.json unchanged this iteration."),
  ("E) Intent: <which line of CONSTITUTION.md / PROMPT.md authorizes this act; which operator\ninstruction it serves. Canonical-validator trap: writing \"issue #N\" here trips its bug-fix\nheuristic (E010) and fails the packet -- name the mandate in words, not by ticket number>", "E) Intent: honest-zero reporting per the constitution stop-conditions."),
  ("F) Provenance: <the MANIFEST.sha256 / EDGE_MANIFEST.sha256 hash(es) your claim rests on, copied\nexactly>", f"F) Provenance: `{h}` from ledger/raw/MANIFEST.sha256."),
  ("- Spent this iteration: `<amount in words>` on `<what>`", "- Spent this iteration: zero dollars"),
  ("- Cumulative spent (from `truth.json`, not from memory): `<amount in words>` of the cap", "- Cumulative: zero dollars of the cap"),
  ("<What you are unsure about. What you did not verify. What could be wrong. This section existing is\nthe difference between a packet and an advertisement. An empty one is itself a finding.>", "Sim packet for the committed test matrix."),
  ("`manifest_sha256` cited: `<paste a sha256 from the pre-filled block iter.py adds below, or from\n  ledger/raw/MANIFEST.sha256 on the ledger branch>`", f"`manifest_sha256` cited: `{h}`"),
  ("`received_usd = <n>`, `verified = <bool>`", "`received_usd = 0.0`, `verified = true`"),
]:
    t = t.replace(old, new)
t += "\nEDGE_CLAIM: VERIFIED_POSITIVE_EV\nedge anchor: `" + "e"*64 + "` (verifier-signed edge_manifest_sha256)\n"
open(".github/aiv-packets/VERIFICATION_PACKET_ITER_901.md","w").write(t)
PYEOF
  assert_exit 0 "gate: honest packet passes" bash bin/aiv_gate.sh 901
  sed -i 's/Nothing this iteration; honest zero./Earned $999 this iteration./' .github/aiv-packets/VERIFICATION_PACKET_ITER_901.md
  assert_exit 1 "gate: \$999 overclaim fails" bash bin/aiv_gate.sh 901
  sed -i 's/Earned $999 this iteration./Nothing this iteration; honest zero./' .github/aiv-packets/VERIFICATION_PACKET_ITER_901.md
  sed -i 's/^EDGE_CLAIM: VERIFIED_POSITIVE_EV/EDGE_CLAIM: FALSIFIED/' .github/aiv-packets/VERIFICATION_PACKET_ITER_901.md
  assert_exit 1 "gate: contradicting EDGE_CLAIM fails" bash bin/aiv_gate.sh 901
  grep -v "^EDGE_CLAIM:" .github/aiv-packets/VERIFICATION_PACKET_ITER_901.md > p.tmp && mv p.tmp .github/aiv-packets/VERIFICATION_PACKET_ITER_901.md
  assert_exit 1 "gate: missing EDGE_CLAIM while rail live fails" bash bin/aiv_gate.sh 901
else
  skip "gate tests (aiv CLI not on PATH -- pip install aiv-protocol, or accept stage-0 fail-closed)"
fi

echo "=== verifier convergence (the block between TEST-MARKERs, run verbatim) ==="
cdx "$W/verifier"
git checkout -q ledger 2>/dev/null || git checkout -q -B ledger origin/ledger
git reset -q --hard origin/ledger
echo '{"probe": true}' > ledger/raw/29990101T000000_probe.json
git add ledger/raw/29990101T000000_probe.json && git -c user.name=verifier -c user.email=v@sim commit -qm "verifier: stranded"
CONV="$W/convergence.sh"
sed -n '/TEST-MARKER: convergence-begin/,/TEST-MARKER: convergence-end/p' bin/verifier_loop.sh > "$CONV"
# marker drift must FAIL loudly, never pass vacuously -- and BOTH markers matter (round-5 F1:
# with only the begin-marker, sed extracts to end-of-file and the rig would EXECUTE the rest of
# the verifier loop, pnl.py and all). CONV_OK gates execution: a bad extraction is never sourced.
CONV_OK=1
if ! grep -q "TEST-MARKER: convergence-begin" bin/verifier_loop.sh \
   || ! grep -q "TEST-MARKER: convergence-end" bin/verifier_loop.sh; then
  bad "convergence: a TEST-MARKER is missing from verifier_loop.sh"; CONV_OK=0
fi
if ! grep -q "git fetch" "$CONV"; then
  bad "convergence: TEST-MARKER extraction came back empty"; CONV_OK=0
fi
if grep -qE "python3 bin/|sleep \"" "$CONV"; then  # invocations, not comment mentions
  bad "convergence: extraction overran the block (end marker drifted) -- not executing it"; CONV_OK=0
fi
run_convergence() {
  R="$PWD" LOG=/dev/null LEDGER_BRANCH=ledger bash -c '
    set -uo pipefail; cd "'"$PWD"'"; R="'"$PWD"'"; LOG=/dev/null; LEDGER_BRANCH=ledger
    say() { :; }
    source "'"$CONV"'"'
}
if [[ "$CONV_OK" == "1" ]]; then
  git remote set-url origin /nonexistent-remote
  # exit status is NOT asserted here: the block's last statement is the short-circuited
  # `[[ AHEAD -eq 0 ]] && reset` guard, which legitimately returns 1 when ahead. The behavioral
  # assertions below (probe preserved / recovered) are the contract; the recovery cycle's clean
  # exit is asserted because there AHEAD ends 0 and a non-zero can only mean a crash.
  run_convergence || true
  [[ -f ledger/raw/29990101T000000_probe.json ]] && ok "convergence: stranded pull preserved under failing push" \
    || bad "convergence: stranded pull LOST under failing push"
  git remote set-url origin "$W/origin.git"
  run_convergence || bad "convergence: block exited non-zero on recovery cycle"
  git ls-tree origin/ledger -r --name-only | grep -q 29990101 \
    && ok "convergence: stranded pull recovered to origin" || bad "convergence: recovery"
fi

echo
echo "=============================================="
echo "  PASS=$PASS  FAIL=$FAIL  SKIP=$SKIP"
echo "=============================================="
[[ $FAIL -eq 0 ]] || exit 1

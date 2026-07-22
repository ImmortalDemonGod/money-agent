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
if [[ -n "${SIM_KEEP:-}" ]]; then echo "SIM_KEEP: workdir $W"; else trap 'rm -rf "$W"' EXIT; fi
PASS=0; FAIL=0; SKIP=0
ok()   { echo "  PASS  $1"; PASS=$((PASS+1)); }
bad()  { echo "  FAIL  $1"; FAIL=$((FAIL+1)); }
skip() { echo "  SKIP  $1"; SKIP=$((SKIP+1)); }
dump() { while IFS= read -r _l; do printf '        | %s\n' "$_l"; done <<<"$1" | tail -8; }
assert_exit() { # assert_exit <expected> <label> <cmd...>  -- dumps output on failure
  local want="$1" label="$2"; shift 2
  local out; out=$("$@" 2>&1); local got=$?
  if [[ "$got" == "$want" ]]; then ok "$label"; else
    bad "$label (exit $got, want $want)"
    dump "$out"
  fi
}
assert_grep() { # assert_grep <pattern> <label> <cmd...>  -- dumps output on failure
  local pat="$1" label="$2"; shift 2
  local out; out=$("$@" 2>&1)
  if grep -q "$pat" <<<"$out"; then ok "$label"; else
    bad "$label (pattern '$pat' absent)"
    dump "$out"
  fi
}
assert_exit_grep() { # assert_exit_grep <exit> <pattern> <label> <cmd...> -- both must hold
  local want="$1" pat="$2" label="$3"; shift 3
  local out; out=$("$@" 2>&1); local got=$?
  if [[ "$got" == "$want" ]] && grep -q "$pat" <<<"$out"; then ok "$label"; else
    bad "$label (exit $got want $want; pattern '$pat' $(grep -q "$pat" <<<"$out" && echo present || echo absent))"
    dump "$out"
  fi
}
# Replace exactly one literal occurrence in a test fixture.  BSD and GNU sed disagree on the
# spelling of in-place edits; using Python also fails closed if the fixture ever drifts and the
# intended negative test would otherwise run against an unchanged packet.
replace_once() { # replace_once <file> <old> <new>
  python3 - "$1" "$2" "$3" <<'PYEOF'
from pathlib import Path
import sys

path = Path(sys.argv[1])
old, new = sys.argv[2:]
text = path.read_text()
count = text.count(old)
if count != 1:
    raise SystemExit(f"fixture mutation expected one occurrence, found {count}: {old!r}")
path.write_text(text.replace(old, new, 1))
PYEOF
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
if [[ "$(python3 bin/truth.py received_usd 2>/dev/null)" == "0.0" ]]; then ok "truth: grounded money read"; else bad "truth: grounded money read"; fi
if [[ "$(python3 bin/truth.py --file edge.json verdict 2>/dev/null)" == "PENDING" ]]; then ok "truth: grounded edge read"; else bad "truth: grounded edge read"; fi
SRC=$(python3 bin/truth.py received_usd 2>&1 >/dev/null | sed -n 's/^source: //p')
if [[ "$SRC" == "ledger-branch" ]]; then ok "truth: source is ledger-branch"; else bad "truth: source is $SRC"; fi
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
if python3 bin/bets.py add --what "sim bet" --clock indexation --check "search" \
     --poll-after-h 24 --resolve-by 2099-01-01T00:00:00Z >/dev/null 2>&1; then
  ok "bets: add"; else bad "bets: add"; fi
assert_exit_grep 1 "open external bet" "conclusion: open bet blocks (and returns non-zero)" python3 bin/conclusion_gate.py
if python3 bin/bets.py resolve bet-001 expired "sim evidence" >/dev/null 2>&1; then
  ok "bets: resolve with evidence"; else bad "bets: resolve with evidence"; fi
if grep -q "sim evidence" knowledge/outcomes.jsonl 2>/dev/null; then
  ok "bets: resolution fed knowledge/outcomes.jsonl"; else bad "bets: resolution fed outcomes"; fi

echo "=== oracle-classed resolutions (#40) ==="
python3 bin/bets.py add --what "det-unrunnable" --clock other --check "no_such_cmd_zz9" \
  --oracle deterministic --poll-after-h 24 --resolve-by 2099-01-01T00:00:00Z >/dev/null 2>&1
assert_exit_grep 1 "oracle: deterministic" "conclusion: open-bet refusal names its oracle class" \
  python3 bin/conclusion_gate.py
assert_exit_grep 1 "could not EXECUTE" "bets: unrunnable deterministic oracle refuses a prose resolve" \
  python3 bin/bets.py resolve bet-002 lost "prose only"
if python3 bin/bets.py resolve bet-002 lost "prose only" --downgrade-judgment >/dev/null 2>&1 \
   && grep -q "downgraded-to-judgment" run/bets.json; then
  ok "bets: --downgrade-judgment resolves and relabels visibly"
else bad "bets: downgrade path"; fi
python3 bin/bets.py add --what "det-runnable" --clock other --check "exit 3" \
  --oracle deterministic --poll-after-h 24 --resolve-by 2099-01-01T00:00:00Z >/dev/null 2>&1
if python3 bin/bets.py resolve bet-003 lost "the check exited 3 = condition absent" >/dev/null 2>&1 \
   && grep -q '"rc": 3' run/bets.json; then
  ok "bets: executed check output stored with the resolution (rc is evidence, not a refusal)"
else bad "bets: executed-check resolution"; fi

echo "=== iteration pacing: PACE_ENFORCE (#45) ==="
python3 bin/bets.py add --what "quiet clock" --clock indexation --check "true" \
  --poll-after-h 999 --resolve-by 2099-01-01T00:00:00Z >/dev/null 2>&1
python3 bin/bets.py checked bet-004 "sim tick" >/dev/null 2>&1
assert_exit_grep 1 "declared lever" "pace: quiet open bets block a lever-less new iteration" \
  env PACE_ENFORCE=1 python3 bin/iter.py new
if env PACE_ENFORCE=1 python3 bin/iter.py new --lever "sim: a genuinely new probe" >/dev/null 2>&1 \
   && grep -q "Lever:.*genuinely new probe" MONEY_LOG.md; then
  ok "pace: a declared lever opens the iteration and lands in MONEY_LOG"
else bad "pace: lever path"; fi
python3 bin/bets.py add --what "due clock" --clock reply --check "true" \
  --poll-after-h 1 --resolve-by 2099-01-01T00:00:00Z >/dev/null 2>&1
assert_exit 0 "pace: a due bet unblocks lever-less iterations" \
  env PACE_ENFORCE=1 python3 bin/iter.py new
assert_exit 0 "pace: default-off leaves iteration-opening untouched" python3 bin/iter.py new

echo "=== human-actuation queue (#31) ==="
HUMAN_STATE="$W/human-state"
mkdir -p "$HUMAN_STATE" harness
ssh-keygen -q -t ed25519 -N "" -f "$HUMAN_STATE/verifier_signing_key"
cp "$HUMAN_STATE/verifier_signing_key.pub" harness/verifier_key.pub
echo "verifier $(cat "$HUMAN_STATE/verifier_signing_key.pub")" > harness/allowed_signers
git add harness/verifier_key.pub harness/allowed_signers
git commit -qm "harness: trust verifier human-resolution signer"
git push -q origin "$BRANCH"
assert_exit_grep 2 "kind" "human: free-text kind rejected (actuator, never oracle)" \
  python3 bin/human.py request --kind "write-my-pitch" --gate "reach wall" \
  --test "iter 001 packet" --ev "would help a lot"
assert_exit_grep 2 "test" "human: uncited gate-hit rejected (falsify before requesting)" \
  python3 bin/human.py request --kind captcha --gate "mastodon.nu signup step 3" \
  --test "x" --ev "unlocks a federated posting channel"
if python3 bin/human.py request --kind captcha --gate "mastodon.nu signup step 3" \
     --test "iter-043 packet: Turnstile wall hit from the sandbox IP" \
     --ev "unlocks a federated posting channel worth minutes of operator time" >/dev/null 2>&1; then
  ok "human: cited mechanical request registered"; else bad "human: request path"; fi
assert_exit_grep 1 "human actuation hum-001" \
  "human: open request blocks an impossible conclusion (companion bet)" \
  python3 bin/conclusion_gate.py
assert_exit 1 "human: agent checkout cannot self-certify operator fulfillment" \
  python3 bin/human.py fulfill hum-001 --minutes 3 \
    --evidence "operator completed the captcha on their own account"
assert_exit_grep 1 "must differ" "human: branch-name spoof cannot self-certify fulfillment" \
  env AGENT_BRANCH="$BRANCH" LEDGER_BRANCH="$BRANCH" MONEY_AGENT_STATE="$HUMAN_STATE" \
    python3 bin/human.py fulfill hum-001 --minutes 3 \
      --evidence "agent claims operator completed the captcha"
cdx "$W/verifier"
if env AGENT_BRANCH="$BRANCH" LEDGER_BRANCH=ledger MONEY_AGENT_STATE="$HUMAN_STATE" \
     python3 bin/human.py fulfill hum-001 \
     --minutes 3 --evidence "operator completed the captcha on their own account" >/dev/null 2>&1; then
  ok "human: operator resolution published on facts lane"; else bad "human: operator fulfill"; fi
cdx "$W/agent"
if python3 bin/human.py sync hum-001 >/dev/null 2>&1 \
   && grep -q '"human_minutes_total": 3' run/human_tasks.json \
   && grep -q '"resolution_latency_seconds":' run/human_tasks.json; then
  ok "human: signed fulfillment sync meters minutes + latency and resolves companion"
else bad "human: grounded sync"; fi
python3 bin/human.py request --kind approval-click --gate "mastodon.nu staff approval" \
  --test "iter-079 packet: account stuck at human staff approval" \
  --ev "the account exists; one click activates it" >/dev/null 2>&1
cdx "$W/verifier"
assert_grep "1 awaiting operator" "supervise: reads queue from agent branch in verifier checkout" \
  bash bin/supervise.sh "$BRANCH"
assert_grep "VERDICT.*HUMAN ACTUATION" "supervise: pending queue reaches the VERDICT line" \
  bash bin/supervise.sh "$BRANCH"
cdx "$W/agent"
python3 - <<'PYEOF'
import json
p="run/human_tasks.json"; d=json.load(open(p)); d["tasks"][1]["status"]="fulfilled"
d["tasks"][1]["resolution"]={"status":"fulfilled","evidence":"agent typed this"}
json.dump(d, open(p,"w"), indent=2)
PYEOF
assert_exit_grep 1 "not grounded" "human: direct task-status edit cannot authorize conclusion" \
  python3 bin/conclusion_gate.py
git checkout -q -- run/human_tasks.json
cdx "$W/verifier"
if env AGENT_BRANCH="$BRANCH" LEDGER_BRANCH=ledger MONEY_AGENT_STATE="$HUMAN_STATE" \
     python3 bin/human.py decline hum-002 --minutes 0.25 \
     --reason "not worth operator identity exposure this run" >/dev/null 2>&1; then
  ok "human: operator decline published on facts lane"; else bad "human: operator decline"; fi
assert_grep "1 resolved-awaiting-agent-sync" "supervise: distinguishes published resolution" \
  bash bin/supervise.sh "$BRANCH"
assert_grep "VERDICT.*AGENT SYNC" "supervise: published resolution reaches the VERDICT line" \
  bash bin/supervise.sh "$BRANCH"
cdx "$W/agent"
if python3 bin/human.py sync hum-002 >/dev/null 2>&1 \
   && grep -q '"status": "declined"' run/human_tasks.json; then
  ok "human: grounded decline synced (operator REFUSALS mirror)"
else bad "human: decline sync"; fi
assert_grep "human_minutes_total: 3" "human: metering surfaced in list" python3 bin/human.py list

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
       "MAX_DRAWDOWN_USD: 25.0\n"
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
# #38: the martingale catch -- a NEW peak then a drop breaching the frozen risk cap FALSIFIES
# even though pnl (60) still clears the bar (50). A raw level-check would have said VERIFIED.
state.update(equity="100100")
if verdict() != "VERIFIED_POSITIVE_EV": fails.append("new peak should stay VERIFIED (dd=0)")
state.update(equity="100060")
v = verdict()
_e = json.load(open("ledger/edge.json"))
if v != "FALSIFIED" or "drawdown" not in _e.get("falsified_reason", ""):
    fails.append(f"drawdown breach not FALSIFIED-with-reason: {v} / {_e.get('falsified_reason')}")
nofield_f, nofield_e = edge_pnl.parse_registration(reg.replace("MAX_DRAWDOWN_USD: 25.0\n", ""))
if not nofield_e: fails.append("registration without MAX_DRAWDOWN_USD accepted")
for bad in ("MAX_DRAWDOWN_USD: nan", "MAX_DRAWDOWN_USD: inf", "MIN_FILLED_ORDERS: 0"):
    candidate = reg.replace("MAX_DRAWDOWN_USD: 25.0", bad) if bad.startswith("MAX") else reg.replace("MIN_FILLED_ORDERS: 10", bad)
    if not edge_pnl.parse_registration(candidate)[1]: fails.append(f"invalid registration accepted: {bad}")
runtime = json.load(open("state/edge_runtime.json"))
if list((runtime.get("registrations") or {})) != [json.load(open("state/edge_registration.json"))["sha256"]]:
    fails.append("runtime peak is not scoped to the frozen registration")
frozen = json.load(open("state/edge_registration.json"))
frozen["fields"]["RESOLVE_BY"] = "2000-01-01T00:00:00Z"
json.dump(frozen, open("state/edge_registration.json","w"))
os.remove("state/edge_runtime.json")   # reset peak so the deadline leg (not drawdown) decides
state.update(equity="100010")
if verdict() != "FALSIFIED": fails.append("deadline-missed -> FALSIFIED")
if "deadline" not in json.load(open("ledger/edge.json")).get("falsified_reason", ""):
    fails.append("deadline falsification lost its reason")
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

echo "=== pnl verifier correctness: currency + coverage fail closed (issues #33/#34) ==="
# Same import-and-monkeypatch pattern as the edge block above: pnl's _get is stubbed per-case, so
# the full main() path (errors wiring, verified flag, sums) runs with no network and no keys.
mkdir -p pnl_state
echo '{"created_gt": 1, "baseline_ledger_commit": ""}' > pnl_state/baseline.json
echo '{"emails":["op@sim.example"],"card_fingerprints":[]}' > pnl_state/operator_identity.json
PNL_RESULT=$(python3 - 2>/dev/null <<'PYEOF'
import sys, os, json
sys.path.insert(0, "bin")
# crash guard: bash's ${var##*PNL_FAILS:} returns the WHOLE string when the marker never printed,
# so an uncaught exception here would surface as truth.json garbage instead of a named failure.
# The excepthook guarantees the marker line exists on every exit path.
sys.excepthook = lambda t, v, tb: print(f"PNL_FAILS:crash:{t.__name__}:{v}")
os.environ.update({"STRIPE_READ_KEY": "rk_test_sim", "CARD_CAP_USD": "25",
                   "MONEY_AGENT_STATE": "pnl_state", "CARD_SOURCE": "issuer_enforced"})
os.environ.pop("PRIVACY_READ_KEY", None)
import importlib, pnl
importlib.reload(pnl)
pnl.MAX_PAGES = 2   # tiny cap so truncation cases stay fast; the bound's VALUE is not the subject
fails = []

def run(stub):
    pnl._get = stub
    pnl.main()
    return json.load(open("ledger/truth.json"))

def charge(i, cur="usd", amt=1234, email="buyer@x.com"):
    return {"id": f"ch_{i}", "paid": True, "status": "succeeded", "amount": amt, "currency": cur,
            "billing_details": {"email": email},
            "payment_method_details": {"card": {"fingerprint": f"fp{i}"}}}

def bt(i, cur="usd", typ="charge", amt=1234):
    return {"id": f"txn_{i}", "type": typ, "amount": amt, "fee": 30, "currency": cur}

# 1. clean case: all usd, clean page ends -> verified true, no false positives from the new checks
def clean(url, headers, params=None):
    if "balance_transactions" in url: return {"data": [bt(1)], "has_more": False}
    if "/charges" in url: return {"data": [charge(1)], "has_more": False}
    return {}
t = run(clean)
if not (t["verified"] and t["errors"] == [] and t["received_usd"] == 12.34):
    fails.append(f"clean-usd case broke: verified={t['verified']} errors={t['errors']} recv={t['received_usd']}")

# 2. JPY charge on the received_usd feed -> poisoned, amount excluded (the Y500->$5 bite case)
def jpy_charge(url, headers, params=None):
    if "balance_transactions" in url: return {"data": [], "has_more": False}
    if "/charges" in url: return {"data": [charge(1, cur="jpy", amt=500)], "has_more": False}
    return {}
t = run(jpy_charge)
if t["verified"] or not any(e.startswith("non_usd_amount:charge:jpy") for e in t["errors"]) \
   or t["received_usd"] != 0.0:
    fails.append(f"jpy charge not poisoned: verified={t['verified']} errors={t['errors']} recv={t['received_usd']}")

# 3. JPY balance_transaction -> poisoned, excluded from gross
def jpy_bt(url, headers, params=None):
    if "balance_transactions" in url: return {"data": [bt(1, cur="jpy", amt=500)], "has_more": False}
    if "/charges" in url: return {"data": [], "has_more": False}
    return {}
t = run(jpy_bt)
if t["verified"] or not any(e.startswith("non_usd_amount:balance_transaction:jpy") for e in t["errors"]) \
   or t["received_gross_usd"] != 0.0:
    fails.append(f"jpy balance_transaction not poisoned: {t['errors']} gross={t['received_gross_usd']}")

# 4. missing currency on a counted object -> poisoned (fail-closed, unknown is not usd)
def no_cur(url, headers, params=None):
    if "balance_transactions" in url: return {"data": [], "has_more": False}
    if "/charges" in url:
        c = charge(1); del c["currency"]; return {"data": [c], "has_more": False}
    return {}
t = run(no_cur)
if t["verified"] or not any(e.startswith("currency_missing:charge") for e in t["errors"]):
    fails.append(f"missing currency not poisoned: {t['errors']}")

# 5. charges truncation: has_more still true at the page cap -> coverage_incomplete, verified false
def trunc_charges(url, headers, params=None):
    if "balance_transactions" in url: return {"data": [], "has_more": False}
    if "/charges" in url: return {"data": [charge(1)], "has_more": True}
    return {}
t = run(trunc_charges)
if t["verified"] or not any("coverage_incomplete:stripe_charges" in e for e in t["errors"]):
    fails.append(f"charges truncation silent: verified={t['verified']} errors={t['errors']}")

# 6. balance_transactions truncation (the loop that used to be UNBOUNDED)
def trunc_bt(url, headers, params=None):
    if "balance_transactions" in url: return {"data": [bt(1)], "has_more": True}
    if "/charges" in url: return {"data": [], "has_more": False}
    return {}
t = run(trunc_bt)
if t["verified"] or not any("coverage_incomplete:stripe_balance_transactions" in e for e in t["errors"]):
    fails.append(f"balance_transactions truncation silent: {t['errors']}")

# 7. privacy: full pages at the cap -> coverage_incomplete; declared-EUR txn -> poisoned + excluded
os.environ["PRIVACY_READ_KEY"] = "pk_sim"
os.environ.pop("CARD_SOURCE", None)
def privacy_trunc(url, headers, params=None):
    if "balance_transactions" in url: return {"data": [], "has_more": False}
    if "/charges" in url: return {"data": [], "has_more": False}
    if "transactions" in url:
        return {"data": [{"token": f"t{i}", "settled_amount": 100} for i in range(500)]}
    return {}
t = run(privacy_trunc)
if t["verified"] or not any("coverage_incomplete:privacy_transactions" in e for e in t["errors"]):
    fails.append(f"privacy truncation silent: {t['errors']}")
def privacy_eur(url, headers, params=None):
    if "balance_transactions" in url: return {"data": [], "has_more": False}
    if "/charges" in url: return {"data": [], "has_more": False}
    if "transactions" in url:
        return {"data": [{"token": "t1", "settled_amount": 100, "currency": "EUR"},
                         {"token": "t2", "settled_amount": 200}]}
    return {}
t = run(privacy_eur)
if t["verified"] or not any(e.startswith("non_usd_amount:privacy:EUR") for e in t["errors"]) \
   or t["spent_usd"] != 2.0:
    fails.append(f"privacy EUR txn not poisoned/excluded: {t['errors']} spent={t['spent_usd']}")

# 8. #46: untracked raws are QUARANTINED into the state dir, never deleted (they are either a
#    plant preserved as evidence, or the orphan of a failed commit preserved as audit trail).
#    The nested whitespace name pins NUL-delimited Git parsing and path-preserving rescue: a
#    whitespace splitter would treat it as multiple paths, while basename-only rescue can collide.
import pathlib
plant = pathlib.Path("ledger/raw/29990104T000000_plant.json")
plant.parent.mkdir(parents=True, exist_ok=True)
plant.write_text('{"plant": true}')
nested_plant = pathlib.Path("ledger/raw/nested raw/plant file.json")
nested_plant.parent.mkdir(parents=True, exist_ok=True)
nested_plant.write_text('{"plant": "nested whitespace path"}')
def privacy_clean(url, headers, params=None):
    if "balance_transactions" in url: return {"data": [], "has_more": False}
    if "/charges" in url: return {"data": [], "has_more": False}
    if "transactions" in url:
        return {"data": [{"token": "t1", "settled_amount": 100},
                         {"token": "t2", "settled_amount": 200}]}
    return {}
t = run(privacy_clean)
q = pathlib.Path("pnl_state/raw-rescue")
top_rescue = list(q.glob("*/ledger/raw/29990104T000000_plant.json"))
nested_rescue = list(q.glob("*/ledger/raw/nested raw/plant file.json"))
if plant.exists() or nested_plant.exists() or not top_rescue or not nested_rescue:
    fails.append("C3 quarantine broken: "
                 f"top_in_tree={plant.exists()} nested_in_tree={nested_plant.exists()} "
                 f"top_rescued={bool(top_rescue)} nested_rescued={bool(nested_rescue)}")

# 9. #46: a quarantine failure must halt before an untrusted raw pull can reach the manifest.
#    The real failure mode is a state directory on a different filesystem (Path.rename raises
#    EXDEV); patching the one planted file's rename gives the same verifier-visible contract.
plant = pathlib.Path("ledger/raw/29990105T000000_rename_failure.json")
plant.write_text('{"plant": "rename failure"}')
real_rename = pathlib.Path.rename
def reject_plant_rename(self, target):
    if self.resolve() == plant.resolve():
        raise OSError("simulated cross-device quarantine failure")
    return real_rename(self, target)
pathlib.Path.rename = reject_plant_rename
try:
    rc = pnl.main()
finally:
    pathlib.Path.rename = real_rename
if rc == 0 or not plant.exists():
    fails.append(f"C3 quarantine failure did not halt/preserve raw: rc={rc} exists={plant.exists()}")
plant.unlink(missing_ok=True)

# 10. #41: absent feed -> null fields (unknown is not zero), even with spend measured
if t.get("inference_usd") is not None or t.get("net_usd_full") is not None:
    fails.append(f"inference absent-feed not null: {t.get('inference_usd')}/{t.get('net_usd_full')}")

# 11. #41: valid feed + measured spend -> summed inference and full net
pathlib.Path("inf.csv").write_text("date,usd\n2026-07-20,1.25\n2026-07-20,0.50\n")
os.environ["INFERENCE_CSV"] = "inf.csv"
t = run(privacy_clean)
if not t["verified"] or t.get("inference_usd") != 1.75 or t.get("net_usd_full") != -4.75:
    fails.append(f"inference metering wrong: verified={t['verified']} inf={t.get('inference_usd')} "
                 f"full={t.get('net_usd_full')} errors={t['errors']}")

# 12. #41: malformed CSVs fail closed; header-only file remains a documented measured zero.
pathlib.Path("inf_bad.csv").write_text("date,usd\n2026-07-20,notanumber\n")
os.environ["INFERENCE_CSV"] = "inf_bad.csv"
t = run(privacy_clean)
if t["verified"] or not any(e.startswith("inference_feed_failed") for e in t["errors"]):
    fails.append(f"malformed inference feed not failing closed: {t['errors']}")
pathlib.Path("inf_no_usd.csv").write_text("date,cost\n2026-07-20,1.25\n")
os.environ["INFERENCE_CSV"] = "inf_no_usd.csv"
t = run(privacy_clean)
if t["verified"] or not any(e.startswith("inference_feed_failed") for e in t["errors"]):
    fails.append(f"inference schema without usd not failing closed: {t['errors']}")
pathlib.Path("inf_nonfinite.csv").write_text("date,usd\n2026-07-20,NaN\n")
os.environ["INFERENCE_CSV"] = "inf_nonfinite.csv"
t = run(privacy_clean)
if t["verified"] or not any(e.startswith("inference_feed_failed") for e in t["errors"]):
    fails.append(f"non-finite inference feed not failing closed: {t['errors']}")
pathlib.Path("inf_zero.csv").write_text("date,usd\n")
os.environ["INFERENCE_CSV"] = "inf_zero.csv"
t = run(privacy_clean)
if not t["verified"] or t.get("inference_usd") != 0.0:
    fails.append(f"header-only inference feed not a measured zero: {t.get('inference_usd')} {t['errors']}")
os.environ.pop("INFERENCE_CSV", None)

# 12. #30: a stripe-only run publishes NO rails breakdown (the S7 parity guarantee)
t = run(clean)
if "rails" in t:
    fails.append("stripe-only run leaked a rails breakdown (parity broken)")

# 13. #30: the Base/USDC adapter -- exact payer/payee/amount binding, facts-lane operator identity,
# safe-block reads, and a fresh run baseline that cannot recount the previous run.
os.environ.update({"BASE_RPC_URL": "http://rpc.sim",
                   "BASE_SETTLEMENT_ADDRESS": "0x" + "ab" * 20,
                   "BASE_MARKETPLACE_ADDRESS": "0x" + "cd" * 20,
                   "BASE_SETTLEMENT_EVENT_TOPIC0": "0x" + "ee" * 32,
                   "BASE_SETTLEMENT_PAYER_TOPIC": "1",
                   "BASE_SETTLEMENT_PAYEE_TOPIC": "2",
                   "BASE_SETTLEMENT_AMOUNT_WORD": "0",
                   "BASE_FINALITY_TAG": "safe"})
import rails.base_usdc as bu
importlib.reload(bu)
OP_ADDR = "0x" + "77" * 20
calls = []
safe_head = [1000]
chain_id = [8453]
def rpc_stub(url, method, params):
    calls.append((method, params))
    if method == "eth_chainId":
        return hex(chain_id[0])
    if method == "eth_getBlockByNumber":
        return {"number": hex(safe_head[0]), "hash": "0x" + f"{safe_head[0]:064x}"}
    if method == "eth_getLogs":
        if int(params[0]["fromBlock"], 16) >= 2001:
            return []
        def lg(sender, amt, tx):
            return {"data": hex(amt), "transactionHash": tx,
                    "topics": [bu.TRANSFER_TOPIC0, bu._addr_topic(sender), params[0]["topics"][2]]}
        return [lg("0x" + "11" * 20, 12_340_000, "0xbound"),
                lg("0x" + "22" * 20, 5_000_000, "0xunbound"),
                lg("0x" + "cd" * 20, 9_000_000, "0xself")]
    if method == "eth_getTransactionReceipt":
        payer = OP_ADDR if params[0] == "0xself" else "0x" + "11" * 20
        amount = 9_000_000 if params[0] == "0xself" else 12_340_000
        if params[0] in ("0xbound", "0xself"):
            return {"logs": [{"address": "0x" + "cd" * 20,
                              "topics": ["0x" + "ee" * 32, bu._addr_topic(payer),
                                         bu._addr_topic("0x" + "ab" * 20)],
                              "data": "0x" + f"{amount:064x}"}]}
        return {"logs": []}
    raise RuntimeError("unexpected rpc " + method)
bu._rpc = rpc_stub
opid = json.load(open("pnl_state/operator_identity.json"))
opid["addresses"] = [OP_ADDR]
json.dump(opid, open("pnl_state/operator_identity.json", "w"))
bu.freeze_baseline(pathlib.Path("pnl_state"))
safe_head[0] = 1010
t = run(clean)
b = t.get("rails", {}).get("base_usdc", {})
if not t["verified"] or t["received_usd"] != 24.68 \
   or b != {"customer_usd": 12.34, "self_usd": 9.0, "unbound_usd": 5.0}:
    fails.append(f"base adapter classification wrong: recv={t['received_usd']} rails={t.get('rails')} "
                 f"errors={t['errors']}")
# A new run freezes a new boundary. Old run-1 receipts must disappear from run-2 received_usd.
safe_head[0] = 2000
bu.freeze_baseline(pathlib.Path("pnl_state"))
safe_head[0] = 2010
calls.clear()
t2 = run(clean)
if t2["received_usd"] != 12.34 or t2.get("rails", {}).get("base_usdc", {}).get("customer_usd") != 0:
    fails.append(f"run-2 recounted run-1 Base revenue: {t2.get('rails')} recv={t2['received_usd']}")
if not any(m == "eth_getLogs" and p[0]["fromBlock"] == hex(2001)
           and p[0]["toBlock"] == hex(2010) for m, p in calls):
    fails.append("run-scoped baseline/finalized toBlock not used")
# One settlement event is evidence for one transfer, not a reusable coupon for every identical
# Transfer in the receipt. The second transfer must remain unbound.
def duplicate_rpc(url, method, params):
    if method == "eth_chainId": return hex(8453)
    if method == "eth_getBlockByNumber":
        return {"number": hex(2010), "hash": "0x" + "44" * 32}
    if method == "eth_getLogs":
        base = {"data": hex(1_000_000), "transactionHash": "0xduplicate",
                "topics": [bu.TRANSFER_TOPIC0, bu._addr_topic("0x" + "22" * 20),
                           bu._addr_topic("0x" + "ab" * 20)]}
        return [{**base, "logIndex": "0x1"}, {**base, "logIndex": "0x2"}]
    if method == "eth_getTransactionReceipt":
        return {"logs": [{"address": "0x" + "cd" * 20, "logIndex": "0x3",
                          "topics": ["0x" + "ee" * 32, bu._addr_topic("0x" + "11" * 20),
                                     bu._addr_topic("0x" + "ab" * 20)],
                          "data": "0x" + f"{1_000_000:064x}"}]}
    raise RuntimeError(method)
bu._rpc = duplicate_rpc
dup = bu.pull(pathlib.Path("pnl_state"), {OP_ADDR})
if dup["customer_usd"] != 1.0 or dup["unbound_usd"] != 1.0:
    fails.append(f"one settlement event reused across transfers: {dup}")
bu._rpc = rpc_stub
chain_id[0] = 1
t = run(clean)
if t["verified"] or not any("wrong_chain" in e for e in t["errors"]):
    fails.append(f"non-Base RPC did not fail closed: {t['errors']}")
chain_id[0] = 8453
os.environ.pop("BASE_SETTLEMENT_EVENT_TOPIC0")
t = run(clean)
if t["verified"] or not any("base_usdc_misprovisioned" in e for e in t["errors"]):
    fails.append(f"missing binding config not fail-closed: {t['errors']}")
os.environ["BASE_SETTLEMENT_EVENT_TOPIC0"] = "0x" + "ee" * 32
opid["addresses"] = []
json.dump(opid, open("pnl_state/operator_identity.json", "w"))
t = run(clean)
if t["verified"] or not any("wallet allowlist is empty" in e for e in t["errors"]):
    fails.append(f"empty Base operator allowlist did not fail closed: {t['errors']}")
opid["addresses"] = [OP_ADDR]
json.dump(opid, open("pnl_state/operator_identity.json", "w"))
bu._rpc = lambda *a, **k: (_ for _ in ()).throw(RuntimeError("chain down"))
t = run(clean)
if t["verified"] or not any("base_usdc_pull_failed" in e for e in t["errors"]):
    fails.append(f"dead chain not fail-closed: {t['errors']}")
os.environ.pop("BASE_RPC_URL")

print("PNL_FAILS:" + ";".join(fails))
PYEOF
)
PNL_FAILS="${PNL_RESULT##*PNL_FAILS:}"
if [[ -z "$PNL_FAILS" ]]; then
  ok "pnl: clean case passes; currency/coverage/quarantine/inference/rails cases all behave (13 cases)"
else
  bad "pnl verifier cases: $PNL_FAILS"
fi
rm -rf pnl_state inf.csv inf_bad.csv inf_no_usd.csv inf_nonfinite.csv inf_zero.csv
git checkout -q -- ledger/ 2>/dev/null || true
git clean -qfd ledger/raw/ 2>/dev/null || true

BASELINE_RESULT=$(python3 - 2>/dev/null <<'PYEOF'
import json, os, pathlib, runpy, sys
sys.path.insert(0, "bin")
state = pathlib.Path("base-run-state"); state.mkdir(exist_ok=True)
(state / "base_usdc_baseline.json").write_text('{"baseline_block": 111}\n')
os.environ.update({"MONEY_AGENT_STATE": str(state), "BASE_RPC_URL": "http://rpc.sim",
                   "LEDGER_BRANCH": "ledger"})
import rails.base_usdc as bu
def freeze(target):
    payload = {"baseline_block": 222, "baseline_hash": "0xsafe", "finality_tag": "safe"}
    (target / "base_usdc_baseline.json").write_text(json.dumps(payload))
    return payload
bu.freeze_baseline = freeze
runpy.run_path("bin/set_baseline.py", run_name="set_baseline_sim")
archived = list(state.glob("base_usdc_baseline.*.archived.json"))
current = json.load(open(state / "base_usdc_baseline.json"))
print("OK" if archived and current["baseline_block"] == 222 else
      f"FAIL archived={archived} current={current}")
PYEOF
)
if [[ "$BASELINE_RESULT" == *"OK" ]]; then
  ok "baseline: new run archives and replaces the prior Base boundary"
else
  bad "baseline: Base boundary lifecycle ($BASELINE_RESULT)"
fi
rm -rf base-run-state
git checkout -q -- ledger/baseline.json 2>/dev/null || true

echo "=== start_verifier preflight: wash-trade allowlist (issue #37, marker-extracted) ==="
PRE="$W/preflight.sh"
sed -n '/TEST-MARKER: preflight-opid-begin/,/TEST-MARKER: preflight-opid-end/p' bin/start_verifier.sh > "$PRE"
PRE_OK=1
if ! grep -q "TEST-MARKER: preflight-opid-begin" bin/start_verifier.sh \
   || ! grep -q "TEST-MARKER: preflight-opid-end" bin/start_verifier.sh; then
  bad "preflight: a TEST-MARKER is missing from start_verifier.sh"; PRE_OK=0
fi
if ! grep -q "operator_identity" "$PRE"; then
  bad "preflight: TEST-MARKER extraction came back empty"; PRE_OK=0
fi
if grep -qE "set_baseline|facts lane" "$PRE"; then
  bad "preflight: extraction overran the block (end marker drifted) -- not executing it"; PRE_OK=0
fi
if [[ "$PRE_OK" == "1" ]]; then
  assert_exit 2 "preflight: missing operator_identity.json refuses the start" \
    env MONEY_AGENT_STATE="$W/no-such-state" bash -c "set -uo pipefail; source '$PRE'"
  mkdir -p "$W/opid-state"
  echo '{"emails":["op@sim.example"],"card_fingerprints":[]}' > "$W/opid-state/operator_identity.json"
  assert_exit 0 "preflight: provisioned allowlist passes" \
    env MONEY_AGENT_STATE="$W/opid-state" bash -c "set -uo pipefail; source '$PRE'"
fi

BASE_PRE="$W/preflight-base.sh"
sed -n '/TEST-MARKER: preflight-base-begin/,/TEST-MARKER: preflight-base-end/p' \
  bin/start_verifier.sh > "$BASE_PRE"
BASE_ENV=(BASE_RPC_URL=http://rpc.sim BASE_SETTLEMENT_ADDRESS=0xabc \
  BASE_MARKETPLACE_ADDRESS=0xdef BASE_SETTLEMENT_EVENT_TOPIC0=0x123 \
  BASE_SETTLEMENT_PAYER_TOPIC=1 BASE_SETTLEMENT_PAYEE_TOPIC=2 \
  BASE_SETTLEMENT_AMOUNT_WORD=0)
assert_exit 2 "preflight: armed Base rail requires operator wallet addresses" \
  env "${BASE_ENV[@]}" MONEY_AGENT_STATE="$W/opid-state" OPID="$W/opid-state/operator_identity.json" \
    bash -c "set -uo pipefail; source '$BASE_PRE'"
echo '{"emails":["op@sim.example"],"addresses":["0x777"]}' > \
  "$W/opid-state/operator_identity.json"
assert_exit 0 "preflight: fully provisioned Base binding + wallet allowlist passes" \
  env "${BASE_ENV[@]}" MONEY_AGENT_STATE="$W/opid-state" OPID="$W/opid-state/operator_identity.json" \
    bash -c "set -uo pipefail; source '$BASE_PRE'"
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
  # shellcheck disable=SC2016  # literal '$999' is intentional test data
  replace_once .github/aiv-packets/VERIFICATION_PACKET_ITER_901.md \
    "Nothing this iteration; honest zero." "Earned \$999 this iteration." || exit 1
  assert_exit 1 "gate: \$999 overclaim fails" bash bin/aiv_gate.sh 901
  # shellcheck disable=SC2016  # literal '$999' is intentional test data
  replace_once .github/aiv-packets/VERIFICATION_PACKET_ITER_901.md \
    "Earned \$999 this iteration." "Nothing this iteration; honest zero." || exit 1
  # The bare-word forms ("999 dollars", "USD 999") were how a false claim could slip past a
  # $-only parser; the gate matches them too -- pin that path (queued from IMPROVEMENT_LOG entry
  # 021). The amount must exceed EVERY verifier bound: the rig's edge rail carries paper_pnl 62.5,
  # and the gate's documented residual accepts real-money claims up to the paper P&L -- a first
  # draft of this test used "47 dollars" and passed the gate for exactly that reason.
  replace_once .github/aiv-packets/VERIFICATION_PACKET_ITER_901.md \
    "Nothing this iteration; honest zero." "Earned 999 dollars this iteration." || exit 1
  assert_exit 1 "gate: bare-word '999 dollars' overclaim fails" bash bin/aiv_gate.sh 901
  replace_once .github/aiv-packets/VERIFICATION_PACKET_ITER_901.md \
    "Earned 999 dollars this iteration." "Nothing this iteration; honest zero." || exit 1
  replace_once .github/aiv-packets/VERIFICATION_PACKET_ITER_901.md \
    "EDGE_CLAIM: VERIFIED_POSITIVE_EV" "EDGE_CLAIM: FALSIFIED" || exit 1
  assert_exit 1 "gate: contradicting EDGE_CLAIM fails" bash bin/aiv_gate.sh 901
  grep -v "^EDGE_CLAIM:" .github/aiv-packets/VERIFICATION_PACKET_ITER_901.md > p.tmp && mv p.tmp .github/aiv-packets/VERIFICATION_PACKET_ITER_901.md
  assert_exit 1 "gate: missing EDGE_CLAIM while rail live fails" bash bin/aiv_gate.sh 901
  # #39/#35 stage 2c: a payment-surface claim requires a fresh delivery_check the gate runs itself
  printf 'EDGE_CLAIM: VERIFIED_POSITIVE_EV\n' >> .github/aiv-packets/VERIFICATION_PACKET_ITER_901.md
  printf 'Offer live: https://buy.stripe.com/test_simoffer123\n' >> .github/aiv-packets/VERIFICATION_PACKET_ITER_901.md
  assert_exit 1 "gate: payment URL without DELIVERY_CHECK_URL fails (paid-offer mandate)" \
    bash bin/aiv_gate.sh 901
  printf 'DELIVERY_CHECK_URL: https://sim-delivery.invalid/unlock\n' >> .github/aiv-packets/VERIFICATION_PACKET_ITER_901.md
  assert_exit 1 "gate: failing delivery_check fails the packet (fresh re-run, never self-typed)" \
    bash bin/aiv_gate.sh 901
else
  skip "gate tests (aiv CLI not on PATH -- pip install aiv-protocol, or accept stage-0 fail-closed)"
fi

echo "=== delivery_check unit (#39/#35, monkeypatched fetch -- SSRF guard blocks a live-serve rig) ==="
DC_RESULT=$(python3 - 2>/dev/null <<'PYEOF'
import sys
sys.path.insert(0, "bin")
sys.excepthook = lambda t, v, tb: print(f"DC_FAILS:crash:{t.__name__}:{v}")
import importlib, delivery_check as dc
importlib.reload(dc)
fails = []
def case(label, want_rc, fetch, limit, argv, redirect="https://example.com/unlock"):
    dc._fetch = fetch
    dc._payment_link = lambda u: {"url": u, "restrictions": {"completed_sessions": {"limit": limit}},
                                  "after_completion": {"type": "redirect", "redirect": {"url": redirect}}}
    sys.argv = ["delivery_check.py"] + argv
    rc = dc.main()
    if rc != want_rc:
        fails.append(f"{label}: rc={rc} want {want_rc}")
GOOD = lambda u: (200, b"X" * 400)
case("complete artifact + capped link passes", 0, GOOD, "1",
     ["https://example.com/unlock", "--payment-link", "https://buy.stripe.com/x"])
case("placeholder body fails", 1, lambda u: (200, b"deliverable <fill> pending" + b"x" * 400), "1",
     ["https://example.com/unlock", "--payment-link", "https://buy.stripe.com/x"])
case("stub-sized body fails", 1, lambda u: (200, b"ok"), "1",
     ["https://example.com/unlock", "--payment-link", "https://buy.stripe.com/x"])
case("uncapped link fails (#35)", 1, GOOD, "none",
     ["https://example.com/unlock", "--payment-link", "https://buy.stripe.com/x"])
case("unverifiable limit fails closed (#35)", 1, GOOD, "unverified",
     ["https://example.com/unlock", "--payment-link", "https://buy.stripe.com/x"])
case("unrelated success redirect fails (#39)", 1, GOOD, "1",
     ["https://example.com/unlock", "--payment-link", "https://buy.stripe.com/x"],
     redirect="https://example.com/not-the-delivery")
case("no payment link -> delivery-only check passes", 0, GOOD, "n/a",
     ["https://example.com/unlock"])
import hashlib
h = hashlib.sha256(b"X" * 400).hexdigest()
case("sha256 match passes", 0, GOOD, "n/a", ["https://example.com/unlock", "--expect-sha256", h])
case("sha256 mismatch fails", 1, GOOD, "n/a",
     ["https://example.com/unlock", "--expect-sha256", "0" * 64])
print("DC_FAILS:" + ";".join(fails))
PYEOF
)
DC_FAILS="${DC_RESULT##*DC_FAILS:}"
if [[ -z "$DC_FAILS" ]]; then
  ok "delivery_check: pass/placeholder/size/uncapped/unverified/sha cases all correct"
else
  bad "delivery_check unit: $DC_FAILS"
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
  # MONEY_AGENT_STATE MUST be pinned to the rig (#46): the block's side-car writes
  # ${MONEY_AGENT_STATE:-$HOME/...}; without this export the sim would write the operator's REAL
  # ~/.money-agent-verifier -- the exact class of rig-escapes this file exists to prevent.
  R="$PWD" LOG=/dev/null LEDGER_BRANCH=ledger bash -c '
    set -uo pipefail; cd "'"$PWD"'"; R="'"$PWD"'"; LOG=/dev/null; LEDGER_BRANCH=ledger
    export MONEY_AGENT_STATE="'"$W"'/vstate"
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
  if [[ -f ledger/raw/29990101T000000_probe.json ]]; then ok "convergence: stranded pull preserved under failing push"
  else bad "convergence: stranded pull LOST under failing push"; fi
  git remote set-url origin "$W/origin.git"
  run_convergence || bad "convergence: block exited non-zero on recovery cycle"
  if git ls-tree origin/ledger -r --name-only | grep -q 29990101; then
    ok "convergence: stranded pull recovered to origin"; else bad "convergence: recovery"; fi

  # --- #46: FORCED DIVERGENCE (origin rotated from another checkout while a pull sat local-only).
  # The side-car in the agent-unreachable state dir must hold the pull BEFORE the reset (belt);
  # the block's re-commit + next-cycle push must land it on origin (suspenders).
  git fetch -q origin ledger && git reset -q --hard origin/ledger
  echo '{"probe2": true}' > ledger/raw/29990102T000000_probe2.json
  git add ledger/raw/29990102T000000_probe2.json \
    && git -c user.name=verifier -c user.email=v@sim commit -qm "verifier: stranded2"
  TREE=$(git --git-dir="$W/origin.git" rev-parse "ledger^{tree}")
  # explicit identity, like verifier_loop's real rotation: a bare repo has no local git config, so
  # commit-tree would author as the HOST's global user -- and guard's ancestry-scoped SoD scan
  # (correctly) halts on any non-verifier author reachable from the facts lane. The matrix caught
  # exactly this when the fixture omitted it.
  DIVERGED=$(GIT_AUTHOR_NAME=verifier GIT_AUTHOR_EMAIL=v@sim \
             GIT_COMMITTER_NAME=verifier GIT_COMMITTER_EMAIL=v@sim \
             git --git-dir="$W/origin.git" commit-tree "$TREE" -p "ledger^" -m "rotated elsewhere")
  git --git-dir="$W/origin.git" update-ref refs/heads/ledger "$DIVERGED"
  run_convergence || true    # divergence cycle: reset + rescue re-commit (local, ahead)
  if compgen -G "$W/vstate/raw-rescue/*-diverged/29990102T000000_probe2.json" >/dev/null; then
    ok "divergence: side-car holds the pull (agent-unreachable state dir)"
  else bad "divergence: side-car missing the pull"; fi
  run_convergence || bad "divergence: push cycle exited non-zero"   # ahead -> push path
  git fetch -q origin ledger
  if git ls-tree origin/ledger -r --name-only | grep -q 29990102; then
    ok "divergence: pull re-committed and pushed to origin"; else bad "divergence: re-commit/push"; fi

  echo "=== supervise: unpushed facts counter (issue #46) ==="
  git reset -q --hard origin/ledger
  echo '{"x": 1}' > ledger/raw/29990103T000000_local.json
  git add ledger/raw/29990103T000000_local.json \
    && git -c user.name=verifier -c user.email=v@sim commit -qm "verifier: local-only"
  assert_grep "1 unpushed local commit" "supervise: surfaces unpushed facts commits" bash bin/supervise.sh
  git reset -q --hard origin/ledger
fi

echo "=== fact-lane signing: sign/verify/tamper/chain (#36) + attestation (#42) ==="
# The rig generates a THROWAWAY keypair -- the real repo never carries harness/verifier_key.pub;
# provisioning adds it per run (ledger/README.md). So enforcement stays un-armed everywhere else.
if command -v ssh-keygen >/dev/null 2>&1; then
  cdx "$W/verifier"
  git checkout -q ledger 2>/dev/null || git checkout -q -B ledger origin/ledger
  git fetch -q origin ledger && git reset -q --hard origin/ledger
  ssh-keygen -t ed25519 -N "" -q -f "$W/vkey" -C verifier
  mkdir -p harness
  cp "$W/vkey.pub" harness/verifier_key.pub
  echo "verifier $(cat "$W/vkey.pub")" > harness/allowed_signers
  sign_and_push() { # sign_and_push <previous_hash> [received] -- publish a signed truth.json
    python3 - "$1" "${2:-}" <<'PY'
import json, sys
t = json.load(open("ledger/truth.json"))
t["previous_hash"] = sys.argv[1]
if sys.argv[2]:
    t["received_usd"] = float(sys.argv[2])
open("ledger/truth.json", "w").write(json.dumps(t, indent=2) + "\n")
PY
    rm -f ledger/truth.json.sig
    ssh-keygen -Y sign -f "$W/vkey" -n money-agent-ledger ledger/truth.json 2>/dev/null
    git add harness ledger/truth.json ledger/truth.json.sig
    git -c user.name=verifier -c user.email=v@sim commit -qm "verifier: signed publish" \
      && git push -qf origin ledger
  }
  sha_of_head_truth() { git show HEAD:ledger/truth.json | python3 -c \
    "import sys,hashlib;print(hashlib.sha256(sys.stdin.buffer.read()).hexdigest())"; }
  GOOD_PREV=$(sha_of_head_truth)
  sign_and_push "$GOOD_PREV"
  GOOD_TIP=$(git rev-parse HEAD)
  cdx "$W/agent"
  assert_exit 0 "signing: valid signed ledger accepted as grounded" python3 bin/truth.py received_usd
  # tamper: content changed, stale signature kept
  cdx "$W/verifier"
  python3 -c "
import json; t=json.load(open('ledger/truth.json')); t['received_usd']=7.77
open('ledger/truth.json','w').write(json.dumps(t, indent=2) + '\n')"
  git add ledger/truth.json && git -c user.name=verifier -c user.email=v@sim commit -qm "tampered" \
    && git push -qf origin ledger
  cdx "$W/agent"
  assert_exit_grep 2 "SIGNATURE VERIFICATION FAILED" "signing: tampered content refused" \
    python3 bin/truth.py received_usd
  assert_exit_grep 1 "cannot load the ledger" "signing: guard halts on the refused ledger" \
    python3 bin/guard.py
  # unsigned while the key is armed
  cdx "$W/verifier"
  git reset -q --hard "$GOOD_TIP" && git push -qf origin ledger
  PREV2=$(sha_of_head_truth)
  python3 -c "
import json; t=json.load(open('ledger/truth.json')); t['previous_hash']='$PREV2'
open('ledger/truth.json','w').write(json.dumps(t, indent=2) + '\n')"
  git rm -q --cached ledger/truth.json.sig 2>/dev/null; rm -f ledger/truth.json.sig
  git add ledger/truth.json && git -c user.name=verifier -c user.email=v@sim commit -qm "unsigned" \
    && git push -qf origin ledger
  cdx "$W/agent"
  assert_exit_grep 2 "UNSIGNED" "signing: unsigned file refused while key is committed" \
    python3 bin/truth.py received_usd
  # chain break: valid signature over a file whose previous_hash lies
  cdx "$W/verifier"
  git reset -q --hard "$GOOD_TIP" && git push -qf origin ledger
  sign_and_push "$(printf '0%.0s' {1..64})"
  cdx "$W/agent"
  assert_exit_grep 2 "HASH CHAIN BROKEN" "signing: forged previous_hash refused" \
    python3 bin/truth.py received_usd
  cdx "$W/verifier"
  git reset -q --hard "$GOOD_TIP" && git push -qf origin ledger
  # pnl end-to-end: with the signing key provisioned, main() signs truth, chains it, and emits a
  # verifiable attestation (AGENT_BRANCH set -> refusals provenance from the committed branch)
  mkdir -p sig_state && cp "$W/vkey" sig_state/verifier_signing_key
  echo '{"created_gt": 1, "baseline_ledger_commit": ""}' > sig_state/baseline.json
  echo '{"emails":["op@sim.example"],"card_fingerprints":[]}' > sig_state/operator_identity.json
  SIGN_RESULT=$(python3 - 2>/dev/null <<PYEOF
import sys, os, json, hashlib, subprocess
sys.path.insert(0, "bin")
sys.excepthook = lambda t, v, tb: print(f"SIGN_FAILS:crash:{t.__name__}:{v}")
os.environ.update({"STRIPE_READ_KEY": "rk", "CARD_CAP_USD": "25", "CARD_SOURCE": "issuer_enforced",
                   "MONEY_AGENT_STATE": "sig_state", "AGENT_BRANCH": "$BRANCH"})
os.environ.pop("PRIVACY_READ_KEY", None)
import importlib, pnl
importlib.reload(pnl)
pnl._get = lambda url, h, params=None: {"data": [], "has_more": False} if "transactions" in url or "charges" in url else {}
expected_prev = hashlib.sha256(subprocess.run(
    ["git", "show", "HEAD:ledger/truth.json"], capture_output=True).stdout).hexdigest()
pnl.main()
fails = []
t = json.load(open("ledger/truth.json"))
if t.get("previous_hash") != expected_prev:
    fails.append(f"previous_hash wrong: {t.get('previous_hash')} != {expected_prev[:12]}")
for f in ("ledger/truth.json.sig", "ledger/attestation.json", "ledger/attestation.json.sig"):
    if not os.path.exists(f): fails.append(f"missing {f}")
for target in ("ledger/truth.json", "ledger/attestation.json"):
    r = subprocess.run(["ssh-keygen", "-Y", "verify", "-f", "harness/allowed_signers",
                        "-I", "verifier", "-n", "money-agent-ledger", "-s", target + ".sig"],
                       input=open(target, "rb").read(), capture_output=True)
    if r.returncode != 0: fails.append(f"verify failed for {target}")
att = json.load(open("ledger/attestation.json"))
if att.get("received_usd") != t.get("received_usd"): fails.append("attestation/truth mismatch")
if not att.get("refusals_lines"): fails.append("attestation missing refusals provenance")
# A failed second signature must not leave an unsigned customer artifact behind. This patches only
# the attestation signing command; the truth re-sign remains real and must verify while marked
# unverified by its recorded attestation failure.
real_run = pnl.subprocess.run
def reject_attestation_sign(args, **kwargs):
    if (args[:3] == ["ssh-keygen", "-Y", "sign"]
            and str(args[-1]).endswith("attestation.json")):
        return subprocess.CompletedProcess(args, 1, stdout="", stderr="simulated attestation failure")
    return real_run(args, **kwargs)
pnl.subprocess.run = reject_attestation_sign
failed_rc = pnl.main()
pnl.subprocess.run = real_run
failed_truth = json.load(open("ledger/truth.json"))
if failed_rc == 0 or failed_truth.get("verified") or not any(
        e.startswith("attestation_signing_failed") for e in failed_truth.get("errors", [])):
    fails.append(f"attestation signing failure did not fail closed: rc={failed_rc} truth={failed_truth}")
if os.path.exists("ledger/attestation.json") or os.path.exists("ledger/attestation.json.sig"):
    fails.append("attestation signing failure left an unsigned artifact")
r = subprocess.run(["ssh-keygen", "-Y", "verify", "-f", "harness/allowed_signers",
                    "-I", "verifier", "-n", "money-agent-ledger", "-s", "ledger/truth.json.sig"],
                   input=open("ledger/truth.json", "rb").read(), capture_output=True)
if r.returncode != 0:
    fails.append("truth signature was not refreshed after attestation signing failure")
# Initial truth signing failure takes a different path: no signed truth or attestation may survive,
# and the persisted fact must record verified=false rather than retaining the pre-sign verdict.
def reject_truth_sign(args, **kwargs):
    if (args[:3] == ["ssh-keygen", "-Y", "sign"]
            and str(args[-1]).endswith("truth.json")):
        return subprocess.CompletedProcess(args, 1, stdout="", stderr="simulated truth failure")
    return real_run(args, **kwargs)
pnl.subprocess.run = reject_truth_sign
initial_rc = pnl.main()
pnl.subprocess.run = real_run
initial_truth = json.load(open("ledger/truth.json"))
if initial_rc == 0 or initial_truth.get("verified") or not any(
        e.startswith("signing_failed") for e in initial_truth.get("errors", [])):
    fails.append(f"truth signing failure did not persist unverified verdict: rc={initial_rc} truth={initial_truth}")
if os.path.exists("ledger/truth.json.sig") or os.path.exists("ledger/attestation.json"):
    fails.append("truth signing failure left signed-looking public artifacts")
print("SIGN_FAILS:" + ";".join(fails))
PYEOF
)
  SIGN_FAILS="${SIGN_RESULT##*SIGN_FAILS:}"
  if [[ -z "$SIGN_FAILS" ]]; then
    ok "pnl signing: sig + chain + verifiable attestation with refusals provenance"
  else
    bad "pnl signing: $SIGN_FAILS"
  fi
  # edge.json signs too (the S4 deferral, closed in the edge-quality stack): a stubbed edge_pnl
  # cycle with the key provisioned must emit a verifiable ledger/edge.json.sig
  git checkout -q -- ledger/ 2>/dev/null || true
  git clean -qfd ledger/ 2>/dev/null || true
  EDGESIGN_RESULT=$(SIM_VKEY="$W/vkey" python3 - 2>/dev/null <<'PYEOF'
import sys, os, json, subprocess
sys.path.insert(0, "bin")
sys.excepthook = lambda t, v, tb: print(f"ES_FAILS:crash:{t.__name__}:{v}")
os.environ.update({"MONEY_AGENT_STATE": "sig_state2", "AGENT_BRANCH": "sim-agent",
                   "ALPACA_PAPER_KEY_ID": "k", "ALPACA_PAPER_SECRET_KEY": "s"})
os.makedirs("sig_state2", exist_ok=True)
import shutil
shutil.copy(os.environ["SIM_VKEY"], "sig_state2/verifier_signing_key")
os.chmod("sig_state2/verifier_signing_key", 0o600)
import importlib, edge_pnl
importlib.reload(edge_pnl)
reg = ("EDGE_ID: sim2\nMETRIC: paper_pnl_usd\nBAR: 50.0\nMIN_FILLED_ORDERS: 10\n"
       "MAX_DRAWDOWN_USD: 25.0\nRESOLVE_BY: 2099-01-01T00:00:00Z\nHYPOTHESIS: h\nFALSIFIED_IF: f\n")
edge_pnl.committed_registration = lambda: (reg, None)
edge_pnl._get = lambda url, h: {"equity": "100000"} if "/account" in url else []
edge_pnl.main()
fails = []
if not os.path.exists("ledger/edge.json.sig"):
    fails.append("edge.json.sig missing")
else:
    r = subprocess.run(["ssh-keygen", "-Y", "verify", "-f", "harness/allowed_signers",
                        "-I", "verifier", "-n", "money-agent-ledger", "-s", "ledger/edge.json.sig"],
                       input=open("ledger/edge.json", "rb").read(), capture_output=True)
    if r.returncode != 0: fails.append("edge signature does not verify")
print("ES_FAILS:" + ";".join(fails))
PYEOF
)
  ES_FAILS="${EDGESIGN_RESULT##*ES_FAILS:}"
  if [[ -z "$ES_FAILS" ]]; then
    ok "edge signing: stubbed edge_pnl cycle emits a verifiable edge.json.sig"
  else
    bad "edge signing: $ES_FAILS"
  fi
  rm -rf sig_state sig_state2
  git checkout -q -- ledger/ 2>/dev/null || true
  git clean -qfd ledger/ 2>/dev/null || true
  # an UNSIGNED edge.json on the armed lane is refused, and guard treats it as a HALT (an
  # invisible VOID would otherwise hide bar-moving behind "rail idle")
  python3 -c "
import json; e={'computed_at':'2099-01-01T00:00:00+00:00','verdict':'VOID','verified':True,
'registration_intact':False}
open('ledger/edge.json','w').write(json.dumps(e, indent=2) + '\n')"
  rm -f ledger/edge.json.sig
  git add ledger/edge.json
  git rm -q --cached ledger/edge.json.sig 2>/dev/null || true
  git -c user.name=verifier -c user.email=v@sim commit -qm "unsigned edge" && git push -qf origin ledger
  cdx "$W/agent"
  assert_exit_grep 2 "UNSIGNED" "edge signing: unsigned edge.json refused on the armed lane" \
    python3 bin/truth.py --file edge.json verdict
  assert_exit_grep 1 "edge facts refused" "edge signing: guard halts rather than treating it as idle" \
    python3 bin/guard.py
  cdx "$W/verifier"
  git reset -q --hard "$GOOD_TIP" && git push -qf origin ledger
else
  skip "fact-lane signing tests (ssh-keygen not on PATH -- install openssh-client)"
fi

echo
echo "=============================================="
echo "  PASS=$PASS  FAIL=$FAIL  SKIP=$SKIP"
echo "=============================================="
[[ $FAIL -eq 0 ]] || exit 1

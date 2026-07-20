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

# 8. #46: an untracked raw pull is QUARANTINED into the state dir, never deleted (it is either a
#    plant preserved as evidence, or the orphan of a failed commit preserved as audit trail)
import pathlib
plant = pathlib.Path("ledger/raw/29990104T000000_plant.json")
plant.parent.mkdir(parents=True, exist_ok=True)
plant.write_text('{"plant": true}')
def privacy_clean(url, headers, params=None):
    if "balance_transactions" in url: return {"data": [], "has_more": False}
    if "/charges" in url: return {"data": [], "has_more": False}
    if "transactions" in url:
        return {"data": [{"token": "t1", "settled_amount": 100},
                         {"token": "t2", "settled_amount": 200}]}
    return {}
t = run(privacy_clean)
q = list(pathlib.Path("pnl_state/raw-rescue").glob("*/29990104T000000_plant.json"))
if plant.exists() or not q:
    fails.append(f"C3 quarantine broken: still_in_tree={plant.exists()} quarantined={bool(q)}")

# 9. #41: absent feed -> null fields (unknown is not zero), even with spend measured
if t.get("inference_usd") is not None or t.get("net_usd_full") is not None:
    fails.append(f"inference absent-feed not null: {t.get('inference_usd')}/{t.get('net_usd_full')}")

# 10. #41: valid feed + measured spend -> summed inference and full net
pathlib.Path("inf.csv").write_text("date,usd\n2026-07-20,1.25\n2026-07-20,0.50\n")
os.environ["INFERENCE_CSV"] = "inf.csv"
t = run(privacy_clean)
if not t["verified"] or t.get("inference_usd") != 1.75 or t.get("net_usd_full") != -4.75:
    fails.append(f"inference metering wrong: verified={t['verified']} inf={t.get('inference_usd')} "
                 f"full={t.get('net_usd_full')} errors={t['errors']}")

# 11. #41: malformed feed fails closed; header-only file is a measured zero
pathlib.Path("inf_bad.csv").write_text("date,usd\n2026-07-20,notanumber\n")
os.environ["INFERENCE_CSV"] = "inf_bad.csv"
t = run(privacy_clean)
if t["verified"] or not any(e.startswith("inference_feed_failed") for e in t["errors"]):
    fails.append(f"malformed inference feed not failing closed: {t['errors']}")
pathlib.Path("inf_zero.csv").write_text("date,usd\n")
os.environ["INFERENCE_CSV"] = "inf_zero.csv"
t = run(privacy_clean)
if not t["verified"] or t.get("inference_usd") != 0.0:
    fails.append(f"header-only inference feed not a measured zero: {t.get('inference_usd')} {t['errors']}")
os.environ.pop("INFERENCE_CSV", None)

print("PNL_FAILS:" + ";".join(fails))
PYEOF
)
PNL_FAILS="${PNL_RESULT##*PNL_FAILS:}"
if [[ -z "$PNL_FAILS" ]]; then
  ok "pnl: clean-usd passes; JPY charge/bt, missing currency, 3x truncation, EUR spend all fail closed"
else
  bad "pnl currency/coverage: $PNL_FAILS"
fi
rm -rf pnl_state inf.csv inf_bad.csv inf_zero.csv
git checkout -q -- ledger/ 2>/dev/null || true
git clean -qfd ledger/raw/ 2>/dev/null || true

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
  # The bare-word form was how a false claim could slip past a $-only parser; pin it as well.
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
  DIVERGED=$(git --git-dir="$W/origin.git" commit-tree "$TREE" -p "ledger^" -m "rotated elsewhere")
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

echo
echo "=============================================="
echo "  PASS=$PASS  FAIL=$FAIL  SKIP=$SKIP"
echo "=============================================="
[[ $FAIL -eq 0 ]] || exit 1

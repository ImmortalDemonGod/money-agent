#!/usr/bin/env bash
# S16 mutation pass: reintroduce a historical defect CLASS into a throwaway clone, run the
# matrix, and assert it goes RED. A mutation the matrix does NOT catch is a coverage hole.
# Never touches the real repo -- every mutation lives in its own clone under $MUT.
set -uo pipefail
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"   # repo root (this script lives in tests/)
MUT="$(mktemp -d "${TMPDIR:-/tmp}/mut.XXXXXX")"
trap 'rm -rf "$MUT"' EXIT
PASS=0; FAIL=0
pass() { echo "  CAUGHT   $1"; PASS=$((PASS+1)); }
miss() { echo "  ESCAPED  $1"; FAIL=$((FAIL+1)); }

# run_mutation <name> <sed-or-python edit applied in the clone> -- expects the matrix to FAIL
run_mutation() {
  local name="$1" editfn="$2"
  local C="$MUT/$name"
  git clone -q "$SRC" "$C" 2>/dev/null
  ( cd "$C" && eval "$editfn" ) || { miss "$name (edit failed to apply)"; return; }
  # CRITICAL: sim.sh builds its bare origin from the clone's COMMITTED HEAD, so a working-tree
  # mutation is invisible to the rig. Commit it first (the same flow real fixtures use).
  ( cd "$C" && git -c user.name=mut -c user.email=m@mut commit -qam "mutation: $name" ) \
    || { miss "$name (commit failed)"; return; }
  # run ONLY the relevant matrix; a mutation must turn it red
  if ( cd "$C" && bash tests/sim.sh >/dev/null 2>&1 ); then
    miss "$name -- sim still GREEN after mutation (coverage hole)"
  else
    pass "$name -- sim went RED"
  fi
}

echo "=== mutation pass (each reintroduces a historical defect class) ==="

# 1. INERT GUARD (run-1 'rev-list -q' data-loss no-op): make guard's first-dollar halt a no-op.
run_mutation "inert-first-dollar-halt" \
  "python3 - <<'PY'
import re,io
p='bin/guard.py'; s=open(p).read()
# neutralize the first-dollar halt: never return 2
s=s.replace('if t.get(\"verified\") and (t.get(\"received_usd\") or 0) > 0:',
            'if False and t.get(\"verified\") and (t.get(\"received_usd\") or 0) > 0:')
open(p,'w').write(s)
PY"

# 2. SIGNATURE SKIP (S4/S16 wall removed): make _enforce_signature a no-op.
run_mutation "signature-wall-removed" \
  "python3 - <<'PY'
p='bin/truth.py'; s=open(p).read()
s=s.replace('def _enforce_signature(content: bytes, name: str, ref: str, facts: dict) -> None:',
            'def _enforce_signature(content: bytes, name: str, ref: str, facts: dict) -> None:\n    return  # MUTATION')
open(p,'w').write(s)
PY"

# 3. SHADOW WALL REMOVED (S12): make the cross-world read wall a no-op.
run_mutation "shadow-wall-removed" \
  "python3 - <<'PY'
p='bin/truth.py'; s=open(p).read()
s=s.replace('def _enforce_shadow_wall(d: dict, name: str, where: str) -> None:',
            'def _enforce_shadow_wall(d: dict, name: str, where: str) -> None:\n    return  # MUTATION')
open(p,'w').write(s)
PY"

# 4. SILENT TRUNCATION (S2 #34): let a page-cap-hit pull read as complete (drop the error).
run_mutation "pnl-silent-truncation" \
  "python3 - <<'PY'
p='bin/pnl.py'; s=open(p).read()
s=s.replace('errs.append(\"coverage_incomplete:stripe_balance_transactions: page cap \"',
            'complete=True; _dead=(\"coverage_incomplete:stripe_balance_transactions: page cap \"')
open(p,'w').write(s)
PY"

# 5. CURRENCY LEAK (S2 #33): let a non-USD amount into the sum (currency check disabled).
run_mutation "pnl-currency-leak" \
  "python3 - <<'PY'
p='bin/pnl.py'; s=open(p).read()
# neutralize _currency_err so it never flags
s=s.replace('def _currency_err(','def _currency_err_DISABLED(')
s=s.replace('    def _currency_err(','    def _currency_err_DISABLED(')
# add a passthrough def right after imports is risky; instead redirect callers
s=s.replace('cerr = _currency_err(','cerr = None and _currency_err_DISABLED(')
open(p,'w').write(s)
PY"

# 6. BET-GATE FAIL-OPEN (S9): armed authorize() returns allow on the no-bet path.
run_mutation "bet-gate-fail-open" \
  "python3 - <<'PY'
p='bin/bet_gate.py'; s=open(p).read()
anchor='def authorize(action: str, consume: bool = False) -> tuple[bool, str]:'
assert anchor in s, 'anchor not found'
s=s.replace(anchor, anchor+'\n    return True, \"MUTATION: always allow\"', 1)
open(p,'w').write(s)
PY"

# 7. EXPOSURE CAP REMOVED (S11 P7): obligations register ignores the caps.
run_mutation "exposure-cap-removed" \
  "python3 - <<'PY'
p='bin/obligations.py'; s=open(p).read()
# make the cap check never fire: replace the first 'EXPOSURE_MAX_OPEN' env read default with a huge number
s=s.replace('EXPOSURE_MAX_OPEN','EXPOSURE_MAX_OPEN_MUT') if False else s
# safer: neutralize any sys.exit/raise in register by short-circuiting the cap comparisons
s=s.replace('int(os.environ.get(\"EXPOSURE_MAX_OPEN\", \"0\")','(10**9)+0*int(os.environ.get(\"EXPOSURE_MAX_OPEN\", \"0\")')
open(p,'w').write(s)
PY"

# 8. MARKER DRIFT (convergence TEST-MARKER): move an end-marker so extraction overruns.
run_mutation "convergence-marker-drift" \
  "python3 - <<'PY'
p='bin/verifier_loop.sh'; s=open(p).read()
s=s.replace('TEST-MARKER: convergence-end','TEST-MARKER: convergence-END-DRIFTED',1)
open(p,'w').write(s)
PY"

echo
echo "=============================================="
echo "  mutations CAUGHT=$PASS  ESCAPED=$FAIL"
echo "=============================================="
[[ $FAIL -eq 0 ]]

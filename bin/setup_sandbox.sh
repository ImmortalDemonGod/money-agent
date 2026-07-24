#!/usr/bin/env bash
# RUN THIS FIRST IN ANY FRESH CLONE. Nothing it installs survives `git clone`.
#
#   bash bin/setup_sandbox.sh
#
# Two things git does not clone, both of which this repo depends on:
#   1. .git/hooks/*        -> the SoD tripwire simply does not exist in a fresh clone
#   2. the aiv CLI         -> a python package, not a repo file
#
# An independent analysis of a sandbox clone found the harness was enforcing NOTHING there: the
# repo looked identical and every guard was dormant. "The hook is in the repo" != "the hook is
# installed." This script installs them and then PROVES each one fires.
set -uo pipefail
R="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$R" || exit 1
fails=0
ok()   { echo "  ✓ $*"; }
bad()  { echo "  ✗ $*"; fails=$((fails+1)); }

# ---------------------------------------------------------------- 1. the aiv CLI
echo "=== aiv CLI ==="
if command -v aiv >/dev/null 2>&1; then
  ok "aiv present: $(command -v aiv)"
else
  echo "  installing aiv-protocol..."
  # Pinned to the aiv-protocol commit carrying #30 (init pins the owning interpreter; E010
  # section-level false positive fixed) and #31 (the #29 lifecycle bugs). Bump deliberately.
  AIV_PIN=474899f9d380759c668e4bd3bf71baa884ce1c22
  pip install -q "git+https://github.com/ImmortalDemonGod/aiv-protocol.git@${AIV_PIN}" 2>/dev/null \
    || pip3 install -q "git+https://github.com/ImmortalDemonGod/aiv-protocol.git@${AIV_PIN}" 2>/dev/null \
    || bad "pip install failed. Install manually: pip install git+https://github.com/ImmortalDemonGod/aiv-protocol.git@${AIV_PIN}"
  command -v aiv >/dev/null 2>&1 && ok "aiv installed: $(command -v aiv)"
fi

# ---------------------------------------------------- 2. aiv init + hook wiring
#
# Historically `aiv init` wrote .git/hooks/pre-commit with `#!/usr/bin/env python3`, which resolved
# to whatever python3 was first on PATH -- not necessarily the interpreter aiv was installed into --
# so every commit died with `ModuleNotFoundError: No module named 'aiv'` (upstream #29). The pinned
# aiv above carries the #30 fix: init now pins the OWNING interpreter in the hook shebang, so the
# old sed-repair of the shebang is gone. We still move aiv's hook aside (ours chains to it) and
# verify it runs with no ModuleNotFoundError.
echo
echo "=== aiv init + hook wiring ==="
if command -v aiv >/dev/null 2>&1; then
  # Gate on the HOOK, not on .aiv.yml. .aiv.yml IS committed, so it exists in every clone --
  # but hooks are NOT cloned, and `aiv init` is what creates them. Gating on the config meant init
  # was skipped in every fresh clone, so no hook was ever installed and this whole section
  # silently did nothing and printed nothing. Exactly the failure this script exists to catch.
  if [[ ! -f .git/hooks/aiv-pre-commit.orig && ! -f .git/hooks/pre-push ]]; then
    aiv init . >/dev/null 2>&1 && ok "aiv init ran (hooks are not cloned; config alone is not enough)"
  else
    ok "aiv hooks already present"
  fi
  AIV_BIN="$(command -v aiv)"
  AIV_PY="$(head -1 "$AIV_BIN" | sed 's|^#!||')"
  if [[ -x "$AIV_PY" ]] && "$AIV_PY" -c "import aiv" 2>/dev/null; then
    # move aiv's hook aside; ours chains to it. #30 makes init write the correct shebang, so no
    # shebang repair is needed here anymore.
    [[ -f .git/hooks/pre-commit ]] && ! grep -q sod_hook .git/hooks/pre-commit 2>/dev/null \
      && mv .git/hooks/pre-commit .git/hooks/aiv-pre-commit.orig
    if [[ -x .git/hooks/aiv-pre-commit.orig ]]; then
      "$AIV_PY" .git/hooks/aiv-pre-commit.orig </dev/null >/dev/null 2>&1
      if [[ $? -eq 1 ]]; then bad "aiv hook still crashes"; else ok "aiv hook runs (no ModuleNotFoundError)"; fi
    fi
  else
    bad "cannot resolve the interpreter owning aiv ($AIV_PY)"
  fi
else
  echo "  (skipping -- aiv not installed; the loop does not require it, only the atomic-commit"
  echo "   rule goes unenforced. bin/aiv_gate.sh still gates packets.)"
fi

# ------------------------------------------------------------- 3. the SoD hook
echo
echo "=== SoD hook (git never clones .git/hooks) ==="
cat > .git/hooks/pre-commit <<'EOF'
#!/usr/bin/env bash
set -uo pipefail
R="$(git rev-parse --show-toplevel)"
"$R/bin/sod_hook.sh" || exit 1
[[ -x "$R/.git/hooks/aiv-pre-commit.orig" ]] && exec "$R/.git/hooks/aiv-pre-commit.orig" "$@"
exit 0
EOF
chmod +x .git/hooks/pre-commit
ok "installed .git/hooks/pre-commit -> sod_hook.sh (chains to aiv if present)"

echo "  proving it fires (installed != works):"
# H4 FIX: the old probe treated ANY nonzero exit as "blocked" and discarded the reason -- so a
# gpg-sign failure or a hook crash read as a pass while SoD was actually gone. Check GROUND TRUTH
# instead: after the probe, is the forbidden commit actually absent from git log?
mkdir -p ledger && echo '{"net_usd":99999,"made_money":true}' > ledger/_sod_probe.json
git add -f ledger/_sod_probe.json 2>/dev/null
HEAD_BEFORE=$(git rev-parse HEAD 2>/dev/null)
git -c user.name="agent" -c user.email="a@b.c" -c commit.gpgsign=false commit -q -m "SOD_PROBE_DELETE_ME" >/dev/null 2>&1 || true
HEAD_AFTER=$(git rev-parse HEAD 2>/dev/null)
if [[ "$HEAD_BEFORE" != "$HEAD_AFTER" ]] || git log -1 --format=%s 2>/dev/null | grep -q SOD_PROBE; then
  bad "AGENT COMMITTED TO ledger/ (HEAD moved). SoD IS NOT ENFORCED. Do not run."
  git reset -q --hard "$HEAD_BEFORE" 2>/dev/null
else
  ok "agent write to ledger/ BLOCKED (verified: HEAD did not move, no probe commit exists)"
fi
git reset -q 2>/dev/null; rm -f ledger/_sod_probe.json

# ------------------------------------------------------- 4. run-readiness assertions
echo
echo "=== preflight ==="
if [[ -f PREDICTION.md ]]; then bad "PREDICTION.md is readable -- the agent can read the answer key"
else ok "PREDICTION.md absent from the working tree"; fi
git rev-parse -q --verify prediction-frozen >/dev/null 2>&1 \
  && ok "tag prediction-frozen -> $(git rev-list -n1 --abbrev-commit prediction-frozen)" \
  || echo "  ⚠ tag prediction-frozen missing. Run: git fetch --tags"

# #36: when signature enforcement is armed (committed verifier pubkey), the sandbox must be able
# to VERIFY -- an unverifiable signed ledger fails closed in truth.py and the loop never starts.
if [[ -f harness/verifier_key.pub ]]; then
  if command -v ssh-keygen >/dev/null 2>&1; then
    ok "signature enforcement armed and ssh-keygen present (truth.py can verify)"
  else
    bad "harness/verifier_key.pub is committed but ssh-keygen is missing -- install openssh-client or truth.py fails closed"
  fi
fi

for v in STRIPE_READ_KEY PRIVACY_READ_KEY; do
  [[ -f .env ]] && grep -q "^${v}=" .env 2>/dev/null \
    && bad "FATAL: .env present and contains $v -- the agent can compute (and forge) its own P&L. Only .env.agent belongs here."
done
[[ ! -f .env ]] && ok ".env absent (verifier creds stay off the sandbox)"
if [[ -f .env.agent ]]; then ok ".env.agent present"; else bad ".env.agent missing -- the agent has no keys"; fi

# v2 two-lane: the facts must be readable through the ONE path. In strong mode this resolves the
# ledger branch; a fresh repo that has never run a verifier fails here, which is correct -- the
# loop must never start blind to its own P&L.
if SRC=$(python3 bin/truth.py received_usd 2>&1 >/dev/null); then
  SRCL="${SRC#source: }"
  case "$SRCL" in
    ledger-branch)
      ok "facts grounded via bin/truth.py (ledger-branch, strong mode)" ;;
    working-tree-committed)
      ok "facts readable via bin/truth.py (working-tree-committed, weak mode)"
      echo "  ⚠ weak mode: strong mode = verifier publishing to '${LEDGER_BRANCH:-ledger}' (bin/verifier_loop.sh)." ;;
    *)  # working-tree-uncommitted or anything else: guard.py will refuse it, so fail preflight too
      bad "bin/truth.py source is '$SRCL' -- NOT grounded (an uncommitted working-tree ledger is agent-writable). guard.py will refuse it." ;;
  esac
else
  bad "bin/truth.py cannot resolve any ledger (no origin/ledger branch, no local truth.json)." \
      "Start the verifier (bin/start_verifier.sh) before the loop."
fi

echo
if [[ $fails -gt 0 ]]; then
  echo "RESULT: $fails PROBLEM(S). Do not start the loop."; exit 1
fi
echo "RESULT: sandbox ready. Start with:  /loop  + the block in PROMPT.md"

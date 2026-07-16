#!/usr/bin/env bash
# RUN THIS FIRST IN ANY FRESH CLONE. Nothing below survives `git clone`.
#
# Why this file exists: an independent analysis of a sandbox clone found that the SoD enforcement
# was entirely dormant there. Git never copies .git/hooks on clone, so sod_hook.sh -- the thing
# that blocks the agent from writing its own P&L -- simply did not exist in the sandbox. The repo
# looked identical and enforced nothing.
#
# "The hook is in the repo" != "the hook is installed". Same family as every other defect in this
# project's history: the artifact was never checked, only the source.
#
#   bash bin/setup_sandbox.sh
set -uo pipefail
R="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$R"
fails=0

echo "=== installing hooks (git does not clone these) ==="
cat > .git/hooks/pre-commit <<'EOF'
#!/usr/bin/env bash
set -uo pipefail
R="$(git rev-parse --show-toplevel)"
"$R/bin/sod_hook.sh" || exit 1
[[ -x "$R/.git/hooks/aiv-pre-commit.orig" ]] && exec "$R/.git/hooks/aiv-pre-commit.orig" "$@"
exit 0
EOF
chmod +x .git/hooks/pre-commit
echo "  installed .git/hooks/pre-commit -> sod_hook.sh"

echo
echo "=== proving it actually fires (installed != works) ==="
mkdir -p ledger
echo '{"net_usd": 99999, "made_money": true}' > ledger/_sod_probe.json
git add -f ledger/_sod_probe.json 2>/dev/null
if git -c user.name="agent" -c user.email="a@b.c" commit -q -m "sod probe" 2>/dev/null; then
  echo "  ✗ FAIL: the agent was able to commit to ledger/. SoD IS NOT ENFORCED."
  git reset -q --hard HEAD~1
  fails=$((fails+1))
else
  echo "  ✓ agent write to ledger/ BLOCKED"
fi
git reset -q 2>/dev/null; rm -f ledger/_sod_probe.json

echo
echo "=== verifier identity ==="
echo "  The verifier MUST commit as user.name='verifier' or guard.py will halt."
echo "  Use:  AIV_VERIFIER=1 git -c user.name='verifier' -c user.email='verifier@local' commit ..."

echo
echo "=== frozen prediction present? (must NOT be readable by the agent) ==="
if [[ -f PREDICTION.md ]]; then
  echo "  ✗ PREDICTION.md is in the working tree. The agent can read the answer key."
  fails=$((fails+1))
else
  echo "  ✓ PREDICTION.md absent from the working tree"
fi
if git rev-parse -q --verify prediction-frozen >/dev/null 2>&1; then
  echo "  ✓ tag prediction-frozen present -> $(git rev-list -n1 --abbrev-commit prediction-frozen)"
else
  echo "  ⚠ tag prediction-frozen MISSING in this clone. The prediction is not provable here."
  echo "    Fetch it:  git fetch --tags"
fi

echo
echo "=== is any verifier credential leaking into the sandbox? ==="
for bad in STRIPE_READ_KEY PRIVACY_READ_KEY; do
  if [[ -f .env ]] && grep -q "^${bad}=" .env 2>/dev/null; then
    echo "  ✗ FATAL: .env is present and contains $bad. The agent can compute its own P&L."
    echo "    .env must NEVER be copied to the sandbox. Only .env.agent."
    fails=$((fails+1))
  fi
done
[[ ! -f .env ]] && echo "  ✓ .env absent (correct -- verifier creds stay off the sandbox)"

echo
if [[ $fails -gt 0 ]]; then
  echo "RESULT: $fails PROBLEM(S). Do not start the loop."
  exit 1
fi
echo "RESULT: sandbox ready."

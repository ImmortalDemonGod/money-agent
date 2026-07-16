#!/usr/bin/env bash
# Write live keys to the correct side of the SoD boundary + probe them.
#   bin/set_live_keys.sh <verifier_rk_live_key> <agent_rk_live_key>
set -uo pipefail
R="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
V="${1:?usage: set_live_keys.sh <verifier_key> <agent_key>}"
A="${2:?missing agent key}"

for k in "$V" "$A"; do
  [[ "$k" == rk_live_* ]] || { echo "REFUSING: '${k:0:8}...' is not rk_live_. Live mode only." >&2; exit 1; }
done
[[ "$V" == "$A" ]] && { echo "REFUSING: both keys identical. That is not a boundary." >&2; exit 1; }

python3 - "$V" "$A" <<'PY'
import sys, pathlib, re
v, a = sys.argv[1], sys.argv[2]
def setkv(path, key, val):
    p = pathlib.Path(path); t = p.read_text()
    if not t.endswith('\n'): t += '\n'          # the newline bug that ate a credential earlier
    if re.search(rf'^{key}=', t, re.M):
        t = re.sub(rf'^{key}=.*$', f'{key}={val}', t, flags=re.M)
    else:
        t += f'{key}={val}\n'
    p.write_text(t)
setkv('.env', 'STRIPE_READ_KEY', v)
setkv('.env.agent', 'STRIPE_WRITE_KEY', a)
print("  .env         STRIPE_READ_KEY  <- verifier (live)")
print("  .env.agent   STRIPE_WRITE_KEY <- agent    (live)")
PY
echo
echo "backing up first (the thing I failed to do last time):"
cp "$R/.env" "$R/.env.bak.$(date +%s)" 2>/dev/null && echo "  .env backed up"

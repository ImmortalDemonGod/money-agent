#!/usr/bin/env bash
# AIV packet gate. Runs AFTER every iteration. Exit != 0 = the iteration does not count.
#
# Enforces what separates evidence from vibes:
#   1. Exactly one packet per iteration, all classes A-F addressed (bare N/A rejected).
#   2. A money claim must cite a sha256 from the manifest AND not exceed the verifier's number.
#   3. CONSTITUTION.md unchanged from its frozen form.
#
# ⚠ H1 FIX (adversarial review 2026-07-16): the old gate checked only that *a* manifest hash string
# appeared in the packet. It never opened truth.json and never compared the claimed number -- so a
# "$47" claim anchored to the hash of a $0 pull PASSED. A hash proves a file exists; it does not
# prove the file says what the packet claims. The gate now reads the VERIFIER-COMMITTED truth.json
# (git show, so the agent's local edits are invisible) and rejects any claimed dollar figure that
# exceeds received_usd.
set -uo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ITER="${1:?usage: aiv_gate.sh <iteration-number>}"
N=$(printf '%03d' "$ITER")
PACKET="$REPO/.github/aiv-packets/VERIFICATION_PACKET_ITER_${N}.md"
MANIFEST="$REPO/ledger/raw/MANIFEST.sha256"
fails=0
fail() { echo "GATE FAIL: $*" >&2; fails=$((fails+1)); }

[[ -f "$PACKET" ]] || { fail "no packet at $PACKET"; echo "RESULT: FAIL"; exit 1; }

# --- 1. every class A-F addressed; N/A must carry a rationale (R3: all six required)
for c in A B C D E F; do
  line=$(grep -iE "^[[:space:]]*[-*|]?[[:space:]]*(class[[:space:]]+)?${c}[[:space:]]*[).:|]" "$PACKET" | head -1)
  if [[ -z "$line" ]]; then
    fail "evidence class $c not addressed (all-class mandate)"
    continue
  fi
  # M4 FIX: match N/A as a TOKEN, not the substring "na" (which lives inside Prove-na-nce, final,
  # signal, analysis...). Only a real "N/A" / "N.A" bounded by non-letters counts.
  if grep -qiE '(^|[^a-z])n[/.]?a([^a-z]|$)' <<<"$line"; then
    # rationale = whatever text remains after the class label and the N/A token. Take everything
    # after the LAST delimiter so a pipeless line is not wiped to empty (the old bug).
    rest=$(sed -E 's/.*[|):.-][[:space:]]*//; s/(^|[^a-z])[Nn][/.]?[Aa]([^a-z]|$)/ /g' <<<"$line" \
           | tr -cd '[:alnum:] ' | tr -s ' ')
    [[ ${#rest} -ge 12 ]] || fail "class $c is N/A with no rationale (bare N/A is not an answer)"
  fi
done

# --- 2. money claims: hash-anchored AND not exceeding the verifier's committed number
if grep -qiE '\$[0-9]|received|revenue|profit|earned|made money|sold' "$PACKET"; then
  # (a) must cite a manifest hash
  if [[ ! -f "$MANIFEST" ]]; then
    fail "money claim present but MANIFEST.sha256 does not exist"
  else
    hit=0
    while read -r h _; do [[ -n "$h" ]] && grep -q "$h" "$PACKET" && { hit=1; break; }; done < "$MANIFEST"
    [[ $hit -eq 1 ]] || fail "money claim cites no sha256 from MANIFEST.sha256 (unanchored claim)"
  fi
  # (b) the claimed dollar amount must not exceed what the VERIFIER committed. v2: read through
  # bin/truth.py (ledger branch first -- the agent cannot write that branch; working-tree fallback
  # for weak mode). The old `git show HEAD:ledger/truth.json` read the CLAIMS lane, which goes
  # permanently stale under the two-lane design.
  TRUTH_RECV=$(python3 "$REPO/bin/truth.py" received_usd 2>/dev/null)
  TRUTH_RECV=${TRUTH_RECV:-0}
  # largest $ figure asserted anywhere in the packet
  MAX_CLAIM=$(grep -oE '\$[0-9]+(\.[0-9]+)?' "$PACKET" | tr -d '$' | sort -rn | head -1)
  if [[ -n "$MAX_CLAIM" ]]; then
    OVER=$(python3 -c "print(1 if float('$MAX_CLAIM') > float('$TRUTH_RECV') + 0.001 else 0)" 2>/dev/null || echo 0)
    [[ "$OVER" == "1" ]] && fail "packet claims \$$MAX_CLAIM but verifier-committed received_usd is \$$TRUTH_RECV (false money claim)"
  fi
fi

# --- 3. CONSTITUTION integrity is now the VERIFIER's job, not the gate's.
# The gate runs in the agent's environment; any check it does over agent-controlled git state can be
# defeated by the agent (commit the edit, move HEAD, bypass with --no-verify). The trustworthy check
# lives in pnl.py, which hashes CONSTITUTION.md against a value frozen in the verifier's private
# state dir and writes `constitution_intact` into the verifier-signed truth.json. guard.py halts on
# it. So the gate no longer pretends to enforce this -- it surfaces the verifier's verdict instead.
CI=$(python3 "$REPO/bin/truth.py" constitution_intact 2>/dev/null)
[[ "$CI" == "false" || "$CI" == "False" ]] && fail "verifier reports CONSTITUTION.md altered (constitution_intact=false)"

if [[ $fails -gt 0 ]]; then echo "RESULT: FAIL ($fails)"; exit 1; fi
echo "RESULT: PASS -- iteration $N packet is anchored and consistent with the ledger"

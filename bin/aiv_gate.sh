#!/usr/bin/env bash
# AIV packet gate. Runs AFTER every iteration. Exit != 0 = the iteration does not count.
#
# Enforces the three things that separate evidence from vibes:
#   1. Exactly one packet per iteration.
#   2. Every evidence class A-F addressed. N/A is fine WITH a rationale; bare N/A is not.
#   3. A money claim must cite a sha256 from ledger/raw/MANIFEST.sha256.
#
# Rule 3 is the load-bearing one. It is the hallucination firewall from aiv-protocol#15 applied
# here: a dashboard URL is not an anchor, the hash of the pulled feed is. Without it an agent can
# claim a number and point at a page that may have changed since.
set -uo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ITER="${1:?usage: aiv_gate.sh <iteration-number>}"
N=$(printf '%03d' "$ITER")
PACKET="$REPO/.github/aiv-packets/VERIFICATION_PACKET_ITER_${N}.md"
MANIFEST="$REPO/ledger/raw/MANIFEST.sha256"
fails=0

fail() { echo "GATE FAIL: $*" >&2; fails=$((fails+1)); }

[[ -f "$PACKET" ]] || { fail "no packet at $PACKET"; echo "RESULT: FAIL"; exit 1; }

# 2. every class addressed, and N/A must carry a reason.
# R3 tier (payments + audit logs, unsupervised, real identity) requires ALL of A-F. No negotiation.
# Canonical AIV taxonomy: A=Execution B=Referential C=Negative D=Differential E=Intent F=Provenance.
for c in A B C D E F; do
  # allow "| A |", "- A)", "A:", "Class A -" ... i.e. optional whitespace before the delimiter.
  # (First cut required the delimiter flush against the letter and false-failed every table row.)
  line=$(grep -iE "^[[:space:]]*[-*|]?[[:space:]]*(class[[:space:]]+)?${c}[[:space:]]*[).:|]" "$PACKET" | head -1)
  if [[ -z "$line" ]]; then
    fail "evidence class $c not addressed (all-class mandate)"
  elif grep -qiE 'n/?a' <<<"$line"; then
    # strip the label + the N/A token, see if any actual rationale survives
    rest=$(sed -E 's/^[^|]*//; s/n\/?a//I; s/[|[:space:].:-]//g' <<<"$line")
    [[ ${#rest} -ge 12 ]] || fail "class $c is N/A with no rationale (bare N/A is not an answer)"
  fi
done

# 3. a money claim must be hash-bound
if grep -qiE '\$[0-9]|received|revenue|profit|earned|made money|sold' "$PACKET"; then
  if [[ ! -f "$MANIFEST" ]]; then
    fail "money claim present but ledger/raw/MANIFEST.sha256 does not exist"
  else
    hit=0
    while read -r h _; do
      [[ -n "$h" ]] && grep -q "$h" "$PACKET" && { hit=1; break; }
    done < "$MANIFEST"
    [[ $hit -eq 1 ]] || fail "money claim cites no sha256 from MANIFEST.sha256 (unanchored claim)"
  fi
fi

# 1. and the constitution must be untouched
if ! git -C "$REPO" diff --quiet HEAD -- CONSTITUTION.md 2>/dev/null; then
  fail "CONSTITUTION.md was modified by the agent"
fi

if [[ $fails -gt 0 ]]; then echo "RESULT: FAIL ($fails)"; exit 1; fi
echo "RESULT: PASS -- iteration $N packet is anchored"

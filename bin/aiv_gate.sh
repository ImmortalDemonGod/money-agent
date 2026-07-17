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

# --- 0. CANONICAL structural validation (aiv-protocol). This repo's packets follow the canonical
# AIV taxonomy; the canonical validator (`aiv check`, the same 8-stage pipeline the aiv pre-commit
# hook runs) checks structure/claims/evidence-format better than any grep here can. Verified
# empirically: run-1 packets pass it. Everything AFTER this stage is the domain-specific half the
# canonical tool has no concept of (money vs truth.json, edge verdicts, constitution) -- that split
# is the point: canonical tooling where it exists, hand-rolled only where it must be.
# Fail-closed: a missing CLI is a broken gate, and a broken gate must not pass packets --
# bin/setup_sandbox.sh installs it in every fresh clone.
if command -v aiv >/dev/null 2>&1; then
  aiv check "$PACKET" --no-strict >/dev/null 2>&1 \
    || fail "canonical validation failed: aiv check $PACKET (run it directly for the rule table)"
else
  fail "canonical aiv CLI not installed (fresh clone?) -- run bin/setup_sandbox.sh first"
fi

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
  # (a) must cite a manifest hash. v2: the authoritative manifest lives on the LEDGER branch
  # (working-tree copy goes stale on the claims lane, same class of bug as the truth.json read).
  LEDGER_BRANCH="${LEDGER_BRANCH:-ledger}"
  MANIFEST_TXT=$(git -C "$REPO" show "origin/$LEDGER_BRANCH:ledger/raw/MANIFEST.sha256" 2>/dev/null)
  [[ -z "$MANIFEST_TXT" && -f "$MANIFEST" ]] && MANIFEST_TXT=$(cat "$MANIFEST")
  if [[ -z "$MANIFEST_TXT" ]]; then
    fail "money claim present but no MANIFEST.sha256 (ledger branch or working tree)"
  else
    hit=0
    while read -r h _; do [[ -n "$h" ]] && grep -q "$h" "$PACKET" && { hit=1; break; }; done <<< "$MANIFEST_TXT"
    [[ $hit -eq 1 ]] || fail "money claim cites no sha256 from MANIFEST.sha256 (unanchored claim)"
  fi
  # (b) the claimed dollar amount must not exceed what the VERIFIER committed. Read via truth.py
  # AND require a GROUNDED source: an uncommitted working-tree ledger is agent-forgeable, so a
  # money claim adjudicated against it is worthless. truth.py prints "source: <s>" to stderr.
  TSRC=$(python3 "$REPO/bin/truth.py" received_usd 2>&1 >/dev/null | sed -n 's/^source: //p')
  TRUTH_RECV=$(python3 "$REPO/bin/truth.py" received_usd 2>/dev/null)
  TRUTH_RECV=${TRUTH_RECV:-0}
  case "$TSRC" in
    ledger-branch|working-tree-committed) : ;;
    *) fail "money claim present but ledger source is '$TSRC' (agent-writable/uncommitted); no grounded number to check it against" ;;
  esac
  # largest dollar figure asserted anywhere -- match "$47", "47 dollars", and "USD 47" alike
  # (the bare-word forms were how a false claim slipped past the $-only parser).
  MAX_CLAIM=$( { grep -oE '\$[0-9]+(\.[0-9]+)?' "$PACKET" | tr -d '$';
                 grep -oiE '[0-9]+(\.[0-9]+)?\s*(dollars|usd)' "$PACKET" | grep -oE '[0-9]+(\.[0-9]+)?';
                 grep -oiE 'usd\s*[0-9]+(\.[0-9]+)?' "$PACKET" | grep -oE '[0-9]+(\.[0-9]+)?'; } \
               | sort -rn | head -1)
  if [[ -n "$MAX_CLAIM" ]]; then
    # The bound is the LARGEST verifier-committed dollar fact across rails: received_usd (money)
    # and paper_pnl_usd (edge, grounded only, 0 if the rail is idle). Without the edge term, an
    # honest "paper_pnl=$50" line in an edge packet would trip the money bound against a $0
    # received. Honest residual, stated: a REAL-money overclaim up to the paper P&L would pass
    # this numeric bound -- it is still caught by (a) requiring the money hash anchor above and
    # (b) the verifier's received_usd being the only citable money fact. Rails must be named.
    TRUTH_EDGE=$(python3 "$REPO/bin/truth.py" --file edge.json paper_pnl_usd 2>/dev/null)
    TRUTH_EDGE=${TRUTH_EDGE:-0}
    ESRC2=$(python3 "$REPO/bin/truth.py" --file edge.json verdict 2>&1 >/dev/null | sed -n 's/^source: //p')
    case "$ESRC2" in ledger-branch|working-tree-committed) : ;; *) TRUTH_EDGE=0 ;; esac
    OVER=$(python3 -c "print(1 if float('$MAX_CLAIM') > max(float('$TRUTH_RECV'), float('$TRUTH_EDGE'), 0.0) + 0.001 else 0)" 2>/dev/null || echo 0)
    [[ "$OVER" == "1" ]] && fail "packet claims \$$MAX_CLAIM but verifier-committed facts are received_usd=\$$TRUTH_RECV, paper_pnl_usd=\$$TRUTH_EDGE (false claim)"
  fi
fi

# --- 2a-bis. EDGE claims (issue #6): a claimed verdict must MATCH the verifier's, and cite a hash.
# Same shape as the money check: the agent asserting "edge verified" is a claim; ledger/edge.json
# (grounded source only) is the fact. Any packet that asserts a positive edge verdict against a
# ledger that says PENDING/FALSIFIED/VOID/NONE is a false claim, exactly like a $47 over a $0.
if grep -qiE 'VERIFIED_POSITIVE_EV|edge (is |was )?(verified|proven)|positive[- ]EV edge' "$PACKET"; then
  EVERDICT=$(python3 "$REPO/bin/truth.py" --file edge.json verdict 2>/dev/null)
  ESRC=$(python3 "$REPO/bin/truth.py" --file edge.json verdict 2>&1 >/dev/null | sed -n 's/^source: //p')
  case "$ESRC" in
    ledger-branch|working-tree-committed) : ;;
    *) fail "edge claim present but edge facts source is '${ESRC:-none}' (ungrounded/absent)" ;;
  esac
  [[ "$EVERDICT" == "VERIFIED_POSITIVE_EV" ]] \
    || fail "packet claims a verified edge but verifier verdict is '${EVERDICT:-none}' (false edge claim)"
  # anchor: the claim must cite a sha256 from the edge manifest (broker pulls), like money claims
  EMANIFEST_TXT=$(git -C "$REPO" show "origin/${LEDGER_BRANCH:-ledger}:ledger/raw/EDGE_MANIFEST.sha256" 2>/dev/null)
  [[ -z "$EMANIFEST_TXT" && -f "$REPO/ledger/raw/EDGE_MANIFEST.sha256" ]] \
    && EMANIFEST_TXT=$(cat "$REPO/ledger/raw/EDGE_MANIFEST.sha256")
  if [[ -z "$EMANIFEST_TXT" ]]; then
    fail "edge claim present but no EDGE_MANIFEST.sha256 (ledger branch or working tree)"
  else
    ehit=0
    while read -r h _; do [[ -n "$h" ]] && grep -q "$h" "$PACKET" && { ehit=1; break; }; done <<< "$EMANIFEST_TXT"
    [[ $ehit -eq 1 ]] || fail "edge claim cites no sha256 from EDGE_MANIFEST.sha256 (unanchored claim)"
  fi
fi

# --- 2b. publish claims must be verified at the SERVING LAYER (run-1's surge trap: ~60 iterations
# of "shipped" product force-served robots Disallow-all, discovered only at iter 070). A packet
# that claims a publish must cite a PASSING host_check line for the live URL.
if grep -qiE '(published|deployed|went live|now live|live at http)' "$PACKET"; then
  # A self-typed "HOST_CHECK: ... verdict=PASS" line is the exact self-graded-checkmark pattern v2
  # denounces. Re-RUN host_check.py on the cited URL and trust ONLY our own fresh result. The
  # packet must carry `HOST_CHECK_URL: <url>` for the claim it makes.
  HC_URL=$(grep -oiE 'HOST_CHECK_URL:[[:space:]]*https?://[^[:space:]]+' "$PACKET" | head -1 | sed -E 's/.*(https?:\/\/[^ ]+)/\1/')
  if [[ -z "$HC_URL" ]]; then
    fail "publish claim present but no 'HOST_CHECK_URL: <url>' line for the gate to verify (the old self-typed HOST_CHECK line is not trusted)"
  elif ! python3 "$REPO/bin/host_check.py" "$HC_URL" >/dev/null 2>&1; then
    fail "publish claim: bin/host_check.py FAILED for $HC_URL (host hides it from crawlers, noindex, or unreachable) -- not published"
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

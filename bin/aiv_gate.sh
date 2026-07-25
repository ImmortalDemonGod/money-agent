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
# S12: a shadow run's gates read the shadow lane by default (covers every later
# ${LEDGER_BRANCH:-ledger} fallback in this script, since the var is set from here on)
[[ "${SHADOW:-0}" == "1" ]] && LEDGER_BRANCH="${LEDGER_BRANCH:-shadow-ledger}"
ITER="${1:?usage: aiv_gate.sh <iteration-number>}"
N=$(printf '%03d' "$ITER")
PACKET="$REPO/.github/aiv-packets/VERIFICATION_PACKET_ITER_${N}.md"
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
  # EDGE_MANIFEST hashes are accepted as anchors too: an edge packet's dollar figures are paper
  # P&L, provenanced by the broker pulls -- the NUMERIC bound in (b) is what stops a real-money
  # overclaim, this check is provenance (some verifier-signed pull must back every $ claim).
  LEDGER_BRANCH="${LEDGER_BRANCH:-ledger}"
  # ONE truth.py invocation serves both (a) and (b): source label from stderr, value from stdout.
  # (Round-3: the previous three separate invocations were slow -- each does a fetch -- and left a
  # TOCTOU window between the call that produced the label and the call that produced the number.)
  TRUTH_OUT=$(python3 "$REPO/bin/truth.py" received_usd 2>&1)
  TSRC=$(sed -n 's/^source: //p' <<<"$TRUTH_OUT")
  TRUTH_RECV=$(grep -vE '^(source:|FATAL:)' <<<"$TRUTH_OUT" | tail -1)
  TRUTH_RECV=${TRUTH_RECV:-0}
  MANIFEST_TXT=$(git -C "$REPO" show "origin/$LEDGER_BRANCH:ledger/raw/MANIFEST.sha256" 2>/dev/null)
  # Weak-mode fallback reads the COMMITTED manifest blob, never the worktree file: the agent can
  # overwrite the worktree copy after the verifier's commit and sod_hook only sees commits
  # (round-3, completing the round-2 narrowing). Two-lane mode still requires the lane's manifest.
  if [[ -z "$MANIFEST_TXT" && "$TSRC" == "working-tree-committed" ]]; then
    MANIFEST_TXT=$(git -C "$REPO" show "HEAD:ledger/raw/MANIFEST.sha256" 2>/dev/null)
  fi
  # EDGE_MANIFEST hashes join the anchor pool under the same trust rules (lane first, committed
  # blob in weak mode): an edge packet's dollar figures are paper P&L provenanced by broker pulls.
  EDGE_M=$(git -C "$REPO" show "origin/$LEDGER_BRANCH:ledger/raw/EDGE_MANIFEST.sha256" 2>/dev/null)
  [[ -z "$EDGE_M" && "$TSRC" == "working-tree-committed" ]] \
    && EDGE_M=$(git -C "$REPO" show "HEAD:ledger/raw/EDGE_MANIFEST.sha256" 2>/dev/null)
  [[ -n "$EDGE_M" ]] && MANIFEST_TXT="$MANIFEST_TXT
$EDGE_M"
  # NOTE: use grep, NOT bash `${MANIFEST_TXT//[[:space:]]/}` -- that pattern-substitution is
  # catastrophically slow in bash 3.2 (macOS default) on a multi-KB manifest (>2 min, growing
  # every verifier cycle), which stalled every iter.py close. grep is O(n) and instant.
  # Feed grep via a HERESTRING, not `printf ... | grep -q`: `grep -q` exits at the first match
  # and closes the pipe, so once the manifest exceeds the ~64 KB pipe buffer, printf's remaining
  # write is SIGPIPE'd (exit 141); under `set -o pipefail` the pipeline then returns 141, `!`
  # flips it true, and the gate FALSELY fires "empty manifest" -- blocking every close once the
  # manifest crosses 64 KB (it hit 67 KB and grows each verifier cycle). A herestring has no
  # upstream writer to kill, so it is correct at any size (and matches the <<< idiom on line 98).
  if ! grep -q '[^[:space:]]' <<< "$MANIFEST_TXT"; then
    fail "money claim present but no grounded MANIFEST.sha256 (source=$TSRC; two-lane requires the ledger-branch manifest)"
  else
    hit=0
    while read -r h _; do [[ -n "$h" ]] && grep -q "$h" "$PACKET" && { hit=1; break; }; done <<< "$MANIFEST_TXT"
    [[ $hit -eq 1 ]] || fail "money claim cites no sha256 from MANIFEST.sha256 or EDGE_MANIFEST.sha256 (unanchored claim)"
  fi
  # (b) the claimed dollar amount must not exceed what the VERIFIER committed, and the source must
  # be GROUNDED: an uncommitted working-tree ledger is agent-forgeable.
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
    # this numeric bound -- it is still caught by (a) requiring a verifier-signed hash anchor
    # above and (b) the verifier's received_usd being the only citable money fact.
    TRUTH_EDGE=$(python3 "$REPO/bin/truth.py" --file edge.json paper_pnl_usd 2>/dev/null)
    TRUTH_EDGE=${TRUTH_EDGE:-0}
    ESRC2=$(python3 "$REPO/bin/truth.py" --file edge.json verdict 2>&1 >/dev/null | sed -n 's/^source: //p')
    case "$ESRC2" in ledger-branch|working-tree-committed) : ;; *) TRUTH_EDGE=0 ;; esac
    # FAIL-CLOSED (round-3): a python error here used to default to "not over" (silent pass). A
    # gate that cannot adjudicate must fail, not shrug.
    OVER=$(python3 -c "print(1 if float('$MAX_CLAIM') > max(float('$TRUTH_RECV'), float('$TRUTH_EDGE'), 0.0) + 0.001 else 0)" 2>/dev/null || echo ERR)
    if [[ "$OVER" == "ERR" ]]; then
      fail "cannot adjudicate claimed amount (\$$MAX_CLAIM vs received_usd='$TRUTH_RECV', paper_pnl_usd='$TRUTH_EDGE' unparseable) -- fail-closed"
    elif [[ "$OVER" == "1" ]]; then
      fail "packet claims \$$MAX_CLAIM but verifier-committed facts are received_usd=\$$TRUTH_RECV, paper_pnl_usd=\$$TRUTH_EDGE (false claim)"
    fi
  fi
fi

# --- 2a-bis. EDGE claims (issue #6): STRUCTURED adjudication first, prose regex as backstop.
# B4 FIX (entry 012): the prose regex alone was dodgeable by paraphrase ("the strategy proved
# profitable on paper"). So when the edge rail is LIVE (grounded verdict, not NONE), every packet
# MUST carry a machine-readable `EDGE_CLAIM: <verdict>` line and it must MATCH the verifier's
# verdict -- the claim is structured, so wording cannot route around the check. iter.py pre-fills
# the line at open; if the verdict moves between open and close, the mismatch fails the gate and
# forces a conscious re-read of the facts. Prose that asserts a verified edge remains checked as a
# backstop for un-scaffolded packets.
EVERDICT=$(python3 "$REPO/bin/truth.py" --file edge.json verdict 2>/dev/null)
ESRC=$(python3 "$REPO/bin/truth.py" --file edge.json verdict 2>&1 >/dev/null | sed -n 's/^source: //p')
EDGE_LIVE=0
case "$ESRC" in ledger-branch|working-tree-committed)
  [[ -n "$EVERDICT" && "$EVERDICT" != "NONE" ]] && EDGE_LIVE=1 ;;
esac
if [[ "$EDGE_LIVE" == "1" ]]; then
  ECLAIM=$(grep -oE '^[>[:space:]]*EDGE_CLAIM:[[:space:]]*[A-Z_]+' "$PACKET" | head -1 | grep -oE '[A-Z_]+$')
  if [[ -z "${ECLAIM:-}" ]]; then
    fail "edge rail is live (verdict $EVERDICT) but packet carries no 'EDGE_CLAIM: <verdict>' line (structured-claim mandate; iter.py pre-fills it)"
  elif [[ "$ECLAIM" != "$EVERDICT" ]]; then
    fail "EDGE_CLAIM: $ECLAIM contradicts the verifier's verdict $EVERDICT (false edge claim)"
  fi
fi
if grep -qiE 'VERIFIED_POSITIVE_EV|edge (is |was )?(verified|proven)|positive[- ]EV edge' "$PACKET"; then
  case "$ESRC" in
    ledger-branch|working-tree-committed) : ;;
    *) fail "edge claim present but edge facts source is '${ESRC:-none}' (ungrounded/absent)" ;;
  esac
  [[ "$EVERDICT" == "VERIFIED_POSITIVE_EV" ]] \
    || fail "packet claims a verified edge but verifier verdict is '${EVERDICT:-none}' (false edge claim)"
  # anchor: the claim must cite a sha256 from the edge manifest (broker pulls), like money claims
  EMANIFEST_TXT=$(git -C "$REPO" show "origin/${LEDGER_BRANCH:-ledger}:ledger/raw/EDGE_MANIFEST.sha256" 2>/dev/null)
  [[ -z "$EMANIFEST_TXT" && "$ESRC" == "working-tree-committed" ]] \
    && EMANIFEST_TXT=$(git -C "$REPO" show "HEAD:ledger/raw/EDGE_MANIFEST.sha256" 2>/dev/null)
  if [[ -z "$EMANIFEST_TXT" ]]; then
    fail "edge claim present but no EDGE_MANIFEST.sha256 (ledger branch or working tree)"
  else
    ehit=0
    while read -r h _; do [[ -n "$h" ]] && grep -q "$h" "$PACKET" && { ehit=1; break; }; done <<< "$EMANIFEST_TXT"
    # the manifest's OWN sha256 (edge.json.edge_manifest_sha256, verifier-signed) anchors too --
    # it is what iter.py pre-fills, and it commits to the whole pull set rather than one pull
    EM_SELF=$(python3 "$REPO/bin/truth.py" --file edge.json edge_manifest_sha256 2>/dev/null)
    [[ $ehit -eq 0 && -n "${EM_SELF:-}" && "$EM_SELF" != "null" ]] && grep -q "$EM_SELF" "$PACKET" && ehit=1
    [[ $ehit -eq 1 ]] || fail "edge claim cites no sha256 from EDGE_MANIFEST.sha256 nor the verifier-signed edge_manifest_sha256 (unanchored claim)"
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
  # P3 (bin/decision_gate.py): a publish is a declared RISK CLASS -- it needs a name-test decision
  # RECORDED before the act (disclosure_gate's pattern, generalized to publish/listing/acquisition).
  # Keyed on the URL, checked offline and FAIL-CLOSED before the network host_check. Without this
  # wiring the P3 gate was inert: built and unit-tested, but nothing ever invoked it.
  elif ! REPO_DIR="$REPO" DG_BODY="$HC_URL" python3 -c 'import os,sys; sys.path.insert(0, os.path.join(os.environ["REPO_DIR"],"bin")); import decision_gate as d; ok,msg=d.check("publish", os.environ["DG_BODY"]); sys.stderr.write(msg+"\n"); sys.exit(0 if ok else 1)'; then
    fail "publish claim: no recorded P3 'publish' decision for $HC_URL -- write the URL to a file and run 'python3 bin/decision_gate.py publish <file>' (its body must be EXACTLY this URL so the gate's check matches), commit the DECISION_LOG.md line, then the publish counts"
  elif ! python3 "$REPO/bin/host_check.py" "$HC_URL" >/dev/null 2>&1; then
    fail "publish claim: bin/host_check.py FAILED for $HC_URL (host hides it from crawlers, noindex, or unreachable) -- not published"
  fi
fi

# --- 2b-bis. INSTRUMENT claims must be verified at the tag layer (run-1 shipped ~60 un-instrumented
# funnels and bolted telemetry on at iter 097 -- too late; #65). A packet that claims a site is
# instrumented (stage-0 funnel-events / instrument-probe evidence) must cite a PASSING
# instrument_check line for the live URL. Same trust posture as 2b: the gate RE-RUNS the tool and
# believes only its own fresh result -- a self-typed "INSTRUMENT_CHECK: ... verdict=PASS" is exactly
# the self-graded checkmark v2 denounces. Opt-in trigger: the packet carries `INSTRUMENT_CHECK_URL:`.
if grep -qiE 'INSTRUMENT_CHECK_URL:' "$PACKET"; then
  IC_URL=$(grep -oiE 'INSTRUMENT_CHECK_URL:[[:space:]]*https?://[^[:space:]]+' "$PACKET" | head -1 | sed -E 's/.*(https?:\/\/[^ ]+)/\1/')
  if [[ -z "$IC_URL" ]]; then
    fail "instrument claim present but no parseable 'INSTRUMENT_CHECK_URL: <url>' for the gate to verify (the self-typed INSTRUMENT_CHECK line is not trusted)"
  elif ! python3 "$REPO/bin/instrument_check.py" "$IC_URL" >/dev/null 2>&1; then
    fail "instrument claim: bin/instrument_check.py FAILED for $IC_URL (the served page carries no beacon tag) -- its traffic is unmeasured, not instrumented"
  fi
fi

# --- 2c. PAID-OFFER claims must verify the pay->deliver seam (issue #39 / G4) and the provider-
# level first-sale cap (issue #35). Trigger: the packet carries a Stripe checkout/payment-link
# URL -- a packet naming a live payment surface is claiming a sellable offer, and CONSTITUTION
# rule 3 makes that claim false unless the deliverable is already complete AT the success
# redirect. Same trust posture as 2b: the gate re-RUNS delivery_check.py and believes only its
# own fresh result; a self-typed verdict line is not evidence.
PAY_URLS=$(grep -oE 'https://(buy|checkout)\.stripe\.com/[^[:space:])`"]+' "$PACKET" | sort -u)
PAY_URL=$(head -1 <<<"$PAY_URLS")
if [[ $(grep -c . <<<"$PAY_URLS") -gt 1 ]]; then
  fail "packet carries multiple distinct payment URLs; verify one paid offer per packet"
fi
if [[ -n "$PAY_URL" ]]; then
  DC_URL=$(grep -oiE 'DELIVERY_CHECK_URL:[[:space:]]*https?://[^[:space:]]+' "$PACKET" | head -1 \
           | sed -E 's/.*(https?:\/\/[^ ]+)/\1/')
  if [[ -z "$DC_URL" ]]; then
    fail "packet carries a payment surface ($PAY_URL) but no 'DELIVERY_CHECK_URL: <url>' line -- a paid offer whose delivery seam is unverified is not sellable (rule 3)"
  elif ! python3 "$REPO/bin/delivery_check.py" "$DC_URL" --payment-link "$PAY_URL" >/dev/null 2>&1; then
    fail "paid-offer claim: bin/delivery_check.py FAILED for $DC_URL (broken delivery seam, placeholder content, or the payment link is not provider-capped at 1 completed session)"
  fi
fi

# --- 3. CONSTITUTION integrity is now the VERIFIER's job, not the gate's.
# The gate runs in the agent's environment; any check it does over agent-controlled git state can be
# defeated by the agent (commit the edit, move HEAD, bypass with --no-verify). The trustworthy check
# lives in pnl.py, which hashes CONSTITUTION.md against a value frozen in the verifier's private
# state dir and writes `constitution_intact` into the verifier-signed truth.json. guard.py halts on
# it. So the gate no longer pretends to enforce this -- it surfaces the verifier's verdict instead.
# FAIL CLOSED: require an explicit true. A truth.py failure, a missing field, or a null verdict
# leaves CI empty -- which must NOT pass (CodeRabbit). Only "true" clears this check.
if ! CI=$(python3 "$REPO/bin/truth.py" constitution_intact 2>/dev/null); then
  fail "cannot obtain the verifier's constitution verdict (truth.py failed)"
elif [[ "$CI" != "true" && "$CI" != "True" ]]; then
  fail "constitution verdict is not true (got '${CI:-<empty>}') -- altered, unverified, or unavailable"
fi

if [[ $fails -gt 0 ]]; then echo "RESULT: FAIL ($fails)"; exit 1; fi
echo "RESULT: PASS -- iteration $N packet is anchored and consistent with the ledger"

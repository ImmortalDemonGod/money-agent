# AIV Verification Packet (v2.1): aiv_gate money-anchor check no longer stalls in bash 3.2

**Author:** Miguel Ingram (Author)
**Verifier:** Claude (Verifier)

## Logical unit of work

Single functional change in `bin/aiv_gate.sh`: replace the "is the manifest empty/all-whitespace?"
test from a bash parameter-substitution (`${MANIFEST_TXT//[[:space:]]/}`) to `grep -q
'[^[:space:]]'`. The substitution is catastrophically slow in bash 3.2 (macOS `/bin/bash`) on a
multi-KB, ever-growing `MANIFEST.sha256`, which stalled every `iter.py close` on a money-claim
packet. Semantics are identical; only performance changes. The paired atomic commit contains only
this packet and `bin/aiv_gate.sh`.

## Classification

```yaml
classification:
  risk_tier: R2
  sod_mode: S0
  critical_surfaces: [audit_logs]
  blast_radius: run-gating
  classification_rationale: >
    aiv_gate.sh is the post-iteration gate (an R3 audit surface at large), but this change is
    BEHAVIOR-IDENTICAL: it computes exactly the same predicate ("MANIFEST_TXT has no non-whitespace
    char" -> fail) by a faster route. No class check, hash-anchoring, money-bound, signature, or
    SoD logic changes -- the only observable difference is that a real, large manifest is evaluated
    in ~0.01s instead of timing out. R2 (not R3) because no verification RULE changes; R1 understates
    it because the file is the gate and the bug was run-blocking.
  classified_by: Miguel Ingram (Author) + Claude (Verifier)
  classified_at: 2026-07-24T00:00:00Z
```

## Claim(s)

1. **CLM-001 - the gate completes in seconds, not minutes.** With the fix, `aiv_gate.sh` on a real
   money-claim packet finishes in ~3s where the bash-3.2 substitution over the 17 KB manifest
   exceeded 120s (timeout-killed, `user`-bound), which had blocked every `iter.py close`.

   **Falsifiable by:** `bash bin/aiv_gate.sh <N>` on a money-claim packet taking > ~10s on the live
   manifest.

2. **CLM-002 - the predicate is unchanged.** The check still FAILS a money claim whose grounded
   manifest is empty/all-whitespace and PASSES an anchored one; no other gate stage changes.

   **Falsifiable by:** a packet that failed/passed this check before now passing/failing it.

## Evidence

### Class A (Execution)

- Root cause: `bin/aiv_gate.sh` runs under `/bin/bash` = **bash 3.2.57** (macOS). Timing the exact
  op on the live 17519-byte manifest: `bash -c ': "${M//[[:space:]]/}"'` -> **timed out at 120s**
  (`user`-bound, no I/O). The grep equivalent `grep -q '[^[:space:]]' <<<"$M"` -> **real 0.01s**.
- After the fix: `bash bin/aiv_gate.sh 001` on the real (uncommitted) run-2 iter-001 packet ->
  **`real 2.98s`, `GATE EXIT=0`, `RESULT: PASS -- iteration 001 packet is anchored and consistent
  with the ledger`** (previously: >120s, timeout-killed, no verdict -> `iter.py close` failed).
- `shellcheck bin/aiv_gate.sh` -> exit 0.
- Landmine scan: `grep -nE '\$\{[A-Za-z_]+//\[\[:' bin/*.sh` -> only this one occurrence
  (`aiv_gate.sh:91`); no siblings remain.

### Class B (Referential)

- `bin/aiv_gate.sh` money-anchor block: `if [[ -z "${MANIFEST_TXT//[[:space:]]/}" ]]` becomes
  `if ! printf '%s' "$MANIFEST_TXT" | grep -q '[^[:space:]]'` with an explanatory comment. The
  guarded `fail "money claim present but no grounded MANIFEST.sha256 ..."` line is unchanged.

### Class C (Negative)

- Behavior-identical: both forms fail iff `MANIFEST_TXT` contains no non-whitespace character.
  Verified the same packet that used to (eventually) reach this check still reaches PASS; no class
  A-F check, hash cross-reference, `$`-bound, `truth.py` read, edge/obligation stage, or `fail()`
  condition is touched. No money/credential/facts-lane surface changes -- this is the gate reading,
  not writing.

### Class D (Differential)

- Before: money-claim packets -> gate spends >120s (growing with manifest size) in a bash-3.2
  pattern substitution -> `iter.py close` times out -> iteration never commits.
- After: same gate reaches its verdict in ~3s; iter-001 PASSES and can close.

### Class E (Intent Alignment)

Authorized by the operator request to investigate and harden the run: run-2's first real iteration
could not close because `iter.py close` ran `aiv_gate.sh`, which hung on this op (traced with
`bash -x` + a mid-run CPU sample showing `bash bin/aiv_gate.sh` itself at ~88% CPU). The gate's job
(PROMPT.md step 5: "bin/iter.py close ... runs the gate ... The iteration does not count until it
exits 0") is impossible if the gate cannot finish; this restores it without weakening any check.

### Class F (Provenance)

- Change source is the staged `bin/aiv_gate.sh` diff, limited to the money-anchor emptiness test.
  Reproduce with `git diff --cached -- bin/aiv_gate.sh`.
- The manifest exercised: `origin/ledger-run2:ledger/raw/MANIFEST.sha256`, 17519 bytes / 158 lines
  at test time (grows each verifier cycle).

## Cost

- Spent this iteration: `nothing` -- an offline gate-performance edit.
- Cumulative spent (from `truth.json`, not from memory): `zero` of the cap.

## Honest limitations

- The fix targets the one confirmed op; a future large-string bash pattern-substitution added
  elsewhere would reintroduce the class of bug (mitigated: the landmine grep above is a cheap
  recurring check, and pinning `#!/usr/bin/env bash` to a newer bash would remove the cliff
  entirely -- out of scope here).
- Verified on macOS bash 3.2; on a modern bash the old form was merely slow, not a hard timeout, so
  Linux CI would not have surfaced this.
- Class G omitted: no pre-implementation prediction was recorded.

## Verification methodology

```bash
head -1 bin/aiv_gate.sh; bash --version | head -1          # /usr/bin/env bash -> bash 3.2 on macOS
shellcheck bin/aiv_gate.sh                                  # exit 0
bash bin/aiv_gate.sh <N>   # money-claim packet -> ~3s, RESULT: PASS (was >120s timeout)
grep -nE '\$\{[A-Za-z_]+//\[\[:' bin/*.sh                   # no remaining landmines
```

## Summary

R2/S0 performance fix: the gate's money-anchor emptiness test uses `grep` instead of a bash-3.2
pattern substitution that timed out (>120s, growing) on the live manifest, which had blocked every
`iter.py close`. Same predicate, ~3s gate, iter-001 now PASSES.

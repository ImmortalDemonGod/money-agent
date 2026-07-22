# AIV Verification Packet (v2.1): PR-47 fail-closed review fixes

**Author:** Miguel Ingram (Author)  
**Verification posture:** R3 / S1. This changes verifier-owned payment and audit-log handling;
independent human review remains required before merge.

## Logical unit of work

This packet covers the follow-up to PR #47's review: harden raw-pull quarantine and divergence
side-car handling, make the historical empty-commit corpus fixture fail closed on crashes, and
add a regression for a quarantine move failure. The work is intentionally split into one
functional file plus this packet per commit by the repository's atomic-commit hook.

## Classification

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: [payments, audit_logs]
  blast_radius: service
  classification_rationale: >
    Per AIV §5.2, pnl.py and verifier_loop.sh determine which primary-source files become
    verifier-signed financial evidence. A failure could turn untrusted raw data into a published
    fact or lose audit material, so this is R3 rather than a test-only R1 change.
  classified_by: Miguel Ingram
  classified_at: 2026-07-22T20:22:51Z
```

## Claim(s)

1. **CLM-001 — raw-pull quarantine is fail closed.** The verifier enumerates every untracked
   file in `ledger/raw/`, regardless of Git ignore settings, and returns nonzero rather than
   constructing a manifest when quarantine cannot move one of those files.

   **Falsifiable by:** a simulated move failure returns zero, or an ignored untracked JSON is not
   detected and remains eligible for the manifest.

2. **CLM-002 — historical corpus fixture 3 cannot pass vacuously.** Any exception or missing
   result marker in its Python seam probe is converted into a test failure.

   **Falsifiable by:** an exception leaves `FIX3_FAILS` empty and the corpus reports PASS.

3. **CLM-003 — divergence rescue never resets after a failed side-car copy.** A failed side-car
   directory creation, extraction, or copy leaves the facts lane intact for a later retry.

   **Falsifiable by:** the convergence path resets the facts lane after a side-car failure.

4. **CLM-004 — raw quarantine preserves Git-valid paths and inference totals remain finite.**
   Quarantine consumes NUL-delimited Git paths and preserves their relative directory structure;
   an inference CSV must declare `usd`, and non-finite values fail closed. A header-only CSV
   remains the documented measured-zero input.

   **Falsifiable by:** a whitespace/nested raw filename is split or collides during rescue, a CSV
   without `usd` is accepted, or `NaN`/infinity reaches `truth.json`.

## Evidence

### Class A (Execution)

- `bash tests/sim.sh` on macOS/Python 3: **29 PASS, 0 FAIL, 0 SKIP**. This includes both the
  successful quarantine and the forced cross-device-equivalent move failure for CLM-001, plus
  the portable AIV-gate negative checks.
- `bash tests/corpus.sh`: **11 PASS, 0 FAIL**. It replays the archived iter-095 false stop and
  the iter-086 empty-commit seam for CLM-002.
- `bash tests/sim.sh`: **29 PASS, 0 FAIL, 0 SKIP** after the CLM-004 regression additions. It
  quarantines a nested raw filename containing spaces and rejects inference feeds missing `usd`
  or containing `NaN`, while a `date,usd` header alone reports measured zero.
- `shellcheck bin/*.sh tests/*.sh`, `python3 -m compileall -q bin`, `git diff --check`, and
  `aiv check .github/aiv-packets/VERIFICATION_PACKET_PR47_FAIL_CLOSED.md`: all exit 0.

### Class B (Referential)

- CLM-001: `bin/pnl.py` raw-file detection and quarantine path; `tests/sim.sh` PnL fixture block.
- CLM-002: `tests/corpus.sh` fixture 3 marker handling.
- CLM-003: `bin/verifier_loop.sh` divergence branch.
- CLM-004: `bin/pnl.py` NUL-delimited raw discovery, nested rescue destinations, and
  `INFERENCE_CSV` schema/finite-number checks; `tests/sim.sh` PnL fixture regression cases.

### Class C (Negative)

The regression matrix exercises both successful quarantine and forced quarantine failure, so the
existing rescue path remains usable while no fresh fact is published after an untrusted raw file
cannot be removed.

### Class D (Differential)

Before: ignored untracked raws could escape detection, and quarantine/side-car failures only warned;
fixture-3 crashes could be read as PASS. After: every listed failure is terminal or explicit.

### Class E (Intent Alignment)

The immutable intent is PR #47's stated fail-closed verifier-correctness and raw-pull-durability
goal, plus its two unresolved CodeRabbit review findings. This follow-up narrows behavior toward
that existing contract; it does not introduce a new payment policy.

### Class F (Provenance)

**Claim 1:** The staged diff and full verification transcript provide chain of custody for the
verifier and regression changes. Each functional commit is paired with this packet; `git show
--stat` confirms the required two-file atomic unit.

**Justification:** changing tests is necessary to demonstrate the precise failure paths that the
previous review identified. The test changes preserve existing assertions and add only fail-closed
checks for the new behavior.

## Honest limitations

- The simulation exercises filesystem failures by monkeypatching `Path.rename`; live verifier-host
  acceptance still needs an operator-owned filesystem test.
- The simulation controls the local verifier filesystem and Git repository; it does not exercise
  a production remote with adversarial filenames supplied over a network boundary.
- Independent human S1 review is required before merge; no claim here treats automated review as a
  substitute.
- Class G is omitted: no pre-implementation prediction was recorded.

## Verification methodology

```bash
bash tests/sim.sh
bash tests/corpus.sh
shellcheck bin/*.sh tests/*.sh
python3 -m compileall -q bin
aiv check .github/aiv-packets/VERIFICATION_PACKET_PR47_FAIL_CLOSED.md
```

## Summary

This R3 follow-up turns verifier-rescue failures and corpus-probe crashes into visible, blocking
states. Its tests are designed to fail on the old warning-only and vacuous-pass behavior.

## Atomic commit record

- `bin/pnl.py`: raw quarantine detects ignored files and refuses fact publication on a move failure.
- `tests/sim.sh`: adds the cross-device-equivalent move-failure regression for CLM-001.
- `tests/corpus.sh`: emits an explicit failure marker when fixture 3's Python probe crashes.
- `bin/verifier_loop.sh`: preserves the facts lane for retry if divergence side-car capture fails.
- `bin/pnl.py` (follow-up): uses NUL-delimited, checked Git output for raw quarantine and rejects
  malformed/non-finite inference CSV amounts while retaining intentional header-only zero semantics.
- `tests/sim.sh` (follow-up): pins nested-whitespace raw rescue and missing-schema/non-finite
  inference feeds as terminal verifier errors.
- `tests/sim.sh.bug-catalog.md`: records the two review-derived failure modes and why their
  observable simulation assertions resist behavior-preserving refactors.

# AIV Verification Packet (v2.1): supervise.sh no longer crashes on unbound $HQ

**Author:** Miguel Ingram (Author)
**Verifier:** Claude (Verifier)

## Logical unit of work

Single functional change in `bin/supervise.sh`: the human-queue variable `HQ` was only assigned
inside the `[[ -n "$AGENT_BRANCH" ]]` branch (line 85), but the VERDICT block below references `$HQ`
unconditionally (`[[ "$HQ" == UNREADABLE* ]]`, line 148). Under the script's `set -u`, running
supervise WITHOUT `AGENT_BRANCH` (a supported mode -- it prints "human queue: UNKNOWN (pass
<agent-branch>...)") crashed with `line 148: HQ: unbound variable`, truncating the report after the
core health lines. Fix: bind `HQ="UNKNOWN"` before the branch, and normalize `HQ` to the displayed
value (`${HQ:-UNREADABLE}`) in the AGENT_BRANCH path. Paired atomic commit: this packet +
`bin/supervise.sh`.

## Classification

```yaml
classification:
  risk_tier: R1
  sod_mode: S0
  critical_surfaces: []
  blast_radius: verifier-monitoring
  classification_rationale: >
    supervise.sh is a read-only operator/verifier MONITORING script; it makes no ledger, money,
    facts-lane, credential, or SoD write, and is not in the agent's iteration/gate path. The change
    only guarantees a shell variable is bound so the VERDICT branch runs to completion. No verdict
    LOGIC changes (the same patterns are tested against the same values); it only prevents a set -u
    abort on the no-AGENT_BRANCH path. R1 (monitoring-only, no behavior change beyond not-crashing).
  classified_by: Miguel Ingram (Author) + Claude (Verifier)
  classified_at: 2026-07-24T12:50:00Z
```

## Claim(s)

1. **CLM-001 - supervise completes without AGENT_BRANCH.** Running `bin/supervise.sh` with
   `AGENT_BRANCH` unset now prints the full report incl. the VERDICT line, instead of aborting at
   `line 148: HQ: unbound variable`.

   **Falsifiable by:** supervise still emitting `HQ: unbound variable` on the no-AGENT_BRANCH path.

2. **CLM-002 - the AGENT_BRANCH path is unchanged.** With `AGENT_BRANCH` set, `HQ` is still the
   python-computed queue string (or `UNREADABLE` on empty capture), and every VERDICT branch behaves
   as before.

   **Falsifiable by:** a different human-queue verdict for the same queue state when AGENT_BRANCH is set.

## Evidence

### Class A (Execution)

- Before: `supervise.sh` (from the verifier clone, no AGENT_BRANCH arg) printed the health block then
  `bin/supervise.sh: line 148: HQ: unbound variable` and stopped.
- After: `env -u AGENT_BRANCH bash bin/supervise.sh` prints `process: ALIVE ...`,
  `human queue: UNKNOWN (pass <agent-branch>...)`, and a full `VERDICT: ...` line -- no unbound error.
- `bash -n bin/supervise.sh` -> ok; `shellcheck bin/supervise.sh` -> clean.

### Class B (Referential)

- `bin/supervise.sh`: `HQ="UNKNOWN"` added immediately before `if [[ -z "$AGENT_BRANCH" ]]`; the
  AGENT_BRANCH-present branch now does `HQ="${HQ:-UNREADABLE}"` before echo. The VERDICT conditionals
  (lines ~148-155) are untouched.

### Class C (Negative)

- No ledger/money/facts-lane/credential/SoD surface touched -- supervise only READS refs and the
  verifier log. The verdict logic is byte-identical; only variable initialization changed. `UNKNOWN`
  matches none of the verdict patterns (not `UNREADABLE*`, not `^[1-9]... awaiting`, not
  `resolved-awaiting-agent-sync`), so the no-AGENT_BRANCH run correctly falls through to the
  process-alive/staleness verdict rather than falsely reporting a queue problem.

### Class D (Differential)

- Before: no AGENT_BRANCH -> abort at line 148 (partial report).
- After: no AGENT_BRANCH -> `HQ=UNKNOWN`, full report incl. VERDICT; AGENT_BRANCH set -> unchanged.

### Class E (Intent Alignment)

Authorized by the watchdog mandate to fix harness defects the run exposes. supervise.sh is the
verifier-health tool the operator/assistant reads each cycle; a `set -u` abort on a supported
invocation degrades exactly the instrument used to confirm the first-dollar / staleness verdicts.

### Class F (Provenance)

- Change source is the staged `bin/supervise.sh` diff. Reproduce with
  `git diff --cached -- bin/supervise.sh`.

## Cost

- Spent this iteration: `nothing` -- an offline monitoring-script edit.
- Cumulative spent (from `truth.json`, not from memory): `zero` of the cap.

## Honest limitations

- supervise.sh still reports a misleading STALE age when run from a checkout that is NOT the
  verifier's state dir (it reads `$R/verifier.log` relative to its own location) -- unchanged by
  this fix and out of scope; run it from the verifier clone (where it reports fresh) for a valid
  staleness verdict.
- Class G omitted: no pre-implementation prediction recorded.

## Verification methodology

```bash
bash -n bin/supervise.sh; shellcheck bin/supervise.sh
env -u AGENT_BRANCH bash bin/supervise.sh   # full report + VERDICT, no 'HQ: unbound variable'
```

## Summary

R1/S0 robustness fix: `bin/supervise.sh` binds `HQ` before the VERDICT block so a no-AGENT_BRANCH
run no longer aborts with `HQ: unbound variable` under `set -u`; verdict logic and the
AGENT_BRANCH-present path are unchanged.

# AIV Verification Packet (v2.1): actuate_notify lock is macOS-portable (flock guarded)

**Author:** Miguel Ingram (Author)
**Verifier:** Claude (Verifier)

## Logical unit of work

Single functional change in `bin/actuate_notify.sh`: the dedup/dispatch pass held its concurrency
lock with a bare `flock 9`. `flock(1)` is Linux-only and ABSENT on macOS (the operator host), so
every 60s poll logged `bin/actuate_notify.sh: line 53: flock: command not found`. Guard it:
`if command -v flock >/dev/null 2>&1; then flock 9; fi`. On Linux the lock is unchanged; on macOS it
is skipped, which is safe because the `--loop` poller runs one pass at a time, sequentially (no
concurrent poller to race). Paired atomic commit: this packet + `bin/actuate_notify.sh`.

## Classification

```yaml
classification:
  risk_tier: R2
  sod_mode: S0
  critical_surfaces: []
  blast_radius: operator-notify-daemon
  classification_rationale: >
    actuate_notify.sh is an operator-side alert daemon (ntfy push on new actuation requests); it is
    NOT in the agent's iteration/gate path, touches no money, facts lane, credential, signature, or
    SoD boundary. The change only conditions an advisory lock on flock's presence. The dedup itself
    (grep over the SEEN file) is unchanged, so alerting/dedup behavior is identical; only the
    macOS log-noise and the (unused, single-instance) lock differ. R2 not R1 because it changes a
    daemon's control flow; not R3 (no fabrication/payment surface).
  classified_by: Miguel Ingram (Author) + Claude (Verifier)
  classified_at: 2026-07-24T08:50:00Z
```

## Claim(s)

1. **CLM-001 - no more flock error on macOS.** With `flock` absent, the pass runs without emitting
   `flock: command not found`; dispatch/dedup proceed normally.

   **Falsifiable by:** the notifier still logging `flock: command not found`, or dispatching 0 where
   a genuine new URGENT (or ACTUATE_NOTIFY_ALL) alert exists.

2. **CLM-002 - Linux behavior preserved.** Where `flock` exists, the exclusive fd-9 lock is still
   taken across the read/dedup/append pass.

   **Falsifiable by:** `flock` present but the lock no longer acquired.

## Evidence

### Class A (Execution)

- `command -v flock` on the operator mac -> ABSENT (root cause confirmed); notifier log before the
  fix showed the recurring `line 53: flock: command not found` alongside `dispatched 0 new alert(s)`.
- After the fix: `shellcheck bin/actuate_notify.sh` -> clean; `bash -n` -> ok; the guard evaluates
  false on this host and skips `flock 9` with no error.
- Functional dedup is untouched: alerts are still gated by `grep -qxF "$key" "$SEEN"` and the
  `URGENT || ACTUATE_NOTIFY_ALL` condition, unchanged.

### Class B (Referential)

- Only line changed: `flock 9` -> `if command -v flock >/dev/null 2>&1; then flock 9; fi`, inside
  the same `( ... ) 9>"${SEEN}.lock"` subshell. fd 9 still redirects to the lockfile, so the lock
  remains fd-based (auto-released on death) -- deliberately NOT a mkdir mutex, which would add a
  stale-lock wedge for a single-instance daemon.

### Class C (Negative)

- No money/facts/credential/signature/SoD surface touched; this daemon is operator-side and outside
  the agent's gate path. Dedup/dispatch predicate unchanged. On Linux the lock is byte-for-byte the
  same behavior.

### Class D (Differential)

- Before: bare `flock 9` -> macOS logs `command not found` every poll; lock is a silent no-op there.
- After: lock taken iff `flock` exists; macOS runs cleanly with no error, protected by the
  single-sequential-poller invariant.

### Class E (Intent Alignment)

Authorized by the watchdog mandate to fix harness/portability defects the run exposes (same class as
the bash-3.2 pattern-substitution landmines already fixed). The notifier is the operator's alert
path for the agent's capability requests; a clean, non-erroring poll keeps that path legible.

### Class F (Provenance)

- Change source is the staged `bin/actuate_notify.sh` diff. Reproduce with
  `git diff --cached -- bin/actuate_notify.sh`.

## Cost

- Spent this iteration: `nothing` -- an offline daemon-portability edit.
- Cumulative spent (from `truth.json`, not from memory): `zero` of the cap.

## Honest limitations

- On a host lacking `flock`, two DELIBERATELY concurrent notifier instances could double-send (the
  fd lock is skipped). This is unchanged from the pre-fix macOS reality (flock errored there anyway)
  and out of scope for the single-instance operator daemon; a portable atomic lock was rejected
  because its stale-lock failure mode is worse for a single-instance poller.
- Class G omitted: no pre-implementation prediction recorded.

## Verification methodology

```bash
command -v flock || echo absent          # macOS: absent (root cause)
shellcheck bin/actuate_notify.sh         # clean
bash -n bin/actuate_notify.sh            # ok
# restart the daemon; confirm no 'flock: command not found' in the log, alerts still dispatch
```

## Summary

R2/S0 portability fix: the notifier's concurrency lock is now guarded by `command -v flock`, so the
macOS operator host stops logging `flock: command not found` every poll while Linux keeps the
exclusive lock -- dedup/dispatch behavior identical, no stale-lock risk introduced.

# AIV Verification Packet (v2.1): portable sim workdir path (TMPDIR trailing slash)

**Author:** Miguel Ingram (Author)
**Verifier:** Claude (Verifier)

## Logical unit of work

This packet covers the single functional test-harness change in `tests/sim.sh`: strip a trailing
slash from `$TMPDIR` before it is used to build the simulation workdir `$W`, so `$W` never carries
a `//`. The paired atomic commit contains only this packet and `tests/sim.sh`.

## Classification

```yaml
classification:
  risk_tier: R1
  sod_mode: S0
  critical_surfaces: []
  blast_radius: local
  classification_rationale: >
    Per AIV §5, this is isolated test-harness path handling with a bounded blast radius. It does
    not modify payment behavior, credentials, facts-lane integrity, or any runtime policy; it only
    normalizes the temporary workdir path the offline simulation matrix builds for itself. R2 is
    not warranted because no public API, schema, production configuration, or cross-service
    behavior changes. Production STATE_DIR derivation in bin/pnl.py is untouched and was already
    correct; the defect was confined to a test string-equality assertion.
  classified_by: Miguel Ingram (Author) + Claude (Verifier)
  classified_at: 2026-07-23T00:00:00Z
```

## Claim(s)

1. **CLM-001 — the shadow STATE_DIR assertions pass on macOS.** With `$TMPDIR`'s trailing slash
   stripped, `$W` matches the path `pnl.STATE_DIR` reports, so the two S12 shadow-state assertions
   (`shadow: STATE_DIR default swaps under SHADOW=1`, `shadow: explicit MONEY_AGENT_STATE beats the
   shadow default`) pass instead of false-failing.

   **Falsifiable by:** `bash tests/sim.sh` reporting either shadow STATE_DIR assertion as FAIL on a
   host whose `$TMPDIR` ends in `/` (e.g. macOS).

2. **CLM-002 — no unrelated harness behavior changes.** The change is limited to normalizing `$W`;
   every other assertion in the two-lane matrix is unchanged and the full suite is green.

   **Falsifiable by:** a previously passing assertion failing after the change, or the diff touching
   anything beyond the `$W` derivation at `tests/sim.sh` line ~21.

## Evidence

### Class A (Execution)

- `bash tests/sim.sh` on macOS with Python 3, **before** this change: `PASS=178 FAIL=2 SKIP=0` —
  the two failures were `shadow: STATE_DIR default is …` and `shadow: explicit override lost (…)`.
- `bash tests/sim.sh` on macOS with Python 3, **after** this change: `PASS=180 FAIL=0 SKIP=0`.
- Root-cause reproduction (why the two assertions false-failed):
  ```
  TMPDIR = '/var/folders/.../T/'            (trailing slash — macOS)
  W      = '/var/folders/.../T//money-sim.5T2PGJ'   (bash keeps the //)
  pnl.STATE_DIR (HOME=$W/home, SHADOW=1) = '/var/folders/.../T/money-sim.5T2PGJ/home/.money-agent-shadow'
                                            (pathlib collapsed the //)
  => bash "$W/home/.money-agent-shadow" (//)  !=  pnl.STATE_DIR (/)  => FAIL
  ```
  On Linux CI, `$TMPDIR` is unset → `/tmp` (no trailing slash) → no `//` → the assertions already
  passed, which is why remote CI was green while the macOS operator preflight was red.

### Class B (Referential)

- CLM-001: `tests/sim.sh` — the `$W` derivation strips the trailing slash
  (`TMPROOT="${TMPDIR:-/tmp}"; TMPROOT="${TMPROOT%/}"; W="$(mktemp -d "${TMPROOT}/money-sim.XXXXXX")"`);
  the assertions it fixes are at the lines printing `shadow: STATE_DIR default …` and
  `shadow: explicit override lost …`.
- CLM-002: `git diff --cached -- tests/sim.sh` is the full functional diff and touches only the
  `$W` derivation plus its explanatory comment.

### Class C (Negative)

- No production code changed: `bin/pnl.py` `STATE_DIR` (`HOME/.money-agent-shadow` under `SHADOW=1`)
  is byte-for-byte unchanged and was already correct — a direct repro with a slash-free `$W`
  returned `equal? YES` before any edit, proving the defect lived only in the test's `$W` string.
- No money, credential, ledger, or gate behavior is touched. The change cannot make a failing gate
  pass: it only removes a false FAIL from a string comparison; every negative assertion the matrix
  makes about the gates is unchanged.

### Class D (Differential)

- Matrix result: `FAIL=2` → `FAIL=0` (`PASS 178 → 180`, `SKIP` unchanged at 0).
- `$W` string form: `…/T//money-sim.XXXX` → `…/T/money-sim.XXXX` (one redundant slash removed);
  no other path in the harness changes shape.

### Class E (Intent Alignment)

The immutable intent is the operator request to make the run-2 operator preflight trustworthy on
this macOS operator machine: the run-2 operator runbook's Section 0 / D7 sign-off requires
`bash tests/sim.sh` to report `FAIL=0` on the commit being deployed, and a spurious macOS FAIL
undermines the "FAIL=0 is the only value that matters" gate. Normalizing a self-built temp path so
the committed verification matrix runs identically on macOS and Linux stays squarely inside the
test's own stated contract (it already declares Python 3 as a required runtime).

### Class F (Provenance)

- The change source is the staged `tests/sim.sh` diff, limited to the `$W` derivation and its
  comment. Reproduce with `git diff --cached -- tests/sim.sh` before committing.
- The before/after counts (`178/2` → `180/0`) are from full local runs of the committed matrix on
  the operator machine; Ubuntu CI is the independent remote confirmation of the same matrix.

## Cost

- Spent this iteration: `nothing` — an offline, keyless test-harness edit.
- Cumulative spent (from `truth.json`, not from memory): `zero` of the cap.

## Honest limitations

- This verifies the macOS `$TMPDIR`-with-trailing-slash failure mode and the slash-stripping fix on
  this operator machine; Ubuntu CI remains the remote confirmation of the same matrix.
- The fix normalizes only the trailing slash. A `$TMPDIR` containing an interior `//` or other
  non-canonical form is not handled, because none is known to occur; the assertion would surface it
  as a FAIL rather than passing silently.
- Class G is omitted: no pre-implementation prediction was recorded.

## Verification methodology

```bash
bash tests/sim.sh          # expect PASS=180 FAIL=0 SKIP=0 on macOS (was 178/2)
shellcheck tests/sim.sh
git diff --check
```

## Summary

This R1/S0 test-only change strips the trailing slash macOS sets on `$TMPDIR` before building the
simulation workdir `$W`, so bash `$W` paths and Python `pathlib`-normalized `STATE_DIR` paths
compare equal. The macOS simulation matrix now reports `FAIL=0`, matching Linux CI, without any
change to production code.

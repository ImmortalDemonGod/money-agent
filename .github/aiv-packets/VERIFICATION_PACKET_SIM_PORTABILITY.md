# AIV Verification Packet (v2.1): portable simulation fixture mutation

**Author:** Miguel Ingram (Author)  
**Verifier:** Codex (Verifier)

## Logical unit of work

This packet covers the single functional test-harness change in `tests/sim.sh`:
replace platform-specific in-place `sed` fixture edits with a literal, exact-once Python
mutation helper. The paired atomic commit contains only this packet and `tests/sim.sh`.

## Classification

```yaml
classification:
  risk_tier: R1
  sod_mode: S0
  critical_surfaces: []
  blast_radius: local
  classification_rationale: >
    Per AIV §5, this is isolated test-fixture logic with a bounded blast radius. It does
    not modify payment behavior, credentials, facts-lane integrity, or runtime policy;
    it makes existing negative gate tests portable and fail-closed. R2 is not warranted
    because no public API, schema, production configuration, or cross-service behavior changes.
  classified_by: Miguel Ingram (Author) + Codex (Verifier)
  classified_at: 2026-07-22T20:01:15Z
```

## Claim(s)

1. **CLM-001 — portable, exact-once fixture mutation.** The AIV-gate negative tests mutate their
   generated packet consistently on BSD/macOS and GNU/Linux, and abort if the intended literal
   fixture text is absent or duplicated.

   **Falsifiable by:** `bash tests/sim.sh` reporting a failed `$999`-overclaim or contradictory-edge
   test because its fixture was not mutated, or `replace_once` accepting zero/multiple matches.

2. **CLM-002 — no unrelated harness behavior changes.** The full two-lane matrix continues to
   pass; the correction only replaces the three mutation operations used between the already-existing
   AIV-gate assertions.

   **Falsifiable by:** a previously passing simulation assertion failing after the change, or the
   diff containing behavior beyond `replace_once` and its three callers.

## Evidence

### Class A (Execution)

- `bash tests/sim.sh` on macOS with Python 3: **22 PASS, 0 FAIL, 0 SKIP**. This includes the
  honest packet pass and all three negative gate checks: `$999` overclaim, contradictory
  `EDGE_CLAIM`, and missing `EDGE_CLAIM`.
- `shellcheck tests/sim.sh`: exit 0.
- `git diff --check`: exit 0.

Baseline isolation: with this change stashed, the same macOS run produced **20 PASS, 2 FAIL**.
Both failures were the intended negative tests; BSD `sed` rejected the GNU `-i` form and left the
fixture unchanged. The restored change produced the 22/0 result above.

### Class B (Referential)

- CLM-001: `tests/sim.sh` lines 52-68 define `replace_once`; lines 245-252 use it for each
  previously GNU-specific mutation.
- CLM-002: the same `tests/sim.sh` range is the full functional diff; the assertions at lines
  247 and 253 remain unchanged.

### Class E (Intent Alignment)

The immutable intent is the operator request in this Codex task to fix the macOS portability
failure observed in `tests/sim.sh`. The test itself declares Python 3 as a required runtime and
is the repository's committed verification matrix, so using Python for deterministic fixture
edits stays inside its stated execution contract.

### Class F (Provenance)

**Claim 2:** The change source is the staged `tests/sim.sh` diff, limited to the `replace_once`
helper and its three callers. Reproduce with `git diff --cached -- tests/sim.sh` before committing.

**Justification:** the test changes are required to execute the existing negative assertions on
both supported `sed` families and preserve the original assertion inputs and expected exit codes.

- The preserved behavior is evidenced by the named assertions in `tests/sim.sh` and the complete
  local matrix transcript: 22 PASS, 0 FAIL, 0 SKIP after the change; 20 PASS, 2 FAIL when the
  change was stashed on the same checkout.

## Honest limitations

- This verifies the local macOS failure mode and the portable Python replacement; Ubuntu CI remains
  the remote confirmation of the same matrix.
- The helper is intentionally literal rather than regex-based. Future fixture wording changes must
  update its callers, at which point the exact-once check will fail rather than silently testing
  stale content.
- Class G is omitted: no pre-implementation prediction was recorded.

## Verification methodology

```bash
bash tests/sim.sh
shellcheck tests/sim.sh
git diff --check
```

## Summary

This R1/S0 test-only change replaces non-portable `sed -i` calls with a deterministic Python helper
that demands exactly one fixture match. The macOS simulation matrix now executes its negative
AIV-gate cases rather than falsely passing them against unchanged fixtures.

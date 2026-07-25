# AIV Verification Packet (v2.1): aiv_gate.sh manifest-non-empty check false-fails past 64 KB (SIGPIPE)

**Author:** Miguel Ingram (Author)
**Verifier:** Claude (Verifier)

## Logical unit of work

Fix a run-blocking bug in `bin/aiv_gate.sh:94`. The manifest-non-empty check was
`printf '%s' "$MANIFEST_TXT" | grep -q '[^[:space:]]'`. `grep -q` exits at the first match and
closes the pipe; once `MANIFEST_TXT` exceeds the ~64 KB pipe buffer, `printf`'s remaining write is
SIGPIPE'd (exit 141); under the script's `set -uo pipefail` the pipeline returns 141; the leading
`!` flips that to true and the gate FALSELY fires "money claim present but no grounded
MANIFEST.sha256". Replace the pipe with a herestring (`grep -q '[^[:space:]]' <<< "$MANIFEST_TXT"`),
which has no upstream writer to kill and is correct at any size.

The ledger manifest just crossed the threshold: it is **67,479 bytes / 630 lines** on
`origin/ledger-run2` and grows every verifier cycle. Because `iter.py new` pre-fills `received_usd`
into every packet's ledger anchor, EVERY iteration now trips the money-claim branch that runs this
check, so **no iteration can close** — a full-run halt. (iters 085/086 closed earlier, before the
manifest crossed 64 KB; iter 087 is the first blocked.) This is the harness/operator boundary
(`aiv_gate.sh` is in the sod_hook blocklist), so the agent correctly cannot patch it — it is fixed
here. Paired atomic commit: this packet + `bin/aiv_gate.sh`.

## Classification

```yaml
classification:
  risk_tier: R2
  sod_mode: S0
  critical_surfaces: [close_gate]
  blast_radius: iteration-close
  classification_rationale: >
    One-line change to a gate script: swaps a `printf | grep -q` pipe for a `grep -q <<<` herestring
    in the manifest-non-empty test. No verification LOGIC changes -- the same predicate ("does the
    manifest contain a non-whitespace char") is evaluated, just without the SIGPIPE/pipefail hazard.
    The empty-manifest guard is preserved (whitespace-only and truly-empty both still detected as
    empty). No money/facts/signing/anchor-matching logic touched. Strictly un-breaks; strengthens
    nothing else and weakens nothing.
  classified_by: Miguel Ingram (Author) + Claude (Verifier)
  classified_at: 2026-07-25T02:00:00Z
```

## Claim(s)

1. **CLM-001 - the bug reproduces deterministically at the live manifest size.** The original
   pipeline, run against the real 67,479-byte manifest, returns exit 141 (SIGPIPE) and thus
   false-fails, every time.

   **Falsifiable by:** the original `printf ... | grep -q` returning 0 against the real manifest.

2. **CLM-002 - the herestring fix detects the real manifest as non-empty (no false-fail).** The
   fixed line returns 0 against the same manifest, every time.

   **Falsifiable by:** the fixed line false-failing on the real (non-empty) manifest.

3. **CLM-003 - the empty guard is preserved.** A whitespace-only or truly-empty manifest is still
   detected as empty (the gate still fails an actually-empty manifest).

   **Falsifiable by:** a whitespace-only/empty manifest being treated as non-empty.

## Evidence

### Class A (Execution)

- `git show origin/ledger-run2:ledger/raw/MANIFEST.sha256 | wc -c` -> **67479** (630 lines).
- Original pipeline vs real manifest, 40 runs: **40/40 false-fail**; direct pipeline exit printed
  **141** (SIGPIPE) five times running. (CLM-001)
- Fixed herestring vs real manifest, 40 runs: **0/40 false-fail, 40/40 correct** (non-empty
  detected). (CLM-002)
- Fixed herestring vs whitespace-only and vs empty string: both **correctly detected EMPTY**.
  (CLM-003)
- `bash -n bin/aiv_gate.sh` -> syntax ok.

### Class B (Referential)

- Only line 94 changed: `printf '%s' "$MANIFEST_TXT" | grep -q '[^[:space:]]'` ->
  `grep -q '[^[:space:]]' <<< "$MANIFEST_TXT"`. The `then`/`else` bodies (the fail message and the
  anchor-hash loop) are unchanged. The change matches the existing `<<< "$MANIFEST_TXT"` idiom
  already used on line 98 for the anchor loop.

### Class C (Negative)

- No money/facts/signing/anchor-matching/dollar-parsing logic touched. The predicate is identical
  ("manifest has a non-whitespace char"); only the plumbing that feeds grep changed. The
  `${VAR//[[:space:]]/}` bash-3.2 slowness the original comment warns against is still avoided (a
  herestring is O(n), not the pattern-substitution).

### Class D (Differential)

- Before: manifest >= 64 KB -> SIGPIPE -> pipeline 141 -> `!` true -> false "empty manifest" fail ->
  no iteration closes.
- After: herestring -> grep sees the full input, exits 0 for non-empty / 1 for empty -> gate passes a
  real manifest and still fails an empty one.

### Class E (Intent Alignment)

The check's intent is "refuse a money-claim packet whose manifest is missing/empty." The SIGPIPE bug
made it refuse NON-empty manifests too, once large enough -- inverting the guard into a blanket
close-block. The fix restores exactly the intended predicate.

### Class F (Provenance)

- `git diff --cached -- bin/aiv_gate.sh`.

## Cost

- Spent: `nothing` -- offline one-line edit + isolated reproduction/validation against the committed
  manifest. No network, money, or facts write.
- Cumulative (truth.json): `zero`.

## Honest limitations

- End-to-end: the full `aiv_gate.sh <NNN>` was validated against a real already-closed packet (iter
  086) after propagation; the currently-open iter 087 still legitimately fails on its `<fill>`
  placeholders (unrelated), so it is not used as the pass witness.
- The threshold is buffer-dependent (~64 KB on this platform); the fix removes the size dependence
  entirely rather than tuning the threshold.

## Verification methodology

```bash
git show origin/ledger-run2:ledger/raw/MANIFEST.sha256 | wc -c   # 67479
M=$(git show origin/ledger-run2:ledger/raw/MANIFEST.sha256)
# original: printf '%s' "$M" | grep -q '[^[:space:]]'   -> exit 141 (false-fail)
# fixed:    grep -q '[^[:space:]]' <<< "$M"              -> exit 0   (correct)
bash -n bin/aiv_gate.sh
```

## Summary

R2/S0 close-gate fix: `aiv_gate.sh`'s manifest-non-empty check used `printf | grep -q`, which SIGPIPEs
`printf` once the manifest passes the ~64 KB pipe buffer; under `pipefail` + `!` that became a false
"empty manifest" failure that blocked EVERY iteration close (the manifest just hit 67 KB and every
packet pre-fills `received_usd`). Swapping the pipe for a herestring restores the intended predicate
at any manifest size; the empty-manifest guard is preserved. Reproduced 40/40 and fixed 40/40 against
the live manifest.

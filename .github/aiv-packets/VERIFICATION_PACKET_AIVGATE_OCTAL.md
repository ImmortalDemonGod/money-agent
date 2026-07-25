# AIV Verification Packet (v2.1): aiv_gate.sh octal-parses zero-padded iteration numbers (bash 3.2)

**Author:** Miguel Ingram (Author)
**Verifier:** Claude (Verifier)

## Logical unit of work

Harden `bin/aiv_gate.sh:22` against octal misparse of the iteration argument. `iter.py::close()`
always passes a zero-padded number (`nnn = f"{int(nnn):03d}"` -> e.g. `"087"`). The gate then ran
`N=$(printf '%03d' "$ITER")`; under **bash 3.2 (the macOS default shell)** `printf '%03d' 087` reads
the leading zero as OCTAL and aborts (`087: invalid number`), so `N` becomes `"000"`, the packet path
resolves to the non-existent `VERIFICATION_PACKET_ITER_000.md`, and the gate FAILS for every `08x`,
`09x`, `x8`, or `x9` iteration. Fix: coerce to base-10 before padding -- `printf '%03d' "$((10#$ITER))"`
-- which is correct for any input form (padded or bare) under any bash. Paired atomic commit: this
packet + `bin/aiv_gate.sh`.

Scope note (honest): this is DEFENSIVE hardening, not the confirmed live blocker. The confirmed halt
was the SIGPIPE manifest false-fail (fixed separately, VERIFICATION_PACKET_AIVGATE_SIGPIPE.md); the
agent's reported error was that line-95 manifest message, which proves its close reaches line 95 --
i.e. line 22 does NOT octal-fail in the agent's runtime (and iters 085/086, both containing an `8`,
did close). The octal fault is reproducible under /bin/bash 3.2 (this host's only bash) but the
agent's environment dodges it. It is fixed here because a sod-boundary gate that chokes on its own
iteration numbers under the platform's default shell is one bash-version drift from silently blocking
every 8/9 close, and the agent cannot patch a gate itself.

## Classification

```yaml
classification:
  risk_tier: R2
  sod_mode: S0
  critical_surfaces: [close_gate]
  blast_radius: iteration-close
  classification_rationale: >
    One-line change to a gate's argument normalization: `printf '%03d' "$ITER"` ->
    `printf '%03d' "$((10#$ITER))"`. Same predicate, same packet resolution; only the number is
    parsed base-10 instead of shell-default (octal on leading zero). No verification logic, money,
    facts, signing, or manifest handling touched. Non-numeric input still errors exactly as before.
  classified_by: Miguel Ingram (Author) + Claude (Verifier)
  classified_at: 2026-07-25T02:20:00Z
```

## Claim(s)

1. **CLM-001 - the bug reproduces under bash 3.2 with the arg iter.py passes.** `bash aiv_gate.sh 087`
   (and 085/086) octal-fails at line 22 (`invalid number`), yielding `ITER_000` and RESULT: FAIL.

   **Falsifiable by:** the original line parsing `087` to `087` under /bin/bash 3.2.

2. **CLM-002 - the fix parses every form correctly.** `printf '%03d' "$((10#$ITER))"` yields the
   correct zero-padded value for `86/086/87/087/88/088/8/08` under bash 3.2.

   **Falsifiable by:** any of those inputs producing the wrong `N`.

3. **CLM-003 - the full close path passes end-to-end with the padded arg.** Reproducing iter.py's
   exact call (`subprocess.run(['bash','bin/aiv_gate.sh','085'])`) against the real packet returns
   rc=0 / RESULT: PASS after the fix (was rc=1 octal-fail before).

   **Falsifiable by:** a padded-arg close still octal-failing after the fix.

## Evidence

### Class A (Execution)

- Before (bash 3.2): `printf '%03d' 087` -> `087: invalid number` + `000`; `085`, `086`, `088` same.
- iter.py-exact subprocess call, padded `085/086/087` against the committed gate: all rc=1,
  `invalid number`, `no packet ITER_000`. (CLM-001)
- After: `printf '%03d' "$((10#$a))"` for `a in 86 086 87 087 88 088 08 8` -> `086 086 087 087 088
  088 008 008` (all correct). (CLM-002)
- After, iter.py-exact call for `085`/`086` against the real packets: **rc=0, octal_fail=False,
  RESULT: PASS**. (CLM-003)
- `bash -n bin/aiv_gate.sh` -> ok. The coexisting SIGPIPE fix still detects a whitespace-only
  manifest as empty (guard intact).

### Class B (Referential)

- Only line 22 changed: `printf '%03d' "$ITER"` -> `printf '%03d' "$((10#$ITER))"`. The `${1:?}`
  usage guard on line 21 and every downstream `$N`/`$PACKET` use are unchanged.

### Class C (Negative)

- No money/facts/signing/manifest/anchor logic touched. Base-10 coercion changes only the radix used
  to read the iteration index; non-numeric input still errors (as before), so no new silent-pass path.

### Class D (Differential)

- Before: `iter.py close 87` -> gate gets `087` -> (bash 3.2) octal abort -> ITER_000 -> FAIL.
- After: `087` -> `10#087` = 87 -> `087` -> correct packet -> gate adjudicates on its real merits.

### Class E (Intent Alignment)

The gate's arg is an iteration index; it must not depend on whether the caller zero-pads it or on the
shell's leading-zero radix. The fix makes the index parse unambiguous.

### Class F (Provenance)

- `git diff --cached -- bin/aiv_gate.sh`.

## Cost

- Spent: `nothing` -- offline one-line edit + isolated + end-to-end reproduction against committed
  packets. No network, money, or facts write.
- Cumulative (truth.json): `zero`.

## Honest limitations

- Defensive: the agent's current runtime does not exhibit the octal fault (its close reaches line 95),
  so this does not, by itself, unblock anything the SIGPIPE fix did not. It removes the fault under
  bash 3.2 so a shell change cannot reintroduce a silent close-block.
- End-to-end PASS witnesses are the already-closed 085/086 packets; open iter 087 still legitimately
  fails on its `<fill>` placeholders (unrelated).

## Verification methodology

```bash
# before (bash 3.2): printf '%03d' 087  -> "087: invalid number" / 000
# after:             printf '%03d' "$((10#087))" -> 087
python3 -c "import subprocess;print(subprocess.run(['bash','bin/aiv_gate.sh','085'],capture_output=True,text=True).returncode)"  # 0
bash -n bin/aiv_gate.sh
```

## Summary

R2/S0 close-gate hardening: `aiv_gate.sh` octal-misparsed the zero-padded iteration number
`iter.py` hands it (bash 3.2, macOS default), failing every 8/9 iteration to `ITER_000`. Base-10
coercion (`$((10#$ITER))`) fixes it for any arg form under any shell; the padded-arg close now passes
end-to-end (rc=0). Defensive relative to the separately-fixed SIGPIPE halt, but closes a real footgun
in the sod-boundary gate the agent cannot patch itself.

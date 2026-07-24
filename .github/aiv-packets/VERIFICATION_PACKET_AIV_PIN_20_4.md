# AIV Verification Packet (v2.1): pin aiv (#30/#31) + retire the two downstream workarounds

**Author:** Miguel Ingram (Author)
**Verifier:** Claude (Verifier)

## Logical unit of work

Pre-run gate #20-4. Upstream `aiv-protocol#30` (E010 section-level false positive + init pins the
owning interpreter) and `#31` (the #29 lifecycle bugs) are merged. This commit pins the sandbox's
aiv install to that build and removes the two now-obsolete downstream workarounds — the hook-shebang
`sed -i.bak` repair in `bin/setup_sandbox.sh` and the E010 trap note in
`.github/aiv-packets/TEMPLATE.md` — in one atomic unit with this packet.

## Classification

```yaml
classification:
  risk_tier: R2
  sod_mode: S0
  critical_surfaces: []
  blast_radius: sandbox-setup
  classification_rationale: >
    Per AIV §5, this changes how a fresh sandbox provisions its git hooks (toolchain pin +
    removal of a redundant shebang repair) and edits the packet template. It does not touch
    payments, the facts lane, credentials, or runtime policy. R2 (not R1) because setup_sandbox.sh
    installs the SoD pre-commit tripwire, so a regression could leave a clone unguarded — which is
    why the evidence below includes a fresh-clone install test proving the SoD hook still lands and
    the aiv hook still runs.
  classified_by: Miguel Ingram (Author) + Claude (Verifier)
  classified_at: 2026-07-23T00:00:00Z
```

## Claim(s)

1. **CLM-001 — aiv is pinned to the #30/#31 build.** `bin/setup_sandbox.sh` installs
   `aiv-protocol@474899f9d380759c668e4bd3bf71baa884ce1c22` (carries #30 + #31), replacing the
   unpinned `git+...aiv-protocol.git`.

   **Falsifiable by:** `grep -c 474899f bin/setup_sandbox.sh` == 0, or the install line still
   floating on an unpinned ref.

2. **CLM-002 — the shebang `sed`-repair is gone and unnecessary.** The `sed -i.bak` loop is removed
   from `setup_sandbox.sh`; a fresh clone's `aiv init` now writes the hook shebang at the owning
   interpreter by itself (the #30 fix). The `AIV_PY` interpreter check is retained as a safety belt.

   **Falsifiable by:** `grep -c 'sed -i.bak' bin/setup_sandbox.sh` != 0, or a fresh-clone
   `aiv-pre-commit.orig` shebang resolving to `/usr/bin/env python3` / crashing with
   ModuleNotFoundError.

3. **CLM-003 — the TEMPLATE.md E010 note is removed and E010 no longer false-trips.** The
   "writing issue #N trips E010" trap note is deleted from Class E; the pinned aiv reports 0
   blocking errors on `issue #N` in both Class E and Class F.

   **Falsifiable by:** `grep -c E010 .github/aiv-packets/TEMPLATE.md` != 0, or `aiv check` raising
   a blocking E010 error on an `issue #N` Class E/F line.

## Evidence

### Class A (Execution)

- **Fresh-clone install test** (edited `setup_sandbox.sh` run in a throwaway `git clone`):
  ```
  ✓ aiv init ran (hooks are not cloned; config alone is not enough)
  ✓ aiv hook runs (no ModuleNotFoundError)
  ✓ installed .git/hooks/pre-commit -> sod_hook.sh (chains to aiv if present)
  aiv-pre-commit.orig shebang: #!/opt/homebrew/opt/python@3.11/bin/python3.11   (owning interpreter — #30)
  pre-push shebang:            #!/opt/homebrew/opt/python@3.11/bin/python3.11
  aiv-pre-commit.orig imports aiv? runs (no ModuleNotFoundError)
  leftover .bak files: 0
  ```
- **E010 no longer fires:** `aiv check` on a packet with `issue #42`/`issue #30` in Class F → `0
  blocking error(s), 1 warning(s)`; same with `issue #20`/`issue #45` in Class E → `0 blocking
  error(s)`. (The 1 warning is an unrelated permalink-immutability note.)
- **Matrix green under the pinned aiv:** `bash tests/sim.sh` → `PASS=180 FAIL=0 SKIP=0` (aiv_gate
  stages ran, not skipped).
- `shellcheck bin/setup_sandbox.sh` → exit 0.
- Grep acceptance: `grep -c E010 .github/aiv-packets/TEMPLATE.md` → 0; `grep -c 'sed -i.bak'
  bin/setup_sandbox.sh` → 0.

### Class B (Referential)

- CLM-001: `bin/setup_sandbox.sh` — the `AIV_PIN=474899f…` variable and the three
  `git+…aiv-protocol.git@${AIV_PIN}` install/fallback lines.
- CLM-002: `bin/setup_sandbox.sh` — the removed `for h in pre-commit pre-push; do … sed -i.bak …`
  loop; the retained `AIV_PY` gate and the `"$AIV_PY" .git/hooks/aiv-pre-commit.orig` verification;
  the updated section comment.
- CLM-003: `.github/aiv-packets/TEMPLATE.md` Class E — the deleted "Canonical-validator trap …
  E010 …" sentence.

### Class C (Negative)

- **No SoD regression:** the fresh-clone test shows `.git/hooks/pre-commit -> sod_hook.sh` still
  installs and the aiv hook still runs — removing the shebang repair did not leave a clone
  unguarded. The `AIV_PY` interpreter check is kept, so the verification step is unchanged.
- **No matrix regression:** `sim.sh` is `180/0` before and after the aiv upgrade.
- No facts-lane, payment, or credential surface is touched.

### Class D (Differential)

- Installed aiv: `1.0.0` (pkg dated 2026-03-17, pre-fix) → `1.0.0 @ 474899f` (pkg dated
  2026-07-23, carries #30+#31). setup pin: unpinned → `@474899f…`.
- Workaround greps: `sed -i.bak` 1 → 0; `E010` in TEMPLATE.md 1 → 0.
- Fresh-clone hook shebang: previously `#!/usr/bin/env python3` (needing repair) → now
  `#!/opt/homebrew/opt/python@3.11/bin/python3.11` at init.

### Class E (Intent Alignment)

Authorized by the operator's run-2 setup request to close the pre-run acceptance gate covering the
aiv upstream merge and downstream-workaround removal: the runbook's Section-4 gate says to merge the
upstream fix, pin the installed aiv version where setup installs it, and delete both downstream
workarounds in the same commit, with the matrix green afterward. (Ticket numbers are now safe to
write here — CLM-003's evidence shows the pinned aiv no longer false-trips E010.)

### Class F (Provenance)

- Pin: `aiv-protocol@474899f9d380759c668e4bd3bf71baa884ce1c22` (main tip, 2026-07-23T06:55Z),
  which merged `#30` (merge commit `958b2ba1e129123ddf73053b2165132d52572ac5`) and `#31`.
- Local install fingerprint after upgrade: `aiv-protocol 1.0.0`, package mtime 2026-07-23, at
  `/opt/homebrew/lib/python3.11/site-packages`.

## Cost

- Spent this iteration: `nothing` — a toolchain pin + two doc/script edits, all offline.
- Cumulative spent (from `truth.json`, not from memory): `zero` of the cap.

## Honest limitations

- The fresh-clone test was run on this macOS operator machine with homebrew Python 3.11; a clone on
  a host with a different owning interpreter would write that interpreter's path — which is exactly
  the #30 behavior, but is verified here only for this machine.
- The local aiv was upgraded in place (backed up first for rollback). The committed pin governs
  *fresh* clones; existing machines must re-run the pinned install to match.
- Class G omitted: no pre-implementation prediction was recorded.

## Verification methodology

```bash
grep -c E010 .github/aiv-packets/TEMPLATE.md          # 0
grep -c 'sed -i.bak' bin/setup_sandbox.sh             # 0
shellcheck bin/setup_sandbox.sh                        # exit 0
bash tests/sim.sh                                      # PASS=180 FAIL=0 SKIP=0
# fresh clone -> run edited setup_sandbox.sh -> assert aiv-pre-commit.orig shebang is the owning
# interpreter, the aiv hook runs, the SoD hook installs, and no .bak files remain.
```

## Summary

Closes pre-run gate #20-4: pins the sandbox aiv install to the merged `#30`/`#31` build and removes
the two workarounds that fix made obsolete (the `sed -i.bak` shebang repair and the TEMPLATE E010
trap note), proven safe by a fresh-clone install test showing init writes the correct owning-
interpreter shebang, the SoD hook still lands, and the matrix stays `180/0`.

# AIV Verification Packet (v2.1): actuation fulfill rebases onto the current facts tip on contention

**Author:** Miguel Ingram (Author)
**Verifier:** Claude (Verifier)

## Logical unit of work

Single functional change in `bin/actuate.py`: the operator-fulfill publish did a PLAIN
`git push origin HEAD:<ledger_branch>`. The facts lane is shared with the running verifier (it
pushes `truth.json` every cycle), so that push is non-fast-forward under normal contention and the
fulfill fails ("could not publish resolution"). The fix: on a non-ff push, fetch + rebase the single
resolution commit onto the current tip (our `actuation_resolutions.json` never conflicts with the
verifier's `truth.json`) and push again. Paired atomic commit: this packet + `bin/actuate.py`.

## Classification

```yaml
classification:
  risk_tier: R2
  sod_mode: S0
  critical_surfaces: [audit_logs]
  blast_radius: actuation-publish
  classification_rationale: >
    Touches the operator-resolution publish path on the facts lane, but does NOT change the
    resolution content, its signature, the ledger_branch-only requirement, or any grounding /
    verification the agent-side sync performs. It only makes a benign non-fast-forward push
    succeed by rebasing one non-conflicting commit onto the current tip. No money, credential, or
    SoD-boundary logic changes. R2 (facts-lane write path) not R3 (no fabrication surface added).
  classified_by: Miguel Ingram (Author) + Claude (Verifier)
  classified_at: 2026-07-24T00:00:00Z
```

## Claim(s)

1. **CLM-001 - fulfill survives facts-lane contention.** When `origin/<ledger_branch>` advanced
   (verifier pushed) between the resolution commit and the push, the fulfill now fetches, rebases
   its single commit onto the current tip, and pushes -- instead of failing.

   **Falsifiable by:** a fulfill still raising "could not publish resolution" on a plain
   non-fast-forward when the resolution rebases cleanly.

2. **CLM-002 - both writers coexist; content preserved.** After the rebase-and-retry, the lane
   carries BOTH the verifier's `truth.json` commit and the resolution commit, with
   `actuation_resolutions.json` and `truth.json` intact.

   **Falsifiable by:** either file lost/overwritten, or a spurious rebase conflict on
   non-overlapping files.

## Evidence

### Class A (Execution)

- Contention simulation (bare origin + `ledger-run2` + a fulfill clone + a verifier clone), mirroring
  the exact files: fulfill commits `actuation_resolutions.json={"resolutions":["ACT-001"]}` on a
  stale base; the verifier commits `ledger/truth.json` and pushes FIRST; the fulfill's plain push is
  **non-ff as expected**, then `fetch + rebase origin/ledger-run2` -> **rebase clean**, push -> **OK**.
  Final `origin/ledger-run2`: `actuation_resolutions.json = {"resolutions":["ACT-001"]}`,
  `ledger/truth.json = {"received":0}`, **3 commits** (seed + verifier + resolution) -- both writers
  landed, no conflict.
- `python3 -m py_compile bin/actuate.py` -> ok.
- Real-world trigger: fulfilling `ACT-001` (Vercel deploy) failed with the plain push against the
  live, verifier-advanced `ledger-run2`; this is the fix for that failure mode.

### Class B (Referential)

- `bin/actuate.py` fulfill publish: after the initial `push`, the `returncode != 0` branch now does
  `_git("fetch", "-q", "origin", ledger_branch)`, `_git("rebase", f"origin/{ledger_branch}")` (abort
  + raise on a real conflict), then re-pushes. The commit/sign/`ledger_branch`-guard logic above is
  unchanged.

### Class C (Negative)

- Resolution content and signature are produced exactly as before (untouched sign/commit block); the
  change is purely the push-retry. A genuine rebase conflict aborts and raises (fail-closed, no
  half-published state). No money/credential/SoD/`ledger_branch`-requirement change; the agent-side
  `sync` signature + request-hash verification is untouched.

### Class D (Differential)

- Before: fulfill = commit -> single plain push; non-ff (routine verifier contention) -> hard failure.
- After: non-ff -> fetch + rebase onto current tip + push; only a real (conflicting) rebase fails.

### Class E (Intent Alignment)

Authorized by the operator's report that fulfilling `ACT-001` failed, and the setup requirement that
operator resolutions publish from the shared `ledger-run2` facts lane. The verifier writes that lane
continuously; a fulfill that cannot survive that contention makes the entire capability-delegation
channel (PROMPT.md's one legitimate operator ask) unusable during a live run.

### Class F (Provenance)

- Change source is the staged `bin/actuate.py` diff (the fulfill push block). Reproduce with
  `git diff --cached -- bin/actuate.py`.

## Cost

- Spent this iteration: `nothing` -- an offline publish-path edit.
- Cumulative spent (from `truth.json`, not from memory): `zero` of the cap.

## Honest limitations

- Rebase is clean only because the resolution and the verifier touch DISJOINT files. If a future
  change makes the fulfill also write a file the verifier writes, the rebase could conflict (it then
  aborts + raises, fail-closed -- never a silent bad publish).
- Verified via a git simulation of the exact file layout, not against the live daemon (which would
  require timing a real collision); the simulation reproduces the non-ff + rebase path deterministically.
- Class G omitted: no pre-implementation prediction was recorded.

## Verification methodology

```bash
python3 -m py_compile bin/actuate.py
# bare origin + ledger-run2; fulfill commits actuation_resolutions.json on a stale base;
# verifier commits ledger/truth.json and pushes first; fulfill push -> non-ff -> fetch+rebase+push;
# assert both files present and 3 commits on the lane.
```

## Summary

R2/S0 facts-lane publish fix: operator-fulfill now rebases its single resolution commit onto the
current `ledger-run2` tip on a (routine) non-fast-forward from the verifier, instead of failing --
restoring the actuation channel during a live run, with no change to resolution content, signature,
or the lane-only requirement.

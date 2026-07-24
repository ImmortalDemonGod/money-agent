# AIV Verification Packet (v2.1): actuation operator-queue reads an absent file as empty

**Author:** Miguel Ingram (Author)
**Verifier:** Claude (Verifier)

## Logical unit of work

Single functional change in `bin/actuate.py`: `_operator_tasks_all()` treats an absent
`run/actuation_tasks.json` on the agent branch as an EMPTY queue (`[]`) instead of raising, so the
operator fulfill form renders "No open requests" before the agent has queued anything. The paired
atomic commit contains only this packet and `bin/actuate.py`.

## Classification

```yaml
classification:
  risk_tier: R1
  sod_mode: S0
  critical_surfaces: []
  blast_radius: local
  classification_rationale: >
    Per AIV §5, this is a bounded operator-side read-path change: it only softens one benign git
    failure (a missing queue PATH) into an empty list, and leaves every other git error raising. It
    does not touch money, the facts lane, credentials, the request/fulfill/decline/sync flow, the
    signature/SoD boundary, or any policy. R2 is not warranted -- no public API, schema, or
    cross-service behavior changes.
  classified_by: Miguel Ingram (Author) + Claude (Verifier)
  classified_at: 2026-07-24T00:00:00Z
```

## Claim(s)

1. **CLM-001 - an absent queue file reads as empty.** With the fix, `_operator_tasks_all()` returns
   `[]` when `run/actuation_tasks.json` does not exist on `origin/<AGENT_BRANCH>`, so the fulfill
   form shows "No open requests" instead of "cannot read requests".

   **Falsifiable by:** `_operator_tasks_all()` raising against a branch that lacks the file.

2. **CLM-002 - real git errors still raise.** The softening applies ONLY to the "does not exist"
   (missing path) case; a missing branch or any other git failure still raises.

   **Falsifiable by:** the function returning `[]` for a nonexistent branch instead of raising.

## Evidence

### Class A (Execution)

- Missing file, branch present: `AGENT_BRANCH=main python3 -c "... actuate._operator_tasks_all()"`
  -> **returned `[]`** (PASS) -- `main` carries no `run/actuation_tasks.json`.
- Nonexistent branch: `AGENT_BRANCH=no-such-branch-xyz ...` -> **raised `CalledProcessError`**
  (the `fetch(..., check=True)` guard) -- real errors still raise.
- `python3 -m py_compile bin/actuate.py` -> ok.
- Behavioral confirmation on the live run: with an empty queue on `origin/run-2`, the fulfill form
  at `http://127.0.0.1:8765` renders `No open requests` (title `money-agent . fulfill`), no
  "cannot read" string.

### Class B (Referential)

- `bin/actuate.py` `_operator_tasks_all()`: the `if r.returncode != 0:` branch now returns `[]`
  when `"does not exist" in r.stderr`, else raises `RuntimeError(... : <stderr>)`. The `_git`
  helper (`capture_output=True, text=True`) supplies `.stderr`. This mirrors the agent-side
  `_tasks()` which already reads an absent file as `[]`.

### Class C (Negative)

- Scope is one benign failure mode: only a missing PATH returns `[]`; a missing branch and other
  git errors still raise (verified above). No change to `request`, `fulfill`, `decline`, `sync`,
  `notify-scan`, signature verification, or the facts-lane resolution read.
- No money/credential/SoD surface touched.

### Class D (Differential)

- Before: any non-zero `git show` -> `RuntimeError("cannot read requests from origin/<b>")` (the
  fulfill form rendered this as an error on an empty, agent-not-yet-started queue).
- After: `"does not exist"` -> `[]`; any other non-zero -> raise with the git stderr appended.

### Class E (Intent Alignment)

Authorized by the operator request to harden the fulfill server so that an empty actuation queue
(the normal state before the agent has queued its first request) renders as "No open requests"
rather than a read error. This aligns the operator-side read with the already-graceful agent-side
`_tasks()` and removes the need to pre-seed an empty queue file per run.

### Class F (Provenance)

- Change source is the staged `bin/actuate.py` diff, limited to the `_operator_tasks_all()`
  `returncode != 0` branch. Reproduce with `git diff --cached -- bin/actuate.py`.

## Cost

- Spent this iteration: `nothing` -- an offline read-path edit.
- Cumulative spent (from `truth.json`, not from memory): `zero` of the cap.

## Honest limitations

- The benign case is matched on the `"does not exist"` substring in git's stderr; a future git
  reworded message could route a missing path to the raise branch (fail-safe: a visible error, not
  a silent wrong result).
- Class G omitted: no pre-implementation prediction was recorded.

## Verification methodology

```bash
AGENT_BRANCH=main             python3 -c "import sys;sys.path.insert(0,'bin');import actuate;print(actuate._operator_tasks_all())"   # []
AGENT_BRANCH=no-such-branch   python3 -c "import sys;sys.path.insert(0,'bin');import actuate;actuate._operator_tasks_all()"          # raises
python3 -m py_compile bin/actuate.py
```

## Summary

R1/S0 read-path fix: the operator fulfill queue reads an absent `run/actuation_tasks.json` as an
empty list, so the fulfill form shows "No open requests" before the agent starts, while every real
git error still raises.

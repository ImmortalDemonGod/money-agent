# AIV Verification Packet (v2.1)

**Commit:** `656558d` (+ bootstrap predecessors `71fbd04`, `07f0d57`)
**Protocol:** AIV v2.0 + Addendum 2.7 (Zero-Touch Mandate)

---

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: [payments, audit_logs, autonomous_execution]
  blast_radius: "Real money on a real card under a real KYC'd legal identity, spent by an
    unsupervised agent overnight. Financial ceiling is the card issuer's hard limit. Reputational
    blast radius is nominally bounded by CONSTITUTION.md rule 2, but that is a PROMPT, not a
    mechanism. Deliberately NOT the Black Box LLC identity (UEI GWHVRM4G5FM1), which carries
    SAM.gov/SDVOSB and must never be exposed to autonomous action."
  classification_rationale: "R3 by the canonical tier table, not by self-assessment. The named R3
    surfaces are Auth, Crypto, PAYMENTS, PII, AUDIT LOGS. This repo is payments PLUS audit logs,
    executed unsupervised. R3 requires A+B+C+E+D+F -- all six classes."
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-16T05:03:12Z"
```

## Claim(s)

1. The **SoD hook rejects** any agent-authored write to `ledger/`, `CONSTITUTION.md`,
   `PREDICTION.md`, `bin/pnl.py`, or `bin/guard.py`, while **permitting** the same write under
   `AIV_VERIFIER=1`.
2. The **verifier fails closed**: `bin/pnl.py` refuses to write `ledger/truth.json` when it cannot
   reach its primary source, and `bin/guard.py` halts the loop on a missing, unverified, or
   exhausted ledger.
3. The **AIV gate is calibrated in both directions**: it rejects a fabricated profit claim and
   accepts an honest zero claim.
4. No existing tests were modified or deleted (there were none; this is the initial harness).

---

## Evidence

### Class E (Intent Alignment)

- **Link:** `CONSTITUTION.md` §"Separation of duties" @ `656558d`; `PREDICTION.md` @ tag
  `prediction-frozen` -> `71fbd0449fa63fd2720e8171887eb28c65d2a2de`.
- **Requirements Verified:**
  1. *"You produce claims. You do not produce facts."* -> enforced mechanically by
     `bin/sod_hook.sh`, not by prompt. Claim 1.
  2. *"An unverified ledger is worse than no ledger: it looks like evidence."* -> enforced by the
     fail-closed paths. Claim 2.

### Class B (Referential Evidence)

**Scope Inventory** (SHA [`656558d`](https://github.com/ImmortalDemonGod/money-agent/tree/656558d))

- Added: `CONSTITUTION.md`, `PREDICTION.md`, `PROMPT.md`, `README.md`, `MONEY_LOG.md`,
  `REFUSALS.md`, `bin/pnl.py`, `bin/guard.py`, `bin/aiv_gate.sh`, `bin/sod_hook.sh`, `.aiv.yml`,
  `.aiv-workflow.yml`, `.github/aiv-packets/TEMPLATE.md`, `.gitignore`
- Hooks (untracked, in `.git/hooks/`): `pre-commit` (chained), `aiv-pre-commit.orig`, `pre-push`

### Class A (Execution Evidence)

Run live 2026-07-15/16. **Nothing below is asserted from reading the code.**

| # | Test | Result |
|---|---|---|
| 1 | Gate vs fabricated `$47` claim, bare N/As, no hash | **FAIL (5 findings)** -- correct |
| 2 | Gate vs honest `$0` claim, real sha256, rationaled N/As | **PASS** -- correct |
| 3 | `pnl.py` with no `STRIPE_READ_KEY` | **exit 2**, `truth.json` NOT written |
| 4 | `guard.py`, no ledger | **HALT** exit 1 |
| 5 | `guard.py`, `verified:false` | **HALT** -- "a failed pull is NOT $0 earned" |
| 6 | `guard.py`, cap exhausted | **HALT** exit 2 (terminal) |
| 7 | Agent commits `ledger/truth.json` (`net_usd:9999`) | **BLOCKED** by SoD hook |
| 8 | Agent edits `CONSTITUTION.md` / `PREDICTION.md` / `bin/pnl.py` | **BLOCKED** 3/3 |
| 9 | Verifier writes `ledger/` under `AIV_VERIFIER=1` | **ALLOWED** -- correct |

- ruff: 0 errors. mypy: 1 pre-existing error (does not touch the SoD or fail-closed paths).

### Class C (Negative Evidence -- regressions absent)

- **Test 9 is the negative control for 7/8:** the SoD hook is not blocking *everything*. It
  discriminates by context, which is what makes claim 1 non-vacuous.
- **Test 2 is the negative control for Test 1:** the gate is not rejecting everything. **A gate
  that only rejects is not calibrated -- it is broken in a flattering direction.** The first cut of
  `aiv_gate.sh` did exactly that (false-failed every valid markdown table row); only running it
  caught that, and it is fixed at `656558d`.
- Search scope: all four protected surfaces exercised individually; verifier bypass exercised
  separately. Discipline borrowed from `verify-finding` (fake F998 refuted, real F017 reproduced).

### Class D (Differential Evidence)

- `.git/hooks/pre-commit`: `aiv init` default (aiv hook alone) -> chained
  `sod_hook.sh || exit 1; exec aiv-pre-commit.orig`. SoD runs **first** and hard-blocks; AIV
  atomicity second.
- `TEMPLATE.md` taxonomy: **invented A-F** (B="artifact", C="third-party", D="repro steps",
  E="scope", F="counter-evidence") -> **canonical** (A=Execution, B=Referential, C=Negative,
  D=Differential, E=Intent, F=Provenance). Corrected against `black-box/.husky/pre-commit`.
- `aiv-pre-commit.orig` shebang: `#!/usr/bin/env python3` ->
  `#!/opt/homebrew/opt/python@3.11/bin/python3.11`.

### Class F (Provenance)

- Frozen prediction: tag `prediction-frozen` -> `71fbd0449fa63fd2720e8171887eb28c65d2a2de`.
- `ledger/raw/MANIFEST.sha256` is the money anchor: every pull hashed, and `bin/aiv_gate.sh`
  rejects a money claim citing no hash from it. Rationale: `aiv-protocol#15` -- a dashboard URL is
  mutable; a hash is not.
- Repo privacy verified two independent ways: `gh` reports `isPrivate:true`; an **unauthenticated**
  `GET api.github.com/repos/ImmortalDemonGod/money-agent` returns **404**.

---

## Honest limitations

1. **Weak-mode SoD is a tripwire, not a wall.** A sandboxed agent can edit any file it sees,
   including `bin/sod_hook.sh`. Only the **card issuer's hard limit** and an **out-of-sandbox
   verifier** are load-bearing. Strong mode is documented in `README.md` and **is not deployed**.
2. **`bin/pnl.py` has never touched a live Stripe account.** Every test above exercised the
   *failure* path. The success path is **UNVERIFIED**. *This is precisely the gap this ecosystem
   keeps shipping: the failure path tested, the success path assumed.* **Do not start the loop
   until `pnl.py` prints `verified:true` against real Stripe.**
3. **`pull_privacy()` is unexercised** -- written from API docs, never called live.
4. **The ethical floor is a prompt, not a mechanism.** CONSTITUTION rule 2 has no enforcement.
5. **This packet was authored by the agent that wrote the code.** Same-author verification is the
   exact SoD weakness AIV exists to name. It needs an independent reviewer before the run.

## Product findings against AIV itself (the dogfooding payoff)

Three real defects, found by **using** the product rather than reading it:

1. **`aiv init` installs a dead hook.** Shebang `#!/usr/bin/env python3`, but `aiv` lives in
   homebrew `python@3.11` site-packages while `python3` here resolves to miniforge ->
   `ModuleNotFoundError: No module named 'aiv'` on every commit. `aiv init` printed **"Installed"**.
   **Installed != works.** Fix: emit the hook with `sys.executable`.
2. **The recommended change lifecycle cannot close.** `aiv begin` -> `git commit` -> `aiv close`
   fails with *"has no commits. Nothing to verify."* `change.json.commits` stays `[]`;
   `detect_untracked_commits()` also returns `[]`. **Isolated against the stock unchained hook --
   NOT caused by the SoD chain.** Root cause is in aiv's own docstring: *"git commit -> pre-commit
   hook appends commit to change.json"* -- **a pre-commit hook runs before the commit exists and
   cannot know its SHA.** Requires a post-commit hook; `aiv init` installs none.
3. **Bootstrap trap.** On a fresh repo, `aiv init` + `git push` is unpushable: the commits that
   *install* AIV touch functional files, cannot have packets, and pre-push blocks them as
   `--no-verify` bypasses. No documented escape. **This packet is the manual workaround.**

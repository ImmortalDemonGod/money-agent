# AIV Verification Packet (v2.1)

**Commit:** `bin/load_keys.sh`, `.env.example`, `CONSTITUTION.md` (name test)
**Protocol:** AIV v2.0 + Addendum 2.7

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: [payments, credentials, audit_logs]
  blast_radius: "Credential handling for a live Stripe account KYC'd to a real individual. A leaked
    STRIPE_READ_KEY would let the agent compute (and therefore forge) its own P&L, voiding the
    experiment. A leaked write key would let anything reachable create charges under a real name."
  classification_rationale: "R3: touches payments + credentials. Same tier as the harness it serves."
  classified_by: "Miguel Ingram"
  classified_at: "2026-07-16T05:27:00Z"
```

## Claim(s)

1. `.env` cannot be committed: it is gitignored and confirmed absent from the staged tree.
2. `bin/load_keys.sh` prefers Keychain over `.env`, and warns on any unset or placeholder key.
3. `CONSTITUTION.md` rule 2 is now enforced by the payment rail rather than by exhortation: the
   statement descriptor is the operator's real name, so the ethical floor is a property of the
   receipt, not a request.

## Evidence

### Class E (Intent Alignment)

- `README.md` §5 told the operator to `export STRIPE_READ_KEY=...` and gave him no file to put it in.
  This closes that gap.
- Ecosystem convention: `garmin`/`edready`/`zybooks` all use Keychain. `[[project_zybooks_pipeline]]`,
  `[[project_edready_pipeline]]`.

### Class B (Referential Evidence)

- Added: `.env.example`, `bin/load_keys.sh`. Modified: `CONSTITUTION.md` (rule 2 -> name test).
- Untracked by design: `.env` (real secrets).

### Class A (Execution Evidence)

- `git check-ignore -v .env` -> `.gitignore:1:.env` (ignored by rule, not by luck).
- `git diff --cached --name-only | grep -x '.env'` -> **no match**. `.env` is not in the staged tree.
- `git status --short | grep -c '\.env$'` -> **0**.

### Class C (Negative Evidence -- regressions absent)

- Verified the *absence* of the failure, not the presence of the intent: `.env` was checked against
  the staged tree AFTER writing real placeholder content to it, not before. A `.gitignore` line is a
  claim; an empty `git diff --cached` is the evidence.
- No existing behavior changed: `pnl.py` and `guard.py` untouched; they still read the same env vars.

### Class D (Differential Evidence)

- Credential source: **none** (README prose only) -> **Keychain, falling back to `.env`**.
- `CONSTITUTION.md` rule 2: an unenforceable request -> a test bound to the statement descriptor.

### Class F (Provenance)

- `.gitignore:1` is the mechanism. Verified by `git check-ignore -v`, which reports the matching
  rule and line, not merely a boolean.

## Honest limitations

1. **`bin/load_keys.sh` has never loaded a real key.** No Keychain entry exists yet and `.env` is all
   `REPLACE_ME`. The Keychain path is **unexercised** -- same gap as `pnl.py`'s success path.
2. **Keychain does not help the sandbox.** It is Mac-local, so it only serves the verifier in strong
   mode. The agent's sandbox still needs plain env vars.
3. **The name test constrains a cooperative agent.** An agent that ignores CONSTITUTION.md is not
   stopped by it. The only hard stops remain the card issuer's limit and the SoD hook.
4. **Authored by the same agent that wrote the code.** Needs an independent reviewer.

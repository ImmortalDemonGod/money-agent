# AIV Verification Packet (v2.1): showcase auto-deploy workflow

**Author:** Miguel Ingram (Author)
**Verifier:** Claude Code (Verifier)

## Logical unit of work

Adds a GitHub Actions workflow (`.github/workflows/deploy-showcase.yml`) that deploys `showcase/` to
Vercel production whenever a push to `main` touches `showcase/`, using repository secrets
(`VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID`) and the Vercel CLI. It deliberately does NOT
use Vercel's GitHub app integration, so no preview deployments are ever created for other branches or
PRs — the failure mode that put "Failed to deploy" checks on unrelated PRs (#47, #57). This commit
contains only the workflow and this packet.

## Classification

```yaml
classification:
  risk_tier: R1
  sod_mode: S0
  critical_surfaces: []
  blast_radius: local
  classification_rationale: >
    Per AIV section 5, this is deployment automation for static marketing content. It runs only on
    main pushes that touch showcase/ (or the workflow), and its sole effect is publishing the existing
    showcase/ directory to a Vercel static project. It does not touch payment behavior, credentials in
    code, the facts-lane/ledger, bin/ runtime, or any production service other than the public site.
    R1 (not R0) because it executes in CI with account-scoped secrets; R2+ is not warranted because
    there is no schema, public API, or cross-service behavior change, and the blast radius is the one
    static page it deploys.
  classified_by: Miguel Ingram (Author) + Claude Code (Verifier)
  classified_at: 2026-07-22T21:15:00Z
```

## Claim(s)

1. **CLM-001 — main-only, showcase-scoped auto-deploy with no preview surface.** The workflow triggers
   only on `push` to `main` filtered to `showcase/**` (plus the workflow file) and `workflow_dispatch`.
   It deploys the `showcase/` directory to the linked Vercel project's production via the CLI. Because
   the Vercel git app is disconnected, no branch/PR ever produces a preview deployment.

   **Falsifiable by:** the workflow's `on:` block triggering on any branch other than `main`, or on
   paths outside `showcase/`; or a preview deployment appearing for a non-main branch.

2. **CLM-002 — no functional/runtime surface beyond CI config.** The commit adds only the workflow
   YAML and this packet. No `bin/`, `tests/`, `ledger/`, source, or other config path changes.

   **Falsifiable by:** `git show --stat` listing any path outside `.github/workflows/deploy-showcase.yml`
   and this packet.

## Ledger anchor

**N/A — rationale:** this change does not mention, read, or affect money. `ledger/truth.json` is
untouched (`received_usd = 0.00`, `verified = true`); no `manifest_sha256` is cited because the packet
makes no money claim. A deployment workflow for a static page has zero ledger surface.

## Evidence

### Class A (Execution)

- YAML validity: the workflow parses as valid YAML
  (`python3 -c "import yaml;yaml.safe_load(open('.github/workflows/deploy-showcase.yml'))"` → no error).
- The three required secrets exist on the repository and the token authenticates:
  `gh secret list` shows `VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID`;
  `vercel whoami --token "$VERCEL_TOKEN"` → `immortaldemongod`.
- The deploy command itself is proven live: the equivalent CLI deploy of `showcase/` to this project's
  production already serves `https://onehonestdollar.com/` at HTTP 200 with the correct content. The
  workflow runs the same command in CI.

### Class B (Referential)

- CLM-001: the trigger scope is the committed `on:` block of
  `.github/workflows/deploy-showcase.yml` (branches `[main]`, paths `showcase/**` + the workflow,
  plus `workflow_dispatch`).
- CLM-002: the commit's complete file list is `.github/workflows/deploy-showcase.yml` and this packet
  — verifiable with `git show --stat HEAD`.

### Class E (Intent Alignment)

The immutable intent is the operator instruction to restore auto-deploy for the showcase with **zero
preview-deployment noise**, after the Vercel git app integration repeatedly put failing deploy records
on unrelated PRs. A token-based Actions deploy is the one way to auto-deploy `main` without the git app
ever touching other branches.

### Class F (Provenance)

- Source: this workflow is authored here; reproduce its scope with
  `git show HEAD:.github/workflows/deploy-showcase.yml`. The secrets it consumes were set out-of-band
  via `gh secret set` (values never committed).

## Honest limitations

- **Classes C (Negative), D (Differential), G (Prediction) omitted with rationale.** This is CI config:
  no adversarial runtime path to probe beyond the scope assertion in A/B (C); no state/`truth.json`
  delta (D); no pre-registered prediction (G).
- **The token is the operator's Vercel CLI session token** (a dedicated sub-token could not be minted:
  the OAuth session returned `forbidden` on token creation). It authenticates as `immortaldemongod` and
  works for deploys; the operator can replace it with a dashboard-scoped token at any time by re-setting
  the `VERCEL_TOKEN` secret. It lives only as a GitHub secret, never in the repo.
- **Full end-to-end firing is confirmed post-merge** via `workflow_dispatch`, since the workflow only
  exists once merged to `main`. The deploy command it runs is already verified live (Class A).

## Verification methodology

```bash
python3 -c "import yaml;yaml.safe_load(open('.github/workflows/deploy-showcase.yml'))"  # valid YAML
git show --stat HEAD                # only the workflow + this packet
vercel whoami --token "$VERCEL_TOKEN"   # immortaldemongod
# post-merge: gh workflow run "Deploy showcase to Vercel production" ; then curl onehonestdollar.com
```

## Summary

Adds a main-only, `showcase/`-scoped GitHub Actions workflow that deploys the site to Vercel production
via a token, with the Vercel git app disconnected so no preview deployments are ever created. R1/S0 CI
config; no runtime, payment, or ledger surface. This restores auto-deploy while permanently ending the
cross-PR "Failed to deploy" noise.

# VERIFICATION PACKET -- ITERATION 070

> **Risk tier: R3 (HIGH).** Payments + audit logs, unsupervised, real legal identity.

## Claim

The pivot opened with three verified results: (1) all five product funnels were GEO-patched
(canonical + machine-validated JSON-LD + llms.txt via new idempotent bin/geo_patch.py), redeployed,
and re-audited to zero findings; (2) surge.sh was discovered and LIVE-VERIFIED to force-serve a
robots.txt Disallow-all on every site, overriding project files -- meaning every product this run
shipped was invisible to compliant crawlers the whole time; (3) neocities was falsified as the
replacement host by an honest submit test (enforced hCaptcha challenge iframe), while deep research
mapped the in-bounds replacements: telegra.ph (zero-gate, index-follow), IndexNow (no account),
Stripe Directory/MPP fiat (existing account is the gate). No money received, none spent; the ledger
is a truthful zero.

## Ledger anchor

- `manifest_sha256` cited: `39e2c8d0fbdb4e1534a7f331867d2eae1c7ba332ae6d077a106bad15e2876cca`
  (whole-manifest sha from verifier-committed `ledger/truth.json`; empty post-baseline
  balance-transactions pull, file sha `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`)
- `ledger/truth.json` at time of claim: `received_usd = 0.0`, `verified = true`, cap remaining
  twenty-five dollars, computed_at `2026-07-16T22:33:54Z`

## Evidence by class -- ALL SIX REQUIRED (R3)

| Class | What it means here | Evidence |
|---|---|---|
| A) Execution | Real work this iteration | guard exit 0 first. bin/audit.py before/after on all five funnels (before: five P1s; after: five clean runs, outputs in-transcript). bin/geo_patch.py committed (5a1cacd). surge deploys returned Success x5; live curl confirmed ld+json present and llms.txt HTTP 200 on all five. robots test: curl of three sites returned Disallow-all; a deployed project robots.txt (Allow) was still served as Disallow -- override falsified. neocities: headed-Playwright honest submit produced a live hCaptcha challenge frame (URL captured in transcript) + screenshot. |
| B) Referential | SHA-pinned artifacts | Commits 5a1cacd (geo-patch + products) and this packet's commit (MONEY_LOG iter-070 + REFUSALS iter-070 + packet together). Research report preserved in session transcript with source URLs. |
| C) Negative | No money lost, no boundary crossed | received zero, spent zero (verifier-measured). No captcha defeated (neocities attempt was an HONEST signup that stopped at the wall and was logged as a refusal). No .env read, no ledger write. Deploys touched only our own five surge sites. |
| D) Differential | State before vs after | Before: five funnels each carrying the P1 we sell the fix for, on a host silently blocking all crawlers, with no map of agent-payable surfaces. After: five clean funnels (JSON-LD live), the crawler-block PROVEN and scoped (discovery pages must move; delivery pages can stay), a falsified host candidate, and a ranked in-bounds action list (Stripe Directory/MPP probe, telegra.ph story hub, IndexNow when root-controllable host exists). |
| E) Intent | Constitution authorization | Operator directive (069): audits closed, "try something completely different." This iteration opens that pivot: own-asset fixes + research + host falsification. Nothing sold, nothing promised post-payment; no outbound messages sent this iteration. |
| F) Provenance | Hash the claim rests on | `39e2c8d0fbdb4e1534a7f331867d2eae1c7ba332ae6d077a106bad15e2876cca` (whole manifest) and `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945` (empty balance-transactions) from `ledger/raw/MANIFEST.sha256`. |

## Cost

- Spent this iteration: zero dollars
- Cumulative spent (from `truth.json`): zero dollars of a twenty-five-dollar cap

## Honest limitations

- **The GEO fixes are on a host that blocks crawlers**, so their standalone discovery value is ~nil
  until discovery pages move to an indexable surface; they were kept because delivery pages remain on
  surge and the patch cost was near-zero.
- **llms.txt research says no major engine reads it** -- shipped as hygiene, not counted as a lever.
- **The mid-iteration verifier reset shipped 4 of 5 sites unpatched for ~10 minutes** before the
  commit-first redeploy corrected it; commit-before-deploy is now standing practice.
- **Stripe Directory/MPP viability is unprobed** -- the restricted write key may lack profile scopes;
  that probe is iteration 071, and a 403 would itself be a finding.
- **Weak-mode caveat unchanged.** The zero is real regardless.

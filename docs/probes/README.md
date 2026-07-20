# docs/probes/ -- issue #32 marketplace probe records

One record per platform, produced by the read-only slice of #32's six-step deep-dive
protocol. These are the DURABLE artifacts; the fit table on #30 is a derived view and every
label in it must trace to a record here.

**Scope executed vs runbooked (operator decision, 2026-07-20):** steps 1 (primary docs),
2 (verbatim ToS/AUP), 3 (onchain explorer reads where reachable), 5 (published unit
economics), 6 (cold-start mechanics as documented) were executed from this sandbox,
read-only -- no signups, no form submissions, no wallet connections. Step 4 (the onboarding
probe from the real environment) is `not_run` in every record and lives in the operator
runbook (`docs/runbooks/RUN2_OPERATOR_RUNBOOK.md`): it requires signup actions this session
deliberately did not take.

**Schema provenance:** adapted from the ProbeRecord suggestion posted on #32 by a third
party (github.com/mheilimo, 2026-07-20 comment). The schema idea and the seven release
gates are taken with adaptation; the product referenced in that comment is unrelated to
these records.

## The honesty gates (bind every field of every record)

1. `not_observed`, `inaccessible`, and `not_run` NEVER render as "absent" and cannot flip
   a platform label. A blocked fetch is a fact about this sandbox, not about the platform.
2. A provider statement stays a CLAIM at its evidence tier. Docs/landing pages are Tier 3-4;
   an onchain read is Tier 1-2. The tier rides with each finding, and landing copy is
   labeled separately from docs.
3. Verbatim quotes are copy-paste with URL + retrieval timestamp. A paraphrase is never
   presented as a quote.
4. Unit economics must be recomputable: task value, platform fee, rail cost, asset, price
   source, capture time. No silent estimates.
5. Payer/worker identities stay `unknown` until evidence classifies them. Seeded or wash
   volume is never inferred from concentration alone.
6. Cold-start fit requires an actual zero-reputation attempt (step 4, runbooked) -- what
   these records carry is only the DOCUMENTED selection mechanics, marked as such. A
   permissionless registration path does not establish access to paid work.
7. A label change (vs the prior #30/#32 labels) records the previous label, the new label,
   one named falsifier, and the evidence that triggered it -- inside the record.
8. Nothing from model memory: these platforms are mostly newer than the researching model's
   cutoff. Every claim carries a fetched source; research was performed by parallel
   subagents bound to these same rules, with load-bearing quotes spot-checked by a second
   independent fetch before transcription (spot-checks noted in the records).

## Record layout (YAML, one file per platform)

```yaml
schema_version: 1
platform_id: ...
captured_at: ...          # UTC, when the probe fetches ran
repository_commit: ...    # HEAD when the record was written
prior_label: ...          # from issue #32's list
verdict: confirmed | flipped | undetermined
verdict_basis: ...        # the named artifact(s); undetermined = read-only slice insufficient
probes:                   # one entry per protocol step executed
  - step: docs | terms | onchain | economics | cold_start | onboarding
    status: observed | not_observed | inaccessible | not_run
    finding: ...
    evidence:
      tier: 1-5           # COMPARATIVE_ANALYSIS.md tier framework
      source_class: primary_docs | terms | landing | explorer | press | third_party
      locator: ...        # URL(s) / tx hash / block range
      retrieved_at: ...
    quotes: [...]         # verbatim only, with per-quote URL
economics: {...}          # recomputable per gate 4, or nulls
limitation: ...           # what the read-only slice could not see
next_falsifier: ...       # what step 4 (runbooked) must chase first
```

Records feed: #30 (rail adapter scope -- the per-chain settlement summary), #31 (which
platforms need the human-actuation queue), and the run-2 strategy memo. They live in docs/
deliberately: the run agent's context discipline (CLAUDE.md "Your world") excludes docs/,
so none of this pre-seeds run-2 strategy into agent-facing files.

# AIV Verification Packet (v2.1): beacon JS-execution gate + honest labeling (v2 template)

**Author:** Miguel Ingram (Author)
**Verifier:** Claude Code (Verifier)

## Logical unit of work

Ports the industry-standard analytics stack into the **v2 reusable beacon template**
(`harness/beacon/worker.js`) so run 2 inherits it, matching the fix already deployed on the run-1
worker. Three changes: (1) a `/px` JS-execution beacon endpoint; (2) a hub `<script>` that fires it;
(3) an honest `stats()` rewrite that reports `est_human_sessions` (JS-confirmed AND not-flagged-bot)
with the method + residual disclosed in the output, instead of a bare `humans` count. This commit
contains only the worker template and this packet.

## Classification

```yaml
classification:
  risk_tier: R1
  sod_mode: S0
  critical_surfaces: []
  blast_radius: local
  classification_rationale: >
    Per AIV section 5, this is analytics/observability code for a static-content beacon. It changes
    how visit counts are gathered (JS gate) and reported (labels), touching no payment behavior, no
    credentials, no facts-lane/ledger, and no bin/ runtime. It reads its own D1 hits table; it does
    not read or write money. R1 (not R0) because it is executable worker code with a public endpoint;
    R2+ is not warranted -- no schema change (uses the existing hits.path column), no cross-service or
    payment surface, blast radius is the beacon's own stats.
  classified_by: Miguel Ingram (Author) + Claude Code (Verifier)
  classified_at: 2026-07-22T22:00:00Z
```

## Claim(s)

1. **CLM-001 — JS-execution gate + honest labeling in the template.** `harness/beacon/worker.js` now
   serves a hub `<script>` firing `/px`, handles `/px` (logs the hit, returns 204), and `stats()`
   reports `est_human_sessions` = rows with `path='/px' AND bot=0`, alongside `raw_hits_all_paths`,
   `js_confirmed_hits`, `server_hits_flagged_bot`, an ASN breakdown of the est-human bucket, and a
   `_method` field disclosing it is an estimate (headless browsers inflate, VPN/cloud-browser humans
   deflate) whose ground truth is `received_usd`.

   **Falsifiable by:** the template lacking a `/px` route or the hub `<script>`; or `stats()` still
   returning a bare `humans` field computed from all server-side hits rather than the JS-gated `/px`
   bucket.

2. **CLM-002 — parity with the already-deployed run-1 worker, no other surface touched.** The three
   changes mirror those live on `iterations/097/worker_beacon.js`. The commit changes only the worker
   template and this packet.

   **Falsifiable by:** `git show --stat` listing any path outside `harness/beacon/worker.js` and this
   packet.

## Ledger anchor

**N/A — rationale:** this change does not mention, read, or affect money. `ledger/truth.json` is
untouched; no `manifest_sha256` is cited because the packet makes no money claim. A visit-analytics
beacon has zero ledger surface — indeed the packet's own point is that the beacon is *not* a money
signal and defers to `received_usd` as ground truth.

## Evidence

### Class A (Execution)

- Syntax: `node --check harness/beacon/worker.js` → passes.
- Presence checks on the committed file: `/px` route = 1, hub `sendBeacon('/px')` = 1,
  `est_human_sessions` referenced (SQL + label + method) = 4.
- The identical change is already deployed and verified live on the run-1 worker
  (`one-honest-dollar.cloud-pyramid.workers.dev`): `/px` returns 204, the hub serves the beacon
  script, and `/stats` returns the new shape — the old server-side "humans" (inflated by browser-UA
  crawlers) collapsed to only the hits that actually executed JS.

### Class B (Referential)

- CLM-001: the three edits live at, respectively, the `/px` handler in the fetch switch, the
  `<script>` in `hubHtml`, and the rewritten `stats()` — all in `harness/beacon/worker.js`.
- CLM-002: the commit's complete file list is `harness/beacon/worker.js` + this packet
  (`git show --stat HEAD`), and the changes correspond one-to-one with the deployed run-1 commit on
  `claude/project-analysis-q4hjrg`.

### Class E (Intent Alignment)

The immutable intent is the operator instruction to make the beacon's human/bot metric honest — not
by proving humanity (impossible at the request layer) but by adopting the standard practical stack
(JS gate + labeled estimate + funnel-weighting to the money). This belongs in the v2 template so the
next run inherits it, rather than only on the run-1 worker.

### Class F (Provenance)

- Source: the three changes are ports of the deployed run-1 worker commit; reproduce by diffing the
  `/px` handler, hub `<script>`, and `stats()` against
  `origin/claude/project-analysis-q4hjrg:iterations/097/worker_beacon.js`.

## Honest limitations

- **Classes C (Negative), D (Differential), G (Prediction) omitted with rationale.** Behavioral
  parity is asserted via the deployed-worker evidence in A (C); there is no state/`truth.json` delta
  (D); no pre-registered prediction (G).
- **The metric remains an estimate, by design and by physics.** A headless real browser runs JS and
  can pass the bot heuristics (inflates); a VPN/cloud-browser human egresses from a datacenter ASN
  and is flagged bot (deflates). No request-layer signal proves humanity — the fix makes the number
  *honest and bounded*, not *true*. The ground truth for a valuing human is `received_usd`.
- The run-1 **funnel** pages (surge) would need the same beacon `<script>` to be JS-gated end-to-end;
  this commit hardens the hub/template. Full funnel coverage is a separate follow-up.

## Verification methodology

```bash
node --check harness/beacon/worker.js
git show --stat HEAD    # only harness/beacon/worker.js + this packet
# live parity: curl "https://one-honest-dollar.cloud-pyramid.workers.dev/stats?k=<secret>"  -> new shape
```

## Summary

Ports the JS-execution gate and honest `est_human_sessions` labeling into the v2 beacon template so
the next run inherits the industry-standard stack instead of raw server-side "anything with a browser
UA is human" logic. R1/S0 observability code; no runtime, payment, or ledger surface. The metric is
now a bounded, disclosed estimate; the money remains the only ground truth.

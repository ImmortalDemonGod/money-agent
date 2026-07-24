# AIV Verification Packet (v2.1): reusable beacon tag + per-site attribution (v2 template)

**Author:** Miguel Ingram (Author)
**Verifier:** Claude Code (Verifier)

## Logical unit of work

Delivers the foundational piece of #65 in the v2 beacon template (`harness/beacon/worker.js`): a
reusable `/beacon.js` analytics tag so any site instruments itself with one line, plus per-site
attribution. Three parts: (1) a `/beacon.js` route serving a small tag that fires the JS-gated `/px`
ping with the site's `data-site` id + referrer; (2) `/px` reads and stores that `site` id (in the
`dest` column) and adds CORS so cross-origin sites can ping it; (3) `stats()` adds
`est_human_sessions_by_site`, and the hub dogfoods the tag instead of an inline snippet. This commit
contains only the worker template and this packet.

## Classification

```yaml
classification:
  risk_tier: R1
  sod_mode: S0
  critical_surfaces: []
  blast_radius: local
  classification_rationale: >
    Per AIV section 5, this is analytics/observability code for a static-content beacon. It adds a
    served JS tag and a query param to an existing endpoint; it touches no payment behavior, no
    credentials, no facts-lane/ledger, and no bin/ runtime. The served tag only calls
    navigator.sendBeacon to the beacon's own /px. R1 (executable worker code, public endpoints);
    R2+ is not warranted -- no schema change (reuses hits.dest), no cross-service or payment surface.
  classified_by: Miguel Ingram (Author) + Claude Code (Verifier)
  classified_at: 2026-07-22T23:20:00Z
```

## Claim(s)

1. **CLM-001 — one-line, per-site instrumentation in the template.** `harness/beacon/worker.js` now
   serves `/beacon.js` (a tag firing `/px?site=<data-site>&ref=<referrer>`), `/px` stores the `site`
   id and returns CORS-open 204, `stats()` reports `est_human_sessions_by_site`, and the hub includes
   the tag via `<script src=".../beacon.js" data-site="hub">` rather than an inline snippet.

   **Falsifiable by:** the template lacking a `/beacon.js` route; or `/px` ignoring the `site` query;
   or `stats()` lacking `est_human_sessions_by_site`.

2. **CLM-002 — no surface beyond the beacon template.** The commit changes only
   `harness/beacon/worker.js` and this packet.

   **Falsifiable by:** `git show --stat` listing any other path.

## Ledger anchor

**N/A — rationale:** this change does not mention, read, or affect money. `ledger/truth.json` is
untouched; no `manifest_sha256` is cited because the packet makes no money claim. Visit analytics
has zero ledger surface — the packet's own point is that the beacon defers to `received_usd` as the
only human-value ground truth.

## Evidence

### Class A (Execution)

- Syntax: `node --check harness/beacon/worker.js` → passes.
- The identical change is **deployed and verified live** on the run-1 worker
  (`one-honest-dollar.cloud-pyramid.workers.dev`, this session):
  - `curl .../beacon.js` → HTTP 200, `content-type: application/javascript`, returns the tag with the
    beacon origin baked in.
  - Server leg: `curl .../px?site=pr65-test` (browser UA + Accept-Language) → 204, and `.../stats`
    then reports `est_human_sessions_by_site` including `{site: "pr65-test", n: 1}` — i.e. a tag-fired
    ping is attributed to its site and surfaces per-site.
  - Client leg: `/beacon.js` is a standard `navigator.sendBeacon` call; its served body was inspected
    directly (above). Live in-browser execution was not re-run here (the local Playwright browser
    binary is not installed); the served JS is the verification of the client leg.

### Class B (Referential)

- CLM-001: the `/beacon.js` route + updated `/px` sit in the fetch switch of
  `harness/beacon/worker.js`; the `est_human_sessions_by_site` query + field are in `stats()`; the
  hub tag is in `hubHtml`.
- CLM-002: `git show --stat HEAD` lists only `harness/beacon/worker.js` and this packet; the changes
  correspond one-to-one with the deployed run-1 commit on `claude/project-analysis-q4hjrg`.

### Class E (Intent Alignment)

The immutable intent is the operator instruction to close #65 — make instrumenting a new site a
single line (a served tag) instead of hand-wiring the ping into every page, so run 2 cannot ship a
blind site. This is the foundation the publish-injection and Stage-0-gate items of #65 build on.

### Class F (Provenance)

- Source: port of the deployed run-1 worker commit; reproduce by diffing the `/beacon.js` route,
  `/px` handler, hub tag, and `stats()` against
  `origin/claude/project-analysis-q4hjrg:iterations/097/worker_beacon.js`.

## Honest limitations

- **Classes C (Negative), D (Differential), G (Prediction) omitted with rationale.** Behavioral
  parity is asserted via the deployed-worker evidence in A (C); no state/`truth.json` delta (D); no
  pre-registered prediction (G).
- **Scope: this is #65 item 1 only.** The publish-path *injection* of the tag (so a site cannot ship
  without it) and wiring the ping into `spine.py`'s Stage-0 `funnel events CONFIRMED` self-test are
  deliberately **follow-up** work, not in this commit.
- **The metric is still an estimate** for the same reasons documented on the JS-gate (#61): headless
  browsers inflate, VPN/cloud-browser humans deflate; `received_usd` stays the only ground truth.
- **Client-leg live-browser run not performed here** (Playwright browser not installed); the served
  tag body was inspected instead.

## Verification methodology

```bash
node --check harness/beacon/worker.js
git show --stat HEAD    # only harness/beacon/worker.js + this packet
# live parity (run-1 worker): curl .../beacon.js ; curl ".../px?site=X" ; curl ".../stats?k=<secret>"
```

## Summary

Adds a reusable `/beacon.js` tag and per-site attribution to the v2 beacon template, so instrumenting
any run-2 site is one line and its traffic is attributable. R1/S0 observability; no runtime, payment,
or ledger surface. Foundation for #65's publish-injection and Stage-0-gate follow-ups.

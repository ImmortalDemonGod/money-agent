# AIV Verification Packet (v2.1): instrument the showcase (onehonestdollar.com) before run 2

**Author:** Miguel Ingram (operator) + Claude Code (this session)
**Context:** operator-side harness prep, not an in-run agent iteration. Pre-run-2 stage-0 work.

## Logical unit of work

Close the one un-instrumented public funnel before run 2 begins. `onehonestdollar.com` (the run-1
showcase, served from Vercel) shipped without the beacon tag, so its traffic is unmeasured — the exact
failure class run 1 hit at scale (~60 funnels with no telemetry, `#65 F3`) and the reason
`instrument_check` records it as `GATE FAIL (unmeasured)`
(`VERIFICATION_PACKET_INSTRUMENT_GATE.md:82`). This adds the one-line beacon tag plus the canonical
privacy disclosure, pointing at the already-live run-1 beacon worker
(`one-honest-dollar.cloud-pyramid.workers.dev`) so no new credential or Worker deploy is required.

Two changes, both in the single functional file `showcase/index.html`:

- **The beacon tag**, inserted before `</body>` by `bin/instrument_check.py --inject` (the mechanized
  path, not a hand-edit): `<script src="https://one-honest-dollar.cloud-pyramid.workers.dev/beacon.js"
  data-site="onehonestdollar"></script>`. `data-site="onehonestdollar"` gives per-site attribution so
  showcase traffic is separable from run-1 data in `/stats` (`est_human_sessions_by_site`).
- **The privacy line**, added to the footer verbatim from the beacon hub's canonical `analytics_note`
  (`harness/beacon/worker.js:23`) with a link to the live `/privacy` page — so the page honestly
  discloses it is now measured, in the established project wording rather than a new phrasing.

## Classification

```yaml
classification:
  risk_tier: R1
  sod_mode: S0
  critical_surfaces: [public_funnel]
  blast_radius: public-showcase-page
  classification_rationale: >
    Edits one static public HTML page (showcase/index.html). No payment surface, no ledger, no
    verifier/gate script, no credential, and no code path the agent is scored on is touched --
    showcase/ is not on the sod_hook protected list. The added beacon worker was itself already
    deployed and privacy-reviewed; this only embeds its existing client tag. The one real-world edge
    is that a push to main auto-deploys to production (onehonestdollar.com), so the change is
    outward-facing -- hence R1 rather than R0, and hence merged by the operator, not pushed
    unilaterally.
  classified_by: Miguel Ingram (operator) + Claude Code (this session)
  classified_at: 2026-07-24T00:00:00Z
```

## Claim(s)

1. **CLM-001 — the showcase source now carries the beacon tag.** `showcase/index.html` contains
   exactly one `<script src=".../beacon.js" data-site="onehonestdollar">` immediately before
   `</body>`, inserted by the mechanized `--inject` path.
   **Falsifiable by:** `grep -c 'beacon\.js' showcase/index.html` != 1, or the tag not anchored before
   `</body>`.

2. **CLM-002 — the beacon host is live and accepts the ping.** The cited host serves `/beacon.js`
   (200) and accepts the `/px` beacon ping (204), so a real browser loading the deployed page will
   register a measurable hit.
   **Falsifiable by:** `/beacon.js` or `/px` returning a non-2xx from the cited host.

3. **CLM-003 — measurement is disclosed in the canonical wording.** The footer carries the beacon
   hub's `analytics_note` verbatim plus a link to the live `/privacy` page (200).
   **Falsifiable by:** the added footer line diverging from `worker.js`'s `analytics_note`, or the
   `/privacy` link 404ing.

4. **CLM-004 (deferred to post-merge) — the LIVE page serves the tag.** After the operator merges to
   main and Vercel redeploys, `python3 bin/instrument_check.py https://onehonestdollar.com` emits
   `verdict=PASS`, clearing the funnel's stage-0 for real.
   **Status:** UNVERIFIED at commit time by construction — the tag is not on the live site until the
   deploy fires (`live beacon.js count = 0` this session). This claim is closed post-merge, not now.

## Ledger anchor

**N/A — rationale:** this change does not read, mention, or affect money. `ledger/truth.json` is
untouched and no ledger file is in the diff (`git show --stat` proves it). The showcase's only revenue
element (the "Tip the experiment" Stripe link) is unchanged by this edit.

## Evidence

### Class A (Execution) — run this session

- **CLM-001 (inject):** `python3 bin/instrument_check.py --inject showcase/index.html --beacon
  https://one-honest-dollar.cloud-pyramid.workers.dev --site onehonestdollar` →
  `instrumented: showcase/index.html (site=onehonestdollar, ...)`, exit 0. `grep -n` confirms the tag
  at line 313, before `</body>`.
- **CLM-002 (host live):** `curl` this session → `/beacon.js` HTTP 200, `/px` HTTP 204, `/privacy`
  HTTP 200 on `one-honest-dollar.cloud-pyramid.workers.dev`. The served `/beacon.js` reads `data-site`
  and fires `/px?site=<id>&ref=<referrer>` via `navigator.sendBeacon` (no-cors), so the cross-origin
  embed on onehonestdollar.com works without a CORS preflight.
- **CLM-004 (the gap, pre-deploy):** `curl https://onehonestdollar.com/ | grep -c beacon.js` → `0`
  this session. This is the state the deploy fixes; the post-deploy PASS is deferred (see Honest
  limitations).

### Class B (Referential)

- CLM-001: the injected `<script ...beacon.js... data-site="onehonestdollar">` line in
  `showcase/index.html` (this commit), anchored directly after the existing inline scroll-progress
  script, before `</body>`.
- CLM-003: the added footer `<p>` in `showcase/index.html`, text matching `CONFIG.analytics_note` in
  `harness/beacon/worker.js`.
- Base: branched from `main` at `b6c9fb2`.

### Class C (Negative)

- **No regression to the page.** The change is +2 lines (one tag, one footer `<p>`); no existing
  markup, copy, styling, or the Stripe tip link is altered (`git diff --stat` → `1 file changed, 2
  insertions(+)`).
- **No over-claim of privacy.** The disclosure is the project's own reviewed wording, not a stronger
  claim than the deployment keeps; the beacon stores no raw IP (salted daily hash, refuses to log
  without `HASH_SALT`).
- **No premature live claim.** The packet deliberately does NOT cite `INSTRUMENT_CHECK_URL:`, so
  `aiv_gate.sh`'s 2b-bis re-run is not invoked against a URL that would (correctly) FAIL pre-deploy;
  the live PASS is claimed only after the deploy makes it true.

### Class D (Differential)

- Before: `showcase/index.html` has no beacon tag; live `onehonestdollar.com` serves 0 beacon tags;
  `instrument_check` records the funnel as `GATE FAIL (unmeasured)`.
- After (source): the file carries the tag + disclosure. After (live, post-merge): the deployed page
  serves the tag and `instrument_check` returns PASS. `truth.json`: no delta.

### Class E (Intent Alignment)

Serves the operator's explicit instruction to instrument the showcase before run 2, and the harness
mandate that a published funnel must be measured by construction rather than by memory — the whole
reason the instrument probe is stage-0 of the business spine. The name-test line of the constitution
is respected: the page already leads with the AI-authorship disclosure and now adds an honest
measurement disclosure in the operator's own words.

### Class F (Provenance)

- The tag was produced by `bin/instrument_check.py --inject` (verifier-frozen tool), not hand-typed;
  the beacon host and `/beacon.js` body were fetched live this session (200 / 204).
- The privacy wording is copied from `harness/beacon/worker.js` `CONFIG.analytics_note`; the
  `/privacy` target is the live page that worker serves.

## Cost

- Spent this change: **nothing**. No new Worker, no new credential — the run-1 beacon worker is reused.
- Cumulative spent (from `truth.json`): **zero** of the $25 cap; unchanged.

## Honest limitations

- **CLM-004 is unverified until the operator merges and Vercel redeploys.** By construction the live
  page cannot serve the tag before the deploy, so no live `verdict=PASS` exists at commit time. The
  packet is honest about this: the live check is a named, deferred claim, closed by re-running
  `instrument_check.py https://onehonestdollar.com` after merge and recording the PASS line — not a
  claim made now.
- **Reused run-1 worker, shared D1.** Showcase hits land in the same database as run-1 beacon data.
  Per-site attribution (`data-site="onehonestdollar"`) keeps them separable in `/stats`, but this is a
  shared instrument, not a fresh run-2 deploy. Chosen deliberately (operator decision) for a
  zero-credential fix; a fresh worker remains a one-line host swap later.
- **The beacon estimates humans; it does not prove them.** `est_human_sessions` has the known,
  irremovable residual the worker states in its own `/stats._method`: headless real browsers inflate,
  VPN/cloud-browser humans deflate. The only ground truth for a valuing human is `received_usd`.
- **This session is not an out-of-band verifier.** Standard SoD caveat: operator-side prep, recorded
  honestly; the change touches no scored surface, so the weaker separation cannot wave a money claim
  through.

## Verification methodology

```bash
grep -c 'beacon\.js' showcase/index.html                       # == 1 (CLM-001)
grep -n 'analytics_note' harness/beacon/worker.js              # source of the footer text (CLM-003)
curl -sI https://one-honest-dollar.cloud-pyramid.workers.dev/beacon.js   # 200 (CLM-002)
git show --stat HEAD                                           # showcase/index.html + this packet, no ledger/
# --- after the operator merges to main (deploy fires) ---
python3 bin/instrument_check.py https://onehonestdollar.com   # verdict=PASS closes CLM-004
```

## Summary

Instruments the last un-measured public funnel before run 2: one mechanized beacon tag +
canonical privacy disclosure in `showcase/index.html`, pointing at the already-live run-1 beacon so
the fix needs no new credential. R1/S0, +2 lines, no scored surface touched. The live-page PASS is a
named, deferred claim closed after the operator merges to main and the Vercel deploy makes it true.

# Traffic beacon — deploy BEFORE the first publish (M7)

Run 1's most expensive measurement failure: 9 funnels, zero analytics, and a headline conclusion
("the binding constraint is reach") that had to be retracted because `$0.00` cannot distinguish a
reach wall from a conversion wall (run-1 iteration 098). The instrument that decides it was built
at iteration 097 — after the run was over. **In v2 the beacon deploys at run START**, so every
publish is measurable from hour one and TRAFFIC_BASELINE-style forensics are never needed again.

What it gives you per hit: path, referrer, UA (raw + bot/human classification), CF country/ASN,
daily-salted truncated IP hash (no raw IPs), and `/go` click-through logging to product/pay links.
`/stats?k=<STATS_SECRET>` returns bot/human split, humans-by-country, click-throughs.

## Deploy (operator or agent-with-token)

1. Fill `CONFIG` in `worker.js` (site name, honest description, disclosure line — run it through
   `bin/disclosure_gate.py` like any outbound surface — pages list, allowed redirect prefixes, a
   fresh 32-hex IndexNow key). Fill `name` in `wrangler.toml`.
2. `wrangler d1 create beacon` → paste the id into wrangler.toml.
3. `wrangler d1 execute beacon --file=schema.sql`
4. `wrangler secret put STATS_SECRET`
5. `wrangler deploy` (needs an authenticated wrangler, or the no-account temporary deploy that
   must then be claimed — run 1 proved both paths; the unclaimed temp host filters crawler UAs,
   so claim it before trusting IndexNow to convert).
6. Verify with `python3 bin/host_check.py https://<worker-host>/` — it must PASS before any packet
   claims the hub is published.

## Instrument each new site with ONE line — and prove it (#65)

Run 1 shipped ~9 funnels with zero analytics because instrumentation was a remembered checklist item,
not a mechanical one. v2 makes it one line and makes shipping-without-it *fail closed*:

1. **Serve the tag.** The worker exposes `GET /beacon.js`. Every page a run-2 site publishes gets:

   ```html
   <script src="https://<worker-host>/beacon.js" data-site="<site-id>"></script>
   ```

   `data-site` attributes the hit; `/stats` breaks humans out by site (`est_human_sessions_by_site`).

2. **Don't hand-paste it — inject it.** Before publishing a built page, mechanize the tag in:

   ```bash
   python3 bin/instrument_check.py --inject dist/index.html --beacon https://<worker-host> --site <id>
   ```

   Idempotent (won't double-add) and **fail-closed**: a page with no `</body>` to anchor to exits
   non-zero rather than shipping blind.

3. **Verify the LIVE page carries it — the gate re-runs this.** After deploy:

   ```bash
   python3 bin/instrument_check.py https://<site-url>          # exit != 0 if the tag is missing
   # -> INSTRUMENT_CHECK: <url> | tag=PRESENT | site=<id> | beacon=<host> | verdict=PASS
   ```

   That `INSTRUMENT_CHECK:` line is the deterministic **Stage-0 instrument-probe evidence** — the
   exact analog of `host_check`'s `HOST_CHECK:` for the substrate probe. Cite it in the packet via
   `INSTRUMENT_CHECK_URL: <url>`; `bin/aiv_gate.sh` **re-runs `instrument_check` on that URL** and
   trusts only its own fresh result (a self-typed verdict line is not evidence). So a site cannot
   clear stage 0 as "instrumented" unless the live page actually serves the tag.

## Privacy / name-test invariants (do not weaken)

- No raw IP is ever stored (SECRET-keyed, daily-salted truncated hash only — set `HASH_SALT` via
  `wrangler secret put HASH_SALT`; a public date salt alone is dictionary-reversible).
- Referrer is minimized to origin+path before storage (query strings carry emails/tokens).
- The hub page renders the analytics disclosure (`CONFIG.analytics_note`), and its disclosure line
  must have a recorded EV decision in `DISCLOSURE_EV_LOG.md` and LEAD the rendered message.
- `/go` redirects only to `CONFIG.allowed_dest_prefixes` (open-redirect guard).
- **Retention:** raw `ua` is kept for bot-classification refinement. Add a scheduled purge (a Cron
  Trigger running `DELETE FROM hits WHERE ts < date('now','-90 days')`) before running this beyond
  a short experiment — indefinite UA retention under a real name is not acceptable.

## Two counting rules the instrument must keep (learned the hard way, 2026-07-20)

Within two hours of first deployment the beacon reported **2 human visitors**. Both were
`/favicon.ico` fetches — one from **Google LLC**'s network, one from a Norwegian hosting company —
wearing full browser user-agents with `Accept-Language`. Zero people had actually opened a page.

1. **Asset paths are not visits.** `favicon.ico`, icons, css/js, fonts. A browser fetches them
   alongside a page, so counting them double-counts a real visitor; and a bare crawler asset fetch
   manufactures a visit out of nothing. They are still LOGGED (they are evidence) but excluded from
   every human-facing number. `ASSET_SQL` in `stats()` must stay in sync with `ASSET_RE`.
2. **A browser UA from a datacenter ASN is a bot.** Cloudflare already hands us `asOrganization`;
   use it. Consumer ISPs are deliberately absent from `DATACENTER_RE`.

The point is not the two rows. It is that **an instrument which flatters its own numbers is worse
than no instrument**, because a false "someone arrived" is exactly the conclusion run 1 had to
retract. `/stats` now reports `page_views`, `humans`, `bots` and `assets_excluded` separately, so
what was dropped is visible rather than silently swallowed.

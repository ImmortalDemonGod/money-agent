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

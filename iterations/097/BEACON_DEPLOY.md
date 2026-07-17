# Beacon deploy — measure real traffic on the claimed Worker

The Worker `one-honest-dollar.cloud-pyramid.workers.dev` is in YOUR Cloudflare account; my sandbox
wrangler is unauthenticated. Either run these yourself, or export a scoped `CLOUDFLARE_API_TOKEN`
(perms: **Account > Workers Scripts: Edit**, **Account > D1: Edit**, **Account settings: Read**) and
I will deploy + verify.

Files (in iterations/097/): `worker_beacon.js`, `wrangler.toml`, `schema.sql`.

```bash
cd iterations/097
# 1. create the D1 database, then paste its database_id into wrangler.toml
wrangler d1 create beacon
# 2. create the table
wrangler d1 execute beacon --remote --file schema.sql
# 3. set the /stats auth secret (any random string)
wrangler secret put STATS_SECRET
# 4. deploy
wrangler deploy
```

## Read the data
- Summary + bot/human split + click-throughs (JSON):
  `curl "https://one-honest-dollar.cloud-pyramid.workers.dev/stats?k=<STATS_SECRET>"`
- Or straight SQL:
  `wrangler d1 execute beacon --remote --command "SELECT bot, COUNT(*) n FROM hits GROUP BY bot"`
  `wrangler d1 execute beacon --remote --command "SELECT ts,country,as_org,substr(ua,1,60) FROM hits WHERE bot=0 ORDER BY id DESC LIMIT 20"`

## What it measures
- Every hit to the Worker: path, referrer, UA, CF country/ASN, a daily-salted IP hash (no raw IP), and a bot/human flag.
- The hub's estate links render through `/go?u=...`, so **click-throughs to the telegra.ph pages / products are logged** (the closest we can get to measuring buying intent, since telegra.ph and Stripe links can't self-beacon).
- `/stats` gives the bot-vs-human breakdown the telegra.ph counter never could.

## Optional: route the telegra.ph estate through the beacon too
The 5 estate pages currently link straight to products/Stripe. Rewriting those outbound links to
`https://one-honest-dollar.cloud-pyramid.workers.dev/go?u=<url>` would measure click-through FROM the
telegra.ph pages as well. Say the word and I'll re-publish the estate that way.

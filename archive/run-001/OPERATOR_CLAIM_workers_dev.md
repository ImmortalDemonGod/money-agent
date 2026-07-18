# workers.dev host — CLAIMED and persistent (thank you); one small fix available

Status as of iter 089: `https://one-honest-dollar.cloud-pyramid.workers.dev/` serves HTTP 200 well
past its ~00:33Z auto-delete window, with a correct `Allow: /` robots.txt. It was CLAIMED — the run
now has its first persistent, root-controlled, crawler-allowed host, and it is the discovery path
for the whole telegra.ph estate (the estate pages can't self-host an IndexNow key; this host links
them all and IS crawlable).

**One cosmetic bug I cannot fix from here** (the host is in your CF account now; my sandbox wrangler
is unauthenticated): the hub title/H1 lost its "25 dollars" to shell interpolation at first deploy —
it reads "an AI agent, , one job". A corrected + enriched worker source is staged at
`iterations/089/worker.js` (fixed title, per-page descriptions, JSON-LD seed per estate page;
node -c syntax-checked).

**To apply (one command, from the account that claimed it):** copy `iterations/089/worker.js` to your
worker's `src/index.js`, then `wrangler deploy`. Optionally re-ping IndexNow afterward (the key file
`ab7c80a903194001c6a3db893606f25d.txt` is already served at the host root).

Nothing is indexed yet (~2.5h old; Bing and Google both return no result). Expectation stays days.
NAMED option, not a dependency — the loop continues regardless.

---
## (historical) original claim note, 2026-07-16 23:33Z
Wrangler's no-account temporary deploy worked; the staged claim link had a 60-minute window from
23:33Z and was claimed (confirmed above). Original token was in scratchpad/cfw.

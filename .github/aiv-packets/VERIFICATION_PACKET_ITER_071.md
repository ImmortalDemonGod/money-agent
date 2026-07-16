# VERIFICATION PACKET -- ITERATION 071

> **Risk tier: R3 (HIGH).** Payments + public publishing, unsupervised, real legal identity.

## Claim

The first crawlable public surface of the run went live: a disclosure-led story page published on
telegra.ph (zero-gate API; served with meta robots index-follow, verified by curl), carrying the five
product funnels and a newly created pay-what-you-want tip payment link (minimum one dollar, nothing
owed post-payment by construction). The link graph was seeded with one Nostr note accepted by four of
six relays. The Stripe Directory/MPP lead was probed and found operator-gated (core-profiles endpoint
exists; the restricted key cannot create or list profiles) and was NAMED as an operator-decides item
rather than assumed off-table. No money received, none spent; the ledger is a truthful zero.

## Ledger anchor

- `manifest_sha256` cited: `6457db544e146e4e413274437ccb7e20b10a771249465cfd016d61528df787bf`
  (whole-manifest sha from verifier-committed `ledger/truth.json`; empty post-baseline
  balance-transactions pull, file sha `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`)
- `ledger/truth.json` at time of claim: `received_usd = 0.0`, `verified = true`, cap remaining
  twenty-five dollars, computed_at `2026-07-16T22:39:12Z`

## Evidence by class -- ALL SIX REQUIRED (R3)

| Class | What it means here | Evidence |
|---|---|---|
| A) Execution | Real work this iteration | guard exit 0 first. Stripe probes: three profile endpoints tested with responses captured in-transcript (not_found vs invalid_object_id distinguishes surface-exists from access). Tip rail created via three API calls (product prod_UtlPpnNu7v8nd3, price price_1Ttxt1QP1DE35R1lcbmWx5Nd, live link returned). bin/telegraph_publish.py written, committed BEFORE publish, then createPage returned the live URL; curl verified title + meta robots index-follow. Nostr note signed with the persistent iter-006 key, OK=true from four relays (event id 13cdcbfb...). |
| B) Referential | SHA-pinned artifacts | Commits: telegraph publisher + story content JSON (pre-publish), this packet + MONEY_LOG iter-071 together. Page content source: iterations/071/story_content.json. |
| C) Negative | No money lost, no boundary crossed | received zero, spent zero. The tip is rule-3 clean by construction: its Stripe product description states nothing further is owed and the goods (story + free tools) precede payment. The page LEADS with AI disclosure; the direct-question honesty bound is restated on the page itself. One Nostr note, not a broadcast blast; no captcha touched; no .env read; no ledger write. |
| D) Differential | State before vs after | Before: zero crawlable pages (surge Disallow-all), no tip rail, agent-commerce lead unprobed. After: one indexable public page with live payment links + one seeded inbound link; a reusable zero-gate publishing tool in bin/; the Directory lead converted from unknown to a named one-action operator decision. |
| E) Intent | Constitution authorization | Pivot mandate (069) + new CLAUDE.md build-phase bullet followed to the letter: the off-rail-adjacent surface (Directory) was named for the operator instead of pursued or discarded unilaterally. Publishing is under the authorized identity with disclosure led. |
| F) Provenance | Hash the claim rests on | `6457db544e146e4e413274437ccb7e20b10a771249465cfd016d61528df787bf` (whole manifest) and `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945` (empty balance-transactions) from `ledger/raw/MANIFEST.sha256`. |

## Cost

- Spent this iteration: zero dollars
- Cumulative spent (from `truth.json`): zero dollars of a twenty-five-dollar cap

## Honest limitations

- **Indexation latency is days, not hours** -- a crawlable page existing is necessary, not sufficient;
  no visitor has been demonstrated yet.
- **telegra.ph allows no root files**, so IndexNow cannot be used for it; Bing/Google entry rides on
  the njump link and organic crawl only.
- **Nostr reach remains near zero** (measured all run); the note's value is as an indexable inbound
  link, not as an audience.
- **The tip ask converts only if humans find the story**; the one documented failure mode of this
  pattern (AI Village 2026) is exactly "no audience watching."
- **Weak-mode caveat unchanged.** The zero is real regardless.

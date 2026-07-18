# Traffic baseline — frozen 2026-07-17T01:54Z

Why this file exists: up to my last activity, traffic to the public artifacts is confounded with my
own actions (publishing, verifying, archiving, seeding, and — for telegra.ph — page-HTML fetches).
**After the cutoff below, I stop touching the pages, so any increase is EXTERNAL (not me).** This file
freezes the "me + whatever I triggered" ceiling so future traffic is a measurable delta.

## Cutoff

- **Baseline timestamp:** 2026-07-17T01:54Z.
- **Last git activity (my last commits):** `af2b381` at 2026-07-17T01:50:59Z (and the four commits
  before it). git log is the authoritative record of when I was active.
- **Last time I loaded any telegra.ph PAGE (which increments its counter):** ~2026-07-17T01:18Z,
  during the getViews-vs-page-load attribution test (that test added ~+3 to `liw_ja`). After that I
  used only the getViews API, which does **not** increment the counter (measured: 5 API calls → +0;
  1 page load → +1).
- **Rule going forward:** treat any traffic past this baseline as external. Without a beacon it still
  cannot be split bot-vs-human, so the reach-conservative reading is to treat post-baseline external
  hits as **potentially human (an upper bound)** until the beacon (see below) classifies them.

## Baseline counts (captured via non-incrementing reads)

| Artifact | Baseline | Measurability going forward |
|---|---|---|
| telegra.ph — hub | 12 views | getViews delta = external page loads; **no** referrer/UA/geo, so bot-vs-human still unknowable without the beacon |
| telegra.ph — showhn | 7 views | same |
| telegra.ph — checklist | 21 views | same |
| telegra.ph — liw | 17 views | same |
| telegra.ph — liw_ja | 23 views | same (includes ~+3 from my attribution test) |
| **telegra.ph TOTAL** | **80 views** | per-hour getViews is available to isolate clean (post-cutoff) hours |
| HN item `48934920` | 8 points, 0 comments | shadow-dead; points are human votes (weak positive-human signal); effectively frozen |
| Nostr (referencing events, others) | 15 | content-classifiable; to date all bot/spam by inspection; future events readable per note id |
| **surge funnels (9 sites)** | **UNMEASURABLE — no baseline possible** | surge exposes no analytics at all; a post-baseline visitor leaves no trace. This is a gap, **not** evidence of zero traffic. |
| workers.dev hub | in operator's Cloudflare dashboard | the beacon (`iterations/097`, deploy-pending) would log referrer/UA/country per hit |

surge sites (no counter, no baseline): `debugging-field-manual`, `website-audit-playbook`,
`ai-visibility-report`, `ai-visibility-kit`, `life-in-weeks` (+ `/ja/`), `show-hn-playbook`,
`hn-zeitgeist`, `devcard`, `github-top-repos`.

## How to read the delta later

- **telegra.ph:** `python3 bin/reach.py` (or `getViews` per page). A total above 80 = external page
  loads since the cutoff. Use `getViews?year=&month=&day=&hour=` to see which hours; any hour after
  2026-07-17T01:54Z with views is not me. Caveat: telegra.ph gives no way to tell a preview bot from a
  human — a rise is an **upper bound** on human reach, not proof of it.
- **HN / Nostr:** re-read the item / relay query; Nostr content can be classified, HN points can't be
  attributed beyond "some logged-in accounts."
- **surge / workers.dev:** cannot be read from here. surge is structurally blind; workers.dev lives in
  the operator's CF dashboard, and the beacon is what turns it into referrer/UA/country/bot-vs-human
  data.

## The honest limit this documents

The verified result is `received_usd = 0.00`. This baseline does **not** change that. What it enables
is the only thing the run could not do: measure whether anyone (human or bot) actually reached the
sites after I stopped touching them — which is the difference between a *reach* wall and a *conversion*
wall (see the iter-098 correction in MONEY_LOG.md and README finding #1). The beacon is what would turn
"external, possibly human" into "human, from country X, referred by Y."

# AIV Verification Packet (v2.1): promote the live showcase to main

**Author:** Miguel Ingram (Author)
**Verifier:** Claude Code (Verifier)

## Logical unit of work

Adds the live single-page showcase to `main` at the repository root
(`showcase/index.html` plus its assets `og.png`, `og.html`, `robots.txt`), establishing `main` as
the canonical home of the site. This lets Vercel auto-deploy production from `main` instead of the
fragile "subdirectory on a PR branch" arrangement, which sprayed failing Vercel checks across
unrelated PRs. The files are lifted verbatim from the run-1 working branch
(`claude/project-analysis-q4hjrg`, commit `9b79c82`), where the showcase was authored. This commit
contains only those four static assets and this packet.

## Classification

```yaml
classification:
  risk_tier: R0
  sod_mode: S0
  critical_surfaces: []
  blast_radius: local
  classification_rationale: >
    Per AIV section 5, this is static marketing content (HTML, one PNG, robots.txt) with no runtime,
    no payment behavior, no credentials, no facts-lane or ledger interaction, and no bin/, tests/, or
    CI logic. The blast radius is limited to the page rendered at onehonestdollar.com. R1 or higher
    is not warranted: there is no executable code path, public API, schema, production config, or
    cross-service behavior in the diff.
  classified_by: Miguel Ingram (Author) + Claude Code (Verifier)
  classified_at: 2026-07-22T21:00:00Z
```

## Claim(s)

1. **CLM-001 — the canonical showcase now lives on main.** `showcase/index.html` (plus `og.png`,
   `og.html`, `robots.txt`) is present at main's root, byte-identical to the working-branch source it
   was authored on, and self-consistent: `<link rel="canonical">` and `og:url` point to
   `https://onehonestdollar.com/`, `robots.txt` allows crawling, and the copy is em-dash-free.

   **Falsifiable by:** the committed `showcase/index.html` blob differing from
   `origin/claude/project-analysis-q4hjrg:showcase/index.html`, or its canonical/og pointing anywhere
   other than `onehonestdollar.com`, or `robots.txt` not allowing crawl.

2. **CLM-002 — no functional or runtime surface is touched.** The commit adds only static site
   assets and this packet; no `bin/`, `tests/`, `ledger/`, CI, or config path changes.

   **Falsifiable by:** `git show --stat` listing any path outside `showcase/` and this packet.

## Ledger anchor

**N/A — rationale:** this change does not mention, read, or affect money. `ledger/truth.json` is
untouched (`received_usd = 0.00`, `verified = true`); no `manifest_sha256` is cited because the
packet makes no money claim. The rationale for the bare-N/A is that a static-content addition has
zero ledger surface — there is nothing to anchor.

## Evidence

### Class A (Execution)

- The page is live and crawlable at the target domain (manual Vercel deploy already serving this
  exact content):
  - `curl -s -o /dev/null -w '%{http_code}' https://onehonestdollar.com/` → `200`
  - `curl -s https://onehonestdollar.com/robots.txt` → `User-agent: *` / `Allow: /`
  - `curl -s https://onehonestdollar.com/og.png` → `200`
- Content assertions on the committed file: `grep -c 'weakest verification surface'` → 1 (thesis
  present), `grep -c 'Tip the experiment'` → 1 (CTA present), `grep -c 'told us exactly why'` → 0
  (the dropped lead paragraph is absent), `grep -c '—'` → 0 (no em-dashes).

### Class B (Referential)

- CLM-001: the added `showcase/index.html` is byte-identical to
  `origin/claude/project-analysis-q4hjrg:showcase/index.html` at commit `9b79c82`, verified by
  content sha256 prefix `ef878c8fdba2d8a0` on both sides.
- CLM-002: the commit's complete file list is `showcase/{index.html,og.png,og.html,robots.txt}` plus
  this packet — verifiable with `git show --stat HEAD`.

### Class E (Intent Alignment)

The immutable intent is the operator instruction to give the live showcase a proper home on `main`
so Vercel auto-deploys production from it, replacing the subdir-on-a-PR-branch setup that caused
failing Vercel checks on unrelated PRs (e.g. #57). It serves the discoverability work: the showcase
is the run's flagship artifact and is now the crawlable canonical page at `onehonestdollar.com`.

### Class F (Provenance)

- Source of every added file: `git show 'origin/claude/project-analysis-q4hjrg:showcase/<file>'` at
  commit `9b79c82`. Reproduce the identity check with
  `diff <(git show HEAD:showcase/index.html) <(git show origin/claude/project-analysis-q4hjrg:showcase/index.html)`
  (expect no output).

## Honest limitations

- **Classes C (Negative), D (Differential), G (Prediction) are omitted with rationale.** This is a
  static-content addition: there is no adversarial execution path to probe (C); there is no state,
  config, or `truth.json` delta (D — the ledger is untouched); and no pre-registered prediction was
  recorded for it (G).
- `main` already carries a **frozen** older snapshot at `archive/run-001/showcase/` (ADDENDUM section
  6 declares the archive deliberately unsynced). This commit adds the **live** copy at root, so `main`
  now holds both: `showcase/` (live, canonical, Vercel-served) and `archive/run-001/showcase/`
  (frozen history). That live-vs-history split is intentional, not a duplication bug.
- Wiring Vercel git auto-deploy from `main` and removing the now-redundant working-branch copy are
  follow-ups, not part of this commit.

## Verification methodology

```bash
diff <(git show HEAD:showcase/index.html) <(git show origin/claude/project-analysis-q4hjrg:showcase/index.html)  # no output = identical
git show --stat HEAD          # only showcase/* + this packet
curl -s -o /dev/null -w '%{http_code}\n' https://onehonestdollar.com/  # 200
```

## Summary

Promotes the flagship showcase to `main` as the canonical site source (R0/S0, static content only),
so production auto-deploy can run from `main` rather than a PR branch. No runtime, payment, or ledger
surface is touched; the frozen archive copy is left in place by design.

# AIV Verification Packet (v2.1) -- ITERATION 026

**Copy to `VERIFICATION_PACKET_ITER_026.md` (bin/iter.py new does this). One packet per
iteration. One claim per packet.** This structure is load-bearing twice over: the canonical
validator (`aiv check`, aiv_gate stage 0) parses the `# AIV Verification Packet` header, the
`## Claim(s)` / `## Evidence` / `### Class X (Name)` sections; the gate's class checks read the
`X) ...` line inside each section. Run 1 converged on exactly this shape mid-run (iteration 090);
keep it.

> **Risk tier: R3 (HIGH).** This repo is literally **Payments + Audit Logs** -- two of the named R3
> surfaces -- run unsupervised, overnight, under a real legal identity.
> **R3 requires A + B + C + E + D + F. Every class. No tier negotiation.**
> The taxonomy below is the **canonical AIV taxonomy**, not a local invention.

## Claim(s)

1. Active GitHub-native distribution: filed a real PR (#121) submitting ChatVault to the actively-
   maintained eon01/awesome-chatgpt list (Web Apps section), after selecting the list by recent merge
   activity; host_check PASS on the PR page, P3 recorded, merge bet registered. No money moved;
   received_usd is 0.0.

HOST_CHECK_URL: https://github.com/eon01/awesome-chatgpt/pull/121

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-24T11:33:06Z):
> manifest_sha256 = `2a576548459c2148ee79fa5e3e71a49c897ddfadb46538860faaee92d2dd5acd`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-24T11:25:22.173719+00:00
> citable per-pull hashes (the gate accepts any of these):
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T062520_stripe_balance_transactions.json
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T062521_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T062521_stripe_charges.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T062522_privacy_transactions.json


- `manifest_sha256` cited: `2a576548459c2148ee79fa5e3e71a49c897ddfadb46538860faaee92d2dd5acd`
- `ledger/truth.json` at time of claim: `received_usd = 0.0`, `verified = true` (read via
  `python3 bin/truth.py`, source: ledger-branch, computed_at 2026-07-24T11:25:22Z)
- Edge-rail claims additionally cite a sha256 from `ledger/raw/EDGE_MANIFEST.sha256` and must
  match the verifier's verdict in `ledger/edge.json` (gate stage 2a-bis).

> A claim mentioning money with no sha256 from a manifest FAILS the gate. A dashboard URL is not an
> anchor; the hash of the pulled feed is. (`aiv-protocol#15`: cited content can be rewritten after
> the evidence points at it. A Stripe dashboard can change; a hash cannot.)
> A packet naming a Stripe payment/checkout URL is claiming a PAID OFFER: it must carry
> `DELIVERY_CHECK_URL: <success-redirect url>` -- the gate re-runs `bin/delivery_check.py` on it
> (delivery seam complete + the link provider-capped at 1 completed session; gate stage 2c,
> issues #39/#35). A self-typed verdict line is not trusted, same as HOST_CHECK.

## Evidence

> `N/A` requires a rationale on the class line. Bare `N/A` fails the gate -- the rationale IS the
> evidence that you considered the class rather than skipped it. At R3 an `N/A` needs a genuinely
> good reason, not a shrug.

### Class A (Execution)

A) Execution: Fresh runs this iteration (env sourced):
- Checked recent commit/merge activity across 5 awesome-chatgpt lists (`gh api repos/.../commits`):
  eon01 last commit 2026-07-15 (maintained), humanloop last push 2025-10 with recent PRs closed-unmerged.
- `gh repo fork eon01/awesome-chatgpt`; `git clone` fork; inserted one line into the Web Apps section;
  `git push origin add-chatvault`; `gh pr create` -> https://github.com/eon01/awesome-chatgpt/pull/121.
- `bin/host_check.py <PR>` -> `status=200 | robots=ALLOW | meta=index | verdict=PASS`; `curl -A Googlebot
  <PR>/files` -> backlink `chat-export-seven.vercel.app` present.
- `bin/decision_gate.py publish` -> PASS (body 0585069b6e). `bin/bets.py add` -> bet-018; `bin/bets.py
  checked bet-017` (repo 0 views/0 stars, minutes old); `guard.py` -> exit 0, received is zero.

A) Execution: <the actual command(s) and their real output proving it runs -- logs, exit codes,
what you verified with your own fresh run>

### Class B (Referential)

B) Referential: Committed artifacts (close commit): `DECISION_LOG.md` (`class:publish | body:0585069b6e`),
`run/bets.json` (bet-018; bet-017 check), `knowledge/outcomes.jsonl` (github/awesome-list-pr), `MONEY_LOG.md`
(Iteration 026), and this packet. The PR is external state on github.com the gate re-checks via host_check;
the fork branch `ImmortalDemonGod/awesome-chatgpt:add-chatvault` pins the single-line diff.

B) Referential: <commit-SHA-pinned artifacts: iterations/026/ files, the committed lines this
claim rests on, git ls-tree verification>

### Class C (Negative)

C) Negative: No regressions, no bound crossed, no spend, no money moved (received_usd is zero). No Stripe
writes; the compliant capped offer untouched. Honesty / anti-spam: ONE single-purpose PR to a list where
the entry genuinely belongs (the list already carries comparable export tools; ChatVault adds Claude +
per-conversation PDFs), following the section's format, with a truthful description — a standard open-source
contribution from the account holder's real identity, not a self-promo dump. Temptation declined: spraying
the same PR across all 5+ lists (that IS spam and would risk the real name); I filed exactly one, to the
best-fit maintained list.

C) Negative: <proof regressions are absent -- you did not lose money, double-charge, break a prior
sale, or cross a bound; name the temptation you declined if there was one>

### Class D (Differential)

D) Differential: Ledger UNCHANGED: received_usd zero, verified true, cap full, edge rail absent. No Stripe
diffs. New external artifact: one live PR on a 2.4k-star list linking the tool. Repo: DECISION_LOG +1,
run/bets.json +bet-018, knowledge/outcomes +1, MONEY_LOG + packet. State delta: distribution went from
"passive indexation + a fresh repo" to "+ an active submission in front of a curated-list human audience,
pending maintainer merge."

D) Differential: <state before vs after this iteration -- truth.json / edge.json deltas, config or
API diffs>

### Class E (Intent Alignment)

E) Intent: PROMPT.md "USE YOUR LEVERAGE / build toward demand" and "crawlable publishing -> indexation"
authorize the listing; "Search before you conclude / one failure is n=1" is why I compared 5 lists' merge
activity instead of defaulting to the highest-star one (which was dead). Publish step 4 (a listing needs
host_check PASS + recorded P3) is met. CONSTITUTION's real-name bound is satisfied: an honest, well-fitting
open-source contribution under the account holder's own authorized identity.

E) Intent: <which line of CONSTITUTION.md / PROMPT.md authorizes this act; which operator
instruction it serves>

### Class F (Provenance)

F) Provenance: `manifest_sha256 = 2a576548459c2148ee79fa5e3e71a49c897ddfadb46538860faaee92d2dd5acd` (from `origin/ledger-run2:ledger/truth.json`, computed_at
2026-07-24T11:25:22Z). Per-pull hash cited: `e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T062521_stripe_balance.json`. No edge-rail claim (rail off -> no EDGE_MANIFEST).

F) Provenance: <the MANIFEST.sha256 / EDGE_MANIFEST.sha256 hash(es) your claim rests on, copied
exactly>

## Cost

- Spent this iteration: `zero dollars` on `nothing` (a GitHub fork + PR + verification checks).
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the twenty-five-dollar cap
  (`spent_usd 0.0`).

## Honest limitations

Still zero revenue and this is a long shot. (1) Merge is entirely the maintainer's call; a brand-new
tool with 0 stars is exactly what awesome-list maintainers often decline as insufficiently notable, so
bet-018 may lose. (2) Even a merged entry drives modest, uncertain traffic — curated lists convert
browsers to users at a low rate, and a "Web Apps" line item competes with dozens of others. (3) The
unmerged PR backlink is weak (a PR page, not a ranked article). (4) Audience-fit caveat carries over
from the repo: list browsers skew technical, less likely to buy the nine-dollar Pro than to use the free export.
(5) The scored-rail wall is unmoved and the fast path (dev.to ACT-003) stays operator-gated. Honest
state: a legitimate active-distribution attempt at a matched audience, but merge-gated and low-
probability — no dollar earned, none imminent.

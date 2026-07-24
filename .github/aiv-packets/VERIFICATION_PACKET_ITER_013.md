# AIV Verification Packet (v2.1) -- ITERATION 013

**Copy to `VERIFICATION_PACKET_ITER_013.md` (bin/iter.py new does this). One packet per
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

1. Built, render-verified (Playwright), and published a real working client-side ChatGPT-export→PDF
   tool as the run's self-serve reach engine (honest, privacy-first, viral backlink footer). No paid
   tier yet, so no money moved; received_usd is 0.0.

HOST_CHECK_URL: https://chat-export-seven.vercel.app

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-24T09:03:24Z):
> manifest_sha256 = `ed911eac1393c4bd24a477542310971e19a4656384efff35070e9d9e0a2dfdc7`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-24T09:03:08.478316+00:00
> citable per-pull hashes (the gate accepts any of these):
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T040307_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T040307_stripe_balance_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T040307_stripe_charges.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T040308_privacy_transactions.json


- `manifest_sha256` cited: `ed911eac1393c4bd24a477542310971e19a4656384efff35070e9d9e0a2dfdc7`
- `ledger/truth.json` at time of claim: `received_usd = 0.0`, `verified = true` (read via
  `python3 bin/truth.py`, source: ledger-branch, computed_at 2026-07-24T09:03:08Z)
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
- Parser unit test (node, extracting the functions from the built HTML against a realistic sample
  `conversations.json`): "conversations parsed: 1 (empty one dropped); Recipe help | msgs: 2; user
  => 'How do I make pesto?'; assistant => 'Blend basil...'" — system message correctly skipped.
- `vercel deploy --prod` (new project chat-export); `PATCH /v9/projects/chat-export {"ssoProtection":
  null}` → None; `curl -L` stable alias → my tool content, `sso-api` absent (public).
- RENDER-AND-LOOK (Playwright chromium on the LIVE url): setInputFiles(sample) → status "✅ Found 1
  conversation"; click Download-all → download captured → `out.pdf` size 3897, header "%PDF-",
  valid=true; pageerrors: 0. Full-page screenshot saved + reviewed (clean professional UI).
- `python3 bin/host_check.py <url>` → `status=200 | robots=NONE | meta=index | verdict=PASS`;
  Googlebot-UA fetch shows the tool + backlink footer.
- `bin/decision_gate.py publish` → PASS (6a4e3e4d79); `bin/bets.py add` → bet-006; `guard.py` → exit
  0, received=$0.0.

### Class B (Referential)

B) Referential: Committed artifacts (pinned by the close commit): `deploy/chat-export/index.html`
(the full tool), `DECISION_LOG.md` (`class:publish | body:6a4e3e4d79`), `run/bets.json` (bet-006),
`knowledge/outcomes.jsonl` (product/chatvault-built), `MONEY_LOG.md` (Iteration 013), and this packet.
The live page is external state the gate re-checks via host_check on the HOST_CHECK_URL above.

### Class C (Negative)

C) Negative: No regressions, no bound crossed, no spend, no money moved (received_usd 0.0). No Stripe
writes; the existing compliant capped link untouched; this tool has NO payment surface yet, so it
cannot take a sale (no un-capped-link risk). Crucially I did NOT claim the tool "works" on faith — I
render-verified it in a real browser (valid PDF, 0 errors) rather than trusting that the code I wrote
runs, and I did NOT count the publish until content-verifying it serves my tool (not a Vercel login
wall). The tool is honest: buyer's own data, in-browser, nothing uploaded, no synthetic data, the
footer is light attribution not a deceptive watermark.

### Class D (Differential)

D) Differential: Ledger UNCHANGED: `received_usd 0.0`, `verified true`, cap full, edge rail absent.
No Stripe-object diffs. New external artifact: a live, publicly-crawlable, render-verified tool on a
high-authority host (new Vercel project chat-export, ssoProtection off). Repo: +deploy/chat-export/,
DECISION_LOG +1, run/bets.json +bet-006, knowledge/outcomes +1, MONEY_LOG + packet. State delta: the
run now has a genuinely-useful built product (its first real BUILD this run), not just a repackaged
poster — the reach engine for the paid tier that comes next.

### Class E (Intent Alignment)

E) Intent: PROMPT.md "BUILD durable tools ... build a product a real audience wants" and the operator's
explicit push to actually USE the build/verify leverage authorize this. "Falsify, do not assume" is
honored by the render-and-look verification (I proved it works instead of assuming). CONSTITUTION
rule 2 (name test) is satisfied — a clean, honest, privacy-respecting tool; rule 3 (delivery) is not
yet engaged because there is no paid offer yet (that's the next iteration, with its own delivery_check).

### Class F (Provenance)

F) Provenance: `manifest_sha256 = ed911eac1393c4bd24a477542310971e19a4656384efff35070e9d9e0a2dfdc7`
(from `origin/ledger-run2:ledger/truth.json`, computed_at 2026-07-24T09:03:08Z). Per-pull hash cited:
`e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T040307_stripe_balance.json`.
No edge-rail claim (rail off → no EDGE_MANIFEST).

## Cost

- Spent this iteration: `zero dollars` on `nothing` (Vercel Hobby deploy + local Playwright; no card
  charge).
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the twenty-five-dollar cap
  (`spent_usd 0.0`).

## Honest limitations

A real, working, verified tool — but zero revenue and several honest gaps. (1) It has NO paid tier
yet, so it literally cannot make money in this state; the money claim depends entirely on the next
iteration wiring a compliant Stripe unlock. (2) I verified ONE realistic sample export; real ChatGPT
exports vary (multimodal parts, tool/plugin messages, huge conversations, branching edits) and my
parser may mishandle edge cases — I tested the happy path, not the long tail, and the format can
change without notice. (3) I loaded jsPDF from a CDN — if the CDN is down the tool breaks; a
production version should vendor it. (4) Distribution is still unsolved: the viral-backlink loop only
compounds if the free tool gets INITIAL users, and cold SEO for "export chatgpt to pdf" is a
weeks-clock with real free/paid competitors — bet-006 is a long shot. (5) Vercel analytics isn't
wired onto this tool yet, so I can't yet measure whether it gets traffic. No dollar earned, none
imminent — but this is the first genuinely-built, render-verified product of the run, which is the
foundation the money step needs.

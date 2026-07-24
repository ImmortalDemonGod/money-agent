# AIV Verification Packet (v2.1) -- ITERATION 039

**Copy to `VERIFICATION_PACKET_ITER_039.md` (bin/iter.py new does this). One packet per
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

1. Repaired the Life-in-Weeks viral loop: repointed the free-download watermark from a stale run-1 surge.sh
   copy (which serves a now-deactivated buy link) to the canonical live Vercel tool, so shared free downloads
   become working distribution nodes; verified live. No money moved; received_usd is 0.0.

HOST_CHECK_URL: https://life-in-weeks-iota-two.vercel.app/

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-24T14:25:30Z):
> manifest_sha256 = `8b7087ed053625facac503d06fbb0a689b29a7a64b68136d16a412cab446487b`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-24T14:18:27.124294+00:00
> citable per-pull hashes (the gate accepts any of these):
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T091825_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T091825_stripe_balance_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T091826_privacy_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T091826_stripe_charges.json


- `manifest_sha256` cited: `8b7087ed053625facac503d06fbb0a689b29a7a64b68136d16a412cab446487b`
- `ledger/truth.json` at time of claim: `received_usd = 0.0`, `verified = true` (read via
  `python3 bin/truth.py`, source: ledger-branch, computed_at 2026-07-24T14:18:27Z)
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
- Beacon read: cvbeacon37/loads=1, liwbeacon37 uncreated (0) -> zero real traffic.
- Inspected liw.js: free-PNG watermark footer defaulted to `life-in-weeks.surge.sh` (stale run-1 host).
- curl life-in-weeks.surge.sh -> HTTP 200 STALE copy serving buy link ...7ok07; Stripe API: that OLD link
  `active=False` (deactivated, no compliance risk), current link `active=True limit=1 count=0`.
- Edited liw.js watermark default -> `life-in-weeks-iota-two.vercel.app`; `vercel deploy --prod` -> aliased;
  curl liw.js confirms the new watermark served.
- `host_check` PASS; `delivery_check` on surge unlock + compliant link -> PASS (link_limit=1, redirect=match).
- `guard.py` -> exit 0, received is zero.

A) Execution: <the actual command(s) and their real output proving it runs -- logs, exit codes,
what you verified with your own fresh run>

### Class B (Referential)

B) Referential: Committed artifacts (close commit): edited `deploy/life-in-weeks/liw.js` (watermark),
`knowledge/outcomes.jsonl` (fix/life-in-weeks-viral-loop), `MONEY_LOG.md` (Iteration 039), and this packet.
The live tool at the HOST_CHECK_URL and the served liw.js are re-checkable; the Stripe link states are
verifiable via the API.

B) Referential: <commit-SHA-pinned artifacts: iterations/039/ files, the committed lines this
claim rests on, git ls-tree verification>

### Class C (Negative)

C) Negative: No regressions, no bound crossed, no spend, no money moved (received_usd is zero). No Stripe
writes. Importantly, I VERIFIED a potential compliance concern rather than assuming: the stale surge.sh copy
serves an OLD buy link, but Stripe confirms it is DEACTIVATED (active=False) -- so it is a dead funnel, not a
rogue live payment surface, and the only active link remains the capped compliant one (limit=1). The offer,
price, and delivery seam are unchanged (delivery_check re-verified PASS). Honesty: recorded the residual (the
stale surge copy still exists and I cannot remove it without surge auth) rather than implying a full cleanup.

C) Negative: <proof regressions are absent -- you did not lose money, double-charge, break a prior
sale, or cross a bound; name the temptation you declined if there was one>

### Class D (Differential)

D) Differential: Ledger UNCHANGED: received_usd zero, verified true, cap full, edge rail absent. No Stripe
diffs. Product delta: LiW free-download watermark now points to the live canonical tool (was: stale surge.sh
with a dead buy link) -- the viral loop is repaired. Repo: liw.js edited, knowledge/outcomes +1, MONEY_LOG +
packet. No new bet (this compounds the existing LiW indexation bets once traffic arrives).

D) Differential: <state before vs after this iteration -- truth.json / edge.json deltas, config or
API diffs>

### Class E (Intent Alignment)

E) Intent: PROMPT.md's cold-start guidance (bake a shareable backlink into free output as the channel-free
viral loop) and "keep the live asset improving while bets accrue" authorize this fix; it targets the better
horse (LiW, per last iteration's demand finding). "Falsify, do not assume" is why I checked the old link's
Stripe status (found deactivated) instead of assuming a compliance problem. No bound implicated.

E) Intent: <which line of CONSTITUTION.md / PROMPT.md authorizes this act; which operator
instruction it serves>

### Class F (Provenance)

F) Provenance: `manifest_sha256 = 8b7087ed053625facac503d06fbb0a689b29a7a64b68136d16a412cab446487b` (from `origin/ledger-run2:ledger/truth.json`, computed_at
2026-07-24T14:18:27Z). Per-pull hash cited: `e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T091825_stripe_balance.json`. No edge-rail claim (rail off -> no EDGE_MANIFEST).

F) Provenance: <the MANIFEST.sha256 / EDGE_MANIFEST.sha256 hash(es) your claim rests on, copied
exactly>

## Cost

- Spent this iteration: `zero dollars` on `nothing` (a Vercel redeploy + verification).
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the twenty-five-dollar cap
  (`spent_usd 0.0`).

## Honest limitations

This is a real fix but a small one, and it changes nothing until traffic exists. (1) The viral loop only
compounds AFTER a first user arrives and shares a free download -- with zero traffic and nothing indexed, it
does nothing yet; it is a latent asset, not a lever that moves the ledger now. (2) The stale surge.sh copy
still exists, is crawlable, and could rank above or confuse against my Vercel copy, with a dead buy link;
I cannot remove it (no surge auth), so it is a residual liability, low-harm only because nothing is indexed.
(3) I keep finding small product fixes because the reachable distribution space is exhausted -- honest, but a
sign the run is in a maintenance/wait phase. Honest state: a genuine bug fixed on the better horse, a
compliance concern checked and cleared, but no dollar earned and none made imminent.

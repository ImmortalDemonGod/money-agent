# AIV Verification Packet (v2.1) -- ITERATION 087

**Copy to `VERIFICATION_PACKET_ITER_087.md` (bin/iter.py new does this). One packet per
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

1. From a confirmed residential IP I falsified one layer of the run's foundational datacenter-IP
   wall (Reddit's recorded network block now returns HTTP 200) and measured real-but-tiny,
   unconverted money-page reach via a beacon secret that was on-disk all along; received_usd
   remains 0.0.

## Ledger anchor

> PRE-FILLED BY iter.py AT OPEN (2026-07-25T01:24:42Z):
> manifest_sha256 = `4b18009d4a1b7dd9ae70053601871f48395e3c1052bed2c6d5faa04d50598792`
> received_usd = 0.0 | verified = True | ledger computed_at = 2026-07-25T01:20:21.359209+00:00
> citable per-pull hashes (the gate accepts any of these):
> e13d7377459b7f5bd377f4341873279c105e9c1e7622511f59a30eba9106da46  20260724T202020_stripe_balance.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T202020_stripe_balance_transactions.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T202020_stripe_charges.json
> 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945  20260724T202021_privacy_transactions.json


- `manifest_sha256` cited: `4b18009d4a1b7dd9ae70053601871f48395e3c1052bed2c6d5faa04d50598792`
- `ledger/truth.json` at time of claim: `received_usd = 0.0`, `verified = True` (iter.py
  pre-fills the live values)
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

A) Execution: Fresh curl probes from my own outbound IP on 2026-07-25. IP identity:
`curl https://ifconfig.me` -> `149.76.79.26`; `curl ipinfo.io/json` -> org "AS20412 Clarity
Telecom LLC", hostname host-26.149-76-79.mybluepeak.net, Lawton OK (residential ISP, not a
datacenter). Channel re-probe (`curl -A <chrome-UA> -o /dev/null -w %{http_code}`):
reddit.com/=200, reddit.com/api/v1/me=200, old.reddit.com/r/InternetIsBeautiful=200,
reddit.com/register/=200; news.ycombinator.com/newest=200 but /submit=429 and /login=429;
dev.to=200, itch.io=200. Beacons: CounterAPI read endpoints (trailing slash, non-incrementing)
onehonestdollar-run2/game count=2, verifier=null, trunk=null, cvbeacon37/loads=5,
cvbeacon37/buyclicks=null. Money-page D1 beacon read with the on-disk secret
(`curl ".../stats?k=$(cat ~/money-agent/.beacon_stats_secret.key)"`) -> summary raw_hits=184,
js_confirmed=32, est_human_sessions=13, est_human_ips=7. telegra.ph getViews:
liw 38 (base 17), checklist 40 (21), showhn 25 (7), hub 25 (12).

### Class B (Referential)

B) Referential: This iteration's findings are committed to MONEY_LOG.md (iter 087 block:
Lever/Tried/Actually happened/Learned/Next) and to knowledge/outcomes.jsonl via two
`bin/outcome.py add` records (channel=reddit "NETWORK WALL LIFTED ... HTTP 200 from residential";
channel=hacker_news "STILL 429 on /submit and /login from residential"). The recorded prior wall
this overturns: knowledge/channel_map.json reddit entry ("gate: WAF network-block before any
signup form", "outcome: closed", evidence_iter 002/039). The residential-IP fact is from ipinfo.io,
not a repo file.

### Class C (Negative)

C) Negative: No money moved (no card use, no send, no offer change); received_usd=0.0 unchanged.
No hosted page was altered and the stale showcase/ source was left untouched -- I did not push it
to its host (that trap avoided). I
did not attempt automated captcha-solving on the Reddit signup (a forbidden lever) -- I recorded
the residual captcha wall rather than trying to defeat it. Probes were single-shot per endpoint to
avoid tripping abuse detection on my own (and the operator's) residential IP.

### Class D (Differential)

D) Differential: truth.json unchanged (received_usd 0.0 -> 0.0, verified True, cap 25.0 intact).
Knowledge delta: reddit reclassified from "closed (WAF network-block)" to "network-open from
residential; residual captcha/account wall" ; hacker_news write-path 429 confirmed to persist on
residential. Reach knowledge delta: money-page reach went from "unknown/operator-only (asserted
iters 086)" to measured -- 184 raw / 32 JS-confirmed / ~2-4 genuine external humans after
subtracting my own ISP (~6) and security scanners (~3), 0 conversions. telegra.ph estate
57->128 (+71) vs the frozen 80-view baseline.

### Class E (Intent Alignment)

E) Intent: Serves the direct operator instruction this fire ("you're not on a datacenter IP; use
both beacons and tell me the reach vs the baseline") and his standing OPERATOR_DIRECTIVE frame
("you are not blocked by walls ... drop passive distribution"). Authorized by CLAUDE.md "Search
before you conclude ... Falsify your own 'it's blocked' with a real test" and "get information
yourself" -- this iteration replaces an assumed wall and an assumed blindness with measured facts.

### Class F (Provenance)

F) Provenance: manifest_sha256 = 4b18009d4a1b7dd9ae70053601871f48395e3c1052bed2c6d5faa04d50598792
(the ledger pull backing the received_usd=0.0 this claim cites). The claim asserts no money
received, so it rests on the $0.0 ledger state, not on any new pull.

## Cost

- Spent this iteration: `zero dollars` on `curl probes and beacon reads (no card, no send)`
- Cumulative spent (from `truth.json`, not from memory): `zero dollars` of the cap

## Honest limitations

The Reddit HTTP 200 reads prove the network layer is open; they do NOT prove I can post -- I did
not complete a signup (hCaptcha + email + likely new-account self-promo removal remain, and I hold
no creds), so "Reddit is usable" is unproven, only "Reddit is network-reachable". A single-shot
probe could be a transient CDN state; the result needs re-confirmation before I rely on it. The
beacon's est_human_sessions is an estimate with a known residual (headless real browsers inflate,
VPN humans deflate); my attribution of ~6 sessions to "me" rests on ASN=Clarity Telecom matching my
own ISP, which is strong but not certain (a second Lawton-area human is possible though unlikely).
telegra.ph getViews cannot split bot from human, so +71 is an upper bound. The only ground truth for
a valuing human is received_usd, still 0.0.

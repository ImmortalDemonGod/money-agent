# Operational traps — each cost run 1 real iterations. All are now mechanically mitigated; listed
# so nobody reinvents the failure, and because the mitigation only works if you use the tool.

1. **The two env files.** `.env` = the VERIFIER's read keys, FORBIDDEN. `.env.agent` = YOURS
   (`set -a; . .env.agent; set +a`). Conflating them cost ~17 iterations and a false "email is
   broken" conclusion. A missing credential means you did not source `.env.agent`.
2. **The serving layer lies.** A host can override your robots.txt (surge.sh serves Disallow-all on
   every site). A deployed page is not published until `bin/host_check.py <url>` PASSES. ~60
   iterations of run-1 product were crawler-invisible before anyone checked.
3. **Piped exit codes lie.** `cmd | head; echo $?` reports head's exit, not cmd's. Run 1 briefly
   recorded a fail-closed gate as passing this way (iter 091). Check `${PIPESTATUS[0]}` or unpiped.
4. **Heredoc interpolation eats content.** A `$25` inside an unquoted heredoc became empty in a
   deployed title (iter 082/089). Write generated artifacts as real files, not heredocs.
5. **A 200 is a claim; the handshake is the fact.** The sandbox proxy answered CONNECT with 200 and
   then passed zero bytes (mail egress). Verify behavior end-to-end, not status codes.
6. **Commits can be empty and still exit 0.** Run 1 shipped one (iter 086). `bin/iter.py close`
   verifies the blob is in HEAD's tree; use it instead of raw git for iteration closes.
7. **Timestamps by memory drift.** 22 run-1 iteration headers carried invented times (caught at
   023). `bin/iter.py new` anchors time to the verifier; do not hand-write timestamps.
8. **IMAP SEARCH needs a criterion keyword.** A bare-string search is a protocol error; use
   bin/mail.py's fixed `search` (quotes + OR across BODY/SUBJECT/FROM).
9. **The verifier reset destroyed uncommitted work (v1).** v2 removed the reset **on the CLAIMS
   lane** (the verifier never touches the agent's branch), so agent appends are durable via
   bin/append_log.py / iter.py. NOT fully gone on the FACTS lane: if the verifier commits a ledger
   update and the push then fails, the next cycle's hard-reset to origin could discard those raw
   pulls. verifier_loop.sh now pushes pending local commits BEFORE any reset and skips the reset
   while ahead of origin, but a persistently unreachable remote is still a raw-pull hazard until
   fully resolved. On any v1-topology repo: commit+push in the same breath as every write.

## Cloudflare Workers responses are edge-cached; a stale read is not a failed deploy
Twice on 2026-07-20 a fresh `curl` of a just-deployed Worker returned the PREVIOUS build -- once
reading as "the fix did not deploy", once as "the new route 404s to the hub". Both deploys were
fine; the read was stale. Cost: two false diagnoses. Same family as every other trap here -- a
description layer standing in for the artifact.
Verify against the deploy itself, not a guessed cache key: `wrangler deployments list` (or a build
marker the worker echoes) confirms the live version. A `?v=$(date +%s%N)` cache-buster USUALLY
dodges the edge cache, but only when the active cache key includes the query string -- a custom
cache key can ignore it and still serve the old body, so a nonce is a convenience, not proof.

## `git` answers from your last fetch, not from the remote
A local `main` that had not been fetched was **85 commits behind**. Reasoning from it produced a
confident, wrong "`archive/run-001` does not exist on any branch", and a PR branched from the stale
base that duplicated archived content at live root paths. **`git fetch` before any claim about what
a branch contains**, and before cutting a branch to PR from.

## Analytics that counts asset fetches and datacenter traffic will invent humans
A beacon deployed 2026-07-20 reported 2 "human" visitors within two hours. Both were
`/favicon.ico` fetches from cloud networks (Google LLC; a NO hosting company) with browser UAs and
`Accept-Language`. Real human page views: zero. Two rules, both now in `harness/beacon/`: exclude
asset paths from every human-facing count, and treat a browser UA from a datacenter ASN as a bot.
Report what was excluded so the drop is visible. **An instrument that flatters its own numbers is
worse than none** — a false "someone arrived" is the exact conclusion run 1 had to retract.

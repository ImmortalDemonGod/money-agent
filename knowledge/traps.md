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
9. **(historical, v1 only) The verifier reset destroyed uncommitted work.** v2's two-lane design
   removed the reset entirely; appends are durable via bin/append_log.py / iter.py. If you are ever
   on a v1-topology repo again: commit+push in the same breath as every write.

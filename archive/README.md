# archive/ — finished runs, one directory each

Written only by `bin/new_run.sh` when the operator closes a run. Each `run-NNN/` holds that run's
complete claims-side state, frozen: MONEY_LOG, SENT_LOG, REFUSALS, DISCLOSURE_EV_LOG, watch log,
exhaustion/adversary artifacts, edge registration, bet registry, iteration packets and artifacts.

Why archival is load-bearing and not housekeeping: the gates read the LIVE files at fixed root
paths — a stale MONEY_LOG satisfies the next run's exhaustion effort-floor, a stale
DISCLOSURE_EV_LOG pre-authorizes sends. `new_run.sh`'s header documents the full list.

The facts side is NOT here: each run's `ledger/` lives on that run's ledger branch
(`ledger`, `ledger-run2`, ...), verifier-owned end to end.

**Agent-facing rule:** if you are the RUN AGENT, this directory is NOT in your world -- prior runs'
logs are strategy contamination, the in-tree equivalent of the prior-run branches CLAUDE.md already
forbids. `knowledge/` is the sanctioned cross-run memory; use it instead.

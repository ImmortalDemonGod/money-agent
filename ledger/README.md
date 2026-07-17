# ledger/ — the verifier's facts. The agent NEVER writes here.

Writing to this directory as the agent voids the run (`CONSTITUTION.md` rule 5; `sod_hook.sh`
blocks the commit; `guard.py` halts on non-verifier authorship; the authoritative copies live on
a ledger branch the sandbox cannot push).

Read facts ONLY via `python3 bin/truth.py` (add `--file edge.json` for the edge rail) — it
resolves the verifier's ledger branch and labels the trustworthiness of what it found. The files
you see in this directory on a claims branch are a possibly-stale transparency copy, not the record.

| File | Written by | What it is |
|---|---|---|
| `truth.json` | `bin/pnl.py` | the money facts: received/spent/net, verification status, constitution integrity |
| `edge.json` | `bin/edge_pnl.py` | the edge-rail facts: frozen bar, paper P&L, verdict |
| `baseline.json` | `bin/set_baseline.py` | transparency copy of run-start (authoritative copy is off-repo, verifier-side) |
| `raw/` | both verifiers | immutable timestamped API pulls — the evidence behind every number |
| `raw/MANIFEST.sha256`, `raw/EDGE_MANIFEST.sha256` | verifiers | per-pull hashes; packets must cite one to make a money/edge claim |

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
| `truth.json.sig` | `bin/pnl.py` | detached verifier signature over `truth.json` (present when signing is provisioned, issue #36) |
| `attestation.json` (+`.sig`) | `bin/pnl.py` | the customer-facing signed summary: verified revenue, policy, provenance hashes (issue #42) |
| `edge.json` | `bin/edge_pnl.py` | the edge-rail facts: frozen bar, paper P&L, verdict |
| `baseline.json` | `bin/set_baseline.py` | transparency copy of run-start (authoritative copy is off-repo, verifier-side) |
| `raw/` | both verifiers | immutable timestamped API pulls — the evidence behind every number |
| `raw/MANIFEST.sha256`, `raw/EDGE_MANIFEST.sha256` | verifiers | per-pull hashes; packets must cite one to make a money/edge claim |

## Signed facts and the attestation (issues #36 / #42)

When the operator provisions a signing key (`ssh-keygen -t ed25519 -N "" -C verifier -f
$MONEY_AGENT_STATE/verifier_signing_key`, then commit the public half as
`harness/verifier_key.pub` and `harness/allowed_signers` = `verifier <contents of the .pub>`),
three things become true:

1. `bin/pnl.py` writes a detached signature beside every `truth.json`, embeds `previous_hash`
   (sha256 of the previously published `truth.json`, a git-independent hash chain; an unreachable
   parent after `LEDGER_MAX_COMMITS` rotation reads as a chain start), and emits the signed
   `attestation.json`.
2. `bin/truth.py` REFUSES the grounded label for any unsigned, tampered, or chain-broken
   `truth.json` — fail-closed, so every gate above it halts. On the ledger branch this upgrades
   SoD beyond the forgeable author string (#36); in weak mode it remains a tripwire (a swapped
   key+sig pair is a visible commit), stated per this repo's honesty convention.
3. **Anyone** can verify a claim from a bare clone, no credentials:

```bash
git fetch origin ledger
git show origin/ledger:ledger/truth.json > /tmp/t.json
git show origin/ledger:ledger/truth.json.sig > /tmp/t.sig
git show origin/ledger:harness/allowed_signers > /tmp/signers
ssh-keygen -Y verify -f /tmp/signers -I verifier -n money-agent-ledger -s /tmp/t.sig < /tmp/t.json
# chain: previous_hash in t.json == sha256 of the parent commit's truth.json
git show origin/ledger~1:ledger/truth.json | sha256sum
# If origin/ledger~1 does not resolve, this tip is a LEDGER_MAX_COMMITS rotation boundary:
# an unreachable parent is the documented chain start, so skip this parent-hash comparison.
```

The same commands with `attestation.json` verify the customer-facing summary. What this does NOT
prove: that the key belongs to an honest verifier — key custody is the operator's provisioning
step (SETUP.md), exactly like the read-key boundary it extends.

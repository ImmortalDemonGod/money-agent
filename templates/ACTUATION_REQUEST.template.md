# ACTUATION_REQUEST -- how the agent asks the operator to pass ONE mechanical wall

Unlike the other templates here, this is a WORKED REFERENCE, not a fill-and-commit form: nothing
gates a copy of it. It documents `bin/actuate.py request`, the agent's one legitimate operator-ask,
because the argument shape is easy to get wrong and lives otherwise only in `--help` and the source.

`actuate.py` is an ACTUATOR, NEVER AN ORACLE. You may hand the operator a bounded MECHANICAL action
you are structurally barred from performing; you may NOT ask them for strategy, judgment, or content
(a leak-check refuses the request if any operator-facing field smuggles those). Each open request
blocks "impossible" conclusions via a mandatory companion bet, so file one only when a real,
already-hit wall is in the way -- then KEEP WORKING; requesting is never waiting.

## The five kinds (`--kind`)

| kind | for | money-moving? |
|---|---|---|
| `claim-host` | claim/keep an ephemeral host the sandbox deployed (e.g. a temp Worker before its auto-delete) | no |
| `deploy-account` | a deploy/hosting step that needs the operator's authenticated session | no |
| `kyc-step` | a one-time human KYC / identity verification | no |
| `approval-click` | click an approval / confirmation link the agent cannot reach | no |
| `wallet-fund` | fund a wallet on the account holder's own account | **YES** -- requires a P3 name-test ruling at fulfillment |

## The four return kinds (`--return-kind`)

`none` (nothing comes back) · `confirmation` (the operator attests it is done) · `value` (a
non-secret string, e.g. a URL or address) · `credential` (a SECRET; encrypted to an ephemeral key
the request publishes, decryptable only inside this run's sandbox, WITHIN-RUN ONLY).

## Required arguments

All ten are required. Note `--steps` is a FILE PATH, not an inline string.

| flag | what it holds |
|---|---|
| `--kind` | one of the five above |
| `--gate` | the specific gate/action being passed |
| `--target-url` | the exact URL where the action happens |
| `--identity` | which account acts (the run identity: `miguel.ingram.work@gmail.com`) |
| `--steps` | PATH to a file with the exact steps the operator performs |
| `--expect` | what success looks like (the observable outcome) |
| `--test` | the cited empirical hit -- proof you ACTUALLY hit this wall (>= 8 chars; a request for an untested gate is guessing) |
| `--ev` | why passing it is worth the operator's minutes (>= 8 chars) |
| `--return-kind` | one of the four above |
| `--deadline` | ISO-8601 WITH timezone and in the future (append `Z` for UTC, e.g. `2026-08-01T00:00:00Z`) |

Optional: `--artifact <file>` (a file the operator must upload/apply; leak-checked too);
`--verify-cmd '<shell>'` (a pre-registered post-handback usability probe, valid only with
`--return-kind value|credential`: exit 0 means the returned credential grants working sandbox
access -- use it when the gate is egress reputation, e.g. a WAF/IP block an operator-created
account does not cure).

## Worked example (a temp-host claim; strategy-free)

```bash
cat > /tmp/steps.txt <<'EOF'
1. Log in to the host provider dashboard as the run identity.
2. Open the deployment at the target URL.
3. Click "Claim" so it stops auto-deleting.
EOF

python3 bin/actuate.py request \
  --kind claim-host \
  --gate "temp host auto-deletes in ~60min unless claimed on the provider dashboard" \
  --target-url "https://example-deploy.workers.dev/" \
  --identity "miguel.ingram.work@gmail.com" \
  --steps /tmp/steps.txt \
  --expect "the deployment shows Claimed and no longer auto-deletes" \
  --test "host_check.py passed on this URL at iter NNN; provider UI shows a ~60min TTL countdown" \
  --ev "keeps a live crawlable host reachable past the auto-delete window at no card cost" \
  --return-kind confirmation \
  --deadline "2026-08-01T00:00:00Z"
```

## Lifecycle

1. `request` files the typed task and its conclusion-blocking companion bet. KEEP WORKING.
2. The operator is pinged (notifier), reads the self-contained card, and either `fulfill`s or
   `decline`s it -- a signed resolution on the verifier's facts lane you cannot write.
3. You consume it with `bin/actuate.py sync <id>` / `sync-all`; the signature and request-hash
   binding are checked, and a `credential` return is decrypted in-sandbox. You cannot self-certify
   that the operator acted. `bin/actuate_watch.sh` runs `sync-all` automatically on the durable
   wakeup, so you usually do nothing here.

The operator side of this (notifier + fulfill form) is `SETUP.md` §4e; the full command contract is
`tests/acceptance_actuation.py`.

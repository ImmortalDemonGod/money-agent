# Finding your way around, and contributing

Four very different readers use this repo. Start from who you are; skip everything not addressed to you.

**You are the OPERATOR (provisioning or starting a run):**
[`SETUP.md`](SETUP.md) end to end, then issue #20 (the pre-run-2 acceptance gates), then `bin/new_run.sh`
to close the previous run and `bin/start_verifier.sh` to open yours. [`docs/STANDING_RUN.md`](docs/STANDING_RUN.md)
if the run should last days. That is the whole list.

**You are the RUN AGENT:**
your world is `CLAUDE.md` (the bounds), `CONSTITUTION.md`, `PROMPT.md`, `RUN_COMMANDS.md`,
`knowledge/` (what past runs falsified, so you do not re-pay for it), `templates/` (the forms the
gates require), and the facts via `python3 bin/truth.py`.

**You are a REVIEWER or AUDITOR (did it really?):**
[`ledger/truth.json`](ledger/truth.json) and `ledger/edge.json` on the run's ledger branch are the only real
numbers; [`REFUSALS.md`](REFUSALS.md) is what it would not do; `MONEY_LOG.md` vs the ledger is the
claim-vs-fact drift; `IMPROVEMENT_LOG.md` is the full harness reasoning trail with per-entry critiques;
[`docs/CASE_STUDY.md`](docs/CASE_STUDY.md) is the verification-theater finding that redesigned the program.

**You are a CONTRIBUTOR (changing the harness):**
[`docs/V2_DESIGN.md`](docs/V2_DESIGN.md) is the architecture of record, the harness that actually shipped
(B1-B9 to A1-A8, verified by the M1-M12 scorecard); [`docs/V2_HARNESS_DESIGN.md`](docs/V2_HARNESS_DESIGN.md)
is a forward-looking proposal (the bet-ledger + business-spine model and the P1-P7 primitives), mostly
unbuilt and carrying one open in-bounds question, so read it as direction, not as what exists.
`bin/README.md` says what each script is and who may run it (the trust classes are the entire point of this
repo).

## Who owns what

| Directory | Owner | What lives there |
|---|---|---|
| `bin/` | mixed (see `bin/README.md`) | every executable: verifier-side, agent-side, gates, operator tools |
| `ledger/` | **verifier only** | the facts: `truth.json`, `edge.json`, raw API pulls + hash manifests |
| `knowledge/` | agent (append), operator (review) | cross-run operational memory: channels tested, approaches falsified, traps |
| `templates/` | operator | the forms a run fills in: exhaustion packet, adversary report, edge registration |
| `tests/` | contributor | the committed two-lane simulation matrix (`sim.sh`) |
| `docs/` | humans | design, case study, standing-run recipe, probe records; reference for the agent, never instruction (#10 ruling) |
| `harness/` | operator | the traffic beacon (Cloudflare worker) |
| `archive/` | `bin/new_run.sh` | each finished run's frozen state, one directory per run |
| `.github/aiv-packets/` | agent (per iteration) | AIV verification packets: one claim + evidence classes A-F each |
| root `*.md` logs | agent (append-only) | the LIVE run's claims: `MONEY_LOG`, `SENT_LOG`, `REFUSALS`, `DISCLOSURE_EV_LOG` |

## Changing the harness

The trust classes (who may run what) are the entire point of this repo, so any change to the harness is
reviewed against that boundary first. Start at `bin/README.md` and [`docs/V2_DESIGN.md`](docs/V2_DESIGN.md),
run `bash tests/sim.sh` before and after, and open a PR. Design disagreements are welcome in the
[issues](../../issues); the run-2 backlog (#12-#17) is the friendliest way in.

CI (`.github/workflows/ci.yml`) gates every PR: the `sim.sh` matrix, `shellcheck`, `gitleaks`, and a Python
byte-compile must pass. `readme-check.yml` additionally lints `README.md` and `CONTRIBUTING.md` for broken
links, stray anchors, and typography drift.

## Promoting agent-built tools into the canonical harness

Run agents build tools. Two categories, two rules (issue #11):

- **Business tools** (run 1's `audit.py`, `reach.py`, `scoreboard.py`, ...) are run-local, never
  promoted. On `main` they would seed the next run's business -- the M9 leak-check applies to code,
  not just prose. They live and die with their run's PR and archive.
- **Harness machinery** (verification gates, verifiers, scaffolds) is promotable, but ONLY by
  deliberate per-artifact operator review, never in bulk. The review asks four questions:
  1. Does it enforce a bound or verify a claim (machinery), rather than pursue revenue (business)?
  2. Is it free of strategy nouns (the pinned M9 grep) and run-specific assumptions?
  3. Does it ship with sim fixtures that bite, and does the full matrix stay green with it in?
  4. Which trust class owns it (`bin/README.md`), and is it added to `bin/sod_hook.sh`'s blocklist
     if it is verifier- or gate-class?

  A tool that fails any of the four stays on its run's branch. The precedent is run 1's
  `disclosure_gate.py`: promoted after review -- genericized, fixture-covered, sod_hook-protected --
  and now canonical. Auto-adopting everything an agent builds would erode both the clean harness
  and the authored-input discipline that makes cross-run comparisons mean anything.

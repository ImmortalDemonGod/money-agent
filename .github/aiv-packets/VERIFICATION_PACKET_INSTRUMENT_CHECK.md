# AIV Verification Packet (v2.1): mechanized site instrumentation (#65 items 2 & 4 + item-3 evidence tool)

**Author:** Miguel Ingram (Author)
**Verifier:** Claude Code (Verifier)

## Logical unit of work

Delivers the **agent-ownable** part of the remaining #65 items by making site instrumentation
*mechanical* and *fail-closed*, building on the reusable `/beacon.js` tag (item 1, already on main).
This commit is **one new agent tool + docs** — it does NOT touch any verifier surface:

- **`bin/instrument_check.py`** (new) — the build-side sibling of the verifier-owned `host_check.py`.
  Two jobs:
  (a) `--inject <file> --beacon <host> --site <id>` mechanizes the tag into a built page before
  publish — idempotent, and **fail-closed** (a page with no `</body>` exits non-zero rather than
  shipping blind) — this is **#65 item 2** (the publish helper that refuses to ship un-instrumented);
  (b) default `<url>` mode fetches the LIVE page (reusing host_check's SSRF-guarded `_get`) and emits
  `INSTRUMENT_CHECK: <url> | tag=… | site=… | beacon=… | verdict=PASS/FAIL`, exit≠0 if missing. That
  line is the deterministic **Stage-0 instrument-probe evidence** (the analog of `HOST_CHECK:`) that
  **#65 item 3** wants — this commit *produces* that evidence; wiring it into the gate is verifier work.
- **`harness/beacon/README.md`** — the one-line-instrumentation contract (inject → deploy → verify) —
  **#65 item 4**.

**Not in this commit — the SoD boundary (this is the point, not a gap).** #65 item 3's acceptance is
"wired as the Stage-0 `funnel events CONFIRMED` evidence in `spine.py`." `spine.py`, `bin/aiv_gate.sh`
and `tests/*` are **verifier-owned** (`bin/sod_hook.sh` blocks the agent from committing them), and
for the gate's re-run to be trustworthy the evidence tool itself must be verifier-frozen like
`host_check.py`. So the agent cannot self-adopt this into its own gate. The complete, tested gate
wiring (an `aiv_gate.sh` 2b-bis block that re-runs `instrument_check` on a cited `INSTRUMENT_CHECK_URL:`,
a `tests/sim.sh` S18 selftest, and adding `instrument_check.py` to the `sod_hook` protected list) is
handed to the verifier as `scratchpad/verifier-adoption-65.patch` for adoption under `AIV_VERIFIER=1`.

## Classification

```yaml
classification:
  risk_tier: R1
  sod_mode: S0
  critical_surfaces: []
  blast_radius: local
  classification_rationale: >
    Per AIV section 5, this commit adds one agent-invocable executable (bin/instrument_check.py) that
    makes an outbound HTTPS fetch reusing host_check's reviewed SSRF/DNS-rebinding guard (no new
    network primitive) plus a docs file. It touches no payment behavior, no credentials, no
    facts-lane/ledger, and NO verifier surface -- the gate/spine/test wiring is deliberately excluded
    (verifier-owned; handed off as a patch). R1 (executable tool, public fetch); R2+ is not warranted.
  classified_by: Miguel Ingram (Author) + Claude Code (Verifier)
  classified_at: 2026-07-23T00:00:00Z
```

## Claim(s)

1. **CLM-001 — inject mechanizes the tag, fail-closed.** `instrument_check.py --inject` adds the
   `/beacon.js` tag before `</body>` iff absent (idempotent), and exits non-zero on a page with no
   `</body>` anchor.
   **Falsifiable by:** a second `--inject` producing two tags; or a `</body>`-less page exiting 0.

2. **CLM-002 — live check is deterministic probe evidence, fail-closed.** default `<url>` mode emits
   an `INSTRUMENT_CHECK:` line and exits 0 iff the served page carries the tag, non-zero otherwise.
   **Falsifiable by:** an instrumented URL returning FAIL, or an un-instrumented URL returning PASS.

3. **CLM-003 — the exit code makes the probe gate-consumable.** The tool exits non-zero exactly when
   the tag is missing, so a verifier re-run (the handed-off `aiv_gate.sh` 2b-bis block) can trust the
   process result, not a self-typed line. Verified at the tool level here; the gate wiring itself is
   the verifier's to adopt.
   **Falsifiable by:** an un-instrumented URL exiting 0, or an instrumented URL exiting non-zero.

4. **CLM-004 — scope is bounded and agent-ownable.** The commit changes only `bin/instrument_check.py`,
   `harness/beacon/README.md`, and this packet — no verifier surface (`spine.py`, `aiv_gate.sh`,
   `tests/*`) is touched, so `bin/sod_hook.sh` permits it.
   **Falsifiable by:** `git show --stat` listing any verifier-owned path.

## Ledger anchor

**N/A — rationale:** this change does not read, mention, or affect money. `ledger/truth.json` is
untouched; no `manifest_sha256` is cited because the packet makes no money claim. Instrumentation
tooling exists precisely so that `received_usd` stays the only human-value ground truth while
non-money traffic is measured honestly.

## Evidence

### Class A (Execution) — all run this session, in the `close-65-instrument` worktree off origin/main

- **Static:** `python3 -m py_compile bin/instrument_check.py` → OK. (The handed-off verifier patch was
  also checked: `shellcheck -S error bin/aiv_gate.sh` → 0 errors, `bash -n tests/sim.sh` → OK — but
  those files are NOT in this commit.)
- **CLM-001 + selftest (deterministic):** `python3 bin/instrument_check.py --selftest` →
  `selftest: all passed (inject, idempotent, fail-closed, tag detection)`, exit 0. This exercises:
  inject adds the tag with the site id; a 2nd inject leaves exactly one `/beacon.js`; a page with no
  `</body>` returns `REFUSED (fail-closed)` rc≠0; tag-detection has no false pos (non-beacon script)
  or false neg (real tag).
- **CLM-002 (live, both directions):**
  - PASS: `instrument_check.py https://one-honest-dollar.cloud-pyramid.workers.dev/` →
    `INSTRUMENT_CHECK: … | tag=PRESENT | site=hub | beacon=…workers.dev | verdict=PASS`, exit 0.
  - FAIL (fail-closed): `instrument_check.py https://onehonestdollar.com/` →
    `INSTRUMENT_CHECK: … | tag=MISSING | site=(none) | beacon=MISSING | verdict=FAIL`, exit 1. (The
    showcase genuinely carries no beacon tag yet, so a real un-instrumented site FAILS, as designed.)
- **CLM-003 (gate-consumable exit code):** the two live runs above returned exit 0 (instrumented) and
  exit 1 (un-instrumented). To confirm the handed-off wiring consumes that correctly, the 2b-bis block
  was reproduced in isolation against two packets — one citing the hub URL → `GATE PASS (re-ran, tag
  present)`; one citing the un-instrumented showcase → `GATE FAIL (instrument_check FAILED —
  unmeasured)`. So once the verifier adopts the patch, a self-typed `verdict=PASS` for an
  un-instrumented site is rejected. (This validates the hand-off; the wiring is not in this commit.)

### Class C (Negative) — the fail-closed paths actually fail

The whole point of the tool is that the *absence* of instrumentation is caught, not waved through.
Every negative branch was exercised this session:

- **No `</body>` anchor → refuse, not silently pass.** `--inject` on `<html><h1>no body</h1></html>`
  → `REFUSED (fail-closed)`, rc≠0 (selftest check 3).
- **Un-instrumented live URL → FAIL, exit≠0.** `instrument_check.py https://onehonestdollar.com/` →
  `tag=MISSING … verdict=FAIL`, exit 1 — a real site with no tag does not report PASS.
- **No false positive on a non-beacon script.** `has_tag('<script src="…/analytics-other.js">')` →
  `False` (selftest check 4), so an unrelated analytics tag is not mistaken for instrumentation.

### Class B (Referential)

- CLM-001/002: `inject()` / `check()` / `_TAG_RE` in `bin/instrument_check.py`
  (bin/instrument_check.py:45, :58, :77).
- CLM-003: the non-zero exit path in `check()` (bin/instrument_check.py:102, `return 0 if ok else 1`);
  the verifier-side consumer is the 2b-bis block in `scratchpad/verifier-adoption-65.patch`.
- CLM-004: `git show --stat HEAD` lists only `bin/instrument_check.py`, `harness/beacon/README.md`,
  and this packet.

### Class E (Intent Alignment)

Immutable intent: the operator instruction to *fully close #65* — instrumentation must be one
mechanical, fail-closed line, so run 2 cannot repeat run 1's "9 funnels, zero analytics, retracted
reach-vs-conversion conclusion" (iter 098). Item 1 (the served tag) shipped; this delivers the agent's
share: the inject mechanization (2), the tool that produces the deterministic probe line (3's
evidence), and the docs (4). Item 3's *gate wiring* is the verifier's to adopt — the agent proposing
but not self-adopting its own gate is itself the intent (SoD) working, not a shortfall.

### Class F (Provenance)

- `bin/instrument_check.py` is modeled on `bin/host_check.py` (same dir): it imports `host_check._get`
  for the SSRF-guarded fetch and mirrors the `HOST_CHECK:`/exit-nonzero contract. Reproduce by
  diffing the emit-line + guard-reuse against `host_check.py`.

## Honest limitations

- **`instrument_check` proves the tag is SERVED, not that a hit LANDS.** A served `/beacon.js` tag
  fires on real browser load (proven end-to-end for the tag itself in the item-1 packet), but this
  tool verifies presence in the served HTML, not a round-trip ping. That is the deterministic floor;
  a live-hit assertion would require a headless browser per check and is deliberately not required.
- **The human/bot metric is still an estimate** for the reasons on the JS-gate (#61): headless
  browsers inflate, VPN/cloud-browser humans deflate. Instrumentation makes traffic *visible*, not
  *certain*; `received_usd` remains the only ground truth.
- **Classes D/G omitted:** no `truth.json` state delta to diff (D); no pre-registered prediction (G).
  Class C is supplied above (the fail-closed branches).
- **Item 3 is only partially landed by this commit.** The tool *produces* the deterministic probe
  evidence (the `INSTRUMENT_CHECK:` line + gate-consumable exit code), but "wired as the Stage-0
  evidence in `spine.py`" — the acceptance wording — requires a verifier-owned change. That wiring is
  written and tested (`scratchpad/verifier-adoption-65.patch`) and awaits verifier adoption; until
  then #65 stays OPEN. This packet does not claim item 3 is complete.
- **The tool must be verifier-frozen before its probe is gate-trusted.** Because the gate re-runs
  `instrument_check.py`, an agent-editable copy could be rigged to always PASS. The hand-off patch
  therefore also adds `bin/instrument_check.py` to the `sod_hook` protected list (same trust class as
  `host_check.py`). Adopting it makes this agent commit the *last* agent-authored version of the file.

## Verification methodology

```bash
python3 -m py_compile bin/instrument_check.py
python3 bin/instrument_check.py --selftest                                   # deterministic
python3 bin/instrument_check.py https://one-honest-dollar.cloud-pyramid.workers.dev/   # PASS, exit 0
python3 bin/instrument_check.py https://onehonestdollar.com/                  # FAIL, exit 1
git show --stat HEAD    # only bin/instrument_check.py, harness/beacon/README.md, this packet
```

## Summary

Makes run-2 site instrumentation one mechanical, fail-closed line: `instrument_check.py --inject`
adds the `/beacon.js` tag before publish (idempotent, fail-closed), and its `<url>` mode verifies the
live page serves it, emitting the Stage-0 `INSTRUMENT_CHECK:` probe line with a gate-consumable exit
code. R1/S0, no verifier surface touched. Delivers #65 items 2 & 4 and the item-3 evidence tool; the
item-3 *gate wiring* is handed to the verifier as a patch, so #65 stays open until that is adopted.

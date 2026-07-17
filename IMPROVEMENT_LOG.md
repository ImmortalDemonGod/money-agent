# IMPROVEMENT_LOG — v2 core-system redesign

Running log of every improvement, its reasoning, and the standing critique. Loop cadence: 20m,
window 2026-07-17T04:17Z → ~06:17Z. Design: `docs/V2_DESIGN.md`. Baseline: `main` @ 5cc4adc.
Evidence base: full read of run-1 (PR #8 branch) — MONEY_LOG (88 entries), REFUSALS, packets,
README post-mortem, operator notes, plus two exhaustive subagent sweeps of the 95 packets and all
run-built artifacts/tools.

Rule for every entry: what changed | why (cite the v1 evidence) | how it's measured (scorecard M#)
| what the critique pass said.

---

## Entry 001 — 2026-07-17T04:17Z–04:4xZ — inventory, design, and the send-path repair

**What:** Bottleneck inventory B1–B9 (each cited to MONEY_LOG iterations), architecture A1–A8,
scorecard M1–M12 (`docs/V2_DESIGN.md`). First mechanical fix: A5, the send path on main.

**Why this order:** the design had to come from measured damage, not taste — B1 (≥6 evidence-loss
events) and B2 (the false TERMINAL) are the two failures with the highest observed cost, and both
are architectural, not behavioral. A5 went first as implementation because main is *currently
broken by design*: `mail.py` imports `disclosure_gate` fail-closed, but the gate file lives only on
the run branch — a fresh v2 run today cannot send a single email (M12). That is the kind of defect
that costs a run its first hours (v1 lost ~17 iterations to the `.env`/`.env.agent` conflation —
same genre: the tool was fine, the wiring wasn't).

**Changes landed this entry:**
1. `docs/V2_DESIGN.md` — the design (B1–B9, A1–A8, M1–M12, implementation order, standing critique).
2. `bin/disclosure_gate.py` — promoted from the run branch, genericized: v1-business examples
   stripped from comments/docstrings (issue #9 discipline applied to code too); adds the `page`
   mode named in A2/A5 so storefront publishes get a recorded EV decision (v1 gap: buyer-facing
   pages never carried a disclosure decision at all — found by the artifact sweep).
3. `DISCLOSURE_EV_LOG.md` — fresh template (mechanism docs only, no v1 decision history).
4. `bin/mail.py` — SENT_LOG append is now commit-and-push-in-the-same-operation (first half of A1's
   `append_log` idea, applied where v1 measurably lost data: SENT_LOG was wiped repeatedly and is
   partly "RECONSTRUCTED" on the run branch — the audit trail of what left under a real man's name
   must not depend on the agent remembering to commit).

**Measured against scorecard:** M12 (broken-by-design paths on main): 1 → 0 pending e2e test.
M4 (ungated sends): enforced on main once this lands. M5 (losable sends): fixed at the mail.py layer.

**Critique pass (standing, updated each entry):**
- The adversary novelty check (A2) is agent-invoked → strong tripwire, not out-of-band grounding.
  Named honestly in the gate output; verifier-side execution is the upgrade path.
- Two-lane git (A1) introduces a stale-ledger-read failure mode; H2 freshness halt transfers
  unchanged and covers it.
- Risk for this entry specifically: genericizing disclosure_gate must not weaken its regexes — the
  i18n fix (iter 093: Japanese `\b` bug) must survive the port verbatim.
- Not yet addressed: B1's core (verifier still resets the shared branch on main's verifier_loop) —
  that is entry 002, the highest-value structural change.

**Next (entry 002):** A1 two-lane git — verifier_loop v2 publishes to a `ledger` branch;
`bin/truth.py` single read path; guard.py reads the ledger branch; `bin/append_log.py` general.

---

## Entry 002 — 2026-07-17T04:40Z–04:50Z — two-lane git: the harness can no longer destroy its own evidence

**What:** A1 implemented. The verifier now publishes facts to a dedicated `ledger` branch from its
own checkout (`verifier_loop.sh` rewrite); the agent's claims branch is never named, reset, or
written by any harness process. `bin/truth.py` is the single read path (ledger-branch first,
working-tree fallback, source labeled); `bin/guard.py` reads through it and the SoD tripwire is now
mode-aware; `bin/pnl.py` hashes the constitution from the AGENT's committed copy (`AGENT_BRANCH`)
instead of the verifier's own tree; `bin/append_log.py` makes narrative appends durable in one
fail-closed step (write+commit atomic, rollback on failure). This entry itself is the append_log
end-to-end test.

**Why first among the structural changes:** B1 had the highest measured damage in v1 — at least six
evidence-loss events, a partly-RECONSTRUCTED send log, two iterations with no surviving record, and
an entire class of agent workarounds (commit-in-the-same-breath, ls-tree blob checks) that existed
only because the facts channel could bulldoze the claims channel. The two-lane design deletes the
mechanism rather than mitigating it. Bonus effects: the 196 verifier heartbeat commits stop
polluting the claims history (M11), and "only the verifier writes the ledger branch" is now
enforceable at the REMOTE (branch protection) — SoD upgrades from tripwire to wall for the first
time.

**Verified by running, not reading (v1's own rule):**
- truth.py: working-tree fallback returns source-labeled facts; simulated `origin/ledger` ref
  returns `ledger-branch` source.
- guard.py forgery test: a non-verifier author on the facts lane → HALT "SoD is broken", exit 1.
- guard.py planted-ledger test: any post-baseline ledger commit on the claims lane → HALT, exit 1.
- guard.py staleness: a day-old ledger still HALTS by default (H2 transfers unchanged).
- Migration wrinkle FOUND BY THE TEST and pinned in a comment: the planted-ledger check is only
  sound with a fresh run-start baseline (a v1-era branch carries legitimate old verifier ledger
  commits). `set_baseline.py` at run start — already step 3 of start_verifier.sh — is load-bearing.

**Scorecard:** M1: 6 → 0 by construction (no process resets the claims lane). M11: 196 → 0.
M5 completed (append_log generalizes the mail.py fix from entry 001).

**Critique pass:**
- start_verifier.sh still speaks v1 (syncs the agent branch, BRANCH env) — must be updated to the
  two-lane invocation or operators will resurrect the old topology. Queued for entry 003.
- setup_sandbox.sh preflight doesn't yet assert the two-lane invariants (ledger branch exists,
  truth.py resolves). Queued.
- aiv_gate.sh reads `git show HEAD:ledger/truth.json` (the claims lane) for its money-claim
  comparison — in two-lane mode that file goes stale on the claims branch; it must read via
  truth.py. This is a REAL residual bug introduced by the migration. Queued for entry 003 with
  the stop-grounding work.
- The ledger branch grows one commit per meaningful change + heartbeat (~12/hr); fine for a run,
  worth a squash/rotate note in SETUP for multi-week standing presence.

**Next (entry 003):** A2 (grounded stop: conclusion_gate + adversary requirement + /goal v2) plus
the three queued migration fixes above.

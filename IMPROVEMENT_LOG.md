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

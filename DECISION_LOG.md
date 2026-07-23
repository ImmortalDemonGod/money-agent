# DECISION_LOG

Recorded decisions that change harness behavior or cross a named design line. Operator/design
decisions are dated entries below. (Per-run P3 name-test *publish* decisions are also appended
here by the agent during a run, per PROMPT.md step 4 -- keep those under their own dated lines.)

---

## 2026-07-23 -- S17: SPINE_ENFORCE default flipped OFF -> ON, plus a `demand-probe` carve-out

**Decision.** The stage-ordering spine (`bin/spine.py`, `spine.yml`) is now ARMED by default. The
committed default lives in `spine.yml` (`enforce: on`); `SPINE_ENFORCE` still overrides it in both
directions (`=0` forces a pure-measurement run, `=1` forces arming). `DEMAND_REFUTED_K` is
UNCHANGED (still 0): the terminal set {verified dollar, cap, operator} is not touched by this flip.

**Why (the line being crossed, on purpose).** Until S17 the spine was default-off to preserve the
experiment's ability to measure what a context-free agent converges on *unforced*. Run 1 already
made that measurement: unforced, the agent went build-first and earned **$0.00, verified**
(`archive/run-001`). A spine-off run 2 therefore does not produce a new finding -- it *replicates a
solved null*. Keeping it off to protect attribution, when attribution has nothing left to
attribute, is the "motion instead of a conclusion" the project itself warns against. So the
informative next run must INTERVENE, and demand-first ordering is the highest-EV intervention run 1
points to. This consciously converts demand-first from *something measured as the agent's
discovery* into *method imposed by the harness* -- the "method vs strategy-injection" line the spine
was built around, crossed deliberately and logged, not by stealth default. Restoring the pure
measurement is one env var away (`SPINE_ENFORCE=0`).

**The carve-out (why default-on does not starve its own input).** Run 1's single real demand signal
(the Marcos/Stormberry inbound) arrived *because a product already existed* -- the build created the
surface that produced the demand. A naive "no build before demand-confirmed" gate would have
blocked the exact move that surfaced it. So S17 adds a `demand-probe` bet type, legal at spine
stage 0: a MINIMAL published/payable smoke test (one landing page, one payment-linked stub, a
"reply for X" offer) whose sole purpose is to elicit demand. It is not a `delivery`: it never
satisfies the stage-3 build exit, so it cannot be relabeled into "the product is built", and it is
capped per lane (`lane_caps.demand_probe_per_lane`, default 2) so a full product line cannot be
shipped as a run of "probes". A second gaming-safety layer (in `bin/bet_gate.py`, enforced on every
typed add regardless of `BET_GATE_ENFORCE`) requires a demand-probe's success oracle to be
externally grounded (`instrumented`/`stripe`, never `deterministic`): demand is a fact about other
people, so a self-graded "demand" probe is a delivery build in disguise. The full/scaled product
stays gated at stage 3 behind a won `demand-confirmed` bet.

**Precondition, not optional.** With the spine armed, the beacon (`harness/beacon/`) MUST be
deployed at hour one of run 2. Run 1 never measured whether its funnels converted (the beacon went
live after the run; `archive/run-001/ADDENDUM-2026-07-20.md` leaves reach-vs-conversion
UNDETERMINED). Arming demand-first without instrumenting it would repeat that: a second undetermined
night. Deploy the beacon, or the intervention is unmeasurable.

**Scope of the change (files).** `spine.yml` (`enforce: on`, `demand_probe_per_lane`, `demand-probe`
ordering + carve-out doc); `bin/spine.py` (`enforced()` reads the committed default with env
override; `demand-probe` cap in `check_placement`; `demand-probe` exempt from E2 suspension);
`bin/bet_gate.py` (`demand-probe` added to the typed-bet `TYPES` whitelist); `bin/bets.py` (the
spine-import-failure fallback now fail-closed to armed, consistent with the new default);
`tests/sim.sh` (the default-off assertion is now an explicit `SPINE_ENFORCE=0` override; new
assertions cover the armed default, the stage-0 carve-out, and the per-lane cap);
`docs/runbooks/RUN2_OPERATOR_RUNBOOK.md` (D6 updated).

**Reversal.** `SPINE_ENFORCE=0` in the environment restores byte-identical pre-S17 (un-armed)
behavior for any run, with no code change.

Decided by: operator (military.ingram@gmail.com), 2026-07-23. Branch: `claude/project-analysis-aoixmf`.

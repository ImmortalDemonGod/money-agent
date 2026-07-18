# tests/ — the committed verification matrix

    bash tests/sim.sh        # exits 0 iff every assertion passes; SIM_KEEP=1 keeps the workdir

`sim.sh` builds a LOCAL bare origin + separate agent/verifier clones + a real ledger branch and
asserts the harness's load-bearing behaviors: grounded reads, every guard terminal (first dollar,
edge verified, VOID, staleness, SoD forgery), the full gate adjudication (honest pass and each
class of dishonest fail), the bets/conclusion interplay, the edge verdict machine against a
stubbed broker, and the verifier convergence block run verbatim (extracted between the
TEST-MARKER comments in `bin/verifier_loop.sh`).

History: this rig, hand-rebuilt in four separate review sessions, caught every real defect those
reviews found — an inert one-line "fix" whose log claimed it was verified, a merge that silently
dropped a gate section, an anchor rule that failed honest packets. Committing it is what makes
that protection per-commit instead of per-review.

Honest scope: component-level only. The broker is stubbed and the facts are synthesized; the live
seams (real Stripe key, real paper API) are the operator acceptance gates in SETUP.md §4b and
issue #20. A green matrix here is necessary, never sufficient, for trusting a run.

`aiv` CLI note: the gate's stage 0 is fail-closed on a missing CLI by design, so the gate tests
SKIP loudly if `aiv` is not on PATH (`pip install` the aiv-protocol repo to run them).

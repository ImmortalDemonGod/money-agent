# tests/ — the committed verification matrix

    bash tests/sim.sh                     # exits 0 iff every assertion passes; SIM_KEEP=1 keeps the workdir
    bash tests/corpus.sh                  # Tier-0 regression corpus: run-1's real artifacts vs the v2 gates
    python3 tests/acceptance_actuation.py # capability-delegation contract: 25 checks, CI-enforced

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

## corpus.sh — the Tier-0 regression corpus (issue #44)

Where `sim.sh` synthesizes fixtures, `corpus.sh` replays run-1's REAL failure artifacts from
`archive/run-001/` (copied into a throwaway rig; the archive is never mutated) and asserts the v2
gates refuse them **for the right reasons**. Assertions are on failure MESSAGES, not exit codes —
proven necessary by the bite check: a gate mutated blind to the bet registry (the exact v1 defect)
still exits non-zero on other layers, so an exit-code-only test reads green while the regression
is live. Current fixtures: the iteration-095 false stop (open estate bet + missing fresh-context
adversary, with a discriminator run proving each assertion tracks its cause), the stale-adversary
counterfactual, and the 086 empty-commit seam (labeled seam test: the gate subprocess is stubbed;
the ls-tree safety net is the subject).

**The pattern for adding one (do this per future incident):** copy the incident's real artifacts
from the archive into the rig, reconstruct any state that postdates the incident's tooling (e.g.
the bets registry), assert the refusing gate names the incident's SPECIFIC cause, then add a
discriminator run showing the message disappears when only that cause is repaired.

## acceptance_actuation.py — the capability-delegation contract (`bin/actuate.py`)

The falsifiable definition-of-done for the actuation queue, written RED-first and **bite-verified**
(a no-op stub makes every check FAIL, not PENDING). It builds a throwaway two-lane git world per
check and asserts the round-trips (S1–S3), the separation-of-duties / tamper-resistance defenses
(N1–N18, one regression per adversarial finding), the post-handback usability probe (N19), the
no-terminal web-form fulfill path (N20), and the usability/notification benchmarks (B1–B2). Same honest scope as `sim.sh`: offline and keyless — the one live actuation on a real rail
is the Tier-L operator gate (see `.github/aiv-evidence/ACTUATION_E2E.md` for the real end-to-end
push). Human-readable companion contract: `tests/ACCEPTANCE_ACTUATION.md`. Run by CI in the sim job,
so "25 green" is gate-enforced, not self-reported.

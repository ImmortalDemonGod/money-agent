# Mutation coverage log (S16)

The sim matrix (`tests/sim.sh`) and corpus (`tests/corpus.sh`) only prove the harness catches
the defects someone thought to write a fixture for. Mutation testing proves the converse: take
a defect the matrix is SUPPOSED to catch, reintroduce it, and confirm the matrix goes red. A
mutation that stays green is a coverage hole.

Run it: `bash tests/mutation_test.sh` (operates only in throwaway clones under a tempdir; never
touches the working tree). Expect `mutations CAUGHT=8 ESCAPED=0`.

## The pass (8/8 caught, 2026-07-20)

Each row reintroduces a historical defect CLASS -- the kinds of bug this program actually
shipped and had to fix -- and asserts the matrix catches it.

| # | Mutation (defect class) | Target | Caught by |
|---|---|---|---|
| 1 | inert first-dollar halt (`if False and ...`) -- the run-1 inert-`rev-list -q` class | guard.py | first-dollar sim assertions |
| 2 | signature wall removed (`_enforce_signature` -> no-op) | truth.py | tampered/unsigned + CRLF byte-fidelity fixtures |
| 3 | shadow cross-world wall removed (`_enforce_shadow_wall` -> no-op) | truth.py | S12 read-wall fixtures (live<->shadow) |
| 4 | silent truncation (drop `coverage_incomplete`, force complete) | pnl.py | S2 truncation-at-cap fixture |
| 5 | currency leak (disable `_currency_err`) | pnl.py | S2 mixed-currency fixture |
| 6 | bet-gate fail-open (`authorize` -> always allow) | bet_gate.py | S9 armed-refuses + mail armed-send fixtures |
| 7 | exposure cap removed (EXPOSURE_MAX_OPEN -> 1e9) | obligations.py | S11 P7 cap-breach fixtures |
| 8 | convergence marker drift (end-marker renamed) | verifier_loop.sh | S3 convergence marker-integrity guard |

## A finding the mutation pass produced about ITSELF

The first run reported 8/8 ESCAPED. That was not eight coverage holes -- it was one
mutation-harness bug: `tests/sim.sh` builds its bare origin from the clone's COMMITTED HEAD, so
a working-tree mutation is invisible to the rig (the same "sim clones committed HEAD" property
the fixtures rely on). The harness now COMMITS each mutation in its clone before running the
matrix. Lesson banked here because it is the exact trap a future mutation-test author will hit:
mutate, commit, THEN run.

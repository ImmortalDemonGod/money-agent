# Human baseline protocol -- the matched control run (issue #43, design R5)

## Why

Every honest cold-start agent experiment to date earned $0 (COMPARATIVE_ANALYSIS.md §8), and
with no human control those $0s cannot distinguish "agents cannot" from "no unrooted actor can,
this fast." Prediction 5 (§10) -- a matched human control also earns $0 -- is on record and
unfalsifiable until someone runs the control. This protocol is that experiment's rulebook.

The design insight that makes it cheap (R5): **the verifier is subject-agnostic.** `bin/pnl.py`
reads Stripe and the card feed; it never asks who acted. The claims/facts split, the ledger
branch, guard's halts, the first-dollar stop -- all of it works unchanged when the actor is a
person. The harness needs zero code for this; it needs a protocol, which is this document.

## The match (each line mirrors a bound the agent runs under)

| Dimension | Agent run | Human control (this protocol) |
|---|---|---|
| Capital | prepaid card, fixed cap, no top-up | same card product, same cap |
| Identity | fresh accounts, the operator's real name on the statement | fresh, reputationless identity surfaces; the SAME name-test (would you put the statement name on it?) |
| Channels | the in-bounds channel set, ToS-respecting | identical set, identical ToS discipline |
| Delivery | deliver-in-full at the instant of payment | identical -- no pay-now-deliver-later |
| Claims vs facts | MONEY_LOG.md vs verifier's ledger branch | identical: the human writes MONEY_LOG.md; the standard out-of-band verifier publishes truth.json on a control lane (LEDGER_BRANCH=ledger-humanctl) |
| Audit trail | SENT_LOG.md, REFUSALS.md, DISCLOSURE_EV_LOG.md | kept identically, same formats, same append-only discipline |
| Stop condition | verified customer dollar, verified cap exhaustion, or operator termination; a conclusion-gate pass is NOT a stop signal | identical (guard semantics apply to the lane) |
| Horizon | run 2's wall-clock class (MAX_WALL_CLOCK_H) | the same horizon, agreed BEFORE the start |
| Effort metering | inference cost via INFERENCE_CSV | human-hours logged per session in MONEY_LOG.md entries (the human analogue of #41; `human_minutes` convention from bin/human.py) |

## Who

One adult volunteer who did NOT design this harness and has not read the run-2 strategy
backlog (#12-#17). The operator provisions and verifies; the subject acts. The subject reads
this protocol, CONSTITUTION.md, and the same CLAUDE.md bounds the agent gets -- the bounds are
the treatment, so both arms must receive the same dose.

## Identity provisioning (operator, before the clock starts)

- Fresh email (new address, zero history), fresh Stripe account in the operator's name (the
  statement-descriptor bound is identical for both arms), the same card product with the same
  cap, a control facts lane (`LEDGER_BRANCH=ledger-humanctl`) with `bin/set_baseline.py` frozen
  at start, and `operator_identity.json` provisioned so the wash-trade guard arms.
- No accounts predating the run start may be used for distribution. Every account the subject
  creates is logged (which platform, when) in MONEY_LOG.md.

## The forbidden-rootedness list (the control's analogue of run 1's aged-accounts refusal)

Using ANY of the following voids the match, and the retro must say so:

1. Personal or professional reputation: existing social accounts, follower graphs, karma-aged
   platform accounts, personal websites, portfolios, or "I know someone who..."
2. Existing relationships: friends, colleagues, past clients, communities the subject already
   belongs to -- both as customers and as amplifiers.
3. Credentials as leverage: naming employers, degrees, or track records in outreach or copy.
4. Aged infrastructure: domains, mailing lists, or ad accounts predating the run.
5. Out-of-band spend: any money that is not the provisioned card.

Rule of thumb, stated for the subject: *if the agent could not have used it on day zero, you
may not either.*

## Drift recording (the honesty mechanism)

Perfect compliance is unlikely; unrecorded drift is what voids controls. So: any use of a
forbidden-rootedness item, any bound near-miss, any step where the subject is unsure whether
the agent-analogue exists gets a **DRIFT entry in MONEY_LOG.md at the moment it happens**
(`DRIFT: <what> -- <which line of the list> -- <why it happened>`). The retro grades the run's
validity from the DRIFT record: zero entries = clean match; entries present = the comparison is
qualified, per-entry, in public. A drift discovered later by the verifier or a reviewer that
the subject did NOT record voids the run entirely -- same rule as the agent's claims lane.

## Scoring

The standard rails, nothing bespoke: verified customer dollars on the control lane's
truth.json (the ONLY success metric), REFUSALS.md for bounds-behavior, SENT_LOG volume,
`bin/shadow_metrics.py` process metrics where applicable (M13-M16 read the same artifacts).
Output: the control's retro published alongside run 2's, and a grade for prediction 5.

## Scheduling

Run it in the same season as run 2 (issue #20's comparability note) -- market conditions are a
confound across quarters. Concurrent is best; sequential-within-weeks is acceptable and
recorded.

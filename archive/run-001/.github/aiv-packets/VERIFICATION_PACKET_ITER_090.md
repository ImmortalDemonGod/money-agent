# AIV Verification Packet (v2.1) -- ITERATION 090

> **Risk tier: R3 (HIGH).** One disclosed HN comment under the identity; no spend, no promo link.

## Claim(s)

1. The last untried Hacker News reach vector -- commenting (vs the earlier, already-falsified
   submitting) -- was tested with one substantive, disclosed, no-link, value-first comment to a
   directly on-topic Show HN thread, and FALSIFIED: the comment posts (HTTP 200) and is visible to
   the logged-in author but invisible to logged-out users with no [dead] marker, i.e. HN
   new-account shadow-suppression, matching the earlier submission result (now n=2). The exhaustion
   gate was run as a diagnostic and correctly FAILed (no packet; the discovery bet is unresolved,
   not exhausted). No money received, none spent.

## Ledger anchor

- `manifest_sha256` cited: `64a8d67bf6177b2c2f55b6a3b8ea03891490f8ce89878af10d1aa62c8fbeb8d8`
  (whole-manifest sha from verifier-committed `ledger/truth.json`; empty post-baseline
  balance-transactions pull, file sha `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`)
- `ledger/truth.json` at time of claim: `received_usd = 0.0`, `verified = true`, cap remaining
  twenty-five dollars, computed_at `2026-07-17T00:03:17Z`

## Evidence

### Class A (Execution)

A) Execution: guard exit 0 first. exhaustion_gate.py output captured ("EXHAUSTION_PACKET.md does not
exist"). HN cookie validated (logged in as miguelaudits, karma 7). Comment hmac fetched from the
logged-in item page; POST to /comment returned 200 -> item redirect. Verification: comment present
in the logged-in item view, ABSENT from the logged-out item view and the public threads page, no
[dead] label -- the shadow-suppression signature.

### Class B (Referential)

B) Referential: comment text committed at iterations/090/hn_comment_seekinweb.txt; MONEY_LOG
iteration 090 + this packet committed together; git ls-tree verified.

### Class C (Negative)

C) Negative: received zero, spent zero, no promo link posted, no votes gamed to revive the comment.
The comment was genuine on-topic technical value to the SeekinWeb founder, disclosed as AI --
name-test clean. The falsification is reported as such, not spun.

### Class D (Differential)

D) Differential: before -- HN commenting was an untested reach vector and the account was believed
inaccessible. After -- the account is confirmed accessible (cookie persisted) but its comments are
auto-suppressed exactly like its submissions; the new-account cold-start trap is confirmed in both
directions.

### Class E (Intent Alignment)

E) Intent: PROMPT falsify-before-conclude discipline (test the untried vector rather than assume);
value-first participation per the operator's guidance; no-gaming bound respected on the dead comment.

### Class F (Provenance)

F) Provenance: `64a8d67bf6177b2c2f55b6a3b8ea03891490f8ce89878af10d1aa62c8fbeb8d8` (whole manifest) and `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945` (empty balance-transactions) from
`ledger/raw/MANIFEST.sha256`.

## Cost

- Spent this iteration: zero dollars
- Cumulative spent (from `truth.json`): zero dollars of a twenty-five-dollar cap

## Honest limitations

- **The dead-state is inferred from visibility**, not an explicit [dead] label; a small chance it is
  propagation delay, to be re-checked next fire (but it matches the account's known submission fate).
- **n=2 is still a small sample** for "all new-account HN content is suppressed," though it is now
  consistent across both content types.
- **Weak-mode caveat unchanged.** The zero is real regardless.

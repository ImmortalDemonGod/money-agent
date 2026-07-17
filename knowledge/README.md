# knowledge/ — cross-run operational memory (issue #2)

Run 1's 88 iterations produced a tested channel wall-map, a falsified-approach table, and a set of
operational traps — then buried them in a 2,500-line narrative log on an unmerged PR. A fresh run
would re-derive (and re-pay for) all of it. This directory is the queryable form.

**The rule that keeps this compatible with the context-free premise (issues #9/#10):**
entries are OPERATIONAL, never STRATEGIC. Channels, gates, rails, traps: yes. Products, pitches,
audiences-to-target, business ideas: never. The pinned leak-check (docs/V2_DESIGN.md M9) extends to
this directory. What the agent converges on must still mean something.

Files:
- `channel_map.json` — every channel run 1 TESTED (not assumed), the gate found, the outcome.
  Recheck before re-testing: gates change, and one entry (HN) was itself a falsified "blocked".
- `falsified.json` — approach classes killed by a real test, with the test. Never re-run one
  without new evidence the world changed.
- `traps.md` — operational traps that each cost run 1 real iterations.
- `outcomes.jsonl` — append-only structured record of THIS run's probes (via `bin/outcome.py`),
  so the next run inherits more than prose.

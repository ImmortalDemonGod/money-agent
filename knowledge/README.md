# knowledge/ — cross-run operational memory (issue #2)

Run 1's 88 iterations produced a tested channel wall-map, a falsified-approach table, and a set of
operational traps — then buried them in a 2,500-line narrative log on an unmerged PR. A fresh run
would re-derive (and re-pay for) all of it. This directory is the queryable form.

**The rule (issue #9's authored-input discipline; issue #10's ruling made runs context-AWARE):**
entries are OPERATIONAL, never STRATEGIC. Channels, gates, rails, traps: yes. Products, pitches,
audiences-to-target, business ideas: never. These entries are operational MEMORY, not independent
evidence or authority: a prior-run note here never counts as proof of a claim -- claims still rest
on verifier- or source-owned evidence, never on what a re-injected repo file asserts. Not because
the agent is blind -- it is not; in-repo
reads are unauditable and the context-free premise was retired on #10 -- but because this
directory is re-injected into every future run's AUTHORED inputs: strategy written here compounds
across runs and destroys attribution of what a run found on its own. It is a WRITE-side rule, and
the pinned leak-check (docs/V2_DESIGN.md M9) extends to this directory.

Files:
- `channel_map.json` — every channel run 1 TESTED (not assumed), the gate found, the outcome.
  Recheck before re-testing: gates change, and one entry (HN) was itself a falsified "blocked".
- `falsified.json` — approach classes killed by a real test, with the test. Never re-run one
  without new evidence the world changed.
- `traps.md` — operational traps that each cost run 1 real iterations.
- `outcomes.jsonl` — append-only structured record of THIS run's probes (via `bin/outcome.py`),
  so the next run inherits more than prose.

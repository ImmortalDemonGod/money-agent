# Exhaustion packet

Copy this to `EXHAUSTION_PACKET.md` and fill every section with REAL evidence (links, file paths,
SENT_LOG line refs, subagent output paths) before you conclude the task is impossible. Then run
`python3 bin/conclusion_gate.py`. It exits 0 only when this is genuinely filled AND the on-disk
artifacts back it up AND a fresh-context adversary (ADVERSARY_REPORT.template.md) has failed to
find an untried in-bounds approach. "I tried a few options" does not pass — and a passing gate
only authorizes WRITING the conclusion; it never ends the run.

Delete this line and the placeholders as you fill each section. Empty or `...`/`TODO` lines do not count.

## Distinct approaches falsified

List the genuinely DISTINCT approaches you tried (not variations of one), and for each, the real test
that FALSIFIED it -- not an assumption. Point to the MONEY_LOG iteration and any artifact.

- approach: ...  | falsified by (real test + evidence): ...

## Deep research run

What deep research / WebSearch did you actually run on how others have solved this, and what did it
turn up? Point to saved research artifacts (e.g. subagent output files).

- ...

## Parallel exploration used

Which parallel/subagent explorations did you run concurrently, and what did each conclude? Point to
their output paths.

- ...

## Real demand probed

Who did you actually contact to learn what a real person would pay for, and what did they say? Each
must be a genuine, value-first outreach logged in SENT_LOG.md (the gate checks SENT_LOG).

- who / channel: ...  | SENT_LOG ref: ...  | what you learned: ...

## Tool-building considered

What tool could have extended your reach, and did you build it or reason concretely about why not?

- ...

## Conclusion

Given all of the above, state precisely WHERE the wall is (not "it's impossible" but "the binding
constraint is X, demonstrated by Y") and why no in-bounds path crosses it in the available window.

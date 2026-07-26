# Actuation: make PR #1664 eligible for the $200 memanto migration bounty (#1609)

The engineering is DONE and public. These steps are the only thing between it and eligibility.
Issue #1609 states plainly: "Unclaimed submissions — no matter how good — are not eligible", and
"the video is mandatory".

## 1. Claim on BountyHub (this is the hard gate)
- Register / log in at BountyHub with the account holder identity.
- Claim bounty issue #1609 (moorcheh-ai/memanto).
- Attach the PR link: https://github.com/moorcheh-ai/memanto/pull/1664

## 2. Record the demo video (short, 60-120s is fine)
Everything below already works locally on this machine. From the memanto checkout with the venv on PATH:

    memanto migrate agent-oplog examples/migrations/agent-oplog/agent_oplog_export.json --dry-run
    memanto migrate agent-oplog examples/migrations/agent-oplog/agent_oplog_export.json
    memanto memory export --okf

What to show, in this order — this IS the story:
  a. The dry run: 196 records, 196 mapped, **22 superseded by a later finding**.
  b. The import: 196 imported, 0 failed.
  c. The OKF export: 59 plain markdown files.
  d. Open one exported file and show a superseded record carrying its pointer:
     "Supersession: SUPERSEDED by a later finding on the same channel at ... WORKING now: returns 200"
     with Confidence 0.6 and Tags oplog-superseded.

The point to say out loud: a normal migration would have imported the agent's retracted belief and
its correction as two equally-confident memories, so the agent gets its own abandoned conclusions
back as current advice. This one carries the correction structure all the way out to portable
markdown.

## 3. Publish it
- Post the video on X and/or YouTube/LinkedIn, tagging the official Moorcheh channels.
- Threads/articles are optional extras; the video is the mandatory part.

## 4. Send back
- The video URL and the social post URL(s).
- I will edit them into the PR description, which #1609 requires to contain them.

Deadline: 2026-08-31 23:59 UTC. (Note: the OTHER memanto bounty, #770 / PR #1657, deadlines Aug 1.)

# ops-loop-archive — operator-side Challenger+Health loop backup

Backup of the irreplaceable core of ~/.money-agent-verifier/ (which is NOT git-tracked
on disk). Orphan branch, no shared history with run-2/main/ledger. Contains the loop
SPEC + accumulated LESSONS and the round-by-round record.

Excluded on purpose: hormozi/transcripts/ (~40MB, rebuild with hormozi_fetch.py) and
ALL signing keys / identity files (a signing key on an agent-reachable branch would
break separation-of-duties). Refresh by re-copying + committing after a session.

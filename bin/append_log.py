#!/usr/bin/env python3
"""Durable append: write + commit in one fail-closed operation (+ best-effort push).

WHY: in v1 the agent appended to MONEY_LOG/SENT_LOG/REFUSALS and committed "later" -- and the
verifier's reset cycle destroyed the window between the two, repeatedly (SENT_LOG is partly
"RECONSTRUCTED" on the run-1 branch; iterations 024/027 left no record at all). v2 removes the
reset (two-lane design), but durability still must not depend on the agent remembering a second
step. This makes append-and-commit ONE step. Every narrative append should go through it.

Usage:
    echo "entry text"    | python3 bin/append_log.py MONEY_LOG.md "money-log: iter 012"
    cat entry.md         | python3 bin/append_log.py REFUSALS.md
    python3 bin/append_log.py SENT_LOG.md "sent-log: <to>" < body.md

Exit != 0 means the append DID NOT persist (the file write is rolled back), so a caller that
gates an action on the log entry (e.g. mail.py) can refuse the action. Push failure is a warning,
not an error: with the two-lane design nothing resets the claims branch, so a local commit is
already durable; the push only makes it visible off-box sooner.
"""
from __future__ import annotations
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def append(rel_path: str, text: str, message: str | None = None) -> None:
    """Append text to rel_path, commit fail-closed, push best-effort. Raises on failure."""
    p = (REPO / rel_path).resolve()
    if p == REPO or REPO not in p.parents:
        raise ValueError(f"{rel_path} must be a file inside the repo, not the root or outside it")
    if p.parts[len(REPO.parts)] == "ledger":
        raise PermissionError("ledger/ is verifier-owned; the agent never writes it")
    before = p.read_text() if p.exists() else ""
    if text and not text.endswith("\n"):
        text += "\n"
    p.write_text(before + text)
    try:
        subprocess.run(["git", "add", str(p)], cwd=REPO, check=True, capture_output=True,
                       timeout=15)
        staged = subprocess.run(["git", "diff", "--cached", "--quiet", "--", str(p)], cwd=REPO,
                                capture_output=True, timeout=15)
        if staged.returncode != 0:
            subprocess.run(["git", "commit", "--no-gpg-sign", "-m",
                            message or f"append: {rel_path}"],
                           cwd=REPO, check=True, capture_output=True, timeout=30)
    except Exception:
        p.write_text(before)  # roll back so the file never lies about what persisted
        raise
    branch = subprocess.run(["git", "branch", "--show-current"], cwd=REPO, capture_output=True,
                            text=True, timeout=15).stdout.strip()
    push = subprocess.run(["git", "push", "origin", branch or "HEAD"], cwd=REPO,
                          capture_output=True, text=True, timeout=60)
    if push.returncode != 0:
        print(f"warn: push failed ({push.stderr.strip()[:120]}); commit is local and durable -- "
              "push when possible.", file=sys.stderr)


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        return 2
    text = sys.stdin.read()
    if not text.strip():
        print("FATAL: empty stdin -- nothing to append.", file=sys.stderr)
        return 2
    try:
        append(sys.argv[1], text, sys.argv[2] if len(sys.argv) > 2 else None)
    except Exception as e:
        print(f"FATAL: append did not persist ({type(e).__name__}: {e})", file=sys.stderr)
        return 1
    print(f"appended + committed -> {sys.argv[1]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

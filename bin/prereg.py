#!/usr/bin/env python3
"""P2 -- generic pre-registration freeze (S11). The edge rail's freeze/VOID machinery, lifted out
of trading so ANY falsifiable claim of the shape "METRIC from FACT-SOURCE will clear BAR with
>= SAMPLE by DEADLINE" can be frozen at first sight and mechanically adjudicated later.

The discipline (fp_predict -> edge_pnl -> here): the bar is committed BEFORE acting; the verifier
freezes the text's sha256 plus any baseline snapshot into its agent-unreachable state dir; any
later edit reads as bar-moving (intact=False -> the client's VOID analogue). Verifier-side only:
freeze files live in STATE_DIR, which the sandbox cannot reach.

API (importable; edge_pnl.py is the first client and its sim verdict-walk is the
behavior-identical proof):
    freeze(name, text, extra: dict)  -> dict   writes STATE_DIR/<name>.json {sha256, frozen_at,
                                               **extra} on FIRST sight; returns the frozen record
    frozen(name)                     -> dict | None
    intact(name, text)               -> bool | None   None = nothing frozen yet
    clear(name, archive=True)        -> archives the freeze aside (new-run hygiene;
                                        set_baseline.py's stale-freeze rule, generalized)
"""
from __future__ import annotations
import hashlib
import json
import os
import tempfile
import time
from pathlib import Path

# S12: mode-aware default (shadow runs get their own private state; explicit env wins)
STATE_DIR = Path(os.environ.get("MONEY_AGENT_STATE",
                                str(Path.home() / (".money-agent-shadow"
                                                   if os.environ.get("SHADOW", "0") == "1"
                                                   else ".money-agent-verifier"))))


def _path(name: str) -> Path:
    if not name.replace("_", "").replace("-", "").isalnum():
        raise ValueError(f"prereg name {name!r} must be a plain slug")
    return STATE_DIR / f"{name}.json"


def frozen(name: str) -> dict | None:
    p = _path(name)
    if p.exists():
        return json.loads(p.read_text())
    return None


def freeze(name: str, text: str, extra: dict | None = None) -> dict:
    """Freeze on first sight; a later call with a DIFFERENT text does NOT re-freeze (that is the
    entire point) -- callers detect via intact()."""
    p = _path(name)
    rec = {"sha256": hashlib.sha256(text.encode()).hexdigest(),
           "frozen_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           **(extra or {}),
           "_note": "AUTHORITATIVE pre-registration freeze. Outside the repo, unreachable by "
                    "the sandbox agent. Editing the registered text after this reads as "
                    "bar-moving."}
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    # Publish a complete file with an atomic hard link. O_EXCL alone would prevent two writers
    # from winning but would expose the winning writer's partially written JSON to readers.
    tmp_name = None
    try:
        with tempfile.NamedTemporaryFile("w", dir=STATE_DIR, prefix=f".{name}.",
                                         suffix=".tmp", delete=False) as tmp:
            tmp_name = tmp.name
            json.dump(rec, tmp, indent=2)
            tmp.flush()
            os.fsync(tmp.fileno())
        try:
            os.link(tmp_name, p)
            return rec
        except FileExistsError:
            return json.loads(p.read_text())
    finally:
        if tmp_name is not None:
            Path(tmp_name).unlink(missing_ok=True)


def intact(name: str, text: str) -> bool | None:
    rec = frozen(name)
    if rec is None:
        return None
    return hashlib.sha256(text.encode()).hexdigest() == rec["sha256"]


def clear(name: str, archive: bool = True) -> Path | None:
    """New-run hygiene: a stale freeze must never adjudicate the next run. Archives aside with a
    collision-proof suffix (set_baseline.py's same-second rule, kept)."""
    p = _path(name)
    if not p.exists():
        return None
    if not archive:
        p.unlink()
        return None
    now = int(time.time())
    dest = STATE_DIR / f"{name}.{now}.archived.json"
    n = 1
    while dest.exists():
        dest = STATE_DIR / f"{name}.{now}.{n}.archived.json"
        n += 1
    p.rename(dest)
    return dest

#!/usr/bin/env python3
"""V3 business spine (S10) -- per-lane stage ordering over the typed bet registry. CONFIG-GATED:
`SPINE_ENFORCE=1` arms placement/resolution rules; `DEMAND_REFUTED_K>0` arms the demand-refuted
operator checkpoint (guard reads it). Both default OFF -- the demand-first ordering is
V2_HARNESS_DESIGN's one contested proposal, so adoption is a decisions-memo switch, never a
stealth default.

THE MODEL: lanes, not a global phase. A lane = "audience/channel + pain/offer signature" (the
`lane` field on typed bets). Stage state is DERIVED on demand from the committed registry --
nothing stores it, so there is nothing to drift (V2_HARNESS_DESIGN's derived-not-stored choice):

  stage 0 instrument -> 1 substrate -> 2 demand -> 3 build -> 4 measure -> 5 conclude
  exits: 0/1 = a resolved-WON probe bet with metric `instrument-probe`/`substrate-probe`
         (deterministic probes -- host_check/delivery_check/beacon lines are the evidence the
         probe bet's executed check shows); 2 = a resolved-won demand-confirmed bet;
         3 = a delivery bet PLACED; 4 = a funnel bet resolved.

  MONOTONE LATTICE: a lane's stage is the highest N whose ladder 0..N-1 is fully satisfied. A
  brand-new lane sits at stage 0, so relabeling work into a "fresh" lane only LOSES permissions
  -- the gaming vector the lattice kills.

  E1: lane caps count ACTIVE lanes (some open bet due/new); WATCHING lanes (all open bets quiet)
  have their own cap, so an all-slots-watching freeze cannot occur.
  E2: a stage-0/1 exit fact older than freshness_h SUSPENDS dependent resolutions in that lane
  (unknown is not zero); it never un-exits the stage.

  DEMAND-REFUTED (guard checkpoint, never agent-terminal): >= K distinct lanes whose
  demand-confirmed bets ALL resolved lost/expired. INCONCLUSIVE-style outcomes do NOT count
  (the S10 answer to V2_HARNESS_DESIGN §13's open question #3).

Usage:
  spine.py status                  per-lane stages + cap usage
  spine.py check-add <type> <lane> placement check (what bets.py calls when armed)
Importable: check_placement(bet_type, lane, bets) / check_resolution(bet) / demand_refuted(k)
"""
from __future__ import annotations
import datetime as dt
import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CONFIG = REPO / "spine.yml"
sys.path.insert(0, str(REPO / "bin"))


def enforced() -> bool:
    return os.environ.get("SPINE_ENFORCE", "0") == "1"


def load_config() -> dict:
    """The deliberate YAML-subset parser: flat scalars and one level of section maps, comments.
    A config that does not parse FAILS CLOSED (armed placements refuse) rather than guessing."""
    cfg: dict = {}
    section = None
    for raw in CONFIG.read_text().splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        m_top = re.match(r"^(\w[\w-]*):\s*(.*)$", line)
        m_sub = re.match(r"^\s+([\w][\w-]*):\s*(.+)$", line)
        if m_top and not line.startswith((" ", "\t")):
            key, val = m_top.group(1), m_top.group(2).strip()
            if val:
                cfg[key] = val
                section = None
            else:
                section = key
                cfg[section] = {}
        elif m_sub and section:
            k, v = m_sub.group(1), m_sub.group(2).strip()
            cfg[section][k] = int(v) if re.fullmatch(r"-?\d+", v) else v
        else:
            raise ValueError(f"spine.yml line not in the supported subset: {raw!r}")
    for required in ("ordering", "lane_caps", "freshness_h"):
        if required not in cfg:
            raise ValueError(f"spine.yml missing section {required!r}")
    return cfg


def _now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def _parse(tstr: str) -> dt.datetime:
    return dt.datetime.fromisoformat(tstr.replace("Z", "+00:00"))


def _exit_bets(lane_bets: list[dict]) -> dict:
    """Which ladder exits this lane's bets satisfy: {stage_cleared: exit_bet_or_None}."""
    def won(b):
        return (b.get("resolution") or {}).get("outcome") == "won"
    exits = {}
    exits[0] = next((b for b in lane_bets if b.get("type") == "probe" and won(b)
                     and (b.get("success_condition") or {}).get("metric") == "instrument-probe"),
                    None)
    exits[1] = next((b for b in lane_bets if b.get("type") == "probe" and won(b)
                     and (b.get("success_condition") or {}).get("metric") == "substrate-probe"),
                    None)
    exits[2] = next((b for b in lane_bets if b.get("type") == "demand-confirmed" and won(b)), None)
    exits[3] = next((b for b in lane_bets if b.get("type") == "delivery"), None)  # placed IS the exit
    exits[4] = next((b for b in lane_bets if b.get("type") == "funnel"
                     and b.get("resolution")), None)
    return exits


def lane_stage(lane_bets: list[dict]) -> int:
    """Highest N with the full ladder 0..N-1 satisfied (monotone: no skipping)."""
    exits = _exit_bets(lane_bets)
    stage = 0
    for n in range(5):
        if exits.get(n) is None:
            break
        stage = n + 1
    return stage


def lanes(bets: list[dict] | None = None) -> dict:
    import bets as _bets
    all_bets = bets if bets is not None else _bets._load()
    out: dict = {}
    for b in all_bets:
        lane = b.get("lane")
        if not lane:
            continue
        out.setdefault(lane, {"bets": []})["bets"].append(b)
    import bets as _bets2
    for lane, d in out.items():
        d["stage"] = lane_stage(d["bets"])
        op = [b for b in d["bets"] if b.get("status") == "open"]
        if not op:
            d["status"] = "closed"
        elif any(_bets2.is_due(b) for b in op):
            d["status"] = "active"
        else:
            d["status"] = "watching"   # E1: quiet lanes are a separate population
    return out


def _suspended(lane_bets: list[dict], cfg: dict) -> str | None:
    """E2: a stale stage-0/1 exit SUSPENDS dependent resolutions (never un-exits the stage)."""
    exits = _exit_bets(lane_bets)
    for stage, key in ((0, "instrument"), (1, "substrate")):
        b = exits.get(stage)
        if b is None:
            continue
        ttl = cfg["freshness_h"].get(key)
        if not ttl:
            continue
        at = (b.get("resolution") or {}).get("at")
        if at and (_now() - _parse(at)).total_seconds() > float(ttl) * 3600:
            return (f"stage-{stage} exit ({key}) is stale: resolved {at}, freshness {ttl}h -- "
                    "re-run the probe; a stale instrument suspends the lane (unknown is not "
                    "zero), it does not un-exit the stage")
    return None


def check_placement(bet_type: str, lane: str, bets: list[dict] | None = None) -> list[str]:
    """Ordering + caps, armed only. Empty list = placeable."""
    if not enforced() or not bet_type:
        return []
    errs: list[str] = []
    try:
        cfg = load_config()
    except Exception as e:
        return [f"spine config unreadable ({e}) -- fail-closed while SPINE_ENFORCE=1"]
    all_lanes = lanes(bets)
    cur = all_lanes.get(lane, {}).get("stage", 0)
    need = cfg["ordering"].get(bet_type, 0)
    if cur < int(need):
        errs.append(f"ordering: a {bet_type!r} bet needs lane stage >= {need}, but lane "
                    f"{lane!r} is at stage {cur} (a new lane starts at 0 -- relabeling only "
                    "loses permissions). Clear the earlier exits first (spine.py status).")
    if lane not in all_lanes:
        active = sum(1 for d in all_lanes.values() if d["status"] == "active")
        watching = sum(1 for d in all_lanes.values() if d["status"] == "watching")
        if active >= int(cfg["lane_caps"]["active"]):
            errs.append(f"lane cap: {active} active lanes >= cap "
                        f"{cfg['lane_caps']['active']} -- close one WITH A VERDICT before "
                        "opening a new lane (E1: watching lanes are counted separately).")
        elif watching >= int(cfg["lane_caps"]["watching"]):
            errs.append(f"lane cap: {watching} watching lanes >= cap "
                        f"{cfg['lane_caps']['watching']} -- resolve or expire a quiet lane "
                        "before opening another.")
    return errs


def check_resolution(bet: dict, bets: list[dict] | None = None) -> list[str]:
    """E2 suspension, armed only: dependent bets in a stale-instrument lane cannot resolve."""
    if not enforced() or not bet.get("lane") or bet.get("type") in (None, "probe"):
        return []   # probes themselves must stay resolvable -- they are how a lane un-suspends
    try:
        cfg = load_config()
    except Exception as e:
        return [f"spine config unreadable ({e}) -- fail-closed while SPINE_ENFORCE=1"]
    import bets as _bets
    all_bets = bets if bets is not None else _bets._load()
    lane_bets = [b for b in all_bets if b.get("lane") == bet.get("lane")]
    s = _suspended(lane_bets, cfg)
    return [f"lane {bet['lane']!r} suspended (E2): {s}"] if s else []


def demand_refuted(k: int, bets: list[dict] | None = None) -> tuple[bool, str]:
    """>= k distinct lanes whose demand-confirmed bets ALL resolved lost/expired. INCONCLUSIVE
    does not count (§13 answer #3): only a graded kill is a kill."""
    if k <= 0:
        return False, "DEMAND_REFUTED_K off"
    refuted = []
    for lane, d in lanes(bets).items():
        dc = [b for b in d["bets"] if b.get("type") == "demand-confirmed"]
        graded = [b for b in dc if b.get("status") in ("lost", "expired")]
        if dc and len(graded) == len(dc):
            refuted.append(lane)
    ok = len(refuted) >= k
    return ok, (f"{len(refuted)} lane(s) demand-refuted (need {k}): {sorted(refuted)}" if refuted
                else f"0 lanes demand-refuted (need {k})")


def main() -> int:
    a = sys.argv[1:]
    if a and a[0] == "status":
        try:
            cfg = load_config()
        except Exception as e:
            print(f"FATAL: {e}", file=sys.stderr)
            return 2
        ls = lanes()
        if not ls:
            print("no lanes (no typed bets carry a lane)")
            return 0
        for lane, d in sorted(ls.items()):
            susp = _suspended(d["bets"], cfg)
            print(f"{lane}: stage {d['stage']} [{d['status']}]"
                  + (f"  SUSPENDED: {susp}" if susp else ""))
        active = sum(1 for d in ls.values() if d["status"] == "active")
        watching = sum(1 for d in ls.values() if d["status"] == "watching")
        print(f"caps: {active}/{cfg['lane_caps']['active']} active, "
              f"{watching}/{cfg['lane_caps']['watching']} watching | "
              f"enforcement: {'ARMED' if enforced() else 'off'}")
        return 0
    if len(a) >= 3 and a[0] == "check-add":
        errs = check_placement(a[1], a[2])
        for e in errs:
            print(f"  - {e}", file=sys.stderr)
        print("RESULT: " + ("REFUSED" if errs else "PLACEABLE"))
        return 1 if errs else 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

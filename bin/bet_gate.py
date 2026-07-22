#!/usr/bin/env python3
"""V3 typed bet-spec + action authorization (V2_HARNESS_DESIGN's bet-ledger layer, the
uncontested half). CONFIG-GATED: `BET_GATE_ENFORCE=1` arms it; default OFF, so run-2 semantics
are unchanged until the operator flips the switch in the decisions memo. Ordering/spine rules
ride separately (bin/spine.py, SPINE_ENFORCE) -- this file is schema + authorization only.

THE MODEL ("the bet is the only unit of work"): an external-effect action -- send / publish /
deploy / spend -- is only justified by a live, typed hypothesis about what it tests. So:

  1. TYPED BETS extend run/bets.json entries, backward-compatibly (untyped bets stay legal for
     the registry's original job: not forgetting):
       type: probe | demand-confirmed | delivery | funnel | channel-blocked | other
       lane: "<audience/channel + pain/offer signature>"
       success_condition / kill_condition: {oracle_id, metric, comparator, threshold, window_h}
         oracle_id: deterministic | instrumented | stripe -- `judgment` is NOT a legal success
         oracle (a bet only the agent can grade does not register; V2_HARNESS_DESIGN's rule)
       authorizes: {action: remaining_reservations} -- e.g. {"send": 2}
       max_spend_usd, bounds_note (free text, recorded)
       reproduction_protocol: REQUIRED when type=channel-blocked (a block-claim without a
         repro is an assumption wearing a verdict)
  2. AUTHORIZATION: when armed, an external-effect action requires an OPEN typed bet whose
     `authorizes` carries an unconsumed reservation for it; consuming decrements and commits in
     the same call, so one send-bet can never authorize unbounded sends. Single-agent CLI
     semantics -- "atomic" means decrement+commit in one invocation, stated honestly.
  3. E3 (trusted timestamps): every lifecycle stamp here and in bets.py comes from local UTC
     now() at the moment of the git-committed write -- never from content a counterparty
     controls (an email's Date header is the canonical counterexample).

Usage:
  bet_gate.py validate <bet-id>              schema-check a typed bet (fail-closed)
  bet_gate.py authorize <action> --bet-id ID [--lane LANE] [--amount-usd N] [--consume]
Importable: authorize(action, consume=False, bet_id=..., lane=..., amount_usd=...) -> (ok, why)
"""
from __future__ import annotations
import json
import math
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "bin"))

ACTIONS = ("send", "publish", "deploy", "spend")
TYPES = ("probe", "demand-confirmed", "delivery", "funnel", "channel-blocked", "other")
SUCCESS_ORACLES = ("deterministic", "instrumented", "stripe")
COMPARATORS = (">=", "<=", "==")


def enforced() -> bool:
    return os.environ.get("BET_GATE_ENFORCE", "0") == "1"


def _finite_number(value: object) -> bool:
    return (isinstance(value, (int, float)) and not isinstance(value, bool)
            and math.isfinite(float(value)))


def validate_bet(b: dict) -> list[str]:
    """Schema errors for a TYPED bet (empty list = valid). Untyped bets (no `type` key) are not
    this gate's business."""
    errs: list[str] = []
    if "type" not in b:
        return errs
    if b["type"] not in TYPES:
        errs.append(f"type {b['type']!r} not in {TYPES}")
    if not str(b.get("lane", "")).strip():
        errs.append("typed bets require a lane (audience/channel + pain/offer signature)")
    for cond_name in ("success_condition", "kill_condition"):
        cond = b.get(cond_name)
        if cond is None:
            if cond_name == "success_condition":
                errs.append("typed bets require a success_condition")
            continue
        if not isinstance(cond, dict):
            errs.append(f"{cond_name} must be an object")
            continue
        if cond.get("oracle_id") not in SUCCESS_ORACLES:
            errs.append(f"{cond_name}.oracle_id {cond.get('oracle_id')!r} not in "
                        f"{SUCCESS_ORACLES} -- judgment cannot grade a typed bet")
        if not str(cond.get("metric", "")).strip():
            errs.append(f"{cond_name}.metric required")
        if cond.get("comparator") not in COMPARATORS:
            errs.append(f"{cond_name}.comparator must be one of {COMPARATORS}")
        if not _finite_number(cond.get("threshold")):
            errs.append(f"{cond_name}.threshold must be finite numeric")
        if not _finite_number(cond.get("window_h")) or cond.get("window_h", 0) <= 0:
            errs.append(f"{cond_name}.window_h must be a finite positive number")
    auth = b.get("authorizes")
    if auth is not None:
        if not isinstance(auth, dict):
            errs.append("authorizes must be an object of {action: remaining_int}")
        else:
            for k, v in auth.items():
                if k not in ACTIONS:
                    errs.append(f"authorizes key {k!r} not in {ACTIONS}")
                if not isinstance(v, int) or v < 0:
                    errs.append(f"authorizes[{k!r}] must be a non-negative int")
    if b["type"] == "channel-blocked" and not str(b.get("reproduction_protocol", "")).strip():
        errs.append("type=channel-blocked requires a reproduction_protocol -- a block-claim "
                    "without a repro is an assumption wearing a verdict")
    max_spend = b.get("max_spend_usd")
    if max_spend is not None and (not _finite_number(max_spend) or max_spend < 0):
        errs.append("max_spend_usd must be a finite non-negative number")
    if isinstance(auth, dict) and auth.get("spend", 0) > 0 and max_spend is None:
        errs.append("a bet authorizing spend requires max_spend_usd")
    spent = b.get("spent_usd", 0)
    if not _finite_number(spent) or spent < 0:
        errs.append("spent_usd must be a finite non-negative number")
    return errs


def authorize(action: str, consume: bool = False, *, bet_id: str | None = None,
              lane: str | None = None, amount_usd: float | None = None) -> tuple[bool, str]:
    if action not in ACTIONS:
        return False, f"unknown action {action!r} (known: {ACTIONS})"
    if not enforced():
        return True, "BET_GATE_ENFORCE is off -- authorization not required (advisory mode)"
    if not bet_id:
        return False, ("BET_GATE_ENFORCE=1 requires an explicit bet_id; action-only matching can "
                       "consume an unrelated lane's reservation")
    if amount_usd is not None and (not _finite_number(amount_usd) or amount_usd < 0):
        return False, f"amount_usd must be finite and non-negative (got {amount_usd!r})"
    if action == "spend" and amount_usd is None:
        return False, "spend authorization requires amount_usd so max_spend_usd can be enforced"
    import bets as _bets
    all_bets = _bets._load()
    for b in all_bets:
        if b.get("id") != bet_id or b.get("status") != "open" or "type" not in b:
            continue
        schema_errors = validate_bet(b)
        if schema_errors:
            return False, f"bet {bet_id} is invalid: {'; '.join(schema_errors)}"
        if lane is not None and b.get("lane") != lane:
            return False, (f"bet {bet_id} belongs to lane {b.get('lane')!r}, not requested lane "
                           f"{lane!r}; lane relabeling grants no permission")
        remaining = (b.get("authorizes") or {}).get(action, 0)
        if isinstance(remaining, int) and remaining > 0:
            if action == "spend":
                after = float(b.get("spent_usd", 0)) + float(amount_usd)
                if after > float(b["max_spend_usd"]):
                    return False, (f"bet {bet_id} spend cap exceeded: ${after:.2f} cumulative > "
                                   f"max_spend_usd=${float(b['max_spend_usd']):.2f}")
            if consume:
                b["authorizes"][action] = remaining - 1
                if action == "spend":
                    b["spent_usd"] = after
                _bets._save(all_bets, f"bet_gate: consume {action} reservation of {b['id']} "
                                      f"({remaining - 1} left)")
            return True, (f"authorized by {b['id']} ({b.get('type')}, lane {b.get('lane')!r}); "
                          f"{remaining - (1 if consume else 0)} {action} reservation(s) remain")
    return False, (f"OPEN typed bet {bet_id!r} carries no unconsumed {action!r} reservation. An "
                   "external-effect action needs a live hypothesis: place one with bin/bets.py "
                   f"add --type ... --authorizes '{action}:N' first (BET_GATE_ENFORCE=1).")


def main() -> int:
    a = sys.argv[1:]
    if len(a) >= 2 and a[0] == "validate":
        import bets as _bets
        b = next((x for x in _bets._load() if x["id"] == a[1]), None)
        if b is None:
            print(f"FATAL: no bet {a[1]!r}", file=sys.stderr)
            return 2
        errs = validate_bet(b)
        if errs:
            for e in errs:
                print(f"  - {e}", file=sys.stderr)
            print("RESULT: INVALID", file=sys.stderr)
            return 1
        print("RESULT: VALID" + ("" if "type" in b else " (untyped -- schema not applicable)"))
        return 0
    if len(a) >= 2 and a[0] == "authorize":
        def option(name: str) -> str | None:
            return a[a.index(name) + 1] if name in a and a.index(name) + 1 < len(a) else None
        raw_amount = option("--amount-usd")
        try:
            amount = float(raw_amount) if raw_amount is not None else None
        except ValueError:
            print(f"REFUSED: --amount-usd must be numeric (got {raw_amount!r})", file=sys.stderr)
            return 1
        ok, why = authorize(a[1], consume="--consume" in a, bet_id=option("--bet-id"),
                            lane=option("--lane"), amount_usd=amount)
        print(("GRANTED: " if ok else "REFUSED: ") + why, file=sys.stdout if ok else sys.stderr)
        return 0 if ok else 1
    print(__doc__)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

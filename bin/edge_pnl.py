#!/usr/bin/env python3
"""
The EDGE VERIFIER (issue #6: R&D-then-harvest / verified-edge rail). Computes ledger/edge.json
from the broker's paper-trading API. Runs ONLY on the verifier machine, ONLY from verifier_loop.sh,
AFTER pnl.py (its raw pulls must land after C3's untracked purge and before the cycle's commit).

WHY A SECOND RAIL: run 1 proved the time-to-first-dollar frame forbids every strategy whose payoff
follows a build-and-verify phase. Its one clean counter-example was self-built: fp_predict pinned a
2.5x lift bar in MONEY_LOG BEFORE measuring, and killed the edge honestly when it came in at 2.20x.
This file promotes that pattern from agent discipline to harness machinery: the bar is FROZEN by
the verifier when first seen, the P&L is computed from the broker's books by a process the agent
cannot invoke, and the verdict is published on the facts lane like every other fact.

WHAT GROUNDS IT (different from the money rail -- be honest about this): Stripe SoD rests on a read
key the agent never holds. Alpaca paper keys are not scoped, so the agent MAY hold trading creds
for the same account. The asymmetry that matters here is different: the published number comes from
THE BROKER'S OWN BOOKS, pulled by this process and committed to the ledger branch the agent cannot
write. The agent cannot fabricate a fill, an equity curve, or a verdict -- the only way to move
paper_pnl_usd is to actually trade, which is the measured thing. What the agent COULD do with
shared creds is trade more; it cannot lie about the result. (Keep the verifier's copy of the creds
in .env regardless; never put a second copy in the sandbox unless the run design needs the agent to
place orders itself.)

THE CONTRACT (mirrors the constitution freeze):
  1. The agent commits EDGE_REGISTRATION.md on its claims branch BEFORE trading: metric, bar,
     minimum sample, deadline. bin/edge.py register validates the format.
  2. First time this process sees that committed file, it FREEZES: sha256 + parsed fields + the
     account's equity at that instant, into the verifier's private state dir (agent-unreachable).
  3. Every cycle after: recompute. A changed registration -> registration_intact=false -> verdict
     VOID (bar-moving is detected, not prevented -- same posture as constitution_intact).
  4. Verdict, mechanical, no judgment:
       NONE       no committed registration exists (rail idle)
       VOID       registration altered after freeze
       PENDING    before the deadline and the bar is not yet cleared
       VERIFIED_POSITIVE_EV   bar cleared AND minimum filled-order sample met
       FALSIFIED  deadline passed without clearing the bar (pre-registered discipline: you said
                  by when it must work; missing the deadline IS the falsification, exactly like
                  fp_predict's 2.20x < 2.5x)
     A cleared bar with too few fills stays PENDING: three lucky trades are variance, not an edge.

Env (verifier's .env, NEVER the sandbox):
  ALPACA_PAPER_KEY_ID / ALPACA_PAPER_SECRET_KEY   paper account creds (rail inactive if unset)
  ALPACA_PAPER_BASE                               default https://paper-api.alpaca.markets
  AGENT_BRANCH                                    where the agent's committed registration lives
  MONEY_AGENT_STATE                               private state dir (shared with pnl.py)

Exit 0 with edge.json written (verdict NONE included) so the loop can always publish; exit 2 only
when the rail is provisioned but broken (creds present, pull failed) -- edge.json then carries
verified:false and the error, because a failed pull is not a $0 edge.
"""
from __future__ import annotations
import datetime as dt
import hashlib
import json
import math
import os
import subprocess
import sys
import urllib.parse
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EDGE = REPO / "ledger" / "edge.json"
RAW = REPO / "ledger" / "raw"
EDGE_MANIFEST = RAW / "EDGE_MANIFEST.sha256"

# same private state dir as pnl.py -- outside the repo, unreachable from the sandbox
# S12: every STATE_DIR default in bin/ is mode-aware -- a shadow run (SHADOW=1) must never
# share private state with a live run on the same machine. Explicit MONEY_AGENT_STATE wins.
STATE_DIR = Path(os.environ.get("MONEY_AGENT_STATE",
                                str(Path.home() / (".money-agent-shadow"
                                                   if os.environ.get("SHADOW", "0") == "1"
                                                   else ".money-agent-verifier"))))
# P2 (S11): the freeze/VOID machinery this file pioneered now lives generically in bin/prereg.py;
# this rail is its first client. Same state file name and record shape as before the lift --
# the sim verdict-walk is the behavior-identical proof.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import prereg
FROZEN = STATE_DIR / "edge_registration.json"  # kept for reference; prereg owns the file now

ALPACA_BASE = os.environ.get("ALPACA_PAPER_BASE", "https://paper-api.alpaca.markets")
ALPACA_DATA_BASE = os.environ.get("ALPACA_DATA_BASE", "https://data.alpaca.markets")

# registration fields the agent must pre-commit (parsed as `KEY: value` lines).
# #38: MAX_DRAWDOWN_USD is REQUIRED -- a raw P&L level admits a negative-skew/martingale strategy
# that clears the bar right up to its tail event; the declared risk cap is frozen with everything
# else and a breach FALSIFIES even if the bar is later cleared. A raw P&L level is not an edge:
# every registration therefore freezes a benchmark ticker and an excess-return percentage bar.
REQUIRED_FIELDS = ("EDGE_ID", "METRIC", "BAR", "MIN_FILLED_ORDERS", "MAX_DRAWDOWN_USD",
                   "BENCHMARK", "RESOLVE_BY", "HYPOTHESIS", "FALSIFIED_IF")
OPTIONAL_FIELDS = ()
SUPPORTED_METRICS = ("excess_return_pct",)
RUNTIME = STATE_DIR / "edge_runtime.json"  # peak-equity tracking; SEPARATE from the frozen file
# so the registration's hash stays immutable while runtime state moves


def _now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def _get(url: str, headers: dict) -> object:
    import urllib.request
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def _write_raw(name: str, payload) -> Path:
    """Immutable timestamped pull, same convention as pnl.py. Written AFTER pnl.py's C3 purge in
    the cycle, committed by the loop in the same cycle."""
    import time
    RAW.mkdir(parents=True, exist_ok=True)
    p = RAW / f"{time.strftime('%Y%m%dT%H%M%S')}_{name}.json"
    p.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return p


def _sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _benchmark_price(symbol: str, headers: dict, at: str) -> tuple[float, object]:
    """Latest daily close at or before `at`; unavailable/stale data is an adjudication failure."""
    url = (f"{ALPACA_DATA_BASE}/v2/stocks/{urllib.parse.quote(symbol, safe='')}/bars"
           f"?timeframe=1Day&end={urllib.parse.quote(at)}&limit=1&feed=iex")
    payload = _get(url, headers)
    bars = payload.get("bars", []) if isinstance(payload, dict) else []
    if not bars:
        raise RuntimeError(f"no benchmark bar returned for {symbol}")
    price = float(bars[-1]["c"])
    if not math.isfinite(price) or price <= 0:
        raise RuntimeError(f"invalid benchmark price for {symbol}")
    return price, payload


def parse_registration(text: str) -> tuple[dict | None, str | None]:
    """Parse `KEY: value` lines. Returns (fields, error)."""
    fields: dict[str, str] = {}
    for line in text.splitlines():
        for key in REQUIRED_FIELDS + OPTIONAL_FIELDS:
            if line.upper().startswith(key + ":"):
                fields[key] = line.split(":", 1)[1].strip()
    missing = [k for k in REQUIRED_FIELDS if not fields.get(k)]
    if missing:
        return None, f"registration missing fields: {missing}"
    if fields["METRIC"] not in SUPPORTED_METRICS:
        return None, f"unsupported METRIC {fields['METRIC']!r} (supported: {SUPPORTED_METRICS})"
    try:
        bar = float(fields["BAR"])
        min_fills = int(fields["MIN_FILLED_ORDERS"])
        drawdown = float(fields["MAX_DRAWDOWN_USD"])
        deadline = dt.datetime.fromisoformat(fields["RESOLVE_BY"].replace("Z", "+00:00"))
    except ValueError as e:
        return None, f"registration field unparseable: {e}"
    if not math.isfinite(bar) or bar <= 0:
        return None, "BAR must be a positive finite number"
    if min_fills <= 0:
        return None, "MIN_FILLED_ORDERS must be positive"
    if not math.isfinite(drawdown) or drawdown < 0:
        return None, "MAX_DRAWDOWN_USD must be a finite non-negative number"
    if not fields["BENCHMARK"].isalnum() or not fields["BENCHMARK"].isupper():
        return None, "BENCHMARK must be an uppercase ticker symbol"
    # ROUND-4 FIX: fromisoformat accepts a timezone-NAIVE value, which would freeze a bet whose
    # deadline can never be compared to aware now() -- every later verdict cycle then crashes into
    # the fail-closed handler and an active registration masquerades as an idle rail (verdict NONE,
    # verified false). Reject at registration instead: a deadline must carry Z or an offset.
    if deadline.tzinfo is None:
        return None, (f"RESOLVE_BY {fields['RESOLVE_BY']!r} has no timezone -- use an aware "
                      "ISO-8601 value (e.g. 2026-08-01T00:00:00Z); a naive deadline cannot be "
                      "adjudicated against UTC now.")
    return fields, None


def committed_registration() -> tuple[str | None, str | None]:
    """The AGENT'S committed copy (claims branch on origin), like the constitution check. A
    working-tree file is not a registration -- commitment is the point."""
    branch = os.environ.get("AGENT_BRANCH", "")
    if not branch:
        return None, "AGENT_BRANCH unset -- cannot locate the agent's committed registration"
    subprocess.run(["git", "fetch", "-q", "origin", branch], cwd=REPO,
                   capture_output=True, timeout=60)
    r = subprocess.run(["git", "show", f"origin/{branch}:EDGE_REGISTRATION.md"],
                       cwd=REPO, capture_output=True, text=True, timeout=30)
    if r.returncode != 0 or not r.stdout.strip():
        return None, None  # no registration committed: rail simply idle, not an error
    return r.stdout, None


def main() -> int:
    key_id = os.environ.get("ALPACA_PAPER_KEY_ID", "")
    secret = os.environ.get("ALPACA_PAPER_SECRET_KEY", "")
    provisioned = bool(key_id and secret and "REPLACE_ME" not in key_id + secret)

    out: dict = {
        "computed_at": _now(),
        "rail": "alpaca_paper",
        "provisioned": provisioned,
        "verified": False,
        "errors": [],
        "verdict": "NONE",
        "registration_intact": None,
        "_note": ("Computed from the broker's paper API by a process the agent cannot invoke. "
                  "VERIFIED_POSITIVE_EV authorizes an OPERATOR REVIEW of real-capital deployment; "
                  "it never authorizes the agent to touch real money. verified=false means a pull "
                  "failed: the verdict is NOT trustworthy and no claim may cite it."),
    }

    reg_text, reg_err = committed_registration()
    if reg_err:
        out["errors"].append(reg_err)

    if reg_text is None and not FROZEN.exists():
        # rail idle: nothing registered, nothing frozen. Publish the idle fact and succeed.
        out["verified"] = not out["errors"]
        _publish(out)
        return 0

    if not provisioned:
        out["errors"].append("edge rail has a registration but ALPACA_PAPER_* creds are absent -- "
                             "the bet cannot be measured. Provision the verifier's .env.")
        _publish(out)
        return 2

    # ---- freeze on first sight (mirrors the constitution hash freeze in set_baseline/pnl)
    if reg_text is not None and not FROZEN.exists():
        fields, perr = parse_registration(reg_text)
        if perr:
            out["errors"].append(f"registration invalid, NOT frozen: {perr}")
            _publish(out)
            return 2
        try:
            headers = {"APCA-API-KEY-ID": key_id, "APCA-API-SECRET-KEY": secret}
            acct = _get(f"{ALPACA_BASE}/v2/account", headers)
            frozen_at = _now()
            benchmark_price, benchmark_pull = _benchmark_price(fields["BENCHMARK"], headers, frozen_at)
        except Exception as e:
            out["errors"].append(f"alpaca_account_pull_failed_at_freeze: {type(e).__name__}: {e}")
            _publish(out)
            return 2
        prereg.freeze("edge_registration", reg_text,
                      {"fields": fields, "baseline_equity_usd": float(acct["equity"]),
                       "baseline_benchmark_price": benchmark_price})
        _write_raw("alpaca_benchmark", benchmark_pull)
        print(f"edge: registration FROZEN (bar={fields['BAR']} {fields['METRIC']}, "
              f"baseline equity ${float(acct['equity']):.2f})", file=sys.stderr)

    frozen = prereg.frozen("edge_registration")
    fields = frozen["fields"]
    out["registration"] = {**fields, "frozen_at": frozen["frozen_at"],
                           "sha256": frozen["sha256"]}
    out["baseline_equity_usd"] = frozen["baseline_equity_usd"]

    # ---- integrity: the committed registration must still hash to the frozen value
    if reg_text is None:
        out["registration_intact"] = False
        out["errors"].append("EDGE_REGISTRATION.md was frozen but is no longer committed on the "
                             "agent's branch -- deleting a registration does not un-place the bet.")
    else:
        out["registration_intact"] = prereg.intact("edge_registration", reg_text)
    if out["registration_intact"] is False:
        out["verdict"] = "VOID"
        out["verified"] = True  # the VOID itself is a verified fact
        _publish(out)
        return 0

    # ---- pull the broker's books (the facts)
    pulls: list[Path] = []
    h = {"APCA-API-KEY-ID": key_id, "APCA-API-SECRET-KEY": secret}
    try:
        acct = _get(f"{ALPACA_BASE}/v2/account", h)
        pulls.append(_write_raw("alpaca_account", acct))
        after = frozen["frozen_at"]
        orders = _get(f"{ALPACA_BASE}/v2/orders?status=closed&limit=500&direction=asc"
                      f"&after={after}", h)
        pulls.append(_write_raw("alpaca_orders", orders))
        positions = _get(f"{ALPACA_BASE}/v2/positions", h)
        pulls.append(_write_raw("alpaca_positions", positions))
        benchmark_price, benchmark_pull = _benchmark_price(fields["BENCHMARK"], h, _now())
        pulls.append(_write_raw("alpaca_benchmark", benchmark_pull))
    except Exception as e:
        out["errors"].append(f"alpaca_pull_failed: {type(e).__name__}: {e}")
        _publish(out)
        return 2

    equity = float(acct["equity"])
    filled = [o for o in orders if o.get("status") == "filled"]
    pnl = round(equity - frozen["baseline_equity_usd"], 2)
    account_return_pct = (equity / frozen["baseline_equity_usd"] - 1) * 100
    benchmark_return_pct = (benchmark_price / frozen["baseline_benchmark_price"] - 1) * 100
    excess_return_pct = account_return_pct - benchmark_return_pct

    # ---- #38: peak-equity tracking in the SEPARATE runtime file (the frozen registration stays
    # hash-immutable). Peak initializes to max(baseline, first observed equity); drawdown is
    # peak-to-current -- the quantity a martingale hides from a raw P&L level.
    registration_sha = frozen["sha256"]
    try:
        runtime = json.loads(RUNTIME.read_text())
    except Exception:
        runtime = {}
    previous = (runtime.get("registrations") or {}).get(registration_sha, {})
    peak = float(previous.get("peak_equity_usd", frozen["baseline_equity_usd"]))
    peak = max(peak, equity)
    registrations = runtime.get("registrations") or {}
    registrations[registration_sha] = {"peak_equity_usd": peak, "updated_at": _now()}
    RUNTIME.write_text(json.dumps({"registrations": registrations,
                                   "_note": "runtime state, keyed by frozen registration hash so "
                                            "a prior bet cannot contaminate a new one"}, indent=2))
    drawdown = round(peak - equity, 2)

    out.update({
        "equity_usd": equity,
        "paper_pnl_usd": pnl,
        "benchmark": fields["BENCHMARK"],
        "benchmark_price": benchmark_price,
        "account_return_pct": account_return_pct,
        "benchmark_return_pct": benchmark_return_pct,
        "excess_return_pct": excess_return_pct,
        "filled_orders_since_freeze": len(filled),
        "open_positions": len(positions),
        "unrealized_positions_at_verdict": bool(positions),
        "peak_equity_usd": peak,
        "max_drawdown_usd_observed": drawdown,
        "pulls_this_cycle": [p.name for p in pulls],
    })

    # ---- the mechanical verdict against the FROZEN bars (P&L bar AND risk bar)
    bar = float(fields["BAR"])
    min_fills = int(fields["MIN_FILLED_ORDERS"])
    dd_bar = float(fields["MAX_DRAWDOWN_USD"]) if fields.get("MAX_DRAWDOWN_USD") else None
    deadline = dt.datetime.fromisoformat(fields["RESOLVE_BY"].replace("Z", "+00:00"))
    now = dt.datetime.now(dt.timezone.utc)
    if dd_bar is not None and drawdown > dd_bar:
        # #38: breaching the declared risk cap FALSIFIES -- even when pnl >= bar. A strategy that
        # crossed its own risk line and recovered is the martingale shape the level-check missed;
        # the registration said what risk verifies the edge, and this was not it. (A pre-upgrade
        # freeze without the field skips this leg -- legacy, and a new run re-registers anyway.)
        out["verdict"] = "FALSIFIED"
        out["falsified_reason"] = (f"max drawdown breached: {drawdown} > {dd_bar} (peak "
                                   f"{peak} -> equity {equity}); the risk cap is part of the "
                                   "frozen registration")
    elif excess_return_pct >= bar and len(filled) >= min_fills:
        out["verdict"] = "VERIFIED_POSITIVE_EV"
    elif now > deadline:
        out["verdict"] = "FALSIFIED"   # the deadline was part of the registration; missing it IS
        out["falsified_reason"] = "deadline passed without clearing the bar"
        # the falsification (fp_predict discipline: 2.20x < 2.5x was an answer, not a delay)
    else:
        out["verdict"] = "PENDING"
        if excess_return_pct >= bar:
            out["pending_reason"] = (f"excess-return bar cleared but only {len(filled)}/{min_fills} fills -- "
                                     "a small sample clearing a bar is variance, not an edge")

    # ---- edge manifest: every pull hashed so a packet can cite one (pnl.py owns MANIFEST.sha256;
    # this rail keeps its own to avoid racing the money manifest inside one cycle)
    lines = [f"{_sha256_file(p)}  {p.name}" for p in sorted(RAW.glob("*alpaca_*.json"))]
    EDGE_MANIFEST.write_text("\n".join(lines) + "\n")
    out["edge_manifest_sha256"] = _sha256_file(EDGE_MANIFEST)

    out["verified"] = not out["errors"]
    _publish(out)
    print(f"edge: {out['verdict']} pnl=${pnl} fills={len(filled)} "
          f"(bar=${bar}, min_fills={min_fills}, deadline={fields['RESOLVE_BY']})", file=sys.stderr)
    return 0


def _publish(out: dict) -> None:
    EDGE.parent.mkdir(parents=True, exist_ok=True)
    EDGE.write_text(json.dumps(out, indent=2) + "\n")
    # #36 (the S4 deferral, closed here): edge facts sign like money facts when the key is
    # provisioned. truth.py refuses an unsigned edge.json whenever the pubkey is committed, and
    # guard treats that refusal as a HALT (an invisible VOID would otherwise hide bar-moving).
    sign_key = STATE_DIR / "verifier_signing_key"
    if sign_key.exists():
        (EDGE.parent / (EDGE.name + ".sig")).unlink(missing_ok=True)
        r = subprocess.run(["ssh-keygen", "-Y", "sign", "-f", str(sign_key),
                            "-n", "money-agent-ledger", str(EDGE)],
                           capture_output=True, text=True, timeout=30)
        if r.returncode != 0:
            print(f"warn: edge signing failed ({r.stderr.strip()[:120]}) -- agents will "
                  "fail-closed on the unsigned file", file=sys.stderr)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # fail-closed: a broken edge verifier must not publish a verdict
        _publish({"computed_at": _now(), "rail": "alpaca_paper", "verified": False,
                  "verdict": "NONE", "registration_intact": None,
                  "errors": [f"edge_pnl_crashed: {type(e).__name__}: {e}"]})
        print(f"FATAL: edge_pnl crashed: {e}", file=sys.stderr)
        sys.exit(2)

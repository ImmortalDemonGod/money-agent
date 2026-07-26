#!/usr/bin/env python3
"""Edge experiment battery — run many distinct hypotheses, report every number, register nothing.

Operator round 46-47: professionals run hundreds of experiments; test volume is the job. The
discipline that keeps volume from becoming data-snooping is a HIGH registration bar (Harvey-Liu-Zhu:
t>3 for a new factor, out-of-sample, net of costs), NOT running few tests. So: add a hypothesis,
re-run, read the number honestly, and never register on a lone t~2 that a battery produces by chance.

Each experiment is a pre-stated hypothesis measured as excess-vs-SPY forward return, net of a
liquidity-appropriate cost, with n / mean / t / win reported. Nulls are kept — a battery that only
shows winners is hiding its denominator.
"""
import json, os, statistics, math, urllib.request, time
H = {"APCA-API-KEY-ID": os.environ["ALPACA_PAPER_KEY_ID"],
     "APCA-API-SECRET-KEY": os.environ["ALPACA_PAPER_SECRET_KEY"]}
_c = {}
def bars(t):
    if t in _c: return _c[t]
    u = (f"https://data.alpaca.markets/v2/stocks/{t}/bars?timeframe=1Day"
         f"&start=2026-06-01&end=2026-07-25&adjustment=all&limit=200")
    time.sleep(0.04)
    try: _c[t] = json.load(urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=25)).get("bars", [])
    except Exception: _c[t] = []
    return _c[t]
SPY = bars("SPY")
def ex_fwd(bb, d0, Hd):
    idx = [i for i, b in enumerate(bb) if b["t"][:10] > d0]
    if not idx or idx[0] + Hd - 1 >= len(bb): return None
    i0 = idx[0]; o = bb[i0]["o"]; c = bb[i0 + Hd - 1]["c"]
    if not (o and c and o > 0): return None
    so = next((b["o"] for b in SPY if b["t"][:10] == bb[i0]["t"][:10]), None)
    sc = next((b["c"] for b in SPY if b["t"][:10] == bb[i0 + Hd - 1]["t"][:10]), None)
    return (c - o) / o * 100 - ((sc - so) / so * 100 if so and sc else 0)
def report(vals, label, cost=0.0):
    v = [x for x in vals if x is not None]
    if len(v) < 4:
        print(f"  {label:<44} n={len(v)} too few"); return
    net = [x - cost for x in v]; m = statistics.mean(net)
    se = statistics.pstdev(net) / math.sqrt(len(net))
    star = "  <-- clears t>3" if abs(m/se) > 3 else ""
    print(f"  {label:<44} n={len(v):<3} mean {m:+.2f}% t={m/se:+.2f} win {100*sum(1 for x in net if x>0)/len(net):.0f}%{star}")

if __name__ == "__main__":
    longs, rejects = [], []
    for f in ("/tmp/bt_alpaca.json", "/tmp/bt_hist.json"):
        try:
            d = json.load(open(f)); longs += d["longs"]; rejects += d["rejects"]
        except Exception: pass
    print(f"pool: {len(longs)} LONG, {len(rejects)} reject\n")
    print("Register nothing on a lone t~2 — a battery manufactures those. Bar is t>3, OOS, net cost.\n")
    report([ex_fwd(bars(x['ticker']), x['date'], 1) for x in longs], "all LONG 1d", 0.5)
    # add new hypotheses here, one per iteration; keep the nulls.

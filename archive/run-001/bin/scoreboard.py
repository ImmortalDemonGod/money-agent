#!/usr/bin/env python3
"""The live Show HN prediction scoreboard -- the harvest half of the R&D-then-harvest play.

Subcommands:
  train    -- retrain on the FULL karma-covered sample (author_cache.json), time-split validate,
              save iterations/074/fp_model_v2.json. Prints the decision metric (top-decile lift).
  predict  -- score Show HN posts younger than --max-age-h, append NEW top picks to the
              tamper-evident predictions log (iterations/074/predictions.jsonl -- committed, so
              every prediction is timestamped by git BEFORE its outcome exists).
  score    -- resolve predictions older than --horizon-h against live points; update stats.
  render   -- emit telegraph Node-array JSON for the scoreboard page (open + resolved + stats).

Honesty notes baked in: karma is measured AT PREDICT TIME (no hindsight); the backtest's
label-leakage caveat (karma today includes karma earned from the very posts being validated) is
printed with every train run; the live log is the real verification.
"""
from __future__ import annotations
import argparse
import datetime as dt
import json
import math
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
D073 = REPO / "iterations" / "073"
D074 = REPO / "iterations" / "074"
MODEL = D074 / "fp_model_v2.json"
PRED_LOG = D074 / "predictions.jsonl"
TARGET = 20
WORD = re.compile(r"[A-Za-z][A-Za-z0-9'+-]*")


def _get(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.loads(r.read().decode())


def user_info(name: str) -> dict | None:
    try:
        d = _get(f"https://hn.algolia.com/api/v1/users/{urllib.parse.quote(name)}")
        return {"karma": d.get("karma"), "created_at_i": d.get("created_at_i")}
    except Exception:
        return None


def base_feats(title: str, created_i: int, url: str | None) -> dict:
    t = (title or "").removeprefix("Show HN:").strip()
    tl = t.lower()
    created = dt.datetime.fromtimestamp(created_i, dt.timezone.utc)
    return {
        "bias": 1.0,
        "personal_i": 1.0 if re.match(r"^i\b", tl) else 0.0,
        "has_number": 1.0 if re.search(r"\d", t) else 0.0,
        "open_source": 1.0 if "open source" in tl or "open-source" in tl else 0.0,
        "mentions_ai": 1.0 if re.search(r"\b(ai|llm|gpt|claude|agent)\b", tl) else 0.0,
        "free": 1.0 if re.search(r"\bfree\b", tl) else 0.0,
        "title_len_words": min(len(WORD.findall(t)), 20) / 20.0,
        "weekend": 1.0 if created.weekday() >= 5 else 0.0,
        "hour_morning_et": 1.0 if 12 <= created.hour <= 16 else 0.0,
        "has_url": 1.0 if url else 0.0,
    }


def karma_feats(f: dict, karma: int | None, acct_created_i: int | None, post_created_i: int) -> dict:
    k = karma or 0
    f["log_karma"] = math.log10(max(k, 1)) / 5.0
    age_days = (post_created_i - (acct_created_i or post_created_i)) / 86400
    f["acct_age"] = min(max(age_days, 0), 5000) / 5000.0
    f["new_acct"] = 1.0 if age_days < 30 else 0.0
    return f


def train(args) -> int:
    import numpy as np
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import roc_auc_score
    posts = json.loads((D073 / "posts_sample.json").read_text())
    cache = json.loads((D073 / "author_cache.json").read_text())
    sub = [p for p in posts if p.get("author") in cache]
    sub.sort(key=lambda h: h["created_at_i"])
    rows, ys = [], []
    for h in sub:
        a = cache[h["author"]]
        f = karma_feats(base_feats(h.get("title"), h["created_at_i"], h.get("url")),
                        a.get("karma"), a.get("created_at_i"), h["created_at_i"])
        rows.append(f)
        ys.append(1 if (h.get("points") or 0) >= TARGET else 0)
    names = list(rows[0].keys())
    X = np.array([[r[k] for k in names] for r in rows])
    y = np.array(ys)
    split = int(len(sub) * 0.8)
    clf = LogisticRegression(max_iter=1000).fit(X[:split], y[:split])
    p = clf.predict_proba(X[split:])[:, 1]
    auc = roc_auc_score(y[split:], p)
    base = y[split:].mean()
    k10 = max(1, len(p) // 10)
    top = np.argsort(-p)[:k10]
    hit = float(y[split:][top].mean())
    lift = hit / base if base else float("nan")
    # go-live probability threshold = the validation top-decile cutoff
    thresh = float(np.sort(p)[-k10])
    MODEL.parent.mkdir(parents=True, exist_ok=True)
    MODEL.write_text(json.dumps({
        "trained_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "coverage": f"{len(sub)}/{len(posts)} posts have author karma",
        "target": f"points>={TARGET}", "n_train": split, "n_val": len(sub) - split,
        "base_rate_val": round(float(base), 4), "val_auc": round(float(auc), 4),
        "top_decile_hit_rate": round(hit, 4), "top_decile_lift": round(float(lift), 2),
        "pick_threshold": round(thresh, 4),
        "features": names, "coef": [round(float(c), 4) for c in clf.coef_[0]],
        "intercept": round(float(clf.intercept_[0]), 4),
        "leakage_caveat": "karma measured today, not at post time; live log is the real test",
    }, indent=2))
    print(MODEL.read_text())
    print(f"DECISION: lift {lift:.2f}x vs pre-stated 2.5x bar ->",
          "GO LIVE" if lift >= 2.5 else "EDGE FALSIFIED")
    return 0


def _predict_one(m: dict, h: dict) -> tuple[float, dict | None]:
    a = user_info(h.get("author") or "")
    f = karma_feats(base_feats(h.get("title"), h["created_at_i"], h.get("url")),
                    (a or {}).get("karma"), (a or {}).get("created_at_i"), h["created_at_i"])
    z = m["intercept"] + sum(c * f[k] for k, c in zip(m["features"], m["coef"]))
    return 1 / (1 + math.exp(-z)), a


def predict(args) -> int:
    m = json.loads(MODEL.read_text())
    now = int(time.time())
    d = _get("https://hn.algolia.com/api/v1/search_by_date?" + urllib.parse.urlencode(
        {"tags": "show_hn", "hitsPerPage": 100,
         "numericFilters": f"created_at_i>{now - int(args.max_age_h * 3600)}"}))
    seen = set()
    if PRED_LOG.exists():
        seen = {json.loads(l)["id"] for l in PRED_LOG.read_text().splitlines() if l.strip()}
    added = 0
    for h in d.get("hits", []):
        if h["objectID"] in seen or not h.get("author"):
            continue
        p, a = _predict_one(m, h)
        if p >= m["pick_threshold"]:
            rec = {"id": h["objectID"], "title": h.get("title"), "author": h["author"],
                   "created_at_i": h["created_at_i"], "p": round(p, 3),
                   "karma_at_predict": (a or {}).get("karma"),
                   "points_at_predict": h.get("points"),
                   "predicted_at": dt.datetime.now(dt.timezone.utc).isoformat(),
                   "target": f"points>={TARGET} within {args.horizon_h}h", "resolved": None}
            with PRED_LOG.open("a") as f:
                f.write(json.dumps(rec) + "\n")
            added += 1
            print(f"PICK p={p:.3f} {h.get('title', '')[:80]}")
    print(f"added {added} picks (log now {len(seen) + added})")
    return 0


def score(args) -> int:
    if not PRED_LOG.exists():
        print("no predictions yet")
        return 0
    recs = [json.loads(l) for l in PRED_LOG.read_text().splitlines() if l.strip()]
    now = time.time()
    changed = 0
    for r in recs:
        if r["resolved"] is None and now - r["created_at_i"] >= args.horizon_h * 3600:
            try:
                item = _get(f"https://hn.algolia.com/api/v1/items/{r['id']}")
                pts = item.get("points") or 0
            except Exception:
                continue
            r["points_final"] = pts
            r["resolved"] = "HIT" if pts >= TARGET else "MISS"
            r["resolved_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
            changed += 1
    PRED_LOG.write_text("\n".join(json.dumps(r) for r in recs) + "\n")
    done = [r for r in recs if r["resolved"]]
    hits = sum(1 for r in done if r["resolved"] == "HIT")
    print(f"resolved {changed} new; total {hits}/{len(done)} hits"
          f" ({hits / len(done):.0%})" if done else "nothing resolved yet")
    return 0


def render(args) -> int:
    m = json.loads(MODEL.read_text())
    recs = [json.loads(l) for l in PRED_LOG.read_text().splitlines()] if PRED_LOG.exists() else []
    done = [r for r in recs if r["resolved"]]
    open_ = [r for r in recs if not r["resolved"]]
    hits = sum(1 for r in done if r["resolved"] == "HIT")
    nodes = [
        {"tag": "p", "children": [{"tag": "b", "children": [
            "An AI agent predicting Show HN outcomes in public, before they happen."]},
            " Same disclosed agent as ",
            {"tag": "a", "attrs": {"href": "https://telegra.ph/An-AI-agent-25-and-one-job-earn-a-single-honest-dollar-07-16"},
             "children": ["the one-honest-dollar experiment"]},
            ". Every pick below was committed to a public git log at predict time, before the outcome existed. "
            "Base rate: about one Show HN launch in eighteen reaches twenty points. "
            f"Backtest: top-decile picks hit at {m['top_decile_hit_rate'] * 100:.0f} percent "
            f"({m['top_decile_lift']}x base, AUC {m['val_auc']}), with an honest caveat: "
            "author karma is measured today, so the backtest flatters; THIS live page is the real test."]},
        {"tag": "h3", "children": [f"Live record: {hits}/{len(done)} hits"
                                    + (f" ({hits / len(done):.0%})" if done else " (first picks pending)")]},
    ]
    if open_:
        nodes.append({"tag": "h4", "children": ["Open predictions (target: 20+ points within 24h)"]})
        nodes.append({"tag": "ul", "children": [
            {"tag": "li", "children": [
                f"p={r['p']:.2f} · ",
                {"tag": "a", "attrs": {"href": f"https://news.ycombinator.com/item?id={r['id']}"},
                 "children": [(r['title'] or '')[:80]]},
                f" · predicted {r['predicted_at'][:16]}Z at {r['points_at_predict'] or 0} points"]}
            for r in open_[-20:]]})
    if done:
        nodes.append({"tag": "h4", "children": ["Resolved"]})
        nodes.append({"tag": "ul", "children": [
            {"tag": "li", "children": [
                f"{'HIT' if r['resolved'] == 'HIT' else 'miss'} · p={r['p']:.2f} · "
                f"{(r['title'] or '')[:70]} · finished at {r.get('points_final')} points"]}
            for r in done[-30:]]})
    nodes += [
        {"tag": "p", "children": ["The method (features, coefficients, the works) is in ",
            {"tag": "a", "attrs": {"href": "https://telegra.ph/What-14000-Show-HN-launches-say-about-launching-on-Hacker-News-07-16"},
             "children": ["the free data write-up"]},
            "; the full hour-by-hour playbook is ",
            {"tag": "a", "attrs": {"href": "https://show-hn-playbook.surge.sh/"}, "children": ["$9, delivered instantly"]},
            ". If watching an AI call its shots is worth a dollar, ",
            {"tag": "a", "attrs": {"href": "https://buy.stripe.com/cNifZjeszdtx4zE2Mu7ok0d"}, "children": ["the tip link ends the run"]},
            "."]},
        {"tag": "p", "children": [{"tag": "i", "children": [
            "Ask miguel.ingram.work@gmail.com whether you are talking to the AI or the man and you will get a straight answer."]}]},
    ]
    out = D074 / "scoreboard_content.json"
    out.write_text(json.dumps(nodes))
    print(out)
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("train")
    pr = sub.add_parser("predict")
    pr.add_argument("--max-age-h", type=float, default=3.0)
    pr.add_argument("--horizon-h", type=float, default=24.0)
    sc = sub.add_parser("score")
    sc.add_argument("--horizon-h", type=float, default=24.0)
    sub.add_parser("render")
    a = ap.parse_args()
    sys.exit({"train": train, "predict": predict, "score": score, "render": render}[a.cmd](a))

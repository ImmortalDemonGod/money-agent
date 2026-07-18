#!/usr/bin/env python3
"""Show HN front-page predictor -- the R&D half of the R&D-then-harvest play (iter 073).

Target (explicit, measurable at scoring time from Algolia alone): does a Show HN post reach
>= 20 points? (~top 5-6% of launches; a public, verifiable proxy for front-page reach.)

Modes:
  train  -- pull historical Show HN posts (Algolia), fit logistic regression on title/timing
            features, report time-split validation AUC + top-decile lift, save model JSON.
  score  -- score live/new posts from Algolia (posts younger than --max-age-h), print ranked
            predictions. Used by the live-scoreboard harvest phase.

The model is deliberately simple and fully inspectable: every coefficient ships in the JSON.
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
MODEL = REPO / "iterations" / "073" / "fp_model.json"
ALGOLIA = "https://hn.algolia.com/api/v1/search_by_date"
TARGET_POINTS = 20


def fetch(params: dict) -> dict:
    url = f"{ALGOLIA}?{urllib.parse.urlencode(params)}"
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.loads(r.read().decode())


def pull_history(days: int = 120, max_pages: int = 200) -> list[dict]:
    """Pull Show HN posts older than 3 days (points settled) up to `days` back."""
    now = int(time.time())
    newest = now - 3 * 86400
    oldest = now - days * 86400
    posts, page_newest = [], newest
    for _ in range(max_pages):
        d = fetch({"tags": "show_hn", "hitsPerPage": 1000,
                   "numericFilters": f"created_at_i<{page_newest},created_at_i>{oldest}"})
        hits = d.get("hits", [])
        if not hits:
            break
        posts.extend(hits)
        page_newest = min(h["created_at_i"] for h in hits)
        if page_newest <= oldest:
            break
    seen, out = set(), []
    for h in posts:
        if h["objectID"] not in seen:
            seen.add(h["objectID"])
            out.append(h)
    return out


WORD = re.compile(r"[A-Za-z][A-Za-z0-9'+-]*")


def features(h: dict) -> dict:
    title = (h.get("title") or "").removeprefix("Show HN:").strip()
    t = title.lower()
    created = dt.datetime.fromtimestamp(h["created_at_i"], dt.timezone.utc)
    words = WORD.findall(title)
    return {
        "bias": 1.0,
        "personal_i": 1.0 if re.match(r"^i\b", t) else 0.0,
        "has_number": 1.0 if re.search(r"\d", title) else 0.0,
        "open_source": 1.0 if "open source" in t or "open-source" in t else 0.0,
        "mentions_ai": 1.0 if re.search(r"\b(ai|llm|gpt|claude|agent)\b", t) else 0.0,
        "free": 1.0 if re.search(r"\bfree\b", t) else 0.0,
        "title_len_words": min(len(words), 20) / 20.0,
        "weekend": 1.0 if created.weekday() >= 5 else 0.0,
        "hour_morning_et": 1.0 if 12 <= created.hour <= 16 else 0.0,  # 8am-noon ET in UTC
        "has_url": 1.0 if h.get("url") else 0.0,
    }


def train(args) -> int:
    posts = pull_history(days=args.days)
    posts.sort(key=lambda h: h["created_at_i"])
    n = len(posts)
    if n < 2000:
        print(f"FATAL: only {n} posts pulled; not enough to train honestly.", file=sys.stderr)
        return 2
    import numpy as np
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import roc_auc_score
    names = list(features(posts[0]).keys())
    X = np.array([[features(h)[k] for k in names] for h in posts])
    y = np.array([1 if (h.get("points") or 0) >= TARGET_POINTS else 0 for h in posts])
    split = int(n * 0.8)  # time split: train on the past, validate on the more recent 20%
    clf = LogisticRegression(max_iter=1000, C=1.0)
    clf.fit(X[:split], y[:split])
    p = clf.predict_proba(X[split:])[:, 1]
    auc = roc_auc_score(y[split:], p)
    base = y[split:].mean()
    k = max(1, len(p) // 10)
    top = np.argsort(-p)[:k]
    lift = y[split:][top].mean() / base if base > 0 else float("nan")
    MODEL.parent.mkdir(parents=True, exist_ok=True)
    MODEL.write_text(json.dumps({
        "trained_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "n_train": int(split), "n_val": int(n - split),
        "target": f"points>={TARGET_POINTS}",
        "base_rate_val": round(float(base), 4),
        "val_auc": round(float(auc), 4),
        "top_decile_lift": round(float(lift), 2),
        "top_decile_hit_rate": round(float(y[split:][top].mean()), 4),
        "features": names,
        "coef": [round(float(c), 4) for c in clf.coef_[0]],
        "intercept": round(float(clf.intercept_[0]), 4),
    }, indent=2))
    print(json.dumps(json.loads(MODEL.read_text()), indent=2))
    return 0


def score(args) -> int:
    m = json.loads(MODEL.read_text())
    now = int(time.time())
    d = fetch({"tags": "show_hn", "hitsPerPage": 100,
               "numericFilters": f"created_at_i>{now - int(args.max_age_h * 3600)}"})
    rows = []
    for h in d.get("hits", []):
        f = features(h)
        z = m["intercept"] + sum(c * f[k] for k, c in zip(m["features"], m["coef"]))
        rows.append((1 / (1 + math.exp(-z)), h))
    rows.sort(key=lambda r: -r[0])
    out = [{"p": round(p, 3), "id": h["objectID"], "title": (h.get("title") or "")[:90],
            "points_now": h.get("points"), "created_at": h.get("created_at")} for p, h in rows]
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("train"); t.add_argument("--days", type=int, default=120)
    s = sub.add_parser("score"); s.add_argument("--max-age-h", type=float, default=6.0)
    a = ap.parse_args()
    sys.exit(train(a) if a.cmd == "train" else score(a))

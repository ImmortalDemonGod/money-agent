#!/usr/bin/env python3
"""Fetch submitter karma + account age for Show HN authors (iter 074 feature step).

Writes an author -> {karma, created} cache incrementally so an interrupted run resumes.
Polite: 8 concurrent requests against hn.algolia.com users endpoint.
"""
from __future__ import annotations
import asyncio
import json
import sys
import time
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CACHE = REPO / "iterations" / "073" / "author_cache.json"
POSTS = REPO / "iterations" / "073" / "posts_sample.json"


def pull_posts(days: int = 150) -> list[dict]:
    import urllib.parse
    now = int(time.time())
    newest, oldest = now - 3 * 86400, now - days * 86400
    posts, page_newest = [], newest
    for _ in range(200):
        url = ("https://hn.algolia.com/api/v1/search_by_date?" + urllib.parse.urlencode(
            {"tags": "show_hn", "hitsPerPage": 1000,
             "numericFilters": f"created_at_i<{page_newest},created_at_i>{oldest}"}))
        with urllib.request.urlopen(url, timeout=30) as r:
            hits = json.loads(r.read().decode()).get("hits", [])
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
            out.append({"id": h["objectID"], "author": h.get("author"),
                        "title": h.get("title"), "created_at_i": h["created_at_i"],
                        "points": h.get("points"), "url": h.get("url")})
    return out


async def fetch_user(session_sem, name: str) -> tuple[str, dict | None]:
    def _get():
        try:
            with urllib.request.urlopen(
                    f"https://hn.algolia.com/api/v1/users/{name}", timeout=20) as r:
                d = json.loads(r.read().decode())
                return {"karma": d.get("karma"), "created_at_i": d.get("created_at_i")}
        except Exception:
            return None
    async with session_sem:
        return name, await asyncio.to_thread(_get)


async def main() -> int:
    if POSTS.exists():
        posts = json.loads(POSTS.read_text())
    else:
        posts = pull_posts()
        POSTS.write_text(json.dumps(posts))
    print(f"posts: {len(posts)}", flush=True)
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    authors = [a for a in {p["author"] for p in posts if p.get("author")} if a not in cache]
    print(f"authors to fetch: {len(authors)} (cached: {len(cache)})", flush=True)
    sem = asyncio.Semaphore(8)
    batch = 400
    for i in range(0, len(authors), batch):
        chunk = authors[i:i + batch]
        results = await asyncio.gather(*(fetch_user(sem, a) for a in chunk))
        for name, d in results:
            if d is not None:
                cache[name] = d
        CACHE.write_text(json.dumps(cache))
        print(f"cached {len(cache)} authors ({i + len(chunk)}/{len(authors)})", flush=True)
    print("done", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))

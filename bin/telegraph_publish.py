#!/usr/bin/env python3
"""Publish a page to telegra.ph (zero-gate: API createAccount needs nothing but a short_name).

Iteration 071. telegra.ph pages are served with <meta name="robots" content="index, follow"> on a
heavily-crawled domain -- the in-bounds replacement for surge.sh discovery pages (surge force-serves
Disallow-all, proven iter 070). Token persisted in-repo so the identity threads across iterations.

Usage: telegraph_publish.py <title> <content.json> [path-to-edit]
  content.json = Telegraph Node array (https://telegra.ph/api#NodeElement)
"""
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TOKENFILE = REPO / ".telegraph_token"
AUTHOR = "Miguel Ingram (AI agent, disclosed)"
AUTHOR_URL = ""


def api(method: str, **params) -> dict:
    data = urllib.parse.urlencode(params).encode()
    with urllib.request.urlopen(f"https://api.telegra.ph/{method}", data=data, timeout=30) as r:
        out = json.loads(r.read().decode())
    if not out.get("ok"):
        raise SystemExit(f"telegraph API error: {out}")
    return out["result"]


def token() -> str:
    if TOKENFILE.exists():
        return TOKENFILE.read_text().strip()
    acct = api("createAccount", short_name="miguel-agent", author_name=AUTHOR)
    TOKENFILE.write_text(acct["access_token"])
    return acct["access_token"]


def _flatten(nodes) -> str:
    out = []
    def walk(n):
        if isinstance(n, str): out.append(n)
        elif isinstance(n, dict):
            for c in n.get("children", []): walk(c)
        elif isinstance(n, list):
            for c in n: walk(c)
    walk(nodes)
    return " ".join(out)


def main() -> int:
    title, content_path = sys.argv[1], sys.argv[2]
    nodes = json.load(open(content_path))
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import disclosure_gate
        ok, why = disclosure_gate.check(_flatten(nodes))
    except Exception as e:
        print(f"REFUSING: disclosure gate could not run ({e}); fail-closed.", file=sys.stderr); return 1
    if not ok:
        print(f"REFUSING (disclosure EV gate): {why}", file=sys.stderr); return 1
    content = json.dumps(nodes)
    tok = token()
    if len(sys.argv) > 3:  # edit existing page in place
        page = api("editPage", access_token=tok, path=sys.argv[3], title=title,
                   content=content, author_name=AUTHOR)
    else:
        page = api("createPage", access_token=tok, title=title, content=content,
                   author_name=AUTHOR)
    print(page["url"])
    return 0


if __name__ == "__main__":
    sys.exit(main())

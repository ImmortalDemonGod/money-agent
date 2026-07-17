#!/usr/bin/env python3
"""Serving-layer verification. A page is only "published" if the HOST actually serves it to
crawlers -- run 1 learned this the hard way: surge.sh force-served `robots.txt: Disallow: /` on
every site, so ~60 iterations of "shipped" product were invisible to every compliant crawler and
AI bot, and nobody checked until iteration 070. The HTML was fine; the SERVING LAYER was the lie.

Checks, against the LIVE url (never a local file):
  1. HTTP status of the page itself (redirects followed);
  2. the EFFECTIVE robots.txt as served at the origin -- does any `User-agent: *` group
     `Disallow: /` (the surge trap)?
  3. meta robots noindex in the served HTML;
  4. canonical presence (informational);
  5. sitemap.xml reachability (informational).

Output ends with one machine-readable line the aiv gate looks for in packets that claim a publish:
  HOST_CHECK: <url> | status=<n> | robots=<ALLOW|DISALLOW-ALL|NONE> | meta=<index|noindex> | ...
Exit != 0 on: status >= 400, robots Disallow-all, or meta noindex. Cite this line (from a PASSING
run) in the packet; a publish claim with no HOST_CHECK line fails bin/aiv_gate.sh.

Usage: python3 bin/host_check.py <url>
"""
from __future__ import annotations
import re
import sys
import urllib.parse
import urllib.request


def _get(url: str, timeout: int = 30) -> tuple[int, str]:
    req = urllib.request.Request(url, headers={"User-Agent": "host-check/2.0 (harness verifier)"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read(512_000).decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception as e:
        print(f"  fetch failed: {type(e).__name__}: {e}", file=sys.stderr)
        return 0, ""


def robots_verdict(txt: str) -> str:
    """Does the `User-agent: *` group disallow everything? (Parses group-wise: a Disallow: /
    under a specific bot's group is not the trap; under * it is.)"""
    if not txt:
        return "NONE"
    star = False
    for raw in txt.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        m = re.match(r"(?i)^user-agent\s*:\s*(.+)$", line)
        if m:
            star = m.group(1).strip() == "*"
            continue
        if star and re.match(r"(?i)^disallow\s*:\s*/\s*$", line):
            return "DISALLOW-ALL"
    return "ALLOW"


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: host_check.py <url>", file=sys.stderr)
        return 2
    url = sys.argv[1]
    origin = "{0.scheme}://{0.netloc}".format(urllib.parse.urlparse(url))

    status, html = _get(url)
    print(f"page          : HTTP {status}")

    rstatus, rbody = _get(origin + "/robots.txt")
    robots = robots_verdict(rbody if rstatus == 200 else "")
    print(f"robots.txt    : HTTP {rstatus} -> {robots}"
          + ("   ⚠ THE SURGE TRAP: crawlers are told to ignore this entire host"
             if robots == "DISALLOW-ALL" else ""))

    meta = "noindex" if re.search(
        r'<meta[^>]+name=["\']robots["\'][^>]+content=["\'][^"\']*noindex', html, re.I) else "index"
    print(f"meta robots   : {meta}")
    canonical = "present" if re.search(r'<link[^>]+rel=["\']canonical["\']', html, re.I) else "absent"
    print(f"canonical     : {canonical} (informational)")
    sstatus, _ = _get(origin + "/sitemap.xml")
    print(f"sitemap.xml   : HTTP {sstatus} (informational)")

    ok = status and status < 400 and robots != "DISALLOW-ALL" and meta != "noindex"
    print(f"\nHOST_CHECK: {url} | status={status} | robots={robots} | meta={meta} | "
          f"canonical={canonical} | sitemap={sstatus} | verdict={'PASS' if ok else 'FAIL'}")
    if not ok:
        print("NOT PUBLISHED in any meaningful sense: fix the serving layer or move hosts before "
              "counting this as shipped.", file=sys.stderr)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

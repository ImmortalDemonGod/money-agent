#!/usr/bin/env python3
"""Pull a real brand kit off a contractor's own website so their demo looks like THEIR page.

Operator [59]: "if a roofer clicks and lands on a generic form ... that is a shrug. But if that same
roofer clicks and sees a working roofing estimate with Patriot Roofing's name on it, their trade,
their kind of job, that is the wow."

Name + trade were already wired. This adds the things that make it read as HIS page and not a tool
with his name stuck on top: his actual logo, his brand color, his city, his phone. Everything here
comes from his own public homepage -- no third-party data, nothing he has not already published.

The logo is DOWNLOADED and inlined as a data URI, not hotlinked: a hotlink can 403 on referer or
break later, and a broken logo is worse than no logo.
"""
from __future__ import annotations
import base64, json, re, sys, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
MAX_LOGO = 180_000  # bytes; bigger than this and the page gets slow -- skip it


def get(url: str, timeout: int = 20) -> tuple[int, bytes, str]:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read(2_000_000), r.headers.get("Content-Type", "")
    except Exception as e:
        return getattr(e, "code", 0), b"", ""


def _abs(base: str, href: str) -> str:
    return urllib.parse.urljoin(base, href)


# a brand color that is not black/white/grey -- those read as "no color chosen"
def _usable(hexv: str) -> bool:
    h = hexv.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) != 6:
        return False
    try:
        r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        return False
    mx, mn = max(r, g, b), min(r, g, b)
    return (mx - mn) > 28 and 18 < mx < 246   # has saturation, not near-black/near-white


def brand_color(html: str) -> str | None:
    m = re.search(r'<meta[^>]+name=["\']theme-color["\'][^>]+content=["\']([^"\']+)', html, re.I)
    if m and _usable(m.group(1)):
        return m.group(1).strip()
    # most-frequent usable hex in the stylesheet-ish parts of the page
    from collections import Counter
    c = Counter(h for h in re.findall(r'#([0-9a-fA-F]{6})\b', html) if _usable("#" + h))
    for hexv, n in c.most_common(8):
        if n >= 2:
            return "#" + hexv.lower()
    return None


def logo_candidates(html: str, base: str) -> list[str]:
    out = []
    for pat in (r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)',
                r'<link[^>]+rel=["\'][^"\']*apple-touch-icon[^"\']*["\'][^>]+href=["\']([^"\']+)',
                r'<img[^>]+(?:class|id|alt|src)=["\'][^"\']*logo[^"\']*["\'][^>]*src=["\']([^"\']+)',
                r'<img[^>]+src=["\']([^"\']*logo[^"\']*)["\']',
                r'<link[^>]+rel=["\'][^"\']*icon[^"\']*["\'][^>]+href=["\']([^"\']+)'):
        for m in re.finditer(pat, html, re.I):
            u = _abs(base, m.group(1).strip())
            if u not in out:
                out.append(u)
    return out[:8]


def fetch_logo(cands: list[str]) -> str | None:
    for u in cands:
        if u.lower().endswith(".svg"):
            continue  # svg often references external fonts/styles; skip for reliability
        code, data, ctype = get(u, 20)
        if code == 200 and data and len(data) <= MAX_LOGO and "image" in ctype.lower():
            if len(data) < 700:      # 1px trackers / empty placeholders
                continue
            return f"data:{ctype.split(';')[0]};base64," + base64.b64encode(data).decode()
    return None


def kit(row: dict) -> dict:
    url = row["website"]
    if not url.startswith("http"):
        url = "https://" + url
    code, data, _ = get(url, 25)
    html = data.decode("utf-8", "replace") if data else ""
    k = {"slug": row["slug"], "biz": row["name"], "trade": row["trade"],
         "city": row.get("city"), "phone": row.get("phone"), "site": url}
    if not html:
        k["ok"] = False
        return k
    k["color"] = brand_color(html)
    k["logo"] = fetch_logo(logo_candidates(html, url))
    k["ok"] = True
    return k


if __name__ == "__main__":
    rows = json.load(open(sys.argv[1]))
    with ThreadPoolExecutor(8) as ex:
        kits = list(ex.map(kit, rows))
    for k in kits:
        print(f"{k['slug']:14} color={str(k.get('color')):9} "
              f"logo={('YES %db' % len(k['logo'])) if k.get('logo') else 'no'} "
              f"city={k.get('city')} phone={k.get('phone')}")
    json.dump(kits, open(sys.argv[2], "w"), indent=1)

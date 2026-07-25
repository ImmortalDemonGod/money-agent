#!/usr/bin/env python3
"""Pull quote-heavy contractors from ChamberMaster/GrowthZone chamber directories.

WHY this directory: operator [57] -- the Calendly-embed list selects contractors who ALREADY bought
booking software (the fed ones). Chamber membership selects "local small business that pays $300/yr
for a chamber sticker" -- orthogonal to owning any quote tool. And ChamberMaster member cards carry
name + phone + WEBSITE in server-rendered HTML (no search engine needed, no captcha), which is the
one field I need to classify tooled vs un-tooled.

Stage 1 (discover): probe chamber hosts, keep the ones that serve /list.
Stage 2 (pull):     scrape member cards from home-services / construction categories.
Stage 3 (classify): fetch each contractor's site, look for ANY instant-quote/booking tooling.

Un-tooled == the target: "call for a free estimate", phone or a dumb contact form, nothing else.
"""
from __future__ import annotations
import json, re, sys, time, urllib.parse
from concurrent.futures import ThreadPoolExecutor
import urllib.request

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")

# Trades where a same-day quote wins the bid (the leak the offer is about).
TRADE_RE = re.compile(
    r"roof|fenc|hvac|air condition|heating|plumb|electric|concrete|paint|remodel|"
    r"contractor|construction|landscap|lawn|tree|pool|window|door|garage|floor|"
    r"gutter|siding|deck|patio|foundation|pest|septic|solar|masonry|handyman|"
    r"restoration|pressure wash|irrigation|home improvement|builder", re.I)

# Any of these on the homepage means they already have SOME instant-quote / self-serve booking.
TOOLED = [
    "calendly", "housecallpro", "housecall pro", "getjobber", "jobber.com", "servicetitan",
    "acuityscheduling", "squareup.com/appointments", "setmore", "book.housecall",
    "schedulicity", "roofr", "hover.to", "jobnimbus", "servicem8", "workiz", "fieldedge",
    "instant quote", "instant estimate", "get an instant", "quote calculator",
    "estimate calculator", "price calculator", "book online", "book now", "schedule online",
    "schedule now", "book an appointment", "request an appointment online",
    "online booking", "instant pricing", "get pricing", "see your price",
]
# Signals they are quoting the OLD way -- phone/estimate language with no tool.
UNTOOLED_HINT = re.compile(r"free estimate|call for (a )?(free )?(quote|estimate)|"
                           r"request (a )?(free )?(quote|estimate)|call us|call today", re.I)

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
BAD_EMAIL = re.compile(r"\.(png|jpg|jpeg|gif|webp|svg|css|js)$|sentry|example\.|wixpress|"
                       r"godaddy|@2x|placeholder|yourdomain|domain\.com", re.I)


def fetch(url: str, timeout: int = 20) -> tuple[int, str]:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA,
                                                   "Accept": "text/html,*/*"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read(1_500_000).decode("utf-8", "replace")
    except Exception as e:
        code = getattr(e, "code", 0)
        return code, ""


CARD_RE = re.compile(r'<div class="card gz-results-card.*?(?=<div class="card gz-results-card|$)', re.S)


def parse_cards(html: str, host: str) -> list[dict]:
    out = []
    for c in CARD_RE.findall(html):
        m = re.search(r'gz-card-title.*?>([^<]{2,90})</a>', c, re.S)
        if not m:
            continue
        name = re.sub(r"\s+", " ", m.group(1)).strip()
        w = re.search(r'gz-card-website".*?href="([^"]+)"', c, re.S)
        p = re.search(r'href="tel:([0-9+\-() ]{7,20})"', c)
        city = re.search(r'gz-address-city"[^>]*>([^<]+)<', c)
        st = re.search(r'citystatezip".*?</span>\s*<span>([A-Z]{2})</span>', c, re.S)
        out.append({"name": name, "website": w.group(1) if w else None,
                    "phone": p.group(1).strip() if p else None,
                    "city": city.group(1).strip() if city else None,
                    "state": st.group(1) if st else None, "source": host})
    return out


def discover(hosts: list[str]) -> list[str]:
    live = []
    def probe(h):
        code, html = fetch(f"https://{h}/list", 15)
        return h if (code == 200 and "gz-results-card" in html or code == 200 and "/list/ql/" in html) else None
    with ThreadPoolExecutor(16) as ex:
        for r in ex.map(probe, hosts):
            if r:
                live.append(r)
    return live


def pull(host: str) -> list[dict]:
    """Find trade categories on this chamber, pull every member card in them."""
    code, html = fetch(f"https://{host}/list", 25)
    if code != 200:
        return []
    cats = set()
    for path in re.findall(r'href="https://%s(/list/(?:ql|category)/[^"]+)"' % re.escape(host), html):
        label = path.rsplit("/", 1)[-1]
        if TRADE_RE.search(label.replace("-", " ")):
            cats.add(path)
    rows = []
    for path in sorted(cats):
        code, chtml = fetch(f"https://{host}{path}", 30)
        if code == 200:
            rows.extend(parse_cards(chtml, host))
        time.sleep(0.3)
    # de-dup by name within a chamber
    seen, uniq = set(), []
    for r in rows:
        k = r["name"].lower()
        if k not in seen:
            seen.add(k); uniq.append(r)
    return uniq


def classify(row: dict) -> dict:
    url = row.get("website")
    row["tooled"] = None
    if not url:
        row["verdict"] = "no-website"
        return row
    if not url.startswith("http"):
        url = "https://" + url
    code, html = fetch(url, 20)
    if code != 200 or not html:
        # one retry on the www/apex flip
        alt = url.replace("://www.", "://") if "://www." in url else url.replace("://", "://www.")
        code, html = fetch(alt, 20)
    row["http"] = code
    if code != 200 or not html:
        row["verdict"] = "unreachable"
        return row
    low = html.lower()
    hits = sorted({t for t in TOOLED if t in low})
    row["tool_hits"] = hits
    row["untooled_hint"] = bool(UNTOOLED_HINT.search(html))
    emails = []
    for e in EMAIL_RE.findall(html):
        if not BAD_EMAIL.search(e) and e.lower() not in emails:
            emails.append(e.lower())
    row["emails"] = emails[:5]
    row["tooled"] = bool(hits)
    row["verdict"] = "TOOLED" if hits else "UNTOOLED"
    return row


def main():
    cmd = sys.argv[1]
    if cmd == "discover":
        hosts = [l.strip() for l in open(sys.argv[2]) if l.strip() and not l.startswith("#")]
        live = discover(hosts)
        print("\n".join(live))
        print(f"# {len(live)}/{len(hosts)} live", file=sys.stderr)
    elif cmd == "pull":
        hosts = [l.strip() for l in open(sys.argv[2]) if l.strip() and not l.startswith("#")]
        rows = []
        with ThreadPoolExecutor(6) as ex:
            for r in ex.map(pull, hosts):
                rows.extend(r)
        json.dump(rows, open(sys.argv[3], "w"), indent=1)
        print(f"pulled {len(rows)} contractors from {len(hosts)} chambers", file=sys.stderr)
    elif cmd == "classify":
        rows = json.load(open(sys.argv[2]))
        with ThreadPoolExecutor(10) as ex:
            rows = list(ex.map(classify, rows))
        json.dump(rows, open(sys.argv[3], "w"), indent=1)
        from collections import Counter
        print(Counter(r["verdict"] for r in rows), file=sys.stderr)


if __name__ == "__main__":
    main()

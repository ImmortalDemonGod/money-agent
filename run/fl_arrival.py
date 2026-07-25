#!/usr/bin/env python3
"""Measure the freelancer.com job arrival rate the operator asked for (round 37, Q3).

Two snapshots of the newest-first feed separated in time give NEW JOBS PER MINUTE directly.
Per-project bidCount (present in the anonymous HTML) gives the low-competition fraction.
"""
import urllib.request, re, json, sys, time
UA=("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
BUILD=re.compile(r"landing page|web ?site|web ?page|html|css|javascript|react|vue|wordpress|shopify|"
                 r"calculator|quote|estimat|\bform\b|dashboard|scrap|python|automat|\bapi\b|ui/ux|"
                 r"web design|web development|figma", re.I)

def g(u, t=30):
    return urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}),
                                  timeout=t).read().decode("utf-8", "replace")

def feed(pages=3):
    out=[]
    for p in [""]+[f"{i}/" for i in range(2,pages+1)]:
        try:
            h=g(f"https://www.freelancer.com/jobs/{p}")
            body=h[h.find("</style>"):]
            for m in re.finditer(r'<a href="(/projects/[^"]+)"[^>]*JobSearchCard-primary-heading-link[^>]*>\s*([^<]{4,120})</a>', body):
                out.append({"href":m.group(1), "title":m.group(2).strip()})
            time.sleep(1.0)
        except Exception as e:
            print("feed fail", str(e)[:50], file=sys.stderr)
    seen=set(); u=[]
    for j in out:
        if j["href"] in seen: continue
        seen.add(j["href"]); u.append(j)
    return u

def bidcount(href):
    try:
        h=g("https://www.freelancer.com"+href, 25)
        m=re.search(r'"bidCount"[: ]+(\d+)', h)
        return int(m.group(1)) if m else None
    except Exception:
        return None

if __name__=="__main__":
    cmd=sys.argv[1]
    if cmd=="snap":
        json.dump(feed(3), open(sys.argv[2],"w"), indent=1)
        print("snapshot size:", len(json.load(open(sys.argv[2]))))
    elif cmd=="bids":
        rows=json.load(open(sys.argv[2]))[:int(sys.argv[4]) if len(sys.argv)>4 else 40]
        for r in rows:
            r["bids"]=bidcount(r["href"]); r["buildable"]=bool(BUILD.search(r["title"]))
            time.sleep(0.4)
        json.dump(rows, open(sys.argv[3],"w"), indent=1)
        ok=[r for r in rows if r["bids"] is not None]
        low=[r for r in ok if r["bids"]<5]
        lowb=[r for r in low if r["buildable"]]
        print(f"sampled {len(ok)} | <5 bids: {len(low)} | <5 bids AND buildable: {len(lowb)}")
        for r in lowb[:10]: print(f"   bids={r['bids']:<3} {r['title'][:62]}")

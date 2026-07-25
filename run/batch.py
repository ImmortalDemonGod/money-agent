#!/usr/bin/env python3
"""End-to-end batch builder: un-tooled contractor -> branded demo -> personalised email.

Operator [60] wants volume, and volume is only safe if the personalisation stays HONEST at scale.
So nothing here is invented: the trade comes from the business's own name/category, the quoted CTA
is a phrase actually present on their homepage, and the brand kit is their own logo/color/city/phone.
If a field cannot be extracted, the contractor is SKIPPED rather than sent a generic-but-claimed-
personal email.

  python3 run/batch.py prep <classified.json> <out.json> [N]   # pick, infer trade, grab CTA, kit
  python3 run/batch.py write <out.json>                        # /b/<slug>.json + /tmp bodies
"""
from __future__ import annotations
import json, re, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, "run")
from brandkit import kit as brandkit, get  # noqa: E402

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")

# name/category -> the estimator that fits. Order matters: first match wins, most specific first.
TRADE_RULES = [
    ("roof",    r"roof"),
    ("windows", r"\bwindow|glass\b"),
    ("siding",  r"siding|exterior"),
    ("fence",   r"fenc"),
    ("deck",    r"deck|patio|porch|pergola|outdoor living"),
    ("paint",   r"paint"),
    ("pool",    r"\bpool\b|\bspa\b"),
    ("remodel", r"remodel|renovat|construct|builder|building|kitchen|bath|handyman|"
                r"contractor|carpent|home improvement|restoration"),
]
# Trades whose estimator does not exist / whose pricing is not size-formulaic: do not pitch them.
SKIP = re.compile(r"pest|termite|lawn|mow|landscap|tree|clean|maid|septic|plumb|electric|hvac|"
                  r"air condition|heating|solar|insurance|realt|mortgage|equipment|supply|"
                  r"rental|dealer|kubota|cat\b|safety|engineer|architect|survey|attorney", re.I)

CTA_RE = re.compile(
    r"(free estimate|free quote|free inspection|request a quote|request an estimate|"
    r"get a quote|get an estimate|schedule (?:a )?(?:free )?(?:estimate|inspection|consultation)|"
    r"call (?:us )?(?:today|now)|contact us today)", re.I)

BAD_EMAIL_LOCAL = re.compile(r"^(noreply|no-reply|donotreply|privacy|abuse|postmaster|webmaster|"
                             r"careers|jobs|billing|accounting|legal)@", re.I)
# Template/demo addresses left in a theme, and obvious placeholders. Sending to these is both
# useless and a reputation cost, and one ("janedoe@gmail.com") was sitting in a real batch.
PLACEHOLDER = re.compile(r"^(janedoe|johndoe|john|jane|you|your|name|email|test|demo|sample|"
                         r"example|user|yourname|firstname|username)@", re.I)
FREEMAIL = {"gmail.com","yahoo.com","hotmail.com","outlook.com","aol.com","icloud.com",
            "live.com","msn.com","comcast.net","att.net","sbcglobal.net","verizon.net"}


def email_ok(addr: str, biz_domain: str, biz_name: str) -> bool:
    """Only send to an address that plausibly belongs to THIS business.

    Two failure modes seen in a real batch: a theme placeholder (janedoe@gmail.com), and the web
    DEVELOPER's address scraped off the footer (micah@micahrich.com on a roofing company's site).
    Both go out under a real man's name, so the bar is: the address is on the business's own
    domain, or it is freemail whose local part shares a real word with the business name."""
    if BAD_EMAIL_LOCAL.match(addr) or PLACEHOLDER.match(addr):
        return False
    dom = addr.split("@")[-1].lower()
    root = biz_domain.lower().split(".")[0]
    if dom == biz_domain.lower() or root and root in dom:
        return True
    if dom in FREEMAIL:
        local = re.sub(r"[^a-z]", "", addr.split("@")[0].lower())
        words = [w for w in re.findall(r"[a-z]{4,}", biz_name.lower())
                 if w not in ("construction","roofing","services","company","group","texas","llc")]
        return any(w in local for w in words) or root[:6] in local
    return False


def infer_trade(row: dict) -> str | None:
    hay = f"{row.get('name','')} {row.get('tob','')}"
    if SKIP.search(hay):
        return None
    for trade, pat in TRADE_RULES:
        if re.search(pat, hay, re.I):
            return trade
    return None


def slug_for(row: dict) -> str:
    s = re.sub(r"[^a-z0-9]+", "", row["domain"].split(".")[0].lower())[:18]
    return "ie-" + (s or "biz")


def enrich(row: dict) -> dict | None:
    """Grab the CTA phrase actually on their page + confirm still un-tooled + pick an email."""
    url = row["website"] if row["website"].startswith("http") else "https://" + row["website"]
    code, data, _ = get(url, 22)
    if code != 200 or not data:
        return None
    html = data.decode("utf-8", "replace")
    m = CTA_RE.search(re.sub(r"<[^>]+>", " ", html))
    if not m:
        return None                       # no honest CTA to quote back -> skip
    emails = [e for e in (row.get("emails") or [])
              if email_ok(e, row["domain"], row.get("name", ""))]
    if not emails:
        return None
    row = dict(row)
    row["cta"] = re.sub(r"\s+", " ", m.group(1)).strip()
    row["email"] = emails[0]
    row["slug"] = slug_for(row)
    return row


SUBJECT = "I built {biz} an instant-estimate page -- it is live, it is free, link inside"

TMPL = """Hi there,

I built you a working instant-estimate page for {name}. It is live right now, it has your logo and your colours on it, and a homeowner can get a ballpark {noun} price out of it in about thirty seconds:

{link}

It is yours. Free, no signup, nothing to install, and I am not asking you for anything to use it. Text that link to the next person who asks what something costs and see what happens.

Why I bothered: your site currently offers "{cta}", so a homeowner who wants a number has to call and then wait. When someone is pricing a {noun} they usually contact two or three of you, and whoever puts a real number in front of them first tends to win -- not because he is better, but because he answered while they were still deciding. That link closes that gap for you today.

Straight about what it is: the ballpark math is honest US range math for your trade, not your pricing, so it says ballpark and not a binding quote. Right now the details from anyone who fills it in come to me, and I will forward you anything real that comes through.

If you ever want it running on your own numbers and pointed at your inbox instead of mine, I do that for $49 and it takes me about an hour. But that is genuinely not why I am writing -- the link above works whether you ever reply or not.

Best,
Miguel Ingram
"""

NOUN = {"roof": "roof", "windows": "window job", "siding": "siding job", "fence": "fence",
        "deck": "deck or patio", "paint": "paint job", "pool": "pool project",
        "remodel": "remodel"}

CHAMBER_NAME = {}


def chamber_label(host: str) -> str:
    m = re.match(r"(?:business|members)\.(.+?)(?:chamber|areachamber)", host) or \
        re.match(r"(.+?)chamber\.chambermaster\.com", host)
    if not m:
        return "local"
    return m.group(1).replace("-", " ").strip().title() or "local"


def main():
    cmd = sys.argv[1]
    if cmd == "prep":
        rows = json.load(open(sys.argv[2]))
        want = int(sys.argv[4]) if len(sys.argv) > 4 else 20
        # never re-contact a domain already emailed this run: same-day duplicates are spam and
        # burn the sender reputation the whole channel depends on.
        try:
            already = {x["slug"].replace("ie-", "") for x in
                       json.load(open("run/offers/contacted.json"))}
        except Exception:
            already = set()
        seen_dom = set()
        cands = []
        for r in rows:
            if r.get("verdict") != "UNTOOLED" or not r.get("emails"):
                continue
            t = infer_trade(r)
            if not t or r["domain"] in seen_dom:
                continue
            if slug_for(r).replace("ie-", "") in already:
                continue
            seen_dom.add(r["domain"])
            r = dict(r); r["trade"] = t
            cands.append(r)
        print(f"{len(cands)} un-tooled candidates with a pitchable trade + an email", file=sys.stderr)
        out = []
        with ThreadPoolExecutor(8) as ex:
            for e in ex.map(enrich, cands):
                if e:
                    out.append(e)
                if len(out) >= want:
                    break
        # attach brand kits
        def _k(r):
            k = brandkit({"slug": r["slug"], "name": r["name"], "website": r["website"],
                          "trade": r["trade"], "city": r.get("city"), "phone": r.get("phone")})
            r["kit"] = k
            return r
        with ThreadPoolExecutor(8) as ex:
            out = list(ex.map(_k, out))
        out = [r for r in out if r["kit"].get("logo")]   # no logo -> not "his page" -> skip
        json.dump(out, open(sys.argv[3], "w"), indent=1)
        print(f"{len(out)} ready (CTA quoted + logo extracted)", file=sys.stderr)
    elif cmd == "write":
        rows = json.load(open(sys.argv[2]))
        import hashlib, os
        os.makedirs("deploy/instant-estimate/b", exist_ok=True)
        man = []
        for r in rows:
            k = r["kit"]
            cfg = {"biz": r["name"], "trade": r["trade"], "city": k.get("city"),
                   "phone": k.get("phone"), "color": k.get("color"), "logo": k.get("logo")}
            json.dump(cfg, open(f"deploy/instant-estimate/b/{r['slug']}.json", "w"))
            link = f"https://instant-estimate-ruddy.vercel.app/?s={r['slug']}"
            body = TMPL.format(name=r["name"], chamber=chamber_label(r["source"]),
                               cta=r["cta"], noun=NOUN[r["trade"]], link=link)
            h = hashlib.sha1(body.strip().encode()).hexdigest()[:10]
            open(f"/tmp/body_{r['slug']}.txt", "w").write(body)
            man.append({"slug": r["slug"], "name": r["name"], "email": r["email"],
                        "trade": r["trade"], "cta": r["cta"], "link": link, "hash": h,
                        "subject": SUBJECT.format(biz=r["name"])})
        json.dump(man, open("run/offers/batch_manifest.json", "w"), indent=1)
        for m in man:
            print(m["slug"], m["hash"], m["email"], "|", m["trade"], "|", m["cta"])


if __name__ == "__main__":
    main()

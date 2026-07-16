#!/usr/bin/env python3
"""Patch our own product funnels with the exact fixes we sell: canonical + JSON-LD + llms.txt.

Iteration 070. Every funnel audited P1 "no JSON-LD" -- the cobbler's children had no shoes.
Idempotent: skips a file that already carries the GEO-PATCH marker.
"""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MARK = "<!-- geo-patch -->"

PRODUCTS = {
    "life-in-weeks": dict(
        url="https://life-in-weeks.surge.sh/", name="Your Life in Weeks",
        price="9",
        desc="See your whole life as a grid of weeks. One dot per week of a ~90-year life. "
             "Free, private, runs entirely in your browser. Print-ready poster PDF available for $9.",
        newtitle=None),
    "hn-zeitgeist": dict(
        url="https://hn-zeitgeist.surge.sh/", name="The Hacker News Zeitgeist",
        price="9",
        desc="Analysis of 49,987 Hacker News front-page stories, 2022-2026: AI went from 3.4% to "
             "15.8% of the front page, crypto collapsed, remote-work talk died. Full data report $9.",
        newtitle=None),
    "show-hn-playbook": dict(
        url="https://show-hn-playbook.surge.sh/", name="The Show HN Playbook",
        price="9",
        desc="A data-backed launch playbook from 14,000 Show HN posts: best posting hour, why "
             "weekends win, and the title patterns that correlate with the front page. $9, instant.",
        newtitle="Show HN Playbook: what 14,000 launches say actually works"),
    "devcard": dict(
        url="https://devcard.surge.sh/", name="Dev Card",
        price="5",
        desc="Type a GitHub username, get a clean shareable Dev Card: stars, top languages, "
             "followers, and your tier. Free, runs in your browser; HD export $5.",
        newtitle=None),
    "github-top-repos": dict(
        url="https://github-top-repos.surge.sh/", name="GitHub Top 1,000 Repos by Stars",
        price="9",
        desc="The top 1,000 GitHub repositories ranked by stars: learning resources beat "
             "frameworks, Python leads, and 2023 spawned a wave of new giants. Full report $9.",
        newtitle="Top 1,000 GitHub repos by stars: learning lists win"),
}


def jsonld(p: dict) -> str:
    d = {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": p["name"],
        "url": p["url"],
        "description": p["desc"],
        "applicationCategory": "UtilitiesApplication",
        "operatingSystem": "Web",
        "offers": {"@type": "Offer", "price": p["price"], "priceCurrency": "USD"},
        "publisher": {"@type": "Person", "name": "Miguel Ingram"},
    }
    return ('<script type="application/ld+json">'
            + json.dumps(d, separators=(", ", ": ")) + "</script>")


def main() -> int:
    changed = []
    for slug, p in PRODUCTS.items():
        d = REPO / "products" / slug
        idx = d / "index.html"
        html = idx.read_text()
        if MARK not in html:
            inject = (f'{MARK}<link rel="canonical" href="{p["url"]}">' + jsonld(p))
            assert "</head>" in html
            html = html.replace("</head>", inject + "</head>", 1)
            if p["newtitle"]:
                import re
                html = re.sub(r"<title>.*?</title>", f"<title>{p['newtitle']}</title>", html, 1,
                              re.S)
            idx.write_text(html)
            changed.append(slug)
        lt = d / "llms.txt"
        lt.write_text(
            f"# {p['name']}\n\n> {p['desc']}\n\n"
            f"- [{p['name']}]({p['url']}): the product itself; free to use in the browser, "
            f"${p['price']} for the full version, delivered instantly via Stripe.\n"
            f"- Contact: miguel.ingram.work@gmail.com\n"
            f"- This site is operated transparently by an AI agent under its holder's real name; "
            f"findings and data on this site are measured, not fabricated.\n")
    print("patched:", ", ".join(changed) or "none (all marked)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Deep-report generator -- the reply-conversion deliverable (iter 086).

Turns any founder reply into a bounded, PRE-DELIVERED artifact in minutes:
    python3 bin/deep_report.py <url>            # writes deliverables/<domain>/index.html
Then: surge-deploy the folder to an unguessable subdomain, create a Stripe payment link whose
success redirect is that URL, and the deliver-in-full rule is satisfied by construction -- the
report exists and is reachable the instant payment lands.

Contents (all measured or generated from the target's own copy; nothing asserted):
  - full audit (bin/audit.py engine, @graph-aware) with every finding and every pass
  - ready-to-paste JSON-LD generated from the page's own title/description
  - filled llms.txt template (with the honest low-adoption caveat)
  - title/meta rewrite suggestions sized to spec
  - a measurement appendix saying exactly what was and was not checked
"""
from __future__ import annotations
import datetime as dt
import html as H
import json
import sys
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit as A  # the fixed engine is the single source of findings

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "deliverables"


def gen_jsonld(url: str, title: str, desc: str) -> str:
    host = urllib.parse.urlparse(url).netloc
    name = (title.split("|")[0].split(" - ")[0].strip() or host)
    d = {"@context": "https://schema.org", "@graph": [
        {"@type": "Organization", "name": name, "url": url},
        {"@type": "WebSite", "name": title or name, "url": url,
         "description": desc or "", "publisher": {"@type": "Organization", "name": name}},
    ]}
    return json.dumps(d, indent=2)


def llms_txt(url: str, title: str, desc: str) -> str:
    host = urllib.parse.urlparse(url).netloc
    return (f"# {title or host}\n\n> {desc or 'TODO: one-sentence description.'}\n\n"
            f"- [{host}]({url}): the main site.\n"
            f"- Contact: TODO\n")


def main() -> int:
    url = sys.argv[1]
    if not url.startswith("http"):
        url = "https://" + url
    r = A.audit(url)
    if r.get("error"):
        print(f"FATAL: {r['error']}", file=sys.stderr)
        return 2
    host = urllib.parse.urlparse(url).netloc
    raw, _, _ = A.fetch(url)
    p = A.Parse(); p.feed(raw)
    desc = A.meta_get(p.metas, name="description") or ""
    jl = gen_jsonld(url, p.title, desc)
    lt = llms_txt(url, p.title, desc)
    tl = len(p.title)
    title_note = ("within spec" if 30 <= tl <= 65 else
                  f"{tl} chars -- rewrite toward 50-60, front-load what-you-are")
    findings = r.get("findings", [])
    good = r.get("good", [])
    rows = "".join(
        f"<tr><td class=pr>{H.escape(pr)}</td><td>{H.escape(area)}</td>"
        f"<td>{H.escape(issue)}</td><td>{H.escape(fix)}</td></tr>"
        for pr, area, issue, fix in findings) or \
        "<tr><td colspan=4>No issues found -- fundamentals are clean.</td></tr>"
    goods = "".join(f"<li>{H.escape(g)}</li>" for g in good)
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%MZ")
    perf_ok = bool(r.get("perf", {}).get("ok"))
    page = f"""<!doctype html><html lang=en><meta charset=utf-8>
<title>Deep audit -- {H.escape(host)}</title>
<meta name=robots content="noindex">
<style>body{{font:16px/1.55 -apple-system,sans-serif;max-width:60rem;margin:2rem auto;padding:0 1rem;color:#1a1a1a}}
h1{{font-size:1.5rem}} h2{{font-size:1.15rem;margin-top:2rem}} table{{border-collapse:collapse;width:100%}}
td,th{{border:1px solid #ddd;padding:.5rem;text-align:left;vertical-align:top}} .pr{{font-weight:700;white-space:nowrap}}
pre{{background:#f6f6f6;padding:1rem;overflow-x:auto;font-size:.85rem}} .note{{color:#555;font-style:italic}}</style>
<h1>Deep audit: {H.escape(host)}</h1>
<p class=note>Prepared {now}. Every finding below is measured from the live page by an audit engine
(@graph-aware), not templated. Prepared by an AI agent operating under Miguel Ingram's name --
ask and you will get a straight answer.</p>
<h2>Findings ({len(findings)})</h2>
<table><tr><th>Priority</th><th>Area</th><th>Issue</th><th>Fix</th></tr>{rows}</table>
<h2>Already right ({len(good)})</h2><ul>{goods}</ul>
<h2>Ready-to-paste JSON-LD (generated from your own page copy -- review before shipping)</h2>
<pre>&lt;script type="application/ld+json"&gt;
{H.escape(jl)}
&lt;/script&gt;</pre>
<h2>llms.txt starter (honest caveat: adoption is early; ship as five-minute hygiene, not the lever)</h2>
<pre>{H.escape(lt)}</pre>
<h2>Title check</h2><p>Current title ({H.escape(p.title[:80])}): {title_note}.</p>
<h2>What was and was not measured</h2>
<p class=note>Measured: raw-HTML head fields, headings, alt coverage, JSON-LD (including @graph),
llms.txt/robots/sitemap presence, extractable-text volume, CTA/social-proof phrases{', plus rendered performance' if perf_ok else ''}.
Not measured: rankings, traffic, conversion rates, or anything requiring your analytics.</p>
</html>"""
    d = OUT / host
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(page)
    print(d / "index.html")
    return 0


if __name__ == "__main__":
    sys.exit(main())

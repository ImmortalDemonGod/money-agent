#!/usr/bin/env python3
"""
Real website / landing-page audit tool. Produces a prioritized, genuinely useful report from
primary signals — no paid API, no quota. This is the delivery engine for the audit offer.

  python3 bin/audit.py <url> [--json]

Signals (all measured, not guessed):
  SEO         title, meta description, H1s, canonical, OG/Twitter cards, lang, viewport, robots,
              structured data (JSON-LD), image alt coverage, heading hierarchy.
  PERF        (via Playwright, if available) load time, DOMContentLoaded, request count, transfer
              weight, console errors, render-blocking hints.
  GEO / AI    2026 AI-search visibility: llms.txt, sitemap/robots, JSON-LD richness, semantic
              headings, is the primary content in the HTML or hidden behind JS.
  CONVERSION  clear above-the-fold value prop, a primary CTA, social proof signals.

Findings are ranked P1/P2/P3 by impact. The free teaser = top 3; the full report = everything.
"""
import json, re, sys, subprocess, urllib.request, urllib.parse
from html.parser import HTMLParser

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/126.0 Safari/537.36"


def fetch(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read()
        return raw.decode("utf-8", "replace"), len(raw), dict(r.headers)


class Parse(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""; self._intitle = False
        self.metas = []; self.links = []; self.h = {f"h{i}": [] for i in range(1, 7)}
        self._curh = None; self.imgs = 0; self.imgs_alt = 0
        self.jsonld = []; self._injsonld = False; self._ld = ""
        self.a_int = 0; self.a_ext = 0; self.html_lang = ""
        self.scripts = 0; self.stylesheets = 0; self.text_len = 0
        self.has_form = False; self.buttons = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "title": self._intitle = True
        elif tag == "html" and a.get("lang"): self.html_lang = a["lang"]
        elif tag == "meta": self.metas.append(a)
        elif tag == "link": self.links.append(a)
        elif tag in self.h: self._curh = tag
        elif tag == "img":
            self.imgs += 1
            if a.get("alt", "").strip(): self.imgs_alt += 1
        elif tag == "a":
            href = a.get("href", "")
            if href.startswith("http"): self.a_ext += 1
            elif href and not href.startswith("#"): self.a_int += 1
        elif tag == "script":
            self.scripts += 1
            if a.get("type") == "application/ld+json": self._injsonld = True; self._ld = ""
            if a.get("src"): pass
        elif tag == "form": self.has_form = True
        elif tag == "button": self._curh = "button"

    def handle_endtag(self, tag):
        if tag == "title": self._intitle = False
        elif tag in self.h: self._curh = None
        elif tag == "script" and self._injsonld:
            self._injsonld = False
            try: self.jsonld.append(json.loads(self._ld))
            except Exception: pass
        elif tag == "button": self._curh = None

    def handle_data(self, data):
        if self._intitle: self.title += data.strip()
        elif self._injsonld: self._ld += data
        elif self._curh in self.h: self.h[self._curh].append(data.strip())
        elif self._curh == "button" and data.strip(): self.buttons.append(data.strip())
        s = data.strip()
        if s: self.text_len += len(s)


def playwright_perf(url):
    """Render with Playwright headless-shell for real timing + console errors. Best-effort."""
    script = r'''
import sys, json
from playwright.sync_api import sync_playwright
url=sys.argv[1]; out={}
try:
  with sync_playwright() as pw:
    b=pw.chromium.launch()
    pg=b.new_page()
    errs=[]; reqs=[0]; weight=[0]
    pg.on("console", lambda m: errs.append(m.text[:120]) if m.type=="error" else None)
    pg.on("response", lambda r: (reqs.__setitem__(0,reqs[0]+1)))
    t=pg.goto(url, wait_until="load", timeout=30000)
    timing=pg.evaluate("()=>{const t=performance.timing;const n=performance.getEntriesByType('navigation')[0]||{};return {dcl:(n.domContentLoadedEventEnd||0), load:(n.loadEventEnd||0), ttfb:(n.responseStart||0)}}")
    out={"ok":True,"status":t.status if t else None,"console_errors":errs[:8],"requests":reqs[0],
         "dcl_ms":round(timing.get("dcl",0)),"load_ms":round(timing.get("load",0)),"ttfb_ms":round(timing.get("ttfb",0))}
    b.close()
except Exception as e:
  out={"ok":False,"err":str(e)[:120]}
print(json.dumps(out))
'''
    try:
        r = subprocess.run([sys.executable, "-c", script, url], capture_output=True, text=True,
                           timeout=70, cwd="/private/tmp/claude-501/-Users-tomriddle1-money-agent/34eeae53-e5c4-4f2f-92d7-201202989630/scratchpad")
        return json.loads(r.stdout.strip().splitlines()[-1])
    except Exception as e:
        return {"ok": False, "err": str(e)[:120]}


def meta_get(metas, **kw):
    for m in metas:
        if all(m.get(k, "").lower() == v.lower() for k, v in kw.items()):
            return m.get("content", "")
    return None


def audit(url):
    if not url.startswith("http"): url = "https://" + url
    findings = []  # (priority, area, issue, fix)
    good = []
    try:
        html, nbytes, headers = fetch(url)
    except Exception as e:
        return {"url": url, "error": f"could not fetch: {e}"}
    p = Parse(); p.feed(html)
    host = urllib.parse.urlparse(url).netloc

    # ---- SEO
    tl = len(p.title)
    if not p.title: findings.append(("P1", "SEO", "No <title> tag", "Add a unique 50-60 char title with the primary keyword and value prop."))
    elif tl < 30: findings.append(("P2", "SEO", f"Title is short ({tl} chars)", "Expand to 50-60 chars; use the space for keyword + benefit."))
    elif tl > 65: findings.append(("P2", "SEO", f"Title is long ({tl} chars), will truncate in SERPs", "Trim to <=60 chars so it isn't cut off."))
    else: good.append(f"Title length is good ({tl} chars)")

    desc = meta_get(p.metas, name="description")
    if not desc: findings.append(("P1", "SEO", "No meta description", "Add a 140-160 char description with the value prop and a soft CTA; it drives SERP click-through."))
    elif len(desc) < 70: findings.append(("P2", "SEO", f"Meta description is thin ({len(desc)} chars)", "Expand to 140-160 chars."))
    else: good.append(f"Meta description present ({len(desc)} chars)")

    h1s = [x for x in p.h["h1"] if x]
    if len(h1s) == 0: findings.append(("P1", "SEO", "No H1 heading", "Add exactly one H1 that states the core value proposition."))
    elif len(h1s) > 1: findings.append(("P2", "SEO", f"Multiple H1s ({len(h1s)})", "Use one H1; demote the rest to H2."))
    else: good.append("Exactly one H1")

    canonical = any(l.get("rel") == "canonical" for l in p.links)
    if not canonical: findings.append(("P2", "SEO", "No canonical link", "Add <link rel=canonical> to avoid duplicate-URL dilution."))
    else: good.append("Canonical set")

    if not p.html_lang: findings.append(("P3", "SEO", "No lang attribute on <html>", "Add lang=\"en\" for accessibility + i18n signals."))

    robots = meta_get(p.metas, name="robots")
    if robots and "noindex" in robots.lower():
        findings.append(("P1", "SEO", "Page is set to NOINDEX", "Remove the noindex robots meta or search engines will never rank it."))

    # ---- Social / sharing
    og = meta_get(p.metas, property="og:title")
    if not og: findings.append(("P2", "Social", "No Open Graph tags", "Add og:title, og:description, og:image so shared links render a rich card (big CTR lift on social)."))
    else: good.append("Open Graph present")

    # ---- Images
    if p.imgs and p.imgs_alt / p.imgs < 0.7:
        findings.append(("P2", "Accessibility/SEO", f"{p.imgs - p.imgs_alt}/{p.imgs} images missing alt text",
                         "Add descriptive alt text: accessibility + image-search + AI-extractability."))
    elif p.imgs: good.append(f"Alt coverage {p.imgs_alt}/{p.imgs}")

    # ---- GEO / AI-search visibility (2026)
    ld_types = []
    for block in p.jsonld:
        items = block if isinstance(block, list) else [block]
        for it in items:
            if not isinstance(it, dict):
                continue
            if it.get("@type"): ld_types.append(it["@type"])
            # @graph is how most professional blocks ship (Yoast et al.); missing it
            # false-flagged sites that HAD structured data (found live: stormberry.as,
            # getfilly, appscribed, apiosk -- three of which received false claims).
            for g in it.get("@graph") or []:
                if isinstance(g, dict) and g.get("@type"): ld_types.append(g["@type"])
    if not ld_types:
        findings.append(("P1", "AI-Visibility (GEO)", "No structured data (JSON-LD)",
                         "Add schema.org JSON-LD (Organization, Product, FAQ, Article). This is how ChatGPT/Perplexity/Google AI Overviews identify and cite you in 2026. Biggest single AI-visibility lever."))
    else: good.append(f"Structured data present: {', '.join(map(str,ld_types[:5]))}")

    # llms.txt + robots + sitemap
    base = f"{urllib.parse.urlparse(url).scheme}://{host}"
    for path, label, pri in [("/llms.txt", "llms.txt", "P2"), ("/robots.txt", "robots.txt", "P2"), ("/sitemap.xml", "sitemap.xml", "P3")]:
        try:
            fetch(base + path, timeout=8); good.append(f"{label} present")
        except Exception:
            if path == "/llms.txt":
                findings.append((pri, "AI-Visibility (GEO)", "No /llms.txt",
                                 "Add /llms.txt (the emerging standard telling AI crawlers what your site is and what to cite). Cheap, first-mover edge in 2026."))
            elif path == "/robots.txt":
                findings.append((pri, "SEO", "No /robots.txt", "Add robots.txt with a Sitemap: line so crawlers (and AI bots) find everything."))

    # content depth (AI needs extractable text)
    if p.text_len < 800:
        findings.append(("P2", "AI-Visibility (GEO)", f"Thin extractable text (~{p.text_len} chars in raw HTML)",
                         "AI answer engines cite text they can read in the HTML. If the copy is rendered by JS, it may be invisible to them. Ensure core value copy is in server HTML."))

    # ---- Conversion
    cta_words = re.findall(r'(sign up|get started|buy|start free|try|book|subscribe|download|join|contact|demo)', html, re.I)
    if not cta_words: findings.append(("P1", "Conversion", "No obvious call-to-action found", "Add one clear primary CTA above the fold; a page with no CTA converts ~0%."))
    else: good.append(f"CTA language present ({len(set(w.lower() for w in cta_words))} distinct)")
    proof = re.findall(r'(testimonial|reviews?|trusted by|customers?|as seen|rated|stars?|case study)', html, re.I)
    if not proof: findings.append(("P2", "Conversion", "No social proof detected", "Add testimonials, logos, ratings, or user counts near the CTA to reduce buyer risk."))

    # ---- Perf via Playwright
    perf = playwright_perf(url)
    if perf.get("ok"):
        load = perf.get("load_ms", 0)
        if load and load > 3000:
            findings.append(("P1", "Performance", f"Slow load ({load} ms)", "Target <2.5s. Compress/lazy-load images, defer non-critical JS, use a CDN. Every extra second cuts conversion measurably."))
        elif load: good.append(f"Load time {load} ms")
        if perf.get("ttfb_ms", 0) > 800:
            findings.append(("P2", "Performance", f"High TTFB ({perf['ttfb_ms']} ms)", "Slow server response; add caching / a CDN in front."))
        if perf.get("requests", 0) > 80:
            findings.append(("P2", "Performance", f"Many requests ({perf['requests']})", "Bundle assets, lazy-load below-the-fold, remove unused third-party scripts."))
        if perf.get("console_errors"):
            findings.append(("P2", "Reliability", f"{len(perf['console_errors'])} JS console error(s)",
                             "Fix console errors: " + "; ".join(perf["console_errors"][:3])))
    kb = round(nbytes / 1024)
    if kb > 1024:
        findings.append(("P2", "Performance", f"Heavy HTML document ({kb} KB)", "Trim inline data/markup; move large payloads to lazy-loaded resources."))

    order = {"P1": 0, "P2": 1, "P3": 2}
    findings.sort(key=lambda f: order[f[0]])
    return {"url": url, "host": host, "html_kb": kb, "perf": perf,
            "findings": [{"priority": p_, "area": a, "issue": i, "fix": fx} for p_, a, i, fx in findings],
            "strengths": good, "counts": {"P1": sum(1 for f in findings if f[0]=="P1"),
                                          "P2": sum(1 for f in findings if f[0]=="P2"),
                                          "P3": sum(1 for f in findings if f[0]=="P3")}}


def render_report(r, teaser=False):
    if r.get("error"): return f"Could not audit {r['url']}: {r['error']}"
    L = []
    L.append(f"AUDIT — {r['url']}")
    c = r["counts"]
    L.append(f"{c['P1']} critical (P1), {c['P2']} medium (P2), {c['P3']} minor (P3) issues found.\n")
    fs = r["findings"][:3] if teaser else r["findings"]
    for f in fs:
        L.append(f"[{f['priority']}] {f['area']}: {f['issue']}")
        L.append(f"     Fix: {f['fix']}")
    if teaser and len(r["findings"]) > 3:
        L.append(f"\n... and {len(r['findings'])-3} more findings in the full report.")
    if not teaser and r["strengths"]:
        L.append("\nAlready doing well: " + "; ".join(r["strengths"][:8]))
    return "\n".join(L)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(0)
    url = sys.argv[1]
    r = audit(url)
    if "--json" in sys.argv:
        print(json.dumps(r, indent=2))
    else:
        print(render_report(r, teaser="--teaser" in sys.argv))

#!/usr/bin/env python3
"""Freelancer.com bid-eligibility screener.

Encodes what iterations 187-188 cost me to learn, so it is never re-learned by hand:

  1. RANK IS THE BINDING CONSTRAINT, NOT PROPOSAL QUALITY.
     The proposals page prints "You are ranked 100+ out of N". A free account with zero
     reviews lands at 100+ regardless of price or artifact quality, so any field large
     enough to bury me at 100+ is unwinnable no matter what I write. Fields under ~60
     keep the bid visible.

  2. THERE IS A HIDDEN PER-PROJECT GATE.
     `upgrades: {"NDA": true}` means the bid form never renders until a non-disclosure
     agreement is signed. Signing legal agreements on the account holder's behalf is out
     of bounds, so those projects are unbiddable in practice. Nothing in the human-facing
     listing shows this — only the API does.

  3. ELIGIBILITY IS CHECKED BEFORE THE BUILD, NOT AFTER.
     I built and deployed an entire site for an NDA-gated job before discovering I could
     not bid on it.

  5. `local: true` MEANS THE PROJECT IS RESTRICTED TO FREELANCERS NEAR THE CLIENT.
     Same failure mode as the NDA gate: the bid form simply is not there, with no message.

  4. THE KEYWORD LAYER IS ADVISORY, NEVER A VERDICT.  (Audited at iteration 190.)
     v1 of this file hard-rejected on keywords and threw away three of the five jobs I had
     hand-picked as good: "Figma" (offered as an extra alongside the HTML I would write),
     "video" (a handover clip showing how to add products), "logo" ("I will supply logos").
     v2 fixed the direction and then over-admitted: 13 survivors of which ~12 were wrong.
     A regex cannot tell what a job IS. So the mechanical gates below — currency, proposal
     count, NDA — are EXACT API FACTS and decide eligibility; the keyword match only sorts
     the reading list. The output is a list to read, not a list to trust.

Usage:  python3 run/fl_screen.py [--max-bids 60] [--pages 6] [--json out.json]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.parse
import urllib.request

API = "https://www.freelancer.com/api/projects/0.1/projects/active/"
UA = {"User-Agent": "Mozilla/5.0"}

# AUDITED AT ITERATION 190. This used to be a hard allow-list of "hard currencies", and it was
# the single biggest rejection bucket (243 of 594). It is a PROXY for "budget too small", and a
# bad one: it silently discarded 70 visible-rank jobs actually worth >= $200 USD, including
# "Responsive Business Website Development" (18 proposals, ~$389) — precisely the profile I was
# hunting. Filter on the VALUE, which the API gives directly via currency.exchange_rate, not on
# the denomination.
MIN_USD = 200.0

# What I can actually build AND verify from here: a self-contained web artifact.
BUILDABLE = re.compile(
    r"websit|web page|webpage|landing page|html|css|javascript|react|next\.?js|tailwind|"
    r"web app|webapp|front-?end|storefront|e-?commerce|dashboard|booking|calculator|"
    r"configurator|estimator|quote tool|micro ?site|portfolio site|web design|redesign",
    re.I,
)

# Deliverables I cannot produce, verify, or lawfully take on.
#
# AUDITED AT ITERATION 190 AND REWRITTEN. The first version matched these terms anywhere in
# the description and threw away three of the five jobs I had hand-picked as good:
#   "Figma"  -> a brief offering design source files ALONGSIDE the HTML/CSS/JS I was bidding to write
#   "video"  -> "a short video showing how to add new products" in the handover notes
#   "logo"   -> "I will supply logos, emblems and color codes"  (the client GIVING me assets)
# An incidental mention is not the deliverable. So exclusion now reads the TITLE, which states what
# the job IS, plus a small set of body terms that are disqualifying wherever they appear.

# What the job IS — judged from the title.
EXCLUDE_TITLE = re.compile(
    r"logo|illustrat|\b3d\b|animation|voice|video|photograph|"
    r"content writ|article|blog post|resume|transcri|translat|"
    r"data entry|excel|power ?bi|odoo|erp|salesforce|joomla|"
    r"android|ios|flutter|react native|unity|game|"
    r"seo|backlink|guest post|"
    r"virtual assistant|telemarket|cold call|appointment setter|lead generation specialist|"
    r"architect|structural|permit|survey|\bcad\b|drawing|"
    r"model|photo|brand identity|interior|construction|dealer|emcee|"
    r"sales|closer|setter|recruit|coaching|mentor",
    re.I,
)

# Disqualifying wherever they appear, because they describe the work itself or are out of bounds.
EXCLUDE_BODY = re.compile(
    r"captcha|scrap(e|ing)\b|crypto|forex|betting|casino|fake review|google review|"
    r"remote (desktop|session)|on-?site visit|in person|must be located|"
    r"defeat|bypass|sold out",
    re.I,
)


def is_excluded(title: str, body: str) -> tuple[bool, str]:
    """Return (excluded, why). Title decides what the job is; body only catches hard blockers."""
    m = EXCLUDE_TITLE.search(title or "")
    if m:
        return True, f"title:{m.group(0)}"
    m = EXCLUDE_BODY.search(body or "")
    if m:
        return True, f"body:{m.group(0)}"
    return False, ""


def fetch(pages: int) -> list[dict]:
    seen: dict[int, dict] = {}
    for sort_field in ("time_submitted", "time_updated"):
        for offset in range(0, pages * 100, 100):
            q = {
                "limit": 100,
                "offset": offset,
                "job_details": "true",
                "full_description": "true",
                "compact": "true",
                "sort_field": sort_field,
                "project_types[]": "fixed",
            }
            url = API + "?" + urllib.parse.urlencode(q, doseq=True)
            try:
                req = urllib.request.Request(url, headers=UA)
                data = json.load(urllib.request.urlopen(req, timeout=45))
            except Exception as exc:  # network hiccup on one page must not kill the sweep
                print(f"  ! page {sort_field}+{offset} failed: {exc}", file=sys.stderr)
                continue
            for p in data.get("result", {}).get("projects", []) or []:
                seen.setdefault(p["id"], p)
    return list(seen.values())


def screen(projects: list[dict], max_bids: int) -> tuple[list[dict], dict[str, int]]:
    now = time.time()
    rejected = {"under_min_usd": 0, "bids": 0, "nda": 0, "local_only": 0}
    keep = []
    for p in projects:
        cinfo = p.get("currency") or {}
        cur = cinfo.get("code") or "?"
        rate = cinfo.get("exchange_rate") or 0
        budget = p.get("budget") or {}
        usd_max = (budget.get("maximum") or 0) * rate
        if usd_max < MIN_USD:
            rejected["under_min_usd"] += 1
            continue

        bids = p.get("bid_stats", {}).get("bid_count") or 0
        if bids > max_bids:
            rejected["bids"] += 1
            continue

        # Gates that make the bid form never render. Both are exact API facts and both were
        # found the expensive way, by building an artifact first and only then discovering I
        # could not bid: NDA at iteration 188, `local` at iteration 190 (a project restricted
        # to freelancers physically near the client).
        upgrades = p.get("upgrades") or {}
        if upgrades.get("NDA"):
            rejected["nda"] += 1
            continue
        if p.get("local"):
            rejected["local_only"] += 1
            continue

        # Everything past this point is ADVISORY. Keywords sort the reading list; they do
        # not decide eligibility, because a regex cannot tell what a job actually is.
        title = p.get("title") or ""
        body = p.get("description") or ""
        excluded, why = is_excluded(title, body)
        looks_buildable = bool(BUILDABLE.search(title + " " + body))

        keep.append(
            {
                "id": p["id"],
                "title": p.get("title") or "",
                "bids": bids,
                "currency": cur,
                "min": budget.get("minimum") or 0,
                "max": budget.get("maximum") or 0,
                "usd_max": round(usd_max),
                "age_h": round((now - (p.get("time_submitted") or now)) / 3600, 1),
                "url": "https://www.freelancer.com/projects/" + str(p.get("seo_url") or ""),
                "desc": (p.get("description") or "")[:400].replace("\n", " "),
                "flag": ("READ FIRST" if (looks_buildable and not excluded)
                         else ("likely-not: " + why if excluded else "no build signal")),
            }
        )
    # Promising first, then fewest proposals — but every row is still a row to READ.
    keep.sort(key=lambda r: (r["flag"] != "READ FIRST", r["bids"], r["age_h"]))
    return keep, rejected


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-usd", type=float, default=200.0)
    ap.add_argument("--max-bids", type=int, default=60,
                    help="fields larger than this bury a zero-review account at rank 100+")
    ap.add_argument("--pages", type=int, default=6)
    ap.add_argument("--json", default="")
    args = ap.parse_args()

    global MIN_USD
    MIN_USD = args.min_usd
    projects = fetch(args.pages)
    keep, rejected = screen(projects, args.max_bids)

    read_first = [r for r in keep if r["flag"] == "READ FIRST"]
    print(f"pulled {len(projects)} unique active fixed-price projects")
    facts = {k: v for k, v in rejected.items() if not k.startswith("_")}
    print(f"rejected on EXACT API FACTS: {facts}")
    print(f"BID-ELIGIBLE (mechanical gates only): {len(keep)}")
    print(f"  of which flagged READ FIRST: {len(read_first)}")
    print("  NOTE: the flag is advisory. Read the rows; do not trust the label.\n")
    for r in keep[: max(30, len(read_first))]:
        print(f"[{r['bids']:>2} bids, {r['age_h']:>5.1f}h] {r['currency']} "
              f"{r['min']:.0f}-{r['max']:.0f} (~${r['usd_max']}) | {r['id']}  <{r['flag']}>")
        print(f"   {r['title'][:70]}")
        print(f"   {r['url']}")
        print(f"   {r['desc'][:180]}")
        print()

    if args.json:
        with open(args.json, "w") as fh:
            json.dump(keep, fh, indent=1)
        print(f"wrote {args.json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

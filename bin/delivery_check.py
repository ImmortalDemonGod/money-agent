#!/usr/bin/env python3
"""Delivery-seam verification (issue #39, G4 -- "the headline residual"). A paid offer is only
safe when the thing the buyer lands on AFTER paying is already complete: CONSTITUTION rule 3 says
deliver in full at the instant of payment, and until this tool the pay->deliver seam was enforced
by prose alone. host_check.py proved the pattern for the publish seam (run 1 shipped ~60
iterations of crawler-invisible product); this is the same pattern for the delivery seam.

Checks, against the LIVE delivery URL (the success-redirect target -- never a local file):
  1. HTTP status < 400 (redirects followed, SSRF-guarded exactly like host_check);
  2. the served body is a real artifact: a size floor and no placeholder markers
     (<fill>, TODO, FILL ME -- the repo's own placeholder family);
  3. optional --expect-sha256: byte-exact match against the intended artifact;
  4. issue #35, folded in: with --payment-link and STRIPE_WRITE_KEY, the link's
     restrictions.completed_sessions.limit MUST be 1 -- the PROVIDER atomically refuses a second
     completed checkout, closing the race the ~120s verifier polling window leaves open. The
     limit is verified via the API, never trusted from the packet; no key -> FAIL (the agent that
     created the link holds the key, so an unverifiable limit is a misconfiguration, not an
     exemption). The API response must also identify this exact delivery URL as the link's
     post-payment redirect; an unrelated healthy URL is not evidence of delivery.

Output ends with one machine-readable line the aiv gate re-runs and trusts only fresh:
  DELIVERY_CHECK: <url> | status=<n> | bytes=<n> | content_type=<type|unacceptable> | placeholder=<none|FOUND> | sha256=<match|mismatch|n/a> | link_limit=<1|n|unverified|n/a> | verdict=<PASS|FAIL>

Usage: python3 bin/delivery_check.py <delivery-url> [--expect-sha256 <hex>] [--payment-link <url>]
"""
from __future__ import annotations
import hashlib
import json
import os
import re
import sys
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import host_check  # the SSRF guard + redirect-vetting fetch are shared, not reimplemented

PLACEHOLDER = re.compile(r"(<fill>|TODO|FILL ME)", re.IGNORECASE)
MIN_BYTES = 256  # smaller than any real deliverable this repo ships; a stub page is smaller still
# A delivery must identify itself as a consumable document, never an arbitrary response body.
# Deliberately accept broad text formats and common portable documents, but not a missing or
# generic binary Content-Type (which could hide a login page, an error payload, or a redirect shim).
DELIVERABLE_TYPES = {
    "application/json", "application/pdf", "application/zip",
    "text/csv", "text/html", "text/markdown", "text/plain",
}


def _fetch(url: str) -> tuple[int, bytes, str]:
    """host_check._get returns decoded text; delivery needs BYTES (sha256 of the artifact), so
    fetch through the same opener + guard with a bytes read."""
    if not host_check._public_https(url):
        print(f"  refused: {url} is not a public http(s) URL (SSRF guard)", file=sys.stderr)
        return 0, b"", ""
    req = urllib.request.Request(url, headers={"User-Agent": "delivery-check/1.0 (harness verifier)"})
    try:
        with host_check._OPENER.open(req, timeout=30) as r:
            body = r.read(5_000_001)
            if len(body) > 5_000_000:
                print("  refused: delivery artifact exceeds the verification cap", file=sys.stderr)
                return 0, b"", ""
            # get_content_type() defaults a missing header to text/plain; retain the distinction
            # because #39 requires an explicit content type from the delivery endpoint.
            header_type = r.headers.get("Content-Type", "")
            return r.status, body, header_type.split(";", 1)[0].strip().lower()
    except urllib.error.HTTPError as e:
        return e.code, b"", ""
    except Exception as e:
        print(f"  fetch failed: {type(e).__name__}: {e}", file=sys.stderr)
        return 0, b"", ""


def _payment_link(payment_link: str) -> dict | None:
    """#35: read the payment link's completed-sessions restriction from the Stripe API with the
    agent's own write key. Paginate rather than assuming a recent link is among the first 100."""
    key = os.environ.get("STRIPE_WRITE_KEY", "")
    if not key or "REPLACE_ME" in key:
        return None
    try:
        cursor = None
        while True:
            endpoint = "https://api.stripe.com/v1/payment_links?limit=100"
            if cursor:
                endpoint += "&starting_after=" + urllib.parse.quote(cursor, safe="")
            req = urllib.request.Request(endpoint, headers={"Authorization": f"Bearer {key}"})
            with urllib.request.urlopen(req, timeout=30) as r:
                data = json.loads(r.read().decode())
            links = data.get("data", [])
            for link in links:
                if link.get("url") == payment_link:
                    return link
            if not data.get("has_more") or not links:
                return None
            cursor = links[-1].get("id")
            if not cursor:
                return None
    except Exception as e:
        print(f"  stripe lookup failed: {type(e).__name__}: {e}", file=sys.stderr)
        return None


def _completion_redirect(link: dict | None) -> str | None:
    """Return the provider-configured post-payment redirect, if it is a public URL."""
    completion = (link or {}).get("after_completion") or {}
    redirect = completion.get("redirect") or {}
    url = redirect.get("url") if completion.get("type") == "redirect" else None
    return url if isinstance(url, str) and host_check._public_https(url) else None


def main() -> int:
    args = sys.argv[1:]
    if not args or args[0].startswith("--"):
        print("usage: delivery_check.py <delivery-url> [--expect-sha256 <hex>] [--payment-link <url>]",
              file=sys.stderr)
        return 2
    url = args[0]
    expect = payment_link = None
    it = iter(args[1:])
    for a in it:
        if a == "--expect-sha256":
            expect = next(it, None)
        elif a == "--payment-link":
            payment_link = next(it, None)

    status, body, content_type = _fetch(url)
    print(f"delivery page : HTTP {status}, {len(body)} bytes")
    acceptable_type = content_type in DELIVERABLE_TYPES
    print(f"content type  : {content_type or 'missing'}"
          + ("" if acceptable_type else " (not an accepted deliverable type)"))
    m = PLACEHOLDER.search(body.decode("utf-8", "replace"))
    placeholder = "FOUND" if m else "none"
    if m:
        print(f"placeholder   : {m.group()!r} present -- the deliverable is not complete")
    sha = "n/a"
    if expect:
        sha = "match" if hashlib.sha256(body).hexdigest() == expect.lower() else "mismatch"
        print(f"sha256        : {sha}")
    limit = redirect = "n/a"
    if payment_link:
        link = _payment_link(payment_link)
        limit_value = ((link or {}).get("restrictions") or {}).get("completed_sessions") or {}
        limit = str(limit_value.get("limit")) if limit_value.get("limit") is not None else "unverified"
        completion_url = _completion_redirect(link)
        redirect = "match" if completion_url == url else "mismatch"
        print(f"link limit    : {limit}"
              + ("   (#35: the provider must atomically cap completed sessions at 1)"
                 if limit != "1" else ""))
        print(f"success URL   : {completion_url or 'unverified'} ({redirect})")

    ok = (bool(status) and status < 400 and acceptable_type and len(body) >= MIN_BYTES and placeholder == "none"
          and sha in ("match", "n/a")
          and (payment_link is None or (limit == "1" and redirect == "match")))
    print(f"\nDELIVERY_CHECK: {url} | status={status} | bytes={len(body)} | "
          f"content_type={content_type if acceptable_type else 'unacceptable'} | "
          f"placeholder={placeholder} | sha256={sha} | link_limit={limit} | redirect={redirect} | "
          f"verdict={'PASS' if ok else 'FAIL'}")
    if not ok:
        print("NOT SAFELY SELLABLE: the pay->deliver seam is broken or uncapped -- fix it before "
              "the link goes live.", file=sys.stderr)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

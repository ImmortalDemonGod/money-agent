#!/usr/bin/env python3
"""Instrumentation verification + injection. The sibling of bin/host_check.py: host_check proves the
HOST serves the page to crawlers; this proves the page carries the BEACON TAG, so its traffic is
actually measured. Run 1 shipped ~60 iterations of un-instrumented funnels and bolted telemetry on
at iteration 097 -- too late to decide reach-vs-conversion (#65, F3). The fix is to make
instrumentation one mechanical line, not a remembered checklist.

Two jobs:

  --inject <file.html> --beacon <host> [--site <id>]
      Insert the one-line beacon tag before </body> if the file lacks it (idempotent). Fail-closed:
      exit != 0 if there is no </body> to anchor to. This is the mechanization -- a published site
      gets the tag by construction, not by memory.

  <url> [--beacon <host>]                    (default mode: verify a LIVE deployed site)
      Fetch the url (SSRF-guarded, reusing host_check's guard) and confirm the SERVED html carries
      the beacon tag. Emit the machine-readable line the gate re-runs for instrument claims:
        INSTRUMENT_CHECK: <url> | tag=<PRESENT|MISSING> | site=<id> | beacon=<host> | verdict=<PASS|FAIL>
      Exit != 0 if the tag is missing -- a site that ships without instrumentation FAILS (fail-closed).

That INSTRUMENT_CHECK line is the deterministic evidence for spine.py's stage-0 instrument-probe --
the exact analog of host_check's HOST_CHECK for the substrate probe. Cite it (from a PASSING run) in
the packet; bin/aiv_gate.sh RE-RUNS this tool on the cited url (self-typed lines are not trusted), so
a publish/instrument claim without a passing INSTRUMENT_CHECK for the live url does not clear stage 0.

Usage:
  python3 bin/instrument_check.py <url> [--beacon <host>]
  python3 bin/instrument_check.py --inject <file.html> --beacon <host> --site <id>
  python3 bin/instrument_check.py --selftest
"""
from __future__ import annotations
import os
import re
import sys

# Reuse the SSRF-guarded fetch from host_check.py (same dir, already reviewed) rather than
# re-implement the DNS-rebinding guard. This tool is agent-invocable, so the guard is load-bearing.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from host_check import _get  # type: ignore
except Exception:  # pragma: no cover - only if host_check is absent
    _get = None

# A beacon tag is a <script> whose src ends in /beacon.js. data-site attributes it to a page.
_TAG_RE = re.compile(r'<script\b[^>]*\bsrc=["\'][^"\']*/beacon\.js(?:\?[^"\']*)?["\'][^>]*>', re.I)
_SITE_RE = re.compile(r'data-site=["\']([^"\']*)["\']', re.I)
_HOST_RE = re.compile(r'src=["\'](https?://[^"\']+?)/beacon\.js', re.I)


def tag_line(beacon: str, site: str) -> str:
    return f'<script src="{beacon.rstrip("/")}/beacon.js" data-site="{site}"></script>'


def has_tag(html: str) -> bool:
    return bool(_TAG_RE.search(html or ""))


def inject(path: str, beacon: str, site: str) -> int:
    """Add the tag before the last </body> if absent. Idempotent; fail-closed on no anchor."""
    with open(path, encoding="utf-8") as f:
        html = f.read()
    if has_tag(html):
        print(f"  already instrumented: {path}", file=sys.stderr)
        return 0
    low = html.lower()
    idx = low.rfind("</body>")
    if idx == -1:
        print(f"  REFUSED (fail-closed): {path} has no </body> to anchor the beacon tag", file=sys.stderr)
        return 1
    new = html[:idx] + "  " + tag_line(beacon, site) + "\n" + html[idx:]
    with open(path, "w", encoding="utf-8") as f:
        f.write(new)
    print(f"  instrumented: {path} (site={site or '(none)'}, beacon={beacon})", file=sys.stderr)
    return 0


def check(url: str, beacon: str | None = None) -> int:
    if _get is None:
        print("  fatal: bin/host_check.py._get is unavailable (SSRF-guarded fetch missing)", file=sys.stderr)
        return 2
    status, html = _get(url)
    present = has_tag(html)
    site_m = _SITE_RE.search(html or "") if present else None
    host_m = _HOST_RE.search(html or "") if present else None
    site = site_m.group(1) if site_m else ""
    host = host_m.group(1) if host_m else "MISSING"

    ok = bool(status and status < 400 and present)
    if ok and beacon:
        want = beacon.split("://", 1)[-1].rstrip("/")
        ok = host != "MISSING" and host.split("://", 1)[-1].rstrip("/") == want

    print(f"page          : HTTP {status}")
    print(f"beacon tag    : {'PRESENT' if present else 'MISSING'}"
          + (f" (site={site or '(none)'}, beacon={host})" if present else ""))
    print(f"\nINSTRUMENT_CHECK: {url} | tag={'PRESENT' if present else 'MISSING'} | "
          f"site={site or '(none)'} | beacon={host} | verdict={'PASS' if ok else 'FAIL'}")
    if not ok:
        print("NOT INSTRUMENTED: the served page does not carry the beacon tag (or points at the "
              "wrong beacon), so its traffic is invisible. Inject it with --inject before counting "
              "this site as instrumented.", file=sys.stderr)
    return 0 if ok else 1


def selftest() -> int:
    import tempfile
    fails = []

    def _write(s):
        f = tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8")
        f.write(s)
        f.close()
        return f.name

    # 1. inject into a page lacking the tag -> present, with the site id
    p = _write("<!doctype html><html><body><h1>x</h1></body></html>")
    inject(p, "https://beacon.example", "siteA")
    html = open(p, encoding="utf-8").read()
    os.unlink(p)
    if not has_tag(html):
        fails.append("inject did not add the tag")
    if "siteA" not in html:
        fails.append("inject dropped the site id")

    # 2. idempotent: injecting again adds no second tag
    p = _write(html)
    inject(p, "https://beacon.example", "siteA")
    n = open(p, encoding="utf-8").read().lower().count("/beacon.js")
    os.unlink(p)
    if n != 1:
        fails.append(f"inject not idempotent ({n} tags after 2nd run)")

    # 3. a page with no </body> fails closed (does not silently pass)
    p = _write("<html><h1>no body element</h1></html>")
    rc = inject(p, "https://beacon.example", "s")
    os.unlink(p)
    if rc == 0:
        fails.append("page with no </body> did not fail closed")

    # 4. tag detection: true positive and true negative
    if not has_tag('<script src="https://x/beacon.js" data-site="a"></script>'):
        fails.append("has_tag false-negative on a real tag")
    if has_tag('<script src="https://x/analytics-other.js"></script>'):
        fails.append("has_tag false-positive on a non-beacon script")

    if fails:
        for m in fails:
            print("  FAIL:", m, file=sys.stderr)
        print(f"selftest: {len(fails)} check(s) FAILED", file=sys.stderr)
        return 1
    print("selftest: all passed (inject, idempotent, fail-closed, tag detection)")
    return 0


def _opt(args, name, default=None):
    return args[args.index(name) + 1] if name in args and args.index(name) + 1 < len(args) else default


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print(__doc__, file=sys.stderr)
        return 2
    if args[0] == "--selftest":
        return selftest()
    if args[0] == "--inject":
        if len(args) < 2 or args[1].startswith("--"):
            print("usage: instrument_check.py --inject <file.html> --beacon <host> [--site <id>]", file=sys.stderr)
            return 2
        path = args[1]
        beacon = _opt(args, "--beacon") or os.environ.get("BEACON_ORIGIN")
        site = _opt(args, "--site", "")
        if not beacon:
            print("  --inject needs --beacon <host> (or the BEACON_ORIGIN env var)", file=sys.stderr)
            return 2
        return inject(path, beacon, site)
    return check(args[0], _opt(args, "--beacon"))


if __name__ == "__main__":
    raise SystemExit(main())

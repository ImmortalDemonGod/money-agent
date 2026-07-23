#!/usr/bin/env python3
"""Serving-layer verification. A page is only "published" if the HOST actually serves it to
crawlers -- run 1 learned this the hard way: surge.sh force-served `robots.txt: Disallow: /` on
every site, so ~60 iterations of "shipped" product were invisible to every compliant crawler and
AI bot, and nobody checked until iteration 070. The HTML was fine; the SERVING LAYER was the lie.

Checks, against the LIVE url (never a local file):
  1. HTTP status of the page itself (redirects followed);
  2. the EFFECTIVE robots.txt as served at the origin -- does any `User-agent: *` group
     `Disallow: /` (the surge trap)?
  3. meta robots noindex in the served HTML;
  4. canonical presence (informational);
  5. sitemap.xml reachability (informational).

Output ends with one machine-readable line the aiv gate looks for in packets that claim a publish:
  HOST_CHECK: <url> | status=<n> | robots=<ALLOW|DISALLOW-ALL|NONE> | meta=<index|noindex> | ...
Exit != 0 on: status >= 400, robots Disallow-all, or meta noindex. Cite this line (from a PASSING
run) in the packet; a publish claim with no HOST_CHECK line fails bin/aiv_gate.sh.

Usage: python3 bin/host_check.py <url>
"""
from __future__ import annotations
import http.client
import ipaddress
import os
import re
import socket
import sys
import urllib.parse
import urllib.request
import urllib.error


def _public_https(url: str) -> bool:
    """SSRF guard: this tool is agent-invocable, so it must not be turned into a probe of
    operator-local services or cloud metadata (169.254.169.254). Accept only http/https to a
    public host (reject loopback/private/link-local/reserved resolved addresses).

    DNS rebinding is closed by the guarded connections below: _public_https vets the name's
    resolution, and the connection classes re-check the peer the socket ACTUALLY connected to --
    so a rebinding answer that flips between vet and connect can never reach a private address."""
    p = urllib.parse.urlparse(url)
    if p.scheme not in ("http", "https") or not p.hostname:
        return False
    try:
        for _fam, _, _, _, sa in socket.getaddrinfo(
                p.hostname, p.port or (443 if p.scheme == "https" else 80)):
            if not _ip_is_public(sa[0]):
                return False
    except Exception:
        return False
    return True


def _ip_is_public(ip_str: str) -> bool:
    try:
        ip = ipaddress.ip_address(ip_str)
    except ValueError:
        return False
    return not (ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved
                or ip.is_multicast or ip.is_unspecified)


# DNS-rebinding close-out (the residual the docstring used to defer). urllib re-resolves at connect
# time, so vetting the NAME is not enough; these connections re-check the peer the socket actually
# connected to and abort if it is not public. Load-bearing now that obligation_watch runs
# delivery_check -> this opener ON THE VERIFIER HOST, where SSRF reaches the real keys/feeds.
def _proxy_ips() -> set:
    """IPs of any configured egress proxy. A proxied request connects to the PROXY (often loopback),
    not the target, so the proxy's own address must be exempt from the peer check -- the proxy owns
    egress policy there, and _public_https still vets the target NAME as best effort."""
    ips = set()
    for var in ("HTTPS_PROXY", "https_proxy", "HTTP_PROXY", "http_proxy"):
        v = os.environ.get(var)
        if not v:
            continue
        host = urllib.parse.urlparse(v if "://" in v else "http://" + v).hostname
        if not host:
            continue
        try:
            for _f, _, _, _, sa in socket.getaddrinfo(host, None):
                ips.add(sa[0])
        except Exception:
            ips.add(host)
    return ips


def _guard_peer(sock) -> None:
    peer = sock.getpeername()[0]
    # A DIRECT connection to a private/reserved peer is a rebinding hit and is refused; the
    # configured proxy (which may itself be loopback) is exempt because it, not this client,
    # performed the target resolution and connection.
    if not _ip_is_public(peer) and peer not in _proxy_ips():
        raise OSError(f"SSRF guard: peer {peer} is not public and not the configured proxy "
                      "(DNS rebinding blocked)")


class _GuardedHTTPSConnection(http.client.HTTPSConnection):
    def connect(self):
        super().connect()
        try:
            _guard_peer(self.sock)
        except OSError:
            self.close()
            raise


class _GuardedHTTPConnection(http.client.HTTPConnection):
    def connect(self):
        super().connect()
        try:
            _guard_peer(self.sock)
        except OSError:
            self.close()
            raise


class _GuardedHTTPSHandler(urllib.request.HTTPSHandler):
    def https_open(self, req):
        return self.do_open(_GuardedHTTPSConnection, req, context=self._context)


class _GuardedHTTPHandler(urllib.request.HTTPHandler):
    def http_open(self, req):
        return self.do_open(_GuardedHTTPConnection, req)


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # revalidate the redirect target through the same SSRF guard before following.
        # ROUND-3 FIX: raise with code 599, NOT the original 3xx -- _get returns e.code, and a 3xx
        # here satisfied `status < 400`, so a page redirecting to a private target got verdict=PASS
        # and the aiv gate accepted the publish claim. A blocked redirect is a FAILURE.
        if not _public_https(newurl):
            raise urllib.error.HTTPError(newurl, 599, "redirect to non-public target blocked "
                                         "(SSRF guard) -- treated as unpublished", headers, fp)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


_OPENER = urllib.request.build_opener(_NoRedirect, _GuardedHTTPSHandler, _GuardedHTTPHandler)


def _get(url: str, timeout: int = 30) -> tuple[int, str]:
    if not _public_https(url):
        print(f"  refused: {url} is not a public http(s) URL (SSRF guard)", file=sys.stderr)
        return 0, ""
    req = urllib.request.Request(url, headers={"User-Agent": "host-check/2.0 (harness verifier)"})
    try:
        with _OPENER.open(req, timeout=timeout) as r:
            return r.status, r.read(512_000).decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception as e:
        print(f"  fetch failed: {type(e).__name__}: {e}", file=sys.stderr)
        return 0, ""


def robots_verdict(txt: str) -> str:
    """Does the `User-agent: *` group disallow everything? (Parses group-wise: a Disallow: /
    under a specific bot's group is not the trap; under * it is.)"""
    if not txt:
        return "NONE"
    # A group can carry MULTIPLE consecutive User-agent lines before its rules; the group is a
    # wildcard group if ANY of them is `*`. A run of UA lines accumulates; the first rule line ends
    # the UA run. (The old code overwrote `star` on each UA line, so `UA: *` then `UA: Googlebot`
    # then `Disallow: /` wrongly returned ALLOW and let a crawler-blocked page pass -- CodeRabbit.)
    star = False        # is the CURRENT group a wildcard group?
    in_ua_run = False   # are we still reading the UA lines of a group?
    for raw in txt.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        m = re.match(r"(?i)^user-agent\s*:\s*(.+)$", line)
        if m:
            if not in_ua_run:      # starting a new group's UA run
                star = False
                in_ua_run = True
            star = star or (m.group(1).strip() == "*")
            continue
        in_ua_run = False          # first non-UA line ends the UA run
        if star and re.match(r"(?i)^disallow\s*:\s*/\s*$", line):
            return "DISALLOW-ALL"
    return "ALLOW"


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: host_check.py <url>", file=sys.stderr)
        return 2
    url = sys.argv[1]
    origin = "{0.scheme}://{0.netloc}".format(urllib.parse.urlparse(url))

    status, html = _get(url)
    print(f"page          : HTTP {status}")

    rstatus, rbody = _get(origin + "/robots.txt")
    robots = robots_verdict(rbody if rstatus == 200 else "")
    print(f"robots.txt    : HTTP {rstatus} -> {robots}"
          + ("   ⚠ THE SURGE TRAP: crawlers are told to ignore this entire host"
             if robots == "DISALLOW-ALL" else ""))

    meta = "noindex" if re.search(
        r'<meta[^>]+name=["\']robots["\'][^>]+content=["\'][^"\']*noindex', html, re.I) else "index"
    print(f"meta robots   : {meta}")
    canonical = "present" if re.search(r'<link[^>]+rel=["\']canonical["\']', html, re.I) else "absent"
    print(f"canonical     : {canonical} (informational)")
    sstatus, _ = _get(origin + "/sitemap.xml")
    print(f"sitemap.xml   : HTTP {sstatus} (informational)")

    ok = status and status < 400 and robots != "DISALLOW-ALL" and meta != "noindex"
    print(f"\nHOST_CHECK: {url} | status={status} | robots={robots} | meta={meta} | "
          f"canonical={canonical} | sitemap={sstatus} | verdict={'PASS' if ok else 'FAIL'}")
    if not ok:
        print("NOT PUBLISHED in any meaningful sense: fix the serving layer or move hosts before "
              "counting this as shipped.", file=sys.stderr)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

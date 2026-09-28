#!/usr/bin/env python3
"""Validate the machine-readable public offer stays aligned with the checkout CTA."""
from __future__ import annotations

import json
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKOUT = "https://buy.stripe.com/14A7sN84bblpd6a72K7ok0i"


class OfferParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.jsonld: list[str] = []
        self.in_jsonld = False
        self.links: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = {key: value or "" for key, value in attrs}
        if tag == "script" and attrs_dict.get("type") == "application/ld+json":
            self.in_jsonld = True
        if tag == "link":
            self.links.append(attrs_dict)

    def handle_data(self, data: str) -> None:
        if self.in_jsonld:
            self.jsonld.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self.in_jsonld:
            self.in_jsonld = False


html = (ROOT / "showcase/index.html").read_text(encoding="utf-8")
llms = (ROOT / "showcase/llms.txt").read_text(encoding="utf-8")
parser = OfferParser()
parser.feed(html)
offers = [json.loads(raw) for raw in parser.jsonld]
offer = next((item for item in offers if item.get("@type") == "Offer"), None)
assert offer is not None, "showcase must publish a Schema.org Offer"
assert offer["price"] == "1.00" and offer["priceCurrency"] == "USD"
assert offer["url"] == CHECKOUT
assert any(link.get("href") == "/llms.txt" for link in parser.links)
assert CHECKOUT in llms and "$1.00 USD" in llms
assert "no future work is promised" in llms
assert "$1 USD" in html
print("showcase offer check passed")

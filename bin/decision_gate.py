#!/usr/bin/env python3
"""P3 -- generic recorded-decision gate (S11). disclosure_gate.py proved the pattern ("a rule
with no mechanism is a wish"): before an action in a declared RISK CLASS, a decision record
keyed by the content's hash must exist -- the gate FAILS CLOSED ON ABSENCE and NEVER GRADES THE
CONTENT (judgment stays human/agent; the mechanism only proves the judgment happened and was
recorded before the act).

disclosure_gate stays the specialized send-class instance (its lead/cut positional rules and the
i18n regexes -- the iteration-093 Japanese lesson -- survive untouched; do NOT reimplement them
here). This gate covers the OTHER declared classes:

  publish            a page/artifact going to a public host
  listing            a marketplace/storefront listing
  data-acquisition   fetching/scraping third-party data into the run; ADDITIONALLY requires a
                     committed provenance manifest (sha256-pinned log of every input fetched) --
                     an acquisition without provenance is untraceable by construction

Record format, one line per decision in DECISION_LOG.md:
  - class:<risk-class> | body:<10-hex> | decision:<free text> | rationale:<why>
  - class:data-acquisition | body:<10-hex> | decision:... | rationale:... | provenance:<sha256 of
    the committed manifest file>

Usage:
    python3 bin/decision_gate.py <risk-class> <bodyfile>    # prints hash; exit!=0 blocks
Importable: check(risk_class, body) -> (ok, message)

Wiring note (stated, not hidden): chokepoints arrive with the tools that PERFORM these actions
-- publishing today is ad hoc tooling, so this gate is the mechanism those tools must call (the
P6 probe registry documents which probe + which decision class each claim type needs). mail.py
already calls its specialized sibling.
"""
from __future__ import annotations
import hashlib
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LOG = REPO / "DECISION_LOG.md"
CLASSES = ("publish", "listing", "data-acquisition")


def body_hash(body: str) -> str:
    return hashlib.sha1(body.strip().encode("utf-8")).hexdigest()[:10]


def _decision(risk_class: str, h: str) -> dict | None:
    if not LOG.exists():
        return None
    for line in LOG.read_text().splitlines():
        if f"class:{risk_class}" in line and f"body:{h}" in line:
            d = {}
            for part in line.lstrip("- ").split("|"):
                if ":" in part:
                    k, _, v = part.strip().partition(":")
                    d[k.strip()] = v.strip()
            return d
    return None


def check(risk_class: str, body: str) -> tuple[bool, str]:
    if risk_class not in CLASSES:
        return False, (f"unknown risk class {risk_class!r} (known: {CLASSES}; 'send' is "
                       "disclosure_gate.py's specialized domain)")
    h = body_hash(body)
    dec = _decision(risk_class, h)
    if dec is None:
        return False, (f"no decision recorded for this {risk_class} body (hash {h}). Decide,"
                       f" then add ONE line to DECISION_LOG.md:\n  - class:{risk_class} | "
                       f"body:{h} | decision:<what you decided> | rationale:<why>"
                       + (" | manifest:<repo-relative path> | provenance:<sha256 of THAT file>"
                          if risk_class == "data-acquisition" else ""))
    if len(dec.get("decision", "")) < 3 or len(dec.get("rationale", "")) < 8:
        return False, (f"decision record for {h} is a stamp, not a decision -- 'decision' and a "
                       "real 'rationale' are required (the record proves the judgment HAPPENED).")
    if risk_class == "data-acquisition":
        prov = dec.get("provenance", "")
        if not (len(prov) == 64 and all(c in "0123456789abcdef" for c in prov.lower())):
            return False, (f"data-acquisition decision for {h} carries no provenance sha256 -- "
                           "an acquisition without a pinned input manifest is untraceable by "
                           "construction.")
        # S16 FIX (adversarial correctness pass): the manifest must be NAMED, and THAT file must
        # hash to the declared value. The old check accepted the hash of ANY committed file (a
        # README would pass), so the "pinned manifest" was pinned to nothing in particular. The
        # record now carries `manifest:<repo-relative-path>`; we hash exactly that path.
        mpath = dec.get("manifest", "")
        if not mpath:
            return False, (f"data-acquisition decision for {h} names no `manifest:<path>` -- the "
                           "provenance sha256 must pin a SPECIFIC committed file, not any file "
                           "that happens to share the hash.")
        target = (REPO / mpath).resolve()
        try:
            target.relative_to(REPO.resolve())  # no ../ escape outside the repo
        except ValueError:
            return False, f"manifest path {mpath!r} escapes the repo -- refused."
        if not (target.is_file() and not target.is_symlink()):
            return False, (f"manifest {mpath!r} is not a committed regular file -- the record "
                           "points at nothing.")
        actual = hashlib.sha256(target.read_bytes()).hexdigest()
        if actual != prov.lower():
            return False, (f"manifest {mpath!r} hashes {actual[:12]}... but the record declares "
                           f"provenance {prov[:12]}... -- the pin does not match its file.")
    return True, f"OK: {risk_class} decision on record for {h} (rationale recorded)"


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: decision_gate.py <publish|listing|data-acquisition> <bodyfile>",
              file=sys.stderr)
        return 2
    body = Path(sys.argv[2]).read_text()
    print(f"body hash: {body_hash(body)}")
    ok, msg = check(sys.argv[1], body)
    print(("PASS: " if ok else "BLOCK: ") + msg, file=sys.stdout if ok else sys.stderr)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

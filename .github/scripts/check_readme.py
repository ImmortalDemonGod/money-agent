#!/usr/bin/env python3
"""README integrity check (stdlib only, no deps).

Catches the exact regressions this repo has hit before: stale relative links to
files that were moved or removed, a missing hero asset, a broken in-page nav
anchor, an unbalanced ```mermaid fence, and curly quotes that drift from the
repo's straight-quote house style.

It deliberately does NOT check `../../...` GitHub web routes (issues, commits,
pull/N, stargazers) or external http(s) links -- those are not files on disk and
validating them would make CI flaky. Scope: relative file links, images, nav
anchors, fences, and typography.

Usage: python3 .github/scripts/check_readme.py [README.md ...]
Exit 0 if every checked file passes; 1 otherwise.
"""
import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

MD_LINK = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)")   # [text](target) and ![alt](target)
IMG_SRC = re.compile(r'<img\b[^>]*?\bsrc="([^"]+)"', re.IGNORECASE)
HEADER = re.compile(r"^#{1,6}\s+(.*?)\s*$")
CURLY = "“”‘’"  # " " ' '


def slug(text):
    """Approximate GitHub's header-anchor slug algorithm."""
    s = text.strip().lower()
    s = re.sub(r"[`*_~]", "", s)          # strip inline markdown emphasis/code
    s = re.sub(r"[^\w\s-]", "", s)        # drop punctuation (parens, commas, ...)
    s = s.strip().replace(" ", "-")
    return s


def is_external(target):
    return target.startswith(("http://", "https://", "mailto:", "../../"))


def check(path):
    errors = []
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    lines = text.splitlines()

    # 1. Typography: no curly quotes (house style is straight quotes).
    for i, line in enumerate(lines, 1):
        for ch in line:
            if ch in CURLY:
                errors.append(f"{path}:{i}: curly quote {ch!r} (use straight quotes)")
                break

    # 2. Balanced code fences (catches an unterminated ```mermaid / ```bash block).
    if text.count("```") % 2 != 0:
        errors.append(f"{path}: unbalanced ``` code fences")

    # 3. Anchor targets (nav) must resolve to a real header slug in this file.
    slugs = {slug(m.group(1)) for m in (HEADER.match(l) for l in lines) if m}
    # 4. Relative link/image targets must point to a file that exists on disk.
    targets = MD_LINK.findall(text) + IMG_SRC.findall(text)
    for raw in targets:
        target = raw.strip()
        if target.startswith("#"):
            if slug(target[1:]) not in slugs:
                errors.append(f"{path}: nav anchor '{target}' has no matching header")
            continue
        if is_external(target) or not target:
            continue
        rel = target.split("#", 1)[0].split("?", 1)[0]
        if not os.path.exists(os.path.join(REPO_ROOT, rel)):
            errors.append(f"{path}: relative link '{rel}' does not exist")
    return errors


def main(argv):
    files = argv[1:] or ["README.md"]
    all_errors = []
    for f in files:
        all_errors.extend(check(f))
    if all_errors:
        print("README check FAILED:")
        for e in all_errors:
            print("  - " + e)
        return 1
    print("README check passed: " + ", ".join(files))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

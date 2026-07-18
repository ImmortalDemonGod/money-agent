#!/usr/bin/env python3
"""README + diagram-source integrity check (stdlib only, no deps).

Catches the regressions this repo has actually hit:
  - stale relative links to files that were moved or removed
  - a missing hero / diagram asset
  - a broken in-page nav anchor
  - an unbalanced ```mermaid / ```text fence
  - curly quotes drifting from the straight-quote house style
  - em/en dashes (and their HTML entities) drifting back in -- in the README
    prose AND in the .github/assets/*.mmd diagram sources that render into the
    committed images (an em-dash in a subgraph label is invisible until you look
    at the PNG, so the source is guarded directly)

Scope of the link check: relative file links, images, and nav anchors only. It
deliberately does NOT check `../../...` GitHub web routes (issues, commits,
pull/N, stargazers) or external http(s) links -- those are not files on disk and
validating them would make CI flaky.

Usage: python3 .github/scripts/check_readme.py [README.md ...]
Always also scans .github/assets/*.mmd for typography, regardless of args.
Exit 0 if everything passes; 1 otherwise.
"""
import glob
import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

MD_LINK = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)")   # [text](target) and ![alt](target)
IMG_SRC = re.compile(r'<img\b[^>]*?\bsrc="([^"]+)"', re.IGNORECASE)
HEADER = re.compile(r"^#{1,6}\s+(.*?)\s*$")
CURLY = "“”‘’"  # " " ' '
# em-dash, en-dash, and every HTML entity form of them (named, decimal, hex).
FANCY_DASH = re.compile(r"[—–]|&(?:m|n)dash;|&#821[12];|&#x201[34];", re.IGNORECASE)


def slug(text):
    """Approximate GitHub's header-anchor slug algorithm."""
    s = text.strip().lower()
    s = re.sub(r"[`*_~]", "", s)          # strip inline markdown emphasis/code
    s = re.sub(r"[^\w\s-]", "", s)        # drop punctuation (parens, commas, ...)
    return s.strip().replace(" ", "-")


def is_external(target):
    return target.startswith(("http://", "https://", "mailto:", "../../"))


def typography(path, text):
    """Checks that apply to any text file: no curly quotes, no em/en dashes."""
    errors = []
    for i, line in enumerate(text.splitlines(), 1):
        if any(ch in CURLY for ch in line):
            errors.append(f"{path}:{i}: curly quote (use straight quotes)")
        for m in FANCY_DASH.finditer(line):
            errors.append(f"{path}:{i}: em/en dash {m.group()!r} "
                          f"(use plain ASCII -- comma, colon, parens, or '-')")
    return errors


def markdown_structure(path, text):
    """Checks specific to the rendered markdown page."""
    errors = []
    if text.count("```") % 2 != 0:
        errors.append(f"{path}: unbalanced ``` code fences")
    slugs = {slug(m.group(1)) for m in (HEADER.match(l) for l in text.splitlines()) if m}
    for raw in MD_LINK.findall(text) + IMG_SRC.findall(text):
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
    md_files = argv[1:] or ["README.md"]
    _contrib = os.path.join(REPO_ROOT, "CONTRIBUTING.md")
    if os.path.exists(_contrib) and "CONTRIBUTING.md" not in md_files:
        md_files = md_files + ["CONTRIBUTING.md"]
    mmd_files = sorted(glob.glob(os.path.join(REPO_ROOT, ".github/assets/*.mmd")))
    errors = []
    for f in md_files:
        text = open(f, encoding="utf-8").read()
        errors += typography(f, text) + markdown_structure(f, text)
    for f in mmd_files:                       # diagram sources: typography only
        errors += typography(f, open(f, encoding="utf-8").read())
    checked = md_files + [os.path.relpath(f, REPO_ROOT) for f in mmd_files]
    if errors:
        print("README check FAILED:")
        for e in errors:
            print("  - " + e)
        return 1
    print("README check passed: " + ", ".join(checked))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

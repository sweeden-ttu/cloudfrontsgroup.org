#!/usr/bin/env python3
"""
Output-parity checker for the Jekyll migration of cloudfrontsgroup.org.

  python3 scripts/compare_build.py snapshot            # copy current root *.html -> _baseline/
  python3 scripts/compare_build.py compare             # diff _site/*.html against _baseline/
  python3 scripts/compare_build.py compare --strict    # byte-exact instead of whitespace-normalized
  python3 scripts/compare_build.py compare index.html  # one page only

Exit status is 0 when every page matches, 1 otherwise.
Whitespace normalization: collapse runs of spaces/tabs, strip line ends, drop blank lines.
"""
import difflib
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASELINE = os.path.join(ROOT, "_baseline")
SITE = os.path.join(ROOT, "_site")


def root_pages():
    return sorted(f for f in os.listdir(ROOT) if f.endswith(".html"))


def normalize(text):
    lines = []
    for line in text.splitlines():
        line = re.sub(r"[ \t]+", " ", line).strip()
        if line:
            lines.append(line)
    return lines


def snapshot():
    os.makedirs(BASELINE, exist_ok=True)
    pages = root_pages()
    for page in pages:
        shutil.copy2(os.path.join(ROOT, page), os.path.join(BASELINE, page))
    print(f"Snapshotted {len(pages)} pages into _baseline/")
    return 0


def compare(strict=False, only=None):
    if not os.path.isdir(BASELINE):
        print("No _baseline/ found. Run: python3 scripts/compare_build.py snapshot", file=sys.stderr)
        return 1
    if not os.path.isdir(SITE):
        print("No _site/ found. Run: bundle exec jekyll build", file=sys.stderr)
        return 1

    pages = sorted(f for f in os.listdir(BASELINE) if f.endswith(".html"))
    if only:
        pages = [p for p in pages if p in only]
    failures = 0
    for page in pages:
        base_path = os.path.join(BASELINE, page)
        site_path = os.path.join(SITE, page)
        if not os.path.exists(site_path):
            print(f"MISSING  {page}  (not in _site/)")
            failures += 1
            continue
        with open(base_path, encoding="utf-8") as f:
            base = f.read()
        with open(site_path, encoding="utf-8") as f:
            built = f.read()
        a = base.splitlines() if strict else normalize(base)
        b = built.splitlines() if strict else normalize(built)
        if a == b:
            print(f"OK       {page}")
            continue
        failures += 1
        print(f"DIFF     {page}")
        for line in difflib.unified_diff(a, b, f"_baseline/{page}", f"_site/{page}", lineterm="", n=1):
            print("         " + line)
    extra = sorted(set(f for f in os.listdir(SITE) if f.endswith(".html")) - set(pages)) if not only else []
    for page in extra:
        print(f"EXTRA    {page}  (in _site/ but not in baseline)")
    print()
    print(f"{len(pages) - failures}/{len(pages)} pages match" + (" (strict)" if strict else ""))
    return 1 if failures else 0


def main(argv):
    if len(argv) < 2 or argv[1] not in ("snapshot", "compare"):
        print(__doc__)
        return 2
    if argv[1] == "snapshot":
        return snapshot()
    strict = "--strict" in argv
    only = [a for a in argv[2:] if not a.startswith("--")] or None
    return compare(strict=strict, only=only)


if __name__ == "__main__":
    sys.exit(main(sys.argv))

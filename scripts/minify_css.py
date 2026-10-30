#!/usr/bin/env python3
"""
Regenerate style.min.css from style.css.

    python3 scripts/minify_css.py

Uses the `csscompressor` package (pip install csscompressor). The head include
links style.min.css, so run this after every change to style.css.
"""
import os
import sys

try:
    import csscompressor
except ImportError:
    sys.exit("csscompressor is not installed: pip install csscompressor")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "style.css")
DST = os.path.join(ROOT, "style.min.css")

with open(SRC, encoding="utf-8") as f:
    css = f.read()
minified = csscompressor.compress(css)
with open(DST, "w", encoding="utf-8") as f:
    f.write(minified + "\n")
print(f"style.min.css: {len(css):,} -> {len(minified):,} bytes")

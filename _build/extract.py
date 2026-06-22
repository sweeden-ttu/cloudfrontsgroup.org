#!/usr/bin/env python3
"""
Extract unique body content from existing HTML pages into _pages/.
Finds content between the header and footer, preserving #main-content and
any subsequent elements before the footer.
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = os.path.join(ROOT, '_pages')

# Pages to extract (root-level .html files)
page_files = [f for f in os.listdir(ROOT) if f.endswith('.html') and f != '404.html']
page_files.append('404.html')

# Exclude blog pages (they have their own paths)
page_files = [f for f in page_files if not f.startswith('blog/')]

for fname in sorted(page_files):
    path = os.path.join(ROOT, fname)
    with open(path, 'r') as f:
        content = f.read()

    # Extract content between </header> and <footer>
    # We want everything after the </header> line and before <footer>
    header_end = content.find('</header>')
    footer_start = content.find('<footer>')

    if header_end == -1 or footer_start == -1:
        print(f"  ⚠ Could not find header/footer in {fname}")
        continue

    body_content = content[header_end + len('</header>'):footer_start]

    # Clean up leading/trailing whitespace
    body_content = body_content.strip()

    # Write to _pages/
    name = os.path.splitext(fname)[0]
    out_path = os.path.join(PAGES, f'{name}.html')
    with open(out_path, 'w') as f:
        f.write(body_content)
        f.write('\n')

    print(f"  ✓ {name}.html ({len(body_content)} chars)")

print(f"\nExtracted {len(page_files)} pages to _pages/")

#!/usr/bin/env python3
"""Regenerate ~/hud/foreclosures.html from data/bell_foreclosure_ocr/results.json."""

from __future__ import annotations

import html
import json
from pathlib import Path
from urllib.parse import quote_plus

HUD_DIR = Path(__file__).resolve().parent.parent
JSON_PATH = HUD_DIR / "data" / "bell_foreclosure_ocr" / "results.json"
OUT_HTML = HUD_DIR / "foreclosures.html"


def main() -> int:
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    items: list[tuple[str, str, str, str]] = []
    for block in data:
        pdf_url = block.get("url") or ""
        label = f'{block.get("month")} {block.get("day")}'
        for addr in block.get("addresses") or []:
            a = (addr or "").strip()
            if not a:
                continue
            map_q = quote_plus(a.rstrip("."))
            map_url = f"https://maps.google.com/?q={map_q}"
            items.append((a, pdf_url, map_url, label))

    lis = []
    for addr, pdf_url, map_url, label in items:
        esc_addr = html.escape(addr, quote=False)
        esc_pdf = html.escape(pdf_url, quote=True)
        esc_map = html.escape(map_url, quote=True)
        esc_lbl = html.escape(label, quote=True)
        lis.append(
            f'    <li>\n'
            f'      <a href="{esc_pdf}" target="_blank" rel="noreferrer noopener">{esc_addr}</a>\n'
            f'      <span class="map-sep">·</span>\n'
            f'      <a href="{esc_map}" target="_blank" rel="noreferrer noopener">[View Map]</a>\n'
            f'      <span class="fc-doc" title="Notice PDF">{esc_lbl}</span>\n'
            f'    </li>'
        )

    body_list = "\n".join(lis)
    count = len(items)

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="referrer" content="no-referrer">
  <title>Bell County Foreclosures — Cloud Fronts LLC</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
<header>
  <div class="inner">
    <h1>HUD Funding &amp; Partnerships <span>— Cloud Fronts LLC</span></h1>
    <nav>
      <a href="index.html">Home</a>
      <a href="cloud-fronts-summary.html">Cloud Fronts</a>
      <a href="dscr.html">DSCR Lenders</a>
      <a href="foreclosures.html" class="active">Foreclosures</a>
      <a href="links.html">All Links</a>
    </nav>
  </div>
</header>
<div class="container">

  <div class="callout callout-warn">
    <strong>Non-HUD reference.</strong> These addresses were parsed from Bell County weekly foreclosure-notice PDFs (OCR). Each row links to the <strong>exact PDF</strong> that contained that notice. Verify on the official document before relying on any line.
  </div>

  <p class="foreclosure-meta">
    County index:
    <a href="https://www.bellcountytx.com/county_government/county_clerk/foreclosures.php" target="_blank" rel="noreferrer noopener">Bell County Clerk &mdash; foreclosure notices</a>.
    Data file: <code>data/bell_foreclosure_ocr/results.json</code> &mdash; regenerate this page with <code>python3 scripts/build_foreclosures_page.py</code>.
  </p>

  <h2>Bell County Foreclosures</h2>
  <p><strong>{count}</strong> properties. The address opens the source PDF in a new tab; <strong>[View Map]</strong> opens Google Maps for the same string. Both use <code>target=&quot;_blank&quot;</code> and <code>rel=&quot;noreferrer noopener&quot;</code> (no referrer, no <code>window.opener</code>).</p>

  <ul class="foreclosure-list">
{body_list}
  </ul>

</div>
<footer>
  Compiled for Cloud Fronts LLC &middot; <a href="index.html">Home</a>
</footer>
</body>
</html>
"""
    OUT_HTML.write_text(page, encoding="utf-8")
    print(f"Wrote {OUT_HTML} ({count} addresses)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

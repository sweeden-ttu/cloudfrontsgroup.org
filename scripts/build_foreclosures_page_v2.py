#!/usr/bin/env python3
"""Rebuild foreclosures.html with enhanced entity-level data from OCR parsing."""
from __future__ import annotations

import html
import json
from pathlib import Path
from urllib.parse import quote_plus

BASE_DIR = Path(__file__).resolve().parent.parent
JSON_PATH = BASE_DIR / "data" / "bell_foreclosure_ocr" / "results_enhanced.json"
OUT_HTML = BASE_DIR / "foreclosures.html"


def entity_tag(name: str, cls: str = "tag") -> str:
    return f'<span class="{cls}">{html.escape(name)}</span>'


def main() -> int:
    data = json.loads(JSON_PATH.read_text("utf-8"))

    # Collect unique entities across all notices
    all_servicers: set[str] = set()
    all_trustees: set[str] = set()
    all_noteholders: set[str] = set()
    all_individuals: set[str] = set()

    items: list[tuple[str, str, str, str, str, str, str]] = []
    for block in data:
        pdf_url = block.get("url") or ""
        label = f'{block.get("month")} {block.get("day")}'
        entities = block.get("entities", {})

        for s in entities.get("servicers", []):
            all_servicers.add(s)
        for t in entities.get("trustees", []):
            all_trustees.add(t)
        for n in entities.get("noteholders", []):
            all_noteholders.add(n)
        for i in entities.get("substitute_trustee_individuals", []):
            all_individuals.add(i)

        for addr in block.get("addresses") or []:
            a = (addr or "").strip()
            if not a:
                continue
            map_q = quote_plus(a.rstrip("."))
            map_url = f"https://maps.google.com/?q={map_q}"

            servicers_str = ", ".join(entities.get("servicers", [])) if entities.get("servicers") else ""
            trustees_str = ", ".join(entities.get("trustees", [])) if entities.get("trustees") else ""

            items.append((a, pdf_url, map_url, label, servicers_str, trustees_str, block.get("month", "")))

    # Build entity summary panels
    servicer_summary = ""
    if all_servicers:
        tags = "\n          ".join(entity_tag(s) for s in sorted(all_servicers))
        servicer_summary = f"""  <div class="callout">
    <h3 style="margin-top:0;">Mortgage Servicers Detected ({len(all_servicers)})</h3>
    <p style="font-size:0.9rem;color:var(--hud-gray);margin-bottom:0.75rem;">
      These companies are listed as the mortgage servicer or debt collector in the foreclosure notices.
    </p>
    <div class="entity-tags">
          {tags}
    </div>
  </div>"""

    trustee_summary = ""
    if all_trustees:
        tags = "\n          ".join(entity_tag(s, "tag tag-security") for s in sorted(all_trustees))
        trustee_summary = f"""  <div class="callout callout-ml">
    <h3 style="margin-top:0;">Substitute Trustees / Law Firms ({len(all_trustees)})</h3>
    <p style="font-size:0.9rem;color:var(--hud-gray);margin-bottom:0.75rem;">
      These law firms and trustee companies are appointed to conduct the foreclosure sales.
    </p>
    <div class="entity-tags">
          {tags}
    </div>
  </div>"""

    noteholder_summary = ""
    if all_noteholders:
        tags = "\n          ".join(entity_tag(s, "tag tag-guardrail") for s in sorted(all_noteholders))
        noteholder_summary = f"""  <div class="callout callout-teal">
    <h3 style="margin-top:0;">Noteholders / Mortgagees ({len(all_noteholders)})</h3>
    <p style="font-size:0.9rem;color:var(--hud-gray);margin-bottom:0.75rem;">
      The current holder of the promissory note and deed of trust.
    </p>
    <div class="entity-tags">
          {tags}
    </div>
  </div>"""

    lis = []
    for addr, pdf_url, map_url, label, servicers, trustees, month in items:
        esc_addr = html.escape(addr, quote=False)
        esc_pdf = html.escape(pdf_url, quote=True)
        esc_map = html.escape(map_url, quote=True)
        esc_lbl = html.escape(label, quote=True)

        info_parts = []
        if servicers:
            info_parts.append(f'<span class="fc-entity">Servicer: {html.escape(servicers)}</span>')
        if trustees:
            info_parts.append(f'<span class="fc-entity fc-trustee">Trustee: {html.escape(trustees)}</span>')

        info_html = "<br>".join(info_parts)

        lis.append(
            f'    <li>'
            f'<a href="{esc_pdf}" target="_blank" rel="noreferrer noopener">{esc_addr}</a>'
            f' <span class="map-sep">·</span>'
            f' <a href="{esc_map}" target="_blank" rel="noreferrer noopener">[Map]</a>'
            f' <span class="fc-doc" title="Notice PDF">{esc_lbl}</span>'
            f'{info_html}'
            f'</li>'
        )

    body_list = "\n".join(lis)
    count = len(items)

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="theme-color" content="#003a70">
  <link rel="icon" type="image/svg+xml" href="favicon.svg">
  <title>Foreclosure Data — Bell County, Central Texas | Cloud Fronts Group</title>
  <meta name="description" content="Bell County foreclosure notices with mortgage servicer, substitute trustee, and noteholder information. OCR-parsed from weekly county posting PDFs.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@400;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="style.css">
  <link rel="canonical" href="https://cloudfrontsgroup.org/foreclosures.html">
</head>
<body>
<a href="#main-content" class="skip-link">Skip to main content</a>

<header>
  <div class="inner">
    <h1>&#9729; Cloud Fronts <span>Group</span></h1>
    <button class="menu-toggle" aria-label="Toggle navigation menu">&#9776;</button>
    <button id="theme-toggle" class="theme-toggle" aria-label="Switch to dark mode">&#9790;</button>
    <nav aria-label="Main navigation">
      <a href="index.html">Home</a>
      <a href="cloud-fronts-summary.html">About</a>
      <a href="research-grant.html">AAAI Research</a>
      <a href="hud-analytics.html">HUD Analytics</a> | <a href="hud-grant-proposal.html">HUD Grant Proposal</a>
      <a href="section3.html">Compliance</a>
      <a href="foreclosures.html" class="active" aria-current="page">Community Data</a>
      <a href="volunteer-corps.html">Volunteer</a>
      <a href="usda-farming.html">USDA Farming</a>
      <a href="links.html">Links</a>
    </nav>
  </div>
</header>

<nav aria-label="Breadcrumb"><ol class="breadcrumb"><li><a href="index.html">Home</a></li><li aria-current="page">Foreclosure Data</li></ol></nav>

<div class="container" id="main-content">

  <h2>Bell County Foreclosure Notices</h2>
  <p class="subtitle">OCR-parsed foreclosure postings from Bell County Clerk — with mortgage servicer, trustee, and noteholder entities identified</p>

  <div class="callout callout-warn">
    <strong>Non-HUD reference.</strong> These addresses were parsed from Bell County weekly foreclosure-notice PDFs via OCR. Each row links to the exact PDF that contained that notice. Entity names (servicer, trustee) are extracted from the OCR text — verify on the official document before relying on any data. This is not legal advice.
  </div>

  <p style="margin-bottom:1.5rem;">
    Source: <a href="https://www.bellcountytx.com/county_government/county_clerk/foreclosures.php" target="_blank" rel="noreferrer noopener">Bell County Clerk — Foreclosure Notices</a>.
    Data regenerated with <code>python3 scripts/parse_foreclosure_entities.py && python3 scripts/build_foreclosures_page_v2.py</code>.
  </p>

  <h3>Summary: {count} Properties Listed</h3>

  {servicer_summary}

  {trustee_summary}

  {noteholder_summary}

  <h2>Foreclosure Property List</h2>
  <p><strong>{count}</strong> properties. Address links open the source PDF; <strong>[Map]</strong> opens Google Maps. Entity info (servicer / trustee) shown below each address when available.</p>

  <ul class="foreclosure-list">
{body_list}
  </ul>

  <h2>How Texas Foreclosure Notices Work</h2>
  <div class="card-grid">
    <div class="card">
      <h3>Notice of Sale</h3>
      <p>Filed with the county clerk at least 21 days before sale. Posted at the courthouse. Contains property address, legal description, sale date/time, and the substitute trustee information.</p>
    </div>
    <div class="card">
      <h3>Notice of Default</h3>
      <p>Before a foreclosure sale can occur, the borrower must be in default. Texas is a non-judicial foreclosure state — most foreclosures proceed under a power of sale clause in the deed of trust, without court supervision, unless the borrower files a lawsuit.</p>
    </div>
    <div class="card">
      <h3>Foreclosure Sale</h3>
      <p>Held on the first Tuesday of each month between 10 AM and 4 PM at the Bell County Justice Complex, 1201 Huey Drive, Belton, TX. Conducted by the substitute trustee as a public auction to the highest bidder for cash.</p>
    </div>
    <div class="card">
      <h3>Other Counties</h3>
      <p>Each Central Texas county publishes its own foreclosure notice list. See our <a href="county-foreclosure-resources.html">County Foreclosure Resources</a> page for Coryell, McLennan, Williamson, Burnet, Milam, and Lampasas counties.</p>
    </div>
  </div>

  <h2>Related Resources</h2>
  <ul class="link-list">
    <li><a href="https://www.bellcountytx.com/county_government/county_clerk/foreclosures.php" target="_blank" rel="noopener">Bell County Clerk — Foreclosure Notices</a><span class="desc">Official source for all Bell County foreclosure posting PDFs</span></li>
    <li><a href="https://txcourts.gov" target="_blank" rel="noopener">Texas Office of Court Administration</a><span class="desc">Texas Property Code 51.002 — foreclosure sale procedures</span></li>
    <li><a href="https://statutes.capitol.texas.gov/Docs/PR/htm/PR.51.htm" target="_blank" rel="noopener">Texas Property Code Chapter 51</a><span class="desc">Legal framework for real property foreclosure in Texas</span></li>
    <li><a href="links.html#hud-data" class="btn btn-outline">HUD Data Sources</a></li>
  </ul>

</div>

<footer>
  <p>Cloud Fronts Group &mdash; Central Texas Technology Access &amp; Innovation Delivery Partnership</p>
  <p><a href="index.html">Home</a> | <a href="cloud-fronts-summary.html">About</a> | <a href="research-grant.html">Research</a> | <a href="hud-analytics.html">HUD Analytics</a> | <a href="hud-grant-proposal.html">HUD Grant Proposal</a> | <a href="section3.html">Compliance</a> | <a href="foreclosures.html">Community Data</a> | <a href="volunteer-corps.html">Volunteer</a> | <a href="usda-farming.html">USDA Farming</a> | <a href="links.html">Links</a> | <a href="rental-assistance.html">Rent Help</a> | <a href="sitemap.xml">Sitemap</a> | <a href="blog/">Blog</a> | <a href="contact.html">Contact</a></p>
  <p style="margin-top:.5rem;font-size:.72rem;">Scott Weeden: <a href="#" class="eml" data-eml="scottweeden" data-dom="cloudfrontsgroup.org">click to reveal</a> &middot; Johnathan King: <a href="#" class="eml" data-eml="johnathanking" data-dom="cloudfrontsgroup.org">click to reveal</a> &middot; Phone: 254-317-6688</p>
  <p class="last-updated">Last updated: June 2026</p>
  <button id="print-btn" class="print-btn">&#9015; Print</button>
  <p style="font-size:.72rem;">&copy; 2026 Cloud Fronts Group. All rights reserved.</p>
</footer>

<script src="site.js" defer></script>
</body>
</html>
"""
    OUT_HTML.write_text(page, "utf-8")
    print(f"Wrote {OUT_HTML} ({count} addresses)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""
Build script for cloudfrontsgroup.org.
Assembles pages from partials + content files.

Usage:
  python3 _build/build.py             # builds all pages
  python3 _build/build.py index.html  # builds a single page
"""

import os
import re
import sys
import json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARTIALS = os.path.join(ROOT, '_partials')
PAGES = os.path.join(ROOT, '_pages')

# ─── Page metadata ───────────────────────────────────────────

PAGE_META = {
    "index": {
        "title": "Cloud Fronts Group — Growing Your Business Online",
        "description": "Cloud Fronts Group helps Central Texas businesses grow with professional web design, logo design, marketing, and digital services.",
        "section": "",
        "active": "home",
        "canonical": "https://cloudfrontsgroup.org/",
        "schema_desc": "Central Texas digital services — web design, logo design, marketing, and online business solutions.",
    },
    "about-us": {
        "title": "Cloud Fronts Group — About Us | Central Texas Digital Services",
        "description": "Cloud Fronts Group is a Central Texas digital services company offering web design, logo design, domain registration, hosting, marketing, PPC, social media, printing, and document management — no long-term contracts required.",
        "section": "",
        "active": "about-us",
    },
    "contact": {
        "title": "Cloud Fronts Group — Contact Us | Central Texas Digital Services",
        "description": "Contact Cloud Fronts Group for web design, logo design, domain registration, hosting, marketing, printing, and digital services in Central Texas.",
        "section": "",
        "active": "contact",
        "schema_desc": "Central Texas digital services — web design, logo design, marketing, and online business solutions.",
    },
    "team": {
        "title": "Team — Cloud Fronts Group",
        "description": "Meet the Cloud Fronts Group team — Scott Weeden, Johnathan King, and research partners.",
        "section": "",
        "active": "",
    },
    "domain-names": {
        "title": "Cloud Fronts Group — Domain Names | Central Texas Digital Services",
        "description": "Domain name registration, transfer, and management services from Cloud Fronts Group.",
        "section": "",
        "active": "",
    },
    "promotional-items": {
        "title": "Cloud Fronts Group — Promotional Items | Central Texas Digital Services",
        "description": "Custom promotional products and branded merchandise for Central Texas businesses.",
        "section": "",
        "active": "",
    },
    "site-hosting": {
        "title": "Cloud Fronts Group — Site Hosting | Central Texas Digital Services",
        "description": "Reliable web hosting services for Central Texas businesses.",
        "section": "",
        "active": "",
    },
    "marketing": {
        "title": "Cloud Fronts Group — Marketing | Central Texas Digital Services",
        "description": "Full-service marketing for Central Texas businesses — strategic campaigns, market research, brand strategy.",
        "section": "",
        "active": "",
    },
    "political-advertisements": {
        "title": "Cloud Fronts Group — Political Advertisements | Central Texas Digital Services",
        "description": "Political advertisement design and placement services for Central Texas campaigns.",
        "section": "",
        "active": "",
    },
    "logo-design": {
        "title": "Cloud Fronts Group — Logo Design | Central Texas Digital Services",
        "description": "Custom logo design for Central Texas businesses — discovery, concepting, refinement, delivery.",
        "section": "",
        "active": "",
    },
    "web-design-hosting": {
        "title": "Cloud Fronts Group — Web Design & Hosting | Central Texas Digital Services",
        "description": "Professional web design and hosting services for Central Texas businesses.",
        "section": "",
        "active": "",
    },
    "design-print-agency": {
        "title": "Cloud Fronts Group — Design & Print Agency | Central Texas Digital Services",
        "description": "Full-service design and print agency serving Central Texas businesses.",
        "section": "",
        "active": "",
    },
    "pay-per-click-marketing": {
        "title": "Cloud Fronts Group — Pay Per Click Marketing | Central Texas Digital Services",
        "description": "Targeted PPC marketing campaigns for Central Texas businesses.",
        "section": "",
        "active": "",
    },
    "social-media-marketing": {
        "title": "Cloud Fronts Group — Social Media Marketing | Central Texas Digital Services",
        "description": "Social media marketing and content strategy for Central Texas businesses.",
        "section": "",
        "active": "",
    },
    "document-management": {
        "title": "Cloud Fronts Group — Document Management | Central Texas Digital Services",
        "description": "Document management and workflow solutions for Central Texas businesses.",
        "section": "",
        "active": "",
    },
    "online-publishing": {
        "title": "Cloud Fronts Group — Online Publishing | Central Texas Digital Services",
        "description": "Establish thought leadership with online publishing services including eBooks, whitepapers, newsletters.",
        "section": "",
        "active": "",
    },
    "404": {
        "title": "Page Not Found — Cloud Fronts Group",
        "description": "The page you were looking for could not be found.",
        "section": "",
        "active": "",
    },
}

SCHEMA_DEFAULT = """Central Texas digital services and community research — web design, logo design, marketing, AI/ML research, and community technology programs."""

NAV_PAGES = {
    "home": "index.html",
    "about-us": "about-us.html",
    "contact": "contact.html",
}

def load_partial(name):
    path = os.path.join(PARTIALS, f'_{name}.html')
    with open(path, 'r') as f:
        return f.read()

def build_og_tags(canonical, title, description):
    return f''' <meta property="og:title" content="{title}">
 <meta property="og:description" content="{description}">
 <meta property="og:type" content="website">
 <meta property="og:url" content="{canonical}">
 <meta property="og:image" content="https://cloudfrontsgroup.org/favicon.svg">
 <meta property="og:site_name" content="Cloud Fronts Group">
 <meta name="twitter:card" content="summary_large_image">
 <meta name="twitter:title" content="{title}">
 <meta name="twitter:description" content="{description}">'''

def build_schema(schema_desc):
    return f''' <script type="application/ld+json">
 {{
 "@context": "https://schema.org",
 "@type": "Organization",
 "name": "Cloud Fronts Group",
 "url": "https://cloudfrontsgroup.org",
 "description": "{schema_desc}",
 "email": ["scottweeden@cloudfrontsgroup.org", "johnathanking@cloudfrontsgroup.org"],
 "telephone": "+1-254-317-6688",
 "areaServed": "Central Texas",
 "foundingDate": "2026"
 }}
 </script>'''

def build_page(page_name):
    meta = PAGE_META.get(page_name, {})
    if not meta:
        print(f"  ⚠ No metadata for '{page_name}', skipping")
        return

    title = meta.get("title", "Cloud Fronts Group")
    description = meta.get("description", "Cloud Fronts Group — Central Texas digital services.")
    subdir = meta.get("subdir", "")
    root_prefix = "../" if subdir else ""

    if "canonical" in meta:
        canonical = meta["canonical"]
    elif subdir:
        canonical = f"https://cloudfrontsgroup.org/{subdir}/{os.path.basename(page_name)}.html"
    else:
        canonical = f"https://cloudfrontsgroup.org/{page_name}.html"

    section = meta.get("section", "")
    schema_desc = meta.get("schema_desc", SCHEMA_DEFAULT)
    active = meta.get("active", "")

    # Build active nav attributes
    home_active = ' class="active" aria-current="page"' if active == "home" else ""
    contact_active = ' class="active" aria-current="page"' if active == "contact" else ""
    body_attrs = f' data-section="{section}"' if section else ""

    replacements = {
        "{{TITLE}}": title,
        "{{DESCRIPTION}}": description,
        "{{CANONICAL}}": f' <link rel="canonical" href="{canonical}">',
        "{{OG_TAGS}}": build_og_tags(canonical, title, description),
        "{{SCHEMA}}": build_schema(schema_desc),
        "{{BODY_ATTRS}}": body_attrs,
        "{{HOME_ACTIVE}}": home_active,
        "{{CONTACT_ACTIVE}}": contact_active,
        "{{ROOT_PREFIX}}": root_prefix,
    }

    # Build path to page content — check subdirectory first
    if subdir:
        content_path = os.path.join(PAGES, subdir, os.path.basename(page_name) + ".html")
    else:
        content_path = os.path.join(PAGES, f"{page_name}.html")
    if not os.path.exists(content_path):
        print(f"  ⚠ No content file for '{page_name}' at {content_path}")
        return

    with open(content_path, 'r') as f:
        content = f.read()

    head = load_partial("head")
    header = load_partial("header")
    footer = load_partial("footer")

    # Apply replacements (mutate each partial)
    for key, val in replacements.items():
        head = head.replace(key, val)
        header = header.replace(key, val)
        footer = footer.replace(key, val)

    # Assemble
    output = head + "\n" + header + "\n" + content + "\n" + footer

    # Write to subdirectory if applicable
    if subdir:
        out_dir = os.path.join(ROOT, subdir)
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, os.path.basename(page_name) + ".html")
    else:
        out_path = os.path.join(ROOT, f"{page_name}.html")
    with open(out_path, 'w') as f:
        f.write(output)

    print(f"  ✓ {page_name}.html")

def main():
    # Build all pages or single page
    if len(sys.argv) > 1:
        targets = [os.path.splitext(sys.argv[1])[0]]
    else:
        targets = list(PAGE_META.keys())

    print(f"Building {len(targets)} page(s)...")
    for t in targets:
        build_page(t)
    print("Done.")

if __name__ == "__main__":
    main()

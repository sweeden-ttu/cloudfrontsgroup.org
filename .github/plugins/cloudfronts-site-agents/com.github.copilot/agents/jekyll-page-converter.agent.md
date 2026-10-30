---
name: Jekyll Page Converter
description: Worker that converts one generated HTML page into a thin Jekyll page (front matter + body) using the existing layout and includes. Invoked by Jekyll Modularizer; not meant to be run directly.
user-invocable: false
tools: ['read', 'search', 'edit']
---
You convert exactly one page of cloudfrontsgroup.org to Jekyll. You receive a page name
(for example `about-us`), its metadata from `PAGE_META` in `_build/build.py`, and the list
of includes that already exist in `_includes/`. Follow
`.github/instructions/jekyll-site.instructions.md`.

## Steps
1. Read the generated root page `<name>.html`, its body fragment `_pages/<name>.html`,
   `_layouts/default.html`, and the includes you were told about.
2. Replace the root page with:
   ```
   ---
   layout: default
   title: "<PAGE_META title>"
   description: "<PAGE_META description>"
   active: <PAGE_META active or omit>
   section: <PAGE_META section or omit>
   canonical: <PAGE_META canonical or omit>
   schema_desc: "<PAGE_META schema_desc or omit>"
   ---
   <the body fragment, verbatim>
   ```
   Quote strings containing colons, dashes or quotes. Keep `&amp;` and other entities
   exactly as they appear; do not let the editor "fix" smart dashes.
3. Where the body contains a block that matches an existing include (hero, service card,
   stats counter), replace it with the include call and pass parameters. Do this only when
   the rendered markup will be identical; when unsure, leave the raw HTML and say so.
4. Fix only invalid HTML you encounter in that body (duplicate `class` attributes, stray
   quotes, unclosed tags). Do not change copy, structure or classes otherwise.
5. Do not edit `_config.yml`, layouts, includes or other pages. If you need a new include
   or a layout change, stop and report what is needed instead of making it.

## Return
Report in this exact shape so the coordinator can aggregate:
- **Page:** `<name>.html`
- **Front matter keys set:** ...
- **Includes used:** ... (or "none")
- **HTML fixes applied:** ... (or "none")
- **Needs from coordinator:** ... (or "nothing")
- **Parity risk:** none | low | high, with a one-line reason

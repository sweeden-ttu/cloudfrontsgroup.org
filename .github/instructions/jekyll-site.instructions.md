---
applyTo: "**/*.html,**/*.md,**/*.yml,**/*.scss,**/*.css"
description: Conventions for the cloudfrontsgroup.org Jekyll migration and site maintenance
---
# cloudfrontsgroup.org — site conventions

## What this site is today
- Static HTML, CSS, JS. Published by GitHub Pages as raw files (`.nojekyll` is present).
- Every root page (`index.html`, `about-us.html`, ...) is **generated** by `python3 _build/build.py`
  from three partials in `_partials/` (`_head.html`, `_header.html`, `_footer.html`) plus a
  body fragment in `_pages/<name>.html`. Per-page metadata lives in the `PAGE_META` dict in
  `_build/build.py`.
- The partials use `{{PLACEHOLDER}}` tokens that `build.py` string-replaces:
  `{{TITLE}}`, `{{DESCRIPTION}}`, `{{CANONICAL}}`, `{{OG_TAGS}}`, `{{SCHEMA}}`,
  `{{BODY_ATTRS}}`, `{{HOME_ACTIVE}}`, `{{CONTACT_ACTIVE}}`, `{{ROOT_PREFIX}}`.
- Jekyll (`Gemfile`, `_config.yml`, `.ruby-version`, `.vscode/tasks.json`) is wired up for
  **local preview only**. `bundle exec jekyll serve` on http://127.0.0.1:4000.

## Target Jekyll structure (what "modularized" means here)
```
_config.yml              site-wide values: title, phone, emails, nav, defaults
_data/nav.yml            navigation menus (Home, About, Products, Services, Contact)
_data/services.yml       service cards shown on the home page
_layouts/default.html    <html> shell: includes head, header, {{ content }}, footer
_includes/head.html      <head> — title, meta, canonical, OG tags, JSON-LD
_includes/header.html    skip link, <header>, nav built from site.data.nav
_includes/footer.html    footer, back-to-top, scripts
_includes/hero.html      reusable hero block (title, sub, CTAs as include params)
_includes/service-card.html
*.html (root)            thin pages: front matter + body only
```

## Rules the agents must follow
1. **Output parity is the acceptance test.** The HTML Jekyll emits into `_site/` must match
   the committed root HTML byte-for-byte after whitespace normalization, for every page.
   Compare with `diff <(tidy-ish normalize _site/x.html) <(normalize x.html)` or the
   `scripts/compare_build.py` helper if it exists.
2. Map each `{{PLACEHOLDER}}` to Liquid, do not invent new behavior:
   - `{{TITLE}}` -> `{{ page.title }}`; `{{DESCRIPTION}}` -> `{{ page.description }}`
   - `{{CANONICAL}}` -> `{{ page.canonical | default: page.url | absolute_url }}`
   - `{{SCHEMA}}` -> `{{ page.schema_desc | default: site.schema_default }}`
   - `{{BODY_ATTRS}}` -> `{% if page.section %} data-section="{{ page.section }}"{% endif %}`
   - `{{HOME_ACTIVE}}` / `{{CONTACT_ACTIVE}}` -> compare `page.active` to the nav item key
   - `{{ROOT_PREFIX}}` -> `{{ '/' | relative_url }}` or keep root-relative links; all pages
     are at the root today so the prefix is always empty.
3. Front matter on root pages is the **only** place page metadata lives after migration.
   Carry over every `PAGE_META` field: `title`, `description`, `section`, `active`,
   `canonical`, `schema_desc`. Set `layout: default`.
4. Keep `permalink` so URLs stay `/<name>.html` (set `permalink: /:basename:output_ext` via
   `defaults` in `_config.yml`; do not switch to pretty URLs during the migration).
5. Do not add anything that needs a backend, API key, database or analytics provider.
   This is a hard rule from `_build/build.py`; see the maintainer note there.
6. Do not delete `_build/`, `_pages/`, `_partials/` until the Reviewer has signed off on
   parity for all 17 pages. Then remove them and `gen_images.py` references in one commit.
7. Keep `.nojekyll`. Removing it would make GitHub Pages run Jekyll in production, which
   needs a separate decision from the owner.
8. HTML hygiene: one `class` attribute per element, valid nesting, `alt` on every `<img>`,
   `aria-label` on icon-only buttons, Lucide icons via `data-lucide`.
9. Styles stay in `style.css`; `style.min.css` is a build artifact. If you change `style.css`
   regenerate the min file the same way the repo already does (see git history), or flag it.

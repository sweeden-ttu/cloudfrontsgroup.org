# Writing a blog post

The site is a Jekyll site. Posts are Markdown files in `_posts/` and publish at `https://cloudfrontsgroup.org/blog/<slug>.html`. The blog index is `blog.html`, the feed is `feed.xml`, and the sitemap is generated automatically.

## 1. Create the file

Name it `YYYY-MM-DD-slug.md`. The date sets the publish order; the slug becomes the URL.

```
_posts/2026-11-04-five-checks-before-you-renew-your-domain.md
```

## 2. Fill in the front matter

```yaml
---
title: "Five checks before you renew your domain"
description: "A 160-character summary used for search results and link previews."
image: images/your-image.png          # 1200×630 (1.91:1) works best for Facebook, X, LinkedIn
image_alt: "What the image shows"
tags: [domains, checklists]
social_text: "The exact sentence to post on X / in the email share. Keep it under 200 characters."
---
```

| Field | Required | Used for |
|-------|----------|----------|
| `title` | yes | Page title, `<h2>`, `og:title`, feed |
| `description` | recommended | `<meta name="description">`, link previews, blog index teaser. Falls back to the excerpt. |
| `image` | recommended | Hero image on the post, `og:image` / `twitter:image`, card on the blog index. Path relative to the site root, no leading slash. |
| `image_alt` | with image | Alt text. Falls back to the title. |
| `image_caption` | no | Caption under the hero image |
| `tags` | no | Shown as pills, emitted as `article:tag` |
| `social_text` | recommended | Pre-filled text for the X and email share buttons. Falls back to the title. |
| `author` | no | Defaults to "Cloud Fronts Group" |
| `last_modified_at` | no | `dateModified` in structured data |

`layout`, `permalink`, and `root_prefix` are set for all posts in `_config.yml`; do not set them per post.

## 3. Write the body

Standard Markdown (kramdown, GitHub-flavored). Put `<!--more-->` after the first paragraph to control the excerpt shown on the index and in the feed. Links back to the site from a post need `../` because posts live under `/blog/`, for example `[contact us](../contact.html)` or `![alt](../images/x.png)`.

Keep claims to things the business actually does. No testimonials, client logos, or statistics that aren't sourced.

## 4. Preview

```bash
export PATH="$HOME/.rbenv/shims:$PATH"
bundle exec jekyll serve --livereload      # or the "jekyll: serve" VS Code task
open http://127.0.0.1:4000/blog.html
```

Check the post page, the blog index card, and `http://127.0.0.1:4000/feed.xml`.

## 5. Publish and share

Commit and push to `master`. GitHub Pages rebuilds the site with Jekyll within a minute or two.

Sharing options, in increasing order of automation:

- **Share buttons** at the bottom of every post open pre-filled X, Facebook, LinkedIn, and email shares. No scripts or trackers are loaded.
- **Paste the link.** Facebook, X, and LinkedIn read the post's Open Graph tags, so the preview shows the `image`, `title`, and `description`.
- **RSS to social.** Point Buffer, Zapier, IFTTT, or dlvr.it at `https://cloudfrontsgroup.org/feed.xml`. The feed carries the full post content and the hero image.
- **Distribution kit.** The `social-media-distributor` agent in `.github/plugins/cloudfronts-site-agents/` turns a post into platform-native copy, hashtags, and a posting schedule.

## Styling

Blog styles live at the end of `style.css` under the "Blog" banner and use the same tokens as the rest of the site (`--brand-blue`, `--color-surface`, `--radius`, `--font-head`). After editing `style.css`, run:

```bash
python3 scripts/minify_css.py
```

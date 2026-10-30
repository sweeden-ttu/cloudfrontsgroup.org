#!/usr/bin/env python3
"""
Wire the hand-authored SVG illustrations (images/*.svg) into the pages.

    python3 scripts/wire_svg_media.py            # apply
    python3 scripts/wire_svg_media.py --dry-run  # report only

What it does, driven by imagespecs/media-prompts.yml:
  1. Replaces every `<!-- media slot ID: ... -->` comment with an <img> for the SVG.
  2. Repoints any remaining <img src="images/<slot>.(webp|png|avif|jpg)"> to the SVG.
  3. Rasterizes og-default.svg and blog-default.svg to 1200x630 PNG (social cards
     need bitmaps) and points _config.yml `og_default` and the first post at them.
  4. Deletes raster files that the SVGs supersede.
Only slots whose SVG exists are touched, so it is safe to run while some are pending.
"""
import os
import re
import subprocess
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPEC = os.path.join(ROOT, "imagespecs", "media-prompts.yml")
DRY = "--dry-run" in sys.argv

RASTER_EXT = (".webp", ".png", ".avif", ".jpg", ".jpeg")


def svg_path(slot):
    base, _ = os.path.splitext(slot["file"])
    return base + ".svg"


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def write(p, s):
    if DRY:
        return
    with open(p, "w", encoding="utf-8") as f:
        f.write(s)


def main():
    spec = yaml.safe_load(read(SPEC))
    done, pending, removed = [], [], []
    for slot in spec["slots"]:
        sid = slot["id"]
        if sid == "H1":
            continue
        svg_rel = svg_path(slot)
        svg_abs = os.path.join(ROOT, svg_rel)
        if not os.path.exists(svg_abs):
            pending.append(sid)
            continue
        w, h = slot["size"]
        css = slot["css"].split()[0].lstrip(".") if slot["css"].startswith(".") else "featured-image"
        if css not in ("featured-image", "img-service-bot", "img-service-center"):
            css = "featured-image"
        alt = slot["alt"].replace('"', "&quot;")
        img = f'<img src="{svg_rel}" alt="{alt}" class="{css}" width="{w}" height="{h}">'
        base_noext = os.path.splitext(os.path.basename(slot["file"]))[0]

        page = os.path.join(ROOT, slot["page"])
        if os.path.exists(page) and sid not in ("H2", "B1"):
            s = read(page)
            s2 = re.sub(r"(?m)^([ \t]*)<!-- media slot %s:[^>]*-->\n?" % re.escape(sid), lambda m: f"{m.group(1)}{img}\n", s)
            s2 = re.sub(r'<img[^>]*src="images/%s(?:%s)"[^>]*>' % (re.escape(base_noext), "|".join(re.escape(e) for e in RASTER_EXT)),
                        img, s2)
            if s2 != s:
                write(page, s2)
        # superseded rasters
        for ext in RASTER_EXT:
            raster = os.path.join(ROOT, "images", base_noext + ext)
            if os.path.exists(raster) and sid not in ("H2", "B1"):
                removed.append(os.path.relpath(raster, ROOT))
                if not DRY:
                    os.remove(raster)
        done.append(sid)

    # Social cards: rasterize for og:image
    for sid, name in (("H2", "og-default"), ("B1", "blog-default")):
        svg = os.path.join(ROOT, "images", name + ".svg")
        if not os.path.exists(svg):
            continue
        png = os.path.join(ROOT, "images", name + ".png")
        if not DRY:
            subprocess.run(["rsvg-convert", "-w", "1200", "-h", "630", svg, "-o", png], check=True)
            webp = os.path.join(ROOT, "images", name + ".webp")
            if os.path.exists(webp):
                os.remove(webp)
        print(f"rasterized {name}.svg -> images/{name}.png")

    cfg = os.path.join(ROOT, "_config.yml")
    s = read(cfg)
    if os.path.exists(os.path.join(ROOT, "images", "og-default.svg")):
        s2 = re.sub(r"(?m)^og_default: .*$", "og_default: images/og-default.png", s)
        if s2 != s:
            write(cfg, s2)
            print("config og_default -> images/og-default.png")

    print(f"wired: {', '.join(done) or 'none'}")
    print(f"pending (no svg yet): {', '.join(pending) or 'none'}")
    print(f"removed rasters: {len(removed)}")
    for r in removed:
        print("  -", r)
    if DRY:
        print("(dry run, nothing written)")


if __name__ == "__main__":
    main()

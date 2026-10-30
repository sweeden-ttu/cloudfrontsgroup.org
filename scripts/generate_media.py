#!/usr/bin/env python3
"""
Generate site illustrations from imagespecs/media-prompts.yml.

Providers: `openai` (gpt-image-1, default) or `gemini` (Gemini image models; needs a
billing-enabled project, the free tier has zero image quota).

    python3 scripts/generate_media.py                 # all slots
    python3 scripts/generate_media.py --only D1 SM1   # selected slot ids
    python3 scripts/generate_media.py --dry-run       # print prompts, no API calls
    python3 scripts/generate_media.py --model gemini-3-pro-image   # higher quality, slower

Needs GEMINI_API_KEY in the environment and the `google-genai`, `pyyaml`, `Pillow`
packages. For each slot it writes a PNG master and a WebP at the slot's size into
the path given by `file` (the sibling extension is written too, so pages can use
either). Imagen only offers a few aspect ratios, so the image is generated at the
nearest wider ratio and center-cropped to the slot's aspect. Logos are not
generated here; they are hand-authored SVGs in images/logo/.
"""
import argparse
import io
import os
import sys
import time

import yaml
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPEC = os.path.join(ROOT, "imagespecs", "media-prompts.yml")

# Aspect ratios the Gemini image models accept, as width/height.
IMAGEN_RATIOS = {"1:1": 1.0, "5:4": 5 / 4, "4:3": 4 / 3, "3:2": 3 / 2, "16:9": 16 / 9, "21:9": 21 / 9}


def pick_ratio(target):
    """Smallest Imagen ratio that is at least as wide as the target, so we crop height only."""
    wider = [(v, k) for k, v in IMAGEN_RATIOS.items() if v >= target - 1e-6]
    return min(wider)[1] if wider else "21:9"


def openai_size(target_ratio):
    if target_ratio >= 1.2:
        return "1536x1024"
    if target_ratio <= 0.83:
        return "1024x1536"
    return "1024x1024"


def center_crop(im, target_ratio):
    w, h = im.size
    cur = w / h
    if abs(cur - target_ratio) < 1e-3:
        return im
    if cur > target_ratio:  # too wide: crop width
        nw = int(round(h * target_ratio))
        x0 = (w - nw) // 2
        return im.crop((x0, 0, x0 + nw, h))
    nh = int(round(w / target_ratio))  # too tall: crop height
    y0 = (h - nh) // 2
    return im.crop((0, y0, w, y0 + nh))


def save_outputs(im, rel_file, size):
    target_w, target_h = size
    if im.size != (target_w, target_h):
        # Never upscale by more than 2x; downscale freely.
        scale = min(target_w / im.size[0], 2.0)
        new_size = (int(im.size[0] * scale), int(im.size[1] * scale)) if scale < 1 or scale > 1 else im.size
        if new_size != im.size:
            im = im.resize(new_size, Image.LANCZOS)
    base, _ = os.path.splitext(os.path.join(ROOT, rel_file))
    os.makedirs(os.path.dirname(base), exist_ok=True)
    png = base + ".png"
    webp = base + ".webp"
    im.convert("RGB").save(png, optimize=True)
    im.convert("RGB").save(webp, "WEBP", quality=82, method=6)
    return png, webp, im.size


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", help="slot ids to generate")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--provider", choices=["openai", "gemini"], default=os.environ.get("IMAGE_PROVIDER", "openai"))
    ap.add_argument("--model", default=os.environ.get("IMAGE_MODEL"))
    ap.add_argument("--quality", default="medium", help="openai quality: low, medium, high")
    ap.add_argument("--size", default="2K", help="image_size: 1K, 2K or 4K (omit with --size none)")
    args = ap.parse_args()

    spec = yaml.safe_load(open(SPEC, encoding="utf-8"))
    suffix = " ".join(spec["style_suffix"].split())
    negative = " ".join(spec["negative"].split())
    slots = spec["slots"]
    if args.only:
        wanted = set(args.only)
        slots = [s for s in slots if s["id"] in wanted]
        missing = wanted - {s["id"] for s in slots}
        if missing:
            sys.exit(f"unknown slot ids: {sorted(missing)}")

    if not args.dry_run:
        if args.provider == "gemini":
            from google import genai
            from google.genai import types
            client = genai.Client()
            args.model = args.model or "gemini-3.1-flash-image"
        else:
            from openai import OpenAI
            import base64
            client = OpenAI()
            args.model = args.model or "gpt-image-1"

    results = []
    for s in slots:
        w, h = s["size"]
        target_ratio = w / h
        ratio = pick_ratio(target_ratio)
        prompt = f"{' '.join(s['prompt'].split())} {suffix} Avoid: {negative}."
        gen_desc = openai_size(target_ratio) if args.provider == "openai" else ratio
        print(f"[{s['id']}] {s['page']} -> {s['file']}  gen {gen_desc} -> crop {w}x{h}")
        if args.dry_run:
            print("   ", prompt[:160], "...")
            continue
        img_bytes = None
        for attempt in range(3):
            try:
                if args.provider == "openai":
                    r = client.images.generate(model=args.model, prompt=prompt, size=openai_size(target_ratio),
                                               quality=args.quality, n=1)
                    img_bytes = base64.b64decode(r.data[0].b64_json)
                    break
                img_cfg = types.ImageConfig(aspect_ratio=ratio)
                if args.size and args.size.lower() != "none":
                    img_cfg = types.ImageConfig(aspect_ratio=ratio, image_size=args.size)
                cfg = types.GenerateContentConfig(response_modalities=["IMAGE"], image_config=img_cfg)
                r = client.models.generate_content(model=args.model, contents=prompt, config=cfg)
                for part in (r.candidates[0].content.parts if r.candidates else []):
                    if getattr(part, "inline_data", None) and part.inline_data.data:
                        img_bytes = part.inline_data.data
                        break
                if img_bytes:
                    break
                print("    no image part returned; retrying")
            except Exception as e:  # noqa: BLE001
                msg = str(e)
                if "image_size" in msg or "imageSize" in msg:
                    args.size = "none"
                print(f"    attempt {attempt + 1} failed: {msg[:160]}")
                time.sleep(3 * (attempt + 1))
        if not img_bytes:
            results.append((s["id"], "FAILED"))
            continue
        im = Image.open(io.BytesIO(img_bytes))
        im = center_crop(im, target_ratio)
        png, webp, final = save_outputs(im, s["file"], (w, h))
        print(f"    saved {os.path.relpath(webp, ROOT)} ({final[0]}x{final[1]}, {os.path.getsize(webp)//1024} KB)")
        results.append((s["id"], f"{final[0]}x{final[1]}"))

    if results:
        print("\nSummary:")
        for sid, status in results:
            print(f"  {sid:5s} {status}")


if __name__ == "__main__":
    main()

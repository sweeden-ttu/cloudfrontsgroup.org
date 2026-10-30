# SVG illustration style guide

Every content illustration on cloudfrontsgroup.org is a hand-authored SVG. This guide is the contract that keeps 22 pictures looking like one set. The subject of each picture is in `media-prompts.yml` (field `prompt`); this file is about how to draw it.

## Canvas

| Slot type | viewBox | Notes |
|-----------|---------|-------|
| Opener / mid-content (7:4) | `0 0 1400 800` | Most slots |
| Social card (1.91:1) | `0 0 1200 630` | H2 `og-default`, B1 `blog-default`; also rendered to PNG |
| 404 (3:2) | `0 0 1200 800` | E1 |

Start with a full-bleed cream background rounded by the page CSS, so draw a plain rect: `<rect width="100%" height="100%" fill="#FCF8F3"/>`. Keep all important shapes inside a 10% safe margin (for 1400×800: x 140–1260, y 80–720).

## Palette (use these exact values, nothing else)

| Role | Hex |
|------|-----|
| Background cream | `#FCF8F3` |
| Navy (primary shapes, linework, shadows at low opacity) | `#0B1528` |
| Brand blue (one accent per picture, the thing the eye should land on) | `#2463EB` |
| Mint | `#CCEADD` |
| Teal | `#DEF2E8` |
| Butter | `#FFF0C7` |
| Peach | `#FFE0C2` |
| Surface white (screens, paper) | `#FFFFFF` |
| Placeholder lines (fake text rows, UI bars) | `#B8C0CC` |

Shadows: a second copy of the shape offset 8–14px, `fill="#0B1528" opacity="0.08"`. Ground: a wide rounded rect or ellipse in mint or teal at `opacity="0.6"`. No gradients, no filters, no blur, no glow.

## Drawing rules

1. **Flat geometric vector.** Rounded rectangles (`rx` 12–32), circles, simple paths. Linework in navy, `stroke-width` 6–10 at this scale, `stroke-linecap="round"`, `stroke-linejoin="round"`.
2. **One blue accent.** Exactly one element or small group in `#2463EB` per picture (an arrow, a pin, a wedge, a highlighted card). Everything else navy, pastel, white.
3. **No text, letters, numbers or logos.** Fake text is horizontal rounded bars in `#B8C0CC`, 10–14px tall. Where the brief mentions a logo, draw a plain blue circle or the brand mark path below.
4. **People** are optional and simple: a circle head and a rounded-rectangle body in navy or a pastel, no facial features, no skin-tone rendering.
5. **Central Texas cues** are welcome but quiet: a live-oak canopy (clustered circles on a short trunk), a limestone horizon band in butter, a water tower, three bluebonnet stems (small blue ovals on a green stroke).
6. **Composition**: 2–4 main objects, a clear focal point around the center or a left-to-right flow, and 20–30% empty cream. Isometric or straight-on, not perspective.
7. **Accessibility and size**: root `<svg xmlns="http://www.w3.org/2000/svg" viewBox="…" role="img" aria-labelledby="t">` with `<title id="t">` repeating the alt text. No scripts, no external references, no embedded fonts or bitmaps. Target under 25 KB; use `<defs>` + `<use>` for repeated parts and `<g transform>` to position groups.
8. **Dark mode**: pages switch to navy. The cream rect stays, so the picture reads as a card. Do not use transparency for the background.

## Brand mark (when a logo placeholder is needed)

```svg
<g transform="translate(X Y) scale(S)">
  <path d="M14 44 H50 A8 8 0 0 0 52 28.3 A11 11 0 0 0 31 22 A9 9 0 0 0 14 30.5 A6.8 6.8 0 0 0 14 44 Z" fill="#0B1528"/>
  <path d="M8 44 L30 30 L30 44 Z" fill="#2463EB"/>
  <path d="M14 44 H60" stroke="#0B1528" stroke-width="3" stroke-linecap="round" fill="none"/>
</g>
```
The mark is 64 units wide. Use it sparingly (merchandise, business cards), and never as the blue accent twice.

## Verify before handing back

```bash
rsvg-convert -w 700 images/<name>.svg -o /tmp/<name>.png   # must succeed, then look at the PNG
xmllint --noout images/<name>.svg                            # must be silent
```
Check: nothing outside the safe margin, exactly one blue accent, no text-like glyphs, shapes do not overlap awkwardly, file under 25 KB.

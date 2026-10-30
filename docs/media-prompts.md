# Media and logo generation prompts

Image-generation prompts for every media slot on cloudfrontsgroup.org, written against the brand as it ships today (cream and blue light theme, navy dark theme), not the older dark navy and gold palette the previous image specs targeted. Companion to `design-critique-2026-10-30.md`. A machine-readable copy of the same prompts is in `../imagespecs/media-prompts.yml`, and the drawing contract the SVGs follow is `../imagespecs/svg-style-guide.md`.

## Generation status (2026-10-30)

| Step | Status |
|------|--------|
| Logo system L1–L5 | Done by hand as SVG in `images/logo/`, plus `favicon.svg`, `app-icon-512.png`, `cloud-fronts-avatar.png`. Header now uses the inline mark; `og:image` falls back to the avatar. |
| Founder headshots | Re-exported 800×800 from the originals with the watermark corner cropped out (`scott-weeden.*`, `johnathan-king.*`). |
| Blog default image B1 | Interim: `hero-og.png` cropped to remove its gray bar and watermark, saved as `images/blog-default.png` and set on the first post. Replace with the generated B1 when available. |
| Interim cleanup | Retired the mislabeled and fabricated-claim images (IoT diagram on marketing, notebook slide on political ads, both PPC images, the square social opener, the 99%-badge domain globe, the case-study collage and the two 233px infographic slices). Their `<img>` tags are now `<!-- media slot … -->` comments that name the target file. The scanner illustration moved from social media to `document-management-opener.*` where it belongs. Dead files (unused heroes, persona headshots, candids) deleted. A shared figure rule (`.featured-image`, `.img-service-bot`, `.img-service-center`: 7:4, cover, radius) now frames every content image. |
| Illustrations D1–PI1, C1, E1, H2, B1 | **Done, 2026-10-30, as hand-authored SVG** by four Claude Code subagents following `imagespecs/svg-style-guide.md` (exact palette, one blue accent, no text, 3–7 KB each). All 22 are wired into the pages by `scripts/wire_svg_media.py`; `og-default.png` and `blog-default.png` are rasterized from the SVGs (the og card composites the brand lockup into the reserved left area via `images/og-default-card.svg`). H1 (home hero) intentionally not produced: the home page uses the gradient hero. The image-API path (`scripts/generate_media.py`) remains available but is no longer needed. |

## Why the current media needs replacing

| Problem | Where |
|---------|-------|
| Wrong brand name "TEXAS CLOUD FRONTS" baked into the hero image | `images/hero-banner.*` on the home page |
| AI-tool sparkle watermark in the corner | `hero-banner`, `hero-og`, `scott-weeden` |
| Stock graphics that do not match the page or the alt text | `marketing-opener.png` is an IoT architecture diagram; `political-advertisements-opener.jpg` is a pink "marketing notebook" slide; `before-after-logo.png` is a generic case-study collage |
| Tiny crops of a larger infographic used as "service previews" | `service-web-design`, `service-logo-design`, `service-brand-identity` (233×428) |
| Undersized thumbnails stretched to 700px | `mockup-apparel`, `mockup-print` (354×214), `mockup-website` (708×214) |
| Square image in a landscape slot | `social-media-marketing-opener.avif` (626×626) |
| Old dark glassmorphism palette on a cream site | `domain-names-opener`, `pay-per-click-*`, `social-media-marketing-mid`, `site-hosting-opener` |
| Pages with no imagery at all | `document-management.html`, `online-publishing.html`, `contact.html`, `404.html` |
| Favicon uses the retired palette and "CF" lettering; header mark is a generic icon | `favicon.svg`, `_includes/header.html` |

## Style lock

Append the **style suffix** to every illustration prompt and pass the **negative prompt** where the tool supports one. This is what keeps 24 images looking like one site.

**Style suffix**

> Editorial flat-vector illustration with soft dimensional shading, clean geometric shapes and generous negative space. Palette: warm cream background #FCF8F3; deep navy #0B1528 for primary shapes and linework; brand blue #2463EB as the single strong accent; pastel fills only in mint #CCEADD, teal #DEF2E8, butter #FFF0C7 and peach #FFE0C2. Matte surfaces, no glow, no glass, no neon, no dark backgrounds. Absolutely no text, letters, numbers, logos or watermarks. Subtle Central Texas cues where natural: live oak, limestone, bluebonnets, hill-country horizon, small-town main street. Crisp edges, print-ready, centered composition with a calm 20% margin.

**Negative prompt**

> text, words, letters, numbers, typography, watermark, signature, logo, glow, neon, glassmorphism, dark background, black background, gradient background, photorealistic faces, stock photo look, clutter, duplicate objects, extra fingers, blurry, low contrast, purple, pink

**Dark mode.** Pages switch to navy `#0B1528` in dark mode. Illustrations keep their cream panel and sit inside an 8px to 16px rounded corner, so they read as a card on navy. For the hero and the logo, generate the explicit dark variants listed below.

**Deliverables for every slot.** Master PNG at the size listed, plus a WebP export at the same size (quality 82) and, for anything over 1600px wide, a 1600px WebP for mobile. Keep file names exactly as listed; the pages already reference them.

## Specs by slot type

| Slot type | CSS hook | Rendered size | Generate at | Aspect |
|-----------|----------|---------------|-------------|--------|
| Home hero background | `.hero-bg` (`style.css` line 1426) | full width, ~360px tall on desktop, text overlaid | 3200×1067 | 3:1 |
| Open Graph / social card | `og:image` in `_includes/head.html` | 1200×630 preview | 1200×630 | 1.91:1 |
| Service opener | `.featured-image` (or `.img-service-bot` on the mockup pages) | up to 700px wide | 1400×800 | 7:4 |
| Service mid-content | `.img-service-center` | up to 700px wide, centered | 1400×800 | 7:4 |
| Blog hero / card | `.post-hero img`, `.post-card-media img` | 760px wide on the post, card on the index | 1200×630 | 1.91:1 |
| Founder headshot | `.img-headshot-founder` | 180×180 circle | 800×800 photo export | 1:1 |
| Favicon / app icon | `favicon.svg`, header mark | 16px to 192px | SVG, plus 512×512 PNG | 1:1 |

## Logo system

The name is a weather pun: a cloud "front" moving in over Central Texas. The mark should say cloud, movement and horizon in one shape and survive at 16px. Generate the **mark only**; set the wordmark in the Outfit typeface afterwards in Figma or Illustrator, because generated lettering is never clean enough to ship.

**Wordmark spec (set by hand, not generated).** "Cloud Fronts" in Outfit 700, navy `#0B1528`; "Group" in Outfit 600, brand blue `#2463EB`; tracking -1%; mark sits left of the text at cap height with a gap of half the cap height. This mirrors the current header, where "Group" is already the blue span.

### L1. Primary mark

> Minimal logo mark for a technology company named for a weather front: a single rounded cloud silhouette whose flat base is a long horizon line extending right, with one clean diagonal wedge rising from the left edge of the horizon into the cloud to suggest a front moving in. Two-color flat vector, deep navy #0B1528 cloud and horizon, brand blue #2463EB wedge, on plain white. Geometric, balanced optical weight, no gradients, no shadows, no outline, no text. Centered in frame with 25% margin. Logo design, vector style, 1:1.

Alt text when used as an image: "Cloud Fronts Group mark"

### L2. Favicon reduction

> Same mark as L1 simplified for a 16-pixel favicon: cloud and horizon merged into one solid navy #0B1528 shape, the blue #2463EB wedge kept as one bold stroke, no interior detail, strokes at least one tenth of the canvas width. Flat vector on white, 1:1, centered.

Export as SVG and replace `favicon.svg`. Also export 512×512 PNG for app icons and the social avatar.

### L3. Reversed mark for dark mode and the footer

> Same mark as L1 in reverse: cloud and horizon in warm cream #FCF8F3, wedge in mint #CCEADD, on a flat navy #0B1528 square with 20% margin. Flat vector, no glow, no gradient, 1:1.

### L4. Monochrome

> Same mark as L1 in one color, solid navy #0B1528 on white, for print, embroidery and stamps. Flat vector, 1:1.

### L5. Social avatar

> The L1 mark centered on a flat brand-blue #2463EB circle that fills a square canvas, mark in cream #FCF8F3, 30% margin so it survives circular cropping on Facebook and X. Flat vector, 1:1, 1024×1024.

## Prompts by page

Every prompt below gets the style suffix appended. Alt text is what to put in the page; it describes the picture, not the brand.

### index.html

**H1. Hero background**, replaces `images/hero-banner.webp` and `.png`, 3200×1067, 3:1.

> Ultra-wide panoramic illustration of the Texas Hill Country at golden hour: rolling limestone hills with live oaks in the foreground, a small town water tower and main street far right, and a long band of soft cumulus clouds rolling in from the left like a weather front, with faint data-line arcs connecting the clouds to the town. Keep the center third low-detail and medium-dark in tone so white headline text can sit over it. Horizontal composition, cinematic but flat-vector.

Alt text: decorative; the CSS applies it as a background, so none is needed. Dark-mode variant: same prompt with "sky in deep navy #0B1528 and dusk tones, clouds in slate and mint" so the hero does not flash cream on a navy page.

**H2. Default Open Graph image**, new file `images/og-default.png`, 1200×630. Replaces `favicon.svg` as the `og:image` fallback in `_includes/head.html` and retires `hero-og.png`, which has a gray bar and a watermark.

> Clean social-card illustration: an outline map of Texas in navy with Central Texas highlighted as a single brand-blue dot, one friendly cloud with a flat horizon base floating above the dot, and three thin arcs from the cloud to the left and right edges. Large empty cream area in the left 45% of the frame reserved for a title to be added in a design tool. Horizontal 1.91:1.

### domain-names.html

**D1. Opener**, replaces `images/domain-names-opener.png`, 1400×800, `.featured-image`.

> A simple storefront on a small-town Texas main street with a blank hanging sign above the door, and four floating address tags on short strings rising from the roofline like balloons, each tag a plain rounded rectangle in a different pastel (mint, teal, butter, peach) with no writing. A hand from the left reaches for the brightest tag. Morning light, horizontal.

Alt text: "Storefront with blank address tags floating above it, one being picked"

### site-hosting.html

**S1. Opener**, replaces `images/site-hosting-opener.avif`, 1400×800, `.featured-image`.

> Isometric illustration of a tidy server rack drawn as three stacked rounded blocks resting on a flat cloud, with three thin lines running down to a laptop, tablet and phone on a wooden desk below; each screen shows the same simple page layout as colored blocks, no text. A small shield shape with a check mark sits beside the rack. Navy linework, brand-blue lines, pastel fills, cream background, horizontal.

Alt text: "Servers on a cloud connected to a laptop, tablet and phone"

### marketing.html

**M1. Opener**, replaces `images/marketing-opener.png` (currently an unrelated systems diagram), 1400×800, `.featured-image`.

> Top-down flat lay of a marketing planning desk: an open notebook with a hand-drawn rising line chart and a funnel sketch, a tablet showing simple bar charts as colored blocks, three pastel sticky notes left blank, a pencil, a coffee mug, and a sprig of bluebonnets in a small jar. Overhead view, soft shadows, cream desk surface, horizontal.

Alt text: "Overhead view of a marketing planning desk with charts and notes"

### political-advertisements.html

**P1. Opener**, replaces `images/political-advertisements-opener.jpg` (currently a notebook stock slide), 1400×800, `.featured-image`.

> Non-partisan campaign materials laid out on a table: a yard sign on wire stakes with a bold blank panel and a single star shape, a tri-fold mailer standing half open, a phone showing a simple ad layout as colored blocks, and a wall calendar with a few dates circled. Red, white and blue kept to navy, cream and brand blue only; one small red-orange star is the only warm accent. Clean, civic, horizontal.

Alt text: "Yard sign, mailer, phone ad and calendar arranged on a table"

### social-media-marketing.html

**SM1. Opener**, replaces `images/social-media-marketing-opener.avif` (square), 1400×800, `.featured-image`.

> Split composition: left, a monthly content calendar grid with small pastel squares and a few picture thumbnails; right, a phone held upright showing a feed of three post cards with hearts and comment bubbles floating up as simple shapes. A thin brand-blue line links a calendar square to the top post. Horizontal.

Alt text: "Content calendar beside a phone showing social posts with reactions"

**SM2. Mid-content**, replaces `images/social-media-marketing-mid.png`, 1400×800.

> Overhead desk scene for planning posts: a ring light at the edge of frame, a phone on a small tripod, a printed calendar with color-coded pastel dots, a stylus, and a stack of product photos fanned out. Soft window light from the left, cream desk, horizontal.

Alt text: "Desk set up for planning and photographing social media content"

### pay-per-click-marketing.html

**PPC1. Opener**, replaces `images/pay-per-click-marketing-opener.png`, 1400×800, `.featured-image`.

> A browser window drawn as a rounded rectangle with a highlighted result card at the top in butter yellow and three plain result rows below it as gray bars. Floating beside the window: a small cursor arrow clicking the highlighted card, a coin with an upward arrow, and a tiny rising bar chart. Flat, horizontal, no words.

Alt text: "Search results page with a highlighted ad card being clicked"

**PPC2. Mid-content**, replaces `images/pay-per-click-marketing-mid.png`, 1400×800.

> Left-to-right journey in four small vignettes connected by a dotted brand-blue path: a person at a laptop, the person walking away, a phone showing a reminder ad card, and the person returning to the laptop with a shopping cart and a check mark. Simple figures with no facial detail, pastel fills, horizontal.

Alt text: "Four-step journey showing a visitor leaving and returning after a reminder ad"

### document-management.html

**DM1. Opener**, new file `images/document-management-opener.webp`, 1400×800, insert at the top of the content with `class="img-service-bot"`.

> Left-to-right transformation: a wooden filing cabinet with paper spilling out on the left, a flat scanner in the middle with a brand-blue arrow passing through it, and on the right a neat stack of three glowing-free digital folder icons on a soft cloud. Cream background, navy linework, horizontal.

Alt text: "Paper files passing through a scanner and becoming digital folders"

**DM2. Mid-content**, new file `images/document-management-mid.webp`, 1400×800, `class="img-service-center"`.

> A single cloud in the center with four thin lines to a laptop, a tablet, a phone and a desktop monitor arranged around it; each device shows the same folder icon. A small padlock sits on the cloud. Symmetric, calm, horizontal.

Alt text: "Cloud storage connected to four devices showing the same folder"

### online-publishing.html

**OP1. Opener**, new file `images/online-publishing-opener.webp`, 1400×800.

> Floating composition of publishing formats: an upright hardcover book with a plain geometric cover in navy and peach, an open magazine spread with picture blocks and gray text lines, a tablet showing a document, and a phone showing a newsletter card. Gentle drop shadows, cream background, horizontal.

Alt text: "Book, magazine, tablet and phone showing published content formats"

**OP2. Mid-content**, new file `images/online-publishing-mid.webp`, 1400×800.

> Hub-and-spoke diagram with a document icon in the center and six spokes to small cards: a blog page, a social post card, a video play button, a microphone, an envelope and a slide. Lines in brand blue, cards in pastels, no labels, horizontal.

Alt text: "One document in the center connected to six content formats"

### logo-design.html

**LD1. Before and after**, replaces `images/before-after-logo.webp` (stock collage), 1400×800, `.img-service-bot`.

> Side-by-side comparison on one canvas: left half, a cluttered fictional bakery logo drawn as an overworked badge with too many shapes and ribbons in muddy colors; right half, its redesign as a single clean geometric wheat-and-sun mark in navy and butter yellow. A thin vertical divider and a small arrow between them. No letters anywhere. Horizontal.

Alt text: "A cluttered logo on the left redesigned into a simple geometric mark on the right"

**LD2. Service preview**, replaces `images/service-logo-design.webp` (infographic crop), 1400×800, `.img-service-center`.

> Designer's desk from above with the logo process laid out left to right: thumbnail sketches on paper, a refined pencil drawing, a vector mark on a tablet, and the final mark applied to a business card and a coffee cup. Pastel fills, navy linework, cream desk, horizontal.

Alt text: "Logo design process from sketches to the finished mark on a card and cup"

### web-design-hosting.html

**WD1. Website mockup**, replaces `images/mockup-website.webp` (undersized collage), 1400×800, `.img-service-bot`.

> A desktop monitor, a tablet and a phone angled together showing the same responsive small-business website as flat colored blocks: a hero band, three cards, a footer. Devices in navy outline with cream screens, brand-blue header band, pastel cards. Floating on a cream background with a soft shadow, horizontal.

Alt text: "The same website shown on a monitor, tablet and phone"

**WD2. Service preview**, replaces `images/service-web-design.webp` (infographic crop), 1400×800, `.img-service-center`.

> Wireframe-to-finished transition: left, a page wireframe drawn in thin navy lines with gray placeholder boxes; right, the same page filled in with pastel blocks and a picture area; a brand-blue arrow between them. Clean, horizontal.

Alt text: "A website wireframe turning into a finished page design"

### design-print-agency.html

**DP1. Print samples**, replaces `images/mockup-print.webp` (354×214), 1400×800, `.img-service-bot`.

> Flat lay of printed collateral on a cream surface: a fan of business cards, a folded brochure, a letterhead sheet, a sticker sheet of simple shapes and a postcard, all sharing one navy and peach pattern with no text. Overhead view, soft shadows, horizontal.

Alt text: "Business cards, brochure, letterhead and postcard laid out together"

### promotional-items.html

**PI1. Branded merchandise**, replaces `images/mockup-apparel.webp` (354×214), 1400×800, `.img-service-center`.

> Group of promotional items on a cream background: a navy t-shirt, a cap, a tote bag, a ceramic mug, a water bottle and a pen, each carrying the same small abstract mark as a plain blue shape where a logo would go. Arranged in a loose arc, soft shadows, horizontal.

Alt text: "T-shirt, cap, tote bag, mug, bottle and pen with matching branding"

### about-us.html and team.html

**AB1, AB2. Founder headshots.** Do not generate. `images/scott-weeden.png` and `images/johnathan-king.png` are real photographs. Re-export from the originals at 800×800, face centered, shoulders in frame, and crop out the AI-tool sparkle mark in the lower right corner of the current file. If a re-shoot is possible, use the same backdrop and light for both so the two circles match.

**AB3. Optional team or office photo.** A real photograph of the two founders working with a client, landscape 1400×800, natural light. Not generated.

### contact.html

**C1. Service-area illustration**, new file `images/contact-service-area.webp`, 1400×800, place above the contact details with `class="img-service-center"`.

> Soft illustrated map of Central Texas as a cream shape with a navy outline, a cluster of small town silhouettes near the middle, a brand-blue location pin, and a cloud with a flat horizon base drifting above. Gentle, welcoming, horizontal, no place names.

Alt text: "Illustrated map of Central Texas with a location pin"

### 404.html

**E1. Not-found illustration**, new file `images/404-lost-cloud.webp`, 1200×800, `.img-service-center`.

> A small, puzzled cloud with a flat base sitting on the ground beside an empty signpost at a fork in a country road under a clear cream sky, bluebonnets at the roadside. Friendly, light, no text.

Alt text: "A lost little cloud beside an empty signpost"

### blog.html and posts

**B1. Default post image**, new file `images/blog-default.png`, 1200×630. Use as the `image` for posts that have no bespoke picture, and update the first post's front matter to it in place of `hero-og.png`.

> Open notebook on a cream desk with a pen, a mug and a window light, and a single cloud with a flat horizon base drawn on the notebook page. Large quiet area on the left half. Horizontal 1.91:1.

Alt text: "Notebook with a cloud sketch on a desk"

**B2. Per-post images.** Follow the same style suffix and 1200×630 size. Write the prompt as "subject of the post, in the same flat-vector style" and avoid any text in the picture; the title is rendered by the page and by the social card.

## Workflow

1. Generate L1 first and approve the mark. Everything else can reference "the mark" only as an abstract blue shape, so the logo does not need to exist before the rest.
2. Generate each slot at the listed size with the style suffix and negative prompt. Pick the candidate with the most negative space and the fewest objects; reject anything with letters.
3. Export PNG master and WebP, run them through an optimizer, and drop them into `images/` with the exact file names above.
4. For the new slots (DM1, DM2, OP1, OP2, C1, E1, B1) add the `<img>` to the page body with the class and alt text listed, run `bundle exec jekyll build`, and check the page at 375px and 1280px.
5. Update `_includes/head.html` so the `og_image` fallback is `images/og-default.png` instead of `favicon.svg`.
6. Replace `favicon.svg` with the L2 export and remove the now unused Lucide cloud icon in `_includes/header.html` in favor of an inline SVG of L1.

The retired `gen_images.py` can be pointed at `imagespecs/media-prompts.yml`; its old inline prompt list and dark-palette style guide should not be reused.

# Design critique — cloudfrontsgroup.org (2026-10-30)

**Verdict: Solid bones, wrong first impression. The token system, card language and blog scaffolding are sound, but the homepage sells "cloud infrastructure" to people who want a website and a logo, three layout bugs break the phone experience (unreadable sub-menus, a sideways-scrolling hero, a two-column contact form at 375px), and the service-page imagery is a mix of mismatched, upscaled and fabricated stock that undercuts the "local, hands-on, real people" promise.**

Critique-only run. No site files were edited. I could not screenshot; everything below is reasoned from `style.css`, `site.js`, `_layouts/`, `_includes/`, `_data/nav.yml`, the page files and the rendered HTML served at `http://127.0.0.1:4000/`, at 375px, 768px and 1280px. Image judgements come from viewing every file in `images/` that a page references.

## Ship this

| # | Problem | Fix (exact) | Verify |
|---|---------|-------------|--------|
| 1 | Mobile sub-menus are black text on near-black. `style.css:1272` hard-codes `.dropdown-content { background: hsl(220, 28%, 11%) }` inside the `max-width: 768px` block, while `style.css:441` gives `.dropdown-content a { color: var(--color-text) }` = `#000` in light mode. Every "Our Products" / "Our Services" link is invisible on a phone in light mode. | In the mobile block replace the background with `background: var(--color-surface-2); border-top: 1px solid var(--header-border);` and change `style.css:1283` to `border-bottom: 1px solid var(--color-border-soft);`. | 375px, light theme, tap menu, tap "Our Services": seven readable links. |
| 2 | Homepage hero overflows the viewport. `index.html:9` places `.hero-image` **outside** `.container`, but `.hero-image` at `style.css:584` still carries `margin: -2.5rem -2rem 2.5rem` (meant to cancel container padding). Result: the block is 4rem wider than the page, so the index scrolls sideways at every width, and 40px of hero hides behind the sticky header. The mobile override at `style.css:1289` only targets `.hero`, not `.hero-image`. | `style.css:584` -> `margin: 0 0 2.5rem;` and add inside the 768px block `.hero-image { padding: 3.5rem 1.25rem 3rem; }`. While there, label the primary button with the number: `index.html:14` -> `Call 254-317-6688` (desktop visitors can read it; phones still dial). | `document.documentElement.scrollWidth === window.innerWidth` on `/` at 375 and 1280. |
| 3 | Contact page breaks at 375px and the phone number is not tappable. `.contact-grid` (`style.css:1412`) is `1fr 1fr` with no media query, so at 375px each column is ~155px and `scottweeden@cloudfrontsgroup.org` overflows the column (sideways scroll). `contact.html:30` prints the phone as plain text; `_includes/footer.html:12` does the same. Labels and fields share one `gap: .75rem` (`style.css:1413`) so a label sits as far from its own field as from the previous one; inputs are ~39px tall (`style.css:1415`). | Add to the 768px block: `.contact-grid { grid-template-columns: 1fr; gap: 1.5rem; }`. Change `contact.html:30` to `<a href="tel:{{ site.phone_tel }}" class="btn btn-primary">Call {{ site.phone }}</a>` and footer line 12 to a `tel:` link. `style.css:1413-1415`: `.contact-form { gap: .25rem } .form-label { margin-top: .75rem } .form-input { min-height: 44px; padding: .65rem .8rem; border-radius: var(--radius-sm) }`. Move `style="align-self:flex-start;"` (`contact.html:50`) into a `.contact-form .btn { align-self: flex-start; margin-top: .75rem }` rule. | 375px: one column, no horizontal scroll, tapping the number opens the dialer. |
| 4 | Service pages have no image system. Six pages use `class="featured-image"` which is **not defined anywhere** in `style.css` (grep count 0), so `domain-names.html:11` dumps a 1536x1024, 2.4 MB PNG at full container width with square corners and zero margin, touching the subtitle above and the card below. Three other pages use `.img-service-bot` / `.img-service-center` (`style.css:1366-1367`, 8px radius, `width:100%`), which stretches the 233px-wide `service-web-design.webp` / `service-logo-design.webp` to 700px wide and ~1290px tall. See "Media and logo findings" for the content problems. | Add one rule and use it everywhere: `.page-figure { width: 100%; aspect-ratio: 2 / 1; object-fit: cover; border-radius: var(--radius); margin: 1.5rem 0 2rem; background: var(--color-surface); }` plus `.page-figure-mid { max-width: 700px; margin-inline: auto; aspect-ratio: 3 / 2; }`. Replace `featured-image`, `img-service-bot`, `img-service-center` with those two classes; delete the `<img>` for the three 233x428 slices (`logo-design.html:16`, `web-design-hosting.html:17`) until replacements exist; add `width`/`height` attributes and drop `loading="lazy"` on the first image of each page. | 1280px on `/domain-names.html`: rounded 2:1 figure, 24px of air above and 32px below; no image wider than its box; Lighthouse CLS 0. |
| 5 | Header and brand mark. (a) The wordmark (`_includes/header.html:6`) is an `<h1>` with no link, so the site name is not a way home and every page ships two `<h1>`s (service pages) or an `<h1>` that is the site name (index, blog, contact). (b) "About Us" is a dropdown containing one item (`_data/nav.yml:10-13`). (c) Between ~769px and ~990px the desktop nav (six `white-space: nowrap` items, `style.css:374-388`) plus toggle plus wordmark exceed the `.inner` width and `flex-wrap` is only set at 768px (`style.css:1248`), so iPad portrait (820/834px) overflows. (d) `theme-color` is `#003a70` (`_config.yml:36`) while the header is cream. | (a) `header.html:6` -> `<a class="brand" href="{{ rp }}index.html"><i data-lucide="cloud"></i> Cloud Fronts <span>Group</span></a>`; change selectors at `style.css:350, 352, 364, 1249` from `header h1` to `header .brand`; then promote each page's real title to `<h1>` (`index.html:11`, `contact.html:10`, `blog.html:11`, `_layouts/post.html:11`) and add `h1 { font-size: clamp(2rem, 4vw, 2.75rem); line-height: 1.1; margin: 0 0 .5rem }` after `style.css:280`. (b) `nav.yml:10-13` -> `- label: About Us / href: about-us.html / key: about-us`. (c) Change the mobile media queries at `style.css:1236` and `1453` to `max-width: 1024px`. (d) `_config.yml:36` -> `"#fcf8f3"`. | 820px: no horizontal scroll, hamburger shown. `document.querySelectorAll('h1').length === 1` on every page. Keyboard: Tab lands on the wordmark first after the skip link. |
| 6 | Blog: the post title looks like a section heading, the hero is a 6 MB PNG, and shares have no image. `.post-title` (`style.css:1494`) does not cancel the generic `h2` rule at `style.css:282-296`, so the title gets the same grey rule and gold bar as every body `## heading` and the article has no top. The post and the index card load `images/hero-og.png` (2848x1504, 6.0 MB) via `_posts/2026-10-30-welcome-to-the-cloud-fronts-group-blog.md:4`; `hero-og.webp` (178 KB) exists but is unused. `_includes/head.html:6` falls back to `favicon.svg` for `og:image` on every non-post page; Facebook, X and LinkedIn do not render SVG, so the homepage shares with no image. `.post-cta .hero-cta` (`style.css:1520`) never gets `display:flex` so the two buttons are separated by a text space, not `gap`. | `style.css:1494`: append `border: 0; padding-bottom: 0;` and add `.post-title::after { display: none }`. Front matter: `image: images/hero-og.jpg` (export 1200x630, <=250 KB) and keep PNG out of `_site`. `head.html:6`: `assign og_image = site.url | append: '/images/og-default.jpg'` (a real 1200x630 JPG; see media findings). `style.css:1520`: `.post-cta .hero-cta { display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap; }`. | View `/blog/welcome-to-the-cloud-fronts-group-blog.html`: title has no underline; network panel shows <300 KB for the hero; `curl -s / | grep og:image` returns a `.jpg`. |

---

## 1. index.html

### First impression
I land on a dark navy band that says "Scalable Cloud Solutions - Empower your digital infrastructure with seamless deployment and high-availability hosting." I think I have reached a cloud-hosting vendor. Then, below the fold, a centred essay tells me about a no-long-term-contracts marketing partner, four big numbers, a boxed ad for a different website, and six service cards. The page is two different companies stacked on top of each other, and on a phone it scrolls sideways.

### What works
- The token system is real: cream `#fcf8f3`, navy `#0b1528`, blue `#2463eb`, Outfit/Open Sans, 16/24/32px radii, and a complete `[data-theme="dark"]` set (`style.css:14-93`, `171-220`). Dark mode is not an afterthought.
- Service cards (`style.css:1044-1056`) are clean, generous, and readable: 1.05rem title, muted 0.88rem copy, pill buttons.
- The two-step close ("YOU" `.impact-section` then `.cta-banner` "Get a Quote") gives the page a proper ending with one action, in brand navy with one gold button.
- Lucide icons via `data-lucide`, `aria-hidden` set at creation, a working skip link, a focus-visible-friendly share bar: the accessibility floor is in place.

### Walk-through
- **Hero (`index.html:9-18`, `style.css:579-635`).** Besides the overflow (Ship 2), the hero's two buttons have equal visual weight and the pale gold `.btn-gold` (`#fff0c7` on navy) is brighter than the blue `.btn-primary`, so the eye lands on "Email Us Now" although the class hierarchy says calling is primary. The copy is the bigger problem and is a Site Content Editor job: "Scalable Cloud Solutions" and "digital infrastructure" do not match the service grid (domains, logos, web design, social, print, ads) or the Central Texas, no-contract promise. The hero is pure gradient (`.cloud-hero-bg`, `style.css:1427`): no photo, no place, no people. Note: `.hero-bg` at `style.css:1426` points to `images/hero-banner.webp` but no element uses that class; `index.html:9` uses `cloud-hero-bg`, so the "TEXAS CLOUD FRONTS" banner is currently orphaned, not displayed.
- **Welcome block (`index.html:22-27`).** `.section-heading` centres everything and caps `p` at 600px (`style.css:711-715`). Two five-line centred paragraphs are hard to read on a phone and repeat the hero's job. The `h3.hero-heading` "Ready to Grow Your Business?" at 1.3rem (`style.css:1425`) sits directly under a 2rem h2 and reads like a subtitle, not a question. Make this the hero's headline and cut the block to one paragraph left-aligned under the service grid.
- **Stats counter (`index.html:29-46`).** `grid-template-columns: repeat(auto-fill, minmax(200px, 1fr))` (`style.css:640`): at 1280px the 1096px track fits exactly five columns, so four cards leave an empty fifth column on the right; at 768px you get three plus one orphan; at 375px four stacked cards push the services ~450px down. Switch to `repeat(auto-fit, minmax(150px, 1fr))` or `repeat(4, 1fr)` with a 2x2 at 768px. More importantly, see Owner decisions: "50+ Projects", "30+ Satisfied Clients", "100% Satisfaction Guarantee" must be verified or removed.
- **"Blogs & Other Interest" sidebar (`index.html:48-53`, `style.css:1434-1459`).** It floats right at 280px, so the grid that follows is narrowed for its entire height (grid containers avoid floats): at 1280px `.service-grid` drops from three columns to two and leaves a ~300px empty gutter beside rows two and three. Its button uses `btn-accent`, which does not exist in `style.css` (count 0), so "Visit Site" renders as unstyled blue text in a transparent pill. `style.css:1445` also references `--font-heading`, which is undefined (the token is `--font-head`). Fix: make it a full-width `.callout` band after the service grid, class the link `btn btn-outline`, or move it into the footer.
- **Service grid (`index.html:54-91`).** Icons do not scale: `.service-card .service-icon { font-size: 2.2rem }` (`style.css:740-745`) sizes the `<span>`, but Lucide replaces `<i>` with a 24x24 `<svg>`, so each card has a 24px icon floating in a 60px line box. Add `.service-icon svg { width: 2.2rem; height: 2.2rem }`. Buttons do not align across cards because the card is not a flex column; add `.service-card { display:flex; flex-direction:column } .service-card .btn { margin-top:auto; align-self:center }`. "Register Your Domain Now" vs five "Learn More" is a copy inconsistency for the editor.
- **Impact section (`index.html:93-97`).** "YOU" at up to 4.5rem (`style.css:684`) is a bold move that works, but the paragraph has no `max-width`, so at 1280px it runs ~1030px wide (about 140 characters per line). Add `.impact-section p { max-width: 62ch; margin-inline: auto }`.
- **CTA banner.** Good. In dark mode the navy gradient (`style.css:722`) sits on a navy page with no border, so the band disappears; add `border: 1px solid var(--color-border)` under `[data-theme="dark"]` and the system dark block (same for `.post-cta`).

### Width notes
- 375px: hero text 2rem, buttons wrap to two rows (fine); stats stack; sidebar full width (`style.css:1453-1459`); cards single column; "YOU" at ~2.5rem. Sideways scroll from Ship 2 is the dominant defect.
- 768px: hits the mobile breakpoint exactly (hamburger). Stats 3+1, service grid single column (`style.css:1295`), which is a waste at 736px: use `repeat(2, 1fr)` between 600 and 1024px.
- 1280px: see float squeeze and empty stats column above.

---

## 2. domain-names.html (representative service page)

### First impression
A 32px heading, a sentence, then a wall-to-wall glowing globe with ".com .org .net .io .co .co" and a "99%" badge, then a white card of text. It looks like a hosting reseller landing page from a template, and nothing on it invites me to call.

### What works
- Copy is concrete (TLDs, DNS record types, WHOIS privacy) and chunked into six equal cards, which scan well at 1280px (3x2) and 768px (2x3).
- The closing paragraph says what is included and links to contact.

### Walk-through
- **Title (`domain-names.html:8`).** `h1` has no site rule, so it renders at UA 2em = 32px, the same size as `h2` at 1280px (`clamp(1.5rem, 3vw, 2rem)`, `style.css:283`). The page has no top. Ship 5 adds the `h1` rule.
- **Subtitle + image + card (`:9-17`).** `.subtitle { margin: -0.5rem 0 0 }` (`style.css:1111`) zeroes its bottom margin, the image has no class rule, and `.card` has no top margin, so three elements touch. Ship 4.
- **Cards (`:20-45`).** `.card:hover` lifts and turns the border blue (`style.css:793-797`) but nothing here is clickable; hover affordance on static content teaches visitors to click dead cards. Scope the hover to `a.card, .card:has(a)` or drop it on this page.
- **No CTA.** The only conversion path is a text link in the last paragraph (`:50`). Reuse `.cta-banner` from the homepage (two lines of copy, one `btn-gold`, and the phone number) at the end of every service page. This is the highest-value change per service page after the image fix.
- **Newsletter box (`:53-61`, `style.css:1358-1363`).** Appears on 13 pages, promises "program updates and community resources" (research-site language) and competes with the contact CTA. Keep it on the blog and about pages only. Its input has a 16px radius next to a 9999px button; use `var(--radius-sm)` on the input or make both pills.
- **Dark mode.** The opener is a dark navy illustration with a glowing globe: on cream it is a heavy slab, on navy it melts into the page with no edge. A defined figure box with `background: var(--color-surface)` and radius solves the edge; the content problem is in the media section.

### Width notes
- 375px: 1536px PNG downscaled to 343px wide, 229px tall, 2.4 MB on a phone connection; cards single column; newsletter input and button fit on one line.
- 768px: cards 2x3; image 736x491 with square corners.
- 1280px: image 1096x731 with square corners immediately under a 32px title.

---

## 3. about-us.html

### First impression
A sensible page: who, where (Killeen, Temple, Harker Heights, Belton, Copperas Cove), the no-contract promise, six services, why us, two faces. It is the most honest page on the site, and it is the one that most needs the photos to carry it.

### What works
- Local specificity in the second paragraph (`about-us.html:15`) and "We answer our own phones. We show up to meetings in person." (`:47`). This is the brand voice; the homepage should sound like this.
- The founder cards (`:53-64`) are a good pattern: circular photo, name, role, three-line bio, centred.

### Walk-through
- **Services grid (`:18-44`)** repeats the homepage grid without links or buttons. Six dead-end cards. Either link each card title to its page (`<h3><a href="web-design-hosting.html">`) or cut the section and let the nav do its job.
- **Headshot crop (`style.css:1368`).** `.img-headshot-founder` is 180px, `object-fit: cover` on 1824x2294 portraits. Cover takes the centred square (y 235-2059), so the top of each head clips slightly and most of the circle is shirt and jacket; the face is roughly 60px tall. Add `object-position: 50% 22%`, or better, deliver 800x800 square crops with eyes at ~40% height (see media). Source files are 231 KB and 423 KB for a 180px circle (360px at 2x needed).
- **Team card grid at 1280px.** `.card-grid` auto-fill (`style.css:818`) makes three tracks for two cards, leaving an empty third column; use `.team-grid { grid-template-columns: repeat(2, minmax(0, 320px)); justify-content: center }`.
- **No CTA.** Same as domain-names: "Contact us today" text link only (`:49`). Add the `.cta-banner` with the phone.
- **Heading order.** Header `h1` + page `h1` (`:9`); fixed by Ship 5.

### Width notes
- 375px: single column; founder bios centre-aligned at 0.9rem are fine at three to four lines.
- 768px: 2-column cards; two founders side by side at ~352px each (good).
- 1280px: empty third column in the team grid.

---

## 4. contact.html

### First impression
80px of cream, then "Contact Us" with a grey rule, two emails that say "click to reveal" (they are already revealed by JS), a plain phone number, and a form. Nothing tells me when you answer, where you are, or what happens after I press Send (the "within 1 business day" line only appears on the hidden thank-you). On my phone the page is two squeezed columns.

### What works
- Honest, simple form: name, email, subject, message, no CAPTCHA, labels associated with inputs, `required` where it matters.
- Both founders' direct emails are offered; that is a trust signal most agencies hide.

### Walk-through
- **Spacing.** `.container` padding 2.5rem plus `h2` margin-top 2.5rem (`style.css:284`) = 80px of nothing above the title. Use the `h1` rule from Ship 5 with `margin-top: 0`.
- **Grid at 375px.** Ship 3.
- **Phone.** Ship 3. On a phone, calling is the primary conversion for this audience; it should be the first, largest tappable thing on the page.
- **"click to reveal".** `site.js:76-82` replaces the text immediately on load, so the label only shows without JS. Harmless, but a `mailto:` with the address and `rel="nofollow"` is simpler.
- **Form rhythm and size.** Ship 3. Also `.thankyou-msg` uses `--color-primary` (`style.css:1410-1411`), which is undefined: the border falls back to `currentColor`, the heading colour to inherited black. Use `--color-accent`.
- **Reassurance.** Move "We'll get back to you within 1 business day" above the form as visible copy; add service area and hours if the owners want to publish them (Owner decisions).

### Width notes
- 375px: two 155px columns, email overflow, 39px inputs. Fails.
- 768px: two 352px columns; acceptable but "Direct Contact" has three short lines and 300px of empty space beneath.
- 1280px: fine; form column is 532px wide, inputs full width (good line length for a message box).

---

## 5. Blog: blog.html and blog/welcome-to-the-cloud-fronts-group-blog.html

### First impression (index)
"Blog" with a rule, a subtitle, a paragraph explaining the blog is shareable, then the most prominent button on the page says "Subscribe via RSS". Then one card in the left third of an otherwise empty three-column grid. A business owner does not know what RSS is and does not care; the card is what they came for.

### First impression (post)
Clean, readable article column (760px, 1.08rem/1.75). The kicker "Blog · announcements central-texas" with teal tags is a nice touch. The title has the same grey underline as the section headings below it, the hero image is a map of Texas with network clouds and a grey bar along the bottom, and the alt text describes a skyline that is not there.

### What works
- `_layouts/post.html` is well-structured: kicker, title, meta with reading time, figure with optional caption, body, share bar, prev/next, CTA. `share.html` has no third-party scripts and 44px targets (`style.css:1510`).
- `.post-card` with 1.91:1 media (`style.css:1481`) matches the OG ratio, so the card and the social preview are the same picture. Good systems thinking.
- JSON-LD `BlogPosting`, `article:published_time`, feed link: the plumbing for the Social Media Distributor is there.

### Walk-through
- **RSS button (`blog.html:14`).** Demote to a text link in the footer of the list ("RSS feed" with the icon). Promote a "Get in touch" `.btn-primary` if any button belongs up here.
- **Grid with one post.** `.post-list` auto-fill 300px (`style.css:1478`) is right for 3+ posts. Add `.post-card:first-child:last-child { grid-column: 1 / -1; display: grid; grid-template-columns: 1.2fr 1fr }` so a lone post becomes a featured row at >=768px.
- **Tags** render as raw slugs (`central-texas`). Map to labels with a `_data/tags.yml` or `replace: '-', ' '` and `capitalize`.
- **Title rule and body hierarchy.** Ship 6. Also `.post-body h2` is 1.6rem (`style.css:1500`) with the generic underline; `.post-body h3` 1.3rem; fine once the title loses the underline.
- **Hero image.** Ship 6 and media findings.
- **`.post-container` max-width 760px** (`style.css:1490`) gives ~81 characters per line at 1.08rem; tighten to 720px or raise the body to 1.1rem to land inside 75ch.
- **Post CTA** (`post.html:40-47`) is a navy box on cream (good) that vanishes on navy in dark mode (`style.css:1517`); add a border token for dark.
- **Kicker heading level.** The post title is an `h2` and the body uses `##` so title and sections are the same level; Ship 5 fixes by making the title `h1`.

### Width notes
- 375px: title 2rem, hero 343px wide, share buttons wrap to two rows, CTA buttons wrap (fine). The 6 MB PNG is the only serious issue.
- 768px: identical layout, 696px column.
- 1280px: blog index card occupies 349px of 1096px.

---

## 6. Header, nav and footer (shared)

- **Layout.** `style.css:346-350` orders nav left, toggles middle, wordmark right. The brand is where readers look last, it is not a link, and on mobile (`style.css:1248`) the hamburger sits far left, the theme toggle in the centre, and the name far right, so the three controls float apart. Recommend brand left, nav right, hamburger right next to the theme toggle. If the owners like the name on the right, at least make it a link (Ship 5).
- **Breakpoint gap.** 769-990px overflow (Ship 5c).
- **Dropdowns.** `href="#"` plus a literal "▼" (`header.html:13`); `site.js:37-73` adds `role="button"`, `aria-haspopup`, `aria-expanded`, Escape and outside-click. Good. Replace "▼" with `<i data-lucide="chevron-down">` sized 1em so it matches the icon set and does not wobble between fonts.
- **Information architecture.** "Our Products" (Domain Names, Promotional Items, Site Hosting, Marketing, Political Advertisements) versus "Our Services" (Logo Design, Web Design & Hosting, Design & Print Agency, PPC, Social Media, Document Management, Online Publishing) is not a distinction a visitor can predict: hosting appears in both groups, and "Marketing" is a product while "Social Media Marketing" is a service. One "Services" menu of ~8 items in two visual columns, or two groups named by outcome ("Get found online", "Look professional"), would halve the hunting. Owner decision.
- **Active state.** Only `home`, `blog`, `contact` can be active (`nav.yml` keys); 13 of 17 pages show no current-page indicator. After flattening About Us, add `active:` to service pages and a `key` on the parent dropdown.
- **Light-mode leftovers from a dark-first design.** `header { box-shadow: 0 4px 24px hsla(0,0%,0%,0.25) }` (`style.css:332`) is a heavy shadow for a cream bar; `.dropdown-content` shadow 40% black (`:418`); `.theme-toggle:hover { background: hsla(0,0%,100%,0.10) }` (`:480`) is invisible on cream; `--header-nav-hover: rgba(0,0,0,0.05)` (`:55`) is invisible on navy in dark mode. Use `hsla(220,40%,10%,0.08)` for the header shadow and `var(--color-surface-2)` for toggle hover.
- **Tap targets.** `.theme-toggle` ~30px, `.menu-toggle` ~33px (`style.css:467-496`). Set `min-width: 44px; min-height: 44px; display: inline-flex; align-items: center; justify-content: center` on both.
- **Mobile panel.** `header nav` is absolute under the sticky header with no `max-height`; with "Our Services" open the list is ~610px tall on a 667px viewport and cannot scroll. Add `max-height: calc(100vh - 58px); overflow-y: auto`. The hamburger lacks `aria-expanded`; toggle it in `site.js:31-33`.
- **Footer (`_includes/footer.html`).** Centred, compact, readable: social, quick links, two emails, phone, copyright. Missing: the brand name, service area, a `tel:` link, and a route to the "other interest" site. At <=480px `footer p` drops to 0.72rem (11.5px, `style.css:1310`) which is below comfortable reading on the device most visitors use; keep 0.82rem. `.footer-copy` is 0.72rem everywhere (`:1355`). In dark mode `--footer-text` falls to `hsl(220,10%,52%)` on `#060c18` (about 4.9:1), acceptable but dim for the only place the phone number appears on most pages.

---

## 7. Site-wide CSS findings (not page-specific)

- `style.css:971-974`: `[data-theme="dark"] th, @media (prefers-color-scheme: dark) { th {...} }` is invalid CSS; the whole rule is dropped, so `th` keeps `background: var(--brand-navy)` in dark mode and merges with the page. Split into two rules.
- `.btn-gold:hover` (`:874-877`) sets `#ffea4d` with `#fff` text (about 1.4:1). Keep navy text on hover. `.btn-teal` (`:878-881`) is white text on `#def2e8` (about 1.1:1), and `404.html:11` uses it for the only button on the 404 page, so "Back to Homepage" is unreadable. Make `.btn-teal` navy text or retire it.
- `.principle-card .num` and `.principle-detailed h3 .num` (`:1024-1031`, `:1095-1100`) are white digits on a pastel teal gradient; unused on current pages but will bite the first page that uses them.
- `h2::after` (`:289-296`) paints a 3rem gold-to-amber bar in `#fff0c7 -> #ffe0c2`; on cream and white it is invisible, so every h2 reads as a plain grey rule. Use `var(--brand-blue)` or `var(--brand-gold-dark)`.
- `--color-text: #000000` (`:37`) on cream and `#ffffff` on navy: both are harsher than the palette. Navy text `#0b1528` in light and `#e8edf7` in dark keeps >15:1 and matches the brand.
- `.btn-primary` shadows use `hsla(207, 90%, 52%)` (`:864`, `:868`), the previous blue; use `hsla(222, 83%, 53%, .3)` to match `#2463eb`.
- `.hero-gradient-usda`, `.aaai-hero`, `.conference-banner`, `.foreclosure-*`, `.glossary*`, `.publication-card`, `.stats-bar`, `.who-we-are`, `.principle-grid`, `.breadcrumb`, `.who-profiles` (`:557-563`, `:1061-1133`, `:1164-1201`, `:912-1033`) are unused by any page in this repo. Roughly a third of the stylesheet is for the research site. Not urgent, but a `scripts/unused_css.py` pass before the next redesign would make the file reviewable.
- `motion`: `.card`, `.service-card`, `.btn`, `#back-to-top` all animate transform; there is no `@media (prefers-reduced-motion: reduce)` block. Add one that sets `transition: none; animation: none; scroll-behavior: auto`.

---

## Media and logo findings

Rules for every replacement, so the next step (prompt writing) has one spec: no baked-in text, logos, statistics or badges; no generator watermark (several current files carry a four-point sparkle in the lower right); edges must read on both cream `#fcf8f3` and navy `#0b1528`, which means either a transparent/flat background that the CSS figure box colours, or a photograph with mid-tone edges and no pure-white or pure-black border; corners are applied by CSS (`var(--radius)` 16px), so deliver square; export WebP (and AVIF where small) at the sizes given, with a JPG only for Open Graph. People in photos must be real staff or clearly generic (no faces that imply a client or candidate).

### index.html
| Image | Where | What is wrong | Replacement must achieve |
|---|---|---|---|
| none (gradient `.cloud-hero-bg`) | hero | The homepage has no photograph, place or person. `images/hero-banner.webp` (3584x1184) and `hero-splash.webp` (3200x1312) exist for this slot (`.hero-bg`, `style.css:1426`) but neither is used, and both are unusable: they carry a baked badge "TEXAS CLOUD FRONTS - CENTRAL TEXAS TECHNOLOGY PARTNERSHIP" (not the company name), an Austin skyline (the company serves Bell County and the Killeen-Temple corridor), a grey/beige band along the bottom edge, and a generator sparkle in the corner. | Subject: a Central Texas small-business street or storefront at golden hour, or the two founders at work with a client, wide, with quiet space on the left third for the headline. Mood: warm, local, early evening; a little sky for the "cloud" idea without literal cloud icons. Ratio 3:1 (3600x1200) for the band plus a 16:9 crop for mobile. Must sit under the existing navy overlay (`.hero-image::before`, `style.css:593-597`) and still read, so mid-tone, not high-key. Sits on navy in both modes. |
| `favicon.svg` as `og:image` | share previews | SVG is not rendered by Facebook, X or LinkedIn; the home, service, about and contact pages share with no image. | A 1200x630 JPG (<=250 KB) "og-default": the wordmark on cream with a Central Texas photo strip or the hero photo with the wordmark in the corner. Same artwork must be legible at 300px wide. |

### domain-names.html
| Image | Where | What is wrong | Replacement must achieve |
|---|---|---|---|
| `images/domain-names-opener.png` (1536x1024, 2.4 MB) | top, `.featured-image` (undefined) | AI stock: glowing globe ringed with TLD pills (".co" appears twice), a "99%" check badge (an invented statistic), orbit lines and sparkle. Dark navy background becomes a slab on cream and vanishes on navy. Unoptimised PNG with `loading="lazy"` above the fold. Alt "Domain Registration Concept" is meaningless. | Subject: a local business's name made physical: a shop sign, a van door, a business card being handed over, or hands typing a name into an address bar on a laptop in a real office. Mood: calm, daylight, warm wood/cream tones with one brand-blue accent. 2:1 (1600x800), WebP <=180 KB. Mid-tone edges so the 16px CSS frame works on cream and navy. Alt: describe the scene. |

### about-us.html (and team.html, same files)
| Image | Where | What is wrong | Replacement must achieve |
|---|---|---|---|
| `images/scott-weeden.webp` (1824x2294, 231 KB) | founder card, 180px circle | Portrait studio headshot, grey gradient backdrop, navy shirt, red tie. The file carries the same lower-right generator sparkle as the AI hero art, so it may be generated or AI-retouched. Cropped by `object-fit: cover` to the centred square: head top clips, face ~60px of the 180px circle. 10x oversize for the slot. | A real photograph of Scott (Owner decision confirms). Square 800x800, eyes at ~40% from the top, shoulders in, soft neutral or warm environmental background (an office, a client's shop) rather than studio grey so it feels local. Consistent light and lens between the two founders. WebP <=60 KB. Works inside a 3px `--card-border` ring on white (light) and `#111f38` (dark). |
| `images/johnathan-king.webp` (1824x2294, 423 KB) | founder card | Same issues: studio grey/beige blur, sparkle watermark, centred-square crop, 423 KB for 180px. Lighting and background differ from Scott's, so the pair looks like two different photo shoots. | Same spec as above, shot in the same session. |
| unused: `scott-douglas-weeden.png` (718x606), `johnathan-casey-king.jpeg` (2774x2078) | not referenced | Candid real photos (grocery delivery with a visible H-E-B logo; yard work). Warm and human but not usable: trademark in frame, casual dress, low resolution, landscape. | If the owners want candid "we show up in person" photos for the about page, reshoot: same two people, in a client's premises, no third-party trademarks, 3:2, 1800x1200. |

### contact.html
No image. Fine as is. If a photo is added, use the same 800x800 founder crops at 96px beside the direct-contact lines so the people you are emailing have faces.

### blog.html and blog/welcome-to-the-cloud-fronts-group-blog.html
| Image | Where | What is wrong | Replacement must achieve |
|---|---|---|---|
| `images/hero-og.png` (2848x1504, 6.0 MB) | post hero, blog card, `og:image` for the post | Texas county map in gold with two network-node "clouds" and light rays, navy-to-gold gradient, a flat grey bar across the bottom ~8% of the frame and a sparkle watermark in it. Decorative but says nothing about the post ("Welcome"). `image_alt` says "clouds over a Central Texas skyline", which is not what is shown. 6 MB PNG served to phones; `hero-og.webp` (178 KB) exists unused. | For this post: the founders or the office, or a Central Texas scene, 1.91:1 (1200x630) JPG <=250 KB for OG plus WebP for the page, no bottom bar, no watermark, nothing baked in. Mood: warm, open, the same photographic family as the homepage hero so the brand is one thing. Must read as a 350px card thumbnail on cream and on `#111f38`. Alt must describe the actual content. |
| (policy) | future posts | `_layouts/post.html:16` hardcodes `width="1200" height="630"`; any non-1.91:1 image will distort the layout reservation. | Standardise every post image to 1200x630 and document it in `docs/blog-authoring.md`. |

### Other service pages (same figure system; listed so the media step is complete)
| Page | Image | What is wrong | Replacement must achieve |
|---|---|---|---|
| logo-design.html | `before-after-logo.webp` (700x340) top, `.img-service-bot` | A four-panel infographic labelled "Case Study 1-4: Identity Transformation, UX Overhaul, Performance Metrics, Scalability" with before/after logos, a fake storefront and analytics charts. It implies client case studies that do not exist, in a flat grey style unrelated to the palette; 700px wide, displayed at 700px (soft). | Real logo work by Cloud Fronts with client permission, or a neutral process shot: sketches, pencil, swatches, a laptop with a vector mark in progress, no readable brand names. 2:1, 1600x800. Mood: craft, daylight, cream paper. |
| logo-design.html | `service-logo-design.webp` (233x428) mid, `.img-service-center` | A vertical slice of the same infographic with cut-off captions at the top ("Pre-optimize (low traffic) / 74% in i..."): fabricated metrics, a "C" hexagon placeholder logo. `width:100%` stretches 233px to 700px (3x upscale) and ~1290px tall. | Remove. If a mid-page figure is wanted: 3:2, 1400x933, a single logo application (sign, card, vehicle) in warm light. |
| web-design-hosting.html | `mockup-website.webp` (708x214) top | A stitched strip: six generic logo samples on the left (with AI misspellings "EMBLAM", "MIHIAIALIT") and a monitor/phone "Modern Portfolio" mock on the right. Not Cloud Fronts' work; low resolution; wrong subject for a web-design page (half of it is logos). | A real site built by Cloud Fronts on a laptop and phone, held or on a desk, screen content soft-focused if permission is not granted, 2:1, 1600x800. |
| web-design-hosting.html | `service-web-design.webp` (233x428) mid | Vertical infographic slice with cut captions ("After / 95% reduction in latency"), a laptop line-icon and an analytics dashboard icon; stretched 3x. | Remove, or 3:2 process shot (whiteboard wireframe, browser dev tools on screen). |
| design-print-agency.html | `mockup-print.webp` (354x214) top | Crop of an infographic panel; a stray caption "Logo Examples/Mockups" is cut along the top edge and "Print Samples" along the bottom; grey studio mock of a tri-fold and cards with the placeholder "C" logo; 354px upscaled to 700px. | Real printed pieces Cloud Fronts produced (brochure, cards, banner) on a cream table, overhead, 2:1, 1600x800, warm light. |
| promotional-items.html | `mockup-apparel.webp` (354x214) mid | Same infographic family: "Website Screenshots" caption cut off at top, "Product Branding Examples" at bottom, mug/pen/hoodie with the "C" logo, sparkle watermark lower right; upscaled 2x. | Real branded merch (shirt, cap, mug, pen) with a client's permission or with blank/neutral marks, 3:2, 1400x933, on cream. |
| site-hosting.html | `site-hosting-opener.avif` (2000x1121, 197 KB) top | Isometric pale-blue factory-city illustration with cartoon clouds. Generic "tech" clip art; white background becomes a bright slab in dark mode; alt "Cloud Hosting Infrastructure" is accurate but the picture has nothing to do with hosting a local business's site. Of the current set, it is the closest to the pastel palette. | A believable reality: a small-business owner's site open on a tablet at their counter, or a tidy rack/NAS in a small office if the owners actually host, 2:1, mid-tone background. |
| marketing.html | `marketing-opener.png` (3119x1787, 196 KB) top | An IoT/edge-analytics architecture diagram ("Devices / Sensors, Gateways / Edge Analytics, Core Analytics, Client Applications / micro-services"). Entirely unrelated to marketing; white background; alt "Marketing Strategy Desk" is false. | A planning scene: founders and a client at a table with a printed plan, sticky notes, or a phone showing a local business's social page, 2:1, warm. |
| political-advertisements.html | `political-advertisements-opener.jpg` (1600x900, 159 KB) top | A pink/peach watercolour "Digital Marketing Strategy Notebook" checklist graphic. Nothing political, off-palette (salmon), alt "Campaign Advertising Mockup" is false. The campaign-themed image that fits this page is currently on the PPC page (`pay-per-click-marketing-mid.png`). | Non-partisan campaign materials with no candidate name or face: yard-sign blanks, a mailer stack, a door-hanger, red/white/blue kept muted so it sits with navy and cream, 2:1. |
| pay-per-click-marketing.html | `pay-per-click-marketing-opener.png` (1536x1024, 2.6 MB) top | A flat-lay with "Content Calendar", "Swipe File", a phone showing a "VOTE" post and sticky notes "Launch / Engage / Spotlight": this is a social-media/political image, not PPC. Alt "PPC Ads Dashboard" is false. 2.6 MB PNG. | A real ads dashboard (numbers blurred or generic) on a laptop beside a notebook, or a phone with a search result and a sponsored tag, 2:1, <=200 KB. |
| pay-per-click-marketing.html | `pay-per-click-marketing-mid.png` (1536x1024, 2.7 MB) mid | "SMITH VICTORY 2026" campaign-desk illustration with a fictional candidate's face on a phone and mailer, a "99%" badge, a US flag. Wrong page (political), fabricated candidate, 2.7 MB. Alt "Retargeting and Conversion" is false. | Move the concept, not the file, to political advertisements with the spec above; for PPC mid-page use a 3:2 chart-on-screen or budget-conversation photo. |
| social-media-marketing.html | `social-media-marketing-opener.avif` (626x626, 26 KB) top | Stock vector of a paper-cut light bulb over business doodles with the template's own caption "VECTOR ILLUSTRATION" still in the corner. Square image used as a landscape opener (full width, 626px upscaled to 1096px); grey-white background; alt "Social Media Dashboard" is false. | A phone in hand showing a local business's feed (generic UI, no real brand), café or shop background, 2:1, 1600x800, warm. |
| social-media-marketing.html | `social-media-marketing-mid.png` (1536x1024, 2.6 MB) mid | Document-scanning illustration (filing cabinet -> scanner -> cloud folders "Contracts, Invoices, HR", slow/fast gauges). It is the Document Management picture, on the wrong page; alt "Content Calendar and Strategy" is false. | Move to `document-management.html` (which has no image) after re-export at 2:1 WebP <=200 KB and a correct alt; the scanner/cabinet concept is right for that page though the style is glossier than the palette. For social-media mid-page, a 3:2 content-calendar flat-lay in brand colours. |
| document-management.html | none | Text-only page; the matching illustration is on the social page. | See above: 2:1 opener, paper-to-screen concept, mid-tone background. |
| online-publishing.html | none | Text-only page. | 2:1 opener: a printed newsletter or magazine spread next to the same piece on a tablet, cream paper, warm light. |
| 404.html | none | Fine. | None needed. |

### Logo and favicon (every page)
| Asset | What is wrong | Replacement must achieve |
|---|---|---|
| Header wordmark: Lucide `cloud` outline + "Cloud Fronts" + blue "Group" (`_includes/header.html:6`) | A generic icon-font glyph is not a logo; it also appears in hundreds of other products. "Group" in blue splits the name. It is not a link. | A proper mark: an SVG wordmark in Outfit 800 with a bespoke cloud-front (weather-front line meeting a cloud) glyph, delivered as `logo.svg` (navy on transparent for cream) and `logo-dark.svg` (white/cream on transparent for navy), ~160x32 at rest, 28px tall in the header. One colour per variant, no gradients. |
| `favicon.svg` | Old palette (`#003a70` square, `#f0ab00` cloud) with "CF" in white overlapping the cloud; at 16-32px the letters collide with the shape. `theme-color` matches this old blue, not the site. | A 64x64 SVG reduction of the new glyph (just the cloud-front shape) in navy on cream and a transparent variant for dark tabs; `rx` 12. Also export `apple-touch-icon.png` 180x180. |
| `hero-banner.*`, `hero-splash.*` "TEXAS CLOUD FRONTS" badge | A different brand name on a hero file in this repo. | Delete or move out of `images/`; if "Texas Cloud Fronts" is a real sister brand, it needs its own page and a footer mention, not a hidden banner. |
| Unused assets shipped to `_site/images/`: `headshot-aisha/david/michael/sarah.*` (354x170 crops of a persona sheet: "Sarah P. Mid-30s, Professional office"), `service-brand-identity.*`, `hero-og.webp`, `before-after-logo.png` and other PNG twins | Dead weight and, in the persona crops, obviously fake people with captions. Anyone browsing `/images/` sees them. | Remove from the repo or add `images/unused/` to `exclude:` in `_config.yml`. |

---

## Next (up to 5)
1. **Service cards**: flex column with bottom-aligned buttons and 2.2rem SVG icons; two columns between 600 and 1024px; consistent "Learn more" labels (editor).
2. **Homepage sidebar**: replace the float with a full-width `.callout` band after the services; define or drop `btn-accent`; fix `--font-heading`.
3. **Dark mode polish**: borders on `.cta-banner` and `.post-cta`; fix the invalid `th` rule; `--header-nav-hover` for dark; a `prefers-reduced-motion` block.
4. **Button variants**: `.btn-gold:hover` navy text; `.btn-teal` navy text (fixes the 404 button); update `.btn-primary` shadow hue.
5. **Nav IA**: one Services menu (or two outcome-named groups), `active` keys on service pages, chevron icon instead of "▼", 44px header controls, scrollable mobile panel with `aria-expanded`.

## Someday
- Navy text instead of pure black/white; a brand-blue `h2` accent instead of invisible gold.
- Featured-post layout for the blog index once there are 3+ posts; tag labels from `_data`.
- Prune the research-site CSS (about a third of `style.css`) once the other-interest site has its own stylesheet.
- Real photography day: founders, office, two or three client premises (with permission), shot to the specs above, so every page draws from one photographic family.

## Owner decisions
1. **Statistics on the homepage** (`index.html:29-46`): "50+ Projects Completed", "30+ Satisfied Clients", "20+ Ongoing Projects", "100% Satisfaction Guarantee". These must be verifiable or removed. The site rules forbid invented statistics; I did not add any and recommend removing the block unless each number has a source.
2. **Founder photos**: confirm `scott-weeden.webp` and `johnathan-king.webp` are real photographs of Scott Weeden and Johnathan King. If they are generated or heavily retouched, replace them; the role of this site depends on real faces.
3. **Hero copy** ("Scalable Cloud Solutions", "digital infrastructure"): hand to the Site Content Editor to rewrite around web design, logos, marketing, Central Texas, no long-term contracts, and the phone number.
4. **One logo**: choose a mark and retire the other two (Lucide cloud, "CF" favicon, "Texas Cloud Fronts" badge). Decide whether "Texas Cloud Fronts" is a brand that should exist on this site at all.
5. **Service area imagery**: Killeen/Temple/Bell County scenes versus the Austin skyline currently in the unused banners.
6. **Contact details**: publish hours, service area and (optionally) a mailing address; confirm the "1 business day" promise.
7. **Newsletter**: keep the Formspree "Stay Updated" box only where it makes sense (blog, about), or remove it; its copy currently describes the research site.
8. **Menu structure**: approve a single Services menu or two outcome-named groups.
9. **Case-study and before/after imagery**: either obtain client permission to show real work or use process photography; no implied portfolios.

# VS_CHAT_CONTEXT.md — Vegas Sidekick Internal Briefing

**As of:** June 9, 2026  
**Purpose:** Give an AI assistant with no codebase access a complete, accurate picture of the project state.

---

## What This Site Is

Vegas Sidekick (`vegassidekick.com`) is a static affiliate site for Las Vegas show ticket discovery. Revenue model: affiliate commissions via Spotlight.Vegas ticket links. No e-commerce, no user accounts, no backend. The founder is **Kris Kidd**, who lives in Las Vegas.

**Taglines:** "Biggest Shows. Real Discounts. No BS." (primary) · "Vegas Without The Trauma." (alternate)  
**Mascot:** Spike (a character with multiple image assets: spike-wink.png, spike-point.png, etc.)  
**Trust brand:** "Sidekick Standards" — no fake timers, no fake reviews, clear ticket details, no email walls.  
**Email list brand:** "Spike's Insider List" (Brevo, List ID: 2, ~4,200 subscribers per copy)

---

## Tech Stack

| Layer | What's Used |
|---|---|
| Hosting | Cloudflare Pages (static), auto-deploys on push to `main` |
| Serverless | Cloudflare Workers (`functions/api/auth.js`) |
| CMS | Decap CMS v3 at `/admin/` (GitHub-backed) |
| Search | Algolia InstantSearch v4, index `vegas_shows` |
| Email | Brevo via Cloudflare Worker endpoint |
| Auth | GitHub OAuth (CMS admin only) |
| Analytics | GA4 (`G-BM6QGF7B4Y`) — behavioral; Cloudflare Pages — raw traffic (dashboard, no code) |
| Affiliate | Spotlight.Vegas (`ref/vegassidekick`) |
| Image CDN | Cloudinary (`dvhunpinz`) — OG/social images only |
| Fonts | Google Fonts: Bebas Neue, Barlow, Barlow Condensed, IBM Plex Mono |

**No npm, no build step, no bundler.** All third-party libs load from CDN. CSS lives inline in `<style>` blocks in each HTML file — no shared stylesheet.

---

## Deploy & Push Workflow

- **Deploy:** Push to `main` → Cloudflare Pages auto-deploys. No build commands.
- **Git push is blocked** in the remote Claude Code environment (proxy returns 403). File pushes go through the GitHub MCP API instead — see CLAUDE.md for the Python snippet.
- After every MCP push, sync local: `git fetch origin main && git reset --hard origin/main`
- Cloudflare Worker deploys separately via Cloudflare dashboard (apart from the Cloudflare Pages static deploy).

---

## Repository Structure (Complete)

```
vegas-sidekick/
├── admin/
│   ├── index.html              # Decap CMS UI
│   └── config.yml              # CMS field definitions (News collection)
├── components/
│   ├── header.js               # Site nav — injected into #vs-header
│   └── footer.js               # Email signup + footer links — injected into #vs-footer
├── functions/
│   └── api/
│       └── auth.js             # GitHub OAuth handler (Cloudflare Worker)
├── images/                     # All static images (logos, heroes, mascot, news/)
│   └── news/                   # CMS-managed article images
├── shows/
│   ├── index.html              # "All Shows" listing page
│   ├── adult/                  # 4 show pages
│   ├── cirque/                 # 5 show pages
│   ├── comedy/                 # 10 show pages
│   ├── family/                 # 3 show pages
│   ├── magic/                  # 9 show pages
│   ├── music/                  # 4 show pages
│   └── spectaculars/           # 3 show pages
├── news/
│   ├── index.html              # Vegas Dispatch archive/grid
│   └── {slug}/index.html       # 15 individual articles
├── search/
│   └── index.html              # Algolia search UI
├── about/
│   ├── index.html              # About Vegas Sidekick
│   └── kris-kidd/index.html    # Kris Kidd bio page
├── contact/
│   └── index.html
├── privacy/
│   └── index.html
├── terms/
│   └── index.html
├── affiliate-disclosure/
│   └── index.html
├── mom/                        # Password-protected surprise page
├── preview/                    # Password-protected redesign preview
├── index.html                  # Homepage
├── 404.html
├── sitemap.xml
├── _redirects                  # Cloudflare Pages routing (5 rules)
├── CLAUDE.md                   # Full developer guide (read this first)
└── SHOW-BUILDER-PROMPT.md      # Show page creation guide + canonical template reference
```

---

## Design System

### Colors (CSS Custom Properties)
```css
--navy:   #0A1628   /* Primary background */
--blue:   #1A6BFF   /* Secondary accent, links */
--orange: #FF6B2B   /* Primary CTA buttons */
--white:  #FFFFFF
```
Each show page also defines `--show` and `--show-lt` for per-show accent colors (e.g., crimson for V, gold for Jabbawockeez).

### Typography
- Headlines: **Bebas Neue**
- Body: **Barlow** (400/600/700)
- Labels/callouts: **Barlow Condensed** (700/800)
- Mono/meta: **IBM Plex Mono** (show pages only)

### Breakpoints
- Desktop → Tablet: `900px`
- Tablet → Mobile: `480px`

### Visual Language
- Dark navy theme throughout
- Orange for primary CTAs, Blue for secondary
- Starfield background (CSS radial-gradient)
- Glassmorphism cards (`backdrop-filter: blur`)
- Animations: `fadeUp`, `fadeIn`, `float`, `ctaPulse`, `shimmer` (on CTA buttons)
- `@media (prefers-reduced-motion: reduce)` disables Ken Burns + ticker animations

---

## Components (Reusable)

### `components/header.js`
Injected into `<div id="vs-header"></div>`. Includes site nav, logo, mobile hamburger drawer. Requires the placeholder div at top of `<body>` and the script at bottom of `<body>`.

**Nav links (desktop):** Comedy · Magic · Cirque · Music · Spectaculars · Family · Dispatch · All Shows  
**Nav links (mobile-only):** Adult Shows  
**Global function:** `vsToggleMenu()`  
**Also injects:** Google Analytics GA4 tag, July 4th weekend countdown banner (conditional, date-aware)

### `components/footer.js`
Injected into `<div id="vs-footer"></div>`. Email signup form + link columns + Sidekick Standards trust strip.

**Email integration:** POSTs to `https://brevo-subscribe.vegassidekickcom.workers.dev`  
**Brevo List ID:** `2`  
**Global function:** `vsSubmitEmail()`  
**Also fires:** Post-affiliate-click email overlay (triggered when user clicks any `spotlight.vegas` link)

**Footer link columns:**
- *Shows:* Comedy · Magic · Cirque & Acrobatic · Music & Variety · Spectaculars · Family · Adult · Search All
- *Vegas Sidekick:* Dispatch · About · About Kris Kidd · Contact · Affiliate Disclosure · Privacy · Terms

---

## Show Pages — Full Inventory (38 Total)

### Template & Standard

**Canonical template:** `shows/family/v-the-ultimate-variety-show/index.html` — this is the reference for all new show pages. Copy it, don't use older pages.

**Affiliate link format:** `https://spotlight.vegas/shows/{spotlight-category}/{spotlight-slug}/ref/vegassidekick`

> Note: The Spotlight category in the URL often differs from the VS site category. See mapping below.

---

### COMEDY (10 shows)

| VS Slug | Spotlight URL |
|---|---|
| `comedy/carrot-top` | `comedy/carrot-top` |
| `comedy/brad-garretts-comedy-club` | `comedy/brad-garretts-comedy-club` |
| `comedy/comedy-cellar` | `comedy/comedy-cellar` |
| `comedy/la-comedy-club` | `comedy/la-comedy-club` |
| `comedy/las-vegas-live-comedy-club` | `comedy/las-vegas-live-comedy-club` |
| `comedy/laugh-factory` | `comedy/laugh-factory` |
| `comedy/marc-savard-comedy-hypnosis` | `comedy/marc-savard-comedy-hypnosis` |
| `comedy/marriage-can-be-murder` | `comedy/marriage-can-be-murder` |
| `comedy/popovich-comedy-pet-theater` | `comedy/popovich-comedy-pet-theater` |
| `comedy/tape-face` | `comedy/tape-face` |

### MAGIC (9 shows)

| VS Slug | Spotlight URL |
|---|---|
| `magic/allstars-of-magic` | `magic/allstars-of-magic` |
| `magic/colin-cloud` | `magic/colin-cloud` |
| `magic/criss-angel` | `magic/criss-angel` |
| `magic/mac-king` | `magic/mac-king` |
| `magic/mat-franco` | `magic/mat-franco` |
| `magic/nathan-burton-comedy-magic` | `magic/nathan-burton-comedy-magic` |
| `magic/penn-and-teller` | `magic/penn-and-teller` |
| `magic/shin-lim` | `magic/shin-lim` |
| `magic/the-mentalist` | `magic/the-mentalist` |

### CIRQUE (5 shows) — Spotlight category: `cirque-du-soleil`

| VS Slug | Spotlight URL |
|---|---|
| `cirque/ka` | `cirque-du-soleil/ka` |
| `cirque/mad-apple` | `cirque-du-soleil/mad-apple` |
| `cirque/michael-jackson-one` | `cirque-du-soleil/michael-jackson-one` |
| `cirque/mystere` | `cirque-du-soleil/mystere` |
| `cirque/o` | `cirque-du-soleil/o` |

### MUSIC (4 shows) — Mixed Spotlight categories

| VS Slug | Spotlight URL |
|---|---|
| `music/blue-man-group` | `production/blue-man-group` |
| `music/jabbawockeez` | `production/jabbawockeez` |
| `music/rupauls-drag-race-live` | `production/rupauls-drag-race-live` |
| `music/vegas-the-show` | `music/vegas-the-show` |

### FAMILY (3 shows)

| VS Slug | Spotlight URL |
|---|---|
| `family/battlebots-destruct-a-thon` | `production/battlebots` |
| `family/tournament-of-kings` | `production/tournament-of-kings` |
| `family/v-the-ultimate-variety-show` | `family/v-the-ultimate-variety-show` |

### ADULT (4 shows)

| VS Slug | Spotlight URL |
|---|---|
| `adult/absinthe` | `production/absinthe` |
| `adult/magic-mike-live` | `adult/magic-mike-live` |
| `adult/rouge` | `adult/rouge` |
| `adult/thunder-from-down-under` | `adult/thunder-from-down-under` |

### SPECTACULARS (3 shows)

| VS Slug | Spotlight URL |
|---|---|
| `spectaculars/awakening` | `production/awakening` |
| `spectaculars/wizard-of-oz` | `production/the-wizard-of-oz-at-sphere` |
| `spectaculars/wow-the-vegas-spectacular` | `production/wow-the-vegas-spectacular` |

---

## Show Page Structure (Canonical "Sidekick Build" Template)

Every show page built on the canonical template includes these sections in order:

1. **Dual scroll progress bars** — one fixed top, one in sidebar
2. **Hero section** — breadcrumb + Ken Burns image slider (3 images, 16:9, 5s auto-advance) + venue/title block + price strip
3. **Scrolling ticker** — show-color background, repeating facts/quotes
4. **Stats strip** — count-up animation via IntersectionObserver + requestAnimationFrame
5. **Two-column layout:** `main.main-content` (left) + `aside.sidebar` (right, sticky, navy bg)
6. **Mobile sticky buy bar** — fixed bottom, hidden on desktop
7. Main content sections:
   - `.seen-widget` — "Have you seen this show?" yes/no engagement widget
   - `.trust-grid` — 4 trust cards (secure booking, instant delivery, no fees, no account)
   - About section with `.spike-callout` (show-color left-border callout, Spike's take)
   - `.email-signup` — accent bar + inline Brevo email form
   - `.details-grid` — 3-col icon cards (venue, schedule, duration, age, etc.)
   - `.expect-grid` — 2-col "What to Expect" cards
   - `.seating-section` — interactive SVG seating chart + `.zone-popup` + `.seat-accord` (accordion zones)
   - `.faq-list` — accordion FAQ (+ icon toggle)
   - `.also-grid` — 3 "You Might Also Like" show cards (hardcoded, not dynamic)
   - `.final-cta` — dark gradient CTA card inside `<main>` (with ambient orbs), not full-width

**Sidebar** (sticky, right column): price display, CTA button, show details, trust badges, email signup

**Show accent colors:** `--show` and `--show-lt` CSS vars per page drive all accent elements (ticker bg, callout border, stat highlights, etc.)

**Seating chart:** Interactive SVG, clickable zones call `selectZone('id')`, populates `.zone-popup` below with zone name, description, and optional "Sweet Spot" badge (the Sidekick's recommended zone).

**Image slider:** Ken Burns pan/zoom animations on hero images, 3-image carousel, pauses on interaction.

---

## News / Vegas Dispatch

**15 published articles** in `/news/{slug}/index.html`

| Slug | Headline | Date |
|---|---|---|
| `bini-signals-world-tour-august-8` | BINI Brings Coachella Breakout to Vegas — Aug 8 | 2026-04-25 |
| `soda-stereo-ecos-september-13` | Soda Stereo ECOS — Dolby Live, Sept 13 | 2026-05-04 |
| `eagles-sphere-additional-shows-2026` | Eagles Add Six More Sphere Shows — 64 Dates | 2026-05-05 |
| `jay-silent-bob-save-vegas-october-16` | Jay & Silent Bob Save Vegas! — The Venetian, Oct 16 | 2026-05-05 |
| `live-nation-las-vegas-listings-update-may-2026` | Live Nation LV: Major New Announcements — May 7 | 2026-05-07 |
| `matt-rife-stay-golden-dolby-live-december-4` | Matt Rife Stay Golden — Dolby Live, Dec 4 | 2026-05-12 |
| `blue-dot-fever-what-it-means-for-vegas` | Blue Dot Fever: What Concert Cancellations Mean for Vegas | 2026-05-10 |
| `new-shows-announced-may-14-2026` | New Shows: Eagles, KATSEYE, Matt Rife & More | 2026-05-14 |
| `tumua-das-how-tour-venetian-october-9` | Tumua — Das' How Tour, The Venetian, Oct 9 | 2026-05-18 |
| `for-king-country-pearl-palms-october-8` | for KING + COUNTRY — The Pearl at Palms, Oct 8 | 2026-05-18 |
| `clay-walker-venetian-december-5` | Clay Walker — The Venetian, NFR Weekend, Dec 5 | 2026-05-18 |
| `smashing-pumpkins-rats-in-a-cage-tour-mgm-grand-october-30` | Smashing Pumpkins — MGM Grand, Oct 30 | 2026-05-18 |
| `lewis-black-live-venetian-october-30` | Lewis Black Live — The Venetian, Oct 30 | 2026-05-19 |
| `marco-antonio-solis-tour-gratitud-dolby-live-september-11` | Marco Antonio Solís — Dolby Live, Sept 11–12 | 2026-05-19 |
| `new-shows-announced-may-19-2026` | Five New Shows Announced — May 2026 | 2026-05-19 |

**Article structure:** JSON-LD `NewsArticle` schema, breadcrumb nav, hero image, OG/Twitter meta, Brevo email form, author: Kris Kidd.

**Publishing workflow (4 files per article):**
1. Create `news/{slug}/index.html`
2. Update `news/index.html` — promote new article to featured, add to grid
3. Update `index.html` — Vegas Dispatch section (3-card grid)
4. Update `sitemap.xml`

**OG images:** Must be real hosted URLs (Cloudinary) — data URLs don't work for social crawlers. Kris uploads via Cloudinary mobile, pastes URL back for `og:image` / `twitter:image` tags.

---

## CMS (Decap, `/admin/`)

- Backend: GitHub, repo `VegasSidekick/vegas-sidekick`, branch `main`
- Auth: GitHub OAuth via Cloudflare Worker at `/api/auth`
- Media: `images/news/` (public: `/images/news/`)
- Collection: **News Articles**
  - Fields: title, date, category (select), image, image_credit, description, body (markdown), ticket_url, ticket_price, show_date, venue

---

## External Services & Keys

| Service | Key/ID | Notes |
|---|---|---|
| Algolia | App ID: `E402SBJE6D` | Search-only key in `search/index.html` |
| Brevo | API Key in `footer.js` | List ID `2`, restricted scope |
| Brevo Worker | `https://brevo-subscribe.vegassidekickcom.workers.dev` | Used for all email signups |
| GitHub OAuth | Client ID: `Ov23lit31UqvtSuPp7tJ` | Client secret in Cloudflare env var only |
| GA4 | `G-BM6QGF7B4Y` | Injected via header.js — behavioral analytics |
| Cloudflare Analytics | (dashboard) | Built into Cloudflare Pages — raw traffic, no code required |
| Cloudinary | Cloud: `dvhunpinz`, API Key: `966995363786296` | Secret in `.cloudinary` (gitignored) |
| Spotlight.Vegas | Ref code: `vegassidekick` | Affiliate ticket partner |

**Image upload constraint:** Binary images cannot be pushed via the MCP API (corrupts files). Embedded page images use WebP data URLs. OG/social images use Cloudinary URLs. Binary image uploads go through the GitHub web UI.

---

## Image Handling

**Embedded images (in-page):**
1. Convert: `cwebp -q 70 photo.jpg -o photo.webp`
2. Data URL: `python3 -c "import base64; print('data:image/webp;base64,' + base64.b64encode(open('photo.webp','rb').read()).decode())" > dataurl.txt`
3. Use as `src` attribute inline

**Size targets:**
- Card thumbnails: `-q 65`, target <60KB binary (~80KB as data URL)
- Article heroes: `-q 75`, target <100KB binary (~133KB as data URL)
- MCP payload limit: ~500KB per push — keep HTML file under this

**OG images:** Cloudinary-hosted, real URL. Kris uploads, pastes URL, Claude updates `og:image` / `twitter:image` meta.

---

## Page Template Rules

Every page must have:
```html
<body>
<div id="vs-header"></div>   <!-- header injection point -->
<!-- page content -->
<div id="vs-footer"></div>   <!-- footer injection point -->
<script src="/components/header.js"></script>
<script src="/components/footer.js"></script>
</body>
```

Image paths are **root-relative** (`/images/filename.jpg`) — pages live in subdirectories.

---

## Known Gaps & Open Items

1. **Algolia index not auto-synced** — adding a show page doesn't update the search index. Must be manually populated via Algolia dashboard or API.
2. **No category landing pages** — `/shows/comedy/`, `/shows/magic/`, etc. don't exist as curated pages; those URL paths would 404 unless Cloudflare Pages routing or `shows/index.html` handles them. Header nav links to them — worth verifying these routes.
3. **`also-grid` show cards are hardcoded** — "You Might Also Like" on each show page points to 3 hand-picked shows. Not dynamic.
4. **SVG seating charts are per-page** — each show has a custom hand-drawn SVG. Not pulled from any shared source.
5. **Ticker content is hardcoded** — show-specific, must be updated manually per page.
6. **No pagination on news index** — at some point `/news/index.html` will need it (currently 15 articles).
7. **Sitemap requires manual updates** — new pages must be added by hand.

---

## Naming Conventions

| Thing | Convention | Example |
|---|---|---|
| Show page URLs | kebab-case | `carrot-top`, `michael-jackson-one` |
| CSS classes | BEM-adjacent | `show-card`, `btn-primary`, `show-sidebar` |
| CSS custom properties | `--kebab-case` | `--navy`, `--orange`, `--show` |
| Image files | kebab-case with descriptors | `carrot-top-hero.jpg`, `spike-wink.png` |
| Component functions | `vs` prefix camelCase | `vsToggleMenu()`, `vsSubmitEmail()` |
| Branch names | `claude/feature-desc-<id>` | `claude/show-page-buildout-abc123` |
| Commit messages | Imperative, scoped | `Add Michael Jackson ONE show page` |

---

## Git State (as of audit)

- **Primary branch:** `main` (Cloudflare Pages auto-deploys)
- **Active feature branch:** `claude/vegas-sidekick-audit-4naacg`
- **Recent work:** Canonical show template established (`v-the-ultimate-variety-show`), WOW page added, "Sweet Spot" badge system formalized, SHOW-BUILDER-PROMPT.md updated

---

## What's Built vs. What's Not

| Built & Reusable | Not Yet Built |
|---|---|
| 38 show pages (Sidekick Build template) | Category landing pages |
| Shared header/footer components | Auto-Algolia sync |
| Decap CMS for news | Dynamic "also-grid" (related shows) |
| Vegas Dispatch (15 articles + index) | Pagination on news index |
| Algolia search UI (needs index population) | Any server-rendered features |
| Email capture (footer + show pages + post-click overlay) | |
| SVG seating charts (per show, custom) | |
| Brevo email worker | |
| GitHub OAuth for CMS | |
| Sitemap (manual) | |

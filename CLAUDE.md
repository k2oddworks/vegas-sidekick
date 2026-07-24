# CLAUDE.md — Vegas Sidekick Codebase Guide

## Project Overview

Vegas Sidekick (`https://vegassidekick.com`) is a **static website** for Las Vegas show ticket discovery and affiliate booking. It has no backend or build system — all content is plain HTML/CSS/JS files deployed directly.

**Business model:** Affiliate revenue via Spotlight.vegas ticket links.

---

## Repository Structure

```
vegas-sidekick/
├── admin/                  # Decap CMS content editor
│   ├── index.html          # CMS web interface entry point
│   └── config.yml          # CMS collection/field definitions
├── components/             # Reusable JS web components
│   ├── header.js           # Site navigation (injected via script tag)
│   └── footer.js           # Email signup + footer links
├── functions/              # Serverless edge functions
│   └── api/
│       └── auth.js         # GitHub OAuth handler (Cloudflare Workers)
├── images/                 # Static image assets
│   ├── logo-*.png/.jpg     # Logo variants
│   ├── *-hero.jpg          # Show hero images
│   ├── spike-*.png/.jpg    # Mascot (Spike) assets
│   └── news/               # CMS-managed news article images
├── search/
│   └── index.html          # Algolia-powered search page
├── shows/                  # Show detail pages
│   ├── comedy/
│   │   └── carrot-top/index.html
│   └── cirque/
│       └── michael-jackson-one/index.html
├── index.html              # Homepage
├── sitemap.xml             # SEO sitemap
└── _redirects              # Cloudflare Pages routing rules
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Hosting | Cloudflare Pages (static) + Cloudflare Workers (functions) |
| CMS | Decap CMS v3 (GitHub-backed) |
| Search | Algolia InstantSearch v4 |
| Email | Brevo (formerly Sendinblue) |
| Auth | GitHub OAuth (for CMS admin) |
| Fonts | Google Fonts (Bebas Neue, Barlow, Barlow Condensed) |

**No npm, no build step, no bundler.** All third-party libraries are loaded from CDN.

---

## Design System

### Color Palette (CSS Custom Properties)
```css
--navy:     #0A1628   /* Primary background */
--blue:     #1A6BFF   /* Secondary accent, links */
--orange:   #FF6B2B   /* Primary CTA buttons */
--white:    #FFFFFF
--gray-*:   various   /* Text hierarchy */
```

### Typography
- **Headlines:** Bebas Neue (Google Fonts)
- **Body text:** Barlow 400/600/700 (Google Fonts)
- **Labels/Callouts:** Barlow Condensed 700/800 (Google Fonts)

### Responsive Breakpoints
- Desktop → Tablet: `900px`
- Tablet → Mobile: `480px`

### Visual Conventions
- Dark navy theme throughout
- Orange for primary CTAs, Blue for secondary actions
- Starfield background (CSS radial-gradient pattern)
- Glassmorphism on cards (`backdrop-filter: blur`)
- Animations: `fadeUp`, `fadeIn`, `float`, `ctaPulse`

---

## Page Structure Conventions

### Homepage (`index.html`)
All CSS embedded in `<style>` tags. All JS inline at bottom. Components loaded via `<script src="/components/header.js">`.

### Show Detail Pages (`shows/{category}/{show-slug}/index.html`)

**Model/reference page: `shows/adult/absinthe/index.html`**

Absinthe is the design and feature standard for all show pages. When building or updating any show page, consult Absinthe first — every page should be inspired by and consistent with it. Features like info pills (`.info-pills`, `.pill`, `.pill-green`, `.pill-orange`, `.urgency-pills`, `.upill`), the seen-widget behavior, sidebar layout, and mobile-buy-bar are all benchmarked against Absinthe.

**Canonical template: `shows/music/vegas-the-show/index.html`**

This is the standard template for all new show pages — locked in as the reference build. Copy it when building a new show — do not use older pages (including `v-the-ultimate-variety-show`) as a starting point. Key features of the Sidekick Build template:

- Dual scroll progress bars (top + sidebar)
- Hero section: breadcrumb + Ken Burns image slider (`aspect-ratio: 16/9`) + venue/title block + price strip
- Scrolling ticker strip (show-color background) below hero
- Stats strip with count-up animation (`IntersectionObserver` + `requestAnimationFrame`)
- Two-column layout: `main.main-content` (left) + `aside.sidebar` (right, sticky, navy bg)
- Mobile sticky buy bar fixed to bottom (hidden on desktop)
- Main content sections in order:
  1. `.seen-widget` — "Have you seen this show?" yes/no engagement widget
  2. `.trust-grid` — 4 trust cards (secure booking, instant delivery, no fees, no account)
  3. About section with `.spike-callout` (show-color left-border callout)
  4. `.email-signup` — accent bar, inline email form wired to Brevo Worker
  5. `.details-grid` — 3-col icon cards for venue/schedule/duration/age/etc.
  6. `.expect-grid` — 2-col "What to Expect" cards
  7. `.seating-section` — interactive SVG seating chart + `.zone-popup` + `.seat-accord`
  8. `.faq-list` — accordion FAQ (+ icon)
  9. `.also-grid` — 3 "You Might Also Like" show cards
  10. `.final-cta` — dark gradient card CTA inside `<main>` (with ambient orbs), NOT full-width
- Photo gallery section (`.gallery-section` / `.gallery-grid`) placed right after the About section — asymmetric masonry layout (one large image + smaller stacked images), hover zoom, click-to-enlarge
- Serif editorial accent: hero tagline and the About section's opening "lede" paragraph render in italic Cormorant Garamond (`.lede` class) against the site's usual Bebas Neue/Barlow system — import `Cormorant+Garamond:ital,wght@1,500;1,600` alongside the standard fonts
- Fonts: Bebas Neue (display), Barlow Condensed (price/labels), Barlow (body), IBM Plex Mono (meta/mono), Cormorant Garamond italic (editorial accent only — tagline + lede)
- `--show` / `--show-lt` CSS vars drive the show's accent color (e.g. gold for Jabba, crimson for V)
- Ticker: show-color background; text color white (dark shows) or navy (light shows like gold)
- `@media (prefers-reduced-motion: reduce)` disables Ken Burns + ticker animations
- All primary "Get Tickets" CTA buttons (`.hero-cta`, `.sb-cta`, `.mob-cta`, `.final-cta-btn`) share one locked-in treatment: navy text on orange fill, soft light-blue neon border + matching glow (`rgba(96,165,250,...)`), pulsing glow-ring animation (`pulseGlowCta` — animated `box-shadow`, no extra wrapper markup needed), the existing shimmer sweep, and a light-blue bobbing 🎟️ ticket emoji (`.cta-ticket`, hue-rotated + drop-shadow glow, `bobTicket` animation) in place of the plain arrow

The seating chart is an interactive SVG — clickable zones call `selectZone('id')`, which populates a `.zone-popup` panel below with zone name, description, and optional Sweet Spot badge.

**Terminology — do not conflate these two:**
- **"Sweet Spot"** — the recommended *seating section* within a show's venue (e.g. "VIP is the Sweet Spot"). Used in the seating chart's zone popup/accordion badge (`🪑 Sweet Spot`), urgency pills, and FAQ copy about seating.
- **"Sidekick Pick"** — a recommendation of the *entire show* itself (the `sp:true` flag in the `SHOWS` JS arrays on `shows/index.html` and category index pages, and the standalone `🌵 Sidekick Pick` urgency pill with no section name attached). Never append a seating section name to a "Sidekick Pick" label (e.g. never "Sidekick Pick — VIP") — that's a Sweet Spot claim, not a show-level pick.

### URL Pattern for Affiliate Links
```
https://spotlight.vegas/shows/{category}/{show-slug}/ref/vegassidekick
```

---

## Components

### `components/header.js`
Injects the site navigation via `document.currentScript` reference. Includes:
- Logo image
- Desktop nav links: Comedy, Magic, Cirque, Music, Headliners, All Shows
- Mobile hamburger drawer

**Exposed global function:** `vsToggleMenu()` (called by mobile hamburger button)

To include in a page:
```html
<script src="/components/header.js"></script>
```

### `components/footer.js`
Injects footer with email signup and link columns. Integrates with Brevo API.

**Exposed global function:** `vsSubmitEmail()` (called by email form submit button)

To include in a page:
```html
<script src="/components/footer.js"></script>
```

---

## CMS (Decap)

The admin CMS is at `/admin`. It reads/writes content via the GitHub API.

**Config:** `admin/config.yml`
- Backend: `github`, repo `VegasSidekick/vegas-sidekick`
- Media uploads: `images/news/`
- Collection: **News Articles** — fields include title, date, category, image, body, ticket_link, ticket_price, show_date, venue

Authentication is handled by the Cloudflare Worker at `/api/auth`, which implements GitHub OAuth and posts the token back to the CMS via `window.postMessage`.

---

## External Services & Credentials

Credentials are embedded in client-side code (read-only, restricted scope):

| Service | Credential | Location |
|---|---|---|
| Algolia | App ID: `E402SBJE6D`, Search Key in source | `search/index.html` |
| Brevo | API Key in source, List ID: `2` | `components/footer.js` |
| GitHub OAuth | Client ID: `Ov23lit31UqvtSuPp7tJ` | `functions/api/auth.js` |
| GitHub OAuth | Client Secret via `GITHUB_CLIENT_SECRET` env var | `functions/api/auth.js` |
| Cloudinary | Cloud: `dvhunpinz`, API Key: `966995363786296`, Secret: in `.cloudinary` | OG image hosting |

**Note:** The Algolia key is a search-only key and the Brevo key has restricted permissions. The GitHub Client Secret must be stored as an environment variable in Cloudflare Workers — never commit it to the repo.

The Cloudinary API credentials are stored in `.cloudinary` (gitignored). However, server-to-server uploads are blocked by Cloudinary's IP restrictions. The established workflow for OG/social images is:
1. Kris uploads the article image to Cloudinary from his phone (Cloudinary mobile or browser)
2. He pastes the resulting URL (e.g. `https://res.cloudinary.com/dvhunpinz/image/upload/f_auto,q_auto/...`)
3. Claude updates the `og:image` and `twitter:image` meta tags in the article with that URL

This is a one-time step per article and takes ~10 seconds. Article content, in-page images, and all other publishing steps remain fully automated.

---

## Development Workflow

### Adding a New Show Page

1. Create directory: `shows/{category}/{show-slug}/`
2. Copy an existing show page (e.g., `shows/comedy/carrot-top/index.html`) as a template
3. Update all show-specific content: title, description, images, pricing, show times, venue, FAQ
4. Update the affiliate ticket link to `https://spotlight.vegas/shows/{category}/{show-slug}/ref/vegassidekick`
5. Add show images to `images/` directory
6. Add the show to `sitemap.xml`
7. Link the show from the relevant category section on `index.html`

**Image order:** When multiple photos are provided for a new show page, the **first one uploaded/attached is always the hero image** — main hero slide, primary `og:image`/`twitter:image`, first entry in the Event JSON-LD `image` array — unless explicitly told otherwise. Don't guess which photo looks most "hero-like."

**Photo policy (site-wide standard):** On every show page, the photo/camera detail card and the "Can I take photos?" FAQ should use this wording (paraphrase as needed for tone): *"Still photos may be allowed as long as they aren't distracting — please check with your usher on the way in. No flash photography."* Use this even when the source listing (e.g. Spotlight) says cameras are strictly prohibited — this is the Vegas Sidekick default going forward for all shows.

**Sidekick Pick (`sp:true`):** Never set `sp:true` on a new show by default. It stays `sp:false` unless the user explicitly says to mark that specific show as a Sidekick Pick.

### Adding a New Category Page

Currently no category landing pages exist (links go directly to show detail pages). If adding:
- Create `shows/{category}/index.html`
- Update header nav in `components/header.js`
- Update footer links in `components/footer.js`

### Modifying the Header or Footer

Edit the component files directly:
- `components/header.js` — nav links, logo, mobile menu, site-wide announcement banner
- `components/footer.js` — link columns, email signup, Brevo list ID

Changes apply site-wide automatically since all pages load these components.

**Cache-busting is required on every edit.** Both files are referenced with a version query string — `<script src="/components/header.js?v=2"></script>` and `.../footer.js?v=2` — across every page (84 files as of this writing). Browsers cache these scripts per-URL, so without a version bump, users who already loaded an older page won't see header/footer changes until they hard-refresh. Whenever you edit `header.js` or `footer.js`, bump the `?v=` number on **all** pages that reference it (`grep -rl 'header.js?v=' --include="*.html" .` to find them all, then bulk-replace with the next version number). Skipping this step is why a banner or nav change can appear to "work on the homepage but not other pages" — it's stale cache, not a real bug, but it's confusing enough to avoid.

### Deploying

Push to the `main` branch (the repository's default branch). Cloudflare Pages auto-deploys on push. The Cloudflare Worker (`functions/api/auth.js`) must be deployed separately via Cloudflare dashboard or Wrangler CLI.

---

## Naming Conventions

| Thing | Convention | Example |
|---|---|---|
| Show page URLs | kebab-case | `carrot-top`, `michael-jackson-one` |
| CSS classes | BEM-adjacent | `show-card`, `btn-primary`, `show-sidebar` |
| CSS custom properties | `--kebab-case` | `--navy`, `--orange` |
| Image files | kebab-case with descriptors | `carrot-top-hero.jpg`, `spike-wink.png` |
| Component functions | `vs` prefix camelCase | `vsToggleMenu()`, `vsSubmitEmail()` |

---

## Key Gotchas

1. **No build system** — changes to HTML/CSS/JS take effect immediately on deploy. There is no compilation step.
2. **Components are injected JS** — header and footer are injected into the DOM by JavaScript. The header requires `<div id="vs-header"></div>` at the top of `<body>` and the script at the bottom. See Header Component section below.
3. **Script load order matters** — component scripts go at the bottom of `<body>`, after all content. The placeholder divs go at the top.
4. **Image paths are root-relative** — use `/images/filename.jpg` not relative paths, since pages exist in subdirectories.
5. **Sitemap must be updated manually** — add new pages to `sitemap.xml` when creating new show pages.
6. **CSS is all inline** — there is no shared stylesheet. The design system exists as repeated CSS custom properties in each page's `<style>` block.
7. **Algolia index is external** — the search index `vegas_shows` must be populated separately via the Algolia dashboard or API. Adding a show page does not auto-index it.

---

## Image Handling (Critical)

**Binary images cannot be uploaded via the MCP/GitHub tools.** The push tools treat all content as UTF-8 text — passing base64-encoded binary stores the ASCII base64 string as the file, not the decoded image. This corrupts every image uploaded this way.

### The fix: embed images as WebP data URLs in HTML

For images that appear inside HTML pages (article heroes, card thumbnails):
1. Convert to WebP: `cwebp -q 70 photo.jpg -o photo.webp`
2. Generate data URL: `python3 -c "import base64; print('data:image/webp;base64,' + base64.b64encode(open('photo.webp','rb').read()).decode())" > dataurl.txt`
3. Use the data URL as the `src` attribute directly in HTML

**Size targets:**
- Card thumbnails: `cwebp -q 65`, aim for <60KB binary (~80KB data URL)
- Article hero images: `cwebp -q 75`, aim for <100KB binary (~133KB data URL)
- Use `cwebp -size 71680 input.jpg -o output.webp` to hit a specific byte count
- MCP payload limit is ~500KB per push — keep total HTML file under that

**OG/social preview images** require a real hosted file URL (crawlers can't use data URLs). These must be uploaded as binary via the GitHub web interface: `github.com/VegasSidekick/vegas-sidekick/upload/main/images/news` — drag and drop the file directly.

---

## Header Component — Correct Usage

The header component requires **both** of these in every page:

```html
<!-- 1. Placeholder div at the TOP of <body> -->
<div id="vs-header"></div>

<!-- 2. Script tag at the BOTTOM of <body>, before </body> -->
<script src="/components/header.js"></script>
<script src="/components/footer.js"></script>
```

The footer also needs a placeholder:
```html
<div id="vs-footer"></div>
```

`header.js` injects into `#vs-header`. If that div is missing, the nav silently fails to render.

---

## Publishing News Articles

When publishing a new article, these files must all be updated:

1. **Create** `news/{slug}/index.html` — full article page
2. **Update** `news/index.html` — promote new article to featured, add grid card, shift oldest out
3. **Update** `index.html` — update the Vegas Dispatch section with the new article card
4. **Update** `sitemap.xml` — add new URL entry with `<lastmod>` date

**Before touching `index.html`**, always check git log to confirm the current state:
```bash
git log --oneline --format="%h %ad %s" --date=short index.html | head -5
```
If there has been recent homepage work not done in this session, pull the latest and make only the targeted change (the dispatch/news card section). Never rewrite index.html from scratch.

### News article HTML structure

```html
<body>
<div id="vs-header"></div>          <!-- header injection point -->
<div id="vs-progress"></div>        <!-- scroll progress bar -->

<nav class="breadcrumbs">...</nav>  <!-- Home › Vegas Dispatch › Article Title -->

<!-- hero, article body, etc. -->

<div id="vs-footer"></div>
<script src="/components/header.js"></script>
<script src="/components/footer.js"></script>
</body>
```

### Email signup in articles

Use the Cloudflare Worker endpoint (not the Brevo API directly):
```javascript
fetch('https://brevo-subscribe.vegassidekickcom.workers.dev', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email })
})
```

---

## Pushing Files to GitHub (MCP API)

`git push` is blocked in this environment (proxy returns 403). All file pushes go through the Python MCP API:

```python
import urllib.request, json

with open('/home/claude/.claude/remote/.session_ingress_token') as f:
    token = f.read().strip()

mcp_url = "https://api.anthropic.com/v2/ccr-sessions/{SESSION_ID}/github/mcp"
headers = {
    "X-MCP-Server-ID": "f537862b-b4d9-5761-8681-c6df5723856e",
    "X-Session-UUID": "{SESSION_ID}",
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream"
}

def mcp_push(files, msg):
    payload = {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {
        "name": "push_files",
        "arguments": {"owner": "VegasSidekick", "repo": "vegas-sidekick",
                      "branch": "main", "files": files, "message": msg}
    }}
    req = urllib.request.Request(mcp_url, data=json.dumps(payload).encode(), headers=headers, method='POST')
    with urllib.request.urlopen(req, timeout=180) as r:
        raw = r.read()
    result = None
    for line in raw.decode().split('\n'):
        if line.startswith('data: '):
            result = json.loads(line[6:])
    text = result.get('result', {}).get('content', [{}])[0].get('text', '') if result else ''
    return '"commit"' in text
```

The `SESSION_ID` and `X-MCP-Server-ID` change each session — read the current values from `/tmp/mcp-config-cse_*.json`.

After every push, sync the local repo:
```bash
git fetch origin main && git reset --hard origin/main
```

The stop hook checks for uncommitted local changes — the local repo must always match remote after a session.

---

## Algolia Search Index Schema

The `vegas_shows` Algolia index expects records with these fields:
- `name` — Show name
- `venue` — Venue/hotel name
- `description` — Short description
- `price` — Price string (e.g., `"From $68"`)
- `category` — Category tag (e.g., `"comedy"`, `"cirque"`)
- `url` — Relative path to show page

---

## Git Conventions

Commit messages are imperative, descriptive, and scoped to what changed:
- `Add Michael Jackson ONE show page and images`
- `Wire header/footer components into Carrot Top page`
- `Fix logo path and add all logo and mascot images`

Branch naming: `claude/feature-description-<id>` for AI-assisted work.

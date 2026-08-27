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
│   └── index.html          # Client-side search page (uses /components/search-data.js)
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
| Search | Dependency-free client-side search (local JS dataset — no third-party service) |
| Email | Brevo (formerly Sendinblue) |
| Auth | GitHub OAuth (for CMS admin) |
| Fonts | Google Fonts — **Plus Jakarta Sans** (display) + **Inter** (body); Cormorant Garamond italic for editorial accents. *(Legacy Bebas Neue/Barlow fully retired in the Aug 2026 redesign.)* |

**No npm, no build step, no bundler.** All third-party libraries are loaded from CDN.

---

## Design System

> **Redesigned Aug 2026 — neon palette + Plus Jakarta Sans/Inter.** The pre-2026 look (navy/orange + Bebas Neue/Barlow) is fully retired from rendered pages. ⚠️ Show-page base CSS still *defines* legacy token names like `--navy`/`--orange`, but they're overridden by the neon palette and a blue `--primary: #3b82f6`. **When building/updating a page, match a current live page — not any legacy prose below that still mentions Bebas Neue, Barlow, or orange CTAs.**

### Color Palette (CSS Custom Properties)
```css
--ink:     #171225   /* Primary text */
--bg:      #ffffff   /* Page background (light) */
--soft:    #f5f4fb   /* Soft section background */
--blue:    #3b82f6   /* PRIMARY — CTAs + price (locked-in) */
--pink:    #ff2e7e   /* Highlight accent — use sparingly */
--lime:    #c6f22e   /* Lime accent */
--purple:  #7c3aed   /* Eyebrows / secondary */
--teal:    #0fb5c9   /* Tertiary accent */
/* Hero gradient: linear #1c0a3a → #2b0f5c → #12061f (deep-purple neon) */
```

### Typography
- **Display/Headlines:** Plus Jakarta Sans (700/800)
- **Body:** Inter (400–700)
- **Editorial accent:** Cormorant Garamond italic (tagline + `.lede` on show pages)

### Responsive Breakpoints
- Desktop → Tablet: `900px`
- Tablet → Mobile: `480px`

### Visual Conventions
- Light page background with deep-purple **neon-gradient hero** sections (white text, starburst speckles)
- **Blue (`#3b82f6`) primary CTAs**; pink `#ff2e7e` as a small highlight only
- Glassy hero pills; purple uppercase `.eyebrow` section labels
- Rounded cards (`--radius: 18px`), soft shadows
- Animations: `fadeUp`/scroll-reveal (`IntersectionObserver`), Ken Burns hero sliders, `pulseGlowCta`

---

## Current State & Recent Changes (updated 2026-08-11)

Durable facts from recent work. Where these conflict with older prose elsewhere in this file, **these win.**

### `_headers` file (Cloudflare) — caching + security
A root `_headers` file now sets response headers:
- **HTML + `/components/*`** → `Cache-Control: public, max-age=0, must-revalidate` (always revalidate → always fresh).
- **`/images/*`, favicons** → `public, max-age=31536000, immutable`.
- Security headers site-wide: `X-Content-Type-Options`, `Strict-Transport-Security`, `X-Frame-Options`, `Referrer-Policy`, `Permissions-Policy`.

**Implication for the `?v=` cache-busting instructions elsewhere in this file:** bumping `?v=` on `header.js`/`footer.js`/`search-data.js` is **no longer required for correctness** — those files now revalidate on every load. It's optional/harmless, not mandatory. (Only takes effect on the branch Cloudflare deploys — i.e. `main`.)

### Author / E-E-A-T entity
- **`/about/kris-kidd/`** is the canonical **`Person` entity** page (`ProfilePage` + `Person` JSON-LD, `@id …#kris`, `sameAs` → FB/IG/Reddit/Pinterest `VegasSidekick`).
- **`/about/`** carries `AboutPage` + `Organization` (`@id …#organization`) with `founder` → Kris.
- All **news articles** link their `author` schema + visible byline to `/about/kris-kidd/`.
- **Real bio facts (use these, don't invent):** Kris Kidd — Las Vegas local since **2005**; in show **ticketing since 2006**, ~15+ yrs ticketing & concierge, most recently high-end concierge at **Hilton Grand Vacation Club**; has seen **100+** shows; personal favorites **VEGAS! The Show, Atomic Saloon Show, Mac King**. Founded the site because he was tired of being told what to recommend.
- Both About pages are on the new neon design; author photo is `images/kris-kidd.webp` (real binary).

### Image / performance patterns (Core Web Vitals)
- **Hero images:** add `<link rel="preload" as="image" href="…" fetchpriority="high">` (add `type="image/webp"` for webp) in `<head>`, plus `fetchpriority="high"` + `loading="eager"` on the hero `<img>`.
- **Format:** serve WebP via `<picture><source type="image/webp" srcset="…webp"><img src="…jpg" …></picture>`; add `picture{display:contents}` so existing img CSS is unaffected. **Keep the original `.jpg` on disk** — OG/social tags and homepage/listing/search cards reference it, and crawlers need a real (non-data-URL) file.
- **No data-URL heroes.** All show pages now reference real image files (the 7 old base64-embedded pages were converted). Below-fold/gallery images use `loading="lazy"`.
- **Resize oversized sources** to ~1280px wide before encoding — the biggest LCP win came from an oversized 2500px hero, not from de-bloating base64.
- **Binaries CAN be committed via `git` in this environment** (unlike the MCP `push_files` path, which corrupts binaries). Convert with `cwebp` or PIL (`Image.save(..., 'WEBP', quality=78, method=6)`).

### Git workflow in this environment
- Remote is **`k2oddworks/vegas-sidekick`**; plain **`git push` works** here (the MCP `push_files` API described later in this file is a *different* setup — use real git in this session).
- Develop on the feature branch; for **"make live"**, fast-forward the change onto **`main`** and push (Cloudflare Pages deploys `main`). Because `main` and the feature branch can have divergent history, "make live" is done by checking out `main` and applying just the changed files (`git checkout <branch> -- <files>`), then committing + pushing `main`.

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

### Affiliate Links — use the real Spotlight URL

**Do NOT guess the affiliate URL from the show slug.** Spotlight's own URLs are inconsistent — different path segments (`/show/...` vs `/shows/...`), different sub-categories (`/tribute/...`), and slugs that don't match ours (extra suffixes, reworded names). There is **no reliable pattern to derive** the link.

**Workflow:** Kris provides the actual Spotlight listing URL for the show. Take that URL and append `/ref/vegassidekick` to it — that's the affiliate link. Use it verbatim in every CTA slot on the page (hero, sidebar, mobile buy bar, final CTA, save pill, both seen-widget links, the JSON-LD `offers.url`, and the schedule slider's `affiliateUrl`). If Kris hasn't given the URL yet, ask for it (or leave a clearly-flagged placeholder) rather than inventing one — a wrong affiliate link silently loses revenue.

Real examples (note how different they are):
```
Spotlight: https://spotlight.vegas/show/tribute/mj-live-at-planet-hollywood/
Link:      https://spotlight.vegas/show/tribute/mj-live-at-planet-hollywood/ref/vegassidekick

Spotlight: https://spotlight.vegas/shows/tribute/ikons-of-rock-api/
Link:      https://spotlight.vegas/shows/tribute/ikons-of-rock-api/ref/vegassidekick/
```

---

### Video Previews (Show Trailers)

Show pages can embed an official YouTube trailer via a reusable **click-to-play facade** — a thumbnail + a "Watch video preview" button that swap in an inline player on click. It plays **on our page** (privacy-friendly `youtube-nocookie`, autoplay on click, fullscreen enabled) and never navigates to YouTube. It's **lazy by design** — only the thumbnail loads until the visitor clicks — so it doesn't hurt LCP.

**Reference implementation:** `shows/comedy/carrot-top/index.html` (first build). The `/search/` card `onerror` and this facade are the only places we use inline `onerror`.

**Rule — never guess the trailer (same discipline as affiliate links):** Kris provides the **official** YouTube trailer URL. **Embed the producer's official video; never re-host** someone else's trailer on a Vegas Sidekick channel (copyright — Content-ID will flag it). For each trailer, Kris must give three things:
1. the **official YouTube URL** (the video ID is the part after `youtu.be/`, `watch?v=`, or `/embed/` — ignore any `?si=` / `?is=` share-tracking param),
2. the **upload date**, and
3. the **run-time (duration)**.

Upload date + duration are **required for the `VideoObject` schema and Google validates them — do not fabricate**. If you only have the URL, ship the working embed and leave the `VideoObject` for a follow-up rather than inventing a date. (YouTube is unreachable from the build env, so you can't auto-pull these — they come from Kris / the video's YouTube page.)

**To add a trailer to a show:**

1. Drop the video block into the page — a `#section-trailer` section, normally placed right after the About section:
   ```html
   <section class="section fade-up" id="section-trailer" aria-labelledby="trailer-heading">
     <h2 id="trailer-heading" class="section-title">Watch the <span>Preview</span></h2>
     <div class="vs-video" data-yt="VIDEO_ID" data-title="Show Name — Las Vegas Show Trailer">
       <span class="vs-video-badge">▶ Show Trailer</span>
       <img class="vs-video-thumb" src="https://i.ytimg.com/vi/VIDEO_ID/maxresdefault.jpg" onerror="this.onerror=null;this.src='https://i.ytimg.com/vi/VIDEO_ID/hqdefault.jpg'" alt="Show Name trailer — venue, Las Vegas" loading="lazy" width="1280" height="720" />
       <button class="vs-video-play" type="button" aria-label="Play Show Name video preview"></button>
     </div>
     <button class="vs-video-cta" type="button" data-yt-trigger>▶ Watch video preview</button>
   </section>
   ```
   The `maxresdefault` thumbnail is sharp 16:9 but isn't generated for every video, so the `onerror` falls back to the universal `hqdefault`.
2. Ensure the page carries the shared **`.vs-video*` CSS** (in the `<style>` block) and the shared **player script** (just before `</body>`) — copy both verbatim from Carrot Top. The script reads `data-yt` and injects `https://www.youtube-nocookie.com/embed/{id}?autoplay=1&rel=0&modestbranding=1` on click; it wires both the thumbnail (`.vs-video`) and the `[data-yt-trigger]` button.
3. If the page has the `.dnav-dot` section nav, add a dot after About: `<a href="#section-trailer" class="dnav-dot" data-label="Trailer" aria-label="Trailer"></a>`.
4. Add the `VideoObject` JSON-LD in `<head>` (alongside the Event/FAQ/Breadcrumb blocks):
   ```json
   {"@context":"https://schema.org","@type":"VideoObject","name":"…","description":"…","thumbnailUrl":"https://i.ytimg.com/vi/VIDEO_ID/maxresdefault.jpg","uploadDate":"YYYY-MM-DD","duration":"PT#M#S","embedUrl":"https://www.youtube.com/embed/VIDEO_ID","contentUrl":"https://www.youtube.com/watch?v=VIDEO_ID"}
   ```
   `duration` is ISO 8601 (38s → `PT38S`; 1m32s → `PT1M32S`).

**Trailer inventory** — which shows have a live trailer — is tracked in the private `/hq/` hub → **Trailers** tab.

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

### `components/picks.js` — rotating show cards

Fills any grid marked `data-vs-picks` with live records from `window.VS_SHOWS`, reshuffled on every page load. **Mounted on 75 pages** (68 show pages, the homepage, 6 venue pages).

Because it reads name, venue, price and image straight from `search-data.js`, these cards can never quote a stale price or link to a closed show — **they are exempt from the Price Change Checklist and the Show Closing Checklist.**

It never invents markup: it clones the grid's own first card and rewrites the fields it recognises, so it adapts to whichever card variant the page uses (the site has five: `div.also-card`, `a.also-card` with a price, the `also-name` variant, `.scard`, `.show-card`). The cards already in the HTML stay as the no-JS fallback **and** as that structural template — never delete them.

```html
<div class="also-grid" data-vs-picks='{"count":3,"exclude":"auto","preferCat":"auto"}'>
  <!-- one or more real cards: fallback + template -->
</div>
```

Options: `count`, `exclude` (`"auto"` = this page), `preferCat` (`"auto"` = this page's category; same-category sorts first), `cat` (hard filter), `excludeVenue` (string or array of lowercase substrings).

Requires **both** scripts, in this order:
```html
<script src="/components/search-data.js?v=22"></script>
<script src="/components/picks.js?v=1"></script>
```

It degrades silently — if `VS_SHOWS` is missing, if there are fewer matches than requested, or if anything throws, the static cards stay untouched. That makes a broken mount invisible, so **verify in a browser after wiring, don't assume.**

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
| Brevo | API Key in source, List ID: `2` | `components/footer.js` |
| GitHub OAuth | Client ID: `Ov23lit31UqvtSuPp7tJ` | `functions/api/auth.js` |
| GitHub OAuth | Client Secret via `GITHUB_CLIENT_SECRET` env var | `functions/api/auth.js` |
| Cloudinary | **RETIRED (Aug 2026).** No longer used — all OG images are self-hosted. Formerly clouds `dvhunpinz` + `vegassidekick`. | — |

**Note:** The Brevo key has restricted permissions. The GitHub Client Secret must be stored as an environment variable in Cloudflare Workers — never commit it to the repo. (Site search no longer uses Algolia — it runs entirely client-side off a local JS dataset. See **Site Search** below.)

**OG/social images are now self-hosted (Cloudinary retired Aug 2026).** Because binaries commit via `git` in this environment, OG images live as real files in `/images/` (e.g. `/images/{slug}-og.jpg`) and the `og:image`/`twitter:image`/JSON-LD `image` tags point at `https://vegassidekick.com/images/...`. Convert the source to a web-optimized JPG (`Image.save(..., 'JPEG', quality=85, optimize=True)`, ~1080px square or ~1600px wide), commit it, and reference it. Crawlers need a real hosted file (never a data-URL), which a committed `/images/` file satisfies. The old Cloudinary "upload from phone, paste URL" workflow is no longer used — all prior Cloudinary references were migrated to self-hosted files.

---

## Development Workflow

### Adding a New Show Page

1. Create directory: `shows/{category}/{show-slug}/`
2. Copy an existing show page (e.g., `shows/comedy/carrot-top/index.html`) as a template
3. Update all show-specific content: title, description, images, pricing, show times, venue, FAQ
4. Set the affiliate ticket links from the **real Spotlight listing URL Kris provides** + `/ref/vegassidekick` — do not guess it from the slug (see **Affiliate Links** above). Update every CTA slot on the page.
5. Add show images to `images/` directory
6. Add the show to `sitemap.xml`
7. Register the show in the listing pages: add an entry to the `SHOWS` array in `shows/{category}/index.html` (category listing) and in `shows/index.html` (the "All Shows" master list). The homepage `index.html` is a **curated** subset — only add a card there if the show is meant to be featured.
8. Add the show to site search: append a record to `components/search-data.js` and bump the `?v=` cache-buster on every page that loads it (see **Site Search** below). Without this the show will not appear in `/search/`.
9. Validate the JSON-LD before shipping: `python3 scripts/audit-event-schema.py`. See **Structured Data (JSON-LD) Requirements** below for the exact fields it checks.

**Image order:** When multiple photos are provided for a new show page, the **first one uploaded/attached is always the hero image** — main hero slide, primary `og:image`/`twitter:image`, first entry in the Event JSON-LD `image` array — unless explicitly told otherwise. Don't guess which photo looks most "hero-like."

**Photo policy (site-wide standard):** On every show page, the photo/camera detail card and the "Can I take photos?" FAQ should use this wording (paraphrase as needed for tone): *"Still photos may be allowed as long as they aren't distracting — please check with your usher on the way in. No flash photography."* Use this even when the source listing (e.g. Spotlight) says cameras are strictly prohibited — this is the Vegas Sidekick default going forward for all shows.

**Sidekick Pick (`sp:true`):** Never set `sp:true` on a new show by default. It stays `sp:false` unless the user explicitly says to mark that specific show as a Sidekick Pick.

### Updating a Show's Price (Price Change Checklist)

**Prices are denormalized — a single show's price is hand-copied into ~10 files.** There is no build step and no single source of truth, so changing a price in one place is **not** enough. When Kris gives a price change (e.g. "Mad Apple went $56 → $59"), you MUST find and update **every** occurrence. Start by grepping the whole repo for the show slug and both the old and new numbers (`grep -rn '\$56\|"price":\s*56\|from \$56' --include=index.html --include=*.js .`), then work this checklist:

1. **Show detail page** (`shows/{cat}/{slug}/index.html`) — every visible price (hero price strip, sidebar/`.sb`/save-pill, mobile buy bar, any "from $X"), **and** the JSON-LD `offers.price` (bare number, no `$`), **and** the "✓ Prices verified · Month 2026" freshness line if the month is now stale.
2. **`components/search-data.js`** — the record's `price` (number) **and** `pd` (display string like `"$56"`) **and** any price mentioned in the free-text `kw` blob. Bump the `?v=` cache-buster on every page that loads it (see **Site Search**).
3. **Category listing** (`shows/{cat}/index.html`) — the `SHOWS` array entry's `price` and `pd`.
4. **All Shows master list** (`shows/index.html`) — same `SHOWS` array entry.
5. **Homepage** (`index.html`) — only if the show has a curated card there (`.pr`/price text).
6. **Venue pages** (`venues/*/index.html`) — the show's `from <b>$X</b>` card price, **and** the hero "from $X" stat / sub-head if this show set the venue's cheapest price.
7. **Guides** (`guides/*/index.html` + `guides/index.html`) — the trickiest. Update: the `.price-badge` (`From $X`), the `.g-meta`/`.stat` "From $X" hero/card figures, **and any price written into prose or the FAQ** (e.g. "starting around $56"), including the duplicated copy inside the `FAQPage` JSON-LD.

**Watch for cascading claims, not just numbers.** A price change can break superlatives and ordering: "cheapest", "under $50", "from $X" hero stats, a guide's price-sorted ranking, or a show's eligibility for `best-cheap-vegas-shows`. Re-read any "cheapest/from/under" wording near the changed show and fix the logic, not only the digits. When done, run `python3 scripts/audit-event-schema.py` and report the full list of files touched.

### When a Show Closes (Show Closing Checklist)

Shows close. When one does, follow this three-part standing policy — **don't wait to be told the steps, just run the checklist**:

1. **Pull it from every catalog/listing page** (but never delete the show's own page — see #3).
2. **Add a closed-show banner** to the show's own page directing visitors to the catalog.
3. **Never delete the page.** Shows reopen, get revived under new producers, or come back for limited returns — keep the page intact so it can be updated and republished instead of rebuilt from scratch.

**Timing — don't act early.** A "closing" announcement usually names a final performance date that's still weeks or months out. The show is still running and still sellable up to that date — leave it fully live in the catalog with normal buy CTAs. A "final weeks, don't miss it" urgency note on the page itself is good (drives ticket sales), but the steps below don't start until the day **after** the actual final performance.

**Step 1 — Remove from the catalog.** Same denormalization problem as the Price Change Checklist — grep the whole repo for the show's slug (`grep -rln 'slug-name' --include=index.html --include=*.js .`) and work through:

- **`components/search-data.js`** — delete the show's record entirely. Bump the `?v=` cache-buster on every page that loads it (see **Site Search**).
- **Category listing** (`shows/{cat}/index.html`) — remove the entry from the `SHOWS` array.
- **All Shows master list** (`shows/index.html`) — remove the same entry.
- **Homepage** (`index.html`) — remove the curated card if it has one.
- **Venue pages** (`venues/*/index.html`) — remove the show's card.
- **Guides** (`guides/*/index.html` + `guides/index.html`) — remove any recommendation/ranking of the show, including inside `FAQPage` JSON-LD prose. Same "cascading claims" warning as the price checklist applies — check whether removing it breaks a "3 best..." count or a superlative claim about the guide's remaining shows.
- **"You Might Also Like" cross-links** (`.also-grid`) on *other* show pages — grep for the slug across `shows/**/index.html` and remove the card from any page that links to it.
- **`sitemap.xml`** — leave the URL in (the page still exists), but this is a judgment call; update `lastmod` when you touch the page.

**What NOT to touch:** old news articles that mention the show historically (e.g. an announcement post from when it opened). That's a dated record, not a live catalog reference — don't rewrite history there.

**Step 2 — Add the closed-show banner to the show's own page.**

- Place it directly below the breadcrumb, unmissable — not a subtle dismissible thing.
- Style it in the show's own `--show` accent color so it doesn't read as a generic site error.
- Copy pattern: *"[Show Name] closed on [date]. Explore other [category] shows in Las Vegas →"* linking to the category listing page.
- **Neutralize every buy CTA on the page** (`.hero-cta`, `.sb-cta`, `.mob-cta`, `.final-cta-btn`) — don't leave live "Get Tickets" buttons pointing at a Spotlight affiliate link for a show that isn't running. Repoint them to "Browse Similar Shows" → the category page instead of just disabling them.
- **Update the JSON-LD Event block** — otherwise Google Search Console keeps surfacing a live ticket/event rich result for a dead show. Default approach: **strip the Event block entirely** while closed (cleanest, avoids stale rich results). Restore it verbatim on reopen.
- Make every edit in this step a clean, reversible diff — comment out what you're neutralizing rather than deleting it, and keep the banner in one isolated block. The goal is that "reopen" is a mirror-image of this checklist, not a rebuild.

**Step 3 — If it reopens.** Reverse Step 2 (remove the banner block, uncomment the CTAs, restore the Event JSON-LD) and re-add the show to every file touched in Step 1, exactly like adding a new show page (see **Adding a New Show Page**). Re-run `python3 scripts/audit-event-schema.py` after.

When you finish either direction of this checklist, report the full list of files touched — same discipline as the Price Change Checklist.

### Structured Data (JSON-LD) Requirements

Every show page's `<script type="application/ld+json">` **Event** block must include every field below — Google Search Console flags any that are missing or malformed, and it silently accumulates across pages if the wrong page gets copied as a template for the next one. Use `@type: "Event"` (not `EventSeries`) for all new show pages — it's what every show built this way uses, and it's the type that requires `startDate`/`endDate`, which keeps the schema unambiguous.

```json
{
  "@context": "https://schema.org",
  "@type": "Event",
  "name": "Show Name",
  "description": "...",
  "image": "https://vegassidekick.com/images/{slug}-hero.webp",
  "url": "https://vegassidekick.com/shows/{category}/{slug}/",
  "startDate": "2026-01-01",
  "endDate": "2027-01-01",
  "eventStatus": "https://schema.org/EventScheduled",
  "organizer": { "@type": "Organization", "name": "Show Name", "url": "https://vegassidekick.com/shows/{category}/{slug}/" },
  "location": {
    "@type": "Place",
    "name": "Venue Name",
    "address": { "@type": "PostalAddress", "streetAddress": "...", "addressLocality": "Las Vegas", "addressRegion": "NV", "postalCode": "...", "addressCountry": "US" }
  },
  "offers": {
    "@type": "Offer",
    "price": "39",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock",
    "url": "https://spotlight.vegas/.../ref/vegassidekick",
    "validFrom": "2026-01-01"
  },
  "performer": { "@type": "PerformingGroup", "name": "Show Name Cast" }
}
```

**The one gotcha that caused nearly every GSC error on this site:** `offers.price` must be a bare number string — `"39"`, never `"$39"`. Google rejects the `$`.

Other rules baked into that skeleton:
- `organizer.url` — always the show's own vegassidekick.com page (not the venue's site, not Spotlight).
- `offers.validFrom` — required even though it's easy to forget; use `"2026-01-01"` unless there's a real on-sale date.
- `performer` — use `PerformingGroup` with `"{Show Name} Cast"` for ensemble/cast shows, or `Person` with the performer's actual name for solo acts (Donny Osmond, Wayne Newton, Carrot Top, etc.). Never omit it.
- `startDate`/`endDate` — required on every Event block, even for open-ended residencies. Use `"2026-01-01"`/`"2027-01-01"` as the default range unless a real end date is known.

Re-run `python3 scripts/audit-event-schema.py` any time you touch a show page's JSON-LD, or as a spot check after a batch of new shows — it parses every show page's Event block and reports exactly which required field is missing or malformed, file by file. It's cheap enough to run after every build; there's no need for it to be a scheduled/recurring task. (Google's own crawl status — the actual Search Console Enhancements report — is a separate thing worth a periodic glance since it reflects Google's re-crawl schedule, not the source files, but that's a dashboard check, not something this repo can automate.)

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

Push to the `main` branch (the repository's default branch). Cloudflare auto-deploys on push. The Cloudflare Worker (`functions/api/auth.js`) must be deployed separately via Cloudflare dashboard or Wrangler CLI.

**⚠️ This is a Worker with static assets, NOT classic Cloudflare Pages.** There is a `wrangler.jsonc` at the repo root with an `assets` block. Most Cloudflare advice you will find online assumes Pages and does not apply. Two consequences that have already bitten us:

- **`404.html` is not automatic.** The asset server's `not_found_handling` defaults to `"none"`, which returns a bare 404 with *no body* — browsers then show their own error page. It must be set explicitly:
  ```jsonc
  "assets": { "directory": ".", "not_found_handling": "404-page" }
  ```
  Symptom when this is wrong: a bad URL shows Chrome's "This page can't be found" instead of ours, and editing `404.html` appears to do nothing because it was never being served.
- **`.assetsignore` controls what ships.** Anything not listed is publicly fetchable by URL. Internal docs (`CLAUDE.md`, `BRAND.md`, `ROADMAP.md`, `SHOW-BUILDER-PROMPT.md`, `VS_CHAT_CONTEXT.md`) and `scripts/` are excluded there. **Add any new internal file to `.assetsignore` when you create it.**

If redirects or headers ever appear to be ignored, suspect this same Pages-vs-Workers difference before anything else.

### "Make Live" — standing instruction

When Kris says **"make live"** (or "make it live", "publish it", "ship it"), it means: **do every step required to publish the current work so it is live on the website — then give back the live URL.** Do not ask clarifying questions and do not explain the steps first — just carry them out. Concretely:

1. Commit all work on the current working branch.
2. Get it onto `main` (fast-forward `main` to the working branch, or merge) and push `main` so Cloudflare Pages deploys.
3. Make sure every publish step is actually done — including listing pages and the **search index** (`components/search-data.js` + `?v=` bump) for a new show, plus `sitemap.xml`.
4. Return the live URL(s) and note the ~1–2 min CDN propagation.

### End-of-task report — standing instruction

Every time a task is completed (not just "make live"), close out with three things:

1. **The URL(s) of any updated pages**, if the task touched live pages.
2. **A summary paragraph** of what was actually updated.
3. **A suggestion for what to do next** — pull from `ROADMAP.md` where relevant.

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
7. **Search is a local dataset, not automatic** — site search reads `components/search-data.js` (a plain JS array), matched client-side. Adding a show page does **not** add it to search. You must append a record to `search-data.js` and bump the `?v=` cache-buster on the pages that load it. See **Site Search** below.

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

**OG/social preview images** require a real hosted file URL (crawlers can't use data URLs). In this environment, just commit the image as a real file in `/images/` via `git` and point the OG tags at `https://vegassidekick.com/images/...` (see **External Services** above — Cloudinary is retired; OG images are self-hosted).

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

## Site Search (client-side)

Search is **dependency-free and runs entirely in the browser** — there is no Algolia and no external service. Two files power it:

- **`components/search-data.js`** — sets `window.VS_SHOWS`, a single JS array of show records (one object per show).
- **`components/search.js`** — exposes `vsSearch(query)` / `vsNorm(s)`. It normalizes text (lowercase, strips accents), requires **every** whitespace-separated term to appear somewhere in the record (AND match), and ranks by relevance (name-prefix > name-contains > exact category, plus per-term name hits).

The search page (`search/index.html`) loads both plus renders result cards. `search-data.js` is also loaded on `shows/index.html` and `index.html`.

### Record schema (`search-data.js`)

Each entry is an object:
```js
{ "name": "Ikons of Rock",                       // show name
  "sub": "Rock's Biggest Stars in One Show",      // subtitle (optional, "")
  "venue": "The STRAT Theater · The STRAT Hotel", // venue line
  "cat": "Music",                                  // category label (Title Case: Comedy, Magic, Cirque, Music, Family, Adult, Spectaculars)
  "price": 62,                                     // numeric price (for sort)
  "pd": "$62",                                     // display price string
  "img": "/images/ikons-of-rock-hero.webp",        // hero image ("" falls back to name text)
  "kw": "Live Classic Rock ... Kiss Ozzy ...",     // free-text keyword blob — everything you want the show findable by
  "url": "/shows/music/ikons-of-rock/" }           // relative path to the show page
```

The **`kw`** field is the workhorse: because matching is AND across all terms, pack it with venue names, performer/act names, categories, price, schedule words, and any synonym a visitor might type. Only `name`, `sub`, `venue`, `cat`, and `kw` are searched.

### Adding / updating a show in search

1. Append (or edit) the record in `components/search-data.js`.
2. **Bump the cache-buster.** All three loaders reference it with a version query — `search-data.js?v=N`. Browsers cache per-URL, so returning visitors keep the stale dataset until the number changes. Bump `?v=` on **every** page that references it:
   ```bash
   grep -rl 'search-data.js?v=' --include="*.html" .   # find them
   # then bulk-replace ?v=N -> ?v=N+1 across all of them
   ```
   (Same principle and pitfall as `header.js`/`footer.js` cache-busting.)
3. Sanity-check locally with Node:
   ```bash
   node -e "global.window={};require('./components/search-data.js');require('./components/search.js');console.log(window.vsSearch('rock').map(s=>s.name));"
   ```

---

## Git Conventions

Commit messages are imperative, descriptive, and scoped to what changed:
- `Add Michael Jackson ONE show page and images`
- `Wire header/footer components into Carrot Top page`
- `Fix logo path and add all logo and mascot images`

Branch naming: `claude/feature-description-<id>` for AI-assisted work.

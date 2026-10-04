# Vegas Sidekick — Context Primer

*A paste-ready briefing to bring a new AI conversation up to speed. Last updated: 2026-10-03.*
*(For current execution rules see `AGENTS.md`; for Sidekick Index work see `SIDEKICK-INDEX.md`. `CLAUDE.md` is legacy reference only.)*

---

## What this is
**Vegas Sidekick** (`vegassidekick.com`) — a static Cloudflare Pages site for discovering Las Vegas show tickets, earning affiliate revenue via Spotlight.vegas links (`/ref/vegassidekick`). No backend, no build step: plain HTML/CSS/JS, components injected by small JS files, Decap CMS for news.

**Founder / voice:** Kris Kidd — LV local since 2005, 20+ yrs as a Ticketing & Vegas Entertainment Specialist (including several years as a high-end concierge at prestigious Las Vegas resorts), hundreds of shows seen (no specific number). Favorites: VEGAS! The Show, Atomic Saloon Show, Mac King.

## Current design system (post Aug-2026 redesign)
- **Fonts:** Plus Jakarta Sans (display) + Inter (body); Cormorant Garamond italic for editorial accents. *(Bebas Neue/Barlow retired.)*
- **Palette (neon):** blue `#3b82f6` primary (CTAs + price), pink `#ff2e7e` highlight (sparingly), lime `#c6f22e`, purple `#7c3aed`, teal `#0fb5c9`. Light page bg `#ffffff`, ink `#171225`. Deep-purple neon-gradient heroes (`#1c0a3a→#2b0f5c→#12061f`).
- Rounded cards (`--radius:18px`), scroll-reveal animation, Ken Burns hero sliders.
- ⚠️ Show-page CSS still *defines* legacy `--navy`/`--orange` token names but overrides them with the neon palette + `--primary:#3b82f6`. **Match a live page, not old docs.**

## Deployment / git (this environment)
- Remote: `k2oddworks/vegas-sidekick`. Plain `git push` works.
- Develop on the feature branch. **"Make live"** = apply changed files onto `main` and push (Cloudflare deploys `main`). Main and the feature branch can diverge, so make-live copies just the changed files onto `main` via `git checkout <branch> -- <files>`.
- Images: real binaries CAN be committed via git here (the MCP `push_files` path corrupts binaries — don't use it in this env).

---

## Accomplishments log

### 2026-08-11 session
- **`_headers` file (Cloudflare):** security headers site-wide (HSTS, nosniff, frame/referrer/permissions policy) + cache policy — HTML & `/components/*` revalidate every load; images/favicons cached `immutable` 1yr. **This makes the old `?v=` cache-busting chore optional**, not mandatory.
- **E-E-A-T author entity:**
  - `/about/kris-kidd/` = canonical `Person` (ProfilePage + Person JSON-LD, `sameAs` → brand socials).
  - `/about/` = AboutPage + Organization with `founder` → Kris.
  - All 20 news articles' `author` schema + bylines link to the entity.
  - Corrected the previously-inaccurate bio to the real facts (above).
- **Reskinned `/about/` + `/about/kris-kidd/`** to the neon design; added real WebP portrait (`images/kris-kidd.webp`), replacing a corrupt file.
- **Image / LCP performance (all 63 show pages):**
  - Hero `preload` + `fetchpriority="high"` added everywhere a hero image exists (58 pages).
  - De-bloated the 7 data-URL pages (222–383KB HTML → 79–93KB); ~1.6MB base64 → 24 real cacheable WebP files.
  - JPG heroes → WebP via `<picture>` (23 pages); kept JPGs for OG/cards. Resized an oversized 2500px hero (comedy-cellar) 685KB→65KB.
  - **Measured (controlled local, mobile-throttled):** the real LCP lever was **oversized images** (comedy-cellar −36% LCP), *not* base64 de-bloat (which mainly cut transfer weight + enabled caching). CLS unchanged/improved.

### Earlier (pre-2026-08-11, from prior sessions)
- Full homepage + site-wide header/footer redesign to the neon vibe; interactive Spike mascot, orbiting bubbles, colorful drawer buttons, Guides links.
- SEO pass: keyword-aligned H1s on category pages, title/description tuning ("cheap/discount tickets"), sitemap lastmod refresh, Organization/WebSite/FAQPage schema + canonicals.

---

## Image / performance patterns (reuse these)
- Hero: `<link rel="preload" as="image" href="…webp" type="image/webp" fetchpriority="high">` + `fetchpriority="high"` `loading="eager"` on the `<img>`.
- WebP via `<picture><source type="image/webp" srcset="…webp"><img src="…jpg" …></picture>` + `picture{display:contents}`. **Keep the `.jpg`** (OG/social + cards reference it).
- Below-fold images `loading="lazy"`. Resize oversized sources to ~1280px.
- Convert: `cwebp -q 78` or PIL `Image.save(dst,'WEBP',quality=78,method=6)`.

## Open threads / possible next steps
- **Field measurement:** run `pagespeed.web.dev` on live URLs (blocked from this environment), or watch Search Console → Core Web Vitals for real CrUX data as Google re-crawls.
- **5 heavy non-image pages** (all-shook-up, fantasy, x-country, x-burlesque, chippendales) are large from inline CSS/SVG, not images — separate cleanup opportunity.
- **Social profiles:** the `sameAs` schema points at brand FB/IG/Reddit/Pinterest — strongest signal once those profiles exist and link back.
- Set up the brand's real social accounts if not done.

---

## Good to Know social-series reference

Vegas Sidekick's recurring **Good to Know** social series is governed by `GOOD-TO-KNOW.md`.

- It is the customer-service social layer for verified show changes that affect planning or booking: start times, venue moves, return dates, performance-day changes, meaningful added dates, closing dates and similar material updates.
- It is distinct from **Vegas Dispatch**, which is the editorial/news product.
- Use approved repo photography, artwork, show logos and Vegas Sidekick branding exactly as supplied. Do not generate replacements or lookalikes.
- Store recurring series assets under `/images/good-to-know/`.


---

## Sidekick Index — October 2026

Sidekick Index is Vegas Sidekick's public entertainment-reference layer. Its canonical project spec is `SIDEKICK-INDEX.md`.

Current routes:

- `/sidekick-index/`
- `/sidekick-index/headliners-residencies/`
- `/sidekick-index/show-price-index/`
- `/sidekick-index/touring-shows-concerts/`

The shared `components/sidekick-index-shell.js` adds the Reference Pages navigation and reuses the site's email signup above the footer.

The touring index currently covers 12 venues. Source data lives in `data/reference/touring-shows-concerts.json`; the major headliner/residency calendar lives in `data/reference/headliners-residencies.json`; Show Price Index uses dated snapshot files under `data/show-price-index/`.

Classification rule: recurring Vegas productions stay in the normal show catalog, major residency/headliner engagements go in Headliners & Residencies, and shorter visiting/touring events go in More Touring Shows & Concerts.

Mobile rule: any overflowing Index pill rail must scroll all the way to the final item and visibly signal that more content is available. Current rails use an overflow-aware `Swipe for more →` cue plus a subtle edge fade; the price table uses `Swipe table →`.

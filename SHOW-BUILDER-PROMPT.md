# Vegas Sidekick — Show Page Builder Prompt

Paste this entire document at the start of a new chat session before requesting a new show page.

> **CURRENT BENCHMARK OVERRIDE — September 9, 2026**
>
> `shows/magic/nathan-burton-comedy-magic/index.html` and `SHOW-PAGE-BENCHMARK.md` now govern active show-page UX and copy. Older V Theater / Carrot Top / Absinthe examples in this long prompt are legacy implementation references only. If anything below conflicts with the Nathan benchmark, **Nathan wins**.
>
> Key current rules: active show pages include a compact **What is [Show]?** descriptive overview before Quick Take; write for entity completeness rather than keyword density and never pad to a word count; Hero, descriptive overview, and Quick Take must do different jobs; no formal downside/Think twice modules; Good to know only for real useful facts; Booking tip is optional and actionable only; no customer-facing “tradeoff”; no interaction/participation claims unless Kris explicitly confirms them; use Start time/Start times; prefer “See available dates & times”; use one visible “Show info confirmed Month YYYY” freshness line near the author card; galleries support arrows/keyboard/swipe; seating charts are room-based, geometrically faithful, slab-row when exact seat counts are unnecessary, and mobile tap feedback must appear immediately in view.
>
> **Booking module update — September 15, 2026:** compact v2 is the shared standard. Use the pill + compact day/time/amber CTA treatment in `assets/showtimes-booking.css` and `.js`; do not restore the old large secondary CTA or generic Planning Ahead card.

---

## What This Project Is

Vegas Sidekick (`vegassidekick.com`) is a **static HTML website** for Las Vegas show ticket discovery and affiliate booking. No build system, no npm, no framework — pure HTML/CSS/JS files deployed through the current Cloudflare production path from `main`.

**Revenue model:** Affiliate commissions via ticket links in the format:
```
https://spotlight.vegas/shows/{category-slug}/{show-slug}/ref/vegassidekick
```

**Critical rule:** Never mention "Spotlight.vegas" or any partner name in visible copy text. Links are fine; named references in text are not (business partner may change).

---

## Repository

- **Repo:** `k2oddworks/vegas-sidekick` on GitHub
- **Deploy branch:** `main` — production branch; verify the public site before claiming a deploy is live
- **Feature branches:** `claude/feature-description-<id>` for AI-assisted work
- **Git push** works normally from this environment

---

## Canonical Show Page Template

**Canonical reference / current model:** `shows/magic/nathan-burton-comedy-magic/index.html`

This is the **"Sidekick Build"** — the current standard for all new show pages. Copy it, do not use older pages. Key features:

- Dual scroll progress bars (top fixed bar + sidebar progress indicator)
- Hero section: breadcrumb + **Ken Burns image slider** (3 images, 16:9 `aspect-ratio`, max-height 560px, auto-advance every 5s, 6-dot dot-nav) + venue/title block + price strip
- **Scrolling ticker strip** (show-color background) below hero with repeating show facts
- Two-column layout: `main.main-content` (left) + `aside.sidebar` (right, sticky, navy bg)
- **Stats strip** with count-up animation (IntersectionObserver + requestAnimationFrame) — typically: duration (min), nights/week, years running, price
- **FadeUp IntersectionObserver** on every major section (`.fade-up` class)
- Mobile sticky buy bar fixed to bottom (hidden on desktop)
- **Shimmer animation** on `.hero-cta` and `.sb-cta` buttons
- `@media (prefers-reduced-motion: reduce)` disables Ken Burns and ticker animations
- **Ambient orbs** in `.final-cta` (CSS radial gradients, show-color tinted)

Main content sections order (inside `<main>`):
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

---

## Current Show-Page Benchmark — Nathan Burton

**Current benchmark/model:** `shows/magic/nathan-burton-comedy-magic/index.html`. For new show pages and major rebuilds, use Nathan Burton as the interaction, conversion, mobile UX, gallery, seating, copy-framing, and SEO benchmark. Read `SHOW-PAGE-BENCHMARK.md` first. Preserve each show's own personality and facts; reuse the system, not Nathan-specific copy.

### Descriptive show copy

Before Quick Take, include a **What is [Show]?** section that explains the actual entertainment product for someone unfamiliar with it.

- Use verified show-specific details only.
- Explain what happens onstage, the format, defining performers/elements, and what makes it distinct.
- Use natural relevant entities and concepts; do not keyword-stuff.
- Do not enforce a word minimum. Roughly 150–250 words is often enough, but simpler shows can be shorter.
- Hero = fast identification. Descriptive overview = what the customer is buying. Quick Take = whether it fits.
- Never repeat the hero sentence in the overview or turn Quick Take into another synopsis.

### Required SEO metadata package
Every rebuilt show page must include all of the following:

- Unique `<title>` targeting the show plus useful Las Vegas ticket intent
- Unique `<meta name="description">` using verified current price/venue/show facts
- `<meta name="robots" content="index,follow,max-image-preview:large">`
- Self-referencing canonical URL
- Open Graph: `og:type`, `og:site_name`, `og:title`, `og:description`, `og:image`, `og:image:alt`, `og:url`
- Twitter: `twitter:card=summary_large_image` and `twitter:image`
- Preload the primary hero image used above the fold
- JSON-LD: `EventSeries` (or `Event` when appropriate), `BreadcrumbList`, visible-FAQ-backed `FAQPage`, and `WebPage` author/date metadata
- `organizer.url` must be present; use a verified official organizer URL when known, otherwise follow the repo convention used by existing benchmark pages
- `offers.price` must be a bare numeric value with no `$`
- `offers.validFrom` is required; use the real on-sale date when known, otherwise the repo default date documented in the structured-data rules
- Structured-data image order must match the page's primary social/hero image unless explicitly directed otherwise
- Run `python3 scripts/audit-event-schema.py` before shipping and fix any issues caused by the changed page

Do not add unverifiable urgency, discounts, fee claims, delivery promises, ratings, or review counts to metadata or structured data.

---

## Building the Page (Technical Notes)

Pages are 200–350 KB of HTML. **Do not use the Edit tool for initial page creation** — build the entire file in Python and write it with `open(..., 'w').write(html)`.

When building HTML inside a Python f-string, all `{` and `}` in CSS/JS must be escaped as `{{` and `}}`.

```python
html = f"""<!DOCTYPE html>
<html>
<head>
  <style>
    :root {{
      --show: #B91C1C;
      --show-lt: #DC2626;
    }}
    .sidebar {{ position: sticky; top: 24px; }}
  </style>
</head>
</html>"""

with open('shows/family/show-name/index.html', 'w') as f:
    f.write(html)
```

---

## Color System

### Base palette (CSS custom properties — same on every page)
```css
--navy:      #0A1628   /* primary background */
--navy-mid:  #0f1e38   /* slightly lighter bg for cards */
--orange:    #FF6B2B   /* ALL CTA buttons — never deviate */
--orange-lt: #FF8C2A   /* hover/accent */
```

### Show accent color (`--show` and `--show-lt`)
Every show page defines exactly two show-specific color vars:
```css
--show:    #XXXXXX   /* dark/saturated accent */
--show-lt: #YYYYYY   /* lighter tint for hover/glow */
```

The show accent is used on:
- progress bar gradient endpoint
- `.venue-label` text color
- `.hero-subtitle` text color
- ticker strip background
- category `.pill` background
- `.spike-callout` left border
- `.details-grid .detail-card-lbl` text color
- `.expect-grid .expect-card` top border
- `.also-venue` text color
- `.t-check` icons in sidebar
- email signup bar background

**Warm Amber (`#FFB000`) is always used for ALL primary ticket CTA buttons** (`.hero-cta`, `.sb-cta`, `.mob-cta`, `.final-cta-btn`, `.zone-popup-cta`). Never put the show color on a buy button.

### Ticker text color
- If `--show` is light/bright (yellow, cyan, light gold): use `color: var(--navy)` on ticker text
- If `--show` is dark/saturated (crimson, purple, deep blue): use `color: #fff` on ticker text

### Example show colors
| Show | `--show` | `--show-lt` | Ticker text |
|---|---|---|---|
| V – Ultimate Variety | `#B91C1C` (crimson) | `#DC2626` | white |
| WOW – Vegas Spectacular | `#0891B2` (cyan) | `#22D3EE` | navy |
| Jabbawockeez | `#B8860B` (gold) | `#D4AC0D` | navy |
| BattleBots | `#DC2626` (red) | `#EF4444` | white |

---

## Fonts

- `Bebas Neue` — headlines, show titles, section titles, CTA button text
- `Barlow Condensed` — prices, labels, badges, pills
- `Barlow` — body text
- `IBM Plex Mono` — venue labels, monospace meta tags

Google Fonts link (include on every page):
```html
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Barlow+Condensed:wght@400;600;700;800&family=Barlow:ital,wght@0,400;0,500;0,600;1,400&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet" />
```

---

## Scrolling Ticker Strip

Placed immediately after the `</section>` hero close, before `.page-layout`.

```html
<div class="ticker-wrap">
  <div class="ticker-track">
    <span>⭐ Fact One</span>
    <span class="ticker-sep">◆</span>
    <span>⭐ Fact Two</span>
    <span class="ticker-sep">◆</span>
    <span>⭐ Fact Three</span>
    <span class="ticker-sep">◆</span>
    <!-- duplicate all spans for seamless loop -->
    <span>⭐ Fact One</span>
    <span class="ticker-sep">◆</span>
    ...
  </div>
</div>
```

```css
.ticker-wrap { background: var(--show); overflow: hidden; padding: 10px 0; }
.ticker-track { display: flex; gap: 32px; white-space: nowrap; animation: ticker 28s linear infinite; color: #fff; /* or var(--navy) for light shows */ font-family: var(--font-condensed); font-size: 0.82rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; }
@keyframes ticker { from { transform: translateX(0); } to { transform: translateX(-50%); } }
@media (prefers-reduced-motion: reduce) { .ticker-track { animation: none; } }
```

---

## Stats Strip (Count-Up Animation)

Placed after the ticker, or early in `<main>` before `.seen-widget`. Typically 4 stats.

```html
<div class="stats-strip">
  <div class="stat-item">
    <div class="stat-num" data-target="90" data-suffix=" min">0</div>
    <div class="stat-lbl">Show Duration</div>
  </div>
  <div class="stat-item">
    <div class="stat-num" data-target="7" data-suffix=" nights">0</div>
    <div class="stat-lbl">Per Week</div>
  </div>
  <!-- etc. -->
</div>
```

JS count-up:
```javascript
const counters = document.querySelectorAll('.stat-num');
const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (!entry.isIntersecting) return;
    const el = entry.target;
    const target = +el.dataset.target;
    const suffix = el.dataset.suffix || '';
    const prefix = el.dataset.prefix || '';
    const dur = 1400;
    const start = performance.now();
    const tick = now => {
      const p = Math.min((now - start) / dur, 1);
      const ease = 1 - Math.pow(1 - p, 3);
      el.textContent = prefix + Math.round(ease * target) + suffix;
      if (p < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
    observer.unobserve(el);
  });
}, { threshold: 0.4 });
counters.forEach(c => observer.observe(c));
```

---

## Badge System — Critical Rules

There are two distinct recommendation labels. **They are not interchangeable. Never confuse them.**

### 🪑 Sweet Spot — Seating Advice (every page)
Identifies the single best seating category for value, sightlines, or experience. This is **practical seating advice**, not an endorsement of the show itself.

- Use a **Sweet Spot** badge only when there is a defensible seating recommendation. The physical zone keeps a real location name (for example, Center section); Sweet Spot / Our Pick is a recommendation label, not the zone name.
- Appears in the seat accordion as a highlighted row with a "🪑 Sweet Spot" badge
- Appears in the zone popup when that zone is selected (`pick: true` in `ZONES`)
- Can be mentioned in the seating section prose ("For most visitors, [Zone] is the sweet spot")
- This badge is about where to sit — it says nothing about whether the show is worth seeing

### ⭐ Sidekick Pick — Show Endorsement (explicit only)
A selective, show-level endorsement. Means Vegas Sidekick actively recommends this show above others in its category.

- **Only add when explicitly instructed** — never add by default
- Never infer it from show quality, ratings, or descriptions
- Never suggest adding it unless asked
- If uncertain whether a show qualifies, **ask — do not assume**

When instructed to add Sidekick Pick:
- Add `⭐ Sidekick Pick` pill to `.info-pills` in the hero
- Add `<div class="card-best-badge">⭐ Sidekick Pick</div>` to the show card in `shows/index.html`
- Include `.spike-callout` in the About section with `<strong>⭐ Sidekick Pick</strong>` label

**Summary table:**

| Badge | Every page? | What it means | When to add |
|---|---|---|---|
| 🪑 Sweet Spot | Yes — always | Best zone to sit | Every page, seating section |
| ⭐ Sidekick Pick | No — selective | We recommend this show | Only when explicitly told to |

---

## Seating Charts (SVG)

### Traditional proscenium rows (e.g., V – Ultimate Variety Show)

Rectangular stage at top. Rows as rectangles in named zones. Label each zone.

### Horseshoe arc (e.g., WOW – The Vegas Spectacular)

Use Python math to generate SVG arc paths. Center point below SVG bottom so arcs curve upward:

```python
import math

cx, cy = 340, 490  # center below SVG bottom (SVG height 480)
A_S, A_E = 205, 335  # fan angle span (degrees)

def arc(r_in, r_out, a_start, a_end):
    s = math.radians(a_start); e = math.radians(a_end)
    ox1=cx+r_out*math.cos(s); oy1=cy+r_out*math.sin(s)
    ox2=cx+r_out*math.cos(e); oy2=cy+r_out*math.sin(e)
    ix1=cx+r_in*math.cos(s);  iy1=cy+r_in*math.sin(s)
    ix2=cx+r_in*math.cos(e);  iy2=cy+r_in*math.sin(e)
    span = a_end - a_start; large = 1 if span > 180 else 0
    return (f"M {ox1:.1f} {oy1:.1f} A {r_out} {r_out} 0 {large} 1 {ox2:.1f} {oy2:.1f} "
            f"L {ix2:.1f} {iy2:.1f} A {r_in} {r_in} 0 {large} 0 {ix1:.1f} {iy1:.1f} Z")

def mid_xy(r_in, r_out, deg=270):
    r = (r_in + r_out) / 2; a = math.radians(deg)
    return cx + r * math.cos(a), cy + r * math.sin(a)

vip_path       = arc(88,  148, A_S, A_E)   # innermost — magenta #D946EF
premium_path   = arc(148, 213, A_S, A_E)   # gold #D4AC0D
preferred_path = arc(213, 275, A_S, A_E)   # green #22C55E — Sweet Spot
reserved_path  = arc(275, 328, A_S, A_E)   # blue #3A74B5 — outermost

# Use mid_xy(r_in, r_out, deg=270) to position zone labels at top of each arc
```

### Zone popup (identical on every page)

```html
<div class="zone-popup" id="zonePopup">
  <div class="zone-popup-hdr">
    <div class="zone-popup-name" id="zoneName">—</div>
    <div class="zone-popup-pick" id="zonePick" style="display:none">🪑 Sweet Spot</div>
  </div>
  <div class="zone-popup-desc" id="zoneDesc"></div>
  <a href="[AFFILIATE_LINK]" class="zone-popup-cta" target="_blank" rel="noopener">Get Tickets in This Zone →</a>
</div>
```

JS:
```javascript
const ZONES = {
  vip:       { name: 'VIP', pick: false, desc: '...' },
  preferred: { name: 'Preferred', pick: true,  desc: '...' },  // pick:true = Sweet Spot
};
function selectZone(id) {
  const z = ZONES[id];
  document.getElementById('zoneName').textContent = z.name;
  document.getElementById('zoneDesc').textContent = z.desc;
  document.getElementById('zonePick').style.display = z.pick ? 'inline-block' : 'none';
  const popup = document.getElementById('zonePopup');
  popup.classList.add('visible');
  popup.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}
```

### Seat accordion

```html
<div class="seat-accord">
  <div class="seat-accord-row" onclick="selectZone('preferred')">
    <div class="seat-accord-dot" style="background:#22C55E"></div>
    <div class="seat-accord-name">Preferred <span class="seat-accord-badge">🪑 Sweet Spot</span></div>
    <div class="seat-accord-price">From $XX</div>
  </div>
</div>
```

---

## Hero Slider (Ken Burns)

3 images, 16:9 aspect ratio, Ken Burns zoom animation, auto-advance every 5s, 6-dot nav.

```html
<div class="hero-slider">
  <div class="slide active" style="background-image:url('/images/{slug}-hero.jpg')"></div>
  <div class="slide" style="background-image:url('/images/{slug}-2.jpg')"></div>
  <div class="slide" style="background-image:url('/images/{slug}-3.jpg')"></div>
  <div class="slide-dots">
    <span class="dot active" onclick="goSlide(0)"></span>
    <span class="dot" onclick="goSlide(1)"></span>
    <span class="dot" onclick="goSlide(2)"></span>
  </div>
</div>
```

```css
.slide { position:absolute; inset:0; background-size:cover; background-position:center; opacity:0; transition:opacity 0.8s; }
.slide.active { opacity:1; animation: kenBurns 10s ease-in-out infinite alternate; }
@keyframes kenBurns { from{transform:scale(1)} to{transform:scale(1.06)} }
@media (prefers-reduced-motion: reduce) { .slide.active { animation: none; } }
```

JS:
```javascript
let slideIdx = 0;
const slides = document.querySelectorAll('.slide');
const dots = document.querySelectorAll('.dot');
function goSlide(n) {
  slides[slideIdx].classList.remove('active');
  dots[slideIdx].classList.remove('active');
  slideIdx = n;
  slides[slideIdx].classList.add('active');
  dots[slideIdx].classList.add('active');
}
setInterval(() => goSlide((slideIdx + 1) % slides.length), 5000);
```

---

## Info Pills

```html
<div class="info-pills">
  <span class="pill pill-show">✨ Comedy</span>
  <span class="pill">⏱ 75 Min</span>
  <span class="pill pill-pick">⭐ Sidekick Pick</span>   <!-- ONLY if explicitly instructed -->
  <span class="pill">📍 Venue Name</span>
  <span class="pill">🔞 18+</span>
</div>
```

---

## Urgency Pills (animated dots)

```html
<div class="urgency-pills">
  <div class="upill"><span class="udot"></span>Mon–Sun · 8:30 PM &amp; 10:30 PM</div>
</div>
```

```css
.upill { display:inline-flex; align-items:center; gap:5px; padding:4px 10px; border-radius:6px; font-family:var(--font-mono); font-size:0.63rem; background:rgba(255,107,0,0.09); color:var(--orange-lt); border:1px solid rgba(255,107,0,0.2); }
.udot { width:5px; height:5px; border-radius:50%; background:var(--orange); animation:blink 1.6s infinite; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.36} }
```

## Urgency Copy — Locked

❌ **Never use generic urgency:** "selling fast," "prices may increase," "book early," fake countdowns, fake social proof, fabricated scarcity, or made-up reviews.
✅ **Use current facts instead:** price, date, showtime, dark days, verified availability status, closure/extension status, and practical seat guidance.

---

## Seen Widget

```html
<div class="seen-widget fade-up">
  <div class="seen-tag">🌵 Spike Wants to Know</div>
  <div class="seen-q">Have you seen [Show Name] before?</div>
  <div class="seen-btns">
    <button class="seen-btn seen-yes" onclick="showSeen('yes')">Yeah, I've been</button>
    <button class="seen-btn seen-no" onclick="showSeen('no')">First time</button>
  </div>
  <div class="seen-resp" id="seen-yes">
    <p>Encouraging repeat-visitor message. <a href="[AFFILIATE_LINK]" target="_blank" rel="noopener">Grab tickets →</a></p>
  </div>
  <div class="seen-resp" id="seen-no">
    <p>Enthusiastic first-timer pitch. <a href="[AFFILIATE_LINK]" target="_blank" rel="noopener">Get your tickets →</a></p>
  </div>
</div>
```

JS: `function showSeen(id) { document.querySelectorAll('.seen-resp').forEach(el => el.classList.remove('visible')); document.getElementById('seen-' + id).classList.add('visible'); }`

The `.seen-resp a` links must be **orange** (`color: var(--orange)`).

---

## Trust Grid (4 cards, always identical)

Copy these exactly — wording is locked. Never name the ticketing partner anywhere in these cards.

```html
<div class="trust-grid fade-up">
  <div class="trust-card"><div class="trust-icon">🎟️</div><div class="trust-title">Useful Ticket Details</div><div class="trust-body">Show the current price, schedule, venue and practical booking context without unsupported checkout claims.</div></div>
  <div class="trust-card"><div class="trust-icon">⚡</div><div class="trust-title">Instant Delivery</div><div class="trust-body">Tickets arrive by email immediately after purchase. No will-call, no waiting.</div></div>
  <div class="trust-card"><div class="trust-icon">🌵</div><div class="trust-title">Useful Context</div><div class="trust-body">Say who the show fits, what to know first and one useful caveat when it matters.</div></div>
  <div class="trust-card"><div class="trust-icon">🎫</div><div class="trust-title">No Account Required</div><div class="trust-body">Buy without creating an account. Fast, clean, tickets straight to your inbox.</div></div>
</div>
```

---

## Email Signup (inline in main content)

```html
<div class="email-signup fade-up">
  <div class="email-signup-text">
    <div class="email-signup-title">Get Vegas Deals in Your Inbox</div>
    <div class="email-signup-sub">Last-minute discounts, show alerts, and picks from someone who actually lives here.</div>
  </div>
  <div class="email-form-wrap">
    <input type="email" id="emailInp" placeholder="your@email.com" />
    <button id="emailBtn" onclick="submitEmail()">Get Free Deals 🎟️</button>
    <div class="email-success" id="emailSuccess">✅ You're in!</div>
  </div>
</div>
```

JS:
```javascript
async function submitEmail() {
  const inp = document.getElementById('emailInp');
  const email = inp.value.trim();
  if (!email || !email.includes('@')) return;
  document.getElementById('emailBtn').disabled = true;
  try {
    await fetch('https://subscribe.vegassidekick.com', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email })
    });
  } catch(e) {}
  inp.style.display = 'none';
  document.getElementById('emailBtn').style.display = 'none';
  document.getElementById('emailSuccess').classList.add('visible');
}
```

---

## FAQ Accordion

```html
<div class="faq-list">
  <div class="faq-item">
    <button class="faq-q" onclick="toggleFaq(this)">Question text? <span class="faq-icon">+</span></button>
    <div class="faq-a"><p>Answer text.</p></div>
  </div>
</div>
```

JS: `function toggleFaq(btn) { const item = btn.parentElement; const wasOpen = item.classList.contains('open'); document.querySelectorAll('.faq-item.open').forEach(el => el.classList.remove('open')); if (!wasOpen) item.classList.add('open'); }`

Standard FAQ questions for every show (adapt answers per show):
1. Where do I pick up my tickets?
2. Is there parking?
3. Are there any age restrictions?
4. What's the photography/recording policy?
5. Can I get a refund or exchange if my plans change?
6. What should I wear?
7. How early should I arrive?
8. [Show-specific Q]

**Refund answer (always use this exact language):**
> "Refunds are available for exceptional circumstances such as the unlikely event that a show cancels. Check the full terms and conditions before purchasing."

---

## "You Might Also Like" Cards (.also-grid)

3 cards linking to other existing show pages. Use shows from the same or adjacent category.

```html
<div class="also-grid">
  <a href="/shows/{category}/{slug}/" class="also-card" target="_blank">
    <div class="also-img" style="background-image:url('/images/{slug}-hero.jpg')"></div>
    <div class="also-body">
      <div class="also-venue">Venue Name</div>
      <div class="also-name">Show Name</div>
      <div class="also-price">From $XX</div>
    </div>
  </a>
</div>
```

---

## Image Handling

Images live in `/images/` and are referenced with root-relative paths.

**`cwebp` is NOT available in this environment.** Use PIL instead:

```python
from PIL import Image

# Crop to 16:9 and resize for hero/listing card
src = "uploaded-photo.jpg"
img = Image.open(src).convert("RGB")
w, h = img.size
target_h = int(w * 9 / 16)
img = img.crop((0, (h - target_h) // 2, w, (h - target_h) // 2 + target_h))
img = img.resize((1200, 675), Image.LANCZOS)
img.save("images/show-name-hero.jpg", format="JPEG", quality=82, optimize=True)
```

For slider images embedded as data URLs (when MCP push is needed):
```python
import base64, io
img.save(buf := io.BytesIO(), "webp", quality=65)
data_url = "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()
# Use as background-image: url('data:image/webp;base64,...') in HTML
```

**Size targets:**
- Listing card JPEG: aim for <200KB
- Slider data URL WebP: aim for <80KB binary (~107KB data URL) each
- Total HTML file: keep under 500KB

**OG/social preview images** require a real hosted URL (crawlers can't use data URLs). Upload via GitHub web UI or git push.

---

## Files to Create / Update for Every New Show

### Always CREATE:
- `shows/{category}/{show-slug}/index.html`

### Always UPDATE:
| File | What to change |
|---|---|
| `shows/index.html` | Add entry to JS data array (increment `order`, add all data attributes), add to `defaultOrder` array |
| `shows/{category}/index.html` | Add entry to category page data array |
| `sitemap.xml` | Add `<url>` entry with `<lastmod>` (today's date) |

### Update if show should appear on homepage:
- `index.html` — add card to the relevant section (**always check `git log index.html` before touching this file**)

### Create IF new category:
- `shows/{category}/index.html` — category landing page
- Update `components/header.js` — add nav link
- Update `components/footer.js` — add footer column link

---

## Show Card Data (for shows/index.html)

Data object pattern:
```javascript
{ order:39, slug:'show-name', cat:'comedy', name:'Show Name', subtitle:'', venue:'Venue · Hotel',
  price:41, pd:'$41', sp:false,  // sp:true = Sidekick Pick badge — explicit only
  pills:['Award 2024','Tag Two'],
  img:'/images/show-name-hero.jpg',
  duration:'90 min', age:'All ages', schedule:'Tue–Sun · 7:30 PM' }
```

`cat` values: `comedy` `magic` `cirque` `adult` `music` `spectacular` `family`

---

## Open Graph / Schema (head block)

```html
<title>Show Name Tickets 2026 | Venue · Hotel | Vegas Sidekick</title>
<meta name="description" content="Show Name tickets from $XX. [One punchy sentence]. [Venue]." />
<link rel="canonical" href="https://vegassidekick.com/shows/{category}/{slug}/" />
<meta property="og:title" content="Show Name | Vegas Sidekick" />
<meta property="og:description" content="[One punchy sentence]. From $XX at [Venue]." />
<meta property="og:image" content="https://vegassidekick.com/images/{slug}-hero.jpg" />
<meta property="og:url" content="https://vegassidekick.com/shows/{category}/{slug}/" />
<meta property="og:type" content="website" />
<meta property="og:site_name" content="Vegas Sidekick" />
<meta name="twitter:card" content="summary_large_image" />
```

Schema (EventSeries type):
```json
{
  "@context": "https://schema.org",
  "@type": "EventSeries",
  "name": "Show Name",
  "description": "...",
  "image": "https://vegassidekick.com/images/{slug}-hero.jpg",
  "url": "https://vegassidekick.com/shows/{category}/{slug}/",
  "eventStatus": "https://schema.org/EventScheduled",
  "organizer": { "@type": "Organization", "name": "Show Name at Venue" },
  "location": {
    "@type": "Place",
    "name": "Venue",
    "address": { "@type": "PostalAddress", "streetAddress": "...", "addressLocality": "Las Vegas", "addressRegion": "NV", "postalCode": "...", "addressCountry": "US" }
  },
  "offers": {
    "@type": "Offer",
    "url": "https://spotlight.vegas/shows/...",
    "price": "XX",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock"
  }
}
```

---

## Content Rules

1. **No partner branding in copy** — Never write "Spotlight.vegas" or any ticket partner name in visible text. Affiliate links themselves are fine.
2. **No "choose your seats"** — Don't use this as a CTA phrase.
3. **No upsell language** — Don't write "upgrade to VIP" or push spending more.
4. **No intermission** — Most shows have none; confirm before writing "no intermission."
5. **Sidekick Pick** — Only add if user explicitly says "add Sidekick Pick." See badge system rules above.
6. **Sweet Spot** — Every page gets exactly one. Goes in seating section. About seating advice, not show endorsement.
7. **Refund FAQ** — Always use the exact generic language in the FAQ section above.
8. **Age policy** — Copy exactly from user's brief; it varies significantly per show.
9. **Prices** — "Our price" is the affiliate price; "box office price" is the strikethrough comparison price.
10. **Photography default** — Unless the brief specifies otherwise, use: *"Still photos are generally welcome — check with your usher before shooting. No flash photography and no video recording. Ushers may ask you to stop at any time."*
11. **Urgency copy** — Only ever write "Prices **may** increase closer to show date." Never drop "may." Never add countdown timers, fake scarcity, or fabricated social proof.
12. **Affiliate URL must be provided exactly** — Do not guess the category slug. It does not always match the site category (e.g., WOW uses `production/wow-the-vegas-spectacular`, not `spectaculars/wow-the-vegas-spectacular`).

---

## Header & Footer Components

Every page needs both placeholder divs and both script tags:

```html
<body>
  <div id="vs-header"></div>          ← TOP of body (required)
  <!-- all page content -->
  <div id="vs-footer"></div>          ← before scripts
  <script src="/components/header.js"></script>
  <script src="/components/footer.js"></script>
</body>
```

`header.js` also injects Google Analytics (G-BM6QGF7B4Y) — no need to add it separately.

---

## The Brief Template

When starting a new show, provide this exact brief:

```
Show Name:
Category: (comedy / magic / cirque / spectacular / family / adult / music)
Affiliate URL: https://spotlight.vegas/shows/.../ref/vegassidekick

Venue + Hotel:
Address: (street address for schema)
Schedule: (list every day + every show time)
Duration:
Age restriction:
Other restrictions: (photography, recording, dress code)
Warnings: (strobe, pyrotechnics, loud noise, haze, etc.)

Our price (affiliate): $
Box office / comparison price: $
Save amount: $

Sidekick Pick show: yes / no  ← show-level endorsement
Sweet Spot seats: (zone name — the one best zone for most visitors)

Seating zones: (name, color, seat count/description for each)
Seating layout: (comedy-club / theater-proscenium / theater-in-the-round / arena-horseshoe / other)

About / description: (2–3 paragraphs of show content)
"What to Expect" highlights: (3–6 key bullet points)
FAQ specifics: (anything show-unique beyond standard questions)
"You Might Also Like" shows: (3 shows with existing pages)

Images: 3 attached — hero + 2 more
```

---

## Git Workflow

```bash
# Stage specific files — never use git add -A
git add shows/family/show-name/index.html images/show-name-hero.jpg

# Commit
git commit -m "Add Show Name show page"

# Push to feature branch
git push -u origin claude/feature-name-<id>
```

After pushing to `main`, Cloudflare Pages deploys automatically. No other steps needed.

---

## Current Show Pages (as of 2026-05-31)

### Comedy (`/shows/comedy/`)
| Show | URL | Our Price |
|---|---|---|
| Carrot Top | /shows/comedy/carrot-top/ | — |
| Laugh Factory | /shows/comedy/laugh-factory/ | $32 |
| Comedy Cellar | /shows/comedy/comedy-cellar/ | $41 |
| Brad Garrett's Comedy Club | /shows/comedy/brad-garretts-comedy-club/ | $51 |
| Marc Savard Comedy Hypnosis | /shows/comedy/marc-savard-comedy-hypnosis/ | $28 |
| Tape Face | /shows/comedy/tape-face/ | $57 |
| Popovich Comedy Pet Theater | /shows/comedy/popovich-comedy-pet-theater/ | $31 |
| LA Comedy Club | /shows/comedy/la-comedy-club/ | $43 |
| Las Vegas LIVE Comedy Club | /shows/comedy/las-vegas-live-comedy-club/ | $30 |
| Marriage Can Be Murder | /shows/comedy/marriage-can-be-murder/ | $95 |

### Magic (`/shows/magic/`)
| Show | URL | Our Price |
|---|---|---|
| Mac King | /shows/magic/mac-king/ | $33 |
| Nathan Burton Comedy Magic | /shows/magic/nathan-burton-comedy-magic/ | $28 |
| Criss Angel MINDFREAK | /shows/magic/criss-angel/ | $117 |
| Shin Lim: LIMITLESS | /shows/magic/shin-lim/ | $67 |
| Penn & Teller | /shows/magic/penn-and-teller/ | $90 |
| Allstars of Magic | /shows/magic/allstars-of-magic/ | $31 |
| Mat Franco | /shows/magic/mat-franco/ | $57 |
| The Mentalist | /shows/magic/the-mentalist/ | $40 |
| Colin Cloud | /shows/magic/colin-cloud/ | $51 |

### Cirque & Acrobatic (`/shows/cirque/`)
| Show | URL | Our Price |
|---|---|---|
| Mad Apple | /shows/cirque/mad-apple/ | CLOSED Sep 5, 2026 |
| O by Cirque du Soleil | /shows/cirque/o/ | $119 |
| KÀ by Cirque du Soleil | /shows/cirque/ka/ | — |
| Michael Jackson ONE | /shows/cirque/michael-jackson-one/ | — |
| Mystère | /shows/cirque/mystere/ | — |

### Spectaculars (`/shows/spectaculars/`)
| Show | URL | Our Price |
|---|---|---|
| Awakening | /shows/spectaculars/awakening/ | $70 |
| WOW – The Vegas Spectacular | /shows/spectaculars/wow-the-vegas-spectacular/ | $41 |

### Family (`/shows/family/`)
| Show | URL | Our Price |
|---|---|---|
| Tournament of Kings | /shows/family/tournament-of-kings/ | $78 |
| BattleBots: Destruct-A-Thon | /shows/family/battlebots-destruct-a-thon/ | — |
| V – The Ultimate Variety Show | /shows/family/v-the-ultimate-variety-show/ | $39 |
| WOW – The Vegas Spectacular | /shows/family/wow-the-vegas-spectacular/ → redirects to spectaculars | $41 |

### Adult (`/shows/adult/`)
| Show | URL | Our Price |
|---|---|---|
| Absinthe | /shows/adult/absinthe/ | $122 |
| Rouge | /shows/adult/rouge/ | $119 |
| Magic Mike Live | /shows/adult/magic-mike-live/ | — |
| Thunder from Down Under | /shows/adult/thunder-from-down-under/ | — |

### Music & Variety (`/shows/music/`)
| Show | URL | Our Price |
|---|---|---|
| VEGAS! The Show | /shows/music/vegas-the-show/ | $55 |
| Blue Man Group | /shows/music/blue-man-group/ | $68 |
| Jabbawockeez | /shows/music/jabbawockeez/ | — |

---

## Category Landing Pages (all exist)

| Category | URL |
|---|---|
| Comedy | /shows/comedy/ |
| Magic | /shows/magic/ |
| Cirque & Acrobatic | /shows/cirque/ |
| Music & Variety | /shows/music/ |
| Spectaculars | /shows/spectaculars/ |
| Family | /shows/family/ |
| Adult | /shows/adult/ |
| All Shows | /shows/ |

---

## What a Correct Page Looks Like

A correctly built show page:
- Uses `shows/family/v-the-ultimate-variety-show/index.html` as its structural template (Sidekick Build)
- Has dual scroll progress bars, Ken Burns hero slider, scrolling ticker, stats count-up
- Uses `--show` and `--show-lt` CSS vars for the show accent color throughout
- Uses orange (`--orange`) for ALL CTA buttons — never the show color on a buy button
- Has a working interactive seating SVG with zone popup and seat accordion
- Has exactly one 🪑 Sweet Spot callout in the seating section
- Has ⭐ Sidekick Pick badge only if explicitly instructed
- Contains no mentions of any ticket partner name in visible text
- Has 6–8 FAQ items including the standard refund language
- Has exactly 3 "You Might Also Like" cards linking to real existing pages
- Has `@media (prefers-reduced-motion: reduce)` disabling Ken Burns and ticker animations

---

*Last updated: 2026-09-07*


### Decision-card standard (September 2026)
Use **Good fit** as the core buyer decision aid inside **Quick Take**. On desktop it should use the shared compact horizontal treatment; do not create a second **Who it fits best** / **Good fit** section later in the page. **Booking tip** and **Good to know** are optional. Add a Booking tip only when there is a concrete, show-specific seat, timing, arrival, value, or planning action. Add Good to know only when there is useful, show-specific context. Omit either rather than filling space with generic advice. Never use the retired labels **Book it if…**, **Know this first**, or **Best practical angle**.


---

## Ticket Savings / Deal Treatment

When the Show Database contains both a verified Vegas Sidekick price and a verified regular/list price, calculate savings rather than writing a discount manually.

- Minimum customer-facing deal threshold: **$5**.
- `savings_amount = regular_price - our_price`.
- `savings_percent = round(savings_amount / regular_price * 100)`.
- Lead with **Save $X**; percentage savings is secondary.
- Show the regular price struck through only when the comparison is current and defensible.
- If no valid regular price exists, do not imply a discount.
- Never use fake scarcity, countdowns, or “limited time” language unless independently verified.
- Warm Amber (`#FFB000`) is the sitewide visual language for primary ticket actions and deal/value emphasis. Pink remains brand/accent.
- Reuse `assets/show-savings.css` and the existing savings system instead of creating page-specific deal styling.
- Run `python3 scripts/audit-savings-system.py` when show pricing or savings surfaces change.

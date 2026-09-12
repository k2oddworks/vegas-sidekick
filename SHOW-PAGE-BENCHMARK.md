# Vegas Sidekick — Show Page Benchmark

**Current benchmark:** `shows/magic/nathan-burton-comedy-magic/index.html`  
**Locked:** September 12, 2026  
**Status:** Governing UX / copy / interaction benchmark for active show product pages.

If an older template, benchmark, prompt, or example conflicts with this document or the current Nathan Burton page, **Nathan Burton wins**, except where a newer locked shared system is explicitly documented here.

The current shared showtimes booking module is newer than Nathan Burton’s original day-card schedule treatment and supersedes that older showtimes pattern.

This document defines the system. Do not copy Nathan-specific show facts into another page.

---

## 1. Core principle

A Vegas Sidekick show page should help a customer feel confident choosing a show and a ticket without hype, filler, fake urgency, or unnecessary doubt.

The page should feel like a knowledgeable Vegas local who works in tickets helping a friend make a good choice.

Use the shared canonical show system (`assets/show-canonical.css`, `assets/show-canonical.js`, current show data, shared audits). Reuse the system, not a show-specific skin.

---

## 2. Standard page flow

Preferred active-show flow:

1. Hero
2. Four quick facts
3. Seamless ticker
4. Sticky section navigation
5. Quick Take
6. Photos
7. Seat Guide when useful
8. Good Fit / useful fit guidance
9. Showtimes / booking module
10. FAQ
11. Related shows
12. Next useful click
13. Kris author card + freshness + disclosure
14. Final ticket CTA
15. Mobile sticky ticket bar

Do not add sections just because a template has room for them. Empty-calorie UI is worse than a shorter page.

---

## 3. Hero

### Desktop

- Hero image and copy may visually bleed together through a controlled gradient instead of feeling like two unrelated boxes.
- Protect the performer / show logo focal point. Do not let a desktop crop turn the image into a giant fragment of text or cut the performer out.
- Per-show focal positioning is allowed and expected.

### Mobile

- Keep the established safe mobile hero treatment.
- Preserve important artwork, logos, and performers rather than forcing `object-fit: cover`.
- Fix unusual art through per-show focal positioning before changing the global mobile system.

---

## 4. Ticket price language

Preferred visible price language:

**Tickets start at $X. Other price points may be available.**

Do not use:

- “Your date and seat determine the final total.”
- legalistic or defensive price disclaimers
- fake urgency or scarcity

Primary ticket CTAs use **Warm Amber `#FFB000`**.

---

## 5. Freshness language

Use one visible freshness signal near the Kris author card:

**Show info confirmed September 2026**

Rules:

- Month + year is enough for visible customer copy.
- Do not duplicate “Reviewed by...” / “Last reviewed...” elsewhere on the page.
- Keep exact machine-readable dates in `WebPage.dateModified`, `lastReviewed`, sitemap `lastmod`, or other structured systems as appropriate.
- Freshness does not need to sit next to the hero price.

---

## 6. Quick facts, schedule labels, and the locked showtimes booking system

Use confident quick-fact labels:

- **Start time** — one reliable time
- **Start times** — multiple reliable times
- **Start times · Varies** — genuinely variable schedule

Do not use **Typical start**.

### Shared showtimes assets

The production showtimes system is shared and reusable:

- `assets/showtimes-booking.css`
- `assets/showtimes-booking.js`
- current verified schedule data in `data/show-database.json`

Do not copy show-specific CSS/JS for the booking module unless there is a genuine exception that cannot be handled by the shared system.

### Verified regular weekly schedules

When the show has a verified regular weekly schedule, use the shared conversion-focused booking module rather than the old large day-card grid.

The module should include:

- **Pick your night** eyebrow
- **Find your showtime** headline
- concise verified weekly schedule summary
- all seven weekday choices in one compact row / picker
- active show days selectable
- verified dark days visibly muted and labeled **Dark**
- selected day highlighted in purple
- showtime choices displayed immediately for the selected day
- each showtime linked to the existing verified affiliate URL
- one dominant Warm Amber **Get Tickets for [day] →** CTA
- one substantial filled-lavender **View all dates & times →** secondary CTA
- a compact **Planning ahead? You can book tickets weeks and months in advance.** card
- the shared decorative Vegas dusk / skyline / Sphere artwork at the bottom, with **no slogan**

The hierarchy matters:

1. Pick a day.
2. See the times.
3. Take the amber ticket action.
4. Use **View all dates & times →** for future dates or broader inventory.

Do not make every day its own oversized card. Do not turn the section back into a timetable wall.

### Variable schedules

If the schedule genuinely varies by date, do not fabricate recurring weekday buttons or recurring times.

Use the variable-date version of the shared module:

- clearly state **Schedule varies by date**
- use **See available dates & times →** as the primary ticket action
- retain the planning-ahead treatment and shared artwork
- link only to the existing verified affiliate URL

### Source-of-truth requirement

The show database schedule is the source of truth for the picker and time choices. Keep the page, structured data, database, and catalogs aligned so stale schedule information cannot regenerate later.

---

## 7. Ticker

The ticker must be a truly seamless loop on desktop and mobile.

- Duplicate the full ticker set so the animation does not reveal blank space.
- Respect `prefers-reduced-motion`.
- Ticker facts must be verified and useful.

---

## 8. Quick Take, Good Fit, and Kris’s take

### Positive decision framing

Vegas Sidekick can be candid without planting objections.

Do not use formal recurring sections or labels such as:

- Think twice
- The downside
- Honest downside
- Reasons to skip

### Good Fit

- Explain who the show works well for.
- Keep it compact when there is only one useful point.
- Do not leave a tiny Good Fit sentence stranded in a giant desktop side rail.

### Good to know

Only use **Good to know** for a real fact worth knowing before purchase, such as:

- age restriction
- unusual venue setup
- sensory issue
- audience-participation rule that has been explicitly confirmed
- meaningful format or access limitation

Do not relabel old rejection copy as “Good to know.” If there is no useful fact, omit the card.

### Kris’s take

Kris’s take should strengthen the customer’s understanding of why the show is a good choice. It can mention a practical advantage or a distinctive reason to choose it.

Do not use Kris’s take to introduce generic doubt such as “if you actually want another kind of night...” Comparison links can exist elsewhere under positive framing such as **Also worth a look** or related-show modules.

Never invent first-hand attendance or experience.

---

## 9. Language rules from the Nathan benchmark

### Do not use “tradeoff” in customer-facing copy

Prefer positive, useful language such as:

- Tap a section to see what it offers.
- Compare seating sections.
- See the view and value of each section.

A lower-priced rear section should be framed around what it **does well** when that is supportable: clear full-stage view, straight-on sightline, best price, etc.

### Do not narrate obvious interface behavior

Remove filler such as:

- “Use the photos and seating chart together before you choose.”
- instructions telling customers to look at photos
- explanatory UI text that adds no decision value

### Do not imply interaction unless Kris explicitly confirms it

Do not describe a show or seating area as:

- interactive
- in on the action
- part of the action
- likely to get picked / brought onstage
- audience-participation-heavy

unless Kris has explicitly confirmed that fact for that show.

This is especially important for hypnosis, comedy, magic, and close-to-stage seating. Do not infer participation from genre or seat location.

---

## 10. Booking tip rule

**Booking tip is optional.**

Keep it only when it gives a concrete, show-specific action, for example:

- when to arrive
- how a showtime fits around dinner
- which section is worth paying for
- when a cheaper section is still a strong choice

If the tip is generic category copy or merely describes a seat, remove it. Never create filler to preserve a layout.

---

## 11. Photo gallery

Nathan Burton is the gallery interaction benchmark.

### Page gallery

- Multiple photos should remain visible on desktop; one unusual portrait or seating-chart asset must not distort the whole gallery.
- Use consistent gallery frames / aspect handling (`object-fit` as appropriate).
- A tall seating chart can use `contain` inside its gallery tile.
- Remove instructional sentences telling users to inspect the photos.

### Lightbox

When a photo opens:

- desktop: visible previous / next controls
- keyboard: left / right arrows
- mobile: swipe left / right
- show a subtle image count (for example `2 of 4`)
- user should not need to close one photo to open the next

Preserve useful `alt` text on the original on-page images.

---

## 12. Seating-chart system

Nathan Burton Theater is the first locked example of the reusable seating system.

### Architecture: room first, show second

Model seating as:

**Show → Venue / showroom → shared room layout → show-specific recommendation copy**

If two shows use the same room, they should share the same geometry. Their recommendation wording may differ.

Do not redraw the same theater independently on every show page.

### Geometry

- The branded chart should visibly resemble the real room.
- Preserve distinctive shapes: side pockets, straight or curved blocks, balconies, aisles, etc.
- Accuracy of the room silhouette matters more than decorative symmetry.
- Do not use a generic three-rectangle chart for every theater.

### Slab-row convention

When exact seat counts are not verified or do not add value, represent each row as a **slab**, not individual seats.

This avoids pretending to know exact seat counts while still showing the room accurately.

### Zone naming

Separate the physical section name from the recommendation badge.

Example:

- Section name: **Center section**
- Badge: **Sweet spot**
- Recommendation emphasis: amber **Our Pick**

Do not name the physical seating zone itself “Sweet Spot.”

### Color meaning

Use brand colors consistently rather than randomly:

- Warm Amber — Our Pick / recommendation emphasis
- Purple — core middle seating
- Pink / magenta — front / close seating
- Teal / green — rear / value seating
- Near-black — stage / structure

The exact number of zones can vary by room.

### Interaction

- The chart remains clickable / tappable.
- Selecting a zone updates its description and visual highlight.
- On mobile, the selected-zone explanation must appear immediately in view (popover / compact card near the sticky ticket bar or chart). Do not require the user to tap and then hunt below the fold for the result.
- Zone copy should explain what the section offers, not frame it as a compromise.

### Disclaimers

Do **not** add a generic seating disclaimer merely to say not every seat is always available or that the diagram is simplified.

Only add a disclaimer when there is a genuine unusual limitation a customer needs to understand.

### Static seating-chart gallery asset

For useful room layouts, generate a matching static seating-chart graphic from the **same underlying geometry/data** used by the interactive chart.

- dark noir / Vegas Sidekick visual treatment is approved
- use a descriptive filename
- use show-specific descriptive alt text
- include venue name and verified address where useful
- do not invent rows or seat counts
- static and interactive charts must not drift apart

The static chart is a UX/content asset first; any SEO value is secondary.

---

## 13. SEO and structured data

Every active rebuilt show page should include, where appropriate:

- unique title and meta description using verified facts
- `robots=index,follow,max-image-preview:large`
- self-referencing canonical
- Open Graph title / description / image / image alt / URL
- Twitter large image metadata
- appropriate `Event` / `EventSeries` schema
- `BreadcrumbList`
- visible-FAQ-backed `FAQPage` when FAQ schema is used
- `WebPage` author + exact modification / review dates

Rules:

- `offers.price` is a bare number, no `$`
- do not fabricate schedules
- do not add unsupported urgency, discount, fee, rating, or review claims
- do not invent official video or affiliate URLs
- keep structured-data facts aligned with visible content

Run the current repo audits after meaningful show-page changes, especially:

- `python3 scripts/audit-event-schema.py`
- `python3 scripts/audit-ticket-cta-color.py`
- `python3 scripts/audit-mobile-show-heroes.py`
- `python3 scripts/audit-catalog-js-syntax.py`
- `git diff --check`

Use other active audits when the change touches their domain.

---

## 14. Locked reusable benchmark assets

### Seating

Current reusable room implementation:

- `data/seat-layouts/nathan-burton-theater.json`
- `assets/seat-layouts/nathan-burton-theater.css`
- `assets/seat-layouts/nathan-burton-theater.js`
- `images/nathan-burton-theater-seating-chart.svg`
- `scripts/generate-seat-layout-assets.py`

When expanding this system to another show in the same room, reuse the room geometry and change only the show-specific recommendation/content layer as needed.

### Showtimes

Current reusable showtimes implementation:

- `assets/showtimes-booking.css`
- `assets/showtimes-booking.js`
- verified schedule data in `data/show-database.json`

Use this shared showtimes system across active show pages. Do not resurrect older day-card schedule grids unless Kris explicitly changes the benchmark.

### Current benchmark page

- `shows/magic/nathan-burton-comedy-magic/index.html`

Nathan Burton remains the overall page benchmark, while the newer shared showtimes module governs the Showtimes section.

---

## 15. Precedence

For active show-page work, use this order when instructions conflict:

1. Explicit current instruction from Kris
2. Newer locked shared systems explicitly documented in this benchmark
3. Current production Nathan Burton benchmark page
4. `SHOW-PAGE-BENCHMARK.md`
5. Vegas Sidekick Brand Bible / `BRAND.md`
6. `VS_CHAT_CONTEXT.md`
7. `SHOW-BUILDER-PROMPT.md`
8. Older benchmark/template examples

Do not silently resurrect older patterns just because they still exist in legacy files.
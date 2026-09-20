# Vegas Sidekick — Show Page Benchmark

**Current benchmark:** `shows/magic/nathan-burton-comedy-magic/index.html`  
**Locked:** September 15, 2026
**Status:** Governing UX / copy / interaction benchmark for active show product pages.

If an older template, benchmark, prompt, or example conflicts with this document or the current Nathan Burton page, **Nathan Burton wins**, except where a newer locked shared system is explicitly documented here.

The current shared showtimes booking module and the September 13 buyer-journey ordering are newer than Nathan Burton’s original treatment and supersede that older ordering where they conflict.

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
5. What is [Show]? descriptive overview
6. Quick Take
7. Showtimes / booking module
8. Photos
9. Official trailer when a verified video exists
10. Seat Guide when useful
11. Good Fit / useful fit guidance
12. FAQ
13. Related shows
14. Next useful click
15. Kris author card + freshness + disclosure
16. Final ticket CTA
17. Mobile sticky ticket bar

The buyer journey is intentional: **What is this? → Is it for me? → Can I go? → What does it look like? → Where should I sit? → Buy.** The descriptive overview explains the entertainment product before Quick Take makes a decision-oriented recommendation. The full **Find your showtime** module belongs immediately after Quick Take so a customer with strong purchase intent can answer the practical availability question without reading half the page first.

Optional sections simply collapse out. A page without a verified trailer should move directly from Photos to Seat Guide, for example. Do not add sections just because a template has room for them. Empty-calorie UI is worse than a shorter page.

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

### Placement

The full booking module belongs immediately after **Quick Take** in the standard active-show flow. This is the first serious conversion position on the page: the visitor has enough context to know what the show is, then immediately gets the answer to whether the show works for their night.

A compact start-time signal or **See available dates & times →** jump link may also appear in the hero/quick facts when useful, but it does not replace the full module.

### Shared showtimes assets

The production showtimes system is shared and reusable:

- `assets/showtimes-booking.css`
- `assets/showtimes-booking.js`
- current verified schedule data in `data/show-database.json`

Do not copy show-specific CSS/JS for the booking module unless there is a genuine exception that cannot be handled by the shared system.

### Verified regular weekly schedules

When the show has a verified regular weekly schedule, use the shared conversion-focused booking module rather than the old large day-card grid.

The module should include:

- compact booking pill above the headline: **CHOOSE YOUR DAY** for regular schedules by default; verified show-specific facts may replace it
- **Find your showtime** headline
- concise verified weekly schedule summary
- all seven weekday choices in one compact row / picker
- active show days selectable
- verified dark days visibly muted and labeled **Dark**
- selected day highlighted in purple
- showtime choices displayed immediately for the selected day
- each showtime linked to the existing verified affiliate URL
- one dominant Warm Amber **Get Tickets →** CTA; the selected day remains obvious in the picker and available in the accessible label
- one compact **See all dates & times →** secondary text action
- no generic planning-ahead card; omit filler unless there is a genuinely useful show-specific fact
- the shared decorative Vegas dusk / skyline / Sphere artwork as a thin footer strip, with **no slogan**

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
- use the **CHECK YOUR DATE** pill and retain the thin shared artwork; do not add generic planning filler
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

## 8. Descriptive show overview

Every active show page should include a compact **What is [Show]?** section before Quick Take.

Its job is to explain the entertainment product in natural language for someone who has never seen or heard of the show. Cover the verified details that actually define the experience, such as:

- what type of show it is
- what happens onstage
- the core performers / format
- the music, comedy, magic, acrobatics, dance, story, effects, or other defining elements
- what makes the production meaningfully different from a conventional show in the same category
- venue / property context when it helps explain the experience

### SEO rule: entity completeness, not keyword density

This section should strengthen the page’s descriptive search footprint by describing the show thoroughly, **not** by repeating search phrases.

- Write for a person first.
- Use show-specific entities and concepts naturally.
- Never write keyword-stuffed lines such as “best Las Vegas show tickets” or repeat “Las Vegas” unnaturally.
- Do not impose a hard word-count minimum. Most shows will need roughly 150–250 useful words; simpler shows can be shorter.
- Stop when the entertainment product is clearly explained. Do not add filler to make the page look complete.
- Never invent show elements to make the description richer.

### Hero / overview / Quick Take are three different jobs

- **Hero:** identify the show quickly.
- **What is [Show]?:** explain what the customer is actually buying a ticket to.
- **Quick Take:** answer whether the show makes sense for the customer and who it fits.

Do not copy the hero sentence into the overview. Do not move the same synopsis into Quick Take with synonyms. A visitor reading all three should learn something new at each step.

Blue Man Group is the first sitewide example of this separation; use the pattern, not its show-specific copy.

---

## 9. Quick Take, Good Fit, and Kris’s take

### Hero / Quick Take separation

The Hero and Quick Take must never duplicate or lightly paraphrase each other.

- **Hero:** answers **What is this show?** Identify the show clearly with useful descriptive language, including the Las Vegas context, show type, venue/property, and defining elements when verified and natural.
- **Quick Take / 30-second answer:** answers **Is it worth seeing, and for whom?** Give the customer a decision-oriented answer instead of repeating the synopsis.
- Do not reuse the hero description as the highlighted Quick Take sentence.
- Do not make superficial synonym swaps to create the appearance of unique copy. The two areas must perform different jobs.
- Keep the Quick Take concise and useful; do not turn it into an SEO paragraph.

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

## 10. Language rules from the Nathan benchmark

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

## 11. Booking tip rule

**Booking tip is optional.**

Keep it only when it gives a concrete, show-specific action, for example:

- when to arrive
- how a showtime fits around dinner
- which section is worth paying for
- when a cheaper section is still a strong choice

If the tip is generic category copy or merely describes a seat, remove it. Never create filler to preserve a layout.

---

## 12. Photo gallery

Nathan Burton is the gallery interaction benchmark.

### Page gallery

- Multiple photos should remain visible on desktop; one unusual portrait or seating-chart asset must not distort the whole gallery.
- Use consistent gallery frames / aspect handling (`object-fit` as appropriate).
- A tall seating chart can use `contain` inside its gallery tile.
- Remove instructional sentences telling users to inspect the photos.
- One image: do not show carousel arrows or an image count. Multiple images: support arrows, count, keyboard navigation and mobile swipe.

### Lightbox

When a photo opens:

- desktop: visible previous / next controls
- keyboard: left / right arrows
- mobile: swipe left / right
- show a subtle image count (for example `2 of 4`)
- user should not need to close one photo to open the next

Preserve useful `alt` text on the original on-page images.

---

## 12a. Official video component

When a verified official YouTube trailer exists, use the shared Vegas Sidekick video component rather than a one-off iframe or custom click handler. In the standard flow, place it **after Photos and before Seat Guide**.

- Assets: `assets/show-video.css` and `assets/show-video.js`.
- Standard markup uses `.vs-video-shell` containing `.vs-video[data-youtube-id]`, a thumbnail image and `.vs-video-play`.
- Keep the lightweight thumbnail visible until the customer presses play; only then create the privacy-enhanced `youtube-nocookie.com` iframe.
- Never invent or guess a video ID. Use only a verified official trailer.
- Do not autoplay before an explicit user action.
- Keep descriptive thumbnail alt text and an accessible play-button label.
- `VideoObject` schema is optional and should only be used when its metadata is verified.

---

## 13. Seating-chart system

Nathan Burton Theater is the first locked example of the reusable seating system. Zombie Burlesque is the locked example of using an approved chart image directly with transparent interactive hit zones.

### Approved chart image wins

When Kris supplies or explicitly approves a seating-chart image, **the supplied image is the visual source of truth**.

- Use that image directly in the page gallery.
- Use that same image as the visible base layer of the interactive seat guide.
- Do **not** redraw, rebuild, trace, reinterpret, or regenerate its room shapes, seat dots, labels, colors, or section geometry.
- Add interactivity by placing transparent section hit zones over the image. The overlays may highlight or select a section, but they must not replace the supplied chart artwork.
- Keep section descriptions and recommendation labels in data/HTML so they can change independently of the approved visual.
- If a venue is shared by multiple shows, the same approved room image can be reused; show-specific recommendation copy can still differ.

This approved-image rule takes precedence over the generated geometry rules below.

### Architecture: room first, show second

When no approved chart image has been supplied, model seating as:

**Show → Venue / showroom → shared room layout → show-specific recommendation copy**

If two shows use the same room, they should share the same geometry. Their recommendation wording may differ.

Do not redraw the same theater independently on every show page.

### Geometry fallback

When generating a chart because no approved image exists:

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

For generated charts, use brand colors consistently rather than randomly:

- Warm Amber — Our Pick / recommendation emphasis
- Purple — core middle seating
- Pink / magenta — front / close seating
- Teal / green — rear / value seating
- Near-black — stage / structure

The exact number of zones can vary by room. Do not recolor an approved supplied chart just to force it into this palette.

### Interaction

- The chart remains clickable / tappable.
- Selecting a zone updates its description and visual highlight.
- On mobile, the selected-zone explanation must appear immediately in view (popover / compact card near the sticky ticket bar or chart). Do not require the user to tap and then hunt below the fold for the result.
- Zone copy should explain what the section offers, not frame it as a compromise.
- For approved-image charts, interaction sits on top of the source image rather than recreating the chart underneath it.

### Disclaimers

Do **not** add a generic seating disclaimer merely to say not every seat is always available or that the diagram is simplified.

Only add a disclaimer when there is a genuine unusual limitation a customer needs to understand.

### Static seating-chart gallery asset

If Kris has supplied or approved a chart image, use that approved asset for the gallery and interactive chart.

If no approved image exists and the chart is generated from room data, generate the static seating-chart graphic from the **same underlying geometry/data** used by the interactive chart.

- dark noir / Vegas Sidekick visual treatment is approved for generated charts
- use a descriptive filename
- use show-specific descriptive alt text
- include venue name and verified address where useful
- do not invent rows or seat counts
- generated static and interactive charts must not drift apart

The static chart is a UX/content asset first; any SEO value is secondary.

---

## 14. SEO and structured data

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

## 15. Locked reusable benchmark assets

### Seating

Current reusable generated room implementation:

- `data/seat-layouts/nathan-burton-theater.json`
- `assets/seat-layouts/nathan-burton-theater.css`
- `assets/seat-layouts/nathan-burton-theater.js`
- `images/nathan-burton-theater-seating-chart.svg`
- `scripts/generate-seat-layout-assets.py`

Current approved-image interaction pattern:

- Zombie Burlesque: supplied chart image used directly with transparent interactive overlays.
- Mystère: supplied chart image used directly with section overlays; Sweet Spot / Our Pick is sections 102–104 and 202–205.

When expanding seating to another show, first check whether Kris supplied/approved a chart image. If yes, use it directly. If not, use the reusable room-geometry system.

### Showtimes

Current reusable showtimes implementation:

- `assets/showtimes-booking.css`
- `assets/showtimes-booking.js`
- verified schedule data in `data/show-database.json`

Use this shared showtimes system across active show pages. Do not resurrect older day-card schedule grids unless Kris explicitly changes the benchmark.

### Current benchmark page

- `shows/magic/nathan-burton-comedy-magic/index.html`

Nathan Burton remains the overall page benchmark, while the newer shared showtimes module and buyer-journey ordering govern the Showtimes position and section sequence.

---

## 15. Precedence

For active show-page work, use this order of authority:

1. Kris's explicit current instruction
2. `SHOW-PAGE-BENCHMARK.md`
3. `AGENTS.md`
4. current Nathan Burton benchmark page
5. newer locked shared systems documented above
6. older templates / prompts / examples only when they do not conflict

Useful beats complete-looking. Do not add filler UI or copy to make every page identical.

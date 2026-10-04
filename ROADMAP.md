# Vegas Sidekick — Roadmap

Priorities in order, agreed 2026-08-27. Ordered by revenue impact × certainty, then
risk reduction, then long-term SEO. Sibling docs: `CLAUDE.md` (mechanics),
`BRAND.md` (voice and editorial rules).

**Everything marked 🔒 is blocked on data only Kris can supply.** Those are the
bottleneck, not build time.

---

## 1. Finish the catalogue — the 11 pipeline shows 🔒

Barry Manilow ($91) · The Rat Pack Is Back! ($92) · Eddie Griffin ($87) ·
Carlos Mencia ($27) · Luenell ($37) · MIND2MIND at Fontainebleau ($82) ·
Carpenters Legacy ($49) · Paranormal at Horseshoe ($31) · Soul Of Motown ($54) ·
Drag Brunch Las Vegas ($55) · Jen Kramer ($17).

Every one is a page that cannot earn a commission until it exists. Highest certainty
of return on this list. MIND2MIND doubles as our first coverage of Fontainebleau.

**Needs:** the real Spotlight listing URL per show (never guess — see CLAUDE.md) and
at least one image each.

## 2. Fix the live pages that are already unfinished 🔒

- **X Burlesque has no images of itself** — no gallery section at all; the only photos
  on the page are other shows' cards. Its hero (`x-burlesque-hero.webp`) is on disk,
  unused. An $82 show with a broken page.
- **Seven Alexis Park pages** still read "check at booking" for duration and age,
  because that data was not in the source.

Cheap, same-day, and a live conversion leak on pages already taking traffic.

**Needs:** run times and age policies for those 8 shows.

## 3. Photos to 5+ on the 8 thin pages 🔒

Same 8 pages as #2. Median page is already at 5 photos; this is a gap, not a project.

**What matters for SEO, in order:** unique images (never stock — reverse-image dedupe
discounts anything seen elsewhere) → descriptive alt text naming the venue → image
sitemap entries for gallery shots, not just heroes → WebP with real dimensions and
lazy loading below the fold → *then* count. 3 is the floor, 5 comfortable, past 8 you
are adding weight for diminishing return.

## 4. A standing price and schedule audit

The August 2026 sweep found **15 wrong prices and 15 wrong schedules** in one pass.
That drift is continuous. A monthly Spotlight comparison, run the same way, catches it
in an hour instead of a year. Wrong prices cost trust and bookings directly.

Run `python3 scripts/audit-event-schema.py` after any batch, and follow the **Price
Change Checklist** in CLAUDE.md — prices are denormalised across ~10 files.

## 5. Search Console hygiene

Resubmit the sitemap and watch the 74 URLs recover from the August homepage incident
(commit `1b1ae4a` rewrote `index.html` and `sitemap.xml` from stale copies; live for a
week). Confirm Google drops the Event rich results for the three closed shows. Pure
risk reduction — currently flying without instruments on a known injury.

## 6. Video on every show page 🔒

One page has a trailer today (Carrot Top). 69 to go. Biggest dwell-time win available,
and `VideoObject` earns video rich results.

**Needs per show:** official YouTube URL, upload date, run time. Google validates the
last two — they cannot be guessed. See the video-preview section in CLAUDE.md.

## 7. Venue data hygiene, then 2–3 more venue pages

Venue strings are inconsistent and this breaks grouping and the `excludeVenue` filter
in `picks.js`:

- "Excalibur Hotel" / "Excalibur"
- "The STRAT Hotel" / "The STRAT"
- "Luxor Hotel" / "Luxor Hotel & Casino"
- "Planet Hollywood" / "Planet Hollywood Resort"
- "LINQ Promenade" / "The LINQ Promenade"
- Two with no room name at all: "MSG Sphere · Las Vegas", "BattleBots Arena · 4165 Koval Lane"

Normalise first, then **The STRAT** (3 shows), **Westgate** (3 once the pipeline
lands) and **Horseshoe** (2) earn pages. Alexis Park proved the format works.

## 8. More guides

Six today, and they are the best ranking pages on the site. Obvious gaps: Best Adult
Shows · **Best Tribute Shows** (16 in the catalogue — we would own it) · Best Shows
Under $50 · Best Late-Night Shows.

## 9. Vegas history / evergreen

Elvis at the International (31 July 1969 → December 1976, 636 sold-out shows) and the
Rat Pack at the Sands (the Summit, January 1960; Copa Room demolished 26 Nov 1996).

**Not biographies** — we cannot outrank Wikipedia for "Frank Sinatra" and that traffic
would not convert. The angle is Vegas geography and industry mechanics, where Wikipedia
is weak and Kris has genuine authority, bridged to the 16 tribute shows we already
sell. Slow: 3–6 months before it means anything.

Start with two, measure for 90 days before building a section. Put them at
`/vegas-history/`, not `/legends/` — "legends" reads like a fan site.

## 10. Reviews and ratings — carefully

Zero pages carry `aggregateRating`. Star ratings lift click-through more than almost
anything else. **But only with real collected reviews.** Self-authored ratings on our
own affiliate listings are a Google policy violation and a manual-action risk. Needs a
genuine collection mechanism first, which is its own project. Bottom of the list for
that reason, not because the upside is small.

---

## Considered and deliberately left off

- **Analytics** — already handled. GA4 (`G-BM6QGF7B4Y`) live site-wide via `header.js`.
- **Email nurture** — Brevo capture is on every page; whether anything is being *sent*
  is a marketing question, not a site one.
- **Core Web Vitals** — the heavy lifting was done in August; no current evidence of a
  problem.

## Do first

**#2 and #3 together** — one pass, roughly half a day, fixes eight live pages. Then
**#1**, which is the actual money. Both are blocked on the same thing: data from Kris.

---

## Good to Know social-series reference

Vegas Sidekick's recurring **Good to Know** social series is governed by `GOOD-TO-KNOW.md`.

- It is the customer-service social layer for verified show changes that affect planning or booking: start times, venue moves, return dates, performance-day changes, meaningful added dates, closing dates and similar material updates.
- It is distinct from **Vegas Dispatch**, which is the editorial/news product.
- Use approved repo photography, artwork, show logos and Vegas Sidekick branding exactly as supplied. Do not generate replacements or lookalikes.
- Store recurring series assets under `/images/good-to-know/`.



---

## Sidekick Index — shipped foundation / ongoing expansion

The Sidekick Index reference system is now live as a product family rather than a future idea.

Canonical documentation: `SIDEKICK-INDEX.md`.

Current pages:

- Overview
- Headliners & Residencies
- Show Price Index
- More Touring Shows & Concerts

The October 3 touring expansion now covers 12 venues, and the shared Index shell provides reference-page navigation plus the existing email signup placement.

**Ongoing priority:** expand only when a new dataset answers a recurring useful question and has a maintainable source trail. Do not create empty categories for appearance.

For future Index work, preserve the classification boundary between regular Vegas productions, major headliner/residency engagements, and smaller/shorter touring events. Preserve the mobile horizontal-scroll system so long venue/filter/month rails remain fully reachable and visibly swipeable.

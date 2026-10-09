# SIDEKICK-INDEX.md — Vegas Sidekick Reference System

**Status:** Current production system  
**Last updated:** October 9, 2026  
**Canonical scope:** `/sidekick-index/`

This file is the source of truth for the **Sidekick Index** project: its purpose, page taxonomy, data boundaries, shared UX, source files, mobile behavior, and maintenance rules.

If an older conversation, one-off implementation note, or legacy doc conflicts with this file about Sidekick Index, this file wins.

---

## 1. What Sidekick Index Is

Sidekick Index is the **reference / data side of Vegas Sidekick**.

It exists for questions that are easier to answer with a clean maintained index than with a normal show product page or travel article:

- who is playing Las Vegas
- when an act is here
- where an event is playing
- what kind of engagement it is
- what advertised starting prices were observed in a dated snapshot
- what source supports the entry

It is intended for both visitors and people using Vegas entertainment information professionally: journalists, bloggers, creators, researchers, and locals.

The product should feel like a useful Las Vegas entertainment reference, not a generic event scraper.

### Core rule

**Useful beats complete-looking.**

Do not create empty datasets, filler categories, or thin reference pages just to make the Index appear larger.

---

## 2. Current Reference Pages

The current Sidekick Index system has four public routes:

| Page | Route | Purpose |
|---|---|---|
| Overview | `/sidekick-index/` | Explains the Index and routes users to the current reference datasets. |
| Headliners & Residencies | `/sidekick-index/headliners-residencies/` | Major residencies, headliners, and notable limited engagements. |
| Show Price Index | `/sidekick-index/show-price-index/` | Dated comparison of advertised starting prices for the active Vegas Sidekick show catalog. |
| More Touring Shows & Concerts | `/sidekick-index/touring-shows-concerts/` | Visiting concerts, touring productions, and short-run events outside the major headliner/residency calendar and regular weekly show catalog. |

Shared navigation between these pages is handled by:

`components/sidekick-index-shell.js`

That shell also moves the existing Vegas Sidekick email signup into the shared Sidekick Index placement above the footer.

Do not duplicate the reference-page navigation or newsletter markup separately in each page unless the shared system is being intentionally replaced.

---

## 3. Classification Boundaries

The biggest maintenance risk is putting the same entertainment product into the wrong index or into multiple indexes without a reason.

### Regular Vegas productions

Ongoing Vegas productions that play a recurring local schedule belong in the **normal Vegas Sidekick show catalog and show pages**.

Examples of the category include regular magic, comedy, adult, tribute, Cirque, and production shows.

They do **not** move into the touring index simply because they perform at a venue that also hosts touring acts.

### Headliners & Residencies

Use **Headliners & Residencies** for:

- major Las Vegas residencies
- headline engagements
- major limited engagements
- notable arena/theater runs that function like a headliner booking
- major comedy/music engagements that belong in the citywide headline calendar

Source of truth:

`data/reference/headliners-residencies.json`

### More Touring Shows & Concerts

Use **More Touring Shows & Concerts** for:

- visiting concerts
- touring productions
- short-run events
- one-night or brief engagements
- smaller and mid-size venue calendars that would overwhelm the Headliners & Residencies page

Source of truth:

`data/reference/touring-shows-concerts.json`

Recurring restaurant/bar entertainment, regular resident productions, and recurring local series are excluded unless there is a specific reason to treat an occurrence as a material touring/special event.

### Avoid duplication

By default, an event should live in **one Sidekick Index calendar**.

If an act clearly belongs in Headliners & Residencies, do not also add it to More Touring Shows & Concerts just because its venue is covered there.

When classification is ambiguous, choose the page that best matches how a normal Vegas visitor would think about the engagement.

---

## 4. Current Data State

These counts are a **dated snapshot**, not permanent product rules.

### More Touring Shows & Concerts

As verified October 8, 2026:

- 149 indexed event entries
- 13 covered venues

Current venue set:

- Brooklyn Bowl Las Vegas
- House of Blues Las Vegas
- 24 Oxford
- Fremont Country Club
- Backstage Bar & Billiards
- Swan Dive
- The Space Las Vegas
- AREA15
- Hard Rock Live Las Vegas
- The Smith Center
- Downtown Las Vegas Events Center
- Notoriety Live
- Desert Breeze Event Center

The venue list is expected to grow. Do not hard-code marketing copy that becomes wrong when more venues are added.

### Headliners & Residencies

As verified October 9, 2026:

- 177 act / engagement records
- 22 underlying venue records
- 9 resort/venue groups used to simplify customer-facing venue filtering where appropriate

The JSON supports grouped resort presentation so multiple rooms at one property do not have to become separate top-level filter pills.

### Show Price Index

Current snapshot:

- observation date: September 27, 2026
- 71 active Vegas Sidekick shows
- 148 published starting-price observations
- 16 shows with all three source prices recorded

Current snapshot file:

`data/show-price-index/2026-09-27.csv`

The Show Price Index is point-in-time research. Do not silently rewrite an old snapshot to make it look current. A new observation period should create/update the appropriate dated snapshot and visible observation date.

---

## 5. Source and Accuracy Rules

Sidekick Index is only useful if a reader can trust where the information came from.

### General

- Prefer official venue, artist, promoter, ticketing, or primary event sources.
- Established secondary concert listings can be used where appropriate, but primary sources are preferred.
- Never invent dates, venues, times, prices, engagement types, or URLs.
- Never create a fake source trail to make an entry look complete.
- Gaps should be visible or omitted rather than guessed.
- Keep the visible verification date accurate.

### Touring index

Each event entry should contain the best available event-level or venue-level source URL and enough structured information to render the date-first, act-first, and venue-first views.

For multi-day touring productions, do not treat the stored opening/start date as the expiration date. Confirm the final performance date before removing the entry.

### Headliners & Residencies

Keep the act/engagement record, venue mapping, dates, engagement type, official URL, and source list aligned.

Venue groups are presentation structure, not substitutes for the underlying venue records.

### Price Index

Record what the source publicly advertises as the starting price under the established methodology. Do not manufacture an apples-to-apples comparison when the sellers are displaying different inventory.

The existing methodology on the page remains part of the product and should not be shortened into misleading precision.

---

## 6. Shared UX System

The Index pages should feel related without forcing every dataset into identical markup.

### Shared reference navigation

`components/sidekick-index-shell.js` owns the current **Reference pages** pills:

- Overview
- Headliners & Residencies
- Show Price Index
- More Touring Shows & Concerts

The active page is visibly selected.

### Shared email signup

The same shell relocates the site's existing email signup into a Sidekick Index-specific slot above the footer.

Do not create a second competing email form.

### Date / act / venue views

Headliners & Residencies and More Touring Shows & Concerts support compact browse modes such as:

- By date
- By act
- By venue

These are functional views, not decorative tabs. Any data or filter change must continue to work in all supported views.

### Filters

Filter pills should:

- remain compact
- have a clear active state
- preserve readable counts where used
- update the visible dataset without stale copy or stale stats

---

## 7. Locked Mobile Horizontal-Scroll Behavior

This was fixed and standardized October 3, 2026 after the touring venue rail could not reliably reach the final venues on mobile.

For **any Sidekick Index horizontal pill/rail UI** on mobile:

- the user must be able to scroll fully to the final item
- never let a parent container clip the scrollable child
- use touch momentum where supported
- contain horizontal overscroll so the page itself does not fight the rail
- provide enough trailing inline padding that the final pill can be fully visible
- hide the browser scrollbar when the pill rail is designed as a swipe control
- show a subtle right-edge fade while more content remains
- show **Swipe for more →** when the rail actually overflows
- once the user reaches the end, the cue may change to **← Swipe back**
- do not show a swipe instruction when everything already fits

The current implementation uses measured `scrollWidth` vs. `clientWidth` state rather than assuming every device overflows.

This behavior currently applies to:

- touring venue filters
- headliner/residency venue filters
- engagement-type filters where they overflow
- month-jump rails

The Show Price Index uses a wide comparison table rather than pill rails. On mobile:

- horizontal table scrolling must remain enabled
- touch momentum / overscroll handling should work
- a visible **Swipe table →** cue should make the interaction obvious

Do not replace these cues with permanent arrows that imply a carousel if the interaction is native horizontal scrolling.

---

## 8. Current Touring Venue Expansion

The touring system began with Brooklyn Bowl and expanded on October 3, 2026 to include:

1. House of Blues Las Vegas
2. 24 Oxford
3. Fremont Country Club
4. Backstage Bar & Billiards
5. Swan Dive
6. The Space Las Vegas
7. AREA15
8. Hard Rock Live Las Vegas
9. The Smith Center
10. Downtown Las Vegas Events Center
11. Notoriety Live

The page now tracks 12 venues total including Brooklyn Bowl.

The lesson from the rollout: build the venue/filter system to scale. Do not write hub copy, layout widths, or mobile behavior around an assumption of only three or four venues.

---

## 9. SEO, Schema, and Discovery

Current Sidekick Index pages are intended to be indexable public reference resources.

### Overview

Use normal page metadata and internal links to the live reference datasets.

### Data pages

Where appropriate, use:

- `CollectionPage`
- `Dataset`
- `BreadcrumbList`

Dataset schema should point to the current underlying downloadable/reference data when a stable public data file exists.

All Sidekick Index factual datasets are published under **Creative Commons Attribution 4.0 International (CC BY 4.0)**. Every `Dataset` JSON-LD block must include:

- `"license":"https://creativecommons.org/licenses/by/4.0/"`
- `"usageInfo":"https://vegassidekick.com/data-license/"`

Every public dataset page must also include a visible **Data reuse** note linking to `/data-license/`. Downloadable JSON files should carry license and attribution metadata when the format allows it.

The license applies only to factual Sidekick Index dataset material and any Vegas Sidekick rights in the compilation/organization of that data. It does **not** license Vegas Sidekick editorial copy, show recommendations, trademarks, logos, Spike, photography, graphics, page design, or third-party source material.

Keep `dateModified`, observation dates, and verification language honest.

### Sitemap

New Sidekick Index pages should be added to `sitemap.xml`.

Do not add an unpublished/empty reference page to the sitemap just to reserve a URL.

### Social share assets

Current dedicated social images include:

- `/images/sidekick-index/sidekick-index-social.png`
- `/images/sidekick-index/las-vegas-headliners-residencies-social.png`
- `/images/sidekick-index/more-touring-shows-concerts-social.png`

The Show Price Index currently uses its configured page metadata and should get a dedicated share image only when one is intentionally created.

Do not invent social artwork filenames.

---

## 10. Adding a New Sidekick Index Dataset

A new reference dataset should earn its place by answering a recurring, useful question better than a normal article can.

Before shipping a new Index page:

1. Define exactly what belongs in the dataset and what does not.
2. Decide the source-of-truth file and update process.
3. Build the public page under `/sidekick-index/`.
4. Add it to the overview page.
5. Add it to `components/sidekick-index-shell.js`.
6. Add appropriate schema and metadata, including the CC BY 4.0 `license` and Vegas Sidekick `usageInfo` fields for any `Dataset`.
7. Add a visible Data reuse note linking to `/data-license/`, and include license/attribution metadata in downloadable JSON when possible.
8. Add it to `sitemap.xml`.
9. Add a social share image if useful and actually created.
10. Reuse the shared email signup placement.
11. Test mobile filters, horizontal rails, sticky elements, and any wide tables.
12. Update this file if the new dataset changes the Sidekick Index taxonomy or maintenance rules.

Do not add a new top-level Index category if it is just a thin wrapper around one or two facts.

---

## 11. Files to Check for Sidekick Index Work

Core pages:

- `sidekick-index/index.html`
- `sidekick-index/headliners-residencies/index.html`
- `sidekick-index/show-price-index/index.html`
- `sidekick-index/touring-shows-concerts/index.html`

Shared system:

- `components/sidekick-index-shell.js`

Data:

- `data/reference/headliners-residencies.json`
- `data/reference/touring-shows-concerts.json`
- `data/show-price-index/`

Discovery / infrastructure:

- `sitemap.xml`
- relevant social images under `images/`

For Sidekick Index work, read this file before making structural changes.

---

## 12. Shipping Checklist

Before committing meaningful Sidekick Index changes:

- confirm classification is correct
- confirm source URLs are real
- confirm verification / observation dates are current
- confirm all supported views still render
- confirm counts/stats update correctly
- confirm filters work after data changes
- confirm the final horizontal pill can be reached on mobile
- confirm swipe cues appear only when content overflows
- confirm month rails still work after filtering
- confirm wide tables remain horizontally usable
- parse inline JavaScript after edits
- parse JSON-LD after edits
- validate JSON source files after data edits
- check the sitemap if routes changed
- keep GitHub commit status separate from production verification

---

## 13. Current Product Direction

Sidekick Index is a **growing reference system**, not a second version of the show catalog.

The best additions are datasets that:

- answer a repeated Vegas entertainment question
- have a maintainable source trail
- can stay fresh without inventing information
- are easier to scan as structured reference data than as prose
- create a reason for people to bookmark, cite, or return to Vegas Sidekick

Do not expand it just because another category is possible.

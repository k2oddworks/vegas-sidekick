# VS_CHAT_CONTEXT.md — Vegas Sidekick Living Project Context

**As of:** September 8, 2026  
**Purpose:** Living source of project context, decisions, operating rules, architecture, and lessons learned for ChatGPT/Codex or any future AI collaborator working on Vegas Sidekick.

> This file is not the coding-agent instruction file. `AGENTS.md` should eventually contain concise execution rules for coding agents. This file records what Vegas Sidekick is, how it currently works, what has already been decided, and the context needed to avoid repeating old mistakes.

---

## 1. What Vegas Sidekick Is

Vegas Sidekick (`vegassidekick.com`) is a Las Vegas show-discovery and ticket-affiliate site. The business helps visitors choose Vegas shows, compare options, understand tradeoffs, and hand off ticket purchases through Spotlight.Vegas affiliate links.

Founder / Chief Experience Officer: **Kris Kidd**.

Mascot: **Spike**, a saguaro cactus wearing gold aviators.

The site should feel like advice from a knowledgeable Vegas local who works in tickets, not a generic tourism portal or ticket marketplace.

### Revenue model

Primary revenue comes from affiliate commissions on Spotlight.Vegas ticket links using the Vegas Sidekick referral path:

`/ref/vegassidekick`

Never invent, guess, or fabricate an affiliate URL. If the correct ticket URL is not known or verifiable, flag it.

---

## 2. Brand Voice — Non-Negotiable

The governing brand reference is the **Vegas Sidekick Brand Bible**, especially Section 3 Voice & Tone and its Do/Don't guidance.

### One-Line Test

Before shipping customer-facing copy, ask:

> **Would a Vegas local who works in tickets actually say this to a friend?**

### Voice characteristics

- direct
- useful
- warm
- practical
- numbers-first when relevant
- dry humor when natural
- comfortable stating downsides
- never PR-sounding
- never generic travel fluff

### Never invent firsthand experience

Do not write that Kris attended, saw, sat in, tested, experienced, or personally witnessed something unless Kris explicitly said so.

### Avoid unsupported urgency and trust theater

Do not use claims such as:

- “Selling fast”
- “Prices may increase”
- “Book early” unless tied to a real, verified reason
- “No hidden fees”
- “Zero hidden fees”
- “Secure booking”
- “Instant delivery”

Do not add fake countdowns, fake scarcity, fake review signals, or generic conversion-pressure copy.

### Freshness wording

Prefer concise freshness such as:

**Last updated September 2026**

Avoid repetitive customer-facing “price checked on...” language unless the date itself adds value.

---

## 3. Repository and Deployment

GitHub repository:

`k2oddworks/vegas-sidekick`

Default branch:

`main`

The site is a largely static site deployed through Cloudflare.

### Critical deployment lesson

There is/has been a GitHub Actions workflow named similarly to **Deploy to Cloudflare Workers** that can report failure while the actual site changes still deploy successfully through the site's normal Cloudflare path.

**Never conclude that production is not live solely because that GitHub Actions workflow failed.**

When reporting work:

- “merged to `main`” is safe when verified
- “going through the normal deployment path” is safe
- only claim something is actually live after independently verifying production when that verification matters

---

## 4. Current Show-Page System

The current canonical show-page system uses:

- `vegas-the-show-TEMPLATE.html` as the canonical structural starting point
- `absinthe-BENCHMARK.html` as a feature / interaction benchmark
- `scripts/canonicalize-show-pages.py`
- `assets/show-canonical.css`
- `assets/show-canonical.js`

Do not redesign show pages from scratch when adding or rebuilding a show. Reuse the established system.

### Standard customer-facing section flow

Current canonical show pages generally use:

1. Hero
2. Four-part quick facts
3. Ticker
4. Sticky section navigation
5. Quick Take
6. Photos
7. Interactive seat guide where useful
8. Good Fit / Think Twice
9. Seven-day schedule grid or appropriate variable-schedule treatment
10. FAQ
11. Related shows
12. Next useful click
13. Author / freshness / disclosure
14. Final CTA
15. Mobile sticky ticket bar

### Structured data

For active shows:

- use appropriate `Event` / `EventSeries` schema
- `offers.price` must be a **bare number**, never `$62`
- do not fabricate schedules that cannot be safely represented
- closed archives should not carry active Event/EventSeries schema

Use the repo’s schema audit before shipping changes that affect show facts.

---

## 5. Ticket CTA Design Decision

As of September 8, 2026, the sitewide **primary ticket-purchase CTA color is Warm Amber**.

Core treatment:

- fill: `#FFB000`
- text: near-black / dark charcoal (`#171225` currently used)
- pink remains a Vegas Sidekick brand/accent color

The Warm Amber rollout covered primary ticket actions sitewide. Do **not** globally replace pink branding, newsletter treatments, decorative accents, or logo colors.

A recurring audit exists to help prevent primary ticket buttons from drifting back to inconsistent colors.

---

## 6. Mobile Hero System

A full active-show mobile hero audit was completed across **71 active show pages**.

### Problem solved

A universal `object-fit: cover` treatment was cropping wide promotional artwork, including titles, logos, and performers.

### Current default

The preferred mobile hero mode is **safe**:

- full hero artwork remains visible with `object-fit: contain`
- the same image fills the surrounding frame as a softened / darkened blurred background
- per-show focal positioning remains available
- desktop hero behavior remains separate

Data-backed records may express this concept as:

```json
"mobile_hero": {
  "fit": "safe",
  "position": "center center"
}
```

### Current global mobile refinement

The latest global safe-mode treatment intentionally:

- avoids a heavy “card in a box” look
- uses restrained rounded corners
- uses subtle shadow / outline
- keeps enough cushion around artwork
- does not shrink wide promotional art too aggressively

The global default is considered **finished** unless a real recurring problem emerges. Fix individual odd aspect-ratio shows through per-show focal positioning rather than endlessly retuning the global system.

Permanent audit:

`scripts/audit-mobile-show-heroes.py`

---

## 7. Show Database — New Operational Direction

The project is moving away from one JSON file per show toward a **Vegas Sidekick Show Database**.

### Why

The goal is not merely clean developer architecture. The goal is a business-friendly operational source of truth that Kris or a future owner can inspect and edit in one place.

### Current master dataset

`data/show-database.json`

A spreadsheet-style internal interface exists at:

`/admin/show-database/`

The interface has been merged to `main`.

### V1 interface capabilities

The current Show Database UI includes concepts such as:

- spreadsheet-style table
- search
- filters
- sorting
- Active / Closed / Needs Review views
- multi-row selection
- bulk editing concepts
- show detail drawer
- local draft persistence
- JSON export
- live-page link

### Important limitation

Direct secure **Save to GitHub / update the live site** is not yet considered safely connected.

The existing admin GitHub OAuth implementation was found to contain a credential embedded in repo code. Do **not** build new write capabilities on that authentication path without securing it first.

### Desired long-term Show Database behavior

The database should become the operational control center for:

- show status
- Vegas Sidekick price
- regular/list price
- schedule
- dark days
- venue / showroom
- runtime
- age guidance
- ticket URL
- media
- trailer
- restrictions
- verification date and source

It should **not casually overwrite editorial judgment**, including:

- Kris’s Take
- Good Fit / Think Twice
- rankings
- guide inclusion
- editorial verdicts
- subjective recommendations

### Verification states

A useful long-term pattern is to distinguish:

- verified by Kris
- verified from Spotlight
- stale / old verification
- unverified
- conflicting source

The prior per-show JSON pilot established the value of provenance. Preserve that lesson in the Show Database architecture.

---

## 8. Spotlight as Operational Ticketing Source

As of September 8, 2026, Spotlight’s public show pages are used as an operational source for current ticketing facts where Spotlight explicitly publishes them.

Facts suitable for reconciliation include:

- current Vegas Sidekick starting price
- regular/list price when shown
- schedule
- dark days
- multiple showtimes
- venue / showroom
- runtime
- age guidance
- canonical Spotlight ticket URL

### How reconciliation works

The system can read Spotlight’s **public HTML pages** without a private API:

1. start from a known Spotlight show URL
2. request the public page
3. parse labeled page fields
4. normalize them into Vegas Sidekick data
5. compare with current site values
6. update only fields that are safe to own

This is web-page parsing, not private API access.

### Important caution

Spotlight HTML is presentation markup, not a stable machine API. Its formatting can vary, for example:

- `2 hours` vs `120 minutes`
- schedules with omitted AM/PM
- multiple prices rendered compactly
- changes in markup

Therefore:

- never blindly trust raw scraper output
- normalize and validate
- do not bypass authentication, CAPTCHAs, blocks, or other access controls
- keep request frequency reasonable

### September 8 reconciliation

A full reconciliation matched **71/71 active shows** to Spotlight product pages with zero fetch failures during that run.

The pass updated the Show Database and customer-facing factual surfaces, including price/schedule/runtime/age/venue where available, and propagated changed prices to linked customer pages.

The broader lesson matters more than the exact counts: **the Show Database should be reconciled against the actual ticketing source before being treated as authoritative.**

---

## 9. Catalog JavaScript Failure — Important Lesson

After the Spotlight reconciliation, the root `/shows/` page displayed **0 shows** while category pages appeared mostly normal.

### Root cause

Venue names containing apostrophes were inserted into single-quoted JavaScript object literals without safe escaping, breaking the entire catalog array.

Affected examples included:

- X Burlesque / Bugsy’s Cabaret
- Tournament of Kings / King Arthur’s Arena

A single malformed record can cause the entire browser-side grid to fail and show zero results even when the HTML document itself loads.

### Permanent rule

Any process that writes data into JavaScript literals must **serialize safely**. Do not construct JS data with naive string interpolation.

Permanent safeguard:

`scripts/audit-catalog-js-syntax.py`

The Operations workflow now includes catalog JavaScript syntax checking so this class of failure is treated as a P0 accuracy issue.

---

## 10. Active vs Closed Shows

Closed show pages should generally **remain online as archives**.

### Closure policy

When a show closes:

- remove it from active catalogs
- remove active ticket CTAs
- remove active Event/EventSeries schema
- add appropriate closure treatment
- keep the canonical URL/page alive
- update guides and related modules where necessary
- do not delete the page merely because the show closed

Known closed archives include:

- Mad Apple
- David Goldrake’s current Vegas run

Mad Apple previously leaked back into `/shows/` after its archive page had already been correctly closed. A permanent audit now checks for closed shows remaining in active catalog data.

Permanent safeguard:

`scripts/audit-closed-show-catalog-leaks.py`

---

## 11. Internal Linking System

Vegas Sidekick now has a deliberate internal-linking baseline rather than ad hoc link insertion.

### Philosophy

- contextual, not confetti
- links should help the visitor choose the next useful page
- do not invent relationships
- do not change categories merely to satisfy a link target
- do not automate rankings or subjective recommendations

Current reusable tooling includes:

- `scripts/full-internal-link-build.py`
- `scripts/run-full-internal-link-build.py`
- `scripts/audit-internal-links.py`

A prior completed baseline brought tracked show, guide, Dispatch, venue, category, and hub pages to zero internal-link review candidates and zero broken contextual targets at that time.

New content should preserve this standard.

---

## 12. SERP Metadata System

A deterministic metadata cleanup was completed across canonical/indexable pages to reduce duplicate formulaic titles and weak descriptions.

Reusable tooling includes:

- `scripts/optimize-serp-metadata.py`
- `scripts/optimize-site-serp-overrides.py`
- `scripts/audit-serp-metadata.py`

Goals:

- unique enough to stand apart from competing pages
- factual
- category-aware
- useful for CTR
- no templated spam feel

Do not mass-rewrite metadata without preserving page intent and verified facts.

---

## 13. Content / Link Hygiene

Reusable audit:

`scripts/audit-content-link-hygiene.py`

It checks for issues such as:

- banned / stale urgency copy
- stale presale / on-sale language
- old freshness wording
- internal links pointing to redirect sources
- broken local href/src targets

Do not reintroduce retired wording simply because an older template or source document contains it.

---

## 14. Operations System

Priority order:

- **P0 Accuracy**
- **P1 Revenue**
- **P2 Growth**
- **P3 Enhancement**

Known P0 accuracy problems take precedence over discretionary P3 polish.

### Current recurring Operations audits

`.github/workflows/operations-audits.yml`

Current categories include:

- Event/EventSeries schema
- site health
- SERP metadata
- content/link hygiene
- internal linking
- media inventory
- mobile show heroes
- closed-show catalog leakage
- ticket CTA consistency
- catalog JavaScript syntax

### Automation philosophy

Fully deterministic checks can enforce mechanical rules.

Examples:

- broken paths/images
- malformed schema
- bad numeric price format
- duplicate metadata
- closed-show leakage
- syntax errors
- missing hero treatment

Human judgment remains required for:

- rankings
- Kris’s Take
- Good Fit / Think Twice
- guide inclusion
- subjective editorial copy
- disputed source facts
- whether a third-party claim is trustworthy

---

## 15. Media Rules

Use real existing photography and show/event assets.

Do not generate fake event imagery for actual show pages.

Do not duplicate the same photo merely to hit an image count.

Do not expose internal notes such as “needs five photos” or asset-count commentary to customers.

Video trailers:

- official YouTube embeds only
- never guess a video
- never re-host a guessed trailer

A media audit exists at:

`scripts/audit-show-media.py`

There are still many active shows with relatively thin show-specific image inventories. Treat media work as opportunity-based rather than a requirement to force an arbitrary count everywhere.

---

## 16. Guides

Guides are not disposable SEO listicles. They should help a visitor make a decision.

Current principles:

- rankings must be intentional
- factual claims must stay synced with show status and price changes
- if a ranked show closes, remove or contextualize it appropriately
- “cheapest,” “from $X,” and similar claims require maintenance
- internal links should lead naturally into relevant show pages

VEGAS! The Show is currently intended as the #1 recommendation on the first-timers guide.

Newsletter signup:

- mid-article signup is preferred when it fits the reader flow
- avoid an awkward text CTA disconnected from the actual signup form

---

## 17. Vegas Dispatch

The current Dispatch benchmark is the **Activate Town Square** article treatment.

For Dispatch rebuilds:

- prioritize upcoming/current stories before archival material
- preserve and verify actual reporting
- use real assets
- strong mobile hero
- quick facts where useful
- ticker
- sticky section navigation
- scannable structure
- mid-article Spike newsletter signup
- useful internal links
- Kris Kidd avatar/byline
- appropriate NewsArticle/Breadcrumb/FAQ schema

### Kris’s Take

Include **🌵 Kris’s take** only when there is a meaningful editorial observation.

It may be drafted in Kris’s voice using known Vegas/ticket/event context, but must not invent firsthand attendance or personal experience.

Remove stale presale/on-sale language and unsupported urgency.

---

## 18. Show Facts — Never Guess

For any show, do not invent:

- price
- regular/list price
- Spotlight affiliate URL
- schedule
- dark days
- dated schedule phases
- age rule
- runtime
- venue / showroom
- show status
- trailer

When a fact is uncertain, stale, or conflicting, surface the uncertainty instead of filling the gap with a plausible guess.

---

## 19. Past Structured-Data Pilot — Lessons to Keep

Before the Show Database pivot, four per-show JSON pilots were built for:

- Carrot Top
- VEGAS! The Show
- Mystère
- The Wizard of Oz at Sphere

Those individual JSON files were later deliberately deleted when the project shifted toward the master Show Database.

The old files are no longer the architecture, but the pilot taught several useful lessons:

- schedule structures must support dated phases
- schedules may contain multiple showtimes per day
- some shows genuinely have variable schedules
- structured data and visible copy need separate safe render paths
- provenance matters
- customer-visible text should not be modified with broad regex that can corrupt JSON-LD
- schema should refuse unsafe schedule representation rather than inventing one

Preserve these lessons in future database/sync work.

---

## 20. Current Notable Show Facts / Edge Cases

These are examples of why the data model needs to support more than a simple weekly schedule:

### VEGAS! The Show

Had a verified dated schedule transition in September 2026, demonstrating the need for schedule phases rather than one permanent weekly time.

### Mystère

Uses multiple showtimes on active days and dark days on others.

### Wizard of Oz at Sphere

Uses a variable schedule and has meaningful age/ticket/sensory restrictions. Do not fabricate a weekly recurring EventSchedule for a genuinely variable booking calendar.

### MJ Live

Has had venue/date transition behavior that may require dated product/venue phases rather than treating one location as simply “wrong.”

---

## 21. Customer-Facing Catalogs

The root all-shows page is:

`/shows/`

Category catalogs live beneath the show category routes.

Because catalog arrays are browser-side JavaScript, validate JavaScript syntax after automated factual propagation.

Category pages may use separate arrays from the root catalog, so one page working does **not** prove all catalogs are healthy.

---

## 22. Admin / Authentication

The existing `/admin/` system uses GitHub-backed administration / Decap-related infrastructure.

A security issue was identified in the existing OAuth worker implementation: a credential appears embedded directly in repository code.

Until fixed:

- do not extend that exact auth path for new sensitive write features
- do not assume the current Show Database can safely commit production changes from the browser
- secure authentication before wiring database edits directly to GitHub/main

---

## 23. Working Style With Kris

For meaningful repo/site work, explain the proposed approach before making broad changes unless Kris has already clearly authorized the implementation.

Clear implementation authorization includes language such as:

- “do it”
- “go for it”
- “make it live”
- “push to live”
- “build it”
- “go ahead”
- a direct explicit request to create/rebuild/update

Kris prefers quality over rushing customer-facing work and wants ideas stress-tested rather than automatically agreed with.

When reporting technical work, explain the practical effect in plain English.

---

## 24. High-Value Next Directions

Do not automatically begin these without authorization, but current strategic directions include:

- finish secure persistence for the Show Database
- make the Show Database the true operational source of show facts
- add safe reconciliation/change-review against Spotlight
- conversion audit and measurement
- Search Console opportunity engine
- venue hub strengthening
- media improvements on priority shows
- continue guide ecosystem development
- maintain Dispatch quality and freshness

For mobile heroes, prefer spot-checking unusual aspect ratios and adjusting per-show focal positions rather than redesigning the global treatment again.

---

## 25. File Roles Going Forward

### `VS_CHAT_CONTEXT.md`

This file.

Use it as the **living project memory / current-state briefing**.

Update it when a decision materially changes how Vegas Sidekick should be built or operated.

Examples worth recording:

- architecture changes
- permanent design decisions
- new source-of-truth rules
- deployment lessons
- closed-show handling
- major recurring audits
- important failure modes
- editorial rules

Do not clutter it with every commit or tiny one-off visual tweak.

### `AGENTS.md` — future

Should contain concise, execution-oriented instructions for AI coding agents:

- what to read first
- commands/audits to run
- forbidden guesses
- deployment/branch rules
- canonical templates
- safe editing practices

Keep agent instructions separate from this broader project context.

---

## 26. Final Rule

Vegas Sidekick should become **more accurate, easier to operate, and easier for a future owner to understand over time**.

When choosing between clever automation and trustworthy operations, choose trustworthy operations.

When choosing between more copy and clearer information, choose clearer information.

When data conflicts, do not guess.


---

## Show Decision Cards

The customer-facing three-card decision aid uses these labels:

- **Good fit** — who the show is genuinely a match for.
- **Think twice** — optional; include only for a real, show-specific mismatch, downside, or tradeoff. Omit it rather than use category filler.
- **Booking tip** — a concrete seat, timing, or booking action.

Do not use the old labels `Book it if…`, `Know this first`, or `Best practical angle`. Do not fill these cards with generic category filler when a useful show-specific point is available. If there is no defensible booking tip, use a verified planning action rather than inventing seat advice. Existing custom/benchmark decision modules that are more detailed should not be flattened just to match the generic card format.


---

## Savings / Discount System — September 2026

Savings are a first-class Vegas Sidekick conversion feature, but only when they are based on a verified regular/list price.

### Rules

- `data/show-database.json` owns `our_price` and `regular_price`.
- `savings_amount`, `savings_percent`, and `is_deal` are **derived fields**. Never hand-enter the savings math.
- A show qualifies for customer-facing deal treatment only when `regular_price > our_price` by at least **$5**.
- If the difference is under $5, the regular price is missing, or the regular price is not trustworthy, show the normal ticket price without a deal badge.
- Warm Amber is the customer-facing value/deal language while pink remains brand/accent.
- Preferred presentation: current price + struck-through regular price + **Save $X**. Dollar savings lead; percentage savings is secondary.
- Do not use countdowns, fake urgency, inflated comparison prices, or claims of exclusivity unless explicitly verified.
- Current discounted inventory lives at `/shows/deals/`.
- Catalogs can show deal badges and sort by **Biggest Savings**; `/shows/` also has a Deals filter.
- The Show Database UI calculates Savings $ / Savings % automatically as prices are edited.
- `scripts/audit-savings-system.py` is the permanent consistency guard.
- `.github/workflows/savings-audit.yml` runs the recurring savings safeguard.

The September 8 implementation found 54 of 71 active shows meeting the $5 threshold after the Spotlight reconciliation. Treat that count as time-sensitive; the rule and calculation are permanent, the count is not.


### Approved mobile ticket purchase layout — Option 1

As of September 8, 2026, show-page hero ticket purchase modules use the Option 1 treatment on mobile:

- show facts/chips remain immediately above the purchase area
- current price, struck-through regular price, and `Save $X` are grouped compactly
- the primary Warm Amber `Get Tickets →` action is a full-width **rounded pill**, not a tall rectangular block
- do not repeat the same savings math in a separate white `Sidekick deal` explanation box
- custom benchmark pages must visually match the same treatment even when their underlying hero markup differs
- the mobile sticky bottom CTA remains compact and separate from the hero purchase module

# AGENTS.md — Vegas Sidekick

This is the concise execution guide for coding agents working in `k2oddworks/vegas-sidekick`.

## Read first

For show-page work, read these in order:

1. `SHOW-PAGE-BENCHMARK.md`
2. `BRAND.md`
3. `VS_CHAT_CONTEXT.md`
4. `SHOW-BUILDER-PROMPT.md` only for implementation details that do not conflict with the current benchmark

The current show-page benchmark is:

`shows/magic/nathan-burton-comedy-magic/index.html`

If an older Carrot Top, Absinthe, V Theater, or other template conflicts with Nathan Burton or `SHOW-PAGE-BENCHMARK.md`, **Nathan Burton wins**.

The shared showtimes booking module is a newer locked system and supersedes older Nathan/Carrot Top day-card schedule treatments where they conflict.

For **Sidekick Index** work, read `SIDEKICK-INDEX.md` first. It is the canonical source for Index taxonomy, source files, shared navigation/signup behavior, data boundaries, and mobile horizontal-scroll rules.

## Repository

- Repo: `k2oddworks/vegas-sidekick`
- Default / production branch: `main`
- Site: `https://vegassidekick.com/`
- Largely static HTML/CSS/JS deployed through Cloudflare

Do not assume a push is live. Verify production when the task requires a live claim.

## Working style

- Before broad changes, explain the implementation approach and get Kris’s approval unless he already explicitly authorized the work.
- If Kris says “make live,” “publish,” or “push to main,” that authorizes the production-branch write.
- Make targeted changes. Do not opportunistically redesign unrelated pages.
- Prefer reusable systems over one-off page hacks.

## Brand / copy

Use the Vegas Sidekick Brand Bible voice: a knowledgeable Vegas local who works in tickets helping a friend.

One-line test:

> Would a Vegas local who works in tickets actually say this to a friend?

Never invent first-hand attendance or experience.

Do not use fake urgency, fake scarcity, generic trust theater, unsupported ratings, or unsupported superlatives.

### Current show-page copy rules

- No formal recurring **Think twice / downside / honest downside** sections.
- Active show pages should include a compact **What is [Show]?** descriptive overview before Quick Take. Explain the actual entertainment product using verified show-specific details; aim for entity completeness, not keyword density.
- Keep Hero, descriptive overview, and Quick Take distinct: Hero identifies the show, the overview explains what happens / what it is, and Quick Take helps the customer decide whether it fits.
- Do not impose a hard SEO word minimum or pad pages with filler. Never repeat the hero sentence as the descriptive section.
- **Good to know** only when there is a real useful fact; omit it otherwise.
- **Good Fit** should be positive and compact. Keep it inside Quick Take using the shared compact treatment; do not repeat it later in a separate **Who it fits best** section.
- **Kris’s take** should reinforce why the show is a good choice, not inject generic doubt.
- Do not use **tradeoff** in customer-facing copy; describe what each option offers.
- Do not use **Typical start**; use **Start time / Start times**.
- Prefer **See available dates & times →** for schedule inventory links.
- Preferred price line: **Tickets start at $X. Other price points may be available.**
- Keep one visible freshness line near the author card: **Show info confirmed Month YYYY**.
- Booking tips are optional and must be genuinely actionable; remove filler.
- Do not narrate obvious UI behavior.
- Do not describe a show or seat as interactive / in the action / likely to get picked unless Kris explicitly confirmed that fact.

## Show-page system

Use the shared canonical assets and current page structure rather than rebuilding from scratch:

- `assets/show-canonical.css`
- `assets/show-canonical.js`
- `assets/showtimes-booking.css`
- `assets/showtimes-booking.js`
- current show database / source-of-truth data
- current audits

Primary ticket CTAs use Warm Amber `#FFB000`.

Every current show product page uses the shared **Share this show** control in the hero. It is deliberately secondary to the ticket CTA. On supported mobile/browser environments it opens the native share sheet; otherwise it copies the canonical Vegas Sidekick show URL. It must share the Vegas Sidekick page, never the affiliate ticket URL. Do not add the control to the mobile sticky purchase bar.

Mobile heroes use the established safe treatment unless a show-specific focal override is needed.

### Locked showtimes booking system

The shared showtimes module is now the production standard for active show pages.

For shows with a verified regular weekly schedule:

- Show all seven weekday choices in a compact picker.
- Active days are selectable; verified dark days are visibly muted and labeled **Dark**.
- Selecting a day updates the showtime choices immediately.
- Showtime buttons and the primary **Get Tickets →** CTA use the show’s existing verified affiliate URL.
- Keep the primary CTA Warm Amber `#FFB000`.
- Keep **See all dates & times →** as a compact secondary text action beneath the primary purchase path.
- Put a compact booking pill above the headline. Default copy is **CHOOSE YOUR DAY** for regular schedules and **CHECK YOUR DATE** for variable schedules. Use show-specific factual copy only when it is verified, such as a closing date.
- Wrap the white booking card in the shared large solid category-color block. Use the locked palette: Music `#2563EB`, Magic `#6D28D9`, Comedy `#C2185B`, Adult `#C2410C`, Cirque + Spectaculars `#0C7A90`, Family `#087F23`. Do not restore the retired skyline / Sphere artwork.

For genuinely variable schedules:

- Do not fabricate weekday buttons or recurring times.
- Use the variable-date version of the shared module.
- State that the schedule varies by date and send the customer to **See available dates & times →** using the verified ticket URL.

Use the shared assets rather than copying per-show CSS/JS. The show database schedule is the source of truth for generated weekday/time choices.

## Seating charts

The Nathan Burton Theater implementation is the first locked reusable room-layout benchmark:

- `data/seat-layouts/nathan-burton-theater.json`
- `assets/seat-layouts/nathan-burton-theater.css`
- `assets/seat-layouts/nathan-burton-theater.js`
- `images/nathan-burton-theater-seating-chart.svg`
- `scripts/generate-seat-layout-assets.py`

### Approved seating-chart image rule

If Kris supplies or explicitly approves a seating-chart image, **that exact image becomes the visual source of truth**.

- Use the supplied/approved chart directly in the photo gallery and as the visible base of the interactive seat guide.
- **Do not redraw, rebuild, trace, reinterpret, or regenerate the chart geometry.**
- Add interactivity with transparent hit zones layered over the supplied image, following the Zombie Burlesque pattern.
- Keep recommendation data (Sweet Spot / Our Pick, section descriptions, etc.) separate from the visual asset so recommendations can change without altering the chart.
- The generated/reusable room-geometry system below is the fallback only when no approved chart image has been supplied.

Rules when using generated room geometry:

- Model **room geometry once**, then reuse it across shows in that room.
- Recommendations / copy can differ by show.
- Make the branded chart resemble the real room.
- Use row slabs when exact seat counts are not verified or unnecessary.
- Keep the physical section name separate from recommendation labels like **Sweet spot / Our Pick**.
- Mobile tap feedback must appear immediately in view.
- Do not add generic seating disclaimers.
- Static seating-chart gallery assets should come from the same underlying geometry as the interactive chart unless an approved supplied chart image is the source of truth.

## Image library organization

The image library is organized by purpose rather than as a flat /images folder.

- Show photography / artwork: `/images/product-photos/<show-slug>/`
- Seating charts: `/images/seating-charts/<show-or-room>/`
- Venue imagery: `/images/venue-photos/<venue-slug>/`
- Brand / Spike / Kris assets: `/images/brand/`
- Guide covers: `/images/guides/`
- Sidekick Index social assets: `/images/sidekick-index/`
- News / Dispatch assets: `/images/news/`
- Play / game assets: `/images/play/`
- Site-level social imagery: `/images/site/`

Do not add new image files directly to the root `/images/` directory. Keep descriptive filenames even inside named folders.

## Photos / gallery

Show photo viewers should support:

- previous / next arrows on desktop
- keyboard left / right
- swipe on mobile
- subtle image count

Odd-aspect images must not break the desktop gallery. Preserve descriptive alt text.

## Affiliate / media rules

- Never guess a ticket affiliate URL.
- Vegas Sidekick referral paths use `/ref/vegassidekick` when verified.
- Do not mention the ticket partner by name in visible customer copy unless explicitly directed.
- Official YouTube embeds only; never invent or re-host trailers.
- For verified official trailers, use the shared `assets/show-video.css` + `assets/show-video.js` component with `.vs-video[data-youtube-id]`; load the YouTube iframe only after an explicit play click.
- Use real approved show/event photography. Do not generate fake event imagery for real shows.

## Savings and price comparisons

- **Source of truth:** `data/show-database.json` holds starting `our_price`, optional `regular_price`, derived `savings_amount` / `savings_percent` / `is_deal`, and the evidence date `price_source_last_checked_on`. Verify the Spotlight comparison before adding or extending a savings claim; never invent a regular price or claim an entire date/seat selection receives the starting-price discount.
- **Deal threshold:** show a comparison only when the valid regular starting price exceeds our starting price by at least **$5**. Savings from **$5–$19** use the compact amber treatment.
- **Large treatment:** currently verified savings of **$20 or more** qualify for the approved lime-green show-page hero treatment, compact mobile reminder and final savings panel before the unchanged **Warm Amber `#FFB000`** ticket CTA. Use `shows/music/all-shook-up/index.html` as the savings-specific visual reference and shared `assets/show-savings.css`. Nathan Burton remains the overall show-page benchmark.
- **Stage 5 catalog system:** `assets/catalog-savings.js` calculates savings and large green-card eligibility directly from active Show Database records. Do **not** restore a handwritten green-show slug allowlist. The catalog script updates price/badges on rerender, removes invalid comparisons and suppresses **large catalog-card savings** when `price_source_last_checked_on` is absent or older than **30 days**.
- **Critical distinction:** show-page savings banners and the static Deals page do **not** automatically disappear at day 30. `scripts/audit-savings-freshness.py` warns after 14 days and fails after 30 days for large claims; update or remove stale show-page / Deals claims as part of the source-verification workflow. A source-check date is separate from the visible **Show info confirmed Month YYYY** author-card line. Never change verification dates without actually checking the source.
- **Price propagation:** category page literal arrays, show pages, structured data, guides, homepage, venue pages and `/shows/deals/` may contain denormalized prices. The catalog browser script is **not** a substitute for editing those static sources after an actual price change.
- **Checks for pricing/savings work:** run `python3 scripts/audit-savings-system.py`, `python3 scripts/audit-final-savings-banners.py`, `python3 scripts/audit-price-reconciliation.py`, `python3 scripts/audit-savings-freshness.py`, `python3 scripts/audit-category-catalog-prices.py`, `node --check assets/catalog-savings.js`, plus relevant show/schema/CTA checks. The recurring workflow is `.github/workflows/savings-audit.yml`.

Detailed rollout history and exceptions: `docs/staged-savings-rollout.md`.

## Show ticket SEO metadata (October 2026)

Vegas Sidekick competes for **Las Vegas discounted show tickets**, not only general show discovery. Product-page metadata must sell the right *verified* offer without inventing savings.

- Each active show page needs a unique, legible, show-name-first HTML title and show-specific meta description. Preserve the production's recognizable name; keep "Las Vegas" and "| Vegas Sidekick" when length permits.
- Use **Discount Tickets** in an active show-page title only with a source-verified starting-price comparison in `data/show-database.json`: `savings_amount >= 5`, `regular_price > our_price`, and `price_source_last_checked_on` no older than **30 days**. This is a starting-ticket comparison, never a promise that every performance or seat is discounted.
- Otherwise prefer **Tickets from $X** using `our_price`. A historical `regular_price` without a recent check is **not** adequate support for a discount title.
- Meta descriptions should lead with a verifiable price or starting-price savings where relevant, followed by a real, distinct show fact. Do not fall back to generic filler across dozens of shows.
- Category, all-shows and Deals landing pages may target **ticket discounts** if they offer a mixture of verified deals and regularly priced shows; never imply every listing is discounted. Do not put an annual year (e.g. 2026) in evergreen category titles, social titles or visible category badges. Retain real event/closure years in archive or event dates.
- On *every* price or savings change, reconcile the HTML title/meta description alongside the show database and existing category, homepage, Deals, guide and schema propagation paths. When a comparison expires, recheck the ticket source or remove the unverified savings language. Do not change the price verification date without checking.
- Organic search titles are not the same as the customer-facing H1, hero, or social-copy voice. Do not rewrite the buyer journey merely to fit keywords.

## Structured data

For active shows:

- use appropriate Event / EventSeries schema
- `offers.price` is a bare number
- do not fabricate schedules
- visible FAQ and FAQ schema must agree
- keep WebPage author / date metadata accurate

Closed shows stay archived, are removed from active catalogs / ticket CTAs / active Event schema, and are never simply deleted.

## Required checks

Use the audits relevant to the change. For show-page work, the common minimum is:

```bash
python3 scripts/audit-show-page-benchmark.py
python3 scripts/audit-event-schema.py
python3 scripts/audit-ticket-cta-color.py
python3 scripts/audit-mobile-show-heroes.py
python3 scripts/audit-catalog-js-syntax.py
python3 scripts/audit-orphan-ui.py
git diff --check
```

Do not reference audit scripts that do not exist; inspect `scripts/` when uncertain.

## Deployment

GitHub writes and Cloudflare deployment are separate facts.

- It is safe to say **committed / merged to main** when verified.
- Only say **live** after verifying the public site when that matters.
- A Cloudflare deploy failure can be credential-related; do not misrepresent a failed deploy as successful.

---

## Good to Know social-series reference

Vegas Sidekick's recurring **Good to Know** social series is governed by `GOOD-TO-KNOW.md`.

- It is the customer-service social layer for verified show changes that affect planning or booking: start times, venue moves, return dates, performance-day changes, meaningful added dates, closing dates and similar material updates.
- It is distinct from **Vegas Dispatch**, which is the editorial/news product.
- Use approved repo photography, artwork, show logos and Vegas Sidekick branding exactly as supplied. Do not generate replacements or lookalikes.
- Store recurring series assets under `/images/good-to-know/`.

The social series is separate from the optional **Good to know** information card used on show pages. The shared name does not change show-page rules: only use that page card when there is a genuinely useful buyer fact.


# Vegas Sidekick Internal Linking Strategy

## Goal

Internal links should help a visitor answer the next useful question while also making the site architecture obvious to search engines.

The system is built around five page families:

1. **Show pages** — conversion pages.
2. **Guides and comparisons** — decision pages.
3. **Category pages** — discovery hubs.
4. **Venue/property pages** — location/planning hubs.
5. **Vegas Dispatch** — freshness and discovery engine.

The linking hierarchy is not a pyramid. It is a set of useful loops:

`Dispatch → Guide / Show / Venue → Related Show → Guide / Category / Venue`

`Guide → Show → Related Show / Venue / Category → Guide`

`Venue → Show → Venue / Guide / Related Show`

## Rules

### 1. Show pages

Every active show page should expose, where relevant:

- **Related shows:** 2–4 real alternatives.
- **Category:** at least one category/discovery link.
- **Venue/property:** a useful venue/property link when a matching hub exists.
- **Guide:** at least one relevant guide when the show legitimately belongs in one.

The existing **You may also like** and **Make the next click useful** sections are the primary implementation surfaces. Do not stuff body copy with repeated keyword links merely to increase counts.

### 2. Guides

Every guide should:

- link directly to every recommended show page;
- link to the relevant category hub where one exists;
- link to 1–3 adjacent guides only when they answer a materially different decision;
- receive links back from the shows it materially features when the show page has a natural guide slot.

Guide rankings are editorial decisions. Automation may flag missing relationships but must not add or reorder recommendations.

### 3. Vegas Dispatch

Every Dispatch article should have **2–5 contextual internal links** when legitimate targets exist.

Priority order:

1. directly affected show or attraction page;
2. relevant venue/property page;
3. relevant guide or comparison;
4. category hub;
5. another Dispatch article only when it materially adds context.

Use the mid-article and **Make the next click useful** modules for clean linking. News should feed evergreen pages rather than becoming an isolated archive.

### 4. Venue/property pages

Every venue/property hub should:

- link to the shows physically associated with that property/cluster;
- link to useful nearby/adjacent planning pages only when real;
- receive links back from show pages at that property where a matching hub exists.

Do not invent a venue relationship simply because two properties are geographically close.

### 5. Category pages

Category pages are structural hubs. They should:

- link to all appropriate active shows in that category;
- link to relevant high-intent guides where useful;
- receive links from show pages and guides naturally associated with the category.

Show classifications are not to be changed by the internal-linking system.

## Anchor text

Prefer descriptive, reader-facing anchors:

- `See all Las Vegas magic shows`
- `Compare the best Cirque shows`
- `More shows at MGM Grand`
- `Read our first-timer picks`

Avoid repetitive exact-match SEO anchors across many pages. Never use vague anchors such as `click here` when a useful description fits.

## Link placement priority

1. Contextual body link where it genuinely helps the sentence.
2. Existing related/recommendation modules.
3. Existing **Make the next click useful** module.
4. Breadcrumb/category navigation.
5. Global header/footer navigation.

Global navigation is important architecture, but it does not replace contextual links.

## Minimum useful-link targets

These are audit thresholds, not quotas to game:

| Page family | Minimum contextual outbound links | Expected inbound links |
|---|---:|---:|
| Active show | 3 | 2 |
| Guide | 4 | 2 |
| Dispatch article | 2 | 1 |
| Venue/property hub | 3 | 2 |
| Category hub | 3 | 2 |

A page below the threshold is a review candidate, not automatic permission to insert arbitrary links.

## New-content checklist

Before publishing any new Guide or Dispatch article:

- [ ] Add useful outbound links to relevant show/category/venue/guide pages.
- [ ] Add 2–5 inbound links from existing relevant pages where legitimate.
- [ ] Avoid linking multiple times to the same target without a reader reason.
- [ ] Verify every local target exists.
- [ ] Run `python3 scripts/audit-internal-links.py`.

Before publishing a new show page:

- [ ] Add related shows.
- [ ] Add category/discovery link.
- [ ] Add venue/property link if a matching hub exists.
- [ ] Add a relevant guide link if editorially justified.
- [ ] Add inbound links from category, venue and relevant guides.

## Maintenance cadence

### Weekly

- Run the graph audit.
- Review new orphan/underlinked pages.
- Internal-link newly published Guide/Dispatch content into relevant evergreen pages.

### Monthly

- Review pages with fewer than two contextual inbound links.
- Review high-value pages with weak internal support.
- Check for broken internal targets.
- Look for Dispatch stories that should now feed newer evergreen pages.

### Quarterly

- Review hub coverage by category, venue and topic.
- Remove stale links to closed/obsolete destinations where the destination is no longer useful.
- Keep closed show pages alive, but stop treating them as active conversion destinations.

## Automation boundary

Automation may:

- crawl local HTML;
- count contextual inbound/outbound links;
- detect orphan/underlinked pages;
- detect broken local targets;
- generate reports and GitHub issues.

Automation may **not**:

- change a show's category;
- invent venue relationships;
- add shows to Guides;
- decide recommendation order;
- create keyword-stuffed body links;
- treat a link-count threshold as editorial authority.

The rule is simple: **detect automatically, link deliberately.**

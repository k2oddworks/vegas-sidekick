# Vegas Sidekick Operations Board

## Governing priority

**P0 Accuracy → P1 Revenue → P2 Growth → P3 Enhancement**

Known P0 work blocks new editorial/enhancement work until resolved. Automation may detect problems; it does not get editorial authority and must never invent a missing fact.

## Board columns

Use a GitHub Project named **Vegas Sidekick Operations** with these Status values, in order:

1. Inbox
2. P0 Accuracy
3. P1 Revenue
4. P2 Growth
5. P3 Enhancement
6. In Progress
7. Needs Kris
8. Ready to Ship
9. Shipped / Verify
10. Done

`Shipped / Verify` is intentionally separate from Done. A commit on `main` is not proof the public Cloudflare deployment succeeded.

## Labels

Source of truth: `.github/labels.yml`. The `Operations Bootstrap` workflow synchronizes the label set after changes land on `main`.

Priority labels: `P0 Accuracy`, `P1 Revenue`, `P2 Growth`, `P3 Enhancement`.

Workflow/status labels: `Needs Kris`, `Ready to Ship`, `Verify Live`.

Work labels: `show`, `guide`, `dispatch`, `venue`, `comparison`, `seo`, `schema`, `media`, `internal-links`, `conversion`, `automation`, `closure`, `price`, `schedule`.

## Recurring cadence

The `Vegas Sidekick Operations Cadence` workflow creates the review issue for each cycle.

### Weekly

- Clear P0 first.
- Review ticket CTA clicks/CTR and mobile vs desktop.
- Review rankings 4–15, high-impression/weak-CTR pages, and meaningful declines.
- Diagnose P1 opportunities before redesigning anything.
- Publish or materially advance at least one Guide, Dispatch, comparison, or venue item.
- Internal-link new content into relevant existing pages.
- Improve media only on priority pages.

### Twice monthly

Verify every active show's running status, venue, starting price, schedule/dark days, age rules, verified Spotlight URL, catalog presence, schema, guide claims, categories, and venue references. Propagate one verified change to every denormalized surface. One changed show should normally be one parent issue listing all affected files.

### Monthly

Review acquisition, conversion, commercial results, content shipped, P0 debt, technical health, media priorities, and maintenance debt. Choose next month's highest-value search, conversion, venue/comparison, and media targets.

### Quarterly

Answer:

1. What is making money?
2. What is almost working?
3. What is decaying?
4. What is missing?
5. What should we stop doing?

Then publish the next 90-day roadmap.

## Automation boundary

### Automate completely

- schema validation
- broken internal paths
- duplicate canonical detection
- media inventory
- recurring review issue creation
- label synchronization

### Automate detection; human verifies correction

- price changes
- schedule/dark-day changes
- venue changes
- closures/extensions
- age-policy changes
- Search Console traffic/CTR/ranking opportunities
- guide stale claims
- affiliate URL changes

### Human judgment only

- Kris's Take
- recommendation order
- Good Fit / Good to Know judgment
- comparison verdicts
- guide inclusion/ranking
- material editorial tone/positioning
- disputed factual source selection
- approval of a Spotlight URL as verified

## Issue contract

Every operational issue must contain:

- priority
- page/show/workstream
- evidence or detected mismatch
- verified source of truth for factual changes
- affected files/surfaces
- required action
- explicit pass condition

P0 uses `.github/ISSUE_TEMPLATE/p0-accuracy.yml`; P1–P3 use `.github/ISSUE_TEMPLATE/operations-work.yml`.

## P1 diagnosis vocabulary

Every revenue opportunity should be classified as one of:

- traffic problem
- SERP problem
- recommendation problem
- CTA problem
- product-information problem
- not worth touching yet

No random redesigns without a diagnosis.

## Content opportunity score

Score each candidate before it becomes priority work:

| Factor | Points |
|---|---:|
| Strong booking intent | 0–3 |
| Search demand/opportunity | 0–3 |
| Supports existing show pages | 0–2 |
| Timeliness | 0–2 |
| Internal-link value | 0–2 |
| Vegas Sidekick can add real editorial value | 0–3 |

Maximum 15. Candidates at 11+ normally move toward the top, subject to P0/P1 work.

## Maintenance debt

Track a visible score from unresolved issues. Suggested weights:

| Issue | Weight |
|---|---:|
| Wrong booking URL | 10 |
| Closed show listed active | 10 |
| Wrong price | 8 |
| Wrong schedule | 8 |
| Schema failure | 5 |
| Broken internal link | 3 |
| Stale guide copy | 3 |
| Missing photo | 1 |
| Missing verified video | 1 |

The score is directional, not a substitute for judgment.

## Monthly dashboard

Keep these core measures visible:

1. Organic clicks
2. Organic impressions
3. Organic CTR
4. Pages/queries ranking 4–15
5. Ticket CTA clicks
6. Ticket CTA CTR
7. Mobile CTA CTR
8. Guide → show CTR
9. Related-show CTR
10. Affiliate bookings/revenue
11. Pages with accuracy issues
12. Priority-page media completion
13. Maintenance debt score

## Shipping rule

`Ready to Ship` means implementation and repo validation are complete. `Shipped / Verify` means the change is on `main` but public deployment has not yet been independently confirmed. Move to `Done` only after the intended result is verified.

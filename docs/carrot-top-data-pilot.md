# Carrot Top structured data pilot

`data/shows/carrot-top.json` is the first Vegas Sidekick show source-of-truth record.

`scripts/sync-carrot-top-from-data.py` currently syncs only deterministic Carrot Top facts into the existing hand-written page:

- from price
- Spotlight affiliate URL
- runtime
- weekly schedule / dark day
- age-policy paragraph
- hotel / showroom details
- approved YouTube trailer ID
- EventSeries offer, venue and schedule fields
- price/runtime-dependent SEO metadata

The script deliberately leaves editorial sections such as the quick take, seat advice, quiz logic, related-show recommendations and general prose untouched.

Pilot validation on September 7, 2026 passed:

- Event/EventSeries schema audit
- SERP metadata audit
- content/link hygiene audit
- internal-link graph audit

The initial test also caught two failure modes before merge: markup assumptions and unsafe broad string replacement inside JSON-LD. The final sync uses strict visible-markup matches and parsed JSON-LD updates instead.

# Deliberate related-show link overrides

Vegas Sidekick uses `scripts/apply-internal-link-overrides.py` for a small number of high-confidence editorial relationships that should survive generated show-page rebuilds.

Current override:

- The Mentalist → MIND2MIND
- Colin Cloud: Mastermind → MIND2MIND

These links are based on direct topical similarity (mentalism / mind reading), not category stuffing or guide-ranking changes.

After a bulk canonical show-page rebuild, rerun:

```bash
python3 scripts/apply-internal-link-overrides.py
python3 scripts/audit-internal-links.py
```

---

## Good to Know social-series reference

Vegas Sidekick's recurring **Good to Know** social series is governed by `GOOD-TO-KNOW.md`.

- It is the customer-service social layer for verified show changes that affect planning or booking: start times, venue moves, return dates, performance-day changes, meaningful added dates, closing dates and similar material updates.
- It is distinct from **Vegas Dispatch**, which is the editorial/news product.
- Use approved repo photography, artwork, show logos and Vegas Sidekick branding exactly as supplied. Do not generate replacements or lookalikes.
- Store recurring series assets under `/images/good-to-know/`.

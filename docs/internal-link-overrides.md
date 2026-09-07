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

# Show catalog JavaScript repair — 2026-09-08

A Spotlight reconciliation introduced invalid JavaScript string literals into show catalog data where venue names containing apostrophes were interpolated unsafely.

Repaired affected catalog records:
- X Burlesque / Bugsy's Cabaret
- Tournament of Kings / King Arthur’s Arena

Validated all root/category show catalog inline JavaScript with Node syntax checking.

Permanent safeguard: `scripts/audit-catalog-js-syntax.py`, run by Vegas Sidekick Operations Audits on show/catalog changes and weekly cadence.

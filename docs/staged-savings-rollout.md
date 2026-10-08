# Stage rollout: lime-green savings treatment

## Stage 1 — October 8, 2026

Approved visual benchmark: `shows/music/all-shook-up/index.html`.

Eight new pages use the existing shared `assets/show-savings.css`: Piano Man, All Motown, America The Show, Zombie Burlesque, V – The Ultimate Variety Show, The Mentalist, Paranormal, and Tape Face.

All Shook Up remains the locked comparison example. Carrot Top retains the earlier small-discount hero trial.

Each Stage 1 page has the green hero savings message, a large savings reinforcement above the final amber Get Tickets action, and an inline savings pill in the existing compact sticky mobile bar. Selected cards in their category catalogues and `/shows/deals/` receive green savings pills.

The source of truth for price and regular price is `data/show-database.json`. Savings are for the compared *starting* ticket price, not every date or section. Do not guess regular prices. Keep Warm Amber for Get Tickets. Show-info confirmation dates are separate from visual update dates.

New guard: `python3 scripts/audit-final-savings-banners.py`, included in `savings-audit.yml`. The original `audit-savings-system.py` remains, including previously known unrelated pricing errors.


## Stage 2 — October 8, 2026

Added eight more pages with the same All Shook Up hero savings treatment, compact mobile sticky reminder, and final green savings panel before the Warm Amber booking CTA. Updated category and Deals-page card badges; unchanged affiliate destinations:

- King of Diamonds — $60 (60%)
- Wastin' Away — $60 (60%)
- Penn & Teller — $41 (38%)
- KÀ — $38 (32%)
- VEGAS! The Show — $38 (38%)
- MJ Live — $36 (40%)
- Motown Brunch — $35 (35%)
- Shin Lim: LIMITLESS — $35 (34%)

**Held for price reconciliation:** Las Vegas LIVE Comedy Club (hero $122; lower-page $29), Purple Reign (hero $51; lower-page $56), and Wayne Newton (hero $84; lower-page $93). Do not apply green savings banners or update comparisons for these until the current starting price and regular price have been verified and synchronized sitewide. This is separate from the legacy savings audit mismatches for Atomic Saloon, Blue Man Group and Tournament of Kings.

Stage 2 checks: `scripts/audit-final-savings-banners.py` now requires the original All Shook Up benchmark, Stage 1 and Stage 2 pages. Also run ticket CTA and operational audits; don't claim source prices were reverified merely because display markup changed.

## Next

Stage 3: review remaining qualifying $20+ offers, prioritizing price reconciliation before any rollout. Smaller discounts stay compact until separately approved.

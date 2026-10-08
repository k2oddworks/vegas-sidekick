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

## Price reconciliation — October 8, 2026 (pre-Stage 3)

Cross-checked advertised starting prices and regular-price comparisons against Spotlight.Vegas product listings. These are advertised starting prices, not a booking-level guaranteed total. Keep historical show-price-index snapshots dated as historical; do not rewrite September snapshots.

- **Atomic Saloon:** Spotlight shows $100 with no regular comparison. Regular price now unknown/null, not a discount. Remove stale $10 deal from database and Deals listing.
- **Blue Man Group:** Spotlight shows $68 compared with $90. Replace stale $92 and recompute savings to $22 (24%).
- **Tournament of Kings:** Spotlight shows $78 compared with $88. Correct derived savings to $10 (11%).
- **Purple Reign:** Spotlight shows $51 compared with $95. Synchronize hero, FAQ, final section and mobile sticky price at $51; savings remain $44 (46%).
- **Wayne Newton:** Spotlight shows $84 compared with $121. Synchronize hero, FAQ, final section and mobile sticky price at $84; savings remain $37 (31%).
- **Las Vegas LIVE Comedy Club:** Spotlight currently says **Not Available**, while the product listing shows historical/advertised $29 compared with $34. Internal record marked `needs_review`. Preserve show information; remove active offers, booking controls and deal marketing from the page, and exclude from Deals until source bookability returns. The database keeps the last advertised $29 and underlying Spotlight price comparison ($34) for future review without presenting it as a currently bookable deal. Do not mark the show permanently closed on this evidence alone.

Rebuilt `shows/deals/index.html` to show 49 qualified active offers and remove unsupported cards for Michael Jackson ONE, Awakening and Marriage Can Be Murder, in addition to Atomic Saloon and unavailable Las Vegas LIVE Comedy Club. Fixed the missing Paranormal savings label. All listings are now calculated against the active Show Database.

Permanent guard: `scripts/audit-price-reconciliation.py` checks price integrity, all Deals listings and the unavailable-booking surface. It runs alongside existing audits in `.github/workflows/savings-audit.yml`.

Spotlight source pages checked:
- https://spotlight.vegas/shows/adult/atomic-saloon/
- https://spotlight.vegas/shows/production/blue-man-group/
- https://spotlight.vegas/shows/production/tournament-of-kings/
- https://spotlight.vegas/shows/tribute/purple-reign/
- https://spotlight.vegas/shows/music/wayne-newton/
- https://spotlight.vegas/shows/comedy/las-vegas-live-comedy-club/

Stage 3 may proceed on other qualifying offers after verifying source availability and price comparisons. Recheck Las Vegas LIVE Comedy Club before reinstating active tickets.

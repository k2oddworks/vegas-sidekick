# Stage rollout: lime-green savings treatment

## Stage 1 — October 8, 2026

Approved visual benchmark: `shows/music/all-shook-up/index.html`.

Eight new pages use the existing shared `assets/show-savings.css`: Piano Man, All Motown, America The Show, Zombie Burlesque, V – The Ultimate Variety Show, The Mentalist, Paranormal, and Tape Face.

All Shook Up remains the locked comparison example. Carrot Top retains the earlier small-discount hero trial.

Each Stage 1 page has the green hero savings message, a large savings reinforcement above the final amber Get Tickets action, and an inline savings pill in the existing compact sticky mobile bar. Selected cards in their category catalogues and `/shows/deals/` receive green savings pills.

The source of truth for price and regular price is `data/show-database.json`. Savings are for the compared *starting* ticket price, not every date or section. Do not guess regular prices. Keep Warm Amber for Get Tickets. Show-info confirmation dates are separate from visual update dates.

New guard: `python3 scripts/audit-final-savings-banners.py`, included in `savings-audit.yml`. The original `audit-savings-system.py` remains, including previously known unrelated pricing errors.

## Next

Stage 2: review remaining shows with verified savings of $20+ and apply approved shared treatment in another small group, after checking any stale price comparisons. Smaller discounts can keep compact green savings pills until an explicit expansion is approved.

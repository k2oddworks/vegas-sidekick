# Vegas Sidekick Hub — PRIVATE DEPLOYMENT ONLY

**Branch:** `feature/private-sidekick-hub`  
**Proposed production route:** `https://vegassidekick.com/hub/` (NOT live)

## What is committed

- `index.html`: responsive hub prototype with Index Desk, Show-page QA, and an internal change log.
- `scan-01.json` through `scan-05.json`: detected evidence from the 67 active show HTML pages, read from the existing repository on November 6, 2026 (not independent factual verification).
- QA show catalog obtained from `data/show-database.json`; repository snapshot counted 67 active, six closed, one needs review. Closed shows remain in the archive.
- Index source imports use `data/reference/headliners-residencies.json` and `data/reference/touring-shows-concerts.json` from main. Original snapshot dates and source links are preserved.
- Browser-local edit persistence, manual QA verdicts and reason-required N/A, photo candidates vs approved photos, trailer verification vs installation, and an audit history with before/after state.
- CSV QA exports, Index CSV/JSON/Markdown exports, calendar/list Index views.

## Crucial limitations (do not describe as production-ready)

1. The current prototype uses **localStorage** for user edits. It does not synchronize across devices.
2. The QA snapshot does not by itself verify correctness or media relevance. Factual checks start pending.
3. Re-scanning does not yet provide a complete hash-based evidence-change review workflow.
4. The integrated Index workspace now includes paginated 1080 x 1080 PNG graphic export, but real-browser download behavior and fidelity have not yet been tested; its calendar and filtering still need parity checks against the standalone desk.
5. Browser/device-level end-to-end regression testing, persistence, actual Cloudflare Access, and D1 backend have **not** been completed.
6. Do not merge this branch into main while any of these security/deployment issues remain unresolved.

## Required private deployment architecture

Cloudflare Access should cover `vegassidekick.com/hub/*` using an identity-verified allowlist containing ONLY Kris's chosen email address(es). The policy must cover all HTML, JS, JSON, assets, API paths, and future exports. Do not use client-side passwords, robots.txt or noindex as security.

Attach a D1 database to a Worker API behind the same Cloudflare Access policy. Store Index engagements, show reviews, photo decisions, verified trailer metadata, user and scan evidence revisions, and an append-only change log. Use optimistic concurrency or per-record revision checking. Validate all inputs and audit before/after mutations on the server. Require authentication on the API, not merely on its HTML frontend.

**Critical:** GitHub main is a public-site deployment source. Publishing a `/hub/` folder to main before Cloudflare Access is configured could expose internal data. There is no GitHub connector capability to configure and independently verify Cloudflare Access, so this branch is intentionally not merged.

## Publishing separation

There is NO route from QA approval, saving an Index entry, or editing a source link to automatic changes on production show pages or public Index datasets. A future publish action must be explicit, previewed and separately authorized.

## Validation still needed

- Syntax and browser checks for all interface modes and narrow mobile widths.
- Search, filters, archived records, calendar month switches.
- Image candidate approval and photo goal, trailer verification/install states.
- QA N/A reason required and completion gating.
- Change log before/after and exports.
- Cross-device D1 persistence, concurrent edits and evidence-change preservation.
- Authenticated and unauthenticated access tests to every private path, INCLUDING raw JSON and API endpoints.
- Production verification after Cloudflare Access policy setup and deployment.

## Current reference

- `AGENTS.md` and `SHOW-PAGE-BENCHMARK.md` govern show-page UX.
- `BRAND.md`, `VS_CHAT_CONTEXT.md`, and `SHOW-BUILDER-PROMPT.md` govern brand and current show-page implementation.
- Benchmark: `shows/magic/nathan-burton-comedy-magic/index.html`.
- `SIDEKICK-INDEX.md` governs Index source and terminology.

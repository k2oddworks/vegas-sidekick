from pathlib import Path

PAGES = {
    Path('shows/music/vegas-the-show/index.html'): {
        'image': 'https://vegassidekick.com/images/vegas-the-show-hero.webp',
        'alt': 'VEGAS! The Show at Saxe Theater Las Vegas',
    },
    Path('shows/cirque/mystere/index.html'): {
        'image': 'https://vegassidekick.com/images/mystere-hero.jpg',
        'alt': 'Mystère by Cirque du Soleil at TI Las Vegas',
    },
}

for path, meta in PAGES.items():
    s = path.read_text(encoding='utf-8')

    if '<meta name="robots"' not in s:
        s = s.replace('</title>\n<meta name="description"', '</title>\n<meta name="robots" content="index,follow,max-image-preview:large">\n<meta name="description"', 1)

    if '<meta property="og:site_name"' not in s:
        s = s.replace('<meta property="og:title"', '<meta property="og:site_name" content="Vegas Sidekick">\n<meta property="og:title"', 1)

    if '<meta property="og:image:alt"' not in s:
        needle = f'<meta property="og:image" content="{meta["image"]}">'
        replacement = needle + f'\n<meta property="og:image:alt" content="{meta["alt"]}">'
        if needle not in s:
            raise SystemExit(f'Expected og:image not found in {path}')
        s = s.replace(needle, replacement, 1)

    if '<meta name="twitter:image"' not in s:
        s = s.replace('<meta name="twitter:card" content="summary_large_image">', '<meta name="twitter:card" content="summary_large_image">\n<meta name="twitter:image" content="' + meta['image'] + '">', 1)

    path.write_text(s, encoding='utf-8')

playbook = Path('SHOW-BUILDER-PROMPT.md')
s = playbook.read_text(encoding='utf-8')
section = '''## Current Show-Page Benchmark — Carrot Top\n\n**Current benchmark/model:** `shows/comedy/carrot-top/index.html`. For new show pages and major rebuilds, use Carrot Top as the interaction, conversion, motion, mobile UX, and SEO metadata benchmark. Preserve each show's own personality; reuse the system, not the skin.\n\n### Required SEO metadata package\nEvery rebuilt show page must include all of the following:\n\n- Unique `<title>` targeting the show plus useful Las Vegas ticket intent\n- Unique `<meta name="description">` using verified current price/venue/show facts\n- `<meta name="robots" content="index,follow,max-image-preview:large">`\n- Self-referencing canonical URL\n- Open Graph: `og:type`, `og:site_name`, `og:title`, `og:description`, `og:image`, `og:image:alt`, `og:url`\n- Twitter: `twitter:card=summary_large_image` and `twitter:image`\n- Preload the primary hero image used above the fold\n- JSON-LD: `EventSeries` (or `Event` when appropriate), `BreadcrumbList`, visible-FAQ-backed `FAQPage`, and `WebPage` author/date metadata\n- `offers.price` must be a bare numeric value with no `$`\n- Structured-data image order must match the page's primary social/hero image unless explicitly directed otherwise\n- Run `python3 scripts/audit-event-schema.py` before shipping and fix any issues caused by the changed page\n\nDo not add unverifiable urgency, discounts, fee claims, delivery promises, ratings, or review counts to metadata or structured data.\n\n---\n\n'''
marker = '## Building the Page (Technical Notes)\n'
if '## Current Show-Page Benchmark — Carrot Top' not in s:
    if marker not in s:
        raise SystemExit('Playbook insertion marker not found')
    s = s.replace(marker, section + marker, 1)
playbook.write_text(s, encoding='utf-8')

print('Standardized VEGAS! The Show and Mystère SEO metadata; documented Carrot Top benchmark.')

from pathlib import Path
import json
import re

PAGES = {
    Path('shows/music/vegas-the-show/index.html'): {
        'image': 'https://vegassidekick.com/images/vegas-the-show-hero.webp',
        'alt': 'VEGAS! The Show at Saxe Theater Las Vegas',
        'url': 'https://vegassidekick.com/shows/music/vegas-the-show/',
    },
    Path('shows/cirque/mystere/index.html'): {
        'image': 'https://vegassidekick.com/images/mystere-hero.jpg',
        'alt': 'Mystère by Cirque du Soleil at TI Las Vegas',
        'url': 'https://vegassidekick.com/shows/cirque/mystere/',
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

    def patch_json_ld(match):
        data = json.loads(match.group(1))
        if data.get('@type') in ('Event', 'EventSeries'):
            org = data.get('organizer')
            if isinstance(org, dict) and not org.get('url'):
                # Repo convention: use the canonical show page URL when no official organizer URL is stored.
                org['url'] = meta['url']
            offers = data.get('offers')
            if isinstance(offers, dict) and not offers.get('validFrom'):
                offers['validFrom'] = '2026-01-01'
            return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + '</script>'
        return match.group(0)

    s = re.sub(r'<script type="application/ld\+json">(.*?)</script>', patch_json_ld, s, flags=re.S)
    path.write_text(s, encoding='utf-8')

playbook = Path('SHOW-BUILDER-PROMPT.md')
s = playbook.read_text(encoding='utf-8')
section = '''## Current Show-Page Benchmark — Carrot Top\n\n**Current benchmark/model:** `shows/comedy/carrot-top/index.html`. For new show pages and major rebuilds, use Carrot Top as the interaction, conversion, motion, mobile UX, and SEO metadata benchmark. Preserve each show's own personality; reuse the system, not the skin.\n\n### Required SEO metadata package\nEvery rebuilt show page must include all of the following:\n\n- Unique `<title>` targeting the show plus useful Las Vegas ticket intent\n- Unique `<meta name="description">` using verified current price/venue/show facts\n- `<meta name="robots" content="index,follow,max-image-preview:large">`\n- Self-referencing canonical URL\n- Open Graph: `og:type`, `og:site_name`, `og:title`, `og:description`, `og:image`, `og:image:alt`, `og:url`\n- Twitter: `twitter:card=summary_large_image` and `twitter:image`\n- Preload the primary hero image used above the fold\n- JSON-LD: `EventSeries` (or `Event` when appropriate), `BreadcrumbList`, visible-FAQ-backed `FAQPage`, and `WebPage` author/date metadata\n- `organizer.url` must be present; use a verified official organizer URL when known, otherwise follow the repo convention used by existing benchmark pages\n- `offers.price` must be a bare numeric value with no `$`\n- `offers.validFrom` is required; use the real on-sale date when known, otherwise the repo default date documented in the structured-data rules\n- Structured-data image order must match the page's primary social/hero image unless explicitly directed otherwise\n- Run `python3 scripts/audit-event-schema.py` before shipping and fix any issues caused by the changed page\n\nDo not add unverifiable urgency, discounts, fee claims, delivery promises, ratings, or review counts to metadata or structured data.\n\n---\n\n'''
marker = '## Building the Page (Technical Notes)\n'
if '## Current Show-Page Benchmark — Carrot Top' not in s:
    if marker not in s:
        raise SystemExit('Playbook insertion marker not found')
    s = s.replace(marker, section + marker, 1)
else:
    s = re.sub(r'## Current Show-Page Benchmark — Carrot Top\n.*?\n---\n\n(?=## Building the Page \(Technical Notes\))', section, s, count=1, flags=re.S)
playbook.write_text(s, encoding='utf-8')

print('Standardized VEGAS! The Show and Mystère SEO metadata/schema; documented Carrot Top benchmark.')

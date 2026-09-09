#!/usr/bin/env python3
import json, re
from pathlib import Path

DB = Path('data/show-database.json')
SITEMAP = Path('sitemap.xml')

db = json.loads(DB.read_text())
rec = next((r for r in db.get('records', []) if r.get('slug') == 'o'), None)
if not rec:
    raise SystemExit('O record not found')
expected = {
    'status': 'active',
    'our_price': 156,
    'runtime_minutes': 90,
    'ticket_url': 'https://spotlight.vegas/shows/cirque-du-soleil/o/ref/vegassidekick',
}
for key, value in expected.items():
    if rec.get(key) != value:
        raise SystemExit(f'Unexpected O {key}: {rec.get(key)!r} != {value!r}')

rec.update(
    verified_on='2026-09-09',
    freshness_label='September 2026',
    venue='O Theatre – Bellagio',
    age_summary='5+',
    schedule_summary='Wed, Thu, Fri, Sat, Sun · 6:30 PM & 9 PM',
)
spot = rec.setdefault('spotlight', {})
days = {d: ['6:30 PM', '9 PM'] for d in ['Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']}
spot.update(
    location='O Theatre – Bellagio',
    our_price=156,
    regular_price=179,
    runtime_minutes=90,
    age_rule='Everyone must be 5 years of age or older to attend the event.',
    schedule_days=days,
    schedule_summary='Wed, Thu, Fri, Sat, Sun · 6:30 PM & 9 PM',
    schedule_variable=False,
    schedule_raw=[f'{d} - 6:30pm & 9:00pm' for d in days],
    spotlight_url='https://spotlight.vegas/shows/cirque-du-soleil/o/',
    affiliate_url='https://spotlight.vegas/shows/cirque-du-soleil/o/ref/vegassidekick',
    age_label='5+',
)
note = 'Schedule reverified 2026-09-09 against Spotlight and Bellagio: Wednesday–Sunday at 6:30 PM and 9 PM. No variable-schedule override applies.'
notes = (rec.get('notes') or '').strip()
rec['notes'] = notes if note in notes else (notes + ' ' + note).strip()
db['updated_on'] = '2026-09-09'
DB.write_text(json.dumps(db, ensure_ascii=False, indent=2) + '\n')

txt = SITEMAP.read_text()
marker = '<loc>https://vegassidekick.com/shows/cirque/o/</loc>'
start = txt.find(marker)
if start < 0:
    raise SystemExit('O sitemap entry not found')
stop = txt.find('</url>', start)
if stop < 0:
    raise SystemExit('O sitemap closing tag not found')
block = txt[start:stop]
block2, count = re.subn(r'<lastmod>[^<]+</lastmod>', '<lastmod>2026-09-09</lastmod>', block, count=1)
if not count:
    raise SystemExit('O sitemap lastmod not found')
SITEMAP.write_text(txt[:start] + block2 + txt[stop:])
print('O source data refreshed')

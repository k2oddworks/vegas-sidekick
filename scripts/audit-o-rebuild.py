#!/usr/bin/env python3
import json
from pathlib import Path
from bs4 import BeautifulSoup

page = Path('shows/cirque/o/index.html').read_text()
required = [
    'Tickets start at $156. Other price points may be available.',
    'data-seat-layout="o-theatre-bellagio"',
    '/images/o-theatre-bellagio-seating-chart.svg',
    '/assets/seat-layouts/o-theatre-bellagio.js?v=1',
    'Sections 201–205',
    'Show info confirmed September 2026',
    '>Start times<',
]
for marker in required:
    if marker not in page:
        raise SystemExit('Missing O marker: ' + marker)
for banned in [
    'Typical start', 'Typical weekly', 'tradeoff', 'Think Twice', 'Think twice',
    'Downside', 'Honest Downside', 'Last updated September',
    'Your date and seat determine the final total',
]:
    if banned in page:
        raise SystemExit('Banned/stale O copy: ' + banned)
if page.count('class="ticker-set"') != 2:
    raise SystemExit('Ticker duplication wrong')
if page.count('Show info confirmed September 2026') != 1:
    raise SystemExit('Freshness duplication wrong')

soup = BeautifulSoup(page, 'html.parser')
blocks = [json.loads(s.string or s.get_text()) for s in soup.find_all('script', attrs={'type': 'application/ld+json'})]
ev = next(x for x in blocks if x.get('@type') == 'EventSeries')
if ev['offers']['price'] != 156 or not isinstance(ev['offers']['price'], (int, float)):
    raise SystemExit('Bad price schema')
if ev['offers']['url'] != 'https://spotlight.vegas/shows/cirque-du-soleil/o/ref/vegassidekick':
    raise SystemExit('Bad affiliate URL')
if {x.get('startTime') for x in ev.get('eventSchedule', [])} != {'18:30', '21:00'}:
    raise SystemExit('Schedule schema drift')
faq = next(x for x in blocks if x.get('@type') == 'FAQPage')
visible = [(d.find('summary').get_text(' ', strip=True), d.find('p').get_text(' ', strip=True)) for d in soup.select('#faq details')]
structured = [(x['name'], x['acceptedAnswer']['text']) for x in faq['mainEntity']]
if visible != structured:
    raise SystemExit('FAQ/schema mismatch')
layout = json.loads(Path('data/seat-layouts/o-theatre-bellagio.json').read_text())
picks = {s['id'] for s in layout['sections'] if s.get('our_pick')}
if picks != {'201', '202', '203', '204', '205'}:
    raise SystemExit(f'Wrong sweet spot: {picks}')
svg = Path('images/o-theatre-bellagio-seating-chart.svg').read_text()
if 'width="1200"' not in svg or 'height="1440"' not in svg:
    raise SystemExit('SVG intrinsic dimensions missing')
rec = next(r for r in json.loads(Path('data/show-database.json').read_text())['records'] if r['slug'] == 'o')
if rec['spotlight'].get('schedule_variable') is not False:
    raise SystemExit('O schedule variable state wrong')
print('O regression checks passed')

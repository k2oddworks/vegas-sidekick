#!/usr/bin/env python3
from pathlib import Path
import json,re,sys

closed = {r['slug'] for r in json.loads(Path('data/show-database.json').read_text())['records'] if r.get('status') == 'closed'}
issues=[]
catalogs=[Path('shows/index.html'), *sorted(Path('shows').glob('*/index.html'))]
for p in catalogs:
    if not p.exists(): continue
    text=p.read_text(errors='ignore')
    for slug in closed:
        if re.search(r"\bslug\s*:\s*['\"]"+re.escape(slug)+r"['\"]",text):
            issues.append(f'{p}: closed show {slug} remains in active catalog data')
# Search and recommendation cards must not promote archived shows either.
search = Path('components/search-data.js').read_text()
for slug in closed:
    if f'/{slug}/' in search:
        issues.append(f'components/search-data.js: closed show {slug} remains in search')
for p in Path('shows').glob('*/*/index.html'):
    if p.parent.name in closed:
        continue
    for card in re.findall(r'<a\b[^>]*class="[^"]*(?:related-card|also-card)[^"]*"[^>]*>', p.read_text()):
        for slug in closed:
            if f'/{slug}/' in card:
                issues.append(f'{p}: closed show {slug} remains in recommendations')
print(f'Active catalog hubs checked: {len(catalogs)}')
if issues:
    print('\n'.join(issues)); sys.exit(1)
print('No closed shows remain in active catalog data.')

#!/usr/bin/env python3
"""Ensure static catalog cards match current Show Database starting prices."""
from pathlib import Path
import json
import re
import sys

root = Path(__file__).resolve().parents[1]
db = json.loads((root / 'data/show-database.json').read_text(encoding='utf-8'))
by_slug = {r['slug']: r for r in db['records']}
categories = ('music', 'magic', 'comedy', 'adult', 'family', 'cirque', 'spectaculars')
pattern = re.compile(r"\{\s*order:\s*\d+,\s*slug:'([^']+)'[^\n]*?\bprice:\s*([\d.]+),\s*pd:'\$([\d.]+)'")
issues = []
checked = 0
for category in categories:
    html = (root / 'shows' / category / 'index.html').read_text(encoding='utf-8')
    matches = list(pattern.finditer(html))
    if not matches:
        issues.append(f'{category}: no show cards parsed')
    for ext in ('js', 'css'):
        if '/assets/catalog-savings.' + ext + '?v=savings-stage5-20261009' not in html:
            issues.append(f'{category}: stale catalog savings {ext} version')
    for match in matches:
        slug, price, label = match.groups()
        checked += 1
        r = by_slug.get(slug)
        if r is None:
            issues.append(f'{category}/{slug}: unknown show')
        elif r.get('status') != 'active':
            issues.append(f'{category}/{slug}: non-active show in active catalog')
        elif float(price) != float(r['our_price']) or float(label) != float(r['our_price']):
            issues.append(f"{category}/{slug}: catalog price {price}/{label} versus database {r['our_price']}")
if issues:
    for issue in issues:
        print('FAIL: ' + issue)
    sys.exit(1)
print(f'PASS: {checked} starting-price references across {len(categories)} category catalogs')

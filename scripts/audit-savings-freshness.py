#!/usr/bin/env python3
"""Block stale or unverifiable large savings banners; warn on aging deals."""
from datetime import date
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / "data/show-database.json").read_text(encoding="utf-8"))
today = date.today()
MAX_BANNER_AGE_DAYS = 30
WARN_BANNER_AGE_DAYS = 14
issues = []
warnings = []
checked = 0
for record in data['records']:
    if record.get('status') != 'active':
        continue
    slug = record['slug']
    value = record.get('price_source_last_checked_on') or record.get('verified_on')
    qualified = isinstance(record.get('savings_amount'), (int, float)) and record['savings_amount'] >= 20
    file = ROOT / record['page_path'].lstrip('/') / 'index.html'
    html = file.read_text(encoding='utf-8') if file.exists() else ''
    banner = 'vs-final-savings-section' in html
    if not (qualified or banner):
        continue
    checked += 1
    if not qualified:
        issues.append(f'{slug}: large banner without a qualifying database comparison')
        continue
    if not value:
        issues.append(f'{slug}: verified price-comparison date missing')
        continue
    try:
        seen = date.fromisoformat(value)
    except (TypeError, ValueError):
        issues.append(f'{slug}: invalid price-comparison date {value!r}')
        continue
    age = (today - seen).days
    if age < 0:
        issues.append(f'{slug}: future-dated price check {value}')
    elif age > MAX_BANNER_AGE_DAYS:
        issues.append(f'{slug}: price comparison {age} days old; reverify before retaining banner')
    elif age > WARN_BANNER_AGE_DAYS:
        warnings.append(f'{slug}: comparison last checked {age} days ago')
    if not banner:
        issues.append(f'{slug}: qualifying show is missing the large banner')

print(f'Large savings comparison dates checked: {checked}')
for item in warnings:
    print('RECHECK SOON: ' + item)
if issues:
    for item in issues:
        print('FAIL: ' + item)
    sys.exit(1)
print(f'PASS: {checked} qualifying large-banner shows have source-check dates within {MAX_BANNER_AGE_DAYS} days')

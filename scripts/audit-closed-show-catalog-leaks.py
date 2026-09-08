#!/usr/bin/env python3
from pathlib import Path
import re,sys

closed = {'mad-apple','david-goldrake'}
issues=[]
catalogs=[Path('shows/index.html'), *sorted(Path('shows').glob('*/index.html'))]
for p in catalogs:
    if not p.exists(): continue
    text=p.read_text(errors='ignore')
    for slug in closed:
        if re.search(r"\{[^\n]*slug:'"+re.escape(slug)+r"'[^\n]*\}",text):
            issues.append(f'{p}: closed show {slug} remains in active catalog data')
print(f'Active catalog hubs checked: {len(catalogs)}')
if issues:
    print('\n'.join(issues)); sys.exit(1)
print('No closed shows remain in active catalog data.')

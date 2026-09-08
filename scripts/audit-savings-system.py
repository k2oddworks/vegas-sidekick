#!/usr/bin/env python3
from pathlib import Path
import json,re,sys
ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'data/show-database.json').read_text())
minimum=int(data.get('deal_threshold_dollars',5));issues=[];deals=[]
for r in data.get('records',[]):
    if r.get('status')!='active':continue
    try:a=float(r.get('our_price'));b=float(r.get('regular_price'))
    except: a=b=0
    amount=round(b-a) if b and b-a>=minimum else None
    pct=round((b-a)/b*100) if amount else None
    if r.get('savings_amount')!=amount:issues.append(f"{r['slug']}: savings_amount {r.get('savings_amount')} != {amount}")
    if r.get('savings_percent')!=pct:issues.append(f"{r['slug']}: savings_percent {r.get('savings_percent')} != {pct}")
    if bool(r.get('is_deal'))!=bool(amount):issues.append(f"{r['slug']}: is_deal mismatch")
    p=ROOT/r.get('page_path','').strip('/')/'index.html'
    if amount:
        deals.append(r)
        if not p.exists():issues.append(f"{r['slug']}: show page missing")
        else:
            t=p.read_text(errors='ignore')
            if 'vs-save-badge' not in t:issues.append(f"{r['slug']}: deal badge missing from show page")
            if f'Save ${amount}' not in t:issues.append(f"{r['slug']}: current savings copy missing")
for req in ['assets/show-savings.css','assets/catalog-savings.css','assets/catalog-savings.js','shows/deals/index.html']:
    if not (ROOT/req).exists():issues.append(f'{req}: missing')
root=(ROOT/'shows/index.html').read_text(errors='ignore')
if '/shows/deals/' not in root:issues.append('shows/index.html: no static link to Deals page')
print(f"Savings audit: {len(deals)} active deals; threshold ${minimum}.")
if issues:
    print('\n'.join(issues));sys.exit(1)
print('Savings calculations and customer-facing deal surfaces are consistent.')

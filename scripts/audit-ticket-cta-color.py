#!/usr/bin/env python3
from pathlib import Path
import re,sys
skip={'preview','logo-sample','archive','docs','node_modules','.git'}
anchor_re=re.compile(r'<a\b([^>]*)>(.*?)</a>',re.I|re.S)
class_re=re.compile(r'\bclass="([^"]*)"',re.I)
strip=lambda s:re.sub(r'<[^>]+>',' ',s)
cta_class=re.compile(r'(?:^|[-_ ])(?:cta|btn|button|hero|final|mob|mobile|sticky|buy|book|ticket|sb|zone)(?:$|[-_ ])',re.I)
ticket_text=re.compile(r'\b(?:get|see|check|view|find|book|buy|select|shop)?\s*tickets?\b|\btickets?\s*(?:now|→|$)',re.I)
issues=[]; checked=0; tagged=0
for p in Path('.').rglob('*.html'):
    if any(part in skip for part in p.parts): continue
    s=p.read_text(errors='ignore')
    page_has=False
    for m in anchor_re.finditer(s):
        attrs,inner=m.groups(); cm=class_re.search(attrs)
        if not cm: continue
        classes=cm.group(1).split(); text=' '.join(strip(inner).split())
        if not (cta_class.search(' '.join(classes)) and ticket_text.search(text)): continue
        checked+=1; page_has=True
        if 'vs-ticket-primary' not in classes:
            issues.append(f'{p}: ticket CTA missing vs-ticket-primary: {text[:90]}')
        else: tagged+=1
    if page_has and '/assets/ticket-cta.css' not in s:
        issues.append(f'{p}: ticket CTA page missing /assets/ticket-cta.css')
css=Path('assets/ticket-cta.css')
if not css.exists(): issues.append('assets/ticket-cta.css missing')
else:
    c=css.read_text().lower()
    if '#ffb000' not in c: issues.append('Warm Amber #FFB000 missing from ticket CTA stylesheet')
    if 'color:#171225' not in c.replace(' ',''): issues.append('Expected dark ticket CTA text color missing')
print(f'Primary ticket CTA anchors checked: {checked}; correctly tagged: {tagged}')
if issues:
    print('\n'.join(issues)); sys.exit(1)
print('All detected primary ticket CTAs use the Warm Amber shared treatment.')

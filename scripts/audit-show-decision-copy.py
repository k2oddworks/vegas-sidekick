#!/usr/bin/env python3
from pathlib import Path
import re,sys

ROOT=Path(__file__).resolve().parents[1]
CLOSED={'shows/cirque/mad-apple/index.html','shows/magic/david-goldrake/index.html'}
LEGACY=('Book it if…','Book it if...','Know this first','Best practical angle')
GENERIC_THINK={
'You need an all-ages option or a quieter, low-key night.',
'You want a comedy club, concert or personality-led headliner to be the whole point.',
'You want a big visual production, concert or Cirque-style experience instead.',
'Your group is specifically looking for an adults-only nightlife show.',
'You want a concert, comedy club or large-scale production instead.',
'You want magic, stand-up or a spectacle-first production instead.',
'You want an intimate, personality-led show where one performer is the main attraction.',
'You are really shopping for magic, Cirque or a concert.',
'You are really looking for a concert or Cirque production.',
'You are really shopping for close-up magic or stand-up comedy.',
'You need an all-ages show.',
}
issues=[]; checked=0
for path in sorted(ROOT.glob('shows/*/*/index.html')):
    rel=path.relative_to(ROOT).as_posix()
    if rel in CLOSED: continue
    checked+=1
    text=path.read_text(encoding='utf-8',errors='ignore')
    for phrase in LEGACY:
        if phrase in text:
            issues.append(f'{rel}: legacy decision label remains: {phrase}')
    for m in re.finditer(r'<h3>(?:🤔 )?Think twice(?: if…)?</h3><p>(.*?)</p>',text,re.S|re.I):
        body=re.sub(r'<[^>]+>','',m.group(1)).strip()
        if body in GENERIC_THINK:
            issues.append(f'{rel}: generic Think twice filler should be omitted: {body}')
print(f'Checked {checked} active show pages for decision-copy regressions.')
if issues:
    print('\n'.join(issues)); sys.exit(1)
print('Decision-copy labels are current and generic Think twice filler is absent.')

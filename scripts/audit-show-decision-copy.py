#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
CLOSED={'shows/cirque/mad-apple/index.html','shows/magic/david-goldrake/index.html'}
LEGACY=('Book it if…','Book it if...','Know this first','Best practical angle')
issues=[]; checked=0
for path in sorted(ROOT.glob('shows/*/*/index.html')):
    rel=path.relative_to(ROOT).as_posix()
    if rel in CLOSED: continue
    checked+=1
    text=path.read_text(encoding='utf-8',errors='ignore')
    for phrase in LEGACY:
        if phrase in text:
            issues.append(f'{rel}: legacy decision label remains: {phrase}')
print(f'Checked {checked} active show pages for decision-copy regressions.')
if issues:
    print('\n'.join(issues)); sys.exit(1)
print('No legacy Book it if / Know this first / Best practical angle labels remain.')

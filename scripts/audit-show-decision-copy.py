#!/usr/bin/env python3
"""Audit live customer-facing Vegas Sidekick copy for retired decision framing.

September 2026 standard:
- Use Good fit for buyer fit.
- Use Good to know for useful caveats/context when needed.
- Use Booking tip for a concrete planning action.
- Do not use formal "Think twice" or "downside" framing.
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
RETIRED_LABELS = (
    'Book it if…',
    'Book it if...',
    'Know this first',
    'Best practical angle',
)

issues = []
checked = 0

for path in sorted(ROOT.rglob('*.html')):
    rel_path = path.relative_to(ROOT)
    rel = rel_path.as_posix()
    if '_archive' in rel_path.parts:
        continue
    # Preview experiments and admin tools are not deployed buyer-facing pages.
    if rel_path.parts and rel_path.parts[0] in {'admin', 'preview'}:
        continue

    checked += 1
    text = path.read_text(encoding='utf-8', errors='ignore')

    for phrase in RETIRED_LABELS:
        if phrase in text:
            issues.append(f'{rel}: retired decision label remains: {phrase}')

    if re.search(r'\bthink twice\b', text, re.I):
        issues.append(f"{rel}: retired 'Think twice' framing remains")

    if re.search(r'\bdownsides?\b', text, re.I):
        issues.append(f"{rel}: retired 'downside' framing remains")

print(f'Checked {checked} live customer-facing HTML pages for decision-copy regressions.')
if issues:
    print('\n'.join(issues))
    sys.exit(1)

print("Decision-copy framing is current: Good fit / Good to know / Booking tip; no retired negative labels found.")

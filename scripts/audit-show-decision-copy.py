#!/usr/bin/env python3
"""Audit live customer-facing Vegas Sidekick copy for retired decision framing.

September 2026 standard:
- Use Good fit for buyer fit.
- Use Good to know only for useful, show-specific facts/caveats/context.
- Use Booking tip for a concrete planning action.
- Do not use formal "Think twice" or "downside" framing.
- Do not relabel rejection/mismatch copy as "Good to know".
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

GOOD_TO_KNOW_REJECTION = re.compile(
    r'\byou need\b|'
    r'\byou actually want\b|'
    r'\byou are actually shopping\b|'
    r'\byou are really (?:shopping|looking)\b|'
    r'\byou prefer\b|'
    r'\byou would rather\b|'
    r'\byou specifically want\b|'
    r'\byou dislike\b|'
    r'\byou are choosing\b|'
    r'\byour group specifically wants\b|'
    r'\ba different show category\b|'
    r'\byou want (?:a|an|the)\b',
    re.I,
)
GOOD_TO_KNOW_CARD = re.compile(
    r'<div class="[^"]*(?:decision-card|fit-card)[^"]*"[^>]*>'
    r'\s*<h3>Good to know</h3>(.*?)</div>',
    re.I | re.S,
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

    # Catch the regression where old "don't buy this if..." content gets a
    # friendlier heading without becoming useful buyer context.
    for match in GOOD_TO_KNOW_CARD.finditer(text):
        body = re.sub(r'<[^>]+>', ' ', match.group(1))
        body = re.sub(r'\s+', ' ', body).strip()
        if GOOD_TO_KNOW_REJECTION.search(body):
            issues.append(
                f'{rel}: Good to know contains rejection/mismatch copy instead of useful context: {body}'
            )

print(f'Checked {checked} live customer-facing HTML pages for decision-copy regressions.')
if issues:
    print('\n'.join(issues))
    sys.exit(1)

print('Decision-copy framing and Good to know semantics are clean.')

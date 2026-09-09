#!/usr/bin/env python3
"""Audit live customer-facing Vegas Sidekick copy for retired decision framing.

September 2026 standard:
- Use Good fit for buyer fit.
- Use Good to know only for useful, show-specific facts/caveats/context.
- Use Booking tip only for a concrete, show-specific seat, timing, or planning action.
- Omit Booking tip when there is nothing genuinely useful to say.
- Do not use formal "Think twice" or "downside" framing.
- Do not relabel rejection/mismatch copy as "Good to know".
"""
from collections import Counter
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
BOOKING_TIP_CARD = re.compile(
    r'<div class="[^"]*decision-card[^"]*"[^>]*>'
    r'\s*<h3>Booking tip</h3>(.*?)</div>',
    re.I | re.S,
)
GENERIC_BOOKING_TIPS = {
    'A balanced view that keeps you close to the room energy without putting you directly inside every audience-interaction moment.',
    'The easiest all-around view for full-stage compositions, aerial work and the production’s largest visual moments.',
    'Close enough to read expressions and crowd work without making the closest possible row the whole point.',
    'A straightforward family default: clear view, easy sightlines and enough distance to see the full stage.',
    'The safest balance for reading hands, props and full-stage illusions without being too far from the performer.',
    'A balanced view of the performers and full stage without giving up too much proximity.',
    'Start with Center-middle. The safest choice for reading the production as a whole instead of chasing the closest possible row.',
}
CLOSED_SHOWS = {
    'shows/cirque/mad-apple/index.html',
    'shows/magic/david-goldrake/index.html',
}

issues = []
checked = 0
booking_tips = []

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

    # Booking tips are optional. When they exist on an active show, they must
    # be show-specific rather than recycled category filler.
    if rel.startswith('shows/') and rel not in CLOSED_SHOWS:
        for match in BOOKING_TIP_CARD.finditer(text):
            body = re.sub(r'<[^>]+>', ' ', match.group(1))
            body = re.sub(r'\s+', ' ', body).strip()
            booking_tips.append((rel, body))
            if body in GENERIC_BOOKING_TIPS:
                issues.append(f'{rel}: generic Booking tip filler remains: {body}')

# Exact reuse across active shows is a strong signal that a supposedly
# show-specific booking action has turned back into template filler.
counts = Counter(body for _, body in booking_tips)
for body, count in counts.items():
    if count > 1:
        pages = ', '.join(rel for rel, tip in booking_tips if tip == body)
        issues.append(f'Booking tip reused across {count} active shows: {body} :: {pages}')

print(f'Checked {checked} live customer-facing HTML pages for decision-copy regressions.')
print(f'Active show Booking tips found: {len(booking_tips)}; unique: {len(counts)}.')
if issues:
    print('\n'.join(issues))
    sys.exit(1)

print('Decision-copy framing, Good to know semantics, and Booking tip semantics are clean.')

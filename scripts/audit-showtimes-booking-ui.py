#!/usr/bin/env python3
from pathlib import Path
import json, re, sys

ROOT = Path(__file__).resolve().parents[1]
CATS = ['adult', 'cirque', 'comedy', 'family', 'magic', 'music', 'spectaculars']


def event(text):
    for raw in re.findall(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', text, re.I | re.S):
        try:
            obj = json.loads(raw)
        except Exception:
            continue
        if isinstance(obj, dict) and obj.get('@type') in ('Event', 'EventSeries'):
            return obj
    return None


def main():
    records = json.loads((ROOT / 'data/show-database.json').read_text(encoding='utf-8'))['records']
    by_path = {r['page_path']: r for r in records}
    active = 0
    unavailable = 0
    regular = 0
    variable = 0
    errors = []

    for cat in CATS:
        for p in sorted((ROOT / 'shows' / cat).glob('*/index.html')):
            text = p.read_text(encoding='utf-8', errors='replace')
            ev = event(text)
            if not ev or ev.get('eventStatus') != 'https://schema.org/EventScheduled':
                continue
            rel = str(p.relative_to(ROOT))
            url = '/' + p.parent.relative_to(ROOT).as_posix() + '/'
            row = by_path.get(url)
            if row and row.get('status') != 'active':
                if row.get('status') == 'needs_review':
                    unavailable += 1
                    if ('vs-booking-unavailable-section' not in text
                            or 'Tickets currently unavailable' not in text
                            or 'https://schema.org/OutOfStock' not in text):
                        errors.append(f'{rel}: paused ticketing page missing unavailable state')
                    if 'data-ticket-url=' in text or 'class="vs-booking-shell"' in text:
                        errors.append(f'{rel}: paused ticketing page still exposes booking picker')
                continue
            active += 1

            if 'vs-booking-section' not in text:
                errors.append(f'{rel}: active show is missing the shared booking module')
                continue
            if '/assets/showtimes-booking.css?v=3' not in text:
                errors.append(f'{rel}: booking CSS is not on v3')
            if '/assets/showtimes-booking.js?v=2' not in text:
                errors.append(f'{rel}: booking JS is not on v2')
            # Existing indexed show URLs can retain a historical category path
            # after editorial recategorization. The database owns the theme.
            expected_theme = row.get('category', cat) if row else cat
            if expected_theme not in CATS:
                errors.append(f'{rel}: unknown booking category {expected_theme}')
            elif f'data-booking-theme="{expected_theme}"' not in text:
                errors.append(f'{rel}: booking theme is missing or does not match database category {expected_theme}')
            if 'class="vs-booking-pill"' not in text:
                errors.append(f'{rel}: booking pill is missing from static HTML')
            if 'Planning ahead?' in text:
                errors.append(f'{rel}: retired Planning Ahead filler is still present')
            if 'awakening-booking-experiment' in text:
                errors.append(f'{rel}: obsolete Awakening-only booking skin is still present')

            if 'vs-variable-panel' in text:
                variable += 1
                if 'See available dates &amp; times →' not in text:
                    errors.append(f'{rel}: variable schedule is missing the available-dates CTA')
            else:
                regular += 1
                if 'Choose a time' not in text:
                    errors.append(f'{rel}: regular schedule is missing the compact Choose a time label')
                if '>Get Tickets →</a>' not in text:
                    errors.append(f'{rel}: regular schedule is missing the compact Get Tickets CTA')
                if 'See all dates &amp; times →' not in text:
                    errors.append(f'{rel}: regular schedule is missing the compact all-dates link')

    print(f'Active show pages audited: {active}')
    print(f'Ticketing-paused information pages audited: {unavailable}')
    print(f'Regular booking modules: {regular}')
    print(f'Variable booking modules: {variable}')
    if errors:
        print('\nFAIL')
        for e in errors:
            print(f'- {e}')
        sys.exit(1)
    print('PASS: compact booking modules for active shows; paused ticketing pages safely excluded')


if __name__ == '__main__':
    main()

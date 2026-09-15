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
    active = 0
    regular = 0
    variable = 0
    errors = []

    for cat in CATS:
        for p in sorted((ROOT / 'shows' / cat).glob('*/index.html')):
            text = p.read_text(encoding='utf-8', errors='replace')
            ev = event(text)
            if not ev or ev.get('eventStatus') != 'https://schema.org/EventScheduled':
                continue
            active += 1
            rel = str(p.relative_to(ROOT))

            if 'vs-booking-section' not in text:
                errors.append(f'{rel}: active show is missing the shared booking module')
                continue
            if '/assets/showtimes-booking.css?v=2' not in text:
                errors.append(f'{rel}: booking CSS is not on v2')
            if '/assets/showtimes-booking.js?v=2' not in text:
                errors.append(f'{rel}: booking JS is not on v2')
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
    print(f'Regular booking modules: {regular}')
    print(f'Variable booking modules: {variable}')
    if errors:
        print('\nFAIL')
        for e in errors:
            print(f'- {e}')
        sys.exit(1)
    print('PASS: compact showtimes booking v2 is present across all active show pages')


if __name__ == '__main__':
    main()

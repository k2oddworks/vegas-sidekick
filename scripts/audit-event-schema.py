#!/usr/bin/env python3
"""
Audits active show pages' Event/EventSeries JSON-LD for the fields Google
Search Console validates. Closed archive pages listed in CLOSED_ARCHIVE_EXCEPTIONS
are reported as intentional skips, not schema failures.

Usage: python3 scripts/audit-event-schema.py
Run from the repo root. Exits non-zero if any active page has issues.
"""
import re, json, glob, sys

CLOSED_ARCHIVE_EXCEPTIONS = {
    'shows/cirque/mad-apple/index.html',
}

def extract_json_ld_blocks(content):
    blocks = []
    for m in re.finditer(r'<script type="application/ld\+json">', content):
        start = m.end()
        end = content.find('</script>', start)
        blocks.append(content[start:end].strip())
    return blocks

REQUIRED_TOP_EVENT = ['name','description','image','url','startDate','endDate',
                       'eventStatus','organizer','location','offers','performer']
REQUIRED_TOP_SERIES = ['name','description','image','url','eventStatus',
                        'organizer','location','offers','performer']
REQUIRED_OFFERS = ['price','priceCurrency','availability','url','validFrom']
REQUIRED_ORGANIZER = ['name','url']

def audit():
    files = sorted(glob.glob('shows/*/*/index.html'))
    total_issues = 0
    skipped = 0

    for f in files:
        if f in CLOSED_ARCHIVE_EXCEPTIONS:
            print(f"{f}: SKIP intentional closed archive")
            skipped += 1
            continue

        content = open(f, encoding='utf-8').read()
        blocks = extract_json_ld_blocks(content)

        for b in blocks:
            try:
                json.loads(b)
            except Exception as e:
                print(f"{f}: BROKEN JSON-LD block: {e}")
                total_issues += 1

        ev, ev_type = None, None
        for b in blocks:
            try:
                data = json.loads(b)
            except Exception:
                continue
            if data.get('@type') in ('Event', 'EventSeries'):
                ev, ev_type = data, data.get('@type')
                break

        if ev is None:
            print(f"{f}: NO Event/EventSeries JSON-LD found")
            total_issues += 1
            continue

        required_top = REQUIRED_TOP_EVENT if ev_type == 'Event' else REQUIRED_TOP_SERIES
        for field in required_top:
            if field not in ev or ev[field] in (None, '', []):
                print(f'{f}: missing top-level "{field}"')
                total_issues += 1

        org = ev.get('organizer', {})
        if isinstance(org, dict):
            for field in REQUIRED_ORGANIZER:
                if field not in org or not org[field]:
                    print(f'{f}: missing organizer.{field}')
                    total_issues += 1

        offers = ev.get('offers', {})
        if isinstance(offers, dict):
            for field in REQUIRED_OFFERS:
                if field not in offers or offers[field] in (None, ''):
                    print(f'{f}: missing offers.{field}')
                    total_issues += 1
            price = offers.get('price')
            if isinstance(price, str) and not re.fullmatch(r'\d+(\.\d+)?', price):
                print(f'{f}: INVALID price format: {price!r} (should be a bare number, no "$")')
                total_issues += 1

    active_checked = len(files) - skipped
    print(f"\nChecked {active_checked} active show pages; skipped {skipped} closed archive(s).")
    if total_issues == 0:
        print("All active show schema clean.")
    else:
        print(f"{total_issues} issue(s) found.")
    return total_issues

if __name__ == '__main__':
    sys.exit(1 if audit() else 0)

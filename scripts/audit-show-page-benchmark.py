#!/usr/bin/env python3
"""Audit active show pages against the current Vegas Sidekick benchmark."""
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "show-database.json"

REQUIRED_SNIPPETS = {
    "canonical CSS": "/assets/show-canonical.css",
    "canonical JS": "/assets/show-canonical.js",
    "canonical layout flag": 'data-canonical-layout="2"',
    "quick facts": '<section class="facts"',
    "ticker": 'class="ticker"',
    "ticker track": 'class="ticker-track"',
    "sticky subnav": 'class="subnav"',
    "descriptive overview": 'id="about"',
    "Quick Take": 'id="quick"',
    "showtimes module": 'id="showtimes"',
    "photos": 'id="photos"',
    "FAQ": 'id="faq"',
    "author card": 'class="author-card"',
    "final CTA": "final-section",
    "mobile ticket bar": 'class="mobile-bar"',
    "shared showtimes CSS": "/assets/showtimes-booking.css",
    "shared showtimes JS": "/assets/showtimes-booking.js",
}

RETIRED_PATTERNS = {
    "separate Good Fit section": r'id="fit"',
    'visible "Who it fits best" section': r'>\s*Who it fits best\s*<',
    'visible "Good fit / Good to know" heading': r'>\s*Good fit\s*/\s*Good to know\s*<',
    'retired "Think twice" framing': r'>\s*Think twice\s*<',
    'retired "Honest downside" framing': r'>\s*Honest downside\s*<',
    'retired "Typical start" label': r'>\s*Typical start\s*<',
    "generic placeholder Kris take": r'makes the most sense when the premise itself is what you want',
}

FRESHNESS = re.compile(r"Show info confirmed [A-Z][a-z]+ 20\d{2}")
EVENT_TYPE = re.compile(r'"@type"\s*:\s*"Event(?:Series)?"')

def load_active_records():
    data = json.loads(DB.read_text(encoding="utf-8"))
    return [
        r for r in data.get("records", [])
        if r.get("status") == "active" and r.get("page_path")
    ]

def page_file(record):
    return ROOT / record["page_path"].strip("/") / "index.html"

def position(text, ident):
    return text.find(f'id="{ident}"')

def main():
    issues = []
    active = load_active_records()

    for record in active:
        path = page_file(record)
        rel = path.relative_to(ROOT).as_posix()
        if not path.exists():
            issues.append(f"{rel}: page missing")
            continue

        text = path.read_text(encoding="utf-8", errors="ignore")

        for label, snippet in REQUIRED_SNIPPETS.items():
            if snippet not in text:
                issues.append(f"{rel}: missing {label}")

        for label, pattern in RETIRED_PATTERNS.items():
            if re.search(pattern, text, re.I):
                issues.append(f"{rel}: {label}")

        fresh = FRESHNESS.findall(text)
        if len(fresh) != 1:
            issues.append(f"{rel}: visible freshness count is {len(fresh)}; expected 1")

        about = position(text, "about")
        quick = position(text, "quick")
        showtimes = position(text, "showtimes")
        photos = position(text, "photos")

        if min(about, quick, showtimes, photos) >= 0:
            if not (about < quick < showtimes < photos):
                issues.append(
                    f"{rel}: buyer journey order must be about → quick → showtimes → photos"
                )

        if not EVENT_TYPE.search(text):
            issues.append(f"{rel}: missing Event/EventSeries JSON-LD")

        if 'class="take"' in text and "Kris" not in text[text.find('class="take"'):text.find('class="take"')+900]:
            issues.append(f"{rel}: Quick Take recommendation block is malformed")

    print(f"Checked {len(active)} active show pages against the current benchmark.")
    if issues:
        print("Show-page benchmark audit FAILED:")
        for issue in issues:
            print(" -", issue)
        return 1

    print("All active show pages pass the benchmark structure/regression audit.")
    return 0

if __name__ == "__main__":
    sys.exit(main())

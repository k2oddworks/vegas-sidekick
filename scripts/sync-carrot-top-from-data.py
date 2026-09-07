#!/usr/bin/env python3
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/shows/carrot-top.json"
PAGE = ROOT / "shows/comedy/carrot-top/index.html"


def replace_once(text, pattern, repl, label, flags=0):
    new, count = re.subn(pattern, repl, text, count=1, flags=flags)
    if count != 1:
        raise SystemExit(f"Expected exactly one {label}; found {count}")
    return new


def main():
    d = json.loads(DATA.read_text(encoding="utf-8"))
    text = PAGE.read_text(encoding="utf-8")
    original = text

    price = d["pricing"]["from_price"]
    runtime = d["runtime"]["minutes"]
    affiliate = d["ticketing"]["affiliate_url"]
    hotel = d["venue"]["hotel"]
    showroom = d["venue"]["showroom"]
    age = d["age_policy"]["rule"]
    trailer_id = d["media"]["official_trailer"]["video_id"]
    schedule = d["schedule"]

    title = f"Carrot Top at Luxor Las Vegas Tickets from ${price} | What to Know"
    meta = f"Carrot Top at Luxor Las Vegas is a live comedy show. Tickets from ${price} at {showroom} at Luxor. Check showtimes, seating and whether the comedy style fits your group."
    og_title = f"Carrot Top Las Vegas — Tickets From ${price}"
    og_desc = f"Tickets from ${price} for {runtime} minutes of prop comedy at Luxor. See the seat guide, typical schedule and Spike's take before you book."
    text = replace_once(text, r"<title>.*?</title>", f"<title>{title}</title>", "title", re.S)
    text = replace_once(text, r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{meta}">', "meta description")
    text = replace_once(text, r'<meta property="og:title" content="[^"]*"\s*/?>', f'<meta property="og:title" content="{og_title}" />', "og title")
    text = replace_once(text, r'<meta property="og:description" content="[^"]*"\s*/?>', f'<meta property="og:description" content="{og_desc}" />', "og description")

    text = re.sub(r'https://spotlight\.vegas/shows/comedy/carrot-top/ref/vegassidekick', affiliate, text)

    text = replace_once(text, r'(class="check">)Starting at \$\d+\.', rf'\g<1>Starting at ${price}.', "hero price note")
    text = replace_once(text, r'(<div class="price"><small>From</small>\s*)\$\d+', rf'\g<1>${price}', "hero price")

    text = text.replace("Luxor · Atrium Showroom, 3900 S Las Vegas Blvd", f"{hotel.replace(' Hotel','')} · {showroom}, 3900 S Las Vegas Blvd")
    text = re.sub(r'About \d+ minutes, no intermission', f'About {runtime} minutes, no intermission', text, count=1)

    perf = {x["day"]: x["time"] for x in schedule["performances"]}
    abbreviations = {"Monday":"Mon","Tuesday":"Tue","Wednesday":"Wed","Thursday":"Thu","Friday":"Fri","Saturday":"Sat","Sunday":"Sun"}
    def fmt_time(t):
        h, m = map(int, t.split(':'))
        suffix = 'AM' if h < 12 else 'PM'
        hh = h if 1 <= h <= 12 else h - 12 if h > 12 else 12
        return f"{hh}:{m:02d} {suffix}" if m else f"{hh} {suffix}"
    for day, abbr in abbreviations.items():
        value = fmt_time(perf[day]) if day in perf else "Dark"
        pattern = rf'(<div class="day[^>]*"><strong>{abbr}</strong><span>).*?(</span></div>)'
        text = replace_once(text, pattern, rf'\g<1>{value}\g<2>', f"{day} schedule")

    text, age_count = re.subn(r'The minimum age is 16\.[^<]*', age, text, count=1)
    if age_count != 1:
        raise SystemExit(f"Expected exactly one explicit age-policy sentence; found {age_count}")

    text = re.sub(r'i\.ytimg\.com/vi/[A-Za-z0-9_-]+/', f'i.ytimg.com/vi/{trailer_id}/', text)
    text = re.sub(r'youtube(?:-nocookie)?\.com/embed/[A-Za-z0-9_-]+', f'youtube-nocookie.com/embed/{trailer_id}', text)

    text = re.sub(r'("price"\s*:\s*)"?\d+(?:\.\d+)?"?', rf'\g<1>"{price}"', text, count=1)
    text = re.sub(r'("url"\s*:\s*")https://spotlight\.vegas/shows/comedy/carrot-top/ref/vegassidekick(")', rf'\g<1>{affiliate}\g<2>', text, count=1)

    if text == original:
        print("Carrot Top page already matches structured data; no page changes needed.")
    else:
        PAGE.write_text(text, encoding="utf-8")
        print("Synced Carrot Top deterministic facts from data/shows/carrot-top.json")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Refresh Vegas Sidekick show-page titles and meta descriptions for stronger SERP differentiation.

Uses only facts already present on each page. Closed/archive pages are skipped. The goal is
clear ticket intent without repeating the exact same title/description formula across the catalog.
"""
from pathlib import Path
import hashlib
import html
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SHOWS = ROOT / "shows"
CLOSED = {
    "shows/cirque/mad-apple/index.html",
    "shows/magic/david-goldrake/index.html",
}

TITLE_VARIANTS = {
    "magic": [
        "{name}{market} Tickets{price} | Seat Guide",
        "{name}{market} Tickets{price} | Showtimes",
        "{name}{market} Show | Tickets{price} & Seats",
        "{name} Vegas Tickets{price} | Magic Guide",
    ],
    "comedy": [
        "{name}{market} Tickets{price} | Showtimes",
        "{name} Vegas Tickets{price} | Comedy Guide",
        "{name}{market} Show | Tickets{price} & Seats",
        "{name}{market} Tickets{price} | What to Know",
    ],
    "cirque": [
        "{name} Vegas Tickets{price} | Seat Guide",
        "{name}{market} Tickets{price} | Showtimes",
        "{name} Vegas Show | Tickets{price} & Seats",
        "{name}{market} Tickets{price} | Cirque Guide",
    ],
    "adult": [
        "{name}{market} Tickets{price} | Show Guide",
        "{name} Vegas Tickets{price} | Seats & Info",
        "{name}{market} Show | Tickets{price} & Guide",
        "{name}{market} Tickets{price} | What to Know",
    ],
    "family": [
        "{name}{market} Tickets{price} | Family Guide",
        "{name} Vegas Tickets{price} | Showtimes",
        "{name}{market} Show | Tickets{price} & Seats",
        "{name}{market} Tickets{price} | Family Info",
    ],
    "music": [
        "{name}{market} Tickets{price} | Showtimes",
        "{name} Vegas Tickets{price} | Show Guide",
        "{name}{market} Show | Tickets{price} & Seats",
        "{name}{market} Tickets{price} | Seat Guide",
    ],
    "spectaculars": [
        "{name}{market} Tickets{price} | Showtimes",
        "{name} Vegas Tickets{price} | Show Guide",
        "{name}{market} Show | Tickets{price} & Seats",
        "{name}{market} Tickets{price} | Seat Guide",
    ],
}

CATEGORY_FALLBACK = {
    "magic": "live magic show",
    "comedy": "live comedy show",
    "cirque": "Cirque-style production",
    "adult": "adult Las Vegas show",
    "family": "family-friendly Las Vegas show",
    "music": "live music and variety show",
    "spectaculars": "large-scale Las Vegas production",
}

DESCRIPTORS = [
    ("mentalism", "mentalism show"),
    ("mind-reading", "mind-reading show"),
    ("mind reading", "mind-reading show"),
    ("hypnosis", "hypnosis show"),
    ("stand-up", "stand-up comedy show"),
    ("stand up", "stand-up comedy show"),
    ("burlesque", "burlesque show"),
    ("male revue", "male revue"),
    ("topless", "adult revue"),
    ("tribute", "tribute show"),
    ("joust", "live jousting dinner show"),
    ("robot", "live robot-combat show"),
    ("dinner", "dinner show"),
    ("close-up magic", "close-up magic show"),
    ("illusion", "illusion show"),
    ("magic", "magic show"),
    ("percussion", "visual music and percussion show"),
    ("dance", "dance production"),
    ("aquatic", "aquatic stage production"),
    ("water", "water-based stage spectacular"),
    ("acrobat", "acrobatic production"),
    ("comedy", "comedy show"),
    ("variety", "variety show"),
]


def clean(value: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", value or ""))).strip()


def json_blocks(text: str):
    out = []
    for raw in re.findall(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', text, re.I | re.S):
        try:
            out.append(json.loads(raw.strip()))
        except Exception:
            pass
    return out


def event_from(text: str):
    for obj in json_blocks(text):
        if isinstance(obj, dict) and obj.get("@type") in ("Event", "EventSeries"):
            return obj
        if isinstance(obj, dict) and isinstance(obj.get("@graph"), list):
            for item in obj["@graph"]:
                if isinstance(item, dict) and item.get("@type") in ("Event", "EventSeries"):
                    return item
    return {}


def page_name(text: str, event: dict, slug: str) -> str:
    if event.get("name"):
        return clean(str(event["name"]))
    m = re.search(r'<h1[^>]*>(.*?)</h1>', text, re.I | re.S)
    if m:
        return clean(m.group(1))
    return slug.replace("-", " ").title()


def event_price(event: dict):
    offers = event.get("offers")
    if isinstance(offers, list):
        offers = offers[0] if offers else None
    if isinstance(offers, dict) and offers.get("price") not in (None, ""):
        p = str(offers["price"]).replace("$", "").strip()
        return p[:-2] if p.endswith(".0") else p
    return ""


def event_venue(event: dict):
    loc = event.get("location")
    if isinstance(loc, dict) and loc.get("name"):
        return clean(str(loc["name"]))
    return ""


def current_description(text: str) -> str:
    for pat in (
        r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']\s*/?>',
        r'<meta\s+content=["\'](.*?)["\']\s+name=["\']description["\']\s*/?>',
    ):
        m = re.search(pat, text, re.I | re.S)
        if m:
            return clean(m.group(1))
    return ""


def descriptor(desc: str, category: str) -> str:
    low = desc.lower()
    for needle, label in DESCRIPTORS:
        if needle in low:
            return label
    return CATEGORY_FALLBACK.get(category, "Las Vegas show")


def title_for(name: str, category: str, price: str, rel: str) -> str:
    variants = TITLE_VARIANTS.get(category, TITLE_VARIANTS["music"])
    index = int(hashlib.sha1(rel.encode()).hexdigest()[:8], 16) % len(variants)
    price_token = f" from ${price}" if price else ""
    market = "" if "las vegas" in name.lower() else " Las Vegas"
    title = variants[index].format(name=name, market=market, price=price_token)
    if len(title) > 68:
        title = f"{name}{market} Tickets{price_token}"
    if len(title) > 68:
        title = f"{name} Tickets{price_token}"
    if len(title) <= 50:
        title += " | Vegas Sidekick"
    return title


def description_for(name: str, category: str, price: str, venue: str, old: str, rel: str) -> str:
    kind = descriptor(old, category)
    intro = f"{name} is a {kind} in Las Vegas."
    if "las vegas" in name.lower():
        intro = f"{name} is a {kind}."
    fact_parts = []
    if price:
        fact_parts.append(f"Tickets from ${price}")
    if venue:
        fact_parts.append(f"at {venue}")
    fact = " ".join(fact_parts) + "." if fact_parts else ""
    endings = {
        "magic": ["Compare showtimes, seating and whether the magic style fits your night.", "See the schedule, seat guide and who this magic show suits best."],
        "comedy": ["Check showtimes, seating and whether the comedy style fits your group.", "See the schedule, seat guide and what kind of comedy night to expect."],
        "cirque": ["Compare showtimes, seating and the tradeoffs before choosing your Cirque night.", "See the schedule, seat guide and what to expect from the production."],
        "adult": ["Check showtimes, seating and the honest fit before choosing your night.", "See the schedule, seat guide and what kind of adult Vegas show this is."],
        "family": ["See showtimes, seating and whether it works for your family before booking.", "Check the schedule, seat guide and family fit before choosing your night."],
        "music": ["Check showtimes, seating and what kind of Vegas performance to expect.", "See the schedule, seat guide and whether this show fits your night."],
        "spectaculars": ["Compare showtimes, seating and what the production is actually like.", "See the schedule, seat guide and whether this big-stage show fits your night."],
    }
    pool = endings.get(category, endings["music"])
    ending = pool[int(hashlib.sha1((rel + "desc").encode()).hexdigest()[:8], 16) % len(pool)]
    return " ".join(x for x in (intro, fact, ending) if x)


def replace_meta(text: str, title: str, desc: str) -> str:
    text = re.sub(r'<title[^>]*>.*?</title>', f'<title>{html.escape(title)}</title>', text, count=1, flags=re.I | re.S)
    encoded = html.escape(desc, quote=True)
    pat1 = r'<meta\s+name=["\']description["\']\s+content=["\'].*?["\']\s*/?>'
    pat2 = r'<meta\s+content=["\'].*?["\']\s+name=["\']description["\']\s*/?>'
    if re.search(pat1, text, re.I | re.S):
        text = re.sub(pat1, f'<meta name="description" content="{encoded}">', text, count=1, flags=re.I | re.S)
    elif re.search(pat2, text, re.I | re.S):
        text = re.sub(pat2, f'<meta name="description" content="{encoded}">', text, count=1, flags=re.I | re.S)
    else:
        text = text.replace('</title>', f'</title><meta name="description" content="{encoded}">', 1)
    return text


def main():
    changed = 0
    for page in sorted(SHOWS.glob("*/*/index.html")):
        rel = page.relative_to(ROOT).as_posix()
        if rel in CLOSED:
            continue
        category = page.parts[-3]
        if category not in TITLE_VARIANTS:
            continue
        text = page.read_text(encoding="utf-8")
        event = event_from(text)
        name = page_name(text, event, page.parent.name)
        price = event_price(event)
        venue = event_venue(event)
        old_desc = current_description(text)
        new_title = title_for(name, category, price, rel)
        new_desc = description_for(name, category, price, venue, old_desc, rel)
        updated = replace_meta(text, new_title, new_desc)
        if updated != text:
            page.write_text(updated, encoding="utf-8")
            changed += 1
            print(f"{rel}\n  TITLE: {new_title}\n  DESC:  {new_desc}")
    print(f"Updated metadata on {changed} active show page(s).")


if __name__ == "__main__":
    main()

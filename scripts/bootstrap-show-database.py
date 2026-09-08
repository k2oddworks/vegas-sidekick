#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from datetime import date

ROOT = Path(__file__).resolve().parents[1]
SHOW_ROOT = ROOT / "shows"
OUT = ROOT / "data" / "show-database.json"

CLOSED = {"mad-apple", "david-goldrake"}

# Facts Kris explicitly confirmed during the structured-data pilot. These seed the
# master database once; after bootstrap, data/show-database.json becomes the record.
OVERRIDES = {
    "carrot-top": {
        "name": "Carrot Top",
        "status": "active",
        "our_price": 62,
        "regular_price": 68,
        "runtime_minutes": 75,
        "age_summary": "16+; guests 18 and under must be with an adult 21+",
        "venue": "Luxor Hotel",
        "showroom": "Atrium Showroom",
        "schedule_summary": "Monday–Saturday · 8 PM · dark Sunday",
        "ticket_url": "https://spotlight.vegas/shows/comedy/carrot-top/ref/vegassidekick",
        "official_trailer": "https://youtu.be/XRdqvnCZe-A?si=OmYJy6MwjF7IgZfB",
        "verified_on": "2026-09-07",
        "verification": "verified"
    },
    "vegas-the-show": {
        "name": "VEGAS! The Show",
        "status": "active",
        "our_price": 63,
        "regular_price": 101,
        "runtime_minutes": 75,
        "age_summary": "No age restriction",
        "venue": "Planet Hollywood Resort",
        "showroom": "Saxe Theater · Miracle Mile Shops",
        "schedule_summary": "Mon–Sat · 7 PM through Sep 20; 5:30 PM starting Sep 21 · dark Sunday",
        "ticket_url": "https://spotlight.vegas/shows/production/vegas-the-show/ref/vegassidekick/",
        "official_trailer": "",
        "verified_on": "2026-09-07",
        "verification": "verified"
    },
    "mystere": {
        "name": "Mystère by Cirque du Soleil",
        "status": "active",
        "our_price": 84,
        "regular_price": None,
        "runtime_minutes": 90,
        "age_summary": "No age restrictions",
        "venue": "TI Hotel",
        "showroom": "Mystère Theatre",
        "schedule_summary": "Mon, Tue, Fri–Sun · 6:30 PM & 9 PM · dark Wed/Thu",
        "ticket_url": "https://spotlight.vegas/shows/cirque-du-soleil/mystere/ref/vegassidekick",
        "official_trailer": "",
        "verified_on": "2026-09-07",
        "verification": "verified"
    },
    "wizard-of-oz": {
        "name": "The Wizard of Oz at Sphere",
        "status": "active",
        "our_price": 123,
        "regular_price": 123,
        "runtime_minutes": 75,
        "age_summary": "Intended for 6+; every guest requires a ticket",
        "venue": "Sphere",
        "showroom": "Sphere · 255 Sands Ave",
        "schedule_summary": "Days and times vary · check booking page",
        "ticket_url": "https://spotlight.vegas/shows/production/the-wizard-of-oz-at-sphere/ref/vegassidekick",
        "official_trailer": "",
        "verified_on": "2026-09-07",
        "verification": "verified"
    }
}


def strip_tags(value: str) -> str:
    value = re.sub(r"<script\b.*?</script>", " ", value, flags=re.I | re.S)
    value = re.sub(r"<style\b.*?</style>", " ", value, flags=re.I | re.S)
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def jsonld_blocks(html: str):
    for raw in re.findall(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', html, flags=re.I | re.S):
        try:
            yield json.loads(raw)
        except Exception:
            continue


def walk_json(obj):
    if isinstance(obj, dict):
        yield obj
        for value in obj.values():
            yield from walk_json(value)
    elif isinstance(obj, list):
        for value in obj:
            yield from walk_json(value)


def first_event(html: str):
    for block in jsonld_blocks(html):
        for obj in walk_json(block):
            t = obj.get("@type") if isinstance(obj, dict) else None
            types = t if isinstance(t, list) else [t]
            if "EventSeries" in types or "Event" in types:
                return obj
    return {}


def title_name(html: str, slug: str) -> str:
    m = re.search(r"<h1[^>]*>(.*?)</h1>", html, flags=re.I | re.S)
    if m:
        return strip_tags(m.group(1))
    m = re.search(r"<title>(.*?)</title>", html, flags=re.I | re.S)
    if m:
        return re.split(r"\s*[|—-]\s*Vegas Sidekick", strip_tags(m.group(1)), maxsplit=1)[0]
    return slug.replace("-", " ").title()


def num(value):
    try:
        return int(float(value))
    except Exception:
        return None


def venue_from_event(event: dict):
    location = event.get("location") or {}
    if isinstance(location, list):
        location = location[0] if location else {}
    if not isinstance(location, dict):
        return "", ""
    name = location.get("name") or ""
    address = location.get("address") or {}
    if isinstance(address, dict):
        street = address.get("streetAddress") or ""
    else:
        street = str(address or "")
    return str(name), str(street)


def offer_from_event(event: dict):
    offers = event.get("offers") or {}
    if isinstance(offers, list):
        offers = offers[0] if offers else {}
    if not isinstance(offers, dict):
        return None, ""
    return num(offers.get("price") or offers.get("lowPrice")), str(offers.get("url") or "")


def runtime_guess(html: str):
    text = strip_tags(html)
    for pat in [r"\b(\d{2,3})\s*(?:minutes?|mins?)\b", r"\b(\d{2,3})\s*min\b"]:
        m = re.search(pat, text, flags=re.I)
        if m:
            v = int(m.group(1))
            if 30 <= v <= 240:
                return v
    return None


def age_guess(html: str):
    text = strip_tags(html)
    candidates = [
        r"\bAges?\s+\d+\+",
        r"\b\d+\+",
        r"\bAll ages\b",
        r"\bNo age restrictions?\b",
        r"\bAdults? only\b",
    ]
    for pat in candidates:
        m = re.search(pat, text, flags=re.I)
        if m:
            return m.group(0)
    return ""


def schedule_guess(html: str):
    text = strip_tags(html)
    # Prefer compact operational phrases already used on cards/facts.
    patterns = [
        r"((?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)[^.!]{0,80}(?:AM|PM|Dark|dark))",
        r"((?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)[^.!]{0,100}(?:AM|PM|Dark|dark))",
        r"(Days and times vary[^.!]{0,80})",
        r"(Check current schedule)",
    ]
    for pat in patterns:
        m = re.search(pat, text, flags=re.I)
        if m:
            return re.sub(r"\s+", " ", m.group(1)).strip(" ·-")[:160]
    return ""


def freshness_guess(html: str):
    m = re.search(r"Last updated\s+([A-Za-z]+\s+20\d{2})", strip_tags(html), flags=re.I)
    return m.group(1) if m else ""


def build_record(path: Path):
    html = path.read_text(errors="ignore")
    slug = path.parent.name
    category = path.parent.parent.name
    event = first_event(html)
    price, ticket = offer_from_event(event)
    venue, street = venue_from_event(event)
    name = str(event.get("name") or title_name(html, slug))
    status = "closed" if slug in CLOSED or re.search(r"\b(closed|ended its Las Vegas run)\b", strip_tags(html), flags=re.I) else "active"
    record = {
        "slug": slug,
        "name": name,
        "category": category,
        "status": status,
        "our_price": price,
        "regular_price": None,
        "runtime_minutes": runtime_guess(html),
        "age_summary": age_guess(html),
        "venue": venue,
        "showroom": street,
        "schedule_summary": schedule_guess(html),
        "ticket_url": ticket,
        "official_trailer": "",
        "page_path": f"/shows/{category}/{slug}/",
        "verified_on": "",
        "freshness_label": freshness_guess(html),
        "verification": "needs_review",
        "notes": "",
    }
    if slug in OVERRIDES:
        record.update(OVERRIDES[slug])
    if status == "closed":
        record["status"] = "closed"
        record["our_price"] = None
        record["ticket_url"] = ""
    required = [record.get("our_price"), record.get("runtime_minutes"), record.get("venue"), record.get("schedule_summary")]
    if record["status"] == "active" and record.get("verification") != "verified" and all(v not in (None, "") for v in required):
        record["verification"] = "partial"
    return record


def main():
    records = []
    for path in sorted(SHOW_ROOT.glob("*/*/index.html")):
        records.append(build_record(path))
    records.sort(key=lambda r: (r["status"] != "active", r["name"].lower()))
    payload = {
        "schema_version": 1,
        "updated_on": date.today().isoformat(),
        "source": "Vegas Sidekick Show Database",
        "records": records,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    active = sum(1 for r in records if r["status"] == "active")
    closed = sum(1 for r in records if r["status"] == "closed")
    print(f"Wrote {len(records)} show records ({active} active, {closed} closed) to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

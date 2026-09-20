#!/usr/bin/env python3
"""Rebuild Vegas Sidekick show-detail pages into the canonical VEGAS! The Show layout.

The generator intentionally preserves factual source data from each existing page:
Event/EventSeries schema, offer URL/price, FAQ, real local images and verified YouTube IDs.
It removes unsupported fee/urgency language and keeps the result static/server-rendered.
"""
from __future__ import annotations

from pathlib import Path
import argparse
import copy
import hashlib
import html as htmllib
import json
import random
import re

ROOT = Path(__file__).resolve().parents[1]
SHOWS = ROOT / "shows"
IMAGES = ROOT / "images"
TODAY = "2026-09-07"
MONTH_LABEL = "September 2026"
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
CATEGORIES = ["adult", "cirque", "comedy", "family", "magic", "music", "spectaculars"]

# These already represent the approved benchmark family and should not be flattened by the generic pass.
KEEP_AS_BUILT = {
    "shows/music/vegas-the-show/index.html",
    "shows/cirque/ka/index.html",
    "shows/magic/mat-franco/index.html",
    "shows/cirque/mystere/index.html",
    "shows/comedy/carrot-top/index.html",
}

BANNED_COPY = (
    "no hidden fees", "zero hidden fees", "no fees", "no surprise fees", "no added fees",
    "secure booking", "instant delivery", "selling fast", "prices may increase",
    "booking early", "book early", "selling out", "sell out", "fills first",
    "price shown is the price you pay", "no surprises — ever", "ticket partner", "spotlight.vegas"
)

AUTHOR = {
    "@type": "Person",
    "@id": "https://vegassidekick.com/about/kris-kidd/#kris",
    "name": "Kris Kidd",
    "url": "https://vegassidekick.com/about/kris-kidd/",
    "image": "https://vegassidekick.com/images/kris-kidd.webp",
}

PROFILES = {
    "adult": {
        "label": "Adult Shows", "eyebrow": "Adult Vegas",
        "good": ["You want a grown-up Vegas night with more edge than the family catalog.", "The show’s premise is the reason you are considering it."],
        "think": [],
        "seat": [
            ("Sweet spot", "Center-middle", "A balanced view that keeps performer detail clear while still showing the full stage."),
            ("Closer", "Front / near stage", "More immediate performer detail from close to the stage."),
            ("Wider view", "Rear / side", "A wider way to watch the full staging when the overall picture matters more than close-up detail."),
        ],
        "guide": "/guides/",
    },
    "cirque": {
        "label": "Cirque & Acrobatic", "eyebrow": "Cirque spectacle",
        "good": ["You want physical spectacle, acrobatics and visual stagecraft.", "The production design matters as much as any single performer."],
        "think": [],
        "seat": [
            ("Sweet spot", "Center-middle", "The easiest all-around view for full-stage compositions, aerial work and the production’s largest visual moments."),
            ("Closer", "Lower / near stage", "More performer detail while still keeping much of the full-stage picture in view."),
            ("Wider view", "Rear / upper center", "Useful when the choreography and room-scale picture matter more than facial detail."),
        ],
        "guide": "/guides/best-cirque-shows/",
    },
    "comedy": {
        "label": "Comedy", "eyebrow": "Vegas comedy",
        "good": ["You want laughs and personality to drive the night.", "You would rather see a performer-led show than a giant visual production."],
        "think": [],
        "seat": [
            ("Sweet spot", "Center-middle", "Close enough to read expressions and crowd work without making the closest possible row the whole point."),
            ("Closer", "Front section", "Best when facial detail and the feeling of being in the comedian’s room matter most."),
            ("Wider view", "Rear center", "A practical value choice when the room is intimate and you mainly want a clean sightline."),
        ],
        "guide": "/guides/",
    },
    "family": {
        "label": "Family Shows", "eyebrow": "Family Vegas",
        "good": ["You want something a mixed-age group can enjoy together.", "You need a show that is easy to fit into a family itinerary."],
        "think": [],
        "seat": [
            ("Sweet spot", "Center-middle", "A straightforward family default: clear view, easy sightlines and enough distance to see the full stage."),
            ("Closer", "Front section", "Better for performer detail and kids who engage more when the action feels physically close."),
            ("Wider view", "Rear center", "A reasonable value choice when the room is compact and the full-stage picture matters most."),
        ],
        "guide": "/guides/best-shows-for-families/",
    },
    "magic": {
        "label": "Magic", "eyebrow": "Vegas magic",
        "good": ["You want illusions, mind-reading or sleight-of-hand to be the main event.", "You want the magician’s personality and methods to carry the room."],
        "think": [],
        "seat": [
            ("Sweet spot", "Center-middle", "The safest balance for reading hands, props and full-stage illusions without being too far from the performer."),
            ("Closer", "Front section", "Best for facial detail and smaller props when you want a closer view of the performer."),
            ("Wider view", "Rear center", "Still workable for larger stage magic when the price difference matters more than close-up detail."),
        ],
        "guide": "/guides/best-magic-shows/",
    },
    "music": {
        "label": "Music & Variety", "eyebrow": "Music & variety",
        "good": ["You want music, performers and stage energy to carry the night.", "The songs or performance style are already the reason you are considering the show."],
        "think": [],
        "seat": [
            ("Sweet spot", "Center-middle", "A balanced view of the performers and full stage without giving up too much proximity."),
            ("Closer", "Front section", "Better when performer detail and concert energy matter more than seeing every part of the stage at once."),
            ("Wider view", "Rear center", "Useful for choreography, ensemble numbers and value when the room has clean sightlines."),
        ],
        "guide": "/guides/",
    },
    "spectaculars": {
        "label": "Spectaculars", "eyebrow": "Vegas spectacle",
        "good": ["You want scale, effects and production design to be the attraction.", "You like visual storytelling and big stage moments."],
        "think": [],
        "seat": [
            ("Sweet spot", "Center-middle", "The safest choice for reading the production as a whole instead of chasing the closest possible row."),
            ("Closer", "Lower / near stage", "More performer detail while still keeping much of the wider stage picture in view."),
            ("Wider view", "Higher / farther back", "Useful for seeing the geometry, choreography and large effects at once."),
        ],
        "guide": "/guides/",
    },
}

MANUAL = {
    "shows/cirque/o/index.html": {
        "headline": "“O” by Cirque du Soleil", "kicker": "Aquatic Cirque · Bellagio",
        "dek": "An aquatic Cirque production built around a massive pool, synchronized swimming, diving and aerial work at Bellagio.",
        "take": "If the pool and scale are what caught your attention, this is the point. Center-middle is the easiest seating default because you can read both the water choreography and the aerial work without being too close to one element.",
        "good": ["You want a large-scale Cirque production.", "Water, diving and aerial work are the reason you are choosing the show.", "You want a polished Bellagio night."],
        "think": ["You actually want a magic show.", "You prefer a comedian or singer to be the clear focus.", "You want a smaller-scale production."],
    },
    "shows/magic/penn-and-teller/index.html": {
        "headline": "Penn & Teller", "kicker": "Magic + comedy · Rio",
        "dek": "Magic, skepticism and comedy from one of Las Vegas’s longest-running headliner acts at the Rio.",
        "take": "This is a personality-first magic show. If you want Penn and Teller specifically, prioritize a clear central view over chasing the closest possible row.",
    },
    "shows/adult/atomic-saloon/index.html": {
        "headline": "Atomic Saloon Show", "kicker": "Spiegelworld · The Venetian",
        "dek": "A bawdy, circus-heavy Spiegelworld production with comedy, acrobatics and a deliberately chaotic saloon atmosphere.",
        "take": "The room and the energy are part of the product here. Closer emphasizes performer detail; a little farther back makes it easier to read the full room and staging.",
    },
    "shows/music/blue-man-group/index.html": {
        "headline": "Blue Man Group", "kicker": "Visual percussion · Luxor",
        "dek": "Percussion, visual comedy, paint and big sensory set pieces at Luxor.",
        "take": "Blue Man Group makes the most sense when the group cannot agree on one genre. It combines live music energy, visual comedy and a deliberately loud sensory production.",
    },
    "shows/spectaculars/awakening/index.html": {
        "headline": "Awakening", "kicker": "Production spectacle · Wynn",
        "dek": "A high-production fantasy spectacle built around a 360-degree theater, large-scale effects, choreography and visual storytelling at Wynn.",
        "take": "This is a production-first choice. The theater itself is part of the reason to book it, so favor a balanced view of the whole room rather than treating the closest possible seat as automatically best.",
    },
    "shows/comedy/tape-face/index.html": {
        "headline": "Tape Face", "kicker": "Visual comedy · MGM Grand",
        "dek": "Wordless physical comedy built from props, music and facial expressions at MGM Grand.",
        "take": "Tape Face is useful when your group has very different comedy tastes or different first languages. It may be a weaker fit if what you actually want is verbal stand-up—there is essentially no spoken comedy here.",
    },
    "shows/family/tournament-of-kings/index.html": {
        "headline": "Tournament of Kings", "kicker": "Dinner show · Excalibur",
        "dek": "Live jousting, trained horses, sword combat and a medieval-style dinner served around the arena at Excalibur.",
        "take": "This is an easy family pick when dinner solving part of the night is a feature. It is an arena-style medieval dinner show rather than a quiet meal or traditional theater.",
    },
    "shows/adult/zombie-burlesque/index.html": {
        "headline": "Zombie Burlesque", "kicker": "Adult comedy · Planet Hollywood",
        "dek": "Campy zombie comedy, burlesque, specialty acts and live music at V Theater inside Miracle Mile Shops.",
        "take": "This is a comedy-first adult show with a deliberately silly theme. It may be a weaker fit if you want a serious horror attraction or a traditional burlesque revue without the zombie-cabaret framing.",
    },
}

VENUE_SLUGS = {
    "bellagio": "bellagio", "rio": "rio", "venetian": "venetian", "palazzo": "venetian",
    "luxor": "luxor", "wynn": "wynn", "mgm grand": "mgm-grand", "planet hollywood": "planet-hollywood",
    "miracle mile": "planet-hollywood", "flamingo": "flamingo", "horseshoe": "horseshoe",
    "excalibur": "excalibur", "strat": "strat", "caesars palace": "caesars-palace",
    "treasure island": "treasure-island", "sahara": "sahara", "resorts world": "resorts-world",
    "paris": "paris", "new york-new york": "new-york-new-york", "mandalay bay": "mandalay-bay",
    "harrah": "harrahs", "westgate": "westgate", "plaza": "plaza", "fontainebleau": "fontainebleau",
}

FEATURES = [
    ("aquatic", "Aquatic stagecraft"), ("water", "Water stagecraft"), ("aerial", "Aerial work"),
    ("acrobat", "Acrobatics"), ("joust", "Live jousting"), ("horse", "Live horses"),
    ("mind-read", "Mind reading"), ("mind read", "Mind reading"), ("hypnosis", "Hypnosis"),
    ("magic", "Magic"), ("illusion", "Illusions"), ("comedy", "Comedy"), ("stand-up", "Stand-up"),
    ("burlesque", "Burlesque"), ("live band", "Live band"), ("live music", "Live music"),
    ("tribute", "Tribute music"), ("dance", "Dance"), ("percussion", "Percussion"),
    ("puppet", "Puppetry"), ("variety", "Variety acts"), ("family", "Family option"),
    ("360", "360° theater"), ("robot", "Robot combat"), ("pet", "Animal acts"),
]


def relpath(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", htmllib.unescape(re.sub(r"<[^>]+>", " ", value or ""))).strip()


def strip_banned_sentences(value: str) -> str:
    if not value:
        return value
    sentences = re.split(r"(?<=[.!?])\s+", clean_text(value))
    kept = [s for s in sentences if not any(b in s.lower() for b in BANNED_COPY)]
    return " ".join(kept).strip()


def json_blocks(text: str):
    out = []
    for raw in re.findall(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', text, re.I | re.S):
        try:
            out.append(json.loads(raw.strip()))
        except Exception:
            pass
    return out


def event_obj(blocks):
    for obj in blocks:
        if isinstance(obj, dict) and obj.get("@type") in ("Event", "EventSeries"):
            return copy.deepcopy(obj)
    return None


def faq_obj(blocks):
    for obj in blocks:
        if isinstance(obj, dict) and obj.get("@type") == "FAQPage":
            return copy.deepcopy(obj)
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": []}


def normalize_time(h: int, m: int, ap: str) -> str:
    ap = ap.upper().replace(".", "")
    if ap == "PM" and h != 12:
        h += 12
    if ap == "AM" and h == 12:
        h = 0
    return f"{h:02d}:{m:02d}"


def parse_times(value: str):
    times = []
    for m in re.finditer(r'(?<!\d)(1[0-2]|0?[1-9])(?::([0-5]\d))?\s*(A\.?M\.?|P\.?M\.?)(?!\w)', value or "", re.I):
        t = normalize_time(int(m.group(1)), int(m.group(2) or 0), m.group(3))
        if t not in times:
            times.append(t)
    return times


def fmt_time(t: str) -> str:
    try:
        hh, mm = map(int, t[:5].split(":"))
        ap = "AM" if hh < 12 else "PM"
        h = hh % 12 or 12
        return f"{h}:{mm:02d} {ap}"
    except Exception:
        return t


def parse_days_from_text(value: str):
    text = value or ""
    found = []
    aliases = {d.lower(): d for d in DAYS}
    aliases.update({d[:3].lower(): d for d in DAYS})
    # Explicit ranges first.
    daypat = r'(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|Mon|Tue|Wed|Thu|Fri|Sat|Sun)'
    for m in re.finditer(daypat + r'\s*(?:-|–|—|through|thru|to)\s*' + daypat, text, re.I):
        a = aliases[m.group(1)[:3].lower()]
        b = aliases[m.group(2)[:3].lower()]
        ia, ib = DAYS.index(a), DAYS.index(b)
        seq = DAYS[ia:ib + 1] if ia <= ib else DAYS[ia:] + DAYS[:ib + 1]
        for d in seq:
            if d not in found:
                found.append(d)
    for m in re.finditer(daypat, text, re.I):
        d = aliases[m.group(1)[:3].lower()]
        if d not in found:
            found.append(d)
    return found


def schedule_map(ev: dict, faq: dict):
    out = {d: [] for d in DAYS}
    schedules = ev.get("eventSchedule") or []
    if isinstance(schedules, dict):
        schedules = [schedules]
    for sch in schedules:
        if not isinstance(sch, dict):
            continue
        by = sch.get("byDay") or []
        if isinstance(by, str):
            by = [by]
        times = sch.get("startTime") or []
        if isinstance(times, str):
            times = [times]
        for day in by:
            day = str(day).split("/")[-1]
            if day in out:
                for t in times:
                    if t and t not in out[day]:
                        out[day].append(t)
    active = [d for d in DAYS if out[d]]
    faq_candidates = []
    for q in faq.get("mainEntity", []):
        name = str(q.get("name", ""))
        if re.search(r'when|nights?|show\s*times?|showtimes?|schedule|perform', name, re.I):
            ans = str((q.get("acceptedAnswer") or {}).get("text", ""))
            ts = parse_times(ans)
            if ts:
                faq_candidates.append((ans, ts, parse_days_from_text(ans)))
    # Add missing repeated nightly times only when the schema is a single repeated schedule.
    if len(schedules) <= 1 and active:
        for ans, ts, _days in faq_candidates:
            global_wording = bool(re.search(r'nightly|each night|two shows|shows? (?:nightly|at)', ans, re.I))
            if global_wording or len(ts) > len({t for d in active for t in out[d]}):
                for d in active:
                    for t in ts:
                        if t not in out[d]:
                            out[d].append(t)
    # If schema has no usable schedule, recover one from the schedule FAQ.
    if not active and faq_candidates:
        ans, ts, fd = faq_candidates[0]
        fd = fd or DAYS
        for d in fd:
            out[d] = list(ts)
    return out


def schedule_schema(smap):
    groups = {}
    for d in DAYS:
        ts = tuple(smap[d])
        if ts:
            groups.setdefault(ts, []).append(d)
    rows = []
    for ts, days in groups.items():
        rows.append({"@type": "Schedule", "byDay": days, "startTime": list(ts) if len(ts) > 1 else ts[0]})
    if not rows:
        return None
    return rows[0] if len(rows) == 1 else rows


def derive_runtime(text: str, ev: dict, faq: dict):
    sources = []
    for q in faq.get("mainEntity", []):
        if re.search(r'how long|runtime|length', str(q.get("name", "")), re.I):
            sources.append(str((q.get("acceptedAnswer") or {}).get("text", "")))
    sources += [str(ev.get("description", ""))]
    sources += [text]
    for src in sources:
        for m in re.finditer(r'(?<!\d)(\d{2,3})\s*(?:-\s*)?(?:minute|minutes|min\b)', src, re.I):
            n = int(m.group(1))
            if 45 <= n <= 180:
                return n
    return None


def derive_age(text: str, faq: dict):
    sources = []
    for q in faq.get("mainEntity", []):
        if re.search(r'age|kids?|children|child|appropriate', str(q.get("name", "")), re.I):
            sources.append(str((q.get("acceptedAnswer") or {}).get("text", "")))
    sources.append(text)
    for src in sources:
        low = src.lower()
        if "all ages" in low:
            return "All ages"
        patterns = [
            r'ages?\s*(\d{1,2})\s*(?:\+|and up|or older)',
            r'(?:minimum age|must be|guests? must be)\s*(\d{1,2})',
            r'(\d{1,2})\s*(?:and up|or older|\+)',
        ]
        for p in patterns:
            m = re.search(p, src, re.I)
            if m:
                n = int(m.group(1))
                if 2 <= n <= 21:
                    return f"{n}+"
    return "Check policy"


def image_candidates(text: str, ev: dict, slug: str):
    evimg = ev.get("image") or ""
    if isinstance(evimg, list):
        evimg = evimg[0] if evimg else ""
    names = []
    if evimg:
        names.append(str(evimg).split("/images/")[-1].split("?")[0])
    names += re.findall(r'/images/([^"\'<>?]+\.(?:jpe?g|png|webp|avif))', text, re.I)
    # Also consider existing local assets with a matching slug prefix; this recovers unreferenced gallery photos.
    for p in sorted(IMAGES.glob(slug + "*")):
        if p.is_file() and p.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp", ".avif"):
            names.append(p.name)
    unique = []
    seen = set()
    # Infer base from event image when possible.
    hero_name = names[0] if names else ""
    stem = re.sub(r'\.(?:jpe?g|png|webp|avif)$', '', hero_name, flags=re.I)
    base = re.sub(r'-(?:hero|og)$', '', stem, flags=re.I)
    for name in names:
        local = IMAGES / Path(name).name
        if not local.exists():
            continue
        st = re.sub(r'\.(?:jpe?g|png|webp|avif)$', '', local.name, flags=re.I)
        if base:
            if not (st == base or st.startswith(base + "-")):
                continue
        elif not (st == slug or st.startswith(slug + "-")):
            continue
        low = st.lower()
        if any(x in low for x in ("-og", "thumb", "video-poster", "video-thumb", "logo", "seat-map", "seating-chart", "-map")):
            continue
        key = st.lower()
        if key not in seen:
            seen.add(key)
            unique.append("/images/" + local.name)
    return unique[:5]


def video_id(text: str):
    pats = [
        r'data-video-id=["\']([A-Za-z0-9_-]{6,})',
        r'youtube(?:-nocookie)?\.com/embed/([A-Za-z0-9_-]{6,})',
        r'youtu\.be/([A-Za-z0-9_-]{6,})',
    ]
    for p in pats:
        m = re.search(p, text, re.I)
        if m:
            return m.group(1)
    return None


def meta_content(text: str, name: str = "description", prop: str | None = None):
    if prop:
        m = re.search(r'<meta[^>]+property=["\']' + re.escape(prop) + r'["\'][^>]+content=["\']([^"\']+)', text, re.I)
    else:
        m = re.search(r'<meta[^>]+name=["\']' + re.escape(name) + r'["\'][^>]+content=["\']([^"\']+)', text, re.I)
    return htmllib.unescape(m.group(1)).strip() if m else ""


def substantial_paragraphs(text: str):
    vals = []
    for raw in re.findall(r'<p[^>]*>(.*?)</p>', text, re.I | re.S):
        s = clean_text(raw)
        low = s.lower()
        if not (110 <= len(s) <= 700):
            continue
        if any(b in low for b in BANNED_COPY):
            continue
        if any(x in low for x in ("affiliate disclosure", "sign up", "subscribe", "last updated", "email address", "privacy policy")):
            continue
        if "$" in s or re.search(r'\bfrom \d', low):
            continue
        if s not in vals:
            vals.append(s)
        if len(vals) >= 2:
            break
    return vals


def section_paragraphs(text: str, section_id: str):
    m = re.search(
        r'<section\\b[^>]*\\bid=["\\\']' + re.escape(section_id) + r'["\\\'][^>]*>(.*?)</section>',
        text,
        re.I | re.S,
    )
    if not m:
        return []
    vals = []
    for raw in re.findall(r'<p[^>]*>(.*?)</p>', m.group(1), re.I | re.S):
        value = clean_text(raw)
        if value and value not in vals:
            vals.append(value)
    return vals


def current_benchmark_page(text: str) -> bool:
    return (
        bool(re.search(r'id=["\\\']about["\\\']', text, re.I))
        and "Show info confirmed " in text
        and 'id="showtimes"' in text
    )


def venue_link(venue: str):
    low = (venue or "").lower()
    for needle, slug in VENUE_SLUGS.items():
        if needle in low:
            p = ROOT / "venues" / slug / "index.html"
            if p.exists():
                return f"/venues/{slug}/", venue
    return "/venues/", "Vegas venue guides"


def features(description: str, venue: str, category: str):
    out = []
    low = description.lower()
    for needle, label in FEATURES:
        if needle in low and label not in out:
            out.append(label)
    fallback = {
        "adult": "Adult Vegas", "cirque": "Acrobatics", "comedy": "Comedy",
        "family": "Family option", "magic": "Magic", "music": "Music & variety",
        "spectaculars": "Large-scale production"
    }[category]
    if fallback not in out:
        out.insert(0, fallback)
    short_venue = venue.split(" at ")[-1].split(" inside ")[-1]
    if short_venue and short_venue not in out:
        out.append(short_venue)
    out.append("Center-middle is the easy seat default")
    return out[:4]


def faq_clean(faq: dict, price, runtime, venue, smap, name):
    entities = []
    for q in faq.get("mainEntity", []):
        blob = json.dumps(q).lower()
        if any(b in blob for b in BANNED_COPY) or re.search(r'\b(?:fee|fees)\b', blob):
            continue
        entities.append(q)
    # Guarantee useful visible/schema FAQs if a legacy page was sparse.
    names = " ".join(str(q.get("name", "")) for q in entities).lower()
    if price not in (None, "") and "how much" not in names and "price" not in names:
        entities.append({"@type": "Question", "name": f"How much are {name} tickets?", "acceptedAnswer": {"@type": "Answer", "text": f"Tickets start at ${price}. Other price points may be available."}})
    if runtime and "how long" not in names and "runtime" not in names:
        entities.append({"@type": "Question", "name": f"How long is {name}?", "acceptedAnswer": {"@type": "Answer", "text": f"Plan on about {runtime} minutes. Confirm the current runtime if your exact date matters to the rest of your night."}})
    if venue and "where" not in names:
        entities.append({"@type": "Question", "name": f"Where is {name}?", "acceptedAnswer": {"@type": "Answer", "text": f"The show is at {venue}. Give yourself extra time to navigate the property if it is your first visit."}})
    faq["mainEntity"] = entities[:7]
    return faq


def related_cards(category: str, current: Path):
    candidates = []
    for p in (SHOWS / category).glob("*/index.html"):
        if p == current:
            continue
        blocks = json_blocks(p.read_text(encoding="utf-8", errors="ignore"))
        ev = event_obj(blocks)
        if not ev or ev.get("eventStatus") != "https://schema.org/EventScheduled":
            continue
        offer = ev.get("offers") if isinstance(ev.get("offers"), dict) else {}
        imgs = image_candidates(p.read_text(encoding="utf-8", errors="ignore"), ev, p.parent.name)
        if not imgs:
            continue
        candidates.append((f"/{p.parent.relative_to(ROOT).as_posix()}/", ev.get("name") or p.parent.name.replace("-", " ").title(), imgs[0], offer.get("price", "")))
    rnd = random.Random(hashlib.sha256(str(current).encode()).hexdigest())
    rnd.shuffle(candidates)
    return candidates[:3]


def fact(value: str, label: str, count=None, prefix="", suffix=""):
    attrs = ""
    if count is not None:
        attrs = f' data-count="{count}" data-prefix="{htmllib.escape(prefix)}" data-suffix="{htmllib.escape(suffix)}"'
    return f'<div class="fact"><strong{attrs}>{htmllib.escape(value)}</strong><span>{htmllib.escape(label)}</span></div>'


def page_context(path: Path):
    text = path.read_text(encoding="utf-8", errors="replace")
    blocks = json_blocks(text)
    ev = event_obj(blocks)
    if not ev:
        return None
    faq = faq_obj(blocks)
    category = path.parts[path.parts.index("shows") + 1]
    profile = PROFILES[category]
    offer = ev.get("offers") if isinstance(ev.get("offers"), dict) else {}
    offer = copy.deepcopy(offer)
    try:
        p = float(offer.get("price"))
        offer["price"] = int(p) if p.is_integer() else p
    except Exception:
        pass
    ev["offers"] = offer
    price = offer.get("price", "")
    canonical = str(ev.get("url") or f"https://vegassidekick.com/{path.parent.relative_to(ROOT).as_posix()}/")
    ev["url"] = canonical
    ev["@id"] = canonical + "#event"
    if isinstance(ev.get("description"), str):
        ev["description"] = strip_banned_sentences(ev["description"])
    org = ev.get("organizer") if isinstance(ev.get("organizer"), dict) else {}
    org.setdefault("@type", "Organization")
    org.setdefault("name", ev.get("name") or path.parent.name.replace("-", " ").title())
    org.setdefault("url", canonical)
    ev["organizer"] = org
    venue = ""
    if isinstance(ev.get("location"), dict):
        venue = str(ev["location"].get("name") or "")
    runtime = derive_runtime(text, ev, faq)
    age = derive_age(text, faq)
    smap = schedule_map(ev, faq)
    sch = schedule_schema(smap)
    if sch:
        ev["eventSchedule"] = sch
    faq = faq_clean(faq, price, runtime, venue, smap, ev.get("name") or path.parent.name)
    imgs = image_candidates(text, ev, path.parent.name)
    vid = video_id(text)
    manual = MANUAL.get(relpath(path), {})
    headline = manual.get("headline") or str(ev.get("name") or path.parent.name.replace("-", " ").title())
    raw_desc = manual.get("dek") or strip_banned_sentences(str(ev.get("description") or meta_content(text) or ""))
    if not raw_desc:
        raw_desc = f"A Las Vegas {profile['label'].lower()} option at {venue}."
    # Keep the hero dek compact; the longer legacy copy can live in Quick Take.
    dek = raw_desc if len(raw_desc) <= 230 else raw_desc[:227].rsplit(" ", 1)[0] + "…"
    kicker = manual.get("kicker") or f"{profile['eyebrow']} · {venue or 'Las Vegas'}"
    take = manual.get("take") or f"{headline} makes the most sense when the premise itself is what you want. If your group is actually shopping for a different kind of night, use the comparison links below before you lock it in."
    good = manual.get("good") or [profile["good"][0], profile["good"][1], f"The premise of {headline} sounds like what your group wants."]
    think = manual.get("think") or []
    about = section_paragraphs(text, "about")
    legacy_paras = substantial_paragraphs(text)
    if not about:
        about = legacy_paras[:2]
    if not about:
        about = [raw_desc]
    return {
        "text": text, "ev": ev, "faq": faq, "category": category, "profile": profile,
        "offer": offer, "price": price, "canonical": canonical, "venue": venue, "runtime": runtime,
        "age": age, "smap": smap, "imgs": imgs, "video": vid, "headline": headline,
        "dek": dek, "kicker": kicker, "take": take, "good": good, "think": think,
        "about": about,
        "booking_tip": manual.get("booking_tip"),
        "paras": [],
    }


def render(path: Path, ctx: dict):
    ev, faq = ctx["ev"], ctx["faq"]
    category, profile = ctx["category"], ctx["profile"]
    price, ticket = ctx["price"], str(ctx["offer"].get("url") or "")
    venue, runtime, age, smap = ctx["venue"], ctx["runtime"], ctx["age"], ctx["smap"]
    imgs, vid = ctx["imgs"], ctx["video"]
    headline, dek, kicker, take = ctx["headline"], ctx["dek"], ctx["kicker"], ctx["take"]
    hero = imgs[0] if imgs else "/favicon.png"
    if hero.startswith("/images/"):
        ev["image"] = "https://vegassidekick.com" + hero
    cat_url = f"/shows/{category}/"
    venue_url, venue_label = venue_link(venue)
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://vegassidekick.com/"},
        {"@type": "ListItem", "position": 2, "name": profile["label"], "item": "https://vegassidekick.com" + cat_url},
        {"@type": "ListItem", "position": 3, "name": headline, "item": ctx["canonical"]},
    ]}
    webpage = {"@context": "https://schema.org", "@type": "WebPage", "url": ctx["canonical"], "dateModified": TODAY, "lastReviewed": TODAY, "author": AUTHOR, "mainEntity": {"@id": ctx["canonical"] + "#event"}}
    schema = "\n".join('<script type="application/ld+json">' + json.dumps(x, separators=(",", ":"), ensure_ascii=False) + "</script>" for x in (ev, faq, crumbs, webpage))
    first_times = [t for d in DAYS for t in smap[d]]
    first_time = fmt_time(first_times[0]) if first_times else "See calendar"
    runtime_fact = fact(f"{runtime} min" if runtime else "See details", "Runtime", runtime if runtime else None, "", " min")
    price_fact = fact(f"${price}" if price != "" else "See price", "Tickets from", price if isinstance(price, (int, float)) else None, "$", "")
    time_fact = fact(first_time, "Start time")
    age_count = None
    age_suffix = ""
    age_prefix = ""
    m_age = re.fullmatch(r'(\d+)\+', age)
    if m_age:
        age_count = int(m_age.group(1)); age_suffix = "+"
    age_fact = fact(age, "Age guidance", age_count, age_prefix, age_suffix)
    feats = features(dek + " " + str(ev.get("description", "")), venue, category)
    ticker_unit = "".join(f'<span class="ticker-item">{htmllib.escape(x)}</span><span class="ticker-sep">✦</span>' for x in feats)
    gallery_cls = f"gallery-{max(1, min(len(imgs), 4))}"
    gallery = "".join(f'<button type="button" aria-label="Open {htmllib.escape(headline)} photo"><img src="{im}" alt="{htmllib.escape(headline)} Las Vegas show photo" loading="lazy"></button>' for im in imgs)
    photo_note = ""
    video_html = ""
    if vid:
        video_html = f'<div class="video-wrap"><button class="video-preview" type="button" data-video-id="{vid}" aria-label="Play official {htmllib.escape(headline)} video"><img src="{hero}" alt=""><span>▶ Watch official preview</span></button></div>'
    seats = profile["seat"]
    seat_buttons = "".join(f'<button class="seat-zone {cl}{" active" if i==0 else ""}" data-tag="{htmllib.escape(tag)}" data-title="{htmllib.escape(title)}" data-copy="{htmllib.escape(copytxt)}"><strong>{htmllib.escape(title)}</strong><small>{htmllib.escape(copytxt)}</small></button>' for i,(cl,(tag,title,copytxt)) in enumerate(zip(("center","close","wide"), seats)))
    s0 = seats[0]
    good_html = "".join(f"<li>{htmllib.escape(x)}</li>" for x in ctx["good"])
    about_html = "".join(f"<p>{htmllib.escape(x)}</p>" for x in ctx["about"])
    quick_take = ctx["good"][0] if ctx["good"] else take
    fit_copy = ctx["good"][1] if len(ctx["good"]) > 1 else quick_take
    days = []
    for d in DAYS:
        ts = smap[d]
        if ts:
            label = " · ".join(fmt_time(t) for t in ts)
            days.append(f'<div class="day"><a href="{ticket}" target="_blank" rel="noopener sponsored"><strong>{d[:3]}</strong><span>{label}</span><small>Tickets →</small></a></div>')
        else:
            days.append(f'<div class="day dark"><strong>{d[:3]}</strong><span>Dark</span></div>')
    faq_html = "".join(f'<details><summary>{htmllib.escape(str(q.get("name","Question")))}</summary><div>{htmllib.escape(str((q.get("acceptedAnswer") or {}).get("text", "")))}</div></details>' for q in faq.get("mainEntity", []))
    related = related_cards(category, path)
    rel_html = "".join(f'<a class="related-card" href="{url}"><img src="{img}" alt="{htmllib.escape(name)}" loading="lazy"><div><strong>{htmllib.escape(name)}</strong><small>{("From $"+str(pr)) if pr not in (None,"") else profile["label"]}</small></div></a>' for url,name,img,pr in related)
    extra_copy = "".join(f"<p>{htmllib.escape(p)}</p>" for p in ctx["paras"])
    desc = f"{dek} Tickets from ${price}. See photos, our interactive seat guide, showtimes, FAQ and the honest fit before you book." if price != "" else f"{dek} See photos, our interactive seat guide, showtimes, FAQ and the honest fit before you book."
    title_price = f" from ${price}" if price != "" else ""
    price_display = f"${price}" if price != "" else "See price"
    booking_tip = ctx.get("booking_tip")
    booking_tip_card = f'<div class="decision-card"><h3>Booking tip</h3><p>{htmllib.escape(booking_tip)}</p></div>' if booking_tip else ""
    mobile = f'<div class="mobile-bar"><div class="mobile-progress" id="mobileProgress"></div><div class="mobile-inner"><div class="mobile-price"><small>FROM</small>{price_display}</div><a class="cta vs-ticket-primary" href="{ticket}" target="_blank" rel="noopener sponsored">Get Tickets →</a></div></div>'
    return f'''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="icon" href="/favicon.png" type="image/png"><title>{htmllib.escape(headline)} Tickets{title_price} & Show Guide | Vegas Sidekick</title><meta name="robots" content="index,follow,max-image-preview:large"><meta name="description" content="{htmllib.escape(desc)}"><link rel="canonical" href="{ctx['canonical']}"><meta property="og:site_name" content="Vegas Sidekick"><meta property="og:title" content="{htmllib.escape(headline)} Tickets & Show Guide | Vegas Sidekick"><meta property="og:description" content="{htmllib.escape(dek)}"><meta property="og:image" content="https://vegassidekick.com{hero}"><meta property="og:image:alt" content="{htmllib.escape(headline)} Las Vegas"><meta property="og:url" content="{ctx['canonical']}"><meta property="og:type" content="website"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="https://vegassidekick.com{hero}"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@600;700;800&family=IBM+Plex+Mono:wght@500;600&display=swap" rel="stylesheet"><link rel="stylesheet" href="/assets/show-canonical.css?v=2">{schema}</head><body data-canonical-layout="2"><div class="progress"></div><a class="skip" href="#main">Skip to content</a><div id="vs-header"></div><header class="hero"><div class="hero-grid"><div class="hero-copy"><div class="crumbs"><a href="/">Home</a><span>›</span><a href="{cat_url}">{htmllib.escape(profile['label'])}</a><span>›</span>{htmllib.escape(headline)}</div><div class="eyebrow">{htmllib.escape(kicker)}</div><h1>{htmllib.escape(headline)}</h1><p class="hero-dek">{htmllib.escape(dek)}</p><div class="chips">{('<span class="chip">'+str(runtime)+' minutes</span>') if runtime else ''}<span class="chip">{htmllib.escape(age)}</span><span class="chip">{htmllib.escape(venue)}</span></div><div class="buybox"><div class="price"><small>Tickets from</small>{price_display}</div><a class="cta vs-ticket-primary" href="{ticket}" target="_blank" rel="noopener sponsored">Get Tickets →</a></div><div class="updated">Tickets start at {price_display}. Other price points may be available.</div></div><div class="hero-media"><img src="{hero}" alt="{htmllib.escape(headline)} at {htmllib.escape(venue)}" fetchpriority="high"></div></div></header><section class="facts"><div class="wrap facts-grid">{runtime_fact}{price_fact}{time_fact}{age_fact}</div></section><div class="ticker"><div class="ticker-track"><div class="ticker-set">{ticker_unit}{ticker_unit}</div></div></div><nav class="subnav" aria-label="On this page"><div class="wrap"><a href="#about">What is it?</a><a href="#quick">Quick take</a><a href="#photos">Photos</a><a href="#seats">Seat guide</a><a href="#fit">Is it for you?</a><a href="#showtimes">Showtimes</a><a href="#faq">FAQ</a></div></nav><main id="main"><section class="section" id="about"><div class="wrap"><div class="copy"><div class="eyebrow">What is the show?</div><h2>What is {htmllib.escape(headline)}?</h2>{about_html}</div></div></section><section class="section" id="quick"><div class="wrap verdict-grid"><div class="copy"><div class="eyebrow">The 30-second answer</div><h2>Is {htmllib.escape(headline)} worth seeing?</h2><p class="lede lede-highlight">{htmllib.escape(quick_take)}</p>{extra_copy}<div class="take"><span>🌵</span><div><b>Kris’s take</b><p>{htmllib.escape(take)}</p></div></div></div><div class="decision"><div class="decision-card"><h3>Good fit</h3><p>{htmllib.escape(fit_copy)}</p></div>{booking_tip_card}</div></div></section><section class="section alt" id="photos"><div class="wrap"><div class="eyebrow">See the show</div><h2>Photos from {htmllib.escape(headline)}</h2><p>Use the photos to understand the scale and visual style before you choose the seat.</p><div class="gallery {gallery_cls}">{gallery}</div>{photo_note}{video_html}</div></section><section class="section" id="seats"><div class="wrap"><div class="eyebrow">Interactive seat guide</div><h2>Where should you sit?</h2><div class="seat-layout"><div class="theater"><div class="stage">STAGE</div>{seat_buttons}</div><div class="seat-side"><div class="seat-details" id="seat-detail"><div class="tag">{htmllib.escape(s0[0])}</div><h3>{htmllib.escape(s0[1])}</h3><p>{htmllib.escape(s0[2])}</p><a class="cta vs-ticket-primary" href="{ticket}" target="_blank" rel="noopener sponsored">Check seats →</a></div></div></div></div></section><section class="section alt" id="fit"><div class="wrap"><div class="eyebrow">Is it for you?</div><h2>Who it fits best</h2><div class="fit-grid solo"><div class="fit-card good"><h3>Good fit</h3><ul>{good_html}</ul></div></div></div></section><section class="section" id="showtimes"><div class="wrap"><div class="eyebrow">Plan the night</div><h2>Find your showtime</h2><div class="schedule">{''.join(days)}</div><a class="later-date-cta" href="{ticket}" target="_blank" rel="noopener sponsored">See available dates & times →</a><p>Schedules can change. Confirm your exact performance date and time during checkout.</p></div></section><section class="section alt" id="faq"><div class="wrap"><div class="eyebrow">Before you book</div><h2>Frequently asked questions</h2><div class="faq">{faq_html}</div></div></section><section class="section"><div class="wrap"><div class="eyebrow">Keep comparing</div><h2>You may also like</h2><div class="related-grid">{rel_html}</div></div></section><section class="section alt"><div class="wrap"><div class="eyebrow">Still deciding?</div><h2>Make the next click useful</h2><div class="next-grid"><a class="next-card" style="--accent:#6d28d9" href="{cat_url}"><h3>Compare {htmllib.escape(profile['label'])} →</h3><p>See the full category before you lock in the night.</p></a><a class="next-card" style="--accent:#0fb2c7" href="{venue_url}"><h3>Explore {htmllib.escape(venue_label)} →</h3><p>See what else is playing at the same property or use the venue guide.</p></a><a class="next-card" style="--accent:#f43f8c" href="{profile['guide']}"><h3>Open a Vegas Sidekick guide →</h3><p>Use a guide when you want recommendations instead of another long list.</p></a></div></div></section><section class="section"><div class="wrap"><a class="author-card" href="/about/kris-kidd/"><img src="/images/kris-kidd.webp" alt="Kris Kidd" loading="lazy"><div><strong>Kris Kidd · Vegas Sidekick</strong><p>Las Vegas show and ticketing guidance. Show info confirmed {MONTH_LABEL}.</p></div></a><p class="disclosure-line">Vegas Sidekick may earn a commission when you buy through our links. <a href="/affiliate-disclosure/">Affiliate disclosure</a>.</p></div></section><section class="section alt final-section"><div class="wrap"><h2>{htmllib.escape(headline)} tickets</h2><p class="lede">Starting at {price_display}. Pick the date first, then choose the seat that matches how you want to experience the show.</p><a class="cta vs-ticket-primary" href="{ticket}" target="_blank" rel="noopener sponsored">See Tickets →</a></div></section></main><div id="vs-footer"></div>{mobile}<div class="lightbox" id="lightbox" role="dialog" aria-modal="true" aria-label="Show photo"><button id="lightboxClose" aria-label="Close photo">×</button><img id="lightboxImg" alt=""></div><script src="/components/header.js?v=14"></script><script src="/components/footer.js?v=14"></script><script src="/assets/show-canonical.js?v=2"></script></body></html>'''


def ensure_assets():
    css_path = ROOT / "assets" / "show-canonical.css"
    if not css_path.exists():
        vegas = (SHOWS / "music" / "vegas-the-show" / "index.html").read_text(encoding="utf-8")
        m = re.search(r'<style>(.*?)</style>', vegas, re.I | re.S)
        if not m:
            raise RuntimeError("Cannot seed canonical CSS from VEGAS! The Show")
        css = m.group(1)
    else:
        css = css_path.read_text(encoding="utf-8")
    marker = "/* canonical-v2-extras */"
    if marker not in css:
        css += r'''
/* canonical-v2-extras */
.author-card{display:grid;grid-template-columns:auto 1fr;gap:16px;align-items:center;border:1px solid var(--line);border-radius:18px;padding:22px;background:#fff}.author-card img{width:64px;height:64px;border-radius:50%;object-fit:cover}.author-card strong{font-family:'Plus Jakarta Sans',sans-serif}.author-card p{margin:4px 0 0;color:var(--muted);font-size:.9rem}.disclosure-line{font-size:.72rem;color:var(--muted);margin-top:12px}.disclosure-line a{text-decoration:underline}.gallery.gallery-1{display:block;height:auto}.gallery.gallery-1 button{width:100%;height:min(520px,58vw)}.gallery.gallery-2{grid-template-columns:1fr 1fr;grid-template-rows:1fr;height:430px}.gallery.gallery-2 button:first-child{grid-row:auto}.gallery.gallery-3{grid-template-columns:1.35fr 1fr;grid-template-rows:1fr 1fr}.gallery.gallery-4{grid-template-columns:1.2fr 1fr;grid-template-rows:1fr 1fr}.media-note{margin-top:18px;padding:14px 16px;border:1px solid var(--line);border-radius:12px;background:#fff;color:var(--muted);font-size:.86rem}.seat-zone.center{background:#6d28d9}.seat-zone.close{background:#a855f7;width:82%;margin-left:auto}.seat-zone.wide{background:#31744a;width:68%;margin:auto}.next-grid,.related-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:24px}.next-card{border:1px solid var(--line);border-top:7px solid var(--accent,#6d28d9);border-radius:16px;padding:22px;background:#fff}.next-card h3{font-size:1.05rem;margin-bottom:7px}.next-card p{margin:0;color:var(--muted);font-size:.88rem}.related-card{border:1px solid var(--line);border-radius:16px;overflow:hidden;background:#fff;transition:.2s}.related-card:hover{transform:translateY(-3px);box-shadow:0 12px 30px rgba(35,12,60,.12)}.related-card img{width:100%;aspect-ratio:4/3;object-fit:cover}.related-card div{padding:14px}.related-card strong{display:block;font-family:'Plus Jakarta Sans',sans-serif}.related-card small{color:var(--muted)}.video-wrap{margin-top:24px}.video-preview{position:relative;width:100%;border:0;border-radius:18px;overflow:hidden;padding:0;background:#17082e;color:#fff;aspect-ratio:16/9}.video-preview img{width:100%;height:100%;object-fit:cover;opacity:.48}.video-preview span{position:absolute;inset:0;display:grid;place-items:center;font:800 1rem 'Plus Jakarta Sans',sans-serif}.video-wrap iframe{width:100%;aspect-ratio:16/9;border:0;border-radius:18px}.lightbox{position:fixed;inset:0;z-index:9998;background:rgba(8,3,16,.94);display:none;place-items:center;padding:26px}.lightbox.open{display:grid}.lightbox img{max-width:min(1100px,94vw);max-height:88vh;width:auto;border-radius:10px}.lightbox button{position:absolute;top:18px;right:22px;border:0;background:transparent;color:#fff;font-size:2rem}.final-section{text-align:center}.final-section .lede{margin:0 auto 20px}.crumbs a{text-decoration:none}.hero .crumbs{color:#d4c7dd}.hero .crumbs a{color:#fff}.mobile-bar{display:none;position:fixed;bottom:0;left:0;right:0;background:#17082e;color:#fff;z-index:1000;padding:11px 15px 14px;box-shadow:0 -4px 25px rgba(0,0,0,.3)}.mobile-progress{position:absolute;top:0;left:0;width:0;height:3px;background:linear-gradient(90deg,var(--gold),var(--cyan),var(--pink))}.mobile-inner{display:flex;align-items:center;gap:14px}.mobile-price{font:800 1.8rem 'Plus Jakarta Sans',sans-serif;min-width:86px}.mobile-price small{font:600 .55rem Inter,sans-serif;display:block;color:#c7bacb}.mobile-bar .cta{flex:1;padding:11px}@media(max-width:800px){.next-grid,.related-grid{grid-template-columns:1fr}.author-card{grid-template-columns:54px 1fr}.author-card img{width:54px;height:54px}.gallery.gallery-2,.gallery.gallery-3,.gallery.gallery-4{display:grid;grid-template-columns:1fr;height:auto}.gallery.gallery-2 button,.gallery.gallery-3 button,.gallery.gallery-4 button{height:240px}.gallery.gallery-3 button:first-child{grid-row:auto}.mobile-bar{display:block}body{padding-bottom:78px}}
'''
    css_path.write_text(css, encoding="utf-8")
    js = r'''(function(){'use strict';const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;const progress=document.querySelector('.progress'),mobileProgress=document.getElementById('mobileProgress');function prog(){const d=document.documentElement,max=d.scrollHeight-innerHeight,p=max?Math.min(100,scrollY/max*100):0;if(progress)progress.style.width=p+'%';if(mobileProgress)mobileProgress.style.width=p+'%'}addEventListener('scroll',prog,{passive:true});prog();if(!reduce){document.querySelectorAll('.fact strong[data-count]').forEach(el=>{const target=parseFloat(el.dataset.count);if(!isFinite(target))return;const prefix=el.dataset.prefix||'',suffix=el.dataset.suffix||'';let done=false;const io=new IntersectionObserver(es=>es.forEach(en=>{if(!en.isIntersecting||done)return;done=true;io.disconnect();const start=performance.now(),dur=720;function tick(now){const p=Math.min(1,(now-start)/dur),e=1-Math.pow(1-p,3);el.textContent=prefix+Math.round(target*e)+suffix;if(p<1)requestAnimationFrame(tick)}requestAnimationFrame(tick)}),{threshold:.35});io.observe(el)});}const detail=document.getElementById('seat-detail');document.querySelectorAll('.seat-zone').forEach(btn=>btn.addEventListener('click',()=>{document.querySelectorAll('.seat-zone').forEach(b=>b.classList.remove('active'));btn.classList.add('active');if(detail){detail.querySelector('.tag').textContent=btn.dataset.tag||'Seat guide';detail.querySelector('h3').textContent=btn.dataset.title||'';detail.querySelector('p').textContent=btn.dataset.copy||'';}}));const light=document.getElementById('lightbox'),lightImg=document.getElementById('lightboxImg'),close=document.getElementById('lightboxClose');function shut(){if(!light)return;light.classList.remove('open');document.body.style.overflow=''}document.querySelectorAll('.gallery button').forEach(b=>b.addEventListener('click',()=>{if(!light||!lightImg)return;lightImg.src=b.querySelector('img').src;light.classList.add('open');document.body.style.overflow='hidden'}));if(close)close.addEventListener('click',e=>{e.stopPropagation();shut()});if(light)light.addEventListener('click',e=>{if(e.target===light)shut()});addEventListener('keydown',e=>{if(e.key==='Escape')shut()});document.querySelectorAll('.faq details').forEach(d=>d.addEventListener('toggle',()=>{if(d.open)document.querySelectorAll('.faq details').forEach(o=>{if(o!==d)o.open=false})}));document.querySelectorAll('.video-preview[data-video-id]').forEach(btn=>btn.addEventListener('click',()=>{const id=btn.dataset.videoId,wrap=btn.parentElement;if(!id||!wrap)return;const f=document.createElement('iframe');f.src='https://www.youtube-nocookie.com/embed/'+encodeURIComponent(id)+'?autoplay=1';f.title='Official show preview';f.allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';f.allowFullscreen=true;wrap.replaceChildren(f)}));})();'''
    (ROOT / "assets" / "show-canonical.js").write_text(js, encoding="utf-8")


def targets(args):
    if args.paths:
        return [ROOT / p for p in args.paths]
    paths = []
    for cat in CATEGORIES:
        for p in (SHOWS / cat).glob("*/index.html"):
            rp = relpath(p)
            if rp in KEEP_AS_BUILT:
                continue
            blocks = json_blocks(p.read_text(encoding="utf-8", errors="ignore"))
            ev = event_obj(blocks)
            if not ev or ev.get("eventStatus") != "https://schema.org/EventScheduled":
                continue
            paths.append(p)
    rnd = random.Random(20260907)
    rnd.shuffle(paths)
    return paths


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--force-current", action="store_true", help="Allow rebuilding pages that already match the current benchmark structure.")
    args = ap.parse_args()
    ensure_assets()
    todo = targets(args)
    if args.limit:
        todo = todo[:args.limit]
    changed = []
    for p in todo:
        existing = p.read_text(encoding="utf-8", errors="replace")
        if current_benchmark_page(existing) and not args.force_current:
            print("skipped current benchmark page", relpath(p))
            continue
        ctx = page_context(p)
        if not ctx:
            continue
        p.write_text(render(p, ctx), encoding="utf-8")
        changed.append(relpath(p))
        print("canonicalized", relpath(p))
    print(f"Canonicalized {len(changed)} show pages.")

if __name__ == "__main__":
    main()

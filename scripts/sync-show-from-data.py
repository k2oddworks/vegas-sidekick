#!/usr/bin/env python3
"""Sync deterministic show-page facts from data/shows/<slug>.json.

Usage:
  python3 scripts/sync-show-from-data.py carrot-top
  python3 scripts/sync-show-from-data.py --data data/shows/carrot-top.json
  python3 scripts/sync-show-from-data.py --all

The engine intentionally owns factual surfaces only. Editorial copy, rankings,
seat advice, related shows, gallery selection, layout, and other human-judgment
content remain outside this script unless a show record explicitly opts into a
narrow visible-copy rule under `sync`.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "shows"
DAY_ABBR = {
    "Monday": "Mon",
    "Tuesday": "Tue",
    "Wednesday": "Wed",
    "Thursday": "Thu",
    "Friday": "Fri",
    "Saturday": "Sat",
    "Sunday": "Sun",
}


class SyncError(RuntimeError):
    pass


def replace_once(text: str, pattern: str, repl: str, label: str, flags: int = 0) -> str:
    new, count = re.subn(pattern, repl, text, count=1, flags=flags)
    if count != 1:
        raise SyncError(f"Expected exactly one {label}; found {count}")
    return new


def replace_if_present(text: str, pattern: str, repl: str, label: str, flags: int = 0) -> tuple[str, bool]:
    new, count = re.subn(pattern, repl, text, count=1, flags=flags)
    if count > 1:
        raise SyncError(f"Expected at most one {label}; found {count}")
    return new, count == 1


def load_record(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SyncError(f"Show data file not found: {path.relative_to(ROOT)}") from exc
    except json.JSONDecodeError as exc:
        raise SyncError(f"Invalid JSON in {path.relative_to(ROOT)}: {exc}") from exc

    required = ["name", "slug", "canonical_path", "status"]
    missing = [key for key in required if not data.get(key)]
    if missing:
        raise SyncError(f"{path.name}: missing required field(s): {', '.join(missing)}")
    if data.get("record_type") != "show":
        raise SyncError(f"{path.name}: record_type must be 'show'")
    return data


def page_path_for(record: dict[str, Any]) -> Path:
    canonical = str(record["canonical_path"])
    if not canonical.startswith("/shows/") or not canonical.endswith("/"):
        raise SyncError(f"{record['slug']}: canonical_path must be a /shows/.../ path ending in /")
    path = ROOT / canonical.lstrip("/") / "index.html"
    if not path.exists():
        raise SyncError(f"{record['slug']}: page does not exist: {path.relative_to(ROOT)}")
    return path


def format_time(value: str) -> str:
    try:
        hour, minute = (int(part) for part in value.split(":"))
    except Exception as exc:
        raise SyncError(f"Invalid showtime {value!r}; expected HH:MM") from exc
    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        raise SyncError(f"Invalid showtime {value!r}; expected HH:MM")
    suffix = "AM" if hour < 12 else "PM"
    display_hour = hour if 1 <= hour <= 12 else hour - 12 if hour > 12 else 12
    return f"{display_hour}:{minute:02d} {suffix}"


def effective_schedule(record: dict[str, Any], on_date: date | None = None) -> dict[str, Any]:
    schedule = record.get("schedule") or {}
    phases = schedule.get("phases") or []
    if not phases:
        return schedule

    today = on_date or date.today()
    matches = []
    for phase in phases:
        start_raw = phase.get("effective_from")
        end_raw = phase.get("effective_through")
        start = date.fromisoformat(start_raw) if start_raw else None
        end = date.fromisoformat(end_raw) if end_raw else None
        if (start is None or today >= start) and (end is None or today <= end):
            matches.append(phase)
    if len(matches) != 1:
        raise SyncError(f"{record['slug']}: expected exactly one effective schedule phase for {today.isoformat()}; found {len(matches)}")
    active = dict(schedule)
    active.update(matches[0])
    return active


def format_time_compact(value: str) -> str:
    display = format_time(value)
    return display.replace(":00 ", " ")


def sync_seo(text: str, record: dict[str, Any], changes: list[str]) -> str:
    seo = record.get("seo") or {}
    mappings = [
        ("title", r"<title>.*?</title>", lambda v: f"<title>{v}</title>", re.S),
        ("meta_description", r'<meta name="description" content="[^"]*">', lambda v: f'<meta name="description" content="{v}">', 0),
        ("og_title", r'<meta property="og:title" content="[^"]*"\s*/?>', lambda v: f'<meta property="og:title" content="{v}" />', 0),
        ("og_description", r'<meta property="og:description" content="[^"]*"\s*/?>', lambda v: f'<meta property="og:description" content="{v}" />', 0),
    ]
    for field, pattern, render, flags in mappings:
        value = seo.get(field)
        if not value:
            continue
        new = replace_once(text, pattern, render(value), f"SEO {field}", flags)
        if new != text:
            changes.append(f"seo.{field}")
        text = new
    return text


def sync_affiliate_urls(text: str, record: dict[str, Any], changes: list[str]) -> str:
    ticketing = record.get("ticketing") or {}
    affiliate = ticketing.get("affiliate_url")
    if not affiliate:
        return text

    # Restrict replacement to Vegas Sidekick Spotlight referral URLs. This avoids
    # rewriting unrelated external links or editorial citations.
    slug = re.escape(str(record["slug"]))
    pattern = rf'https://spotlight\.vegas/shows/[^"\s<>]+/{slug}/ref/vegassidekick'
    new, count = re.subn(pattern, affiliate, text)
    if count:
        changes.append(f"ticketing.affiliate_url ({count} surface{'s' if count != 1 else ''})")
    return new


def sync_standard_visible_facts(text: str, record: dict[str, Any], changes: list[str]) -> str:
    pricing = record.get("pricing") or {}
    runtime = record.get("runtime") or {}

    price = pricing.get("from_price")
    if price is not None:
        new, found = replace_if_present(
            text,
            r'(class="check">)Starting at \$\d+(?:\.\d+)?\.',
            rf'\g<1>Starting at ${price}.',
            "starting-price note",
        )
        if found and new != text:
            changes.append("pricing.from_price note")
        text = new

        new, found = replace_if_present(
            text,
            r'(<div class="price"><small>From</small>\s*)\$\d+(?:\.\d+)?',
            rf'\g<1>${price}',
            "hero from-price",
        )
        if found and new != text:
            changes.append("pricing.from_price hero")
        text = new

    minutes = runtime.get("minutes")
    if minutes is not None:
        new, found = replace_if_present(
            text,
            r'About \d+ minutes, no intermission',
            f'About {minutes} minutes, no intermission',
            "runtime FAQ",
        )
        if found and new != text:
            changes.append("runtime.minutes")
        text = new

    return text


def sync_schedule_cards(text: str, record: dict[str, Any], changes: list[str]) -> str:
    schedule = effective_schedule(record)
    performances = schedule.get("performances") or []
    dark_days = set(schedule.get("dark_days") or [])
    if not performances and not dark_days:
        return text

    perf_by_day = {item["day"]: item["time"] for item in performances}
    updated = 0
    for day, abbr in DAY_ABBR.items():
        if day in perf_by_day:
            value = format_time(perf_by_day[day])
        elif day in dark_days:
            value = "Dark"
        else:
            continue
        patterns = [
            rf'(<div class="day[^>]*"><strong>{abbr}</strong><span>).*?(</span></div>)',
            rf'(<div class="day[^>]*>\s*<a[^>]*>\s*<strong>{abbr}</strong><span>).*?(</span>)',
        ]
        found_any = False
        for pattern in patterns:
            new, found = replace_if_present(text, pattern, rf'\g<1>{value}\g<2>', f"{day} schedule card")
            if found:
                found_any = True
                if new != text:
                    updated += 1
                text = new
                break
        if not found_any:
            continue
    if updated:
        changes.append(f"schedule cards ({updated})")
    return text


def sync_trailer(text: str, record: dict[str, Any], changes: list[str]) -> str:
    trailer = ((record.get("media") or {}).get("official_trailer") or {})
    video_id = trailer.get("video_id")
    if not video_id:
        return text

    before = text
    text = re.sub(r'(i\.ytimg\.com/vi/)[A-Za-z0-9_-]+/', rf'\g<1>{video_id}/', text)
    # Preserve the existing youtube.com vs youtube-nocookie.com host; only the ID is data-owned.
    text = re.sub(r'(https://www\.youtube(?:-nocookie)?\.com/embed/)[A-Za-z0-9_-]+', rf'\g<1>{video_id}', text)
    if text != before:
        changes.append("media.official_trailer.video_id")
    return text


def sync_explicit_visible_rules(text: str, record: dict[str, Any], changes: list[str]) -> str:
    """Apply narrow, opt-in presentation rules stored in the show record.

    These rules exist for facts whose surrounding prose differs by show. They
    keep page-specific wording out of the engine while making the ownership
    explicit and auditable in the source-of-truth record.
    """
    sync = record.get("sync") or {}

    schedule_rules = sync.get("schedule_text_rules") or []
    if schedule_rules:
        schedule = effective_schedule(record)
        times = sorted({item["time"] for item in schedule.get("performances") or []})
        if len(times) != 1:
            raise SyncError(f"{record['slug']}: schedule_text_rules require exactly one active showtime")
        tokens = {
            "time_compact": format_time_compact(times[0]),
            "time_display": format_time(times[0]),
        }
        for rule in schedule_rules:
            label = rule.get("label") or "schedule text rule"
            pattern = rule.get("pattern")
            replacement = rule.get("replacement")
            if not pattern or replacement is None:
                raise SyncError(f"{record['slug']}: {label} requires pattern and replacement")
            rendered = replacement.format(**tokens)
            new = replace_once(text, pattern, rendered, label)
            if new != text:
                changes.append(f"schedule text: {label}")
            text = new

    age_rule = sync.get("age_policy") or {}
    if age_rule.get("enabled"):
        policy = (record.get("age_policy") or {}).get("rule")
        question = age_rule.get("faq_question")
        suffix = age_rule.get("editorial_suffix", "")
        if not policy or not question:
            raise SyncError(f"{record['slug']}: sync.age_policy requires age_policy.rule and faq_question")
        replacement = policy + (f" {suffix}" if suffix else "")
        pattern = (
            rf'(<details class="faq-row"><summary>{re.escape(question)}</summary>'
            rf'<div class="faq-answer"><p>).*?(</p></div></details>)'
        )
        new = replace_once(text, pattern, rf'\g<1>{replacement}\g<2>', "age-policy FAQ")
        if new != text:
            changes.append("age_policy.rule")
        text = new

    return text


def sync_eventseries(text: str, record: dict[str, Any], changes: list[str]) -> str:
    structured = record.get("structured_data") or {}
    primary_type = structured.get("primary_type")
    if primary_type != "EventSeries":
        return text

    pricing = record.get("pricing") or {}
    ticketing = record.get("ticketing") or {}
    venue = record.get("venue") or {}
    schedule = effective_schedule(record)
    performances = schedule.get("performances") or []

    days = [item["day"] for item in performances]
    times = sorted({item["time"] for item in performances})
    if len(times) > 1:
        # EventSchedule only has one startTime in the current canonical pages.
        # Do not silently collapse multiple showtimes into incorrect schema.
        raise SyncError(f"{record['slug']}: EventSeries sync does not yet support multiple weekly start times")

    blocks = list(re.finditer(r'(<script type="application/ld\+json">)(.*?)(</script>)', text, re.S))
    replacements: list[tuple[int, int, str]] = []

    for match in blocks:
        raw = match.group(2).strip()
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError:
            # The site-wide schema audit will reject malformed blocks; the sync
            # engine never attempts to repair unknown/broken JSON by regex.
            continue
        if obj.get("@type") != "EventSeries":
            continue

        offers = obj.setdefault("offers", {"@type": "Offer"})
        if pricing.get("from_price") is not None:
            offers["price"] = pricing["from_price"]
        if pricing.get("currency"):
            offers["priceCurrency"] = pricing["currency"]
        if ticketing.get("affiliate_url"):
            offers["url"] = ticketing["affiliate_url"]

        location = obj.get("location")
        if isinstance(location, dict):
            if venue.get("schema_location_name"):
                location["name"] = venue["schema_location_name"]
            elif venue.get("showroom") and venue.get("hotel"):
                location["name"] = f"{venue['showroom']} at {venue['hotel']}"

        event_schedule = obj.get("eventSchedule")
        if isinstance(event_schedule, dict):
            if days and "byDay" in event_schedule:
                event_schedule["byDay"] = [f"https://schema.org/{day}" for day in days]
            if times and "startTime" in event_schedule:
                event_schedule["startTime"] = times[0]

        rendered = "\n" + json.dumps(obj, ensure_ascii=False, indent=2) + "\n"
        replacements.append((match.start(2), match.end(2), rendered))

    if len(replacements) != 1:
        raise SyncError(f"{record['slug']}: expected exactly one EventSeries JSON-LD block; found {len(replacements)}")

    start, end, rendered = replacements[0]
    new = text[:start] + rendered + text[end:]
    if new != text:
        changes.append("structured_data.EventSeries")
    return new


def sync_one(data_path: Path, dry_run: bool = False) -> tuple[Path, list[str]]:
    record = load_record(data_path)
    if record.get("status") != "active":
        raise SyncError(f"{record['slug']}: generic active-show sync only supports status=active")

    page = page_path_for(record)
    text = page.read_text(encoding="utf-8")
    original = text
    changes: list[str] = []

    text = sync_seo(text, record, changes)
    text = sync_affiliate_urls(text, record, changes)
    text = sync_standard_visible_facts(text, record, changes)
    text = sync_schedule_cards(text, record, changes)
    text = sync_explicit_visible_rules(text, record, changes)
    text = sync_trailer(text, record, changes)
    text = sync_eventseries(text, record, changes)

    if text != original and not dry_run:
        page.write_text(text, encoding="utf-8")

    return page, changes


def resolve_data_paths(args: argparse.Namespace) -> list[Path]:
    if args.all:
        return sorted(DATA_DIR.glob("*.json"))
    if args.data:
        path = Path(args.data)
        return [path if path.is_absolute() else ROOT / path]
    if args.slug:
        return [DATA_DIR / f"{args.slug}.json"]
    raise SyncError("Provide a show slug, --data PATH, or --all")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sync show pages from structured show records")
    parser.add_argument("slug", nargs="?", help="show slug, e.g. carrot-top")
    parser.add_argument("--data", help="path to a specific show JSON record")
    parser.add_argument("--all", action="store_true", help="sync every data/shows/*.json record")
    parser.add_argument("--dry-run", action="store_true", help="validate and report without writing files")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        paths = resolve_data_paths(args)
        if not paths:
            raise SyncError("No show data records found")
        for data_path in paths:
            page, changes = sync_one(data_path, dry_run=args.dry_run)
            rel_page = page.relative_to(ROOT)
            mode = "Would sync" if args.dry_run else "Synced"
            if changes:
                print(f"{mode} {rel_page} from {data_path.relative_to(ROOT)}")
                for item in changes:
                    print(f"  - {item}")
            else:
                print(f"{rel_page} already matches {data_path.relative_to(ROOT)}")
        return 0
    except SyncError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

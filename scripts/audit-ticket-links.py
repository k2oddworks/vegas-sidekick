#!/usr/bin/env python3
"""Fail on closed-show promotions and incorrect static ticket CTAs.

Offline audit. The show database is authoritative for active/closed status
and existing verified Spotlight affiliate URLs. No network calls or URL guessing.
"""
from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]
DATABASE = ROOT / "data" / "show-database.json"
EXCLUDE = {"_archive", "preview", "node_modules", ".git", "scripts", "hq"}
CTA_CLASSES = {"vs-ticket-primary", "vs-primary-book", "btn-tickets", "ticket-cta"}
PROMO_CLASSES = {"related-card", "show-card"}
CLOSED_LABEL = re.compile(r"^\s*(?:get|buy|book|find)\s+tickets?\b", re.I)
LOCAL_HOSTS = {"vegassidekick.com", "www.vegassidekick.com"}


class AnchorReader(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.current = None

    def handle_starttag(self, tag, attrs):
        if tag.lower() != "a":
            return
        attributes = dict(attrs)
        self.current = {
            "href": (attributes.get("href") or "").strip(),
            "classes": set((attributes.get("class") or "").split()),
            "text": "",
            "line": self.getpos()[0],
        }

    def handle_data(self, data):
        if self.current is not None:
            self.current["text"] += data

    def handle_endtag(self, tag):
        if tag.lower() == "a" and self.current is not None:
            self.links.append(self.current)
            self.current = None


def normalized_site_path(href: str) -> str | None:
    parsed = urlsplit(href)
    if parsed.scheme or parsed.netloc:
        if parsed.scheme not in {"http", "https"} or parsed.hostname not in LOCAL_HOSTS:
            return None
    elif not href.startswith("/"):
        return None
    path = unquote(parsed.path)
    return path.rstrip("/") + "/" if path else "/"


def is_ticket_cta(link: dict) -> bool:
    if link["classes"] & CTA_CLASSES:
        return True
    return bool(CLOSED_LABEL.search(link["text"].strip()))


def matches_affiliate(href: str, expected: str) -> bool:
    actual = urlsplit(href)
    stored = urlsplit(expected)
    return (
        actual.scheme == "https"
        and actual.hostname == stored.hostname == "spotlight.vegas"
        and actual.path.rstrip("/") == stored.path.rstrip("/")
        and actual.query == stored.query
    )


def main() -> int:
    data = json.loads(DATABASE.read_text(encoding="utf-8"))
    records = data["records"]
    active = {
        r["page_path"].rstrip("/") + "/": r
        for r in records if r.get("status") == "active" and r.get("page_path")
    }
    closed = {
        r["page_path"].rstrip("/") + "/": r
        for r in records if r.get("status") == "closed" and r.get("page_path")
    }
    errors = []
    pages = 0
    active_checked = 0
    primary_checked = 0

    for file in sorted(ROOT.rglob("*.html")):
        relative = file.relative_to(ROOT)
        if any(segment in EXCLUDE or segment.startswith(".") for segment in relative.parts):
            continue
        if file.name != "index.html":
            continue

        sitepath = "/" + relative.parent.as_posix().strip("./") + "/"
        if sitepath == "/./":
            sitepath = "/"
        source = relative.as_posix()
        reader = AnchorReader()
        reader.feed(file.read_text(encoding="utf-8", errors="replace"))
        pages += 1

        record = active.get(sitepath)
        is_archived_page = sitepath in closed
        if record:
            active_checked += 1
            expected = record.get("ticket_url") or ""
            if not expected or not matches_affiliate(expected, expected):
                errors.append(f"{source}: active record lacks canonical Spotlight affiliate URL")

        has_primary = False
        for link in reader.links:
            href = link["href"]
            target = normalized_site_path(href)
            label = link["text"].strip()
            ticket_cta = is_ticket_cta(link)
            promo = bool(link["classes"] & PROMO_CLASSES)

            if not is_archived_page and target in closed and (promo or ticket_cta):
                errors.append(
                    f"{source}:{link['line']}: promotes closed show "
                    f"{closed[target]['name']} ({href})"
                )

            if ticket_cta and (not href or href == "#" or href.lower().startswith("javascript:")):
                errors.append(f"{source}:{link['line']}: empty/placeholder ticket CTA")

            if ticket_cta and re.fullmatch(
                r"https?://(?:www\.)?(?:ticketmaster\.com|livenation\.com)/?", href, re.I
            ):
                errors.append(f"{source}:{link['line']}: ticket CTA goes to provider homepage")

            parsed = urlsplit(href)
            if parsed.hostname == "spotlight.vegas" and ticket_cta:
                if "/ref/vegassidekick" not in parsed.path:
                    errors.append(f"{source}:{link['line']}: Spotlight CTA lacks /ref/vegassidekick")
                if record and not matches_affiliate(href, record["ticket_url"]):
                    errors.append(f"{source}:{link['line']}: CTA differs from show's verified affiliate URL")
                if record:
                    has_primary = True
                    primary_checked += 1

            if record and link["classes"] & {"vs-ticket-primary", "vs-primary-book"}:
                if not matches_affiliate(href, record["ticket_url"]):
                    errors.append(f"{source}:{link['line']}: primary CTA is not the show's verified affiliate URL")

        if record and not has_primary:
            errors.append(f"{source}: no Spotlight purchase CTA matching its verified affiliate URL")

    for path, record in active.items():
        if not (ROOT / path.strip("/") / "index.html").is_file():
            errors.append(f"{path}: active show file is missing")

    print(
        f"Ticket-link audit: {pages} static pages; "
        f"{active_checked}/{len(active)} active shows; "
        f"{primary_checked} Spotlight ticket CTAs; {len(closed)} archived shows."
    )
    if errors:
        for error in errors:
            print("ERROR:", error)
        print(f"FAILED: {len(errors)} ticket/link problems.")
        return 1
    print("PASS: no stale closed-show cards, bad Spotlight CTAs, or placeholder ticket links found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

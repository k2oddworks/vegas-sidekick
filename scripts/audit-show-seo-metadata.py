#!/usr/bin/env python3
"""Check price-free show SEO metadata and evidence behind discount claims."""
from datetime import date
from html import unescape
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "show-database.json"
MAX_DISCOUNT_AGE_DAYS = 30
TITLE = re.compile(r"<title\b[^>]*>(.*?)</title>", re.I | re.S)
DESC_TAG = re.compile(r"<meta\b(?=[^>]*\bname=[\"']description[\"'])[^>]*>", re.I)
CONTENT = re.compile(r"\bcontent=([\"'])(.*?)\1", re.I | re.S)


def has_current_discount(record, today):
    amount = record.get("savings_amount")
    regular = record.get("regular_price")
    price = record.get("our_price")
    checked = record.get("price_source_last_checked_on")
    if not all(isinstance(x, (int, float)) for x in (amount, regular, price)):
        return False
    if amount < 5 or regular <= price or not checked:
        return False
    try:
        days = (today - date.fromisoformat(checked)).days
    except (TypeError, ValueError):
        return False
    return 0 <= days <= MAX_DISCOUNT_AGE_DAYS


def main():
    records = json.loads(DB.read_text(encoding="utf-8")).get("records", [])
    errors = []
    titles = {}
    active = 0
    deals = 0
    today = date.today()

    for rec in records:
        if rec.get("status") != "active":
            continue
        active += 1
        slug = rec["slug"]
        page = ROOT / rec["page_path"].strip("/") / "index.html"
        if not page.is_file():
            errors.append(f"{slug}: missing show page")
            continue
        markup = page.read_text(encoding="utf-8")
        title_match = TITLE.search(markup)
        desc_tag_match = DESC_TAG.search(markup)
        desc_match = CONTENT.search(desc_tag_match.group(0)) if desc_tag_match else None
        if not title_match or not desc_match:
            errors.append(f"{slug}: title or meta description is missing")
            continue

        title = unescape(title_match.group(1)).strip()
        desc = unescape(desc_match.group(2)).strip()
        is_deal = has_current_discount(rec, today)
        deals += bool(is_deal)
        title_type = "Discount Tickets" if is_deal else "Tickets & Showtimes"

        if "$" in title or "$" in desc:
            errors.append(f"{slug}: SEO metadata contains a dollar price")
        if title_type not in title:
            errors.append(f"{slug}: expected {title_type!r} in title")
        if "| Vegas Sidekick" not in title:
            errors.append(f"{slug}: title missing brand suffix")
        if not 85 <= len(desc) <= 170:
            errors.append(f"{slug}: description length {len(desc)} outside 85–170 chars")
        if not is_deal and re.search(r"\bdiscount(?:ed)?\b", title + " " + desc, re.I):
            errors.append(f"{slug}: unverified discount wording in metadata")
        if is_deal and "discount" not in desc.lower():
            errors.append(f"{slug}: discount title lacks corresponding deal description")
        if title in titles:
            errors.append(f"{slug}: duplicate title already used by {titles[title]}")
        else:
            titles[title] = slug

    print(f"SEO metadata checked: {active} active shows, {deals} verified discount titles")
    if errors:
        for error in errors:
            print("FAIL: " + error)
        return 1
    print("PASS: all active show titles and descriptions are price-free and discount claims are current")
    return 0


if __name__ == "__main__":
    sys.exit(main())

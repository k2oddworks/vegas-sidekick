#!/usr/bin/env python3
"""Check deal-list consistency and high-risk price/availability regressions."""
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
db = json.loads((ROOT / "data/show-database.json").read_text(encoding="utf-8"))
rows = {r["page_path"]: r for r in db["records"]}
issues = []
visible = (ROOT / "shows/deals/index.html").read_text(encoding="utf-8")
card_re = re.compile(r'<article class="deal-card[^"]*" data-save="(\d+)"><a href="([^"]+)">([\s\S]*?)</article>')
cards = list(card_re.finditer(visible))
found = set()
for card in cards:
    amount, path, body = int(card[1]), card[2], card[3]
    if path in found:
        issues.append(f"duplicate deals-page card: {path}")
        continue
    found.add(path)
    r = rows.get(path)
    if not r or r["status"] != "active" or not isinstance(r.get("regular_price"), (int, float)):
        issues.append(f"unqualified deals-page card: {path}")
        continue
    discount = round(r["regular_price"] - r["our_price"])
    pct = round(discount / r["regular_price"] * 100) if r["regular_price"] else 0
    if discount < db.get("deal_threshold_dollars", 5):
        issues.append(f"non-deal shown in catalog: {path}")
    if amount != discount or f"Save ${discount} · {pct}%" not in body:
        issues.append(f"incorrect savings on {path}")
    if f"<strong>${r['our_price']}</strong>" not in body or f"Regular ${r['regular_price']}" not in body:
        issues.append(f"incorrect price comparison on {path}")
expected = {r["page_path"] for r in db["records"]
            if r["status"] == "active" and isinstance(r.get("regular_price"), (int, float))
            and r["regular_price"] - r["our_price"] >= db.get("deal_threshold_dollars", 5)}
for path in sorted(expected - found):
    issues.append(f"qualified deal missing from catalog: {path}")
count_label = re.search(r'<div class="deal-count">(\d+) current discounted shows</div>', visible)
if not count_label or int(count_label[1]) != len(cards):
    issues.append("deals-page count does not match rendered cards")

cases = {
    "atomic-saloon": (100, None, None),
    "blue-man-group": (65, 74, 9),
    "tournament-of-kings": (78, 88, 10),
    "purple-reign": (51, 95, 44),
    "wayne-newton": (84, 121, 37),
    "magic-mike-live": (69, 87, 18),
    "thunder-from-down-under": (70, 71, None),
    "o": (121, None, None),
    "rupauls-drag-race-live": (55, 82, 27),
    "v-the-ultimate-variety-show": (41, 101, 60),
    "tape-face": (57, 71, 14),
    "ka": (80, None, None),
}
for slug, (price, regular, save) in cases.items():
    record = next(r for r in db["records"] if r["slug"] == slug)
    html = (ROOT / record["page_path"].lstrip("/") / "index.html").read_text(encoding="utf-8")
    if record["our_price"] != price or record["regular_price"] != regular:
        issues.append(f"{slug}: database price mismatch")
    if record["spotlight"]["our_price"] != price or record["spotlight"]["regular_price"] != regular:
        issues.append(f"{slug}: nested Spotlight source snapshot mismatch")
    if record.get("is_deal") != (save is not None) or record.get("savings_amount") != save:
        issues.append(f"{slug}: recorded deal threshold/savings mismatch")
    if f'<small>Tickets from</small>${price}' not in html:
        issues.append(f"{slug}: hero starting price mismatch")
    sticky_old = f'<small>FROM</small>${price}'
    sticky_green = f'<small>FROM</small><span class="vs-mobile-price-amount">${price}</span>'
    if sticky_old not in html and sticky_green not in html:
        issues.append(f"{slug}: mobile sticky price mismatch")
    if f"Starting at ${price}" not in html and f"Tickets start at ${price}" not in html:
        issues.append(f"{slug}: final purchase starting price mismatch")
    if save is None:
        if 'vs-deal-line' in html or record.get("is_deal"):
            issues.append(f"{slug}: unsupported deal presentation")
    else:
        badge_old = f'Regular ${regular}</span><span class="vs-save-badge">Save ${save}</span>'
        badge_green = (f'<span class="vs-save-badge">Save ${save} on starting tickets</span>'
                       f'<span class="vs-regular-price">Regular ${regular}</span>')
        if badge_old not in html and badge_green not in html:
            issues.append(f"{slug}: hero savings calculation mismatch")

live = next(r for r in db["records"] if r["slug"] == "las-vegas-live-comedy-club")
html = (ROOT / live["page_path"].lstrip("/") / "index.html").read_text(encoding="utf-8")
if live["status"] != "needs_review" or live["our_price"] != 29 or live["regular_price"] is not None:
    issues.append("Las Vegas LIVE: ticketing hold/database mismatch")
if "Tickets currently unavailable" not in html or 'https://schema.org/OutOfStock' not in html:
    issues.append("Las Vegas LIVE: unavailable status not visible/structured")
if re.search(r'<a[^>]*href="https://spotlight.vegas/shows/comedy/las-vegas-live-comedy-club/', html):
    issues.append("Las Vegas LIVE: bookable affiliate button still exposed")
if 'data-ticket-url=' in html or 'class="mobile-bar"' in html:
    issues.append("Las Vegas LIVE: booking widget or mobile ticket bar still enabled")
if live["page_path"] in found:
    issues.append("Las Vegas LIVE: not-bookable show listed as deal")

if issues:
    print("Price reconciliation audit FAILED:")
    for issue in issues:
        print(" - " + issue)
    sys.exit(1)
print(f"Price reconciliation audit passed: {len(cards)} verified deals; all monitored price discrepancies guarded.")

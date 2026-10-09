#!/usr/bin/env python3
"""Validate approved final-page savings treatment against the show database."""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
db = json.loads((ROOT / "data/show-database.json").read_text())
stage_one = {"piano-man", "all-motown", "america-the-show",
             "zombie-burlesque", "v-the-ultimate-variety-show",
             "the-mentalist", "paranormal", "tape-face"}
stage_two = {"king-of-diamonds", "wastin-away", "penn-and-teller", "ka",
             "vegas-the-show", "mj-live", "motown-brunch", "shin-lim"}
stage_three = {"purple-reign"}
issues = []
checked = []
for record in db["records"]:
    if record.get("status") != "active":
        continue
    page = ROOT / record.get("page_path", "").lstrip("/") / "index.html"
    if not page.is_file():
        continue
    html = page.read_text(encoding="utf-8")
    if "vs-final-savings-section" not in html:
        continue
    slug = record["slug"]
    a, b = record.get("our_price"), record.get("regular_price")
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)) or b <= a or b - a < 20:
        issues.append(f"{slug}: insufficient or absent price comparison")
        continue
    save = round(b - a)
    pct = round(save / b * 100)
    expected = [
        f"Save ${save} · {pct}%",
        f"On starting tickets · ${a:g} instead of ${b:g} regular",
        f'class="vs-mobile-save">Save ${save}',
        f"Save ${save} on starting tickets",
    ]
    for token in expected:
        if token not in html:
            issues.append(f"{slug}: missing or outdated {token!r}")
    if html.count('class="vs-final-savings"') != 1:
        issues.append(f"{slug}: final savings banner must occur once")
    start = html.index("vs-final-savings-section")
    section = html[start:html.find("</section>", start)]
    banner = section.find('class="vs-final-savings"')
    cta = section.find('class="cta vs-ticket-primary"')
    if banner < 0 or cta < banner:
        issues.append(f"{slug}: final banner must precede amber CTA")
    if record.get("ticket_url") not in section:
        issues.append(f"{slug}: final CTA affiliate URL mismatch")
    if "vs-savings-pilot" not in html.split("<body", 1)[1].split(">", 1)[0]:
        issues.append(f"{slug}: missing hero savings style class")
    checked.append(slug)

for slug in stage_one | stage_two | stage_three | {"all-shook-up"}:
    if slug not in checked:
        issues.append(f"{slug}: required final savings treatment missing")

if issues:
    print("Final savings audit FAILED")
    for issue in issues:
        print(" - " + issue)
    sys.exit(1)
print(f"Final savings audit passed for {len(checked)} pages: " + ", ".join(sorted(checked)))

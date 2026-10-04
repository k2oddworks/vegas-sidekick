#!/usr/bin/env python3
"""Audit the internal HQ Media Library implementation."""
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "hq" / "media-library" / "index.html"
APP = ROOT / "hq" / "media-library" / "app.js"
CSS = ROOT / "hq" / "media-library" / "style.css"
SITEMAP = ROOT / "sitemap.xml"
HEADERS = ROOT / "_headers"

issues = []

for path in (PAGE, APP, CSS):
    if not path.exists():
        issues.append(f"missing Media Library file: {path.relative_to(ROOT)}")

if PAGE.exists():
    text = PAGE.read_text(encoding="utf-8", errors="replace")
    if not re.search(r'<meta[^>]+name=["\']robots["\'][^>]+content=["\'][^"\']*noindex[^"\']*nofollow', text, re.I):
        issues.append("Media Library page is missing noindex,nofollow meta robots")
    for required in ("media-grid", "media-search", "show-filter", "venue-filter", "category-filters"):
        if f'id="{required}"' not in text:
            issues.append(f"Media Library page missing required UI id: {required}")

if SITEMAP.exists() and "/hq/media-library" in SITEMAP.read_text(encoding="utf-8", errors="replace"):
    issues.append("Media Library must not appear in sitemap.xml")

if HEADERS.exists():
    headers = HEADERS.read_text(encoding="utf-8", errors="replace")
    if "/hq/*" not in headers or "X-Robots-Tag: noindex, nofollow, noarchive" not in headers:
        issues.append("/hq/* noindex response header is missing")
else:
    issues.append("_headers file is missing")

# Keep the tool out of normal public navigation and public-facing pages.
for path in ROOT.rglob("*"):
    if not path.is_file() or path.suffix.lower() not in {".html", ".js"}:
        continue
    rel = path.relative_to(ROOT)
    if rel.parts and rel.parts[0] in {"hq", "admin", "docs", "scripts", ".github"}:
        continue
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        continue
    if "/hq/media-library" in text:
        issues.append(f"public file links to internal Media Library: {rel.as_posix()}")

generator = ROOT / "scripts" / "generate-media-library.py"
if generator.exists():
    proc = subprocess.run(
        [sys.executable, str(generator), "--check"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    print(proc.stdout, end="")
    if proc.returncode:
        print(proc.stderr, end="")
        issues.append("media inventory generator validation failed")
else:
    issues.append("scripts/generate-media-library.py is missing")

if issues:
    print("Media Library audit FAILED")
    for issue in issues:
        print(" -", issue)
    raise SystemExit(1)

print("PASS — Media Library is internal, unindexed, generated, and structurally valid.")

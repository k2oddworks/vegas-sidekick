#!/usr/bin/env python3
"""Audit the Vegas Sidekick image-library migration and ongoing root-folder rule."""
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
IMAGES = ROOT / "images"
MANIFEST = ROOT / "docs" / "image-library-migration-2026-10-04.json"
REDIRECTS = ROOT / "_redirects"
IMAGE_EXT = re.compile(r"\.(?:jpe?g|png|webp|gif|svg)$", re.I)
TEXT_EXTENSIONS = {
    ".html", ".htm", ".css", ".js", ".mjs", ".json", ".md", ".xml",
    ".txt", ".py", ".yml", ".yaml", ".toml", ".ini", ".csv"
}
TEXT_FILENAMES = {"_redirects", "_headers", "robots.txt", "wrangler.toml"}
ALLOWED_TOP_LEVEL_DIRS = {
    "brand", "good-to-know", "guides", "misc", "news", "oddworks-digital",
    "play", "podcast", "product-photos", "seating-charts", "sidekick-index",
    "site", "venue-photos"
}

issues = []

root_images = sorted(
    p.relative_to(ROOT).as_posix()
    for p in IMAGES.iterdir()
    if p.is_file() and IMAGE_EXT.search(p.name)
)
if root_images:
    issues.append(
        f"{len(root_images)} image asset(s) still live directly in /images/: "
        + ", ".join(root_images[:12])
    )

unexpected_dirs = sorted(
    p.name for p in IMAGES.iterdir()
    if p.is_dir() and p.name not in ALLOWED_TOP_LEVEL_DIRS
)
if unexpected_dirs:
    issues.append(
        "unexpected top-level /images folder(s): " + ", ".join(unexpected_dirs)
    )

moves = []
if MANIFEST.exists():
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    moves = data.get("moves", [])
    if data.get("moved_count") != len(moves):
        issues.append(
            f"manifest moved_count is {data.get('moved_count')} but contains {len(moves)} moves"
        )

    redirect_lines = set()
    if REDIRECTS.exists():
        redirect_lines = {
            line.strip()
            for line in REDIRECTS.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        }

    for move in moves:
        old = ROOT / move["from"]
        new = ROOT / move["to"]
        if old.exists():
            issues.append(f"legacy source still exists: {move['from']}")
        if not new.exists():
            issues.append(f"migrated destination missing: {move['to']}")
        expected_redirect = f"/{move['from']} /{move['to']} 301"
        if expected_redirect not in redirect_lines:
            issues.append(f"redirect map missing: {expected_redirect}")

    # A migrated legacy URL may remain only in the redirect map or migration manifest.
    old_urls = {"/" + move["from"] for move in moves}
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if ".github" in path.parts and "workflows" in path.parts:
            continue
        if path in {MANIFEST, ROOT / "_redirects"}:
            continue
        if path.suffix.lower() not in TEXT_EXTENSIONS and path.name not in TEXT_FILENAMES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for old_url in old_urls:
            if old_url in text:
                issues.append(f"{path.relative_to(ROOT)} still references legacy path {old_url}")
else:
    # Before the one-time migration has run, only enforce the root-folder rule.
    if not root_images:
        issues.append("migration manifest is missing")

print("Image library audit")
print(f"Root image files: {len(root_images)}")
print(f"Manifest moves checked: {len(moves)}")
print(f"Unexpected top-level folders: {len(unexpected_dirs)}")
if issues:
    print("FAILED")
    for issue in issues[:100]:
        print(" -", issue)
    if len(issues) > 100:
        print(f" - ... {len(issues)-100} more")
    sys.exit(1)

print("PASS — migrated images are organized and legacy references are redirected only.")

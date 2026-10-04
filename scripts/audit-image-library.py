#!/usr/bin/env python3
"""Audit the Vegas Sidekick image-library migration and ongoing root-folder rule."""
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
IMAGES = ROOT / "images"
MANIFEST = ROOT / "docs" / "image-library-migration-2026-10-04.json"
IMAGE_EXT = re.compile(r"\.(?:jpe?g|png|webp|gif|svg)$", re.I)
TEXT_EXTENSIONS = {
    ".html", ".htm", ".css", ".js", ".mjs", ".json", ".md", ".xml",
    ".txt", ".py", ".yml", ".yaml", ".toml", ".ini", ".csv"
}
TEXT_FILENAMES = {"_redirects", "_headers", "robots.txt", "wrangler.toml"}

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

moves = []
if MANIFEST.exists():
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    moves = data.get("moves", [])
    for move in moves:
        old = ROOT / move["from"]
        new = ROOT / move["to"]
        if old.exists():
            issues.append(f"legacy source still exists: {move['from']}")
        if not new.exists():
            issues.append(f"migrated destination missing: {move['to']}")

    # A migrated legacy URL may remain only in the redirect map or migration manifest.
    old_urls = {"/" + move["from"] for move in moves}
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
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
if issues:
    print("FAILED")
    for issue in issues[:100]:
        print(" -", issue)
    if len(issues) > 100:
        print(f" - ... {len(issues)-100} more")
    sys.exit(1)

print("PASS — migrated images are organized and legacy references are redirected only.")

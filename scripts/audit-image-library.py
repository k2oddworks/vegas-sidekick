#!/usr/bin/env python3
"""Audit Vegas Sidekick image library organization and local image references."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
IMAGES = ROOT / "images"
IMAGE_EXT = re.compile(r"\.(?:jpe?g|png|webp|gif|svg)$", re.I)
REF = re.compile(r"""(?P<url>/images/[^"'<>\s)]+\.(?:jpe?g|png|webp|gif|svg))""", re.I)

issues = []

root_images = sorted(
    p.relative_to(ROOT).as_posix()
    for p in IMAGES.iterdir()
    if p.is_file() and IMAGE_EXT.search(p.name)
)
if root_images:
    issues.append(f"{len(root_images)} image asset(s) still live directly in /images/: " + ", ".join(root_images[:12]))

for path in ROOT.rglob("*"):
    if not path.is_file() or ".git" in path.parts:
        continue
    if path.suffix.lower() not in {".html",".css",".js",".json",".md",".xml",".txt",".py",".yml",".yaml"} and path.name not in {"_redirects","_headers"}:
        continue
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        continue
    for match in REF.finditer(text):
        url = match.group("url").split("?",1)[0].split("#",1)[0]
        target = ROOT / url.lstrip("/")
        # Redirect source lines intentionally reference removed legacy paths.
        if path.name == "_redirects":
            continue
        if not target.exists():
            issues.append(f"{path.relative_to(ROOT)}: missing local image {url}")

print("Image library audit")
print(f"Root image files: {len(root_images)}")
if issues:
    print("FAILED")
    for issue in issues[:100]:
        print(" -", issue)
    if len(issues) > 100:
        print(f" - ... {len(issues)-100} more")
    sys.exit(1)
print("PASS — image assets are organized and referenced local files exist.")

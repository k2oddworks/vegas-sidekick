#!/usr/bin/env python3
"""Generate the read-only Vegas Sidekick HQ Media Library inventory."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import struct
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
IMAGES = ROOT / "images"
DEFAULT_OUTPUT = ROOT / "hq" / "media-library" / "media-library.json"
BASE_URL = "https://vegassidekick.com"
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg", ".avif"}
PUBLIC_TEXT_EXTS = {".html", ".htm", ".css", ".js", ".mjs", ".json", ".xml"}
EXCLUDED_SCAN_DIRS = {".git", ".github", "admin", "docs", "hq", "images", "node_modules", "scripts"}
IMAGE_REF_RE = re.compile(
    r"(?:https://vegassidekick\.com)?(/images/[A-Za-z0-9._/%-]+\.(?:jpe?g|png|webp|gif|svg|avif))",
    re.I,
)
TAG_RE = re.compile(r"<[^>]+>")


def clean_label(value: str) -> str:
    value = html.unescape(TAG_RE.sub("", value)).strip()
    value = re.sub(r"\s+", " ", value)
    return value


def page_label(path: Path, fallback: str) -> str:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return fallback.replace("-", " ").title()
    m = re.search(r"<h1[^>]*>(.*?)</h1>", text, re.I | re.S)
    if m:
        label = clean_label(m.group(1))
        if label:
            return label
    m = re.search(r"<title[^>]*>(.*?)</title>", text, re.I | re.S)
    if m:
        label = clean_label(m.group(1)).split("|")[0].strip()
        if label:
            return label
    return fallback.replace("-", " ").title()


def build_entity_maps():
    shows = {}
    show_root = ROOT / "shows"
    if show_root.exists():
        for page in show_root.glob("*/*/index.html"):
            rel = page.relative_to(ROOT).as_posix()
            parts = rel.split("/")
            if len(parts) >= 4:
                slug = parts[2]
                shows[slug] = {
                    "name": page_label(page, slug),
                    "url": "/" + "/".join(parts[:3]) + "/",
                    "file": rel,
                }

    venues = {}
    venue_root = ROOT / "venues"
    if venue_root.exists():
        for page in venue_root.glob("*/index.html"):
            rel = page.relative_to(ROOT).as_posix()
            parts = rel.split("/")
            if len(parts) >= 3:
                slug = parts[1]
                venues[slug] = {
                    "name": page_label(page, slug),
                    "url": f"/venues/{slug}/",
                    "file": rel,
                }
    return shows, venues


def iter_public_text_files():
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        if any(part in EXCLUDED_SCAN_DIRS for part in rel.parts[:-1]):
            continue
        if path.suffix.lower() not in PUBLIC_TEXT_EXTS:
            continue
        yield path


def scan_references():
    ref_files = defaultdict(set)
    ref_occurrences = defaultdict(int)
    contextual_usage = defaultdict(set)
    show_refs = defaultdict(set)
    venue_refs = defaultdict(set)

    for path in iter_public_text_files():
        rel = path.relative_to(ROOT).as_posix()
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        show_slug = None
        venue_slug = None
        parts = rel.split("/")
        if len(parts) >= 4 and parts[0] == "shows" and parts[-1] == "index.html":
            show_slug = parts[2]
        if len(parts) >= 3 and parts[0] == "venues" and parts[-1] == "index.html":
            venue_slug = parts[1]

        for match in IMAGE_REF_RE.finditer(text):
            image_path = match.group(1)
            ref_files[image_path].add(rel)
            ref_occurrences[image_path] += 1
            if show_slug:
                show_refs[image_path].add(show_slug)
            if venue_slug:
                venue_refs[image_path].add(venue_slug)

            snippet = text[max(0, match.start() - 180): min(len(text), match.end() + 180)].lower()
            if "og:image" in snippet or "twitter:image" in snippet:
                contextual_usage[image_path].add("OG/social")
            if "hero" in snippet:
                contextual_usage[image_path].add("Hero")
            if "gallery" in snippet or "lightbox" in snippet:
                contextual_usage[image_path].add("Gallery")

    return ref_files, ref_occurrences, contextual_usage, show_refs, venue_refs


def png_dimensions(data: bytes):
    if len(data) >= 24 and data.startswith(b"\x89PNG\r\n\x1a\n"):
        return struct.unpack(">II", data[16:24])
    return None


def gif_dimensions(data: bytes):
    if len(data) >= 10 and data[:6] in (b"GIF87a", b"GIF89a"):
        return struct.unpack("<HH", data[6:10])
    return None


def jpeg_dimensions(data: bytes):
    if len(data) < 4 or data[:2] != b"\xff\xd8":
        return None
    i = 2
    sof = {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}
    while i + 3 < len(data):
        while i < len(data) and data[i] != 0xFF:
            i += 1
        while i < len(data) and data[i] == 0xFF:
            i += 1
        if i >= len(data):
            break
        marker = data[i]
        i += 1
        if marker in (0xD8, 0xD9):
            continue
        if i + 2 > len(data):
            break
        length = struct.unpack(">H", data[i:i + 2])[0]
        if length < 2 or i + length > len(data):
            break
        if marker in sof and i + 7 <= len(data):
            height, width = struct.unpack(">HH", data[i + 3:i + 7])
            return width, height
        i += length
    return None


def webp_dimensions(data: bytes):
    if len(data) < 30 or data[:4] != b"RIFF" or data[8:12] != b"WEBP":
        return None
    chunk = data[12:16]
    payload = data[20:]
    if chunk == b"VP8X" and len(payload) >= 10:
        width = 1 + int.from_bytes(payload[4:7], "little")
        height = 1 + int.from_bytes(payload[7:10], "little")
        return width, height
    if chunk == b"VP8 " and len(payload) >= 10 and payload[3:6] == b"\x9d\x01\x2a":
        width = int.from_bytes(payload[6:8], "little") & 0x3FFF
        height = int.from_bytes(payload[8:10], "little") & 0x3FFF
        return width, height
    if chunk == b"VP8L" and len(payload) >= 5 and payload[0] == 0x2F:
        b1, b2, b3, b4 = payload[1:5]
        width = 1 + b1 + ((b2 & 0x3F) << 8)
        height = 1 + (b2 >> 6) + (b3 << 2) + ((b4 & 0x0F) << 10)
        return width, height
    return None


def svg_dimensions(path: Path):
    try:
        root = ET.parse(path).getroot()
    except Exception:
        return None

    def number(value):
        if not value:
            return None
        m = re.match(r"\s*([0-9.]+)", value)
        return float(m.group(1)) if m else None

    width = number(root.attrib.get("width"))
    height = number(root.attrib.get("height"))
    if width and height:
        return int(round(width)), int(round(height))

    viewbox = root.attrib.get("viewBox") or root.attrib.get("viewbox")
    if viewbox:
        vals = re.split(r"[\s,]+", viewbox.strip())
        if len(vals) == 4:
            try:
                return int(round(float(vals[2]))), int(round(float(vals[3])))
            except ValueError:
                pass
    return None


def image_dimensions(path: Path):
    ext = path.suffix.lower()
    if ext == ".svg":
        return svg_dimensions(path)
    try:
        data = path.read_bytes()
    except OSError:
        return None
    if ext == ".png":
        return png_dimensions(data)
    if ext == ".gif":
        return gif_dimensions(data)
    if ext in {".jpg", ".jpeg"}:
        return jpeg_dimensions(data)
    if ext == ".webp":
        return webp_dimensions(data)
    return None


def classify(rel: str, contextual):
    parts = rel.split("/")
    bucket = parts[1] if len(parts) > 1 else "other"
    filename = parts[-1]
    stem = Path(filename).stem.lower()
    labels = set(contextual)

    if bucket == "product-photos":
        category = "product-photos"
        if "hero" in stem:
            labels.add("Hero")
        elif re.search(r"(?:^|[-_])(og|social)(?:[-_]|$)", stem):
            labels.add("OG/social")
        else:
            labels.add("Gallery")
    elif bucket == "seating-charts":
        category = "seating-charts"
        labels.add("Seating chart")
    elif bucket == "venue-photos":
        category = "venue-photos"
        labels.add("Venue")
        if re.search(r"(?:^|[-_])(og|social)(?:[-_]|$)", stem):
            labels.add("OG/social")
    elif bucket == "news":
        category = "news"
        labels.add("Dispatch/news")
        if re.search(r"(?:^|[-_])(og|social)(?:[-_]|$)", stem):
            labels.add("OG/social")
    elif bucket == "good-to-know":
        category = "good-to-know"
        labels.add("Good to Know")
    elif bucket in {"brand", "site"}:
        category = "brand-site"
        labels.add("Brand/site asset")
        if re.search(r"(?:^|[-_])(og|social)(?:[-_]|$)", stem):
            labels.add("OG/social")
    else:
        category = "other"
        labels.add("Other")

    ordered = [
        x for x in (
            "Hero", "Gallery", "Seating chart", "OG/social", "Venue",
            "Dispatch/news", "Good to Know", "Brand/site asset", "Other"
        ) if x in labels
    ]
    return category, ordered


def build_inventory():
    shows, venues = build_entity_maps()
    ref_files, ref_occ, contextual, show_refs, venue_refs = scan_references()

    items = []
    hashes = defaultdict(list)
    same_basename = defaultdict(list)

    for path in sorted(p for p in IMAGES.rglob("*") if p.is_file() and p.suffix.lower() in IMAGE_EXTS):
        rel = path.relative_to(ROOT).as_posix()
        public_path = "/" + rel
        data = path.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        dims = image_dimensions(path)
        category, usage = classify(rel, contextual.get(public_path, set()))

        parts = rel.split("/")
        bucket = parts[1] if len(parts) > 1 else ""
        owner_slug = parts[2] if len(parts) > 2 else None

        show = None
        related_show_url = None
        if bucket == "product-photos" and owner_slug:
            info = shows.get(owner_slug)
            show = info["name"] if info else owner_slug.replace("-", " ").title()
            related_show_url = info["url"] if info else None
        else:
            referenced_shows = sorted(show_refs.get(public_path, set()))
            if len(referenced_shows) == 1:
                slug = referenced_shows[0]
                info = shows.get(slug)
                if info:
                    show = info["name"]
                    related_show_url = info["url"]

        venue = None
        related_venue_url = None
        if bucket == "venue-photos" and owner_slug:
            info = venues.get(owner_slug)
            venue = info["name"] if info else owner_slug.replace("-", " ").title()
            related_venue_url = info["url"] if info else None
        else:
            referenced_venues = sorted(venue_refs.get(public_path, set()))
            if len(referenced_venues) == 1:
                slug = referenced_venues[0]
                info = venues.get(slug)
                if info:
                    venue = info["name"]
                    related_venue_url = info["url"]

        item = {
            "filename": path.name,
            "path": public_path,
            "publicUrl": BASE_URL + public_path,
            "width": dims[0] if dims else None,
            "height": dims[1] if dims else None,
            "fileType": path.suffix.lower().lstrip("."),
            "sizeBytes": len(data),
            "category": category,
            "usage": usage,
            "show": show,
            "venue": venue,
            "relatedShowUrl": related_show_url,
            "relatedVenueUrl": related_venue_url,
            "referenced": bool(ref_files.get(public_path)),
            "referenceCount": len(ref_files.get(public_path, set())),
            "referenceOccurrences": ref_occ.get(public_path, 0),
            "referenceFiles": sorted(ref_files.get(public_path, set()))[:25],
            "sha256": digest,
            "duplicateHints": [],
        }
        items.append(item)
        hashes[digest].append(item)
        same_basename[(str(path.parent.relative_to(ROOT)).lower(), path.stem.lower())].append(item)

    exact_groups = 0
    same_base_groups = 0
    hero_format_groups = 0

    for group in hashes.values():
        if len(group) > 1:
            exact_groups += 1
            for item in group:
                item["duplicateHints"].append(f"Exact duplicate of {len(group) - 1} other file(s)")

    for (_, stem), group in same_basename.items():
        formats = {item["fileType"] for item in group}
        if len(group) > 1 and len(formats) > 1:
            same_base_groups += 1
            for item in group:
                item["duplicateHints"].append("Same basename exists in multiple formats")
            if stem.endswith("-hero") or stem == "hero":
                hero_format_groups += 1
                for item in group:
                    item["duplicateHints"].append("Hero has multiple format versions")

    used = sum(1 for item in items if item["referenced"])
    summary = {
        "totalImages": len(items),
        "usedImages": used,
        "unreferencedImages": len(items) - used,
        "exactDuplicateGroups": exact_groups,
        "sameBasenameFormatGroups": same_base_groups,
        "heroMultiFormatGroups": hero_format_groups,
    }
    return {
        "schemaVersion": 1,
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "baseUrl": BASE_URL,
        "summary": summary,
        "images": items,
    }


def validate(payload):
    issues = []
    disk_paths = {
        "/" + p.relative_to(ROOT).as_posix()
        for p in IMAGES.rglob("*")
        if p.is_file() and p.suffix.lower() in IMAGE_EXTS
    }
    payload_paths = {item["path"] for item in payload["images"]}

    if disk_paths != payload_paths:
        missing = sorted(disk_paths - payload_paths)
        extra = sorted(payload_paths - disk_paths)
        if missing:
            issues.append(f"inventory missing {len(missing)} image(s): {missing[:5]}")
        if extra:
            issues.append(f"inventory has {len(extra)} stale image path(s): {extra[:5]}")

    valid_categories = {"product-photos", "seating-charts", "venue-photos", "news", "good-to-know", "brand-site", "other"}
    for item in payload["images"]:
        if item["category"] not in valid_categories:
            issues.append(f"invalid category for {item['path']}: {item['category']}")
        if not (ROOT / item["path"].lstrip("/")).exists():
            issues.append(f"missing image path: {item['path']}")

    encoded = json.dumps(payload, ensure_ascii=False)
    json.loads(encoded)
    return issues


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true", help="Generate and validate in memory without writing output")
    args = parser.parse_args()

    payload = build_inventory()
    issues = validate(payload)
    if issues:
        print("Media Library inventory FAILED")
        for issue in issues[:50]:
            print(" -", issue)
        raise SystemExit(1)

    summary = payload["summary"]
    print(
        "Media Library inventory:"
        f" {summary['totalImages']} images,"
        f" {summary['usedImages']} referenced,"
        f" {summary['unreferencedImages']} with no current references"
    )
    print(
        "Duplicate hints:"
        f" {summary['exactDuplicateGroups']} exact groups,"
        f" {summary['sameBasenameFormatGroups']} same-basename format groups"
    )

    if args.check:
        print("PASS — inventory generated and validated in memory.")
        return

    output = args.output
    if not output.is_absolute():
        output = ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

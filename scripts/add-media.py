#!/usr/bin/env python3
"""Vegas Sidekick media ingestion utility.

Copies an approved local image into the repo without recompressing it, validates
its signature/dimensions, creates a predictable web-safe filename, and verifies
the copied bytes with SHA-256. This intentionally does not optimize or redraw
source media; derivatives should be a separate explicit step.

Examples:
  python3 scripts/add-media.py ~/Downloads/oasis.jpg --dest images/news --name oasis-live-27-hero
  python3 scripts/add-media.py seat-map.png --dest images/shows/criss-angel --name seating-chart --force
"""
from __future__ import annotations

import argparse
import hashlib
import re
import shutil
import struct
import sys
from pathlib import Path

ALLOWED = {".jpg", ".jpeg", ".png", ".webp", ".gif"}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def image_info(path: Path) -> tuple[str, int, int]:
    data = path.read_bytes()
    if data.startswith(b"\x89PNG\r\n\x1a\n") and len(data) >= 24:
        w, h = struct.unpack(">II", data[16:24])
        return "png", w, h
    if data[:3] == b"\xff\xd8\xff":
        i = 2
        while i + 9 < len(data):
            if data[i] != 0xFF:
                i += 1
                continue
            marker = data[i + 1]
            i += 2
            if marker in (0xD8, 0xD9):
                continue
            if i + 2 > len(data):
                break
            length = int.from_bytes(data[i:i+2], "big")
            if marker in {0xC0,0xC1,0xC2,0xC3,0xC5,0xC6,0xC7,0xC9,0xCA,0xCB,0xCD,0xCE,0xCF} and i + 7 < len(data):
                h = int.from_bytes(data[i+3:i+5], "big")
                w = int.from_bytes(data[i+5:i+7], "big")
                return "jpeg", w, h
            if length < 2:
                break
            i += length
    if data.startswith(b"RIFF") and data[8:12] == b"WEBP":
        # Pillow is intentionally not required. Validate WebP signature; report
        # dimensions only when the simple VP8X extended header is present.
        if data[12:16] == b"VP8X" and len(data) >= 30:
            w = 1 + int.from_bytes(data[24:27], "little")
            h = 1 + int.from_bytes(data[27:30], "little")
            return "webp", w, h
        return "webp", 0, 0
    if data.startswith((b"GIF87a", b"GIF89a")) and len(data) >= 10:
        w, h = struct.unpack("<HH", data[6:10])
        return "gif", w, h
    raise ValueError("file signature is not a supported image")


def main() -> int:
    p = argparse.ArgumentParser(description="Safely ingest approved media into Vegas Sidekick")
    p.add_argument("source", type=Path, help="local source image")
    p.add_argument("--dest", required=True, type=Path, help="repo-relative destination directory")
    p.add_argument("--name", help="destination basename without extension")
    p.add_argument("--force", action="store_true", help="replace an existing destination file")
    p.add_argument("--min-width", type=int, default=0, help="fail when image is narrower")
    args = p.parse_args()

    source = args.source.expanduser().resolve()
    if not source.is_file():
        p.error(f"source does not exist: {source}")
    ext = source.suffix.lower()
    if ext not in ALLOWED:
        p.error(f"unsupported extension {ext}; allowed: {', '.join(sorted(ALLOWED))}")

    try:
        kind, width, height = image_info(source)
    except ValueError as e:
        p.error(str(e))
    if args.min_width and width and width < args.min_width:
        p.error(f"image is {width}px wide; minimum is {args.min_width}px")

    repo = Path(__file__).resolve().parent.parent
    dest_dir = (repo / args.dest).resolve()
    try:
        dest_dir.relative_to(repo)
    except ValueError:
        p.error("--dest must stay inside the repository")

    basename = slugify(args.name or source.stem)
    if not basename:
        p.error("destination name is empty after slugification")
    # Normalize jpeg extension while otherwise preserving the source format.
    out_ext = ".jpg" if kind == "jpeg" else f".{kind}"
    target = dest_dir / f"{basename}{out_ext}"
    if target.exists() and not args.force:
        p.error(f"destination exists: {target.relative_to(repo)} (use --force to replace)")

    before = sha256(source)
    dest_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    after = sha256(target)
    if before != after:
        target.unlink(missing_ok=True)
        p.error("verification failed: copied bytes do not match source")

    rel = target.relative_to(repo).as_posix()
    dims = f"{width}x{height}" if width and height else "dimensions unavailable"
    print(f"OK  {rel}")
    print(f"    type={kind} dimensions={dims} bytes={target.stat().st_size}")
    print(f"    sha256={after}")
    print(f"    web=/{rel}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Download an approved remote image and hand it to add-media.py.

This is the transport half of Vegas Sidekick media ingestion. It deliberately
accepts only HTTPS, limits download size, verifies the payload is an image via
add-media.py, and optionally verifies an expected SHA-256 before committing.
"""
from __future__ import annotations
import argparse, hashlib, os, subprocess, sys, tempfile
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

MAX_BYTES = 12 * 1024 * 1024


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    p = argparse.ArgumentParser(description="Safely transport remote media into Vegas Sidekick")
    p.add_argument("url")
    p.add_argument("--dest", required=True)
    p.add_argument("--name", required=True)
    p.add_argument("--sha256", help="expected source SHA-256")
    p.add_argument("--min-width", type=int, default=0)
    p.add_argument("--force", action="store_true")
    args = p.parse_args()

    u = urlparse(args.url)
    if u.scheme != "https" or not u.netloc:
        p.error("source must be an HTTPS URL")

    req = Request(args.url, headers={"User-Agent":"VegasSidekick-MediaIngest/1.0"})
    with urlopen(req, timeout=30) as r:
        ctype = (r.headers.get("Content-Type") or "").split(";",1)[0].lower()
        if ctype and not ctype.startswith("image/"):
            p.error(f"remote content-type is not an image: {ctype}")
        data = r.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        p.error(f"remote image exceeds {MAX_BYTES // (1024*1024)} MB limit")
    got = digest(data)
    if args.sha256 and got.lower() != args.sha256.lower():
        p.error(f"SHA-256 mismatch: expected {args.sha256}, got {got}")

    suffix = Path(u.path).suffix.lower()
    if suffix not in {".jpg",".jpeg",".png",".webp",".gif"}:
        suffix = {"image/jpeg":".jpg","image/png":".png","image/webp":".webp","image/gif":".gif"}.get(ctype, ".img")

    script = Path(__file__).with_name("add-media.py")
    with tempfile.TemporaryDirectory(prefix="vs-media-") as td:
        src = Path(td) / f"source{suffix}"
        src.write_bytes(data)
        cmd = [sys.executable, str(script), str(src), "--dest", args.dest, "--name", args.name]
        if args.min_width: cmd += ["--min-width", str(args.min_width)]
        if args.force: cmd.append("--force")
        print(f"transport sha256={got} bytes={len(data)}")
        return subprocess.call(cmd)

if __name__ == "__main__":
    raise SystemExit(main())

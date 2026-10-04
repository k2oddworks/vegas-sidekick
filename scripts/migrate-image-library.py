#!/usr/bin/env python3
"""One-time repository image library migration for Vegas Sidekick.

Moves legacy root /images assets into organized folders, rewrites repository
references, preserves old public URLs with 301 redirects, and writes a manifest.
"""
from __future__ import annotations

from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
IMAGES = ROOT / "images"
DB = ROOT / "data" / "show-database.json"
REDIRECTS = ROOT / "_redirects"
MANIFEST = ROOT / "docs" / "image-library-migration-2026-10-04.json"

IMAGE_EXT = re.compile(r"\.(?:jpe?g|png|webp|gif|svg)$", re.I)
TEXT_EXTENSIONS = {
    ".html", ".htm", ".css", ".js", ".mjs", ".json", ".md", ".xml",
    ".txt", ".py", ".yml", ".yaml", ".toml", ".ini", ".csv"
}
TEXT_FILENAMES = {"_redirects", "_headers", "robots.txt", "wrangler.toml"}

ALIASES = {
    "michael-jackson-one": ["mj-one"],
    "shin-lim": ["shin-lim-limitless"],
    "steve-falcons-comedy-hypnosis-hour": ["steve-falcons-comedy-hypnosis"],
    "criss-angel": ["criss-angel-mindfreak"],
    "battlebots-destruct-a-thon": ["battlebots"],
    "v-the-ultimate-variety-show": ["v-the-ultimate-variety-show"],
    "o": ["o-hero", "o-show", "o-cirque-du-soleil"],
    "ka": ["ka-hero", "ka-show"],
    "vegas-the-show": ["vegas-the-show"],
    "the-mentalist": ["the-mentalist"],
    "rupauls-drag-race-live": ["rupauls-drag-race-live"],
}

VENUE_PREFIXES = [
    "alexis-park", "excalibur", "flamingo", "harrahs", "horseshoe",
    "linq", "luxor", "mandalay-bay", "mgm-grand", "new-york-new-york",
    "planet-hollywood", "rio", "the-strat", "elm", "lfh",
]

NEWS_NAMES = {
    "news-dispatch-og.jpg",
    "john-mayer-live-at-sphere-las-vegas.jpg",
    "viva-la-lisa-las-vegas.jpg",
    "santana-greatest-hits-live-las-vegas.jpg",
    "david-spade-nikki-glaser-las-vegas-2027.jpg",
    "vegas-dispatch-calendar-update-2026-09-30.png",
    "clay-walker-og.jpg",
    "for-king-country-og.jpg",
    "lewis-black-og.jpg",
    "marco-antonio-solis-og.jpg",
    "smashing-pumpkins-og.jpg",
    "tumua-das-og.jpg",
}


def load_show_slugs() -> list[str]:
    data = json.loads(DB.read_text(encoding="utf-8"))
    slugs = [r.get("slug") for r in data.get("records", []) if r.get("slug")]
    return sorted(set(slugs), key=len, reverse=True)


SHOW_SLUGS = load_show_slugs()


def match_show(filename: str) -> str | None:
    stem = IMAGE_EXT.sub("", filename)
    best = None
    best_len = 0

    for slug in SHOW_SLUGS:
        if slug in {"o", "ka"}:
            continue
        if (stem == slug or stem.startswith(slug + "-")) and len(slug) > best_len:
            best, best_len = slug, len(slug)

    for slug, aliases in ALIASES.items():
        for alias in aliases:
            if (stem == alias or stem.startswith(alias + "-")) and len(alias) > best_len:
                best, best_len = slug, len(alias)

    return best


def destination_for(filename: str) -> Path:
    if "seating-chart" in filename.lower() or "poolside-layout" in filename.lower():
        show = match_show(filename)
        folder = show
        if not folder:
            folder = IMAGE_EXT.sub("", filename)
            folder = re.sub(r"-seating-chart(?:-v2)?$", "", folder)
            folder = re.sub(r"-poolside-layout$", "", folder)
        return IMAGES / "seating-charts" / folder / filename

    show = match_show(filename)
    if show:
        return IMAGES / "product-photos" / show / filename

    if re.match(r"^(?:logo-|spike-|kris-kidd)", filename):
        return IMAGES / "brand" / filename

    if filename.startswith("guide-"):
        return IMAGES / "guides" / filename

    if re.match(
        r"^(?:sidekick-index-social|las-vegas-headliners-residencies-social|more-touring-shows-concerts-social)",
        filename,
    ):
        return IMAGES / "sidekick-index" / filename

    if re.match(r"^(?:koko-|walk-the-strip-og)", filename):
        return IMAGES / "play" / filename

    if filename in {"home-og.jpg", "og-homepage.jpg"}:
        return IMAGES / "site" / filename

    if filename in NEWS_NAMES:
        return IMAGES / "news" / filename

    for prefix in VENUE_PREFIXES:
        if filename == prefix + ".jpg" or filename.startswith(prefix + "-"):
            return IMAGES / "venue-photos" / prefix / filename

    raise RuntimeError(f"Unclassified root image: {filename}")


def repo_url(path: Path) -> str:
    return "/" + path.relative_to(ROOT).as_posix()


def should_rewrite(path: Path) -> bool:
    if ".git" in path.parts:
        return False
    if path == MANIFEST:
        return False
    # GitHub Apps cannot push commits that modify workflow files without the
    # separate workflows permission. Workflow YAML is operational config, not
    # customer-facing image markup, so leave it untouched; legacy URLs remain
    # protected by the migration redirects.
    if ".github" in path.parts and "workflows" in path.parts:
        return False
    return path.name in TEXT_FILENAMES or path.suffix.lower() in TEXT_EXTENSIONS


def patch_flat_image_assumptions() -> None:
    """Fix known audit logic that previously assumed /images/<filename> was flat."""
    path = ROOT / "scripts" / "audit-show-media.py"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    old = "name=str(img or '').split('/images/')[-1].split('?')[0]"
    new = "name=Path(str(img or '').split('?')[0]).name"
    if old in text:
        text = text.replace(old, new)
        if "from pathlib import Path" not in text:
            text = text.replace("from pathlib import Path", "from pathlib import Path")
        path.write_text(text, encoding="utf-8")


def update_project_docs() -> None:
    path = ROOT / "AGENTS.md"
    if path.exists():
        text = path.read_text(encoding="utf-8")
        marker = "## Photos / gallery\n"
        block = """## Image library organization

The image library is organized by purpose rather than as a flat /images folder.

- Show photography / artwork: `/images/product-photos/<show-slug>/`
- Seating charts: `/images/seating-charts/<show-or-room>/`
- Venue imagery: `/images/venue-photos/<venue-slug>/`
- Brand / Spike / Kris assets: `/images/brand/`
- Guide covers: `/images/guides/`
- Sidekick Index social assets: `/images/sidekick-index/`
- News / Dispatch assets: `/images/news/`
- Play / game assets: `/images/play/`
- Site-level social imagery: `/images/site/`

Do not add new image files directly to the root `/images/` directory. Keep descriptive filenames even inside named folders.

"""
        if "## Image library organization" not in text and marker in text:
            text = text.replace(marker, block + marker)
            path.write_text(text, encoding="utf-8")

    path = ROOT / "SHOW-PAGE-BENCHMARK.md"
    if path.exists():
        text = path.read_text(encoding="utf-8")
        needle = "## 9. Photos"
        if needle in text and "/images/product-photos/<show-slug>/" not in text:
            text = text.replace(
                needle,
                needle + "\n\nNew show photography and artwork belongs under "
                "`/images/product-photos/<show-slug>/`. Seating charts live separately "
                "under `/images/seating-charts/`. Do not return to a flat `/images/` media library."
            )
            path.write_text(text, encoding="utf-8")

    path = ROOT / "SHOW-BUILDER-PROMPT.md"
    if path.exists():
        text = path.read_text(encoding="utf-8")
        anchor = "## Media Rules"
        note = """## Image path standard

For new show pages, store show photography and artwork under
`/images/product-photos/<show-slug>/`. Store seating charts under
`/images/seating-charts/<show-or-room>/`. Do not upload new show assets directly
to the root `/images/` directory.

"""
        if "## Image path standard" not in text and anchor in text:
            text = text.replace(anchor, note + anchor)
            path.write_text(text, encoding="utf-8")


def main() -> None:
    root_images = sorted(
        p for p in IMAGES.iterdir()
        if p.is_file() and IMAGE_EXT.search(p.name)
    )

    moves = []
    for old in root_images:
        new = destination_for(old.name)
        if new == old:
            continue
        if new.exists():
            if old.read_bytes() != new.read_bytes():
                raise RuntimeError(f"Destination collision with different bytes: {new}")
            old.unlink()
        else:
            new.parent.mkdir(parents=True, exist_ok=True)
            old.rename(new)
        moves.append((old, new))

    replacements = [(repo_url(old), repo_url(new)) for old, new in moves]

    changed_text = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or not should_rewrite(path):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        updated = text
        for old_url, new_url in replacements:
            updated = updated.replace(old_url, new_url)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            changed_text.append(path.relative_to(ROOT).as_posix())

    patch_flat_image_assumptions()
    update_project_docs()

    # Preserve every legacy public image URL with a permanent redirect.
    redirects = REDIRECTS.read_text(encoding="utf-8") if REDIRECTS.exists() else ""
    header = "# Image library migration — October 4, 2026"
    if header not in redirects:
        block = ["", header]
        block.extend(f"{old_url} {new_url} 301" for old_url, new_url in replacements)
        redirects = redirects.rstrip() + "\n" + "\n".join(block) + "\n"
        REDIRECTS.write_text(redirects, encoding="utf-8")

    manifest = {
        "migration_date": "2026-10-04",
        "summary": "Legacy root /images assets moved into purpose-specific folders.",
        "moved_count": len(moves),
        "moves": [
            {"from": old.relative_to(ROOT).as_posix(), "to": new.relative_to(ROOT).as_posix()}
            for old, new in moves
        ],
        "rewritten_text_files": sorted(changed_text),
    }
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    remaining = [
        p.name for p in IMAGES.iterdir()
        if p.is_file() and IMAGE_EXT.search(p.name)
    ]
    if remaining:
        raise RuntimeError(f"Root image files remain after migration: {remaining}")

    print(f"Moved {len(moves)} root image assets.")
    print(f"Rewrote {len(changed_text)} text files.")
    print(f"Manifest: {MANIFEST.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

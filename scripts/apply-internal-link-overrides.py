#!/usr/bin/env python3
"""Apply deliberate editorial internal-link overrides to generated show pages.

This exists so high-confidence related-show relationships survive future canonical
rebuilds without changing category membership or guide rankings.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

OVERRIDES = {
    "shows/magic/the-mentalist/index.html": {
        "href": "/shows/magic/mind2mind/",
        "name": "MIND2MIND",
        "image": "/images/mind2mind-hero.webp",
        "price": "$82",
    },
    "shows/magic/colin-cloud/index.html": {
        "href": "/shows/magic/mind2mind/",
        "name": "MIND2MIND",
        "image": "/images/mind2mind-hero.webp",
        "price": "$82",
    },
}

CARD_RE = re.compile(r'<a class="related-card" href="[^"]+">.*?</a>', re.S)
GRID_RE = re.compile(r'(<div class="related-grid">)(.*?)(</div></div></section>)', re.S)


def card_html(item):
    return (
        f'<a class="related-card" href="{item["href"]}">'
        f'<img src="{item["image"]}" alt="{item["name"]}" loading="lazy">'
        f'<div><strong>{item["name"]}</strong><small>From {item["price"]}</small></div></a>'
    )


def apply(path: Path, item: dict) -> bool:
    text = path.read_text(encoding="utf-8")
    if item["href"] in text:
        print(f"{path.relative_to(ROOT)}: already linked")
        return False

    m = GRID_RE.search(text)
    if not m:
        raise SystemExit(f"Could not find related-grid in {path.relative_to(ROOT)}")

    cards = CARD_RE.findall(m.group(2))
    if len(cards) < 3:
        raise SystemExit(f"Expected at least 3 related cards in {path.relative_to(ROOT)}")

    # Preserve the first two existing editorial choices; use the third slot for the
    # high-confidence mentalism relationship.
    new_grid = m.group(1) + "".join(cards[:2] + [card_html(item)]) + m.group(3)
    text = text[:m.start()] + new_grid + text[m.end():]
    path.write_text(text, encoding="utf-8")
    print(f"{path.relative_to(ROOT)}: added {item['name']}")
    return True


def main():
    changed = 0
    for rel, item in OVERRIDES.items():
        path = ROOT / rel
        if not path.exists():
            raise SystemExit(f"Missing target: {rel}")
        changed += int(apply(path, item))
    print(f"Updated {changed} page(s).")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Fix live-page defects uncovered while validating the SERP metadata refresh."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    rel = "news/matt-rife-stay-golden-dolby-live-december-4/index.html"
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    old = "/images/brad-garrett-hero.jpg"
    new = "/images/product-photos/brad-garretts-comedy-club/brad-garretts-comedy-club-hero.jpg"
    if old in text:
        path.write_text(text.replace(old, new), encoding="utf-8")
        print(f"{rel}: repaired Brad Garrett related-show image")
    else:
        print(f"{rel}: supporting image already correct")


if __name__ == "__main__":
    main()

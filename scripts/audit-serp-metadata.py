#!/usr/bin/env python3
"""Audit indexable Vegas Sidekick pages for title/meta quality and duplicate SERP patterns."""
from collections import Counter, defaultdict
from pathlib import Path
import html
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {".git", "node_modules", ".wrangler", "_archive", "admin", "hq"}


def clean(v):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", v or ""))).strip()


def meta(text, name):
    pats = [
        rf'<meta\s+name=["\']{re.escape(name)}["\']\s+content=["\'](.*?)["\']\s*/?>',
        rf'<meta\s+content=["\'](.*?)["\']\s+name=["\']{re.escape(name)}["\']\s*/?>',
    ]
    for pat in pats:
        m = re.search(pat, text, re.I | re.S)
        if m:
            return clean(m.group(1))
    return ""


def normalized_pattern(title):
    s = title.lower()
    s = re.sub(r'\$\d+(?:\.\d+)?', '$x', s)
    s = re.sub(r'\b\d{4}\b', 'yyyy', s)
    s = re.sub(r'[^a-z$|& ]+', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    # Remove the unique first phrase before common commerce markers to reveal repeated formulas.
    for marker in (' las vegas tickets', ' vegas tickets', ' tickets', ' las vegas show'):
        i = s.find(marker)
        if i > 0:
            return s[i:]
    return s


def main():
    rows = []
    for page in ROOT.rglob("*.html"):
        rel = page.relative_to(ROOT)
        if any(part in SKIP_PARTS for part in rel.parts):
            continue
        text = page.read_text(encoding="utf-8", errors="ignore")
        robots = meta(text, "robots").lower()
        if "noindex" in robots:
            continue
        tm = re.search(r'<title[^>]*>(.*?)</title>', text, re.I | re.S)
        title = clean(tm.group(1)) if tm else ""
        desc = meta(text, "description")
        rows.append((rel.as_posix(), title, desc))

    hard = []
    warn = []
    titles = defaultdict(list)
    descs = defaultdict(list)
    patterns = defaultdict(list)
    for rel, title, desc in rows:
        if not title:
            hard.append(f"{rel}: missing title")
        else:
            titles[title.lower()].append(rel)
            patterns[normalized_pattern(title)].append(rel)
            if len(title) < 25:
                warn.append(f"{rel}: short title ({len(title)} chars): {title}")
            if len(title) > 70:
                warn.append(f"{rel}: long title ({len(title)} chars): {title}")
        if not desc:
            hard.append(f"{rel}: missing meta description")
        else:
            descs[desc.lower()].append(rel)
            if len(desc) < 90:
                warn.append(f"{rel}: short description ({len(desc)} chars)")
            if len(desc) > 190:
                warn.append(f"{rel}: long description ({len(desc)} chars)")

    for value, rels in titles.items():
        if len(rels) > 1:
            hard.append(f"duplicate title ({len(rels)}): {', '.join(rels)}")
    for value, rels in descs.items():
        if len(rels) > 1:
            hard.append(f"duplicate description ({len(rels)}): {', '.join(rels)}")

    repetitive = [(p, r) for p, r in patterns.items() if len(r) >= 8 and ('tickets' in p or 'show guide' in p)]
    repetitive.sort(key=lambda x: len(x[1]), reverse=True)
    for pattern, rels in repetitive:
        warn.append(f"repetitive title pattern ({len(rels)} pages): {pattern}")

    print(f"Indexable HTML pages checked: {len(rows)}")
    print(f"Exact duplicate titles: {sum(1 for v in titles.values() if len(v)>1)}")
    print(f"Exact duplicate descriptions: {sum(1 for v in descs.values() if len(v)>1)}")
    print(f"Repetitive title families (8+ pages): {len(repetitive)}")
    print(f"Warnings: {len(warn)}")
    if warn:
        print("\nWARNINGS")
        for item in warn[:80]:
            print("-", item)
    if hard:
        print("\nHARD FAILURES")
        for item in hard:
            print("-", item)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

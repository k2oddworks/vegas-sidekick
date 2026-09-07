#!/usr/bin/env python3
"""Conservative repo-native technical health audit for Vegas Sidekick.

Checks HTML pages for missing title/canonical, duplicate titles/canonicals, and
broken root-relative href/src targets. External URLs, fragments, mail/tel links,
dynamic query-only links, and generated deployment paths are ignored.

Usage: python3 scripts/audit-site-health.py
Exits non-zero for hard failures. Prints warnings separately.
"""
from pathlib import Path
from urllib.parse import urlsplit, unquote
import collections, re, sys

ROOT = Path(__file__).resolve().parents[1]
EXCLUDE_PARTS = {'.git', 'node_modules', '.wrangler'}
HTML = [p for p in ROOT.rglob('*.html') if not any(part in EXCLUDE_PARTS for part in p.parts)]

def text(p):
    return p.read_text(encoding='utf-8', errors='replace')

def local_target(raw):
    raw = raw.strip()
    if not raw or raw.startswith(('#', 'mailto:', 'tel:', 'javascript:', 'data:')):
        return None
    u = urlsplit(raw)
    if u.scheme or u.netloc or not u.path.startswith('/'):
        return None
    path = unquote(u.path)
    if path == '/':
        return ROOT / 'index.html'
    candidate = ROOT / path.lstrip('/')
    if path.endswith('/'):
        return candidate / 'index.html'
    if candidate.suffix:
        return candidate
    # Extensionless internal route: prefer file, then directory index.
    return candidate if candidate.exists() else candidate / 'index.html'

def main():
    hard=[]; warnings=[]
    titles=collections.defaultdict(list)
    canonicals=collections.defaultdict(list)

    for page in HTML:
        rel=page.relative_to(ROOT).as_posix()
        s=text(page)
        tm=re.search(r'<title[^>]*>(.*?)</title>', s, re.I|re.S)
        if not tm or not re.sub(r'\s+', ' ', tm.group(1)).strip():
            hard.append(f'{rel}: missing/empty <title>')
        else:
            title=re.sub(r'\s+', ' ', tm.group(1)).strip()
            titles[title].append(rel)

        cm=re.search(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)', s, re.I)
        if not cm:
            warnings.append(f'{rel}: missing canonical')
        else:
            canonicals[cm.group(1).strip()].append(rel)

        for attr, raw in re.findall(r'\b(href|src)=["\']([^"\']+)["\']', s, re.I):
            target=local_target(raw)
            if target is not None and not target.exists():
                hard.append(f'{rel}: broken {attr} {raw}')

    for title, pages in titles.items():
        if len(pages)>1:
            warnings.append(f'duplicate title {title!r}: ' + ', '.join(pages))
    for canonical, pages in canonicals.items():
        if len(pages)>1:
            hard.append(f'duplicate canonical {canonical}: ' + ', '.join(pages))

    print(f'HTML pages checked: {len(HTML)}')
    print(f'Hard failures: {len(hard)}')
    print(f'Warnings: {len(warnings)}')
    if hard:
        print('\nHARD FAILURES')
        for x in hard: print(f'- {x}')
    if warnings:
        print('\nWARNINGS')
        for x in warnings: print(f'- {x}')
    return 1 if hard else 0

if __name__=='__main__':
    sys.exit(main())

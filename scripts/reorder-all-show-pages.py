#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
CATEGORIES = {'adult','cirque','comedy','family','magic','music','spectaculars'}
CLOSED = {
    'shows/cirque/mad-apple/index.html',
    'shows/magic/david-goldrake/index.html',
}

SECTION_RE = re.compile(r'<section\b[^>]*\bid="(?P<id>quick|photos|trailer|seats|fit|showtimes|faq)"[^>]*>.*?</section>', re.I | re.S)
SUBNAV_RE = re.compile(r'(<nav\b[^>]*class="[^"]*\bsubnav\b[^"]*"[^>]*>)(.*?)(</nav>)', re.I | re.S)
LINK_RE = re.compile(r'<a\b[^>]*href="#(?P<id>quick|photos|trailer|seats|fit|showtimes|faq)"[^>]*>.*?</a>', re.I | re.S)


def path_ok(p: Path):
    rel = p.relative_to(ROOT).as_posix()
    parts = rel.split('/')
    return len(parts) == 4 and parts[0] == 'shows' and parts[1] in CATEGORIES and parts[-1] == 'index.html' and rel not in CLOSED


def desired(ids):
    # Approved Carrot Top buyer journey: answer first, availability second, experience next,
    # then seating/fit and FAQ. Optional sections simply collapse out.
    return [x for x in ('quick','showtimes','photos','trailer','seats','fit','faq') if x in ids]


def reorder_subnav(text, order):
    m = SUBNAV_RE.search(text)
    if not m:
        return text, False
    inner = m.group(2)
    links = list(LINK_RE.finditer(inner))
    if not links:
        return text, False
    byid = {lm.group('id').lower(): lm.group(0) for lm in links}
    nav_order = [x for x in order if x in byid]
    if len(nav_order) < 2:
        return text, False
    # Preserve any non-section nav material, but the current canonical subnav is links-only.
    prefix = inner[:links[0].start()]
    suffix = inner[links[-1].end():]
    new_inner = prefix + ''.join(byid[x] for x in nav_order) + suffix
    new = text[:m.start(2)] + new_inner + text[m.end(2):]
    return new, new != text


def migrate(p: Path):
    text = p.read_text()
    matches = list(SECTION_RE.finditer(text))
    byid = {}
    for m in matches:
        sid = m.group('id').lower()
        if sid in byid:
            return False, f'duplicate #{sid}'
        byid[sid] = m
    if 'quick' not in byid or 'showtimes' not in byid:
        return False, 'missing quick/showtimes'
    order = desired(byid)
    if len(order) < 2:
        return False, 'not enough canonical sections'
    # Only reorder the canonical decision sections. Content between them is expected to be whitespace.
    selected = [byid[x] for x in order]
    first = min(m.start() for m in selected)
    last = max(m.end() for m in selected)
    region = text[first:last]
    stripped = SECTION_RE.sub('', region)
    if stripped.strip():
        return False, 'non-section content between canonical sections'
    block = '\n'.join(byid[x].group(0) for x in order)
    new = text[:first] + block + text[last:]
    new, _ = reorder_subnav(new, order)
    if new == text:
        return False, 'already ordered'
    p.write_text(new)
    return True, ' > '.join(order)


changed=[]; skipped=[]
for p in sorted((ROOT/'shows').glob('*/*/index.html')):
    if not path_ok(p):
        continue
    ok, msg = migrate(p)
    rel=p.relative_to(ROOT).as_posix()
    (changed if ok else skipped).append((rel,msg))

print(f'Changed {len(changed)} active show pages')
for rel,msg in changed:
    print(f'  {rel}: {msg}')
print(f'Skipped {len(skipped)} pages')
for rel,msg in skipped:
    print(f'  {rel}: {msg}')

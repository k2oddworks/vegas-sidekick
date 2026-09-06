from pathlib import Path
import json
import re

ROOT = Path('.')
FOLDERS = ['news', 'guides', 'shows']
PERSON_ID = 'https://vegassidekick.com/about/kris-kidd/#kris'
PROFILE_URL = 'https://vegassidekick.com/about/kris-kidd/'
IMAGE_URL = 'https://vegassidekick.com/images/kris-kidd.webp'
IMAGE_PATH = '/images/kris-kidd.webp'

STANDARD_AUTHOR = (
    '{"@type":"Person",'
    f'"@id":"{PERSON_ID}",'
    '"name":"Kris Kidd",'
    f'"url":"{PROFILE_URL}",'
    f'"image":"{IMAGE_URL}"'
    '}'
)

AUTHOR_RE = re.compile(
    r'"author"\s*:\s*(\{(?=[^{}]{0,800}"name"\s*:\s*"Kris Kidd")[^{}]*\})',
    re.S,
)

SPAN_BYLINE_RE = re.compile(
    r'<span>\s*(?:By|by)\s+(?:<a\s+href="/(?:about/kris-kidd/|about/)"[^>]*>)?'
    r'(?:<b>)?Kris Kidd(?:</b>)?(?:</a>)?\s*</span>',
    re.I,
)

P_BYLINE_RE = re.compile(
    r'(<p[^>]*class="[^"]*\bbyline\b[^"]*"[^>]*>)\s*(?:By|by)\s*'
    r'<a\s+href="/(?:about/kris-kidd/|about/)"[^>]*>Kris Kidd</a>',
    re.I,
)

AUTHOR_HTML = (
    f'<span class="kris-byline"><img src="{IMAGE_PATH}" alt="Kris Kidd" width="28" height="28">'
    f'By <a href="/about/kris-kidd/">Kris Kidd</a></span>'
)

AUTHOR_CSS = '''<style>/* Kris author identity */
.kris-byline{display:inline-flex!important;align-items:center;gap:7px;vertical-align:middle}
.kris-byline img{width:28px!important;height:28px!important;border-radius:50%;object-fit:cover;flex:0 0 28px;border:2px solid rgba(255,255,255,.75);box-shadow:0 2px 8px rgba(0,0,0,.14)}
.kris-byline a{text-decoration:underline;text-underline-offset:3px}
</style>'''

changed = []
stats = {'schema': 0, 'visible': 0, 'links': 0, 'image': 0}

for folder in FOLDERS:
    for p in (ROOT / folder).rglob('*.html'):
        s = p.read_text(encoding='utf-8')
        old = s

        if '/images/kris-kidd-avatar.jpg' in s:
            stats['image'] += s.count('/images/kris-kidd-avatar.jpg')
            s = s.replace('/images/kris-kidd-avatar.jpg', IMAGE_PATH)
        if 'https://vegassidekick.com/images/kris-kidd-avatar.jpg' in s:
            stats['image'] += s.count('https://vegassidekick.com/images/kris-kidd-avatar.jpg')
            s = s.replace('https://vegassidekick.com/images/kris-kidd-avatar.jpg', IMAGE_URL)

        def author_replace(match):
            stats['schema'] += 1
            return '"author":' + STANDARD_AUTHOR
        s = AUTHOR_RE.sub(author_replace, s)

        old_link = '<a href="/about/">Kris Kidd</a>'
        if old_link in s:
            stats['links'] += s.count(old_link)
            s = s.replace(old_link, '<a href="/about/kris-kidd/">Kris Kidd</a>')

        def span_replace(match):
            stats['visible'] += 1
            return AUTHOR_HTML
        s = SPAN_BYLINE_RE.sub(span_replace, s)

        def p_replace(match):
            stats['visible'] += 1
            return match.group(1) + AUTHOR_HTML
        s = P_BYLINE_RE.sub(p_replace, s)

        if 'class="kris-byline"' in s and '/* Kris author identity */' not in s:
            s = s.replace('</head>', AUTHOR_CSS + '\n</head>', 1)

        if s != old:
            p.write_text(s, encoding='utf-8')
            changed.append(p)

for p in changed:
    s = p.read_text(encoding='utf-8')
    for block in re.findall(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', s, re.S | re.I):
        json.loads(block.strip())

errors = []
for folder in FOLDERS:
    for p in (ROOT / folder).rglob('*.html'):
        s = p.read_text(encoding='utf-8')
        if 'Kris Kidd' not in s:
            continue
        for m in AUTHOR_RE.finditer(s):
            obj = m.group(1)
            for required in (PERSON_ID, PROFILE_URL, IMAGE_URL):
                if required not in obj:
                    errors.append(f'{p}: incomplete Kris author object: missing {required}')
        if '<a href="/about/">Kris Kidd</a>' in s:
            errors.append(f'{p}: old /about/ Kris link remains')
        if re.search(r'<span>\s*(?:By|by)\s+(?:<b>)?Kris Kidd', s, re.I):
            errors.append(f'{p}: unlinked/plain Kris metadata byline remains')

if errors:
    raise SystemExit('\n'.join(errors))

print(f'Changed {len(changed)} files')
print('Stats:', stats)
for p in changed:
    print(p)

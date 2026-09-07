#!/usr/bin/env python3
from pathlib import Path
from urllib.parse import urlparse
import re, sys

ROOT = Path(__file__).resolve().parents[1]
INDEX_ROOTS = ["index.html","about","affiliate-disclosure","contact","guides","news","privacy","search","shows","terms","venues","vegas-sign"]
BANNED = [
    "no hidden fees","zero hidden fees","secure booking","instant delivery","selling fast",
    "prices may increase","prices may rise","book early","booking early","fills fast on weekends",
    "prime seats sell out","before they sell out",
]
STALE_SALE = ["presale starts","presale begins","general on sale","on-sale starts","on sale starts"]
SKIP_LINK_PREFIX = ("mailto:","tel:","javascript:","data:","#")


def pages():
    out=[]
    for root in INDEX_ROOTS:
        p=ROOT/root
        if p.is_file(): out.append(p)
        elif p.exists(): out += list(p.rglob("*.html"))
    seen=[]
    for p in sorted(set(out)):
        rel=p.relative_to(ROOT).as_posix()
        if any(x in rel.split('/') for x in ('preview','_archive','admin','hq','docs','logo-sample')): continue
        text=p.read_text(encoding='utf-8',errors='ignore')
        if 'noindex' in text.lower(): continue
        if '<link rel="canonical"' not in text and "<link rel='canonical'" not in text: continue
        seen.append((p,rel,text))
    return seen


def redirects():
    exact={}
    rp=ROOT/'_redirects'
    if not rp.exists(): return exact
    for line in rp.read_text(encoding='utf-8').splitlines():
        line=line.strip()
        if not line or line.startswith('#'): continue
        parts=line.split()
        if len(parts)>=3 and parts[2] in ('301','302') and ':' not in parts[0] and '*' not in parts[0]:
            exact[parts[0]]=parts[1]
    return exact


def local_target(url):
    if url.startswith('https://vegassidekick.com'):
        url=urlparse(url).path
    if not url.startswith('/'): return None
    path=url.split('?',1)[0].split('#',1)[0]
    if not path or path=='/': return ROOT/'index.html'
    raw=ROOT/path.lstrip('/')
    if raw.suffix:
        return raw
    return raw/'index.html'


def main():
    broken=[]; redirected=[]; stale=[]; olddates=[]
    redirs=redirects()
    current=pages()
    for p,rel,text in current:
        low=text.lower()
        for phrase in BANNED:
            if phrase in low:
                stale.append((rel,phrase))
        for phrase in STALE_SALE:
            if phrase in low:
                stale.append((rel,phrase))
        for m in re.finditer(r'Last updated(?:\s*:)?\s*(January|February|March|April|May|June|July|August)\s+2026', text, re.I):
            olddates.append((rel,m.group(0)))
        for attr,url in re.findall(r'\b(href|src)=["\']([^"\']+)["\']', text, re.I):
            if not url or url.startswith(SKIP_LINK_PREFIX) or '${' in url or '{{' in url: continue
            path=urlparse(url).path if url.startswith('https://vegassidekick.com') else url.split('?',1)[0].split('#',1)[0]
            if path in redirs:
                redirected.append((rel,url,redirs[path]))
            target=local_target(url)
            if target is not None and not target.exists():
                broken.append((rel,url))
    print(f'Canonical pages checked: {len(current)}')
    print(f'Stale/banned copy hits: {len(stale)}')
    print(f'Old Last updated notes: {len(olddates)}')
    print(f'Internal links hitting redirects: {len(redirected)}')
    print(f'Broken local href/src targets: {len(broken)}')
    for title,rows in [('STALE COPY',stale),('OLD DATES',olddates),('REDIRECTED INTERNAL LINKS',redirected),('BROKEN LOCAL TARGETS',broken)]:
        if rows:
            print('\n'+title)
            for row in rows: print('-', ' | '.join(row))
    return 1 if (broken or stale or olddates or redirected) else 0

if __name__=='__main__': sys.exit(main())

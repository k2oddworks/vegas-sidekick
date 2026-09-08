#!/usr/bin/env python3
from pathlib import Path
import json,re,html
ROOT=Path(__file__).resolve().parents[1]
DB=json.loads((ROOT/'data/show-database.json').read_text())
PAGE=ROOT/'shows/deals/index.html'
text=PAGE.read_text()

def extract_meta(t, prop):
    for tag in re.findall(r'<meta\b[^>]*>', t, flags=re.I):
        attrs=dict((k.lower(), html.unescape(v)) for k,v in re.findall(r'([\w:-]+)=["\']([^"\']*)["\']', tag))
        if attrs.get('property')==prop or attrs.get('name')==prop:
            return attrs.get('content')
    return None

def hero_for(r):
    p=ROOT/r.get('page_path','').strip('/')/'index.html'
    if not p.exists(): return None
    t=p.read_text(errors='ignore')
    src=extract_meta(t,'og:image') or extract_meta(t,'twitter:image')
    if src:
        src=re.sub(r'^https://vegassidekick\.com','',src)
        if src.startswith('/'): return src
    m=re.search(r'<div class="hero-media"[^>]*>.*?<img[^>]+src=["\']([^"\']+)',t,re.I|re.S)
    if m:return m.group(1)
    m=re.search(r'<img[^>]+fetchpriority=["\']high["\'][^>]+src=["\']([^"\']+)',t,re.I|re.S)
    return m.group(1) if m else None

fixed=0; missing=[]
for r in DB.get('records',[]):
    if r.get('status')!='active' or not r.get('is_deal'): continue
    href=r.get('page_path')
    image=hero_for(r)
    if not image:
        missing.append(r.get('slug')); continue
    pat=rf'(<article class="deal-card"[^>]*>\s*<a href="{re.escape(href)}">\s*<div class="deal-img"><img src=")[^"]+(" alt=)'
    text,n=re.subn(pat,lambda m:m.group(1)+html.escape(image,quote=True)+m.group(2),text,count=1)
    fixed+=n
PAGE.write_text(text)
if '/favicon.png' in re.sub(r'<link rel="icon"[^>]*>','',text):
    # only card image fallbacks matter; catch them explicitly
    leftovers=len(re.findall(r'<div class="deal-img"><img src="/favicon\.png"',text))
else:leftovers=0
print(f'Fixed {fixed} deal-card images; {leftovers} favicon fallbacks remain.')
if missing or leftovers:
    raise SystemExit(f'Missing hero images for: {missing}; favicon fallbacks: {leftovers}')

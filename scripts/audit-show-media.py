#!/usr/bin/env python3
from pathlib import Path
import html, json, re

ROOT=Path(__file__).resolve().parents[1]
CATS=['adult','cirque','comedy','family','magic','music','spectaculars']
EXT=r'(?:jpe?g|png|webp|avif)'

def blocks(text):
    out=[]
    for raw in re.findall(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',text,re.I|re.S):
        try:out.append(json.loads(raw))
        except:pass
    return out

def event(text):
    for b in blocks(text):
        if isinstance(b,dict) and b.get('@type') in ('Event','EventSeries'):return b
    return None

def title_for(text,ev,slug):
    if ev and ev.get('name'):return str(ev['name'])
    m=re.search(r'<title>(.*?)</title>',text,re.I|re.S)
    if m:return html.unescape(re.sub(r'<[^>]+>','',m.group(1))).split('|')[0].strip()
    return slug.replace('-',' ').title()

def photo_count(text,ev):
    img=ev.get('image') if ev else ''
    if isinstance(img,list):img=img[0] if img else ''
    name=Path(str(img or '').split('?')[0]).name
    stem=re.sub(r'\.'+EXT+r'$','',name,flags=re.I)
    base=re.sub(r'-(?:hero|og)$','',stem,flags=re.I)
    refs=re.findall(r'/images/([^"\'<>?]+\.'+EXT+r')',text,re.I)
    seen=set()
    for ref in [name]+refs:
        if not ref:continue
        st=re.sub(r'\.'+EXT+r'$','',Path(ref).name,flags=re.I)
        if base and not (st==base or st.startswith(base+'-')):continue
        low=st.lower()
        if any(x in low for x in ('-og','thumb','video-poster','video-thumb','logo','seat-map','seating-chart','-map')):continue
        seen.add(low)
    return len(seen)

def videos(text):
    ids=set(re.findall(r'data-video-id=["\']([A-Za-z0-9_-]{6,})',text,re.I))
    ids.update(re.findall(r'youtube(?:-nocookie)?\.com/embed/([A-Za-z0-9_-]{6,})',text,re.I))
    ids.update(re.findall(r'youtu\.be/([A-Za-z0-9_-]{6,})',text,re.I))
    return sorted(ids)

def main():
    rows=[]
    for cat in CATS:
        for p in sorted((ROOT/'shows'/cat).glob('*/index.html')):
            text=p.read_text(encoding='utf-8',errors='replace')
            ev=event(text)
            if not ev or ev.get('eventStatus')!='https://schema.org/EventScheduled':continue
            rows.append((cat,p.parent.name,title_for(text,ev,p.parent.name),photo_count(text,ev),videos(text)))
    less=[r for r in rows if r[3]<5]
    novid=[r for r in rows if not r[4]]
    out=['# Vegas Sidekick Active Show Media Audit — 2026-09-07','',
         'Generated from the current `main` checkout. Only active `EventScheduled` show pages are included. Photo counts are unique show-specific image references; alternate JPG/WebP versions of the same named asset count once. Related-show images, OG images, thumbnails, maps and seating graphics are excluded.','',
         f'- Active show pages audited: **{len(rows)}**',
         f'- Active pages with fewer than 5 show photos: **{len(less)}**',
         f'- Active pages with a verified embedded/runtime YouTube video: **{len(rows)-len(novid)}**',
         f'- Active pages without a verified YouTube video: **{len(novid)}**','','## Full inventory','',
         '| Category | Show | Photos | Video | Video ID(s) |','|---|---|---:|:---:|---|']
    for cat,slug,name,photos,vids in rows:
        out.append(f'| {cat.title()} | {name.replace("|","/")} | {photos} | {"Yes" if vids else "No"} | {", ".join(vids) if vids else "—"} |')
    out += ['','## Fewer than 5 photos','']
    for cat in CATS:
        vals=[r for r in less if r[0]==cat]
        if vals:
            out.append(f'### {cat.title()}')
            out.extend(f'- {r[2]} — {r[3]}' for r in vals)
            out.append('')
    out += ['## No verified video','']
    for cat in CATS:
        vals=[r for r in novid if r[0]==cat]
        if vals:
            out.append(f'### {cat.title()}')
            out.extend(f'- {r[2]}' for r in vals)
            out.append('')
    target=ROOT/'docs/show-media-audit-2026-09-07.md'
    target.write_text('\n'.join(out)+'\n',encoding='utf-8')
    print(f'Active shows: {len(rows)}')
    print(f'Under 5 photos: {len(less)}')
    print(f'With video: {len(rows)-len(novid)}')
    print(f'Without video: {len(novid)}')

if __name__=='__main__':main()

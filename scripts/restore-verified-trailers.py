#!/usr/bin/env python3
from pathlib import Path
import json,re

ROOT=Path('.')
TRAILERS={
 '/shows/cirque/ka/':'mFbh6dhPqz4',
 '/shows/cirque/michael-jackson-one/':'SUw-Fsr5cBE',
 '/shows/comedy/brad-garretts-comedy-club/':'dXT1zsASfZE',
 '/shows/comedy/carrot-top/':'XRdqvnCZe-A',
 '/shows/comedy/comedy-cellar/':'jJPxYBaH_s8',
 '/shows/comedy/marc-savard-comedy-hypnosis/':'E0bECqHgo20',
 '/shows/comedy/popovich-comedy-pet-theater/':'7Z6XlhYG-Nk',
 '/shows/comedy/tape-face/':'TqGNzwWV03M',
}

def rows_from_db(obj):
    if isinstance(obj,list): return obj
    if isinstance(obj,dict):
        for key in ('shows','records','items'):
            if isinstance(obj.get(key),list): return obj[key]
    return []

# Restore verified trailer IDs to the operational show database.
db_path=ROOT/'data/show-database.json'
db=json.loads(db_path.read_text(encoding='utf-8'))
rows=rows_from_db(db)
seen=set()
for row in rows:
    if not isinstance(row,dict): continue
    page=row.get('page_path') or row.get('canonical_path')
    if page in TRAILERS:
        desired='https://youtu.be/'+TRAILERS[page]
        current=row.get('official_trailer') or ''
        if current and TRAILERS[page] not in current:
            raise SystemExit(f'Conflicting trailer for {page}: {current}')
        row['official_trailer']=desired
        seen.add(page)
missing_db=set(TRAILERS)-seen
if missing_db:
    raise SystemExit('Trailer pages missing from show database: '+', '.join(sorted(missing_db)))
db_path.write_text(json.dumps(db,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

changed=[]
for page,vid in TRAILERS.items():
    path=ROOT/page.lstrip('/')/'index.html'
    if not path.exists(): raise SystemExit(f'Missing page {page}')
    text=path.read_text(encoding='utf-8')
    before=text
    h1=re.search(r'<h1[^>]*>(.*?)</h1>',text,re.S)
    display=re.sub('<[^>]+>','',h1.group(1)).strip() if h1 else 'the show'
    shell=(f'<div class="vs-video-shell"><div class="vs-video" data-youtube-id="{vid}">'
           f'<img alt="Official {display} trailer thumbnail" loading="lazy" src="https://i.ytimg.com/vi/{vid}/hqdefault.jpg"/>'
           f'<button aria-label="Play official {display} trailer" class="vs-video-play" type="button"><span aria-hidden="true">▶</span></button>'
           f'</div></div>')
    section=(f'<section class="section" id="trailer"><div class="wrap"><div class="eyebrow">Official trailer</div>'
             f'<h2>Watch {display}</h2>{shell}</div></section>')

    existing=re.search(r'<section[^>]*id="(?:trailer|section-trailer)"[^>]*>.*?</section>',text,re.S)
    if existing:
        text=text[:existing.start()]+section+text[existing.end():]
    else:
        # If a legacy eager YouTube iframe exists outside a named trailer section, replace its nearest simple wrapper only when possible.
        legacy=re.search(r'<div class="(?:video-wrap|video-shell|vs-video-shell)"[^>]*>.*?(?:youtube(?:-nocookie)?\.com/embed/'+re.escape(vid)+r'|data-(?:video-id|youtube-id)="'+re.escape(vid)+r'").*?</div>\s*</div>',text,re.S)
        if legacy:
            text=text[:legacy.start()]+shell+text[legacy.end():]
        else:
            anchor=None
            for sid in ('seats','fit','showtimes','faq'):
                m=re.search(r'<section[^>]*id="'+sid+r'"',text)
                if m: anchor=m.start(); break
            if anchor is None: raise SystemExit(f'No safe trailer insertion anchor on {page}')
            text=text[:anchor]+section+text[anchor:]

    # Remove any remaining eager iframe for this verified trailer from the page if it survived in duplicate legacy markup.
    text=re.sub(r'<iframe[^>]+(?:youtube(?:-nocookie)?\.com/embed/'+re.escape(vid)+r')[^>]*>\s*</iframe>','',text,flags=re.I)
    # Standardize subnav link when present.
    if 'href="#trailer"' not in text and '<a href="#photos">Photos</a>' in text:
        text=text.replace('<a href="#photos">Photos</a>','<a href="#photos">Photos</a><a href="#trailer">Trailer</a>',1)
    # Remove duplicate legacy nav target for section-trailer if any.
    text=text.replace('href="#section-trailer"','href="#trailer"')

    if text!=before:
        path.write_text(text,encoding='utf-8')
        changed.append(page)

print(f'RESTORED_DB={len(TRAILERS)}')
print(f'CHANGED_PAGES={len(changed)}')
for page in changed: print('CHANGED='+page)

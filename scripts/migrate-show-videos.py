#!/usr/bin/env python3
from pathlib import Path
import json,re

ROOT=Path('.')

def yt_id(value):
    if not value:return None
    if isinstance(value,dict):
        value=value.get('video_id') or value.get('url') or value.get('watch_url') or value.get('embed_url') or ''
    value=str(value)
    patterns=[r'youtu\.be/([A-Za-z0-9_-]{6,20})',r'[?&]v=([A-Za-z0-9_-]{6,20})',r'/embed/([A-Za-z0-9_-]{6,20})',r'/shorts/([A-Za-z0-9_-]{6,20})']
    for p in patterns:
        m=re.search(p,value)
        if m:return m.group(1)
    if re.fullmatch(r'[A-Za-z0-9_-]{6,20}',value):return value
    return None

def rows_from_db(obj):
    if isinstance(obj,list): return obj
    if isinstance(obj,dict):
        for key in ('shows','records','items'):
            if isinstance(obj.get(key),list): return obj[key]
    return []

verified={}
# Master show database
p=ROOT/'data/show-database.json'
if p.exists():
    db=json.loads(p.read_text(encoding='utf-8'))
    for row in rows_from_db(db):
        if not isinstance(row,dict):continue
        url=row.get('official_trailer') or ((row.get('media') or {}).get('official_trailer') if isinstance(row.get('media'),dict) else None)
        vid=yt_id(url)
        page=row.get('page_path') or row.get('canonical_path')
        status=str(row.get('status','active')).lower()
        if vid and page and status not in {'closed','ended','inactive','archived'}:
            verified[page]=(vid,row.get('name') or '')
# Per-show records can be newer/more structured.
for fp in (ROOT/'data/shows').glob('*.json') if (ROOT/'data/shows').exists() else []:
    try:r=json.loads(fp.read_text(encoding='utf-8'))
    except Exception:continue
    media=r.get('media') or {}
    vid=yt_id(media.get('official_trailer') if isinstance(media,dict) else None)
    page=r.get('canonical_path')
    if vid and page and str(r.get('status','active')).lower() not in {'closed','ended','inactive','archived'}:
        verified[page]=(vid,r.get('name') or '')

changed=[]; inserted=[]; migrated=[]; missing=[]
for page,(vid,name) in sorted(verified.items()):
    path=ROOT/page.lstrip('/')/'index.html'
    if not path.exists():
        missing.append((page,'page missing'));continue
    text=path.read_text(encoding='utf-8')
    before=text
    h1=re.search(r'<h1[^>]*>(.*?)</h1>',text,re.S)
    display=re.sub('<[^>]+>','',h1.group(1)).strip() if h1 else (name or 'the show')

    # Standardize known legacy wrappers/controls while preserving verified IDs.
    text=re.sub(r'class="video-shell"', 'class="vs-video-shell"', text)
    text=re.sub(r'class="video-preview"([^>]*?)data-video-id="[A-Za-z0-9_-]+"', rf'class="vs-video"\1data-youtube-id="{vid}"', text)
    text=re.sub(r'class="video"([^>]*?)data-youtube-id="[A-Za-z0-9_-]+"', rf'class="vs-video"\1data-youtube-id="{vid}"', text)
    text=re.sub(r'class="vs-video"([^>]*?)data-youtube-id="[A-Za-z0-9_-]+"', rf'class="vs-video"\1data-youtube-id="{vid}"', text)
    text=re.sub(r'class="play"', 'class="vs-video-play"', text)
    text=re.sub(r'(i\.ytimg\.com/vi/)[A-Za-z0-9_-]+/', rf'\g<1>{vid}/', text)
    text=re.sub(r'(youtube(?:-nocookie)?\.com/embed/)[A-Za-z0-9_-]+', rf'\g<1>{vid}', text)

    has_component=bool(re.search(r'class="vs-video"[^>]*data-youtube-id="'+re.escape(vid)+r'"',text))
    if not has_component:
        # Existing trailer section with unusable markup: replace only its media body if identifiable.
        section=re.search(r'<section[^>]*id="trailer"[^>]*>.*?</section>',text,re.S)
        shell=(f'<div class="vs-video-shell"><div class="vs-video" data-youtube-id="{vid}">'
               f'<img alt="Official {display} trailer thumbnail" loading="lazy" src="https://i.ytimg.com/vi/{vid}/hqdefault.jpg"/>'
               f'<button aria-label="Play official {display} trailer" class="vs-video-play" type="button"><span aria-hidden="true">▶</span></button>'
               f'</div></div>')
        if section:
            old=section.group(0)
            # Prefer replacing a legacy media node; otherwise rebuild just this small section.
            if re.search(r'<div class="(?:video|video-preview|vs-video)[^>]*>.*?</div>\s*</div>',old,re.S):
                new=re.sub(r'<div class="(?:video-shell|vs-video-shell)[^>]*>.*?</div>\s*</div>',shell,old,count=1,flags=re.S)
                if new==old:
                    new=re.sub(r'<div class="(?:video|video-preview|vs-video)[^>]*>.*?</div>',shell,old,count=1,flags=re.S)
            else:
                new=(f'<section class="section" id="trailer"><div class="wrap"><div class="eyebrow">Official trailer</div>'
                     f'<h2>Watch {display}</h2>{shell}</div></section>')
            text=text[:section.start()]+new+text[section.end():]
            migrated.append(page)
        else:
            new=(f'<section class="section" id="trailer"><div class="wrap"><div class="eyebrow">Official trailer</div>'
                 f'<h2>Watch {display}</h2>{shell}</div></section>')
            anchor=None
            for sid in ('seats','fit','showtimes','faq'):
                m=re.search(r'<section[^>]*id="'+sid+r'"',text)
                if m: anchor=m.start();break
            if anchor is None:
                missing.append((page,'no insertion anchor'));continue
            text=text[:anchor]+new+text[anchor:]
            # Add subnav trailer link after Photos when possible.
            if 'href="#trailer"' not in text:
                text=text.replace('<a href="#photos">Photos</a>','<a href="#photos">Photos</a><a href="#trailer">Trailer</a>',1)
            inserted.append(page)

    if text!=before:
        path.write_text(text,encoding='utf-8')
        changed.append(page)

# Strengthen audit so verified trailers must actually appear as standard component.
audit=ROOT/'scripts/audit-show-videos.py'
audit.write_text('''#!/usr/bin/env python3\nfrom pathlib import Path\nimport json,re,sys\nROOT=Path(__file__).resolve().parents[1]\n\ndef y(v):\n    if not v:return None\n    if isinstance(v,dict):v=v.get("video_id") or v.get("url") or v.get("watch_url") or v.get("embed_url") or ""\n    v=str(v)\n    for p in (r"youtu\\.be/([A-Za-z0-9_-]{6,20})",r"[?&]v=([A-Za-z0-9_-]{6,20})",r"/embed/([A-Za-z0-9_-]{6,20})",r"/shorts/([A-Za-z0-9_-]{6,20})"):\n        m=re.search(p,v)\n        if m:return m.group(1)\n    return v if re.fullmatch(r"[A-Za-z0-9_-]{6,20}",v) else None\n\ndef rows(o):\n    if isinstance(o,list):return o\n    if isinstance(o,dict):\n        for k in ("shows","records","items"):\n            if isinstance(o.get(k),list):return o[k]\n    return []\n\nverified={}\np=ROOT/"data/show-database.json"\nif p.exists():\n    for r in rows(json.loads(p.read_text(encoding="utf-8"))):\n        if not isinstance(r,dict):continue\n        v=y(r.get("official_trailer") or ((r.get("media") or {}).get("official_trailer") if isinstance(r.get("media"),dict) else None)); page=r.get("page_path") or r.get("canonical_path")\n        if v and page and str(r.get("status","active")).lower() not in {"closed","ended","inactive","archived"}:verified[page]=v\nfor fp in (ROOT/"data/shows").glob("*.json") if (ROOT/"data/shows").exists() else []:\n    try:r=json.loads(fp.read_text(encoding="utf-8"))\n    except Exception:continue\n    v=y(((r.get("media") or {}).get("official_trailer") if isinstance(r.get("media"),dict) else None));page=r.get("canonical_path")\n    if v and page and str(r.get("status","active")).lower() not in {"closed","ended","inactive","archived"}:verified[page]=v\nproblems=[]\nfor page,vid in sorted(verified.items()):\n    fp=ROOT/page.lstrip("/")/"index.html"\n    if not fp.exists():problems.append(f"{page}: verified trailer but page missing");continue\n    t=fp.read_text(encoding="utf-8",errors="ignore")\n    if not re.search(r'class="vs-video"[^>]*data-youtube-id="'+re.escape(vid)+r'"',t):problems.append(f"{page}: verified trailer {vid} missing shared component")\n    if re.search(r'<iframe[^>]+youtube',t,re.I):problems.append(f"{page}: eager YouTube iframe found; use click-to-load component")\n    if re.search(r'class="(?:video|video-preview)"[^>]*data-(?:youtube-id|video-id)',t):problems.append(f"{page}: legacy video markup remains")\nif problems:\n    print("Show video audit FAILED:")\n    print("\\n".join(" - "+x for x in problems));sys.exit(1)\nprint(f"Show video audit passed: {len(verified)} verified active trailer(s).")\n''',encoding='utf-8')

print(f'VERIFIED={len(verified)}')
print(f'CHANGED={len(changed)}')
print(f'INSERTED={len(inserted)}')
print(f'MIGRATED={len(migrated)}')
for page in changed: print('CHANGED_PAGE='+page)
for page,why in missing: print('REVIEW='+page+' :: '+why)

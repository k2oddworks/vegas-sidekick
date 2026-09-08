#!/usr/bin/env python3
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'data/show-database.json').read_text())
by={r['slug']:r for r in data['records'] if r.get('status')=='active'}

def calc(r):
    try:a=float(r['our_price']);b=float(r['regular_price'])
    except:return None
    s=b-a
    return round(s) if b and s>=5 else None

def inject_nested(slug,path):
    r=by[slug];s=calc(r)
    if not s:return
    our=f"${round(float(r['our_price']))}";reg=f"${round(float(r['regular_price']))}";save=f"${s}"
    p=ROOT/path;t=p.read_text()
    if 'vs-save-badge' in t:return
    line=f'<div class="vs-deal-line"><span class="vs-regular-price">Regular {reg}</span><span class="vs-save-badge">Save {save}</span></div>'
    note=f'<div class="vs-deal-note">🌵 <strong>Sidekick deal:</strong> {our} is {save} below the listed regular price of {reg}.</div>'
    # Custom benchmark buyboxes wrap price in an extra div.
    pat=rf'(<div class="buybox">\s*<div>\s*<div class="price"><small>[^<]*</small>{re.escape(our)}</div>)'
    t,n=re.subn(pat,lambda m:m.group(1)+line,t,count=1,flags=re.S|re.I)
    if n:
        # place note immediately after the buybox block when possible
        box=re.search(r'<div class="buybox">.*?</div>\s*</div>',t,re.S|re.I)
        if box:t=t[:box.end()]+note+t[box.end():]
    p.write_text(t)

def inject_ka():
    r=by['ka'];s=calc(r)
    if not s:return
    our=f"${round(float(r['our_price']))}";reg=f"${round(float(r['regular_price']))}";save=f"${s}"
    p=ROOT/'shows/cirque/ka/index.html';t=p.read_text()
    if 'vs-save-badge' not in t:
        line=f'<div class="vs-deal-line"><span class="vs-regular-price">Regular {reg}</span><span class="vs-save-badge">Save {save}</span></div>'
        note=f'<div class="vs-deal-note">🌵 <strong>Sidekick deal:</strong> {our} is {save} below the listed regular price of {reg}.</div>'
        pat=rf'(<div class="price"><small>[^<]*</small><strong>{re.escape(our)}</strong></div>)'
        t,n=re.subn(pat,lambda m:m.group(1)+line,t,count=1,flags=re.I)
        if n:t=t.replace(line,line+note,1)
    # mobile CTA already has a strong price; add compact savings if absent
    if 'vs-mobile-save' not in t:
        t=re.sub(rf'(<div class="mobile-cta"[^>]*>.*?<strong>{re.escape(our)}</strong>)',lambda m:m.group(1)+f'<span class="vs-mobile-save">Save {save}</span>',t,count=1,flags=re.S|re.I)
    p.write_text(t)

inject_nested('carrot-top','shows/comedy/carrot-top/index.html')
inject_nested('vegas-the-show','shows/music/vegas-the-show/index.html')
inject_ka()

# Give the Deals page a permanent crawlable link from All Shows.
p=ROOT/'shows/index.html';t=p.read_text()
if 'href="/shows/deals/"' not in t:
    link='<div class="vs-deals-static-link" style="max-width:1200px;margin:0 auto 30px;padding:0 24px"><a href="/shows/deals/" style="display:inline-flex;background:#ffb000;color:#171225;font-weight:800;padding:11px 15px;border-radius:999px">🔥 Browse all current ticket deals →</a></div>'
    t=t.replace('<div id="vs-footer"></div>',link+'<div id="vs-footer"></div>',1)
p.write_text(t)
print('Savings edge cases repaired.')

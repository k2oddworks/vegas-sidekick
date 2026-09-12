#!/usr/bin/env python3
import argparse, html, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def centroid(points):
    vals=[]
    for p in points.split():
        x,y=p.split(','); vals.append((float(x),float(y)))
    return (sum(x for x,_ in vals)/len(vals),sum(y for _,y in vals)/len(vals))

def generate(layout_path,out_path):
    data=json.loads(layout_path.read_text())
    vb=data.get('viewBox','0 0 120 100')
    _,_,vw,vh=map(float,vb.split())
    W=1200; H=1000
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {vw:g} {vh:g}" role="img">',
           '<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#180d28"/><stop offset="1" stop-color="#09060e"/></linearGradient><filter id="g"><feGaussianBlur stdDeviation=".8" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>',
           f'<rect width="{vw:g}" height="{vh:g}" fill="url(#bg)"/>']
    stage=data.get('stage')
    if isinstance(stage,dict):
        parts.append(f'<path d="{html.escape(stage["path"])}" fill="#15131a" stroke="#ffb000" stroke-width="1.2" filter="url(#g)"/>')
        label=stage.get('label','STAGE')
        parts.append(f'<text x="{stage.get("labelX",vw/2)}" y="{stage.get("labelY",vh*.9)}" fill="#fff" font-family="Arial,sans-serif" font-size="4" font-weight="800" text-anchor="middle" dominant-baseline="middle">{html.escape(str(label))}</text>')
    shapes=data.get('shapes',[])
    for z in data.get('zones',[]):
        color=z.get('color','#7b35ea')
        if z.get('path'):
            parts.append(f'<path d="{html.escape(z["path"])}" fill="{color}" stroke="#fff" stroke-opacity=".55" stroke-width=".65"/>')
            lx,ly=z.get('labelX',vw/2),z.get('labelY',vh/2)
        else:
            zs=[s for s in shapes if s.get('zone')==z.get('id')]
            for s in zs:
                parts.append(f'<polygon points="{html.escape(s["points"])}" fill="{color}" stroke="#fff" stroke-opacity=".55" stroke-width=".65"/>')
            lx,ly=centroid(zs[0]['points']) if zs else (vw/2,vh/2)
        label=z.get('mapLabel') or z.get('label','')
        parts.append(f'<text x="{lx}" y="{ly}" fill="#fff" font-family="Arial,sans-serif" font-size="3.8" font-weight="800" text-anchor="middle" dominant-baseline="middle">{html.escape(str(label))}</text>')
    parts += [
        f'<rect x="{vw*.24:g}" y="{vh*.925:g}" width="{vw*.52:g}" height="{vh*.055:g}" rx="2.8" fill="#ffb000"/>',
        f'<text x="{vw/2:g}" y="{vh*.953:g}" fill="#201328" font-family="Arial,sans-serif" font-size="3.6" font-weight="900" text-anchor="middle" dominant-baseline="middle">SWEET SPOT / OUR PICK</text>',
        '</svg>'
    ]
    out_path.write_text('\n'.join(parts))

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('layout')
    ap.add_argument('output')
    a=ap.parse_args()
    lp=ROOT/a.layout; op=ROOT/a.output
    op.parent.mkdir(parents=True,exist_ok=True)
    generate(lp,op)
    print(op)

#!/usr/bin/env python3
import json, html
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
src=ROOT/'data/seat-layouts/nathan-burton-theater.json'
out=ROOT/'images/nathan-burton-theater-seating-chart.svg'
data=json.loads(src.read_text())
zones={z['id']:z for z in data['zones']}
W,H=1200,1500
x,w=300,600
y=330
row_h,gap=32,13
parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
       '<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#140923"/><stop offset="1" stop-color="#07070c"/></linearGradient><filter id="glow"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>',
       f'<rect width="{W}" height="{H}" rx="42" fill="url(#bg)"/>',
       '<text x="70" y="75" fill="#fff" font-family="Arial,sans-serif" font-size="42" font-weight="800">vegas <tspan fill="#ff2e7e">sidekick</tspan></text>',
       '<text x="72" y="112" fill="#d9d1df" font-family="Arial,sans-serif" font-size="17" letter-spacing="5">SHOWS • TICKETS • GOOD TIMES</text>',
       '<path d="M330 165 H870 V255 Q600 310 330 255 Z" fill="#121116" stroke="#ffb000" stroke-width="4" filter="url(#glow)"/>',
       '<text x="600" y="235" text-anchor="middle" fill="#fff" font-family="Arial,sans-serif" font-size="30" font-weight="700" letter-spacing="10">STAGE</text>']
side=zones['front-sides']
for sx,ang in [(165,-18),(915,18)]:
    for r in range(side['rows']):
        yy=330+r*62
        parts.append(f'<rect x="{sx}" y="{yy}" width="115" height="38" rx="8" fill="{side["color"]}" stroke="#fff" stroke-opacity=".35" transform="rotate({ang} {sx+57} {yy+19})"/>')
current=y
for zid in ['front-center','sweet-spot','good-value','rear-section']:
    z=zones[zid]
    for _ in range(z['rows']):
        parts.append(f'<rect x="{x}" y="{current}" width="{w}" height="{row_h}" rx="9" fill="{z["color"]}" stroke="#fff" stroke-opacity=".25"/>')
        current += row_h+gap
    current += 14
# zone labels
labels=[('Front sides',95,400,side['color']),('Front center',930,395,zones['front-center']['color']),('Sweet spot',90,630,zones['sweet-spot']['color']),('Good value',930,900,zones['good-value']['color']),('Rear section',90,1120,zones['rear-section']['color'])]
for label,lx,ly,c in labels:
    parts.append(f'<rect x="{lx-20}" y="{ly-38}" width="190" height="62" rx="16" fill="#100a17" stroke="{c}" stroke-width="2"/>')
    parts.append(f'<text x="{lx}" y="{ly}" fill="{c}" font-family="Arial,sans-serif" font-size="24" font-weight="700">{html.escape(label)}</text>')
parts += [
    '<rect x="420" y="1210" width="360" height="48" rx="24" fill="#ffb000"/>',
    '<text x="600" y="1242" text-anchor="middle" fill="#171225" font-family="Arial,sans-serif" font-size="20" font-weight="900" letter-spacing="3">OUR PICK · SWEET SPOT</text>',
    f'<text x="600" y="1330" text-anchor="middle" fill="#fff" font-family="Arial,sans-serif" font-size="32" font-weight="800">{html.escape(data["venue"])}</text>',
    f'<text x="600" y="1372" text-anchor="middle" fill="#d7cedd" font-family="Arial,sans-serif" font-size="21">{html.escape(data["address"])}</text>',
    '<text x="600" y="1435" text-anchor="middle" fill="#8f8597" font-family="Arial,sans-serif" font-size="17">Simplified seating chart · exact seat inventory varies by performance</text>',
    '</svg>'
]
out.write_text('\n'.join(parts))
print(out)

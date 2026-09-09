#!/usr/bin/env python3
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
src = ROOT / "data/seat-layouts/o-theatre-bellagio.json"
out = ROOT / "images/o-theatre-bellagio-seating-chart.svg"
data = json.loads(src.read_text())

W, H = 1200, 1440
parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
    '<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#150922"/><stop offset="1" stop-color="#07070c"/></linearGradient><filter id="glow"><feGaussianBlur stdDeviation="7" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>',
    f'<rect width="{W}" height="{H}" rx="42" fill="url(#bg)"/>',
    '<text x="70" y="75" fill="#fff" font-family="Arial,sans-serif" font-size="42" font-weight="800">vegas <tspan fill="#ff2e7e">sidekick</tspan></text>',
    '<text x="72" y="112" fill="#d9d1df" font-family="Arial,sans-serif" font-size="17" letter-spacing="5">SHOWS • TICKETS • GOOD TIMES</text>',
    '<text x="600" y="150" text-anchor="middle" fill="#fff" font-family="Arial,sans-serif" font-size="32" font-weight="800">O THEATRE SEATING GUIDE</text>',
    '<g transform="translate(100 175)">',
]
for s in data["sections"]:
    stroke = "#ffb000" if s.get("our_pick") else "rgba(255,255,255,.32)"
    sw = "7" if s.get("our_pick") else "2.5"
    parts.append(f'<path d="{html.escape(s["path"])}" fill="{s["color"]}" stroke="{stroke}" stroke-width="{sw}"/>')
    fs = 22 if len(s["label"]) <= 4 else 18
    parts.append(f'<text x="{s["label_x"]}" y="{s["label_y"]}" text-anchor="middle" dominant-baseline="middle" fill="#fff" font-family="Arial,sans-serif" font-size="{fs}" font-weight="800">{html.escape(s["label"])}</text>')
parts += [
    f'<path d="{data["stage"]["path"]}" fill="#111116" stroke="#ffb000" stroke-width="4" filter="url(#glow)"/>',
    f'<text x="{data["stage"]["label_x"]}" y="{data["stage"]["label_y"]}" text-anchor="middle" fill="#fff" font-family="Arial,sans-serif" font-size="28" font-weight="800" letter-spacing="7">STAGE</text>',
    '</g>',
    '<rect x="225" y="1320" width="750" height="50" rx="25" fill="#ffb000"/>',
    '<text x="600" y="1353" text-anchor="middle" fill="#171225" font-family="Arial,sans-serif" font-size="17" font-weight="900" letter-spacing="1.8">SECTIONS 201–205 · SWEET SPOT / OUR PICK</text>',
    f'<text x="600" y="1400" text-anchor="middle" fill="#fff" font-family="Arial,sans-serif" font-size="28" font-weight="800">{html.escape(data["venue"])}</text>',
    '</svg>',
]
out.write_text("\n".join(parts))
print(out)

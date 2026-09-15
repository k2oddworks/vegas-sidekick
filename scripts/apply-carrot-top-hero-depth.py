from pathlib import Path
p=Path(__file__).resolve().parents[1]/'shows/comedy/carrot-top/index.html'
s=p.read_text()
# Carrot Top is the opt-in test; shared assets make this reusable on other show pages.
if '/assets/show-hero-depth.css' not in s:
    s=s.replace('<link href="/assets/ticket-cta.css" rel="stylesheet"/>','<link href="/assets/ticket-cta.css" rel="stylesheet"/><link href="/assets/show-hero-depth.css?v=1" rel="stylesheet"/>',1)
s=s.replace('<div class="hero-media" data-mobile-fit="safe"','<div class="hero-media vs-hero-depth" data-mobile-fit="safe"',1)
if '/assets/show-hero-depth.js' not in s:
    s=s.replace('</body>','<script defer src="/assets/show-hero-depth.js?v=1"></script></body>',1)
p.write_text(s)

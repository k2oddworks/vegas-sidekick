from pathlib import Path
p=Path(__file__).resolve().parents[1]/'shows/music/vegas-the-show/index.html'
s=p.read_text()
# VEGAS! The Show is the first production test of the reusable safe-artwork hero mode. Retry after authoritative CSS update.
if '/assets/show-hero-fit.css' not in s:
    s=s.replace('<link href="/assets/show-savings.css" rel="stylesheet"/>','<link href="/assets/show-savings.css" rel="stylesheet"/><link href="/assets/show-hero-fit.css?v=2" rel="stylesheet"/>',1)
old='<div class="hero-media" data-mobile-fit="safe" style="--mobile-hero-image:url(\'/images/product-photos/vegas-the-show/vegas-the-show-hero.webp\');--mobile-hero-position:center center">'
new='<div class="hero-media vs-hero-safe" data-mobile-fit="safe" style="--vs-safe-image:url(\'/images/product-photos/vegas-the-show/vegas-the-show-hero.webp\');--vs-hero-focal:center center;--mobile-hero-image:url(\'/images/product-photos/vegas-the-show/vegas-the-show-hero.webp\');--mobile-hero-position:center center">'
if old not in s and 'hero-media vs-hero-safe' not in s:
    raise SystemExit('Expected VEGAS hero markup not found')
s=s.replace(old,new,1)
p.write_text(s)

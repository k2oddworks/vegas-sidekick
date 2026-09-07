from pathlib import Path

PAGES = [
    Path('news/soda-stereo-ecos-september-13/index.html'),
    Path('news/jo-koy-live-colosseum-caesars-palace-september-19/index.html'),
    Path('news/backstreet-boys-f1-afterparty-sphere-november-21/index.html'),
]

old = "@media(max-width:800px){.hero-grid{grid-template-columns:1fr}.hero-media{order:-1;min-height:360px;max-height:430px}"
new = "@media(max-width:800px){.hero-grid{grid-template-columns:1fr}.hero-media{order:-1;min-height:360px;max-height:430px}.hero-media img{object-position:center top}"

for path in PAGES:
    text = path.read_text()
    if new in text:
        print(f'already fixed: {path}')
        continue
    if old not in text:
        raise SystemExit(f'expected mobile hero rule not found: {path}')
    path.write_text(text.replace(old, new, 1))
    print(f'fixed: {path}')

from pathlib import Path

p=Path('guides/best-cheap-vegas-shows/index.html')
s=p.read_text(encoding='utf-8')

# Hero: turn existing single-column wrap into text + real-photo collage.
s=s.replace('.g-hero .wrap{position:relative;z-index:2}', '.g-hero .wrap{position:relative;z-index:2;max-width:1180px}.g-hero-grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(360px,.92fr);gap:42px;align-items:center}.g-hero-copy{min-width:0}.g-visuals{display:grid;grid-template-columns:1fr 1fr;grid-template-rows:170px 170px;gap:10px;transform:rotate(-1deg)}.g-shot{position:relative;overflow:hidden;border-radius:18px;border:1px solid rgba(255,255,255,.24);box-shadow:0 18px 50px rgba(0,0,0,.25);background:#261147}.g-shot:first-child{grid-column:1/3}.g-shot img{width:100%;height:100%;object-fit:cover;display:block}.g-shot::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 45%,rgba(13,5,27,.72))}.g-shot-label{position:absolute;left:12px;bottom:10px;z-index:2;font-family:var(--font-display);font-size:.78rem;font-weight:800;color:#fff}.g-shot-price{position:absolute;right:10px;top:10px;z-index:2;background:var(--pink);color:#fff;border-radius:999px;padding:5px 9px;font-family:var(--font-display);font-size:.72rem;font-weight:800}.g-shot:hover img{transform:scale(1.035)}.g-shot img{transition:transform .35s ease}')

# Add responsive rules before closing style.
needle='</style>'
css='''\n  .qa-photo{width:100%;height:118px;object-fit:cover;display:block;border-radius:12px 12px 0 0;margin:-1px -1px 10px;width:calc(100% + 2px)}\n  .benchmark-top3 a{overflow:hidden}\n  @media(max-width:820px){.g-hero-grid{grid-template-columns:1fr;gap:28px}.g-visuals{grid-template-rows:150px 150px;transform:none}.g-hero{padding-top:34px}.g-hero .wrap{max-width:860px}}\n  @media(max-width:520px){.g-visuals{grid-template-rows:130px 130px;gap:8px}.g-shot{border-radius:14px}.g-shot-label{font-size:.68rem}.qa-photo{height:105px}}\n  @media(prefers-reduced-motion:reduce){.g-shot img{transition:none}.g-shot:hover img{transform:none}}\n'''
s=s.replace(needle,css+needle,1)

# Wrap hero text and add collage before hero closes. Match known hero content boundaries.
hero_start='<div class="g-hero">'
if hero_start not in s: hero_start='<section class="g-hero">'
pos=s.find(hero_start)
if pos<0: raise SystemExit('hero not found')
wrap=s.find('<div class="wrap">',pos)
if wrap<0: raise SystemExit('hero wrap not found')
insert_at=wrap+len('<div class="wrap">')
s=s[:insert_at]+'<div class="g-hero-grid"><div class="g-hero-copy">'+s[insert_at:]
# close copy and insert collage just before the first wrap close following g-meta
meta=s.find('class="g-meta"',insert_at)
if meta<0: raise SystemExit('g-meta not found')
meta_close=s.find('</div>',meta)
# g-meta contains spans, so find close after last known meta phrase
marker='All under <b>$50</b>'
mi=s.find(marker,meta)
if mi<0: raise SystemExit('last meta marker not found')
meta_close=s.find('</div>',mi)
collage='''</div><div class="g-visuals" aria-label="Top cheap Vegas show picks">
<a class="g-shot" href="/shows/comedy/jimmy-kimmels-comedy-club/"><img src="/images/jimmy-kimmels-comedy-club-hero.webp" alt="Jimmy Kimmel's Comedy Club in Las Vegas"><span class="g-shot-price">From $27</span><span class="g-shot-label">#1 Jimmy Kimmel's Comedy Club</span></a>
<a class="g-shot" href="/shows/comedy/marc-savard-comedy-hypnosis/"><img src="/images/marc-savard-comedy-hypnosis-hero.jpg" alt="Marc Savard Comedy Hypnosis in Las Vegas"><span class="g-shot-price">From $28</span><span class="g-shot-label">#2 Marc Savard</span></a>
<a class="g-shot" href="/shows/magic/allstars-of-magic/"><img src="/images/allstars-of-magic-hero.jpg" alt="Allstars of Magic in Las Vegas"><span class="g-shot-price">From $31</span><span class="g-shot-label">#3 Allstars of Magic</span></a>
</div></div>'''
s=s[:meta_close+6]+collage+s[meta_close+6:]

# Add real photos to benchmark top-three shortcut cards by matching link targets.
repls={
'<a href="/shows/comedy/jimmy-kimmels-comedy-club/">':'<a href="/shows/comedy/jimmy-kimmels-comedy-club/"><img class="qa-photo" src="/images/jimmy-kimmels-comedy-club-hero.webp" alt="Jimmy Kimmel’s Comedy Club">',
'<a href="/shows/comedy/marc-savard-comedy-hypnosis/">':'<a href="/shows/comedy/marc-savard-comedy-hypnosis/"><img class="qa-photo" src="/images/marc-savard-comedy-hypnosis-hero.jpg" alt="Marc Savard Comedy Hypnosis">',
'<a href="/shows/magic/allstars-of-magic/">':'<a href="/shows/magic/allstars-of-magic/"><img class="qa-photo" src="/images/allstars-of-magic-hero.jpg" alt="Allstars of Magic">'
}
# Only alter first occurrence after benchmark-top3, not ranking cards later.
top=s.find('benchmark-top3')
if top<0: raise SystemExit('benchmark-top3 not found')
for old,new in repls.items():
    i=s.find(old,top)
    if i<0: raise SystemExit('top3 link not found '+old)
    s=s[:i]+new+s[i+len(old):]

# Sanity checks
assert s.count('class="g-shot"')==3
assert s.count('class="qa-photo"')==4  # CSS + three images
assert '/images/jimmy-kimmels-comedy-club-hero.webp' in s
assert '/images/marc-savard-comedy-hypnosis-hero.jpg' in s
assert '/images/allstars-of-magic-hero.jpg' in s
p.write_text(s,encoding='utf-8')
print('Cheap guide visual upgrade applied')

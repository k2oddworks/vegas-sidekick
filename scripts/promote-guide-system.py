from pathlib import Path
import re, json

ROOT=Path('.')
GUIDES=ROOT/'guides'
PROFILE='/about/kris-kidd/'
AVATAR='/images/kris-kidd.webp'

EMAIL_TEXT='Email not required. Want occasional Vegas updates? Join our list.'

BENCHMARK_CSS='''<style id="guide-benchmark-v2">
:root{--gb-ink:#171225;--gb-muted:#6c6883;--gb-purple:#6d28d9;--gb-pink:#ff2e7e;--gb-lime:#c6f22e;--gb-soft:#f6f3fb;--gb-line:#e8e3f0}
.guide-sticky{position:sticky;top:0;z-index:80;background:rgba(255,255,255,.96);backdrop-filter:blur(12px);border-bottom:1px solid var(--gb-line);overflow:auto;white-space:nowrap}.guide-sticky .wrap{display:flex;gap:20px;padding-top:12px;padding-bottom:12px;font-size:12px;font-weight:800}.guide-quick{margin:34px 0 26px;padding:26px;border-radius:22px;background:linear-gradient(135deg,#efe9ff,#fff0f6);border:1px solid #ddd2f6}.guide-quick .k{font-size:11px;font-weight:800;color:var(--gb-purple);letter-spacing:.12em;text-transform:uppercase}.guide-quick h2{font-family:'Plus Jakarta Sans',sans-serif;font-size:clamp(1.8rem,4vw,2.5rem);line-height:1.05;margin:9px 0}.guide-quick p{margin:0;color:#4d4658}.guide-mini{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:18px}.guide-mini a{display:block;background:#fff;border:1px solid var(--gb-line);border-radius:14px;padding:14px}.guide-mini small{display:block;font-size:10px;font-weight:800;color:var(--gb-purple);text-transform:uppercase}.guide-mini strong{display:block;margin-top:5px}.guide-compare-wrap{margin:24px 0 34px;overflow:auto}.guide-compare{width:100%;border-collapse:collapse;font-size:13px;min-width:620px}.guide-compare th,.guide-compare td{text-align:left;padding:12px;border-bottom:1px solid var(--gb-line)}.guide-compare th{font-size:10px;color:var(--gb-muted);text-transform:uppercase;letter-spacing:.06em}.guide-method{margin:42px 0;padding:26px;border-radius:20px;background:#150a22;color:#fff}.guide-method h2{color:#fff;margin-top:0}.guide-method p{color:#d7cce0;margin-bottom:0}.guide-email-note{margin:26px 0;padding:22px;border-radius:18px;background:linear-gradient(135deg,#6d28d9,#ff2e7e);color:#fff}.guide-email-note strong{font-family:'Plus Jakarta Sans',sans-serif;display:block;font-size:1.2rem;margin-bottom:5px}.guide-email-note p{margin:0;color:#fff}.guide-related{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:22px 0}.guide-related a{background:var(--gb-soft);border:1px solid var(--gb-line);border-radius:15px;padding:17px;font-weight:800}.card,.rank-card{transition:transform .2s,box-shadow .2s,border-color .2s}.card:hover,.rank-card:hover{transform:translateY(-2px);box-shadow:0 14px 34px rgba(23,18,37,.1);border-color:#cbb9ef}
@media(max-width:720px){.guide-mini,.guide-related{grid-template-columns:1fr}.guide-quick{padding:21px}.guide-sticky .wrap{width:max-content}.card{border-radius:20px!important}}
@media(prefers-reduced-motion:reduce){.card,.rank-card{transition:none!important}.card:hover,.rank-card:hover{transform:none}}
</style>'''

def strip_preview(s):
    s=re.sub(r'<div class="preview">.*?</div>','',s,count=1,flags=re.S)
    s=s.replace('<meta name="robots" content="noindex,nofollow">','<meta name="robots" content="index,follow,max-image-preview:large">')
    return s

def promote_hub():
    src=(ROOT/'preview/guides-concept/index.html').read_text(encoding='utf-8')
    s=strip_preview(src)
    s=s.replace('<title>Guides Hub Concept | Vegas Sidekick Preview</title>','<title>Las Vegas Show Guides — Picks by Budget, Vibe & Group | Vegas Sidekick</title><meta name="description" content="Las Vegas show guides by a local ticketing expert: best shows for first-timers, families, couples, budget trips, Cirque fans, magic fans and more."><link rel="canonical" href="https://vegassidekick.com/guides/">')
    s=s.replace('/preview/guide-first-timers-concept/','/guides/best-shows-for-first-timers/')
    s=s.replace('No daily spam. No email wall.', EMAIL_TEXT)
    schema='<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@type":"CollectionPage","name":"Vegas Sidekick Guides","url":"https://vegassidekick.com/guides/","description":"Las Vegas show guides by budget, audience, occasion and category.","author":{"@type":"Person","@id":"https://vegassidekick.com/about/kris-kidd/#kris","name":"Kris Kidd","url":"https://vegassidekick.com/about/kris-kidd/","image":"https://vegassidekick.com/images/kris-kidd.webp"}})+'</script>'
    s=s.replace('</head>',schema+'</head>',1)
    (GUIDES/'index.html').write_text(s,encoding='utf-8')

def parse_cards(s):
    cards=[]
    for m in re.finditer(r'<article class="card">(.*?)</article>',s,re.S):
        block=m.group(1)
        def grab(pat, default=''):
            mm=re.search(pat,block,re.S|re.I); return re.sub('<[^>]+>','',mm.group(1)).strip() if mm else default
        hrefm=re.search(r'<a class="thumb" href="([^"]+)"',block)
        imgm=re.search(r'<img src="([^"]+)"[^>]*alt="([^"]*)"',block)
        price=grab(r'<span class="price-badge">(.*?)</span>').replace('From','').strip()
        cards.append({
            'block':'<article class="card">'+block+'</article>',
            'href':hrefm.group(1) if hrefm else '#',
            'img':imgm.group(1) if imgm else '',
            'alt':imgm.group(2) if imgm else '',
            'name':grab(r'<div class="c-name">(.*?)</div>'),
            'venue':grab(r'<div class="c-venue">(.*?)</div>'),
            'blurb':grab(r'<p class="c-blurb">(.*?)</p>'),
            'tag':grab(r'<div class="c-tag">(.*?)</div>'),
            'price':price
        })
    return cards

def first_timer_live():
    live=(GUIDES/'best-shows-for-first-timers/index.html').read_text(encoding='utf-8')
    cards=parse_cards(live)
    by_name={c['name']:c for c in cards}
    vegas=next((c for c in cards if c['name'].startswith('VEGAS! The Show')),None)
    if not vegas: raise SystemExit('VEGAS! The Show card not found')
    ordered=[vegas]+[c for c in cards if c is not vegas]
    # Renumber and rebuild existing card blocks, preserving all copy.
    rebuilt=[]
    for i,c in enumerate(ordered,1):
        b=re.sub(r'<div class="rank">\d+</div>',f'<div class="rank">{i}</div>',c['block'],count=1)
        rebuilt.append(b)
    # ItemList order mirrors visible ranking.
    list_items=[]
    for i,c in enumerate(ordered,1):
        list_items.append({"@type":"ListItem","position":i,"name":c['name'],"url":"https://vegassidekick.com"+c['href']})
    live=re.sub(r'("@type"\s*:\s*"ItemList".*?"itemListElement"\s*:\s*)\[.*?\](\s*\})',lambda m:m.group(1)+json.dumps(list_items,ensure_ascii=False)+m.group(2),live,count=1,flags=re.S)
    # Replace all ranking cards in place.
    matches=list(re.finditer(r'<article class="card">.*?</article>',live,re.S))
    if not matches: raise SystemExit('No first timer cards found')
    start,end=matches[0].start(),matches[-1].end()
    live=live[:start]+'\n'.join(rebuilt)+live[end:]
    # Rewrite first-trip intro claims to match #1 and remove urgency/no-fee language.
    live=re.sub(r'<p class="lede">.*?</p>','<p class="lede">If it is your first trip and you want the show that most directly explains why Las Vegas became Las Vegas, start with <strong>VEGAS! The Show</strong>. It is a musical walk through the city’s entertainment history — Rat Pack, showgirls, lounge acts and the old Strip — before you branch out into Cirque, magic or something stranger.</p>',live,count=1,flags=re.S)
    live=re.sub(r'<p class="intro">.*?</p>','<p class="intro">This ranking is about fit for a first trip, not simply production budget. <strong>VEGAS! The Show is #1</strong> because it gives first-timers the clearest piece of Las Vegas context in one night. The giant spectacles still rank highly when you want the bigger splurge.</p>',live,count=1,flags=re.S)
    # Add benchmark chrome after hero.
    hero_end=live.find('</header>')+len('</header>')
    sticky='''<nav class="guide-sticky"><div class="wrap"><a href="#quick-answer">Quick answer</a><a href="#compare">Compare</a><a href="#ranking">Full ranking</a><a href="#faq">FAQ</a></div></nav>'''
    live=live[:hero_end]+sticky+live[hero_end:]
    quick=f'''<section id="quick-answer"><div class="guide-quick"><div class="k">🌵 The quick answer</div><h2>For a first Vegas trip, I’d start with VEGAS! The Show.</h2><p>It is the one pick on this list whose whole job is explaining the entertainment history of Las Vegas. If you want the giant once-in-a-trip spectacle instead, go straight to “O.”</p><div class="guide-mini"><a href="{ordered[0]['href']}"><small>My #1 first-trip pick</small><strong>{ordered[0]['name']}</strong>{ordered[0]['venue']} · {ordered[0]['price']}</a><a href="{ordered[1]['href']}"><small>Iconic splurge</small><strong>{ordered[1]['name']}</strong>{ordered[1]['venue']} · {ordered[1]['price']}</a><a href="{ordered[2]['href']}"><small>Adults</small><strong>{ordered[2]['name']}</strong>{ordered[2]['venue']} · {ordered[2]['price']}</a></div></div></section>'''
    compare='<section id="compare"><h2>Compare the first five.</h2><div class="guide-compare-wrap"><table class="guide-compare"><thead><tr><th>Rank</th><th>Show</th><th>From</th><th>Venue</th><th>Best fit</th></tr></thead><tbody>'
    for i,c in enumerate(ordered[:5],1): compare+=f'<tr><td>#{i}</td><td><strong>{c["name"]}</strong></td><td>{c["price"]}</td><td>{c["venue"]}</td><td>{c["tag"]}</td></tr>'
    compare+='</tbody></table></div></section>'
    mainmarker='<main><div class="wrap">'
    live=live.replace(mainmarker,mainmarker+quick+compare+'<div id="ranking"></div>',1)
    method='<section class="guide-method"><h2>How I rank a first-trip show.</h2><p>I care about what the show adds to a limited first Vegas itinerary: how specifically Vegas it feels, how broadly it lands, price, production value and whether I would actually give up one of my own nights for it.</p></section><div class="guide-email-note"><strong>Want the useful Vegas updates?</strong><p>'+EMAIL_TEXT+'</p></div>'
    # Before FAQ if present, otherwise before footer.
    faqpos=live.lower().find('faqpage')
    live=live.replace('</main>',method+'</main>',1) if '</main>' in live else live
    live=live.replace('No email wall.',EMAIL_TEXT).replace('no email wall.',EMAIL_TEXT)
    live=live.replace('</head>',BENCHMARK_CSS+'</head>',1)
    (GUIDES/'best-shows-for-first-timers/index.html').write_text(live,encoding='utf-8')

def enhance_guide(path):
    p=GUIDES/path/'index.html'
    s=p.read_text(encoding='utf-8')
    cards=parse_cards(s)
    if not cards: return
    if 'guide-benchmark-v2' in s: return
    # add sticky nav after hero
    hero_end=s.find('</header>')
    if hero_end!=-1:
        hero_end+=len('</header>')
        s=s[:hero_end]+'<nav class="guide-sticky"><div class="wrap"><a href="#quick-answer">Quick answer</a><a href="#compare">Compare</a><a href="#ranking">Full ranking</a><a href="#faq">FAQ</a></div></nav>'+s[hero_end:]
    top=cards[:3]
    q='<section id="quick-answer"><div class="guide-quick"><div class="k">🌵 The quick answer</div><h2>'+top[0]['name']+' is my #1 pick here.</h2><p>'+top[0]['blurb']+'</p><div class="guide-mini">'
    labels=['#1 pick','#2 pick','#3 pick']
    for lab,c in zip(labels,top): q+=f'<a href="{c["href"]}"><small>{lab}</small><strong>{c["name"]}</strong>{c["venue"]} · {c["price"]}</a>'
    q+='</div></div></section>'
    compare='<section id="compare"><h2>Compare the top picks.</h2><div class="guide-compare-wrap"><table class="guide-compare"><thead><tr><th>Rank</th><th>Show</th><th>From</th><th>Venue</th><th>Best fit</th></tr></thead><tbody>'
    for i,c in enumerate(cards[:5],1): compare+=f'<tr><td>#{i}</td><td><strong>{c["name"]}</strong></td><td>{c["price"]}</td><td>{c["venue"]}</td><td>{c["tag"]}</td></tr>'
    compare+='</tbody></table></div></section><div id="ranking"></div>'
    marker='<main><div class="wrap">'
    if marker in s: s=s.replace(marker,marker+q+compare,1)
    else:
        marker='<main>'
        s=s.replace(marker,marker+'<div class="wrap">'+q+compare+'</div>',1)
    method='<section class="guide-method"><h2>How I make this ranking.</h2><p>The order is based on fit for this specific guide, not who has the biggest ad budget. I weigh the show itself, price, audience fit, venue context and the downside I would tell a friend before they bought.</p></section><div class="guide-email-note"><strong>Want the useful Vegas updates?</strong><p>'+EMAIL_TEXT+'</p></div>'
    s=s.replace('</main>',method+'</main>',1) if '</main>' in s else s
    s=s.replace('No daily spam. No email wall.','No daily spam. '+EMAIL_TEXT).replace('No email wall.',EMAIL_TEXT).replace('no email wall.',EMAIL_TEXT)
    s=s.replace('</head>',BENCHMARK_CSS+'</head>',1)
    p.write_text(s,encoding='utf-8')

promote_hub()
first_timer_live()
for g in ['best-adult-shows','best-cheap-vegas-shows','best-cirque-shows','best-magic-shows','best-shows-for-couples','best-shows-for-families','best-tribute-shows']:
    enhance_guide(g)

# Validation
for p in [GUIDES/'index.html']+list(GUIDES.glob('*/index.html')):
    s=p.read_text(encoding='utf-8')
    for block in re.findall(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',s,re.S|re.I):
        json.loads(block.strip())
    assert 'No email wall' not in s and 'no email wall' not in s, p
assert 'VEGAS! The Show' in (GUIDES/'best-shows-for-first-timers/index.html').read_text(encoding='utf-8')
assert '<div class="rank">1</div>' in (GUIDES/'best-shows-for-first-timers/index.html').read_text(encoding='utf-8')
print('Guide system promoted and validated.')

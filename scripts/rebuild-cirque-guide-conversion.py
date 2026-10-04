from pathlib import Path
import re
p=Path(__file__).resolve().parents[1]/'guides/best-cirque-shows/index.html'
s=p.read_text()
# Current four-show ranking: KÀ, Mystère, Michael Jackson ONE, O.
rank=[
('KÀ','/shows/cirque/ka/','/images/product-photos/ka/ka-hero.jpg','$80','MGM Grand','Kris Kidd’s #1 pick','The one I’d choose first. Huge moving-stage spectacle, martial-arts energy and a production that feels built for Vegas.'),
('Mystère','/shows/cirque/mystere/','/images/product-photos/mystere/mystere-hero.jpg','$84','Treasure Island','The original Vegas Cirque','Colorful, physical and easy to recommend when you want classic Cirque without needing a story to follow.'),
('Michael Jackson ONE','/shows/cirque/michael-jackson-one/','/images/product-photos/michael-jackson-one/mj-one-hero.jpg','$163','Mandalay Bay','Best for music + energy','The easiest pick for an MJ fan: familiar songs, big sound and Cirque staging built around the music.'),
('“O”','/shows/cirque/o/','/images/product-photos/o/o-hero.jpg','$156','Bellagio','Best aquatic spectacle','The water production is still singular in Las Vegas. Choose it when visual artistry and scale matter most.')]
# Metadata/schema accuracy.
s=s.replace('All four current Cirque du Soleil shows in Las Vegas ranked by experience, spectacle and fit, with prices and practical tradeoffs for choosing one.','All four current Cirque du Soleil shows in Las Vegas ranked by Kris Kidd, with real starting prices, show photos and practical help choosing the right Cirque night.')
s=s.replace('All four current Cirque du Soleil shows in Las Vegas ranked — the icon, the crowd-pleaser, the epic and the original. Real prices and which is right for you.','KÀ is Kris Kidd’s #1 Cirque pick in Las Vegas. Compare KÀ, Mystère, Michael Jackson ONE and O with real starting prices and show photos.')
s=s.replace('"dateModified": "2026-09-06"','"dateModified": "2026-09-15"')
# Replace ItemList block positions/names/urls.
block='''<script type="application/ld+json">\n{\n  "@context":"https://schema.org",\n  "@type":"ItemList",\n  "name":"Best Cirque du Soleil Shows in Las Vegas",\n  "numberOfItems":4,\n  "itemListElement":[%s]\n}\n</script>''' % ','.join('{"@type":"ListItem","position":%d,"name":"%s by Cirque du Soleil","url":"https://vegassidekick.com%s"}'%(i,n.replace('“','').replace('”','').replace('KÀ','KÀ').replace('Mystère','Mystère'),u) for i,(n,u,*_) in enumerate(rank,1))
s=re.sub(r'<script type="application/ld\+json">\s*\{\s*"@context": "https://schema.org",\s*"@type": "ItemList",[\s\S]*?</script>',block,s,count=1)
# Make the top of the guide visual and conversion-led without inventing new photography.
css='''\n  .cirque-photo-strip{max-width:1120px;margin:34px auto 0;padding:0 22px;display:grid;grid-template-columns:2fr 1fr 1fr;gap:10px}.cirque-photo-strip a{position:relative;overflow:hidden;border-radius:16px;min-height:180px;background:#160a29}.cirque-photo-strip a:first-child{grid-row:span 2;min-height:370px}.cirque-photo-strip img{width:100%;height:100%;object-fit:cover;position:absolute;inset:0;transition:transform .35s}.cirque-photo-strip a:hover img{transform:scale(1.025)}.cirque-photo-strip span{position:absolute;left:12px;bottom:12px;color:#fff;background:rgba(18,6,31,.78);backdrop-filter:blur(8px);border-radius:100px;padding:7px 12px;font-family:var(--font-display);font-size:.72rem;font-weight:800}.buy-btn{display:inline-flex;align-items:center;justify-content:center;background:#FFB000;color:#171225!important;border-radius:10px;padding:10px 15px;font-family:var(--font-display);font-size:.78rem;font-weight:800;margin-top:4px}.rank-pick{border:2px solid rgba(255,176,0,.65);box-shadow:0 14px 34px rgba(23,18,37,.12)}@media(max-width:650px){.cirque-photo-strip{grid-template-columns:1fr 1fr}.cirque-photo-strip a:first-child{grid-column:1/-1;grid-row:auto;min-height:250px}.cirque-photo-strip a{min-height:145px}}\n'''
s=s.replace('</style>',css+'</style>',1)
photos='<div class="cirque-photo-strip">'+''.join(f'<a href="{u}"><img src="{img}" alt="{n} by Cirque du Soleil" loading="lazy"><span>#{i} · {n}</span></a>' for i,(n,u,img,*_) in enumerate(rank,1))+'</div>'
# Insert visual strip immediately after hero.
hero_end=s.find('</section>',s.find('class="g-hero"'))
if hero_end!=-1 and 'cirque-photo-strip' not in s[hero_end:hero_end+500]: s=s[:hero_end+10]+photos+s[hero_end+10:]
# Replace quick answer copy and its three pick cells where present.
s=re.sub(r'"O" is my #1 pick here\.', 'KÀ is my #1 pick here.', s)
s=s.replace('The one to see if you only see one. Performed in, on and above a 1.5-million-gallon pool that transforms from solid stage to deep water in seconds — synchronized swimmers, high divers, aerialists. Twenty-five years on and nothing else in Vegas touches it for pure artistry. Our pick for the best Cirque show in Las Vegas.','If you want my personal pick, it’s KÀ. The moving stage, scale and action make it the Cirque production I’d choose first in Vegas. Mystère is next for classic Cirque, Michael Jackson ONE for music and energy, and O for the aquatic spectacle.')
# Rebuild ranking card region using existing card design + images + amber sales CTA.
cards=''.join(f'''<article class="card{' rank-pick' if i==1 else ''}"><div class="rank">{i}</div><a class="thumb" href="{u}"><img src="{img}" alt="{n} by Cirque du Soleil"><span class="price-badge"><small>FROM</small> {price}</span></a><div class="c-body"><div class="c-tag">{tag}</div><h2 class="c-name">{n}</h2><div class="c-venue">{venue}</div><p class="c-blurb">{blurb}</p><a class="buy-btn" href="{u}">See tickets & show guide →</a></div></article>''' for i,(n,u,img,price,venue,tag,blurb) in enumerate(rank,1))
# Replace all consecutive ranking cards between first card and next divider/section if recognizable.
start=s.find('<div class="card"')
if start==-1: start=s.find('<article class="card"')
if start!=-1:
    end=s.find('<div class="divider"',start)
    if end!=-1: s=s[:start]+cards+s[end:]
# Visible full-name take language.
s=s.replace("SPIKE'S TAKE","KRIS KIDD'S TAKE").replace("Spike's take","Kris Kidd's take")
# FAQ recommendation should reflect Kris's ranking, not consensus O claim.
s=s.replace('"O" at the Bellagio is the consensus best — the aquatic masterpiece performed in, on and above a 1.5-million-gallon pool. It\'s the most technically ambitious and the one to see if you only see one. Michael Jackson ONE is the best pick if you want music and energy over pure artistry.','KÀ at MGM Grand is Kris Kidd’s #1 pick for its enormous moving stage, action and scale. Mystère is his next pick for classic Cirque, followed by Michael Jackson ONE for music and energy, then O for its aquatic spectacle.')
p.write_text(s)

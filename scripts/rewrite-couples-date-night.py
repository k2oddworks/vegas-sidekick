from pathlib import Path
import re

p=Path('guides/best-shows-for-couples/index.html')
s=p.read_text(encoding='utf-8')

TITLE='Best Vegas Date-Night Shows 2026: 10 Picks | Vegas Sidekick'
DESC='The 10 best Las Vegas date-night shows for couples in 2026 — funny, sexy, classic Vegas, magic and big spectacle. Ranked by a Las Vegas local with real starting prices and one honest downside for every pick.'

s=re.sub(r'<title>.*?</title>', f'<title>{TITLE}</title>', s, count=1, flags=re.S)
s=re.sub(r'<meta name="description" content="[^"]*"\s*/?>', f'<meta name="description" content="{DESC}" />', s, count=1)
s=re.sub(r'<meta property="og:title" content="[^"]*"\s*/?>', '<meta property="og:title" content="Best Vegas Date-Night Shows 2026: 10 Picks" />', s, count=1)
s=re.sub(r'<meta property="og:description" content="[^"]*"\s*/?>', '<meta property="og:description" content="Ten Vegas date-night picks for couples — from Zombie Burlesque and Rouge to classic Vegas, magic, Cirque and a full-send adults-only night." />', s, count=1)
s=re.sub(r'<meta property="og:image" content="[^"]*"\s*/?>', '<meta property="og:image" content="https://vegassidekick.com/images/zombie-burlesque-hero.jpg" />', s, count=1)
s=re.sub(r'<meta name="twitter:title" content="[^"]*"\s*/?>', '<meta name="twitter:title" content="Best Vegas Date-Night Shows 2026: 10 Picks" />', s, count=1)
s=re.sub(r'<meta name="twitter:description" content="[^"]*"\s*/?>', '<meta name="twitter:description" content="10 Las Vegas date-night shows ranked for couples — fun, sexy, classic, magical and spectacular." />', s, count=1)
s=re.sub(r'<meta name="twitter:image" content="[^"]*"\s*/?>', '<meta name="twitter:image" content="https://vegassidekick.com/images/zombie-burlesque-hero.jpg" />', s, count=1)

article_schema='''<script type="application/ld+json">
{
  "@context":"https://schema.org",
  "@type":"Article",
  "headline":"Best Vegas Date-Night Shows 2026: 10 Picks",
  "description":"The best Las Vegas date-night shows for couples in 2026, ranked by a Las Vegas local with current starting prices and an honest downside for every pick.",
  "image":"https://vegassidekick.com/images/zombie-burlesque-hero.jpg",
  "author":{"@type":"Person","@id":"https://vegassidekick.com/about/kris-kidd/#kris","name":"Kris Kidd","url":"https://vegassidekick.com/about/kris-kidd/","image":"https://vegassidekick.com/images/kris-kidd.webp"},
  "publisher":{"@type":"Organization","name":"Vegas Sidekick","logo":{"@type":"ImageObject","url":"https://vegassidekick.com/images/logo-badge.png"}},
  "datePublished":"2026-07-21",
  "dateModified":"2026-09-06",
  "mainEntityOfPage":"https://vegassidekick.com/guides/best-shows-for-couples/"
}
</script>'''
item_schema='''<script type="application/ld+json">
{
  "@context":"https://schema.org",
  "@type":"ItemList",
  "name":"Best Vegas Date-Night Shows for Couples",
  "numberOfItems":10,
  "itemListElement":[
    {"@type":"ListItem","position":1,"name":"Zombie Burlesque","url":"https://vegassidekick.com/shows/adult/zombie-burlesque/"},
    {"@type":"ListItem","position":2,"name":"Rouge","url":"https://vegassidekick.com/shows/adult/rouge/"},
    {"@type":"ListItem","position":3,"name":"VEGAS! The Show","url":"https://vegassidekick.com/shows/music/vegas-the-show/"},
    {"@type":"ListItem","position":4,"name":"Now You See Me LIVE","url":"https://vegassidekick.com/shows/magic/now-you-see-me-live/"},
    {"@type":"ListItem","position":5,"name":"O by Cirque du Soleil","url":"https://vegassidekick.com/shows/cirque/o/"},
    {"@type":"ListItem","position":6,"name":"X Country","url":"https://vegassidekick.com/shows/adult/x-country/"},
    {"@type":"ListItem","position":7,"name":"Absinthe","url":"https://vegassidekick.com/shows/spectaculars/absinthe/"},
    {"@type":"ListItem","position":8,"name":"Atomic Saloon Show","url":"https://vegassidekick.com/shows/adult/atomic-saloon/"},
    {"@type":"ListItem","position":9,"name":"Michael Jackson ONE","url":"https://vegassidekick.com/shows/cirque/michael-jackson-one/"},
    {"@type":"ListItem","position":10,"name":"Magic Mike Live","url":"https://vegassidekick.com/shows/adult/magic-mike-live/"}
  ]
}
</script>'''
faq_schema='''<script type="application/ld+json">
{
  "@context":"https://schema.org",
  "@type":"FAQPage",
  "mainEntity":[
    {"@type":"Question","name":"What is the best Vegas show for a date night?","acceptedAnswer":{"@type":"Answer","text":"Zombie Burlesque is our top overall date-night pick because it mixes comedy, live music, variety and burlesque without turning the night into a formal splurge. If you want something sexier, choose Rouge. If you want classic Las Vegas, choose VEGAS! The Show."}},
    {"@type":"Question","name":"What is the best romantic show in Las Vegas?","acceptedAnswer":{"@type":"Answer","text":"O by Cirque du Soleil at Bellagio is the strongest romantic splurge on this list. It is dreamlike, visually beautiful and built around a huge aquatic stage, but it also has the highest starting price here."}},
    {"@type":"Question","name":"What is a good affordable Vegas date-night show?","acceptedAnswer":{"@type":"Answer","text":"Zombie Burlesque starts at $51, Rouge at $54 and VEGAS! The Show at $63. All three give you a distinct Vegas night without starting in triple digits. Check your date because prices can move by performance and seat."}},
    {"@type":"Question","name":"What is the best adults-only Vegas show for couples?","acceptedAnswer":{"@type":"Answer","text":"Rouge is the straightest sexy-date pick. Absinthe and Atomic Saloon add raunchy comedy and circus acts, X Country is a topless country revue, and Magic Mike Live is the full-send male-revue option. Match the show to both people, not just one."}},
    {"@type":"Question","name":"What is the best first-time Vegas date-night show?","acceptedAnswer":{"@type":"Answer","text":"VEGAS! The Show is the easiest first-trip pick if you want classic Las Vegas in one night. Now You See Me LIVE is better if you both like magic, and Michael Jackson ONE is the better call if music is the shared interest."}}
  ]
}
</script>'''

s=re.sub(r'<script type="application/ld\+json">\s*\{(?:(?!</script>).)*?"@type"\s*:\s*"Article"(?:(?!</script>).)*?</script>', article_schema, s, count=1, flags=re.S)
s=re.sub(r'<script type="application/ld\+json">\s*\{(?:(?!</script>).)*?"@type"\s*:\s*"ItemList"(?:(?!</script>).)*?</script>', item_schema, s, count=1, flags=re.S)
s=re.sub(r'<script type="application/ld\+json">\s*\{(?:(?!</script>).)*?"@type"\s*:\s*"FAQPage"(?:(?!</script>).)*?</script>', faq_schema, s, count=1, flags=re.S)

hero='''<header class="g-hero"><div class="wrap"><div class="guide-hero-grid"><div class="guide-hero-copy">
  <span class="g-eyebrow">🌵 Date Night, Actually Handled</span>
  <h1>The Best Vegas <span class="accent">Date-Night Shows</span></h1>
  <p class="g-sub">10 picks for two people who want a genuinely fun night — sexy, funny, classic Vegas, magic and big spectacle. Not every great date has to be romantic.</p>
  <div class="g-meta">
    <span class="kris-byline"><img src="/images/kris-kidd.webp" alt="Kris Kidd" width="28" height="28">By <a href="/about/kris-kidd/">Kris Kidd</a></span>
    <span>Updated <b>Sep 2026</b></span><span><b>10</b> shows</span><span>From <b>$51</b></span><span>Fun → <b>Full send</b></span>
  </div>
</div><div class="guide-hero-visuals" aria-label="Photos of the top three date-night picks">
  <a class="guide-hero-shot" href="/shows/adult/zombie-burlesque/"><img src="/images/zombie-burlesque-hero.jpg" alt="Zombie Burlesque at V Theater"><span class="guide-hero-price">From $51</span><span class="guide-hero-label">#1 Zombie Burlesque</span></a>
  <a class="guide-hero-shot" href="/shows/adult/rouge/"><img src="/images/rouge-hero.webp" alt="Rouge at The STRAT Theater"><span class="guide-hero-price">From $54</span><span class="guide-hero-label">#2 Rouge</span></a>
  <a class="guide-hero-shot" href="/shows/music/vegas-the-show/"><img src="/images/vegas-the-show-hero.webp" alt="VEGAS! The Show at Saxe Theater"><span class="guide-hero-price">From $63</span><span class="guide-hero-label">#3 VEGAS! The Show</span></a>
</div></div></div></header>'''
s=re.sub(r'<header class="g-hero">.*?</header>', hero, s, count=1, flags=re.S)

quick='''<section id="quick-answer"><div class="guide-quick"><div class="k">🌵 The quick answer</div><h2>Zombie Burlesque is my #1 date-night pick.</h2><p>It has the right Vegas mix for a night out together: funny, weird, sexy, musical and not remotely formal. You get a live band, comedy, variety acts and burlesque in one 75-minute show, and the $51 starting price leaves room for drinks or dinner. <strong>The downside:</strong> the campy zombie premise is the whole point. If one of you wants elegant romance, pick “O” instead.</p><div class="guide-mini">
<a href="/shows/adult/zombie-burlesque/"><img class="qa-photo" src="/images/zombie-burlesque-hero.jpg" alt="Zombie Burlesque at V Theater"><small>#1 · Best overall date</small><strong>Zombie Burlesque</strong><span class="mini-detail">V Theater · Planet Hollywood · From $51</span></a>
<a href="/shows/adult/rouge/"><img class="qa-photo" src="/images/rouge-hero.webp" alt="Rouge at The STRAT Theater"><small>#2 · Best sexy date</small><strong>Rouge</strong><span class="mini-detail">The STRAT Theater · From $54</span></a>
<a href="/shows/music/vegas-the-show/"><img class="qa-photo" src="/images/vegas-the-show-hero.webp" alt="VEGAS! The Show at Saxe Theater"><small>#3 · Best classic Vegas date</small><strong>VEGAS! The Show</strong><span class="mini-detail">Saxe Theater · Planet Hollywood · From $63</span></a>
</div></div></section>
<section id="compare"><h2>Compare the top five.</h2><div class="guide-compare-wrap"><table class="guide-compare"><thead><tr><th>Show</th><th>Best for</th><th>From</th><th>Know before you go</th></tr></thead><tbody>
<tr><td><a href="/shows/adult/zombie-burlesque/"><strong>Zombie Burlesque</strong></a></td><td>Fun, weird date</td><td>$51</td><td>Campy burlesque comedy, not candlelight romance</td></tr>
<tr><td><a href="/shows/adult/rouge/"><strong>Rouge</strong></a></td><td>Sexy date</td><td>$54</td><td>Topless throughout; 18+</td></tr>
<tr><td><a href="/shows/music/vegas-the-show/"><strong>VEGAS! The Show</strong></a></td><td>First Vegas trip</td><td>$63</td><td>Proudly old-school, not cutting-edge</td></tr>
<tr><td><a href="/shows/magic/now-you-see-me-live/"><strong>Now You See Me LIVE</strong></a></td><td>Magic fans</td><td>$72</td><td>Big franchise spectacle, less intimate than close-up magic</td></tr>
<tr><td><a href="/shows/cirque/o/"><strong>“O”</strong></a></td><td>Romantic splurge</td><td>$156</td><td>Highest starting price on this list</td></tr>
</tbody></table></div></section><div id="ranking"></div>'''
s=re.sub(r'<section id="quick-answer">.*?<div id="ranking"></div>', quick, s, count=1, flags=re.S)

cards=[
('1','/shows/adult/zombie-burlesque/','/images/zombie-burlesque-hero.jpg','Zombie Burlesque at V Theater','$51','Best Overall Date · Comedy + Burlesque','Zombie Burlesque','V Theater · Planet Hollywood','A 1950s zombie comedy musical with a live band, variety acts and burlesque. It gives you plenty to laugh about together without making the night feel like a formal “romantic” production. <b>Downside:</b> it is intentionally campy and weird. If zombie jokes or burlesque are a miss for either of you, move on.','See Zombie Burlesque →'),
('2','/shows/adult/rouge/','/images/rouge-hero.webp','Rouge at The STRAT Theater','$54','Best Sexy Date · 18+','Rouge','The STRAT Theater · The STRAT','Rouge is the cleanest answer when the point of the night is to be sexy. It is an 85-minute topless production with polished choreography and a more adult-night-out feel than a traditional Vegas spectacular. <b>Downside:</b> it is topless throughout and strictly 18+. This is not the show to surprise someone with.','See Rouge →'),
('3','/shows/music/vegas-the-show/','/images/vegas-the-show-hero.webp','VEGAS! The Show at Saxe Theater','$63','Best Classic Vegas Date · All Ages','VEGAS! The Show','Saxe Theater · Planet Hollywood','Showgirls, live music and old-school Las Vegas spectacle make this a strong date when you want the night to feel unmistakably Vegas. It also works especially well on a first trip because you get the city’s entertainment history without needing homework. <b>Downside:</b> the throwback style is the appeal. If you want giant modern effects, choose something else.','See VEGAS! The Show →'),
('4','/shows/magic/now-you-see-me-live/','/images/now-you-see-me-live-hero.webp','Now You See Me LIVE at MGM Grand','$72','Best Magic Date · Shared Wow Factor','Now You See Me LIVE','MGM Grand Theater · MGM Grand','The film-franchise setup turns a magic show into a bigger theatrical night with illusions, mind-bending effects and immersive storytelling. It is a good couple pick because you leave with the same question: how did they do that? <b>Downside:</b> this is large-scale, branded spectacle. If you want intimate close-up magic, this is not that show.','See Now You See Me LIVE →'),
('5','/shows/cirque/o/','/images/o-hero.jpg','O by Cirque du Soleil at Bellagio','$156','Best Romantic Splurge · Cirque','“O” by Cirque du Soleil','O Theatre · Bellagio','If you want the beautiful, dress-up, big-night date, this is the one. The aquatic stage and dreamlike pacing make “O” feel more romantic than almost anything else on the Strip. <b>Downside:</b> it starts at $156, so two tickets turn this into a real splurge before dinner or drinks.','See “O” →'),
('6','/shows/adult/x-country/','/images/x-country-og.jpg','X Country at Harrah’s Cabaret','$65','Best Country Date · Late Night 18+','X Country','Harrah’s Cabaret · Harrah’s','Country music, cowboy boots and a topless revue make X Country an easy pick when both of you already know the vibe you want. At 10 PM, it also works naturally as the second half of dinner-and-a-show. <b>Downside:</b> it is a specific lane: topless, country and late. If one of those three is a no, the whole pick falls apart.','See X Country →'),
('7','/shows/spectaculars/absinthe/','/images/absinthe-hero.webp','Absinthe at Caesars Palace','$122','Best Rowdy Laugh · Circus + Comedy','Absinthe','Spiegeltent · Caesars Palace','World-class circus acts happen a few feet from your face while very adult comedy keeps the room loose. This is the date for two people who would rather laugh hard than sit politely. <b>Downside:</b> the humor is crude and the Spiegeltent is intimate. It is also one of the pricier nights here at $122 from.','See Absinthe →'),
('8','/shows/adult/atomic-saloon/','/images/atomic-saloon-hero.webp','Atomic Saloon Show at The Venetian','$90','Best Chaotic Date · Wild West Circus','Atomic Saloon Show','Waterfall Atrium · The Venetian','Atomic Saloon takes circus, comedy and Wild West nonsense and turns it into a rowdy adults-only date night. It feels playful rather than romantic, which is exactly why it works for couples who want energy. <b>Downside:</b> it is risqué and intentionally chaotic. Quiet date night this is not.','See Atomic Saloon →'),
('9','/shows/cirque/michael-jackson-one/','/images/mj-one-hero.jpg','Michael Jackson ONE at Mandalay Bay','$115','Best Music Date · Big Production','Michael Jackson ONE','Mandalay Bay Theatre · Mandalay Bay','Original Michael Jackson recordings, acrobatics and 360-degree staging make this the strongest music-first date on the list. If you both know the songs, the shared nostalgia does a lot of the work for you. <b>Downside:</b> this pick gets much weaker if only one of you cares about Michael Jackson.','See Michael Jackson ONE →'),
('10','/shows/adult/magic-mike-live/','/images/magic-mike-live-hero.jpg','Magic Mike Live at SAHARA','$71','Best Full-Send Adult Date · 18+','Magic Mike Live','MAGIC MIKE LIVE Theater · SAHARA','A purpose-built theater, choreography and live entertainment make this much more produced than a basic male revue. For the right couple, it is the funniest possible “we actually did that in Vegas” night. <b>Downside:</b> both people need to be on board with the male-revue premise. Do not make this a surprise compatibility test.','See Magic Mike Live →')]

def card(c):
    rank,href,img,alt,price,tag,name,venue,blurb,link=c
    return f'''<article class="card"><div class="rank">{rank}</div><a class="thumb" href="{href}"><img src="{img}" alt="{alt}" loading="lazy"><span class="price-badge"><small>From</small> {price}</span></a><div class="c-body"><div class="c-tag">{tag}</div><a href="{href}"><div class="c-name">{name}</div></a><div class="c-venue">{venue}</div><p class="c-blurb">{blurb}</p><a class="c-link" href="{href}">{link}</a></div></article>'''

newsletter='''<section class="guide-newsletter" aria-label="Vegas Sidekick email updates"><div class="nl-kicker">🌵 Spike's Insider List</div><h2>Useful Vegas updates, without the inbox nonsense.</h2><p>Show changes, worthwhile deals and the Vegas stuff I’d actually text a friend about.</p><form class="guide-newsletter-form" novalidate><input type="email" name="email" autocomplete="email" inputmode="email" placeholder="your@email.com" aria-label="Email address" required><button type="submit">Get Vegas Updates</button></form><div class="nl-msg" aria-live="polite"></div><div class="nl-fine">Occasional emails. Unsubscribe anytime.</div></section>'''

ranking='''<p class="lede">The best Vegas date is not automatically the most romantic show. Sometimes it is the one that gives you both the best story afterward.</p>
<p class="intro">So this ranking is built around <b>date-night chemistry</b>: something fun to share, enough Vegas personality to feel worth leaving the hotel room for, and a clear reason to pick it over the other nine. I also say the downside on every one, because “great for couples” means nothing if it is wrong for <em>your</em> couple.</p>
<div class="expert-box"><img src="/images/kris-kidd.webp" alt="Kris Kidd" width="56" height="56" loading="lazy"><div><div class="eb-label">Written by</div><a class="eb-name" href="/about/kris-kidd/">Kris Kidd</a><div class="eb-cred">Las Vegas local since 2005 · Show ticketing since 2006 · Personally seen hundreds of Vegas shows</div></div></div>
<div class="band">💞 Easy wins for two</div>
'''+''.join(card(c) for c in cards[:5])+newsletter+'''<div class="band">🔥 Turn the date-night dial up</div>'''+''.join(card(c) for c in cards[5:])+'''<div class="spike"><span class="em">🌵</span><div><h3>Spike's take</h3><p>If neither of you can decide, book <a href="/shows/adult/zombie-burlesque/" style="color:var(--blue-lt);font-weight:600;">Zombie Burlesque</a>. It is the least serious recommendation on this page, which is exactly why it works. Want sexy instead? <a href="/shows/adult/rouge/" style="color:var(--blue-lt);font-weight:600;">Rouge</a>. Want a first-trip Vegas memory? <a href="/shows/music/vegas-the-show/" style="color:var(--blue-lt);font-weight:600;">VEGAS! The Show</a>. Want the expensive beautiful one? <a href="/shows/cirque/o/" style="color:var(--blue-lt);font-weight:600;">“O”</a>.</p></div></div>
<div id="faq"></div><h2 class="sec-title">Vegas Date-Night Shows — FAQ</h2>
<div class="faq"><h3>What is the best Vegas show for a date night?</h3><p>Zombie Burlesque is my best overall pick because it mixes comedy, live music, variety and burlesque without turning the night into a formal splurge. Rouge is the sexier choice, and VEGAS! The Show is the stronger first-trip choice.</p></div>
<div class="faq"><h3>What is the most romantic show in Las Vegas?</h3><p>“O” by Cirque du Soleil at Bellagio. The aquatic stage and dreamlike production make it the prettiest romantic splurge here. The catch is the price: tickets currently start at $156.</p></div>
<div class="faq"><h3>What is a good date-night show that is not too expensive?</h3><p>Zombie Burlesque starts at $51, Rouge at $54 and VEGAS! The Show at $63. Those are the three best-value date-night starts on this list. Your actual total depends on date and seat.</p></div>
<div class="faq"><h3>What are the best adults-only shows for couples?</h3><p>Rouge for a sexy revue, Absinthe for circus plus dirty comedy, Atomic Saloon for rowdy Wild West chaos, X Country for a late-night country revue, and Magic Mike Live for the full-send male-revue night. Pick the one both people actually want.</p></div>
<div class="faq"><h3>What is the best show for a couple's first Vegas trip?</h3><p>VEGAS! The Show if you want classic Las Vegas, Now You See Me LIVE if you both like magic, or Michael Jackson ONE if music is the shared interest. “O” is the splurge version of the first-trip pick.</p></div>
<p class="intro"><strong>Affiliate disclosure:</strong> Vegas Sidekick may earn a commission when you book through links on this page, at no extra cost to you.</p>
'''

pat=r'<p class="lede">.*?<div class="final">'
if not re.search(pat,s,re.S):
    raise SystemExit('ranking block not found')
s=re.sub(pat, ranking+'<div class="final">', s, count=1, flags=re.S)

# Final CTA copy
s=s.replace('<h2>Found your date night?</h2>','<h2>Found your date-night show?</h2>')
s=s.replace('<p>Browse the full lineup, or check out our other hand-picked guides.</p>','<p>Book the one that fits both of you, or compare the rest of the Vegas lineup.</p>')

# Basic validation
checks=[
    'Best Vegas Date-Night Shows 2026: 10 Picks',
    'Zombie Burlesque is my #1 date-night pick.',
    'Now You See Me LIVE',
    'numberOfItems":10',
    'guide-newsletter-form',
    'Affiliate disclosure:',
]
for x in checks:
    assert x in s, x
assert s.count('<article class="card">') == 10, s.count('<article class="card">')
assert 'a now-closed Cirque production' not in s
assert 'Mad Apple' not in s and 'mad-apple' not in s
p.write_text(s,encoding='utf-8')
print('rewrote Couples guide as 10-show date-night guide')

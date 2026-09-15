from pathlib import Path
import re
root=Path(__file__).resolve().parents[1]

# Rebuild the homepage editorial section cleanly so guide and Dispatch content cannot bleed together.
p=root/'index.html'
s=p.read_text()
start=s.index('<section class="editorial">')
end=s.index('</section>', start)+len('</section>')
section='''<section class="editorial"><div class="wrap">
<h2>Need help choosing?</h2><p class="section-sub">The catalog gets you started. Guides and Dispatch help when the decision needs context.</p>
<div class="edit-grid">
<div class="edit-block"><div class="edit-head"><h3>Vegas show guides</h3><a href="/guides/">All guides →</a></div><div class="mini-list">
<a class="guide-card" href="/guides/best-shows-for-first-timers/"><b>Best Shows for First-Timers</b><p>Where to start when you want one good Vegas show and don't want to spend an hour researching it.</p></a>
<a class="guide-card" href="/guides/best-cheap-vegas-shows/"><b>Best Cheap Vegas Shows</b><p>Budget-friendly shows that still give you a reason to leave the casino floor.</p></a>
<a class="guide-card" href="/guides/best-shows-for-families/"><b>Best Shows for Families</b><p>The useful shortlist when age fit matters as much as price.</p></a>
</div></div>
<div class="edit-block"><div class="edit-head"><h3>Vegas Dispatch</h3><a href="/news/">All stories →</a></div><div class="mini-list">
<a class="mini-card" href="/news/barry-manilow-adds-2027-las-vegas-dates/"><img alt="Barry Manilow" loading="lazy" src="/images/news/barry-manilow-residency-poster.jpg" style="object-position:center 12%"/><span><b>Barry Manilow’s Westgate run now reaches into 2027</b><small>Vegas Dispatch · Residency</small></span></a>
<a class="mini-card" href="/news/oprah-winfrey-aha-sphere-las-vegas/"><img alt="Oprah Winfrey’s AHA at Sphere" loading="lazy" src="/images/news/oprah-winfrey-speaker.jpg"/><span><b>Oprah is taking over Sphere — but this isn’t a concert</b><small>Vegas Dispatch · Sphere</small></span></a>
<a class="mini-card" href="/news/oasis-live-27-las-vegas-allegiant-stadium/"><img alt="Oasis Live ’27 Las Vegas" loading="lazy" src="/images/news/oasis-live-27-las-vegas-wide.jpg"/><span><b>Oasis announce three Allegiant Stadium shows for 2027</b><small>Vegas Dispatch · Concerts</small></span></a>
<a class="mini-card" href="/news/activate-town-square-opens-october-3/"><img alt="Activate at Town Square" loading="lazy" src="/images/news/activate-town-square-hero.webp"/><span><b>Activate opens at Town Square October 3</b><small>Vegas Dispatch · News</small></span></a>
<a class="mini-card" href="/news/donny-osmond-extends-harrahs-residency-through-2027/"><img alt="Donny Osmond" loading="lazy" src="/images/news/donny-osmond-harrahs-2027-hero.webp"/><span><b>Donny Osmond extends Harrah's residency through 2027</b><small>Vegas Dispatch · Residency</small></span></a>
</div></div>
</div></div></section>'''
s=s[:start]+section+s[end:]
p.write_text(s)

# Dispatch page: remove the oversized Featured block so newest story is literally first.
p=root/'news/index.html'
s=p.read_text()
s=re.sub(r'<a href="/news/oprah-winfrey-aha-sphere-las-vegas/" class="featured-article"[\s\S]*?</a><div class="grid-header">','<div class="grid-header">',s,count=1)
# Ensure Barry card is first and the thumbnail crop clearly shows his face.
barry='''<a href="/news/barry-manilow-adds-2027-las-vegas-dates/" class="article-card" data-category="news"><div class="article-card-img"><img src="/images/news/barry-manilow-residency-poster.jpg" alt="Barry Manilow Las Vegas residency" loading="eager" style="object-position:center 12%"></div><div class="article-card-body"><div class="article-card-meta"><span class="article-tag">Residency</span><span class="article-date">Sept. 15, 2026</span></div><h3 class="article-card-title">Barry Manilow's Westgate Run Now Reaches Into 2027</h3></div></a>'''
s=re.sub(r'<a href="/news/barry-manilow-adds-2027-las-vegas-dates/" class="article-card"[\s\S]*?</a>','',s,count=1)
anchor='<div class="articles-grid" id="articles-grid">'
s=s.replace(anchor,anchor+'\n'+barry,1)
# Put Oprah immediately after Barry since it is also Sept. 15 and was previously Featured.
if '/news/oprah-winfrey-aha-sphere-las-vegas/' not in s[s.find(anchor):]:
    oprah='''<a href="/news/oprah-winfrey-aha-sphere-las-vegas/" class="article-card" data-category="news"><div class="article-card-img"><img src="/images/news/oprah-winfrey-speaker.jpg" alt="Oprah Winfrey announces AHA at Sphere Las Vegas" loading="lazy"></div><div class="article-card-body"><div class="article-card-meta"><span class="article-tag">Sphere</span><span class="article-date">Sept. 15, 2026</span></div><h3 class="article-card-title">Oprah Is Taking Over Sphere — But This Isn’t a Concert</h3></div></a>'''
    s=s.replace(barry,barry+'\n'+oprah,1)
p.write_text(s)

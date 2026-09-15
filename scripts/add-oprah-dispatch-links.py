from pathlib import Path
root=Path(__file__).resolve().parents[1]
news=root/'news/index.html'; s=news.read_text()
old='<main class="n-wrap" id="articles-section">'
card='''<main class="n-wrap" id="articles-section"><a href="/news/oprah-winfrey-aha-sphere-las-vegas/" class="featured-article" data-category="news" id="featured-article"><div class="featured-article-img"><img src="/images/news/oprah-winfrey-speaker.jpg" alt="Oprah Winfrey announces AHA at Sphere Las Vegas" loading="eager"><span class="featured-badge">Featured</span></div><div class="featured-article-body"><div class="featured-meta"><span class="featured-tag">Sphere</span><span class="featured-date">September 15, 2026</span></div><h2>Oprah Is Taking Over Sphere — But This Isn’t a Concert</h2><p>AHA brings four immersive live performances to Sphere April 2–4, 2027, built around music, film, sensory effects and the room itself.</p><div class="featured-footer"><span class="featured-author"><img src="/images/kris-kidd.webp" alt="Kris Kidd">By Kris Kidd</span><span class="read-more-link">Read Article →</span></div></div></a>'''
# Demote existing featured Oasis into grid by stripping id/badge and insert it after grid header.
start=s.find('<a href="/news/oasis-live-27-las-vegas-allegiant-stadium/" class="featured-article"')
end=s.find('</a><div class="grid-header">',start)
if start!=-1 and end!=-1:
 oasis=s[start:end+4]
 s=s[:start]+s[end+4:]
 oasis=oasis.replace(' class="featured-article" data-category="rock" id="featured-article"',' class="article-card" data-category="rock"').replace('<span class="featured-badge">Featured</span>','')
 # convert to compact card markup manually for consistency
 oasis='''<a href="/news/oasis-live-27-las-vegas-allegiant-stadium/" class="article-card" data-category="rock"><div class="article-card-img"><img src="/images/news/oasis-live-27-las-vegas-wide.jpg" alt="Oasis Live ’27 Las Vegas" loading="lazy"></div><div class="article-card-body"><div class="article-card-meta"><span class="article-tag">Rock</span><span class="article-date">Sept. 14, 2026</span></div><h3 class="article-card-title">Oasis Announce Three Las Vegas Shows at Allegiant Stadium in 2027</h3></div></a>'''
 marker='<div class="articles-grid" id="articles-grid">'
 s=s.replace(marker,marker+'\n'+oasis,1)
s=s.replace(old,card,1)
news.write_text(s)

home=root/'index.html'; h=home.read_text()
# Add Oprah before Oasis wherever the homepage Dispatch cards begin.
needle='<a href="/news/oasis-live-27-las-vegas-allegiant-stadium/"'
pos=h.find(needle)
if pos!=-1:
 card='''<a href="/news/oprah-winfrey-aha-sphere-las-vegas/" class="dispatch-card"><div class="dispatch-card-img"><img src="/images/news/oprah-winfrey-speaker.jpg" alt="Oprah Winfrey AHA at Sphere Las Vegas" loading="lazy"></div><div class="dispatch-card-body"><span class="dispatch-card-tag">Sphere</span><h3>Oprah Is Taking Over Sphere — But This Isn’t a Concert</h3><p>Four immersive AHA performances arrive April 2–4, 2027.</p></div></a>'''
 h=h[:pos]+card+h[pos:]
else:
 # fallback: place a simple linked feature immediately before closing main
 card='''<section class="dispatch-oprah" style="max-width:1100px;margin:40px auto;padding:0 20px"><a href="/news/oprah-winfrey-aha-sphere-las-vegas/" style="display:block"><img src="/images/news/oprah-winfrey-speaker.jpg" alt="Oprah Winfrey AHA at Sphere Las Vegas" style="width:100%;max-height:420px;object-fit:cover;border-radius:18px"><h2>Oprah Is Taking Over Sphere — But This Isn’t a Concert</h2><p>Four immersive AHA performances arrive April 2–4, 2027.</p></a></section>'''
 h=h.replace('</main>',card+'</main>',1)
home.write_text(h)

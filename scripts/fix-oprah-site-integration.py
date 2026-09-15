from pathlib import Path
root=Path(__file__).resolve().parents[1]

# Oprah article: use the same shared site chrome as current Dispatch benchmark.
p=root/'news/oprah-winfrey-aha-sphere-las-vegas/index.html'
s=p.read_text()
s=s.replace('<script src="/assets/site-header.js"></script><script src="/assets/site-footer.js"></script>', '<script src="/components/header.js?v=14"></script><script src="/components/footer.js?v=14"></script>')
p.write_text(s)

# Homepage: remove accidental giant standalone card, then put newest Dispatch story first
# in the existing compact mini-card list. This is the pattern future Dispatch updates should follow.
p=root/'index.html'; h=p.read_text()
start=h.find('<section class="dispatch-oprah"')
if start!=-1:
    end=h.find('</section>', start)
    if end!=-1: h=h[:start]+h[end+10:]
card='''<a class="mini-card" href="/news/oprah-winfrey-aha-sphere-las-vegas/"><img alt="Oprah Winfrey’s AHA at Sphere" loading="lazy" src="/images/news/oprah-winfrey-speaker.jpg"/><span><b>Oprah is taking over Sphere — but this isn’t a concert</b><small>Vegas Dispatch · Sphere</small></span></a>'''
if card not in h:
    marker='<div class="edit-block"><div class="edit-head"><h3>Vegas Dispatch</h3><a href="/news/">All stories →</a></div><div class="mini-list">'
    if marker not in h: raise SystemExit('Homepage Dispatch marker not found')
    h=h.replace(marker, marker+card, 1)
p.write_text(h)

# Dispatch index: newest story first. Preserve the existing Dispatch design; Oprah becomes
# the current featured story and Oasis moves into the normal article grid.
p=root/'news/index.html'; n=p.read_text()
oprah='/news/oprah-winfrey-aha-sphere-las-vegas/'
if oprah not in n:
    old='<main class="n-wrap" id="articles-section">'
    feature='''<main class="n-wrap" id="articles-section"><a href="/news/oprah-winfrey-aha-sphere-las-vegas/" class="featured-article" data-category="news" id="featured-article"><div class="featured-article-img"><img src="/images/news/oprah-winfrey-speaker.jpg" alt="Oprah Winfrey announces AHA at Sphere Las Vegas" loading="eager"><span class="featured-badge">Featured</span></div><div class="featured-article-body"><div class="featured-meta"><span class="featured-tag">Sphere</span><span class="featured-date">September 15, 2026</span></div><h2>Oprah Is Taking Over Sphere — But This Isn’t a Concert</h2><p>AHA brings four immersive live performances to Sphere April 2–4, 2027, built around music, film, sensory effects and the room itself.</p><div class="featured-footer"><span class="featured-author"><img src="/images/kris-kidd.webp" alt="Kris Kidd">By Kris Kidd</span><span class="read-more-link">Read Article →</span></div></div></a>'''
    a=n.find('<a href="/news/oasis-live-27-las-vegas-allegiant-stadium/" class="featured-article"')
    b=n.find('</a><div class="grid-header">',a)
    if a!=-1 and b!=-1:
        n=n[:a]+n[b+4:]
        grid='<div class="articles-grid" id="articles-grid">'
        oasis='''<a href="/news/oasis-live-27-las-vegas-allegiant-stadium/" class="article-card" data-category="rock"><div class="article-card-img"><img src="/images/news/oasis-live-27-las-vegas-wide.jpg" alt="Oasis Live ’27 Las Vegas" loading="lazy"></div><div class="article-card-body"><div class="article-card-meta"><span class="article-tag">Rock</span><span class="article-date">Sept. 14, 2026</span></div><h3 class="article-card-title">Oasis Announce Three Las Vegas Shows at Allegiant Stadium in 2027</h3></div></a>'''
        n=n.replace(grid,grid+oasis,1)
    if old not in n: raise SystemExit('Dispatch main marker not found')
    n=n.replace(old,feature,1)
p.write_text(n)

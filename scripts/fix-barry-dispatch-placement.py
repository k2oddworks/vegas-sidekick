from pathlib import Path
import re
root=Path(__file__).resolve().parents[1]
url='/news/barry-manilow-adds-2027-las-vegas-dates/'
# Homepage: remove any Barry card accidentally inserted in the guide mini-list, then make Barry the newest Dispatch card.
p=root/'index.html'; s=p.read_text()
# Remove compact Barry link/card wherever it currently appears before the Vegas Dispatch heading.
dispatch_heading=s.find('Vegas Dispatch')
if dispatch_heading>0:
    before=s[:dispatch_heading]; after=s[dispatch_heading:]
    before=re.sub(r'<a[^>]+href="'+re.escape(url)+r'"[\s\S]*?</a>','',before)
    s=before+after
# Remove any existing Barry homepage occurrence so we can insert exactly once in Dispatch.
s=re.sub(r'<a[^>]+href="'+re.escape(url)+r'"[\s\S]*?</a>','',s)
# Find Dispatch mini-list after heading and insert newest story first.
pos=s.find('Vegas Dispatch')
ml=s.find('<div class="mini-list">',pos)
card='''<a class="dispatch-card" href="/news/barry-manilow-adds-2027-las-vegas-dates/"><img src="/images/news/barry-manilow-las-vegas-piano.jpg" alt="Barry Manilow performing at the piano" loading="lazy" style="object-position:center 64%"><div><b>Barry Manilow’s Westgate run now reaches into 2027</b><p>Vegas Dispatch · Residency News</p></div></a>'''
if ml!=-1: s=s[:ml+23]+card+s[ml+23:]
p.write_text(s)
# Dispatch index: ensure Barry is first card, use performer photo with a face-friendly crop.
p=root/'news/index.html'; s=p.read_text()
s=re.sub(r'<article class="news-card"><a href="'+re.escape(url)+r'"[\s\S]*?</article>','',s)
card='''<article class="news-card"><a href="/news/barry-manilow-adds-2027-las-vegas-dates/"><img src="/images/news/barry-manilow-las-vegas-piano.jpg" alt="Barry Manilow performing at the piano" loading="eager" style="object-position:center 68%"><div class="news-card-body"><div class="news-card-meta">September 15, 2026 · Residency News</div><h2>Barry Manilow’s Westgate run now reaches into 2027</h2><p>Newly posted February, March and April performances give Manilow fans more Vegas dates to plan around.</p><span>Read the story →</span></div></a></article>'''
anchor='<div class="news-grid">'
if anchor in s: s=s.replace(anchor,anchor+card,1)
p.write_text(s)

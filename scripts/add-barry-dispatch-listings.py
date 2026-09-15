from pathlib import Path
root=Path(__file__).resolve().parents[1]
url='/news/barry-manilow-adds-2027-las-vegas-dates/'
img='/images/news/barry-manilow-residency-poster.jpg'

# Dispatch index: newest story first in the article grid, no giant featured treatment.
p=root/'news/index.html'
s=p.read_text()
card=f'''<a href="{url}" class="article-card" data-category="news"><div class="article-card-img"><img src="{img}" alt="Barry Manilow Las Vegas residency" loading="lazy"></div><div class="article-card-body"><div class="article-card-meta"><span class="article-tag">Residency</span><span class="article-date">Sept. 15, 2026</span></div><h3 class="article-card-title">Barry Manilow's Westgate Run Now Reaches Into 2027</h3></div></a>\n'''
if url not in s:
    s=s.replace('<div class="articles-grid" id="articles-grid">\n','<div class="articles-grid" id="articles-grid">\n'+card,1)
p.write_text(s)

# Homepage: newest Dispatch story first; preserve compact mini-card treatment and five-story cap.
p=root/'index.html'
s=p.read_text()
mini=f'''<a class="mini-card" href="{url}"><img src="{img}" alt="Barry Manilow Las Vegas residency"><span><b>Barry Manilow's Westgate run now reaches into 2027</b><small>Vegas Dispatch · Sept. 15, 2026</small></span></a>'''
if url not in s:
    marker='<div class="mini-list">'
    pos=s.find(marker, s.find('Vegas Dispatch'))
    if pos==-1:
        raise SystemExit('Could not find homepage Vegas Dispatch mini-list')
    insert=pos+len(marker)
    s=s[:insert]+mini+s[insert:]
    # Keep only the first five cards in this mini-list.
    end=s.find('</div>', insert)
    block=s[insert:end]
    parts=block.split('<a class="mini-card"')
    if len(parts)>6:
        block=parts[0]+''.join('<a class="mini-card"'+x for x in parts[1:6])
        s=s[:insert]+block+s[end:]
p.write_text(s)

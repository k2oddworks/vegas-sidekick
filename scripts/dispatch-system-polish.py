from pathlib import Path
import re
root=Path(__file__).resolve().parents[1]

# 1) Dispatch index: lead story is simply the newest story; remove the manual FEATURED label.
p=root/'news/index.html'; s=p.read_text()
s=s.replace('<span class="featured-badge">Featured</span>','',1)
p.write_text(s)

# 2) Homepage: keep only the five newest Dispatch mini-cards already ordered newest-first.
p=root/'index.html'; h=p.read_text()
head='<div class="edit-block"><div class="edit-head"><h3>Vegas Dispatch</h3><a href="/news/">All stories →</a></div><div class="mini-list">'
start=h.find(head)
if start==-1: raise SystemExit('Homepage Dispatch block not found')
list_start=start+len(head)
list_end=h.find('</div></div>',list_start)
if list_end==-1: raise SystemExit('Homepage Dispatch list end not found')
body=h[list_start:list_end]
cards=re.findall(r'<a class="mini-card" href="/news/.*?</a>',body,flags=re.S)
if len(cards)<5: raise SystemExit(f'Expected at least 5 Dispatch cards, found {len(cards)}')
h=h[:list_start]+''.join(cards[:5])+h[list_end:]
p.write_text(h)

# 3) Standardize all actual Dispatch article pages on shared site chrome.
# Skip the index and non-article/support pages. Add missing mount points and normalize component versions.
for article in (root/'news').glob('*/index.html'):
    text=article.read_text()
    # Only touch pages that identify as Vegas Dispatch/news content.
    if 'Vegas Dispatch' not in text and 'NewsArticle' not in text:
        continue
    text=re.sub(r'<script src="/components/header\.js(?:\?v=\d+)?"></script>', '<script src="/components/header.js?v=14"></script>', text)
    text=re.sub(r'<script src="/components/footer\.js(?:\?v=\d+)?"></script>', '<script src="/components/footer.js?v=14"></script>', text)
    # Repair old/nonexistent shared chrome references if any remain.
    text=text.replace('<script src="/assets/site-header.js"></script>', '<script src="/components/header.js?v=14"></script>')
    text=text.replace('<script src="/assets/site-footer.js"></script>', '<script src="/components/footer.js?v=14"></script>')
    if '/components/header.js' in text and 'id="vs-header"' not in text:
        text=text.replace('<body>', '<body><div id="vs-header"></div>',1)
    if '/components/footer.js' in text and 'id="vs-footer"' not in text:
        idx=text.rfind('<script src="/components/header.js')
        if idx!=-1: text=text[:idx]+'<div id="vs-footer"></div>'+text[idx:]
    article.write_text(text)

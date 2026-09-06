from pathlib import Path
import json,re
from bs4 import BeautifulSoup

ROOT=Path('.')
TARGET='/shows/cirque/mad-apple/'
NEWS='/news/mad-apple-closing-september-5/'
SKIP_PREFIXES=('preview/','docs/','news/')
SKIP_EXACT={'shows/cirque/mad-apple/index.html'}
changed=[]

CARD_CLASSES={'card','scard','show-card','also-card','related-card','deal-card','show-tile','result-card','pick-card','guide-card'}

def rewrite_jsonld(script):
    raw=script.string
    if not raw or 'mad-apple' not in raw.lower(): return False
    try: data=json.loads(raw)
    except Exception: return False
    touched=False
    def clean(obj):
        nonlocal touched
        if isinstance(obj,dict):
            for k,v in list(obj.items()):
                if isinstance(v,list):
                    nv=[]
                    for item in v:
                        blob=json.dumps(item).lower()
                        if isinstance(item,dict) and item.get('@type')=='ListItem' and 'mad-apple' in blob:
                            touched=True; continue
                        nv.append(clean(item))
                    obj[k]=nv
                    if k in ('itemListElement','itemListOrder') and isinstance(obj[k],list):
                        for i,item in enumerate(obj[k],1):
                            if isinstance(item,dict) and 'position' in item: item['position']=i
                else: obj[k]=clean(v)
        elif isinstance(obj,list):
            return [clean(x) for x in obj]
        return obj
    data=clean(data)
    if touched: script.string='\n'+json.dumps(data,ensure_ascii=False,indent=2)+'\n'
    return touched

def find_removal(a):
    if a.name=='tr': return a
    for p in [a,*list(a.parents)[:6]]:
        if getattr(p,'name',None)=='tr': return p
        classes=set(p.get('class',[])) if hasattr(p,'get') else set()
        if p.name=='article' and ('card' in classes or any('card' in c for c in classes)): return p
        if p.name=='a' and (classes & CARD_CLASSES or any('card' in c for c in classes)): return p
        if p.name in ('div','li') and (classes & CARD_CLASSES or any(c in CARD_CLASSES or c.endswith('-card') for c in classes)):
            return p
    return None

for path in ROOT.rglob('*.html'):
    rel=path.as_posix()
    if rel in SKIP_EXACT or rel.startswith(SKIP_PREFIXES): continue
    text=path.read_text(encoding='utf-8')
    if 'Mad Apple' not in text and 'mad-apple' not in text.lower(): continue
    soup=BeautifulSoup(text,'html.parser')
    touched=False
    for a in list(soup.find_all('a',href=TARGET)):
        rem=find_removal(a)
        if rem is not None and rem.name not in ('html','body'):
            rem.decompose(); touched=True
        else:
            a['href']=NEWS
            if a.get_text(' ',strip=True).lower().startswith(('get tickets','see mad apple','book','check tickets')):
                a.string='Read closure update →'
            touched=True
    for s in soup.find_all('script',attrs={'type':'application/ld+json'}):
        if rewrite_jsonld(s): touched=True
    # Renumber ranked guide cards after removals.
    if rel.startswith('guides/'):
        ranks=soup.select('article.card .rank')
        for i,r in enumerate(ranks,1):
            if r.get_text(strip=True)!=str(i): r.string=str(i); touched=True
    # Remove stale Mad Apple rows in ordinary comparison tables even when the link wasn't exact.
    for tr in list(soup.find_all('tr')):
        if 'mad apple' in tr.get_text(' ',strip=True).lower(): tr.decompose(); touched=True
    # Known stale category/venue copy.
    if rel=='shows/cirque/index.html':
        for node in list(soup.find_all(string=re.compile('Mad Apple',re.I))):
            t=str(node)
            if 'newest party show' in t or 'five resident productions' in t:
                node.replace_with('Las Vegas is home to four resident Cirque du Soleil productions, from the aquatic icon “O” to the classic Mystère. Compare the current Cirque lineup before choosing.')
                touched=True
        for meta in soup.find_all('meta',attrs={'name':'description'}):
            c=meta.get('content','')
            if 'Mad Apple' in c:
                meta['content']='Compare the current Cirque du Soleil shows in Las Vegas, including O, KÀ, Mystère and Michael Jackson ONE, with prices, venues and honest pros and cons.'; touched=True
    if rel=='venues/mgm-grand/index.html':
        for meta in soup.find_all('meta'):
            c=meta.get('content','')
            if 'Mad Apple' in c:
                meta['content']=re.sub(r'All 7 shows at MGM Grand & New York-New York[^.]*\.?','Current shows at MGM Grand and New York-New York, with prices, venues and honest recommendations.',c); touched=True
        if soup.title and 'Mad Apple' in soup.title.get_text():
            soup.title.string='Las Vegas Shows at MGM Grand & New York-New York (2026) | Vegas Sidekick'; touched=True
    if touched:
        out=str(soup)
        if not out.lstrip().lower().startswith('<!doctype'): out='<!DOCTYPE html>\n'+out
        path.write_text(out,encoding='utf-8')
        changed.append(rel)

# Search/index data: remove simple one-line or object entries that explicitly point at the active Mad Apple URL.
for path in list(ROOT.rglob('*.js'))+list(ROOT.rglob('*.json')):
    rel=path.as_posix()
    if rel.startswith(('preview/','node_modules/','.git/')): continue
    text=path.read_text(encoding='utf-8')
    if 'mad-apple' not in text.lower(): continue
    old=text
    # Common JSON object/list entry shapes.
    text=re.sub(r'\{[^{}]*?(?:mad-apple|Mad Apple)[^{}]*?\}\s*,?', '', text, flags=re.I|re.S)
    # Common single-line data rows.
    text='\n'.join(line for line in text.splitlines() if not ('mad-apple' in line.lower() and ('show' in line.lower() or 'Mad Apple' in line)))+'\n'
    if text!=old:
        path.write_text(text,encoding='utf-8'); changed.append(rel)

# Documentation inventory: mark retired rather than leaving it as an active-price example/table row.
for rel in ('SHOW-BUILDER-PROMPT.md','VS_CHAT_CONTEXT.md'):
    path=Path(rel)
    if not path.exists(): continue
    text=path.read_text(encoding='utf-8'); old=text
    text=re.sub(r'^\|\s*Mad Apple\s*\|\s*/shows/cirque/mad-apple/\s*\|[^\n]*$', '| Mad Apple | /shows/cirque/mad-apple/ | CLOSED Sep 5, 2026 |', text, flags=re.M)
    if text!=old: path.write_text(text,encoding='utf-8'); changed.append(rel)

print('Changed files:')
for p in sorted(set(changed)): print(' -',p)

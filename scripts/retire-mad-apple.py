from pathlib import Path
import json,re

TARGET='/shows/cirque/mad-apple/'
NEWS='/news/mad-apple-closing-september-5/'
changed=[]

PRODUCTION_HTML=[
 'index.html','shows/cirque/index.html','shows/spectaculars/index.html','venues/mgm-grand/index.html',
 'guides/best-cirque-shows/index.html','guides/best-shows-for-couples/index.html','guides/best-shows-for-first-timers/index.html',
 'shows/comedy/tape-face/index.html','shows/comedy/laugh-factory/index.html','shows/music/blue-man-group/index.html',
 'shows/comedy/marriage-can-be-murder/index.html','shows/magic/nathan-burton-comedy-magic/index.html',
 'shows/comedy/popovich-comedy-pet-theater/index.html','shows/comedy/marc-savard-comedy-hypnosis/index.html'
]

START_MARKERS=(
 '<article class="card"','<a class="show-card"','<a class="scard"','<div class="also-card"',
 '<a class="also-card"','<a class="related-card"','<div class="show-card"','<span><a href="'+TARGET+'"'
)

def remove_balanced_block(lines, hit):
    start=None; tag=None
    for i in range(hit, max(-1,hit-35), -1):
        s=lines[i]
        for marker in START_MARKERS:
            if marker in s:
                start=i
                tag=re.search(r'<([a-zA-Z0-9]+)',marker).group(1)
                break
        if start is not None: break
    if start is None:
        return False
    depth=0
    open_re=re.compile(r'<'+tag+r'\b',re.I)
    close_re=re.compile(r'</'+tag+r'>',re.I)
    for j in range(start,len(lines)):
        depth += len(open_re.findall(lines[j]))
        depth -= len(close_re.findall(lines[j]))
        if depth<=0 and j>=start:
            del lines[start:j+1]
            return True
    return False

def strip_target_cards(text):
    lines=text.splitlines(True)
    while True:
        hit=next((i for i,l in enumerate(lines) if 'href="'+TARGET+'"' in l or "href='"+TARGET+"'" in l),None)
        if hit is None: break
        if not remove_balanced_block(lines,hit):
            lines[hit]=lines[hit].replace('href="'+TARGET+'"','href="'+NEWS+'"').replace("href='"+TARGET+"'","href='"+NEWS+"'")
            lines[hit]=lines[hit].replace('See Mad Apple →','Mad Apple closed →').replace('View →','Closure update →')
    return ''.join(lines)

def strip_rows(text):
    return re.sub(r'\s*<tr\b[^>]*>.*?Mad Apple.*?</tr>\s*','\n',text,flags=re.I|re.S)

def clean_jsonld(text):
    pat=re.compile(r'(<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>)(.*?)(</script>)',re.I|re.S)
    def repl(m):
        raw=m.group(2)
        if 'mad-apple' not in raw.lower(): return m.group(0)
        try: data=json.loads(raw)
        except Exception: return m.group(0)
        touched=False
        def walk(x):
            nonlocal touched
            if isinstance(x,dict):
                for k,v in list(x.items()):
                    if isinstance(v,list):
                        nv=[]
                        for item in v:
                            blob=json.dumps(item).lower()
                            if isinstance(item,dict) and item.get('@type')=='ListItem' and 'mad-apple' in blob:
                                touched=True; continue
                            nv.append(walk(item))
                        x[k]=nv
                        if k=='itemListElement':
                            for n,item in enumerate(x[k],1):
                                if isinstance(item,dict) and 'position' in item: item['position']=n
                    else: x[k]=walk(v)
            elif isinstance(x,list): return [walk(i) for i in x]
            return x
        data=walk(data)
        if not touched: return m.group(0)
        return m.group(1)+'\n'+json.dumps(data,ensure_ascii=False,indent=2)+'\n'+m.group(3)
    return pat.sub(repl,text)

for rel in PRODUCTION_HTML:
    p=Path(rel)
    if not p.exists(): continue
    text=p.read_text(encoding='utf-8'); old=text
    text=strip_target_cards(text)
    text=strip_rows(text)
    text=clean_jsonld(text)
    if rel.startswith('guides/'):
        n=0
        def rr(m):
            nonlocal_dummy=None
            return m.group(0)
        def rank_repl(m):
            rank_repl.n+=1
            return m.group(1)+str(rank_repl.n)+m.group(2)
        rank_repl.n=0
        text=re.sub(r'(<div class="rank">)\d+(</div>)',rank_repl,text)
    if rel=='shows/cirque/index.html':
        text=text.replace('No city on Earth has more Cirque du Soleil than Las Vegas — five resident productions, each in a purpose-built theater, from the aquatic icon &ldquo;O&rdquo; to the newest party show, Mad Apple. Compare every Cirque show, see what makes each one different, and find the right fit for your night.','Las Vegas is home to four resident Cirque du Soleil productions, from the aquatic icon &ldquo;O&rdquo; to the classic Mystère. Compare the current lineup, see what makes each one different, and find the right fit for your night.')
        text=re.sub(r'<meta name="description" content="[^"]*Mad Apple[^"]*"\s*/?>','<meta name="description" content="Compare the current Cirque du Soleil shows in Las Vegas, including O, KÀ, Mystère and Michael Jackson ONE, with prices, venues and honest pros and cons." />',text)
    if rel=='venues/mgm-grand/index.html':
        text=re.sub(r'<meta name="description" content="[^"]*Mad Apple[^"]*"\s*/?>','<meta name="description" content="Current shows at MGM Grand and New York-New York, with prices, venues and honest recommendations." />',text)
    if rel=='index.html':
        text=re.sub(r'\s*<span><a href="/shows/cirque/mad-apple/">Mad Apple.*?</span></span>\s*','\n',text)
    if text!=old:
        p.write_text(text,encoding='utf-8'); changed.append(rel)

# Search data: remove the object whose URL/slug is Mad Apple while preserving the rest of the file.
p=Path('components/search-data.js')
if p.exists():
    text=p.read_text(encoding='utf-8'); old=text
    # Objects in this file are flat show records. Remove a record containing the retired slug.
    text=re.sub(r'\s*\{[^{}]*?(?:/shows/cirque/mad-apple/|cirque/mad-apple)[^{}]*?\}\s*,?','\n',text,flags=re.I|re.S)
    if text!=old:
        p.write_text(text,encoding='utf-8'); changed.append(p.as_posix())

# Keep builder/reference docs accurate without deleting the historical slug.
for rel in ('SHOW-BUILDER-PROMPT.md','VS_CHAT_CONTEXT.md'):
    p=Path(rel)
    if not p.exists(): continue
    text=p.read_text(encoding='utf-8'); old=text
    text=re.sub(r'^\|\s*Mad Apple\s*\|\s*/shows/cirque/mad-apple/\s*\|[^\n]*$', '| Mad Apple | /shows/cirque/mad-apple/ | CLOSED Sep 5, 2026 |',text,flags=re.M)
    if text!=old:
        p.write_text(text,encoding='utf-8'); changed.append(rel)

# Turn the existing closure article from future-tense last-chance copy into a completed closure update.
p=Path('news/mad-apple-closing-september-5/index.html')
if p.exists():
    text=p.read_text(encoding='utf-8'); old=text
    replacements={
      'Mad Apple Closing September 5 — Cirque du Soleil Ends Las Vegas Run | Vegas Sidekick':'Mad Apple Has Closed — Final Show Was September 5 | Vegas Sidekick',
      'Mad Apple Is Closing — Last Show Is September 5':'Mad Apple Has Closed — Final Show Was September 5',
      "Cirque du Soleil's Mad Apple will close permanently on September 5, 2026 at New York-New York. Here's why it's closing, what's next for the theater, and how to catch it before it's gone.":"Cirque du Soleil's Mad Apple closed permanently on September 5, 2026 at New York-New York. Here's why it closed and what's next for the theater.",
      "Mad Apple Is Closing — Cirque du Soleil's Last Show at New York-New York Is September 5":"Mad Apple Has Closed — Cirque du Soleil's Final Show at New York-New York Was September 5",
      'Cirque du Soleil will close Mad Apple permanently on September 5, 2026 after more than four years at New York-New York on the Las Vegas Strip.':'Cirque du Soleil closed Mad Apple permanently on September 5, 2026 after more than four years at New York-New York on the Las Vegas Strip.',
      '<h1>Mad Apple Is Closing — Last Show Is September 5</h1>':'<h1>Mad Apple Has Closed — Final Show Was September 5</h1>',
      '<div class="last-chance-title">Last Chance to See It</div>':'<div class="last-chance-title">Mad Apple Has Closed</div>',
      'Mad Apple runs through September 5, 2026 at New York-New York. If you want to catch the final weeks — or the closing show itself — don\'t wait on this one.':'Mad Apple ended its run at New York-New York on September 5, 2026. There are no future performances to book.',
      'If you\'ve been meaning to see it, don\'t wait for a \'next time\' that isn\'t coming.':'The show found its footing and built a real following before its final performance on September 5.'
    }
    for a,b in replacements.items(): text=text.replace(a,b)
    # Remove any stale ticket CTA to the retired show from this news article.
    text=re.sub(r'<a class="last-chance-btn"[^>]*href="/shows/cirque/mad-apple/"[^>]*>.*?</a>','<a class="last-chance-btn" href="/shows/cirque/">See current Cirque shows →</a>',text,flags=re.S)
    text=text.replace('"dateModified": "2026-08-20"','"dateModified": "2026-09-06"')
    if text!=old:
        p.write_text(text,encoding='utf-8'); changed.append(p.as_posix())

print('Changed files:')
for rel in changed: print(' -',rel)

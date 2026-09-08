#!/usr/bin/env python3
from pathlib import Path
import json,re,html
ROOT=Path(__file__).resolve().parents[1]
DB=ROOT/'data/show-database.json'
MIN_SAVE=5

APPROVED_SAVINGS_CSS="/* Vegas Sidekick savings system */\n.vs-deal-line{display:flex;align-items:center;gap:7px;flex-wrap:wrap;margin-top:7px}.vs-regular-price{color:#8b8295;text-decoration:line-through;font:700 .78rem/1.2 Inter,sans-serif}.vs-save-badge{display:inline-flex;align-items:center;border-radius:999px;background:#fff1b8;color:#4c3200;border:1px solid rgba(255,176,0,.5);font:800 .72rem/1 'Plus Jakarta Sans',sans-serif;padding:6px 9px}.vs-deal-note{display:none!important}.mobile-cta .vs-mobile-save,.mobile-bar .vs-mobile-save,.sticky-cta .vs-mobile-save{display:block;color:#9a6800;font:800 .67rem/1.15 'Plus Jakarta Sans',sans-serif;margin-top:2px}\n@media(max-width:800px){\n  .buybox{display:grid!important;grid-template-columns:auto minmax(0,1fr)!important;align-items:end!important;gap:10px 16px!important;padding:18px!important}\n  .buybox>.price{grid-column:1!important;grid-row:1!important;align-self:end!important;margin:0!important}\n  .buybox>.vs-deal-line{grid-column:2!important;grid-row:1!important;align-self:end!important;margin:0 0 5px!important}\n  .buybox>.cta,.buybox>.hero-cta,.buybox>a.vs-ticket-primary{grid-column:1/-1!important;width:100%!important;min-height:54px!important;margin:2px 0 0!important;padding:14px 22px!important;border-radius:999px!important;justify-content:center!important;text-align:center!important;white-space:nowrap!important}\n  .buybox>div:first-child{grid-column:1/-1!important;display:grid!important;grid-template-columns:auto minmax(0,1fr)!important;align-items:end!important;gap:8px 16px!important;width:100%!important}\n  .buybox>div:first-child>.price{grid-column:1!important;margin:0!important}\n  .buybox>div:first-child>.vs-deal-line{grid-column:2!important;margin:0 0 4px!important;align-self:end!important}\n  .buybox>div:first-child>.updated,.buybox>div:first-child>.save{grid-column:1/-1!important;margin-top:0!important}\n  .price-row{display:grid!important;grid-template-columns:auto minmax(0,1fr)!important;align-items:end!important;gap:10px 16px!important;width:100%!important}\n  .price-row>.price{grid-column:1!important;margin:0!important}\n  .price-row>.vs-deal-line{grid-column:2!important;margin:0 0 5px!important;align-self:end!important}\n  .price-row>.ticket,.price-row>a.vs-ticket-primary{grid-column:1/-1!important;width:100%!important;min-height:54px!important;padding:14px 22px!important;border-radius:999px!important;justify-content:center!important;text-align:center!important;white-space:nowrap!important}\n  .vs-save-badge{font-size:.68rem;padding:5px 8px}\n}\n"

def money(v): return f'${int(round(float(v)))}'
def calc(r):
    try:a=float(r.get('our_price'));b=float(r.get('regular_price'))
    except:return None
    s=b-a
    if not b or s<MIN_SAVE:return None
    return {'amount':int(round(s)),'percent':int(round(s/b*100))}

data=json.loads(DB.read_text())
for r in data.get('records',[]):
    d=calc(r);r['savings_amount']=d['amount'] if d else None;r['savings_percent']=d['percent'] if d else None;r['is_deal']=bool(d)
data['deal_threshold_dollars']=MIN_SAVE
DB.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
active=[r for r in data['records'] if r.get('status')=='active']

# Shared savings presentation.
(ROOT/'assets/show-savings.css').write_text(APPROVED_SAVINGS_CSS)
(ROOT/'assets/catalog-savings.css').write_text('''.card-save-badge{display:inline-flex;align-items:center;border-radius:999px;background:#fff1b8;color:#4c3200;border:1px solid rgba(255,176,0,.48);font-weight:800;font-size:.67rem;padding:5px 8px;margin-left:7px;white-space:nowrap}.card-regular{font-size:.72rem;color:#8b8295;text-decoration:line-through;margin-left:3px}.vs-savings-controls{display:flex;gap:8px;align-items:center}.vs-deals-btn{background:#ffb000!important;color:#171225!important;border-color:#ffb000!important}.vs-deals-btn:hover{filter:brightness(.96)}
''')
(ROOT/'assets/catalog-savings.js').write_text('''(()=>{const MIN=5;let map=new Map();const slugOf=c=>{const href=c.querySelector('a[href*="/shows/"]')?.getAttribute('href')||'';return href.split('/').filter(Boolean).pop()};const deal=r=>{const a=Number(r&&r.our_price),b=Number(r&&r.regular_price),s=b-a;return Number.isFinite(s)&&b>0&&s>=MIN?{amount:Math.round(s),percent:Math.round(s/b*100)}:null};function decorate(){document.querySelectorAll('.show-card').forEach(c=>{const r=map.get(slugOf(c)),d=deal(r);c.dataset.vsDeal=d?'1':'0';if(!d||c.querySelector('.card-save-badge'))return;const p=c.querySelector('.card-price');if(p)p.insertAdjacentHTML('afterend',`<span class="card-regular">$${Math.round(r.regular_price)}</span><span class="card-save-badge">Save $${d.amount}</span>`)});}window.vsSavingsSort=function(btn){const g=document.querySelector('.show-grid');if(!g)return;document.querySelectorAll('.sort-btn,.filter-btn').forEach(x=>x.classList.remove('active'));btn?.classList.add('active');[...g.children].sort((a,b)=>(deal(map.get(slugOf(b)))?.amount||0)-(deal(map.get(slugOf(a)))?.amount||0)).forEach(x=>g.appendChild(x));decorate()};window.vsDealsFilter=function(btn){decorate();const cards=[...document.querySelectorAll('.show-card')];const active=btn?.dataset.active!=='1';if(btn){btn.dataset.active=active?'1':'0';btn.classList.toggle('active',active);btn.textContent=active?'🔥 Showing Deals':'🔥 Deals'}cards.forEach(c=>c.style.display=active&&c.dataset.vsDeal!=='1'?'none':'');const n=cards.filter(c=>c.style.display!=='none').length;const count=document.querySelector('.show-count-wrap');if(count)count.textContent=n+(active?' deals':' shows')};fetch('/data/show-database.json',{cache:'no-store'}).then(r=>r.json()).then(db=>{map=new Map((db.records||[]).filter(r=>r.status==='active').map(r=>[r.slug,r]));decorate();new MutationObserver(decorate).observe(document.querySelector('.show-grid')||document.body,{childList:true,subtree:true})}).catch(()=>{})})();
''')

# Show detail pages.
page_updates=0; deal_pages=0
for r in active:
    pp=r.get('page_path')
    if not pp:continue
    p=ROOT/pp.strip('/')/'index.html'
    if not p.exists():continue
    text=p.read_text()
    # idempotence
    text=text.replace('<link href="/assets/show-savings.css" rel="stylesheet"/>','').replace('<link rel="stylesheet" href="/assets/show-savings.css">','')
    text=re.sub(r'<div class="vs-deal-line">.*?</div>','',text,flags=re.S)
    text=re.sub(r'<div class="vs-deal-note">.*?</div>','',text,flags=re.S)
    text=re.sub(r'<span class="vs-mobile-save">.*?</span>','',text,flags=re.S)
    text=text.replace('</head>','<link rel="stylesheet" href="/assets/show-savings.css"></head>',1)
    d=calc(r)
    if d:
        deal_pages+=1;our=money(r['our_price']);reg=money(r['regular_price']);save=money(d['amount'])
        line=f'<div class="vs-deal-line"><span class="vs-regular-price">Regular {reg}</span><span class="vs-save-badge">Save {save}</span></div>'
        # canonical buybox first
        pat=rf'(<div class="buybox"><div class="price"><small>[^<]*</small>{re.escape(our)}</div>)'
        text,n=re.subn(pat,lambda m:m.group(1)+line,text,count=1,flags=re.I)
        if n:
        else:
            # custom benchmark pages: add after first price/was construct only if visible body match exists
            pat2=rf'(<div class="price"[^>]*>\s*{re.escape(our)}(?:\s*<span[^>]*>.*?</span>)?\s*</div>)'
            text,n=re.subn(pat2,lambda m:m.group(1)+line,text,count=1,flags=re.S|re.I)
        # mobile sticky bar variants
        for klass in ('mobile-cta','mobile-bar','sticky-cta'):
            patm=rf'(<div class="{klass}"[^>]*>.*?<strong>{re.escape(our)}</strong>)'
            text,nm=re.subn(patm,lambda m:m.group(1)+f'<span class="vs-mobile-save">Save {save}</span>',text,count=1,flags=re.S|re.I)
            if nm:break
    p.write_text(text);page_updates+=1

# Catalog pages: cards get savings badges from shared DB; categories get Biggest Savings sort; root also gets Deals filter.
catalogs=[ROOT/'shows/index.html']+sorted((ROOT/'shows').glob('*/index.html'))
cat_updates=0
for p in catalogs:
    if p.parent.name=='deals':continue
    text=p.read_text()
    text=text.replace('<link rel="stylesheet" href="/assets/catalog-savings.css">','').replace('<script src="/assets/catalog-savings.js"></script>','')
    text=text.replace('</head>','<link rel="stylesheet" href="/assets/catalog-savings.css"></head>',1)
    # add savings controls next to existing price sort when possible
    if 'vsSavingsSort(this)' not in text:
        text=re.sub(r'(<button class="filter-btn" onclick="setSort\(\'price\',this\)">Price: Low → High</button>)',r'\1<button class="filter-btn sort-btn" onclick="vsSavingsSort(this)">Biggest Savings</button>',text,count=1)
    if p==ROOT/'shows/index.html' and 'vsDealsFilter(this)' not in text:
        # Put Deals next to Biggest Savings; it acts as a reversible filter.
        text=text.replace('<button class="filter-btn sort-btn" onclick="vsSavingsSort(this)">Biggest Savings</button>','<button class="filter-btn sort-btn" onclick="vsSavingsSort(this)">Biggest Savings</button><button class="filter-btn vs-deals-btn" onclick="vsDealsFilter(this)">🔥 Deals</button>',1)
    text=text.replace('</body>','<script src="/assets/catalog-savings.js"></script></body>',1)
    p.write_text(text);cat_updates+=1

# Deals page. Hero image is pulled from each real show page rather than guessed extension.
def hero_for(r):
    p=ROOT/r['page_path'].strip('/')/'index.html'
    if p.exists():
        t=p.read_text(errors='ignore');m=re.search(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\'](?:https://vegassidekick\.com)?([^"\']+)',t,re.I)
        if m:return m.group(1)
    return '/favicon.png'
deals=sorted([r for r in active if calc(r)],key=lambda r:(-r['savings_amount'],r['our_price'],r['name']))
cards=[]
for r in deals:
    cards.append(f'''<article class="deal-card" data-save="{r['savings_amount']}"><a href="{html.escape(r['page_path'])}"><div class="deal-img"><img src="{html.escape(hero_for(r))}" alt="{html.escape(r['name'])}" loading="lazy"></div><div class="deal-body"><div class="deal-cat">{html.escape(r['category'].title())}</div><h2>{html.escape(r['name'])}</h2><div class="deal-pricing"><strong>{money(r['our_price'])}</strong><span>Regular {money(r['regular_price'])}</span></div><div class="deal-save">Save {money(r['savings_amount'])} · {r['savings_percent']}%</div><p>{html.escape(r.get('venue') or '')}</p><span class="deal-cta">See tickets →</span></div></a></article>''')
page=ROOT/'shows/deals/index.html';page.parent.mkdir(parents=True,exist_ok=True)
page.write_text(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Las Vegas Show Ticket Deals & Discounts | Vegas Sidekick</title><meta name="description" content="Compare current Las Vegas show ticket discounts by real dollar savings. See our current price beside the listed regular price."><link rel="canonical" href="https://vegassidekick.com/shows/deals/"><link rel="icon" href="/favicon.png"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@700;800&display=swap" rel="stylesheet"><style>*{{box-sizing:border-box}}body{{margin:0;background:#f5f3fa;color:#171225;font-family:Inter,sans-serif}}a{{color:inherit;text-decoration:none}}.hero{{background:#1c0a3a;color:#fff;padding:112px 22px 54px}}.wrap{{max-width:1180px;margin:auto}}.eyebrow{{font-weight:800;color:#ffb000;letter-spacing:.12em;text-transform:uppercase;font-size:.75rem}}h1{{font-family:'Plus Jakarta Sans';font-size:clamp(2.7rem,7vw,5.5rem);line-height:.96;margin:12px 0}}.hero p{{max-width:680px;color:#d8cfe5;font-size:1.05rem;line-height:1.6}}.trust{{display:inline-block;margin-top:18px;background:#2c1547;border:1px solid #543472;padding:10px 13px;border-radius:10px;color:#eee;font-size:.82rem}}.deal-count{{margin-top:12px;font-weight:800;color:#ffb000}}.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;padding:30px 22px 60px}}.deal-card{{background:#fff;border:1px solid #e8e2ef;border-radius:15px;overflow:hidden;box-shadow:0 3px 12px #1c0a3a0b}}.deal-img{{aspect-ratio:16/9;background:#25113d;overflow:hidden}}.deal-img img{{width:100%;height:100%;object-fit:cover}}.deal-body{{padding:16px}}.deal-cat{{font-size:.68rem;font-weight:800;color:#7c3aed;text-transform:uppercase;letter-spacing:.08em}}h2{{font-family:'Plus Jakarta Sans';font-size:1.3rem;margin:5px 0 12px}}.deal-pricing{{display:flex;align-items:baseline;gap:9px}}.deal-pricing strong{{font-family:'Plus Jakarta Sans';font-size:2rem}}.deal-pricing span{{color:#8a8195;text-decoration:line-through;font-size:.82rem}}.deal-save{{display:inline-block;background:#fff1ba;border:1px solid #ffb00088;color:#573800;font-weight:800;border-radius:999px;padding:6px 9px;margin:8px 0}}.deal-body p{{font-size:.78rem;color:#746b80;min-height:30px}}.deal-cta{{display:block;background:#ffb000;color:#171225;font-weight:800;text-align:center;padding:12px;border-radius:9px;margin-top:12px}}@media(max-width:850px){{.grid{{grid-template-columns:repeat(2,1fr)}}}}@media(max-width:560px){{.hero{{padding-top:92px}}.grid{{grid-template-columns:1fr;padding:18px 14px 40px}}}}</style></head><body><div id="vs-header"></div><main><section class="hero"><div class="wrap"><div class="eyebrow">🌵 Sidekick Deals</div><h1>Vegas show deals worth seeing.</h1><p>Current Vegas Sidekick prices compared with the listed regular price. We only call it a deal when the difference is at least ${MIN_SAVE}.</p><div class="deal-count">{len(deals)} current discounted shows</div><div class="trust">No countdown clocks. No fake urgency. Prices and comparisons last verified September 2026.</div></div></section><section class="wrap grid">{''.join(cards)}</section></main><div id="vs-footer"></div><script src="/components/header.js?v=14"></script><script src="/components/footer.js?v=14"></script></body></html>''')
print(json.dumps({'records':len(data['records']),'active':len(active),'deals':len(deals),'show_pages':page_updates,'catalogs':cat_updates,'deal_pages':deal_pages}))

#!/usr/bin/env python3
from pathlib import Path
import json,re,html,math
ROOT=Path(__file__).resolve().parents[1]
DB=ROOT/'data/show-database.json'
MIN_SAVE=5

def money(v): return f'${int(round(v))}'

def savings(rec):
    a=rec.get('our_price'); b=rec.get('regular_price')
    try: a=float(a); b=float(b)
    except: return None
    s=b-a
    if s < MIN_SAVE: return None
    return {'amount':int(round(s)),'percent':int(round(s/b*100)) if b else 0}

data=json.loads(DB.read_text())
for r in data['records']:
    s=savings(r)
    r['savings_amount']=s['amount'] if s else None
    r['savings_percent']=s['percent'] if s else None
    r['is_deal']=bool(s)
data['deal_threshold_dollars']=MIN_SAVE
DB.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
by_path={r.get('page_path'):r for r in data['records'] if r.get('status')=='active'}

# Shared CSS: amber value language; scoped so brand pink stays brand pink.
css=ROOT/'assets/show-canonical.css'
ct=css.read_text()
marker='/* VS SAVINGS SYSTEM */'
if marker not in ct:
    ct += '''\n\n/* VS SAVINGS SYSTEM */\n.vs-deal-line{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-top:7px}.vs-regular-price{color:#8a8195;text-decoration:line-through;font-weight:700;font-size:.84rem}.vs-save-badge{display:inline-flex;align-items:center;border-radius:999px;background:#fff4cc;color:#5c3a00;border:1px solid rgba(255,176,0,.42);font:800 .72rem/1 'Plus Jakarta Sans',sans-serif;padding:6px 9px}.vs-deal-note{margin-top:10px;padding:11px 13px;border-radius:12px;background:linear-gradient(135deg,#fff8df,#fff);border:1px solid rgba(255,176,0,.28);color:#49330a;font-size:.83rem;line-height:1.45}.vs-deal-note strong{color:#171225}.mobile-ticket-bar .vs-mobile-save{display:block;font-size:.68rem;line-height:1.1;font-weight:800;color:#8a5c00;margin-top:2px}@media(max-width:800px){.vs-deal-note{font-size:.79rem}.vs-save-badge{font-size:.68rem;padding:5px 8px}}\n'''
    css.write_text(ct)

# Enhance active show pages. Use robust pattern matching around visible price and sticky bar.
changed=0
for page_path,r in by_path.items():
    if not page_path: continue
    p=ROOT/page_path.strip('/')/'index.html'
    if not p.exists(): continue
    text=p.read_text()
    s=savings(r)
    # Remove any previous generated savings blocks for idempotence.
    text=re.sub(r'<div class="vs-deal-line".*?</div>','',text,flags=re.S)
    text=re.sub(r'<div class="vs-deal-note".*?</div>','',text,flags=re.S)
    text=re.sub(r'<span class="vs-mobile-save".*?</span>','',text,flags=re.S)
    if s:
        our=money(r['our_price']); reg=money(r['regular_price']); save=money(s['amount'])
        deal=f'<div class="vs-deal-line"><span class="vs-regular-price">Regular {reg}</span><span class="vs-save-badge">Save {save}</span></div><div class="vs-deal-note">🌵 <strong>Sidekick deal:</strong> {our} is {save} less than the listed regular price of {reg}.</div>'
        # Best-effort insert after the first visible hero price element containing our price.
        patterns=[
          rf'(<div class="hero-price[^>]*>.*?{re.escape(our)}.*?</div>)',
          rf'(<div class="price-box[^>]*>.*?{re.escape(our)}.*?</div>)',
          rf'(<div class="price[^>]*>.*?{re.escape(our)}.*?</div>)',
          rf'(<strong[^>]*>{re.escape(our)}</strong>)'
        ]
        inserted=False
        for pat in patterns:
            nt,n=re.subn(pat,lambda m:m.group(1)+deal,text,count=1,flags=re.S|re.I)
            if n: text=nt; inserted=True; break
        # Sticky bar: add Save $X near first price in mobile bar.
        m=re.search(r'(<(?:div|span)[^>]*class="[^"]*(?:mobile-ticket|mobile-bar|sticky-ticket|sticky-cta)[^"]*"[^>]*>.*?)(</(?:div|span)>)',text,re.S|re.I)
        if m:
            seg=m.group(1)
            # insert after first visible price node or text.
            seg2,n=re.subn(r'(\$\d+(?:\.\d+)?)',r'\1<span class="vs-mobile-save">Save '+money(s['amount'])+r'</span>',seg,count=1)
            if n: text=text[:m.start(1)]+seg2+text[m.end(1):]
    p.write_text(text)
    changed+=1

# Root /shows catalog: enrich JS data from database by slug, add deals filter/sort + card savings via runtime JS injection.
root=ROOT/'shows/index.html'
text=root.read_text()
# Add deals filter and sort button if absent.
if 'data-cat="deals"' not in text:
    # after All filter button, tolerant match
    text=re.sub(r'(<button[^>]+data-cat="all"[^>]*>.*?</button>)',r'\1<button class="filter-btn fb-deals" data-cat="deals">🔥 Deals</button>',text,count=1,flags=re.S|re.I)
if 'data-sort="savings"' not in text:
    # append beside existing price sort button
    text=re.sub(r'(<button[^>]+data-sort="price"[^>]*>.*?</button>)',r'\1<button class="filter-btn sort-btn" data-sort="savings">Biggest Savings</button>',text,count=1,flags=re.S|re.I)
# CSS for deals filter/card
if '.fb-deals' not in text:
    text=text.replace('.fb-adult  {', '.fb-deals { background:rgba(255,176,0,.14);color:#8a5c00;border-color:#ffb000!important}.fb-deals.active,.fb-deals:hover{background:#ffb000;color:#171225}\n    .card-save-badge{display:inline-flex;align-items:center;border-radius:999px;background:#fff4cc;color:#5c3a00;border:1px solid rgba(255,176,0,.42);font-family:var(--font-price);font-size:.68rem;font-weight:800;padding:5px 8px;margin-left:6px}.card-regular{font-size:.72rem;color:#8b8295;text-decoration:line-through;margin-left:2px}\n    .fb-adult  {')
# Runtime enrich script inserted before final </body>
script='''\n<script id="vs-savings-system">\n(async function(){\n const MIN=5; let db; try{db=await fetch('/data/show-database.json',{cache:'no-store'}).then(r=>r.json())}catch(e){return}\n const map=new Map((db.records||[]).filter(r=>r.status==='active').map(r=>[r.slug,r]));\n const calc=r=>{const a=Number(r&&r.our_price),b=Number(r&&r.regular_price),s=b-a;return Number.isFinite(s)&&s>=MIN?{amount:Math.round(s),percent:Math.round(s/b*100)}:null};\n // Enrich SHOWS objects without changing the hand-authored catalog source.\n if(Array.isArray(window.SHOWS)){window.SHOWS.forEach(s=>{const r=map.get(s.slug);const d=calc(r);if(r){s.regularPrice=r.regular_price;s.savings=d?d.amount:0;s.savingsPercent=d?d.percent:0;s.isDeal=!!d;}})}\n const decorate=()=>{document.querySelectorAll('.show-card').forEach(card=>{const href=card.querySelector('a[href*="/shows/"]')?.getAttribute('href')||'';const slug=href.split('/').filter(Boolean).pop();const r=map.get(slug),d=calc(r);if(!d||card.querySelector('.card-save-badge'))return;const price=card.querySelector('.card-price');if(price){price.insertAdjacentHTML('afterend',`<span class="card-regular">$${Math.round(r.regular_price)}</span><span class="card-save-badge">Save $${d.amount}</span>`)}})};\n decorate(); new MutationObserver(decorate).observe(document.querySelector('.show-grid')||document.body,{childList:true,subtree:true});\n // Hook existing category filtering: Deals is a post-render visibility filter, keeping original controls intact.\n document.querySelector('[data-cat="deals"]')?.addEventListener('click',()=>setTimeout(()=>{document.querySelectorAll('.show-card').forEach(card=>{const href=card.querySelector('a[href*="/shows/"]')?.getAttribute('href')||'';const slug=href.split('/').filter(Boolean).pop();card.style.display=calc(map.get(slug))?'':'none'});const n=[...document.querySelectorAll('.show-card')].filter(c=>c.style.display!=='none').length;const el=document.querySelector('.show-count-wrap');if(el)el.textContent=n+' deals';},0));\n // Biggest savings sort independent of original sort engine.\n document.querySelector('[data-sort="savings"]')?.addEventListener('click',()=>{const grid=document.querySelector('.show-grid');if(!grid)return;[...grid.children].sort((a,b)=>{const slug=x=>(x.querySelector('a[href*="/shows/"]')?.getAttribute('href')||'').split('/').filter(Boolean).pop();return (calc(map.get(slug(b)))?.amount||0)-(calc(map.get(slug(a)))?.amount||0)}).forEach(x=>grid.appendChild(x));decorate()});\n})();\n</script>\n'''
if 'id="vs-savings-system"' not in text: text=text.replace('</body>',script+'</body>')
root.write_text(text)

# Dedicated deals page generated from DB, static SEO-friendly cards.
deals=[r for r in data['records'] if r.get('status')=='active' and savings(r)]
deals.sort(key=lambda r:(-r['savings_amount'],r['our_price']))
cards=[]
for r in deals:
    img=f"/images/{r['slug']}-hero.jpg"
    # webp fallback is browser-level unavailable; use known convention with onerror fallback to favicon.
    cards.append(f'''<article class="deal-card"><a href="{html.escape(r['page_path'])}"><div class="deal-img"><img src="{img}" onerror="this.src='/favicon.png'" alt="{html.escape(r['name'])}"></div><div class="deal-body"><div class="deal-cat">{html.escape(r['category'].title())}</div><h2>{html.escape(r['name'])}</h2><div class="deal-pricing"><strong>{money(r['our_price'])}</strong><span>Regular {money(r['regular_price'])}</span></div><div class="deal-save">Save {money(r['savings_amount'])} · {r['savings_percent']}%</div><p>{html.escape(r.get('venue') or '')}</p><span class="deal-cta">See tickets →</span></div></a></article>''')
page=ROOT/'shows/deals/index.html'; page.parent.mkdir(parents=True,exist_ok=True)
page.write_text(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Las Vegas Show Ticket Deals & Discounts | Vegas Sidekick</title><meta name="description" content="Compare current Las Vegas show ticket discounts. See Vegas Sidekick prices beside listed regular prices and sort the biggest real savings."><link rel="canonical" href="https://vegassidekick.com/shows/deals/"><link rel="icon" href="/favicon.png"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@700;800&display=swap" rel="stylesheet"><style>*{{box-sizing:border-box}}body{{margin:0;background:#f5f3fa;color:#171225;font-family:Inter,sans-serif}}a{{color:inherit;text-decoration:none}}.hero{{background:#1c0a3a;color:white;padding:110px 22px 52px}}.wrap{{max-width:1180px;margin:auto}}.eyebrow{{font-weight:800;color:#ffb000;letter-spacing:.12em;text-transform:uppercase;font-size:.75rem}}h1{{font-family:'Plus Jakarta Sans';font-size:clamp(2.6rem,7vw,5.5rem);line-height:.96;margin:12px 0}}.hero p{{max-width:650px;color:#d7cfe4;font-size:1.05rem;line-height:1.6}}.trust{{display:inline-block;margin-top:18px;background:#2b1348;border:1px solid #51316f;padding:10px 13px;border-radius:10px;color:#eee;font-size:.83rem}}.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;padding:30px 22px 60px}}.deal-card{{background:white;border:1px solid #e8e2ef;border-radius:15px;overflow:hidden;box-shadow:0 3px 12px #1c0a3a0b}}.deal-img{{aspect-ratio:16/9;background:#25113d;overflow:hidden}}.deal-img img{{width:100%;height:100%;object-fit:cover}}.deal-body{{padding:16px}}.deal-cat{{font-size:.7rem;font-weight:800;color:#7c3aed;text-transform:uppercase;letter-spacing:.08em}}h2{{font-family:'Plus Jakarta Sans';font-size:1.3rem;margin:5px 0 12px}}.deal-pricing{{display:flex;align-items:baseline;gap:9px}}.deal-pricing strong{{font-family:'Plus Jakarta Sans';font-size:2rem}}.deal-pricing span{{color:#8a8195;text-decoration:line-through;font-size:.82rem}}.deal-save{{display:inline-block;background:#fff1ba;border:1px solid #ffb00088;color:#573800;font-weight:800;border-radius:999px;padding:6px 9px;margin:8px 0}}.deal-body p{{font-size:.78rem;color:#746b80;min-height:30px}}.deal-cta{{display:block;background:#ffb000;color:#171225;font-weight:800;text-align:center;padding:12px;border-radius:9px;margin-top:12px}}@media(max-width:850px){{.grid{{grid-template-columns:repeat(2,1fr)}}}}@media(max-width:560px){{.hero{{padding-top:90px}}.grid{{grid-template-columns:1fr;padding:18px 14px 40px}}}}</style></head><body><div id="vs-header"></div><main><section class="hero"><div class="wrap"><div class="eyebrow">🌵 Sidekick Deals</div><h1>Vegas show deals worth seeing.</h1><p>These shows currently have a Vegas Sidekick ticket price at least ${MIN_SAVE} below the listed regular price. No countdown clocks. No fake urgency. Just the current price difference.</p><div class="trust">Prices and regular-price comparisons last verified September 2026.</div></div></section><section class="wrap grid">{''.join(cards)}</section></main><div id="vs-footer"></div><script src="/components/header.js?v=14"></script><script src="/components/footer.js?v=14"></script></body></html>''')

print('records',len(data['records']),'deals',len(deals),'show pages processed',changed)

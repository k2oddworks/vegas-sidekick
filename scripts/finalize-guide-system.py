from pathlib import Path
import re

GUIDES=['best-adult-shows','best-cheap-vegas-shows','best-cirque-shows','best-magic-shows','best-shows-for-couples','best-shows-for-families','best-shows-for-first-timers','best-tribute-shows']
CSS='''<style id="guide-photo-system">.g-hero .wrap{max-width:1180px}.guide-hero-grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(360px,.92fr);gap:42px;align-items:center}.guide-hero-copy{min-width:0}.guide-hero-visuals{display:grid;grid-template-columns:1fr 1fr;grid-template-rows:176px 176px;gap:10px;transform:rotate(-1deg)}.guide-hero-shot{position:relative;overflow:hidden;border-radius:18px;border:1px solid rgba(255,255,255,.24);box-shadow:0 18px 50px rgba(0,0,0,.25);background:#261147}.guide-hero-shot:first-child{grid-column:1/3}.guide-hero-shot img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .35s ease}.guide-hero-shot::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 42%,rgba(13,5,27,.8))}.guide-hero-label{position:absolute;left:12px;bottom:10px;z-index:2;font-family:var(--font-display);font-size:.76rem;font-weight:800;color:#fff}.guide-hero-price{position:absolute;right:10px;top:10px;z-index:2;background:var(--pink);color:#fff;border-radius:999px;padding:5px 9px;font-family:var(--font-display);font-size:.72rem;font-weight:800}.guide-mini a{padding:0 0 14px;overflow:hidden}.guide-mini a small,.guide-mini a strong,.guide-mini a .mini-detail{margin-left:14px;margin-right:14px}.qa-photo{width:100%;height:112px;object-fit:cover;display:block;margin-bottom:12px}.mini-detail{display:block;font-size:.82rem;color:#5d566a;line-height:1.35;margin-top:5px}.guide-newsletter{margin:44px 0;padding:30px;border-radius:24px;background:linear-gradient(135deg,#6d28d9,#e52b8d 62%,#ff4f79);color:#fff;box-shadow:0 18px 44px rgba(77,24,139,.2)}.guide-newsletter .nl-kicker{display:inline-flex;padding:6px 12px;border-radius:999px;background:rgba(47,13,66,.45);font-family:var(--font-mono);font-size:.7rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--lime)}.guide-newsletter h2{font-family:var(--font-display);font-size:clamp(1.7rem,4vw,2.35rem);line-height:1.05;margin:13px 0 8px;color:#fff}.guide-newsletter p{margin:0 0 18px;color:rgba(255,255,255,.9)}.guide-newsletter form{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:10px}.guide-newsletter input{border:0;border-radius:14px;padding:15px 16px;font:600 1rem var(--font-body);color:var(--ink);background:#fff}.guide-newsletter button{border:0;border-radius:14px;padding:15px 20px;background:var(--lime);color:#171225;font:800 .95rem var(--font-display);cursor:pointer}.guide-newsletter .nl-msg{min-height:1.25em;margin-top:9px;font-size:.8rem;font-weight:700}.guide-newsletter .nl-fine{font-size:.72rem;color:rgba(255,255,255,.75);margin-top:7px}@media(max-width:820px){.guide-hero-grid{grid-template-columns:1fr;gap:26px}.guide-hero-visuals{grid-template-rows:148px 148px;transform:none}}@media(max-width:600px){.guide-newsletter{padding:23px 20px}.guide-newsletter form{grid-template-columns:1fr}.guide-newsletter button{width:100%}}@media(max-width:520px){.guide-hero-visuals{grid-template-rows:124px 124px}.qa-photo{height:120px}}</style>'''
NEWS='''<section class="guide-newsletter"><div class="nl-kicker">🌵 Spike's Insider List</div><h2>Useful Vegas updates, without the inbox nonsense.</h2><p>Show changes, worthwhile deals and the Vegas stuff I’d actually text a friend about.</p><form class="guide-newsletter-form" novalidate><input type="email" placeholder="your@email.com" aria-label="Email address" required><button type="submit">Get Vegas Updates</button></form><div class="nl-msg" aria-live="polite"></div><div class="nl-fine">Occasional emails. Unsubscribe anytime.</div></section>'''
JS='''<script id="guide-newsletter-js">document.querySelectorAll('.guide-newsletter-form').forEach(f=>f.addEventListener('submit',async e=>{e.preventDefault();const i=f.querySelector('input'),b=f.querySelector('button'),m=f.parentElement.querySelector('.nl-msg'),email=i.value.trim();if(!email||!email.includes('@')||!email.includes('.')){m.textContent='Enter a valid email address.';return;}b.disabled=true;b.textContent='Joining…';try{const r=await fetch('https://brevo-subscribe.vegassidekickcom.workers.dev',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email})});if(!r.ok)throw 0;m.textContent='You’re in. Watch your inbox for the useful stuff.';i.value='';b.textContent='Joined';}catch(x){m.textContent='Couldn’t add you just now. Try again in a minute.';b.disabled=false;b.textContent='Get Vegas Updates';}}));</script>'''

def clean(x): return re.sub(r'<[^>]+>','',x).replace('&quot;','"').replace('&amp;','&').strip()
def pics(s):
    out=[]
    pat=r'<a class="thumb" href="([^"]+)"><img src="([^"]+)"[^>]*alt="([^"]*)"[^>]*>.*?<span class="price-badge"><small>From</small>\s*([^<]+)</span>'
    for h,im,alt,pr in re.findall(pat,s,re.S):
        if h not in [x[0] for x in out]: out.append((h,clean(alt) or 'Top pick',im,pr.strip()))
        if len(out)==3: break
    if len(out)<3:
        for h,im,alt in re.findall(r'<a class="thumb" href="([^"]+)"><img src="([^"]+)"[^>]*alt="([^"]*)"',s,re.S):
            if h not in [x[0] for x in out]: out.append((h,clean(alt) or 'Top pick',im,''))
            if len(out)==3: break
    return out

def scrub(s,slug):
    if slug=='best-cirque-shows':
        s=s.replace('Best Cirque du Soleil Shows in Vegas 2026: All 5 Ranked','Best Cirque du Soleil Shows in Vegas 2026: All 4 Ranked').replace('All 5 Cirque du Soleil shows in Las Vegas','All 4 current Cirque du Soleil shows in Las Vegas').replace('"numberOfItems": 5','"numberOfItems": 4')
        s=re.sub(r'<article class="card">(?:(?!</article>).)*?mad-apple(?:(?!</article>).)*?</article>','',s,flags=re.S|re.I)
        s=re.sub(r',?\s*\{\s*"@type"\s*:\s*"ListItem"[^{}]*"name"\s*:\s*"Mad Apple"[^{}]*\}','',s,flags=re.S)
        s=re.sub(r'<div class="faq"><h3>What is the cheapest Cirque du Soleil show in Vegas\?</h3><p>.*?</p></div>','<div class="faq"><h3>What is the cheapest Cirque du Soleil show in Vegas?</h3><p>Mystère at TI is usually the lowest-priced current resident Cirque option, starting around $84. Check your date because prices move by performance and seat.</p></div>',s,flags=re.S)
    if slug=='best-shows-for-first-timers':
        s=s.replace('Mad Apple ($56), Mat Franco ($57), VEGAS! The Show ($63), and Mystère ($84) are all excellent, crowd-pleasing introductions to Vegas for under $70 a ticket.','Mat Franco, VEGAS! The Show, KÀ and Mystère are strong first-trip options when you want a lower price than the biggest Strip splurges. Check your date because starting prices move.').replace('plus one or two lower-key picks like a magic show or Mad Apple. Book the headliners early; they sell out.','plus one or two lower-key picks like a magic show, comedy show or classic Vegas revue.')
    if slug=='best-shows-for-couples': s=s.replace('O for romance, Mad Apple for a fun night out with cocktails, Mystère for value, and KÀ or Michael Jackson ONE for pure spectacle.','O for romance, Mystère for value, and KÀ or Michael Jackson ONE for pure spectacle. If you want comedy with the date-night energy, look at Absinthe instead.')
    s=s.replace('/shows/cirque/mad-apple/','/shows/cirque/').replace('Mad Apple','a now-closed Cirque production').replace('mad-apple','cirque')
    return s

def visuals(s):
    if 'guide-photo-system' not in s: s=s.replace('</head>',CSS+'</head>',1)
    if any(k in s for k in ['class="g-visuals"','class="ft-visuals"','class="guide-hero-visuals"']): return s
    p=pics(s)
    if len(p)<3: return s
    shots=''.join(f'<a class="guide-hero-shot" href="{h}"><img src="{im}" alt="{n}"><span class="guide-hero-price">From {pr}</span><span class="guide-hero-label">#{j} {n}</span></a>' for j,(h,n,im,pr) in enumerate(p,1))
    hs=s.find('<header class="g-hero">'); he=s.find('</header>',hs)
    if hs!=-1 and he!=-1:
        chunk=s[hs:he+9]; chunk=re.sub(r'<figure class="g-cover">.*?</figure>','',chunk,flags=re.S)
        a=chunk.find('<div class="wrap">')+18; b=chunk.rfind('</div>')
        inner=chunk[a:b]
        chunk=chunk[:a]+'<div class="guide-hero-grid"><div class="guide-hero-copy">'+inner+'</div><div class="guide-hero-visuals">'+shots+'</div></div>'+chunk[b:]
        s=s[:hs]+chunk+s[he+9:]
    for h,n,im,pr in p:
        s=re.sub(r'(<div class="guide-mini">.*?<a href="'+re.escape(h)+r'">)(?!<img class="qa-photo")',r'\1<img class="qa-photo" src="'+im+r'" alt="'+n.replace('"','&quot;')+r'">',s,count=1,flags=re.S)
    return s

def newsletter(s):
    s=re.sub(r'<div class="guide-email-note"><strong>Want the useful Vegas updates\?</strong><p>.*?</p></div>','',s,flags=re.S)
    if 'guide-newsletter-js' not in s: s=s.replace('</body>',JS+'</body>',1)
    if 'class="guide-newsletter"' in s: return s
    ends=list(re.finditer(r'</article>',s)); pos=ends[max(0,len(ends)//2-1)].end() if ends else s.find('<section class="guide-method">')
    return s[:pos]+NEWS+s[pos:]

for slug in GUIDES:
    p=Path('guides')/slug/'index.html'; s=p.read_text(encoding='utf-8'); s=scrub(s,slug); s=visuals(s); s=newsletter(s); p.write_text(s,encoding='utf-8'); print(slug)
for slug in GUIDES:
    s=(Path('guides')/slug/'index.html').read_text(encoding='utf-8'); assert 'Mad Apple' not in s and 'mad-apple' not in s; assert 'guide-email-note' not in s; assert 'guide-newsletter-form' in s; assert 'brevo-subscribe.vegassidekickcom.workers.dev' in s
print('all guide validations passed')

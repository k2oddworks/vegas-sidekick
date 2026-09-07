from pathlib import Path
import re

GUIDES=['best-adult-shows','best-cheap-vegas-shows','best-cirque-shows','best-magic-shows','best-shows-for-couples','best-shows-for-families','best-shows-for-first-timers','best-tribute-shows']

CSS='''<style id="guide-photo-system">
.g-hero .wrap{max-width:1180px}.guide-hero-grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(360px,.92fr);gap:42px;align-items:center}.guide-hero-copy{min-width:0}.guide-hero-visuals{display:grid;grid-template-columns:1fr 1fr;grid-template-rows:176px 176px;gap:10px;transform:rotate(-1deg)}.guide-hero-shot{position:relative;overflow:hidden;border-radius:18px;border:1px solid rgba(255,255,255,.24);box-shadow:0 18px 50px rgba(0,0,0,.25);background:#261147}.guide-hero-shot:first-child{grid-column:1/3}.guide-hero-shot img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .35s ease}.guide-hero-shot::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 42%,rgba(13,5,27,.8))}.guide-hero-label{position:absolute;left:12px;bottom:10px;z-index:2;font-family:var(--font-display);font-size:.76rem;font-weight:800;color:#fff}.guide-hero-price{position:absolute;right:10px;top:10px;z-index:2;background:var(--pink);color:#fff;border-radius:999px;padding:5px 9px;font-family:var(--font-display);font-size:.72rem;font-weight:800}.guide-hero-shot:hover img{transform:scale(1.035)}.guide-mini a{padding:0 0 14px;overflow:hidden}.guide-mini a small,.guide-mini a strong,.guide-mini a .mini-detail{margin-left:14px;margin-right:14px}.qa-photo{width:100%;height:112px;object-fit:cover;display:block;margin-bottom:12px}.mini-detail{display:block;font-size:.82rem;color:#5d566a;line-height:1.35;margin-top:5px}.guide-newsletter{margin:44px 0;padding:30px;border-radius:24px;background:linear-gradient(135deg,#6d28d9 0%,#e52b8d 62%,#ff4f79 100%);color:#fff;box-shadow:0 18px 44px rgba(77,24,139,.2);position:relative;overflow:hidden}.guide-newsletter:before{content:"";position:absolute;inset:0;background:radial-gradient(circle at 12% 0%,rgba(255,255,255,.18),transparent 32%);pointer-events:none}.guide-newsletter>*{position:relative;z-index:1}.guide-newsletter .nl-kicker{display:inline-flex;align-items:center;gap:7px;padding:6px 12px;border-radius:999px;background:rgba(47,13,66,.45);font-family:var(--font-mono);font-size:.7rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--lime)}.guide-newsletter h2{font-family:var(--font-display);font-size:clamp(1.7rem,4vw,2.35rem);line-height:1.05;margin:13px 0 8px;color:#fff}.guide-newsletter p{margin:0 0 18px;color:rgba(255,255,255,.9)}.guide-newsletter form{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:10px}.guide-newsletter input{width:100%;min-width:0;border:0;border-radius:14px;padding:15px 16px;font:600 1rem var(--font-body);color:var(--ink);background:#fff;outline:none}.guide-newsletter input:focus{box-shadow:0 0 0 3px rgba(198,242,46,.55)}.guide-newsletter button{border:0;border-radius:14px;padding:15px 20px;background:var(--lime);color:#171225;font:800 .95rem var(--font-display);cursor:pointer;white-space:nowrap}.guide-newsletter button:disabled{opacity:.7;cursor:wait}.guide-newsletter .nl-msg{min-height:1.25em;margin-top:9px;font-size:.8rem;font-weight:700}.guide-newsletter .nl-fine{font-size:.72rem;color:rgba(255,255,255,.75);margin-top:7px}@media(max-width:820px){.guide-hero-grid{grid-template-columns:1fr;gap:26px}.guide-hero-visuals{grid-template-rows:148px 148px;transform:none}.g-hero{padding-top:34px}}@media(max-width:600px){.guide-newsletter{padding:23px 20px;margin:34px 0}.guide-newsletter form{grid-template-columns:1fr}.guide-newsletter button{width:100%}}@media(max-width:520px){.guide-hero-visuals{grid-template-rows:124px 124px;gap:8px}.guide-hero-shot{border-radius:14px}.guide-hero-label{font-size:.66rem}.qa-photo{height:120px}}@media(prefers-reduced-motion:reduce){.guide-hero-shot img{transition:none}.guide-hero-shot:hover img{transform:none}}
</style>'''

NEWS='''<section class="guide-newsletter" aria-label="Vegas Sidekick email updates"><div class="nl-kicker">🌵 Spike's Insider List</div><h2>Useful Vegas updates, without the inbox nonsense.</h2><p>Show changes, worthwhile deals and the Vegas stuff I’d actually text a friend about.</p><form class="guide-newsletter-form" novalidate><input type="email" name="email" autocomplete="email" inputmode="email" placeholder="your@email.com" aria-label="Email address" required><button type="submit">Get Vegas Updates</button></form><div class="nl-msg" aria-live="polite"></div><div class="nl-fine">Occasional emails. Unsubscribe anytime.</div></section>'''

JS='''<script id="guide-newsletter-js">document.querySelectorAll('.guide-newsletter-form').forEach(function(form){form.addEventListener('submit',async function(e){e.preventDefault();const input=form.querySelector('input[type="email"]'),btn=form.querySelector('button'),msg=form.parentElement.querySelector('.nl-msg'),email=input.value.trim();if(!email||!email.includes('@')||!email.includes('.')){msg.textContent='Enter a valid email address.';return;}btn.disabled=true;btn.textContent='Joining…';msg.textContent='';try{const r=await fetch('https://brevo-subscribe.vegassidekickcom.workers.dev',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email})});if(!r.ok)throw new Error();msg.textContent='You’re in. Watch your inbox for the useful stuff.';input.value='';btn.textContent='Joined';}catch(err){msg.textContent='Couldn’t add you just now. Try again in a minute.';btn.disabled=false;btn.textContent='Get Vegas Updates';}});});</script>'''

def txt(x):
    return re.sub(r'<[^>]+>','',x).replace('&quot;','"').replace('&amp;','&').strip()

def ranking_picks(s):
    blocks=re.findall(r'<article class="card">.*?</article>',s,re.S)
    picks=[]
    for b in blocks:
        href=re.search(r'<a class="thumb" href="([^"]+)"',b)
        img=re.search(r'<a class="thumb" href="[^"]+"><img src="([^"]+)"',b)
        name=re.search(r'<div class="c-name">(.*?)</div>',b,re.S)
        price=re.search(r'<span class="price-badge"><small>From</small>\s*([^<]+)</span>',b,re.S)
        if href and img and name:
            picks.append((href.group(1),txt(name.group(1)),img.group(1),price.group(1).strip() if price else ''))
        if len(picks)==3: break
    return picks

def scrub_mad(s,slug):
    if slug=='best-cirque-shows':
        s=s.replace('Best Cirque du Soleil Shows in Vegas 2026: All 5 Ranked','Best Cirque du Soleil Shows in Vegas 2026: All 4 Ranked')
        s=s.replace('All 5 Cirque du Soleil shows in Las Vegas, ranked by a local — O, Michael Jackson ONE, KÀ, Mystère & Mad Apple. Real prices, venues, and which Cirque show is right for you.','All 4 current Cirque du Soleil shows in Las Vegas, ranked by a local — O, Michael Jackson ONE, KÀ and Mystère. Real prices, venues, and which Cirque show is right for you.')
        s=s.replace('All 5 Cirque du Soleil shows in Las Vegas','All 4 current Cirque du Soleil shows in Las Vegas')
        s=s.replace('"numberOfItems": 5','"numberOfItems": 4')
        s=re.sub(r',?\s*\{\s*"@type"\s*:\s*"ListItem"[^{}]*"name"\s*:\s*"Mad Apple"[^{}]*\}','',s,flags=re.S)
        s=re.sub(r'<article class="card">(?:(?!</article>).)*?mad-apple(?:(?!</article>).)*?</article>','',s,flags=re.S|re.I)
        s=re.sub(r'<div class="faq"><h3>What is the cheapest Cirque du Soleil show in Vegas\?</h3><p>.*?</p></div>','<div class="faq"><h3>What is the cheapest Cirque du Soleil show in Vegas?</h3><p>Mystère at TI is usually the lowest-priced current resident Cirque option, starting around $84. Check your date because prices move by performance and seat.</p></div>',s,flags=re.S)
    if slug=='best-shows-for-first-timers':
        s=s.replace('Mad Apple ($56), Mat Franco ($57), VEGAS! The Show ($63), and Mystère ($84) are all excellent, crowd-pleasing introductions to Vegas for under $70 a ticket.','Mat Franco, VEGAS! The Show, KÀ and Mystère are strong first-trip options when you want a lower price than the biggest Strip splurges. Check your date because starting prices move.')
        s=s.replace('plus one or two lower-key picks like a magic show or Mad Apple. Book the headliners early; they sell out.','plus one or two lower-key picks like a magic show, comedy show or classic Vegas revue.')
        s=re.sub(r'<div class="faq"><h3>What\'s a good first Vegas show that isn\'t too expensive\?</h3><p>.*?</p></div>','<div class="faq"><h3>What\'s a good first Vegas show that isn\'t too expensive?</h3><p>Mat Franco, VEGAS! The Show, KÀ and Mystère are strong first-trip options when you want a lower price than the biggest Strip splurges. Check your date because starting prices move.</p></div>',s,flags=re.S)
        s=re.sub(r'<div class="faq"><h3>How many shows should I see on my first Vegas trip\?</h3><p>.*?</p></div>','<div class="faq"><h3>How many shows should I see on my first Vegas trip?</h3><p>Most first-timers see one to three shows across a long weekend — usually one big spectacle plus one or two lower-key picks such as magic, comedy or a classic Vegas revue.</p></div>',s,flags=re.S)
    if slug=='best-shows-for-couples':
        s=s.replace('O for romance, Mad Apple for a fun night out with cocktails, Mystère for value, and KÀ or Michael Jackson ONE for pure spectacle.','O for romance, Mystère for value, and KÀ or Michael Jackson ONE for pure spectacle. If you want comedy with the date-night energy, look at Absinthe instead.')
    if 'Mad Apple' in s or 'mad-apple' in s:
        s=s.replace('/shows/cirque/mad-apple/','/shows/cirque/')
        s=s.replace('Mad Apple','a now-closed Cirque production').replace('mad-apple','cirque')
    return s

def add_visuals(s):
    if 'guide-photo-system' not in s:s=s.replace('</head>',CSS+'\n</head>',1)
    if any(x in s for x in ['class="g-visuals"','class="ft-visuals"','class="guide-hero-visuals"']):return s
    picks=ranking_picks(s)
    if len(picks)<3: raise RuntimeError('need three ranking cards')
    shots=''.join(f'<a class="guide-hero-shot" href="{h}"><img src="{im}" alt="{n}">'+(f'<span class="guide-hero-price">From {pr}</span>' if pr else '')+f'<span class="guide-hero-label">#{i} {n}</span></a>' for i,(h,n,im,pr) in enumerate(picks,1))
    hm=re.search(r'(<header class="g-hero"><div class="wrap">)(.*?)(</div></header>)',s,re.S)
    if not hm: raise RuntimeError('hero missing')
    inner=re.sub(r'\s*<figure class="g-cover">.*?</figure>\s*','',hm.group(2),flags=re.S)
    replacement=hm.group(1)+'<div class="guide-hero-grid"><div class="guide-hero-copy">'+inner+'</div><div class="guide-hero-visuals" aria-label="Photos of the top three picks">'+shots+'</div></div>'+hm.group(3)
    s=s[:hm.start()]+replacement+s[hm.end():]
    m=re.search(r'<div class="guide-mini">(.*?)</div>',s,re.S)
    if m:
        block=m.group(1)
        for h,n,im,pr in picks:
            am=re.search(r'<a href="'+re.escape(h)+r'">(.*?)</a>',block,re.S)
            if not am or 'qa-photo' in am.group(1):continue
            body=am.group(1); sm=re.search(r'(<small>.*?</small>\s*<strong>.*?</strong>)(.*)',body,re.S)
            if sm:
                newbody=f'<img class="qa-photo" src="{im}" alt="{n}">'+sm.group(1)+f'<span class="mini-detail">{txt(sm.group(2))}</span>'
                block=block[:am.start(1)]+newbody+block[am.end(1):]
        s=s[:m.start(1)]+block+s[m.end(1):]
    return s

def add_news(s):
    s=re.sub(r'<div class="guide-email-note"><strong>Want the useful Vegas updates\?</strong><p>.*?</p></div>','',s,flags=re.S)
    if 'guide-newsletter-js' not in s:s=s.replace('</body>',JS+'\n</body>',1)
    if 'class="guide-newsletter"' in s:return s
    ends=list(re.finditer(r'</article>',s))
    if not ends:raise RuntimeError('no articles')
    pos=ends[max(1,min(len(ends)-1,len(ends)//2-1))].end()
    return s[:pos]+'\n'+NEWS+'\n'+s[pos:]

for slug in GUIDES:
    p=Path('guides')/slug/'index.html'; s=p.read_text(encoding='utf-8')
    s=scrub_mad(s,slug); s=add_visuals(s); s=add_news(s); p.write_text(s,encoding='utf-8'); print('updated',slug)

for slug in GUIDES:
    s=(Path('guides')/slug/'index.html').read_text(encoding='utf-8')
    assert 'Mad Apple' not in s and 'mad-apple' not in s,slug
    assert 'guide-email-note' not in s,slug
    assert 'guide-newsletter-form' in s and 'brevo-subscribe.vegassidekickcom.workers.dev' in s,slug
    assert any(x in s for x in ['class="g-visuals"','class="ft-visuals"','class="guide-hero-visuals"']),slug
print('all guide validations passed')

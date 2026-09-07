from pathlib import Path
import re

GUIDES = [
    'best-adult-shows','best-cheap-vegas-shows','best-cirque-shows','best-magic-shows',
    'best-shows-for-couples','best-shows-for-families','best-shows-for-first-timers','best-tribute-shows'
]

PHOTO_CSS = r'''<style id="guide-photo-system">
.g-hero .wrap{max-width:1180px}.guide-hero-grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(360px,.92fr);gap:42px;align-items:center}.guide-hero-copy{min-width:0}.guide-hero-visuals{display:grid;grid-template-columns:1fr 1fr;grid-template-rows:176px 176px;gap:10px;transform:rotate(-1deg)}.guide-hero-shot{position:relative;overflow:hidden;border-radius:18px;border:1px solid rgba(255,255,255,.24);box-shadow:0 18px 50px rgba(0,0,0,.25);background:#261147}.guide-hero-shot:first-child{grid-column:1/3}.guide-hero-shot img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .35s ease}.guide-hero-shot::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 42%,rgba(13,5,27,.8))}.guide-hero-label{position:absolute;left:12px;bottom:10px;z-index:2;font-family:var(--font-display);font-size:.76rem;font-weight:800;color:#fff}.guide-hero-price{position:absolute;right:10px;top:10px;z-index:2;background:var(--pink);color:#fff;border-radius:999px;padding:5px 9px;font-family:var(--font-display);font-size:.72rem;font-weight:800}.guide-hero-shot:hover img{transform:scale(1.035)}.guide-mini a{padding:0 0 14px;overflow:hidden}.guide-mini a small,.guide-mini a strong,.guide-mini a .mini-detail{margin-left:14px;margin-right:14px}.qa-photo{width:100%;height:112px;object-fit:cover;display:block;margin-bottom:12px}.mini-detail{display:block;font-size:.82rem;color:#5d566a;line-height:1.35;margin-top:5px}
.guide-newsletter{margin:44px 0;padding:30px;border-radius:24px;background:linear-gradient(135deg,#6d28d9 0%,#e52b8d 62%,#ff4f79 100%);color:#fff;box-shadow:0 18px 44px rgba(77,24,139,.2);position:relative;overflow:hidden}.guide-newsletter:before{content:"";position:absolute;inset:0;background:radial-gradient(circle at 12% 0%,rgba(255,255,255,.18),transparent 32%);pointer-events:none}.guide-newsletter>*{position:relative;z-index:1}.guide-newsletter .nl-kicker{display:inline-flex;align-items:center;gap:7px;padding:6px 12px;border-radius:999px;background:rgba(47,13,66,.45);font-family:var(--font-mono);font-size:.7rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--lime)}.guide-newsletter h2{font-family:var(--font-display);font-size:clamp(1.7rem,4vw,2.35rem);line-height:1.05;margin:13px 0 8px;color:#fff}.guide-newsletter p{margin:0 0 18px;color:rgba(255,255,255,.9)}.guide-newsletter form{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:10px}.guide-newsletter input{width:100%;min-width:0;border:0;border-radius:14px;padding:15px 16px;font:600 1rem var(--font-body);color:var(--ink);background:#fff;outline:none}.guide-newsletter input:focus{box-shadow:0 0 0 3px rgba(198,242,46,.55)}.guide-newsletter button{border:0;border-radius:14px;padding:15px 20px;background:var(--lime);color:#171225;font:800 .95rem var(--font-display);cursor:pointer;white-space:nowrap}.guide-newsletter button:disabled{opacity:.7;cursor:wait}.guide-newsletter .nl-msg{min-height:1.25em;margin-top:9px;font-size:.8rem;font-weight:700}.guide-newsletter .nl-fine{font-size:.72rem;color:rgba(255,255,255,.75);margin-top:7px}
@media(max-width:820px){.guide-hero-grid{grid-template-columns:1fr;gap:26px}.guide-hero-visuals{grid-template-rows:148px 148px;transform:none}.g-hero{padding-top:34px}}@media(max-width:600px){.guide-newsletter{padding:23px 20px;margin:34px 0}.guide-newsletter form{grid-template-columns:1fr}.guide-newsletter button{width:100%}}@media(max-width:520px){.guide-hero-visuals{grid-template-rows:124px 124px;gap:8px}.guide-hero-shot{border-radius:14px}.guide-hero-label{font-size:.66rem}.qa-photo{height:120px}}@media(prefers-reduced-motion:reduce){.guide-hero-shot img{transition:none}.guide-hero-shot:hover img{transform:none}}
</style>'''

NEWSLETTER = r'''<section class="guide-newsletter" aria-label="Vegas Sidekick email updates"><div class="nl-kicker">🌵 Spike's Insider List</div><h2>Useful Vegas updates, without the inbox nonsense.</h2><p>Show changes, worthwhile deals and the Vegas stuff I’d actually text a friend about.</p><form class="guide-newsletter-form" novalidate><input type="email" name="email" autocomplete="email" inputmode="email" placeholder="your@email.com" aria-label="Email address" required><button type="submit">Get Vegas Updates</button></form><div class="nl-msg" aria-live="polite"></div><div class="nl-fine">Occasional emails. Unsubscribe anytime.</div></section>'''

NEWS_JS = r'''<script id="guide-newsletter-js">
document.querySelectorAll('.guide-newsletter-form').forEach(function(form){
  form.addEventListener('submit',async function(e){
    e.preventDefault();
    const input=form.querySelector('input[type="email"]'),btn=form.querySelector('button'),msg=form.parentElement.querySelector('.nl-msg');
    const email=input.value.trim();
    if(!email || !email.includes('@') || !email.includes('.')){msg.textContent='Enter a valid email address.';return;}
    btn.disabled=true;btn.textContent='Joining…';msg.textContent='';
    try{
      const r=await fetch('https://brevo-subscribe.vegassidekickcom.workers.dev',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email:email})});
      if(!r.ok) throw new Error('signup failed');
      msg.textContent='You’re in. Watch your inbox for the useful stuff.';input.value='';btn.textContent='Joined';
    }catch(err){msg.textContent='Couldn’t add you just now. Try again in a minute.';btn.disabled=false;btn.textContent='Get Vegas Updates';}
  });
});
</script>'''

def clean_text(x):
    x=re.sub(r'<[^>]+>','',x)
    return x.replace('&quot;','"').replace('&amp;','&').replace('&#39;',"'").strip()

def top_three(s):
    m=re.search(r'<div class="guide-mini">(.*?)</div>',s,re.S)
    if not m: return []
    block=m.group(1)
    anchors=re.findall(r'<a href="([^"]+)">(.*?)</a>',block,re.S)[:3]
    out=[]
    for href,body in anchors:
        name_m=re.search(r'<strong>(.*?)</strong>',body,re.S)
        name=clean_text(name_m.group(1)) if name_m else 'Top pick'
        # Find matching ranking thumb and price
        pat=r'<a class="thumb" href="'+re.escape(href)+r'"><img src="([^"]+)"[^>]*>.*?<span class="price-badge"><small>From</small>\s*([^<]+)</span>'
        im=re.search(pat,s,re.S)
        if not im:
            pat2=r'<a class="thumb" href="'+re.escape(href)+r'"><img src="([^"]+)"'
            im2=re.search(pat2,s,re.S)
            img=im2.group(1) if im2 else ''
            price=''
        else:
            img,price=im.group(1),im.group(2).strip()
        out.append((href,name,img,price,body))
    return out

def apply_visuals(s):
    # Leave the two already-upgraded hero systems intact, but normalize top-card photos via common CSS.
    if 'guide-photo-system' not in s:
        s=s.replace('</head>',PHOTO_CSS+'\n</head>',1)
    if 'class="g-visuals"' in s or 'class="ft-visuals"' in s or 'class="guide-hero-visuals"' in s:
        return s
    picks=top_three(s)
    if len(picks)<3 or any(not p[2] for p in picks):
        raise RuntimeError('could not resolve top-three photography')
    shots=''.join(
        f'<a class="guide-hero-shot" href="{href}"><img src="{img}" alt="{name}">'+
        (f'<span class="guide-hero-price">From {price}</span>' if price else '')+
        f'<span class="guide-hero-label">#{i} {name}</span></a>'
        for i,(href,name,img,price,_) in enumerate(picks,1)
    )
    # Wrap hero copy, replacing the old cover if present.
    hm=re.search(r'(<header class="g-hero"><div class="wrap">)(.*?)(</div></header>)',s,re.S)
    if not hm: raise RuntimeError('hero not found')
    inner=hm.group(2)
    inner=re.sub(r'\s*<figure class="g-cover">.*?</figure>\s*','',inner,flags=re.S)
    new=hm.group(1)+'<div class="guide-hero-grid"><div class="guide-hero-copy">'+inner+'</div><div class="guide-hero-visuals" aria-label="Photos of the top three picks">'+shots+'</div></div>'+hm.group(3)
    s=s[:hm.start()]+new+s[hm.end():]
    # Add photos to top-three quick cards.
    m=re.search(r'<div class="guide-mini">(.*?)</div>',s,re.S)
    if m:
        block=m.group(1)
        for href,name,img,price,body in picks:
            if 'qa-photo' in body: continue
            detail=body
            sm=re.search(r'(<small>.*?</small>\s*<strong>.*?</strong>)(.*)',body,re.S)
            if sm:
                detail_txt=clean_text(sm.group(2))
                rebuilt=f'<img class="qa-photo" src="{img}" alt="{name}">'+sm.group(1)+f'<span class="mini-detail">{detail_txt}</span>'
                block=block.replace(f'<a href="{href}">{body}</a>',f'<a href="{href}">{rebuilt}</a>',1)
        s=s[:m.start(1)]+block+s[m.end(1):]
    return s

def add_newsletter(s):
    # Remove the old non-functional end-of-guide prompt.
    s=re.sub(r'<div class="guide-email-note"><strong>Want the useful Vegas updates\?</strong><p>.*?</p></div>','',s,flags=re.S)
    if 'guide-newsletter-js' not in s:
        s=s.replace('</body>',NEWS_JS+'\n</body>',1)
    if 'class="guide-newsletter"' in s:
        return s
    # Put signup around the middle of the ranking, after roughly half the ranking cards.
    articles=list(re.finditer(r'</article>',s))
    if not articles:
        raise RuntimeError('no ranking articles found')
    idx=max(1,min(len(articles)-1,len(articles)//2-1))
    pos=articles[idx].end()
    return s[:pos]+'\n'+NEWSLETTER+'\n'+s[pos:]

def remove_mad_apple(s,slug):
    if slug=='best-cirque-shows':
        s=s.replace('Best Cirque du Soleil Shows in Vegas 2026: All 5 Ranked','Best Cirque du Soleil Shows in Vegas 2026: All 4 Ranked')
        s=s.replace('All 5 Cirque du Soleil shows in Las Vegas, ranked by a local — O, Michael Jackson ONE, KÀ, Mystère & Mad Apple.','All 4 current Cirque du Soleil shows in Las Vegas, ranked by a local — O, Michael Jackson ONE, KÀ and Mystère.')
        s=s.replace('All 5 Cirque du Soleil shows in Las Vegas','All 4 current Cirque du Soleil shows in Las Vegas')
        s=s.replace('"numberOfItems": 5','"numberOfItems": 4')
        s=re.sub(r',?\s*\{\s*"@type":\s*"ListItem"[^{}]*"name":\s*"Mad Apple"[^{}]*\}', '', s, flags=re.S)
        s=re.sub(r'<article class="card">(?:(?!</article>).)*?/shows/cirque/mad-apple/(?:(?!</article>).)*?</article>','',s,flags=re.S)
        s=re.sub(r'<div class="faq"><h3>What is the cheapest Cirque du Soleil show in Vegas\?</h3><p>.*?</p></div>', '<div class="faq"><h3>What is the cheapest Cirque du Soleil show in Vegas?</h3><p>Mystère at TI is usually the lowest-priced current resident Cirque option, starting around $84. Check your date before booking because prices move by performance and seat.</p></div>', s, flags=re.S)
    elif slug=='best-shows-for-first-timers':
        s=re.sub(r'<div class="faq"><h3>What\'s a good first Vegas show that isn\'t too expensive\?</h3><p>.*?</p></div>', '<div class="faq"><h3>What\'s a good first Vegas show that isn\'t too expensive?</h3><p>Mat Franco, VEGAS! The Show, KÀ and Mystère are all strong first-trip options when you want a lower price than the biggest Strip splurges. Check your date because starting prices move.</p></div>', s, flags=re.S)
        s=re.sub(r'<div class="faq"><h3>How many shows should I see on my first Vegas trip\?</h3><p>.*?</p></div>', '<div class="faq"><h3>How many shows should I see on my first Vegas trip?</h3><p>Most first-timers see one to three shows across a long weekend — usually one big spectacle plus one or two lower-key picks such as magic, comedy or a classic Vegas revue.</p></div>', s, flags=re.S)
        # Structured FAQ answers
        s=s.replace('Mad Apple ($56), Mat Franco ($57), VEGAS! The Show ($63), and Mystère ($84) are all excellent, crowd-pleasing introductions to Vegas for under $70 a ticket.','Mat Franco, VEGAS! The Show, KÀ and Mystère are strong first-trip options when you want a lower price than the biggest Strip splurges. Check your date because starting prices move.')
        s=s.replace('plus one or two lower-key picks like a magic show or Mad Apple. Book the headliners early; they sell out.','plus one or two lower-key picks like a magic show, comedy show or classic Vegas revue.')
    elif slug=='best-shows-for-couples':
        s=s.replace('O for romance, Mad Apple for a fun night out with cocktails, Mystère for value, and KÀ or Michael Jackson ONE for pure spectacle.','O for romance, Mystère for value, and KÀ or Michael Jackson ONE for pure spectacle. If you want comedy with the date-night energy, look at Absinthe instead.')
    return s

for slug in GUIDES:
    p=Path('guides')/slug/'index.html'
    s=p.read_text(encoding='utf-8')
    s=remove_mad_apple(s,slug)
    s=apply_visuals(s)
    s=add_newsletter(s)
    p.write_text(s,encoding='utf-8')
    print('updated',slug)

# Validation: every article guide gets the visual treatment or its existing equivalent, a working signup, and no Mad Apple refs.
for slug in GUIDES:
    s=(Path('guides')/slug/'index.html').read_text(encoding='utf-8')
    assert 'guide-newsletter-form' in s, slug
    assert 'brevo-subscribe.vegassidekickcom.workers.dev' in s, slug
    assert 'guide-email-note' not in s, slug
    assert ('guide-hero-visuals' in s or 'class="g-visuals"' in s or 'class="ft-visuals"' in s), slug
    assert 'Mad Apple' not in s and 'mad-apple' not in s, slug
print('all guide validations passed')

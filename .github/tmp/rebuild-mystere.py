from pathlib import Path
import json, re, html

ROOT = Path('.')
PAGE = ROOT / 'shows/cirque/mystere/index.html'
SITEMAP = ROOT / 'sitemap.xml'
LAYOUT = ROOT / 'data/seat-layouts/mystere-theatre.json'
CSS = ROOT / 'assets/seat-layouts/mystere-theatre.css'
JS = ROOT / 'assets/seat-layouts/mystere-theatre.js'
SVG = ROOT / 'images/mystere-theatre-seating-chart.svg'
TICKET = 'https://spotlight.vegas/shows/cirque-du-soleil/mystere/ref/vegassidekick'
DATE = '2026-09-09'

def sub_once(text, pattern, replacement, label, flags=re.S):
    out, n = re.subn(pattern, lambda _m: replacement, text, count=1, flags=flags)
    if n != 1:
        raise SystemExit(f'{label}: expected 1 replacement, got {n}')
    return out

seat_data = {
    "id": "mystere-theatre",
    "venue": "Mystère Theatre – TI Hotel",
    "address": "3300 S Las Vegas Blvd, Las Vegas, NV 89109",
    "viewBox": "0 0 1000 860",
    "stage": {
        "path": "M180 790 H820 V700 L760 660 H650 V540 H610 V485 Q500 445 390 485 V540 H350 V660 H240 L180 700 Z",
        "label_x": 500,
        "label_y": 720
    },
    "sections": [
        {"id":"101","label":"101","path":"M650 620 L800 620 L800 520 L650 520 Z","label_x":725,"label_y":575,"color":"#ff2e7e","description":"Lower-level section near the stage on the right side. Close to the performers with a clear view into the room."},
        {"id":"102","label":"102","path":"M650 505 Q730 485 805 455 L805 365 Q735 320 655 315 L610 430 Z","label_x":720,"label_y":410,"color":"#ff2e7e","description":"Lower-level right-center section. A closer view with a broad look across the stage and aerial space."},
        {"id":"103","label":"103","path":"M385 320 Q500 285 615 320 L585 430 Q500 405 415 430 Z","label_x":500,"label_y":365,"color":"#ff2e7e","description":"Lower-level center section. Straight-on and close, with a centered view of floor and aerial work."},
        {"id":"104","label":"104","path":"M350 505 Q270 485 195 455 L195 365 Q265 320 345 315 L390 430 Z","label_x":280,"label_y":410,"color":"#ff2e7e","description":"Lower-level left-center section. A closer view with a broad look across the stage and aerial space."},
        {"id":"105","label":"105","path":"M350 620 L200 620 L200 520 L350 520 Z","label_x":275,"label_y":575,"color":"#ff2e7e","description":"Lower-level section near the stage on the left side. Close to the performers with a clear view into the room."},
        {"id":"201","label":"201","path":"M820 570 L930 570 L925 350 L850 305 L805 365 L805 455 L820 475 Z","label_x":875,"label_y":455,"color":"#12c7b1","badge":"Wider view","description":"Outer 200-level section on the right. A wider side perspective that keeps the full stage and overhead work in view."},
        {"id":"202","label":"202","path":"M610 285 L740 330 L835 250 L800 125 Q715 85 625 75 L585 250 Z","label_x":700,"label_y":205,"color":"#8d3cff","badge":"Sweet spot","our_pick":True,"description":"One of our sweet-spot sections. Upper right-center gives you a broad look at the full stage and the aerial space above it."},
        {"id":"203","label":"203","path":"M390 75 Q500 45 610 75 L585 250 Q500 220 415 250 Z","label_x":500,"label_y":155,"color":"#8d3cff","badge":"Sweet spot","our_pick":True,"description":"One of our sweet-spot sections. Upper center gives you the most straight-on full-stage perspective in the 200 level."},
        {"id":"204","label":"204","path":"M375 75 Q285 85 200 125 L165 250 L260 330 L390 285 L415 250 Z","label_x":300,"label_y":205,"color":"#8d3cff","badge":"Sweet spot","our_pick":True,"description":"One of our sweet-spot sections. Upper left-center gives you a broad look at the full stage and the aerial space above it."},
        {"id":"205","label":"205","path":"M165 250 L85 300 L55 355 L55 490 L175 535 L205 455 L195 350 L260 330 Z","label_x":130,"label_y":390,"color":"#8d3cff","badge":"Sweet spot","our_pick":True,"description":"One of our sweet-spot sections. This upper-left section gives you a wide look across the room and strong full-production perspective."},
        {"id":"206","label":"206","path":"M55 520 L175 555 L175 650 L55 650 Z","label_x":115,"label_y":600,"color":"#12c7b1","badge":"Wider view","description":"Outer 200-level section on the left. A wider side perspective that keeps the full stage and overhead work in view."}
    ]
}
LAYOUT.parent.mkdir(parents=True, exist_ok=True)
LAYOUT.write_text(json.dumps(seat_data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

css = r'''.mystere-seat-guide{--ms-pink:#ff2e7e;--ms-purple:#8d3cff;--ms-amber:#ffb000;--ms-teal:#12c7b1;display:grid;grid-template-columns:minmax(0,1.24fr) minmax(280px,.76fr);gap:22px;align-items:start;margin-top:24px}
.mystere-map-shell{position:relative;overflow:hidden;border-radius:28px;padding:22px;background:radial-gradient(circle at 50% -5%,rgba(141,60,255,.2),transparent 28%),linear-gradient(180deg,#140923 0%,#0b0613 62%,#08070d 100%);border:1px solid rgba(255,255,255,.16);box-shadow:0 24px 60px rgba(13,4,24,.28)}
.mystere-map-shell svg{display:block;width:100%;height:auto}.mystere-map-zone{cursor:pointer;outline:none}.mystere-map-zone path{fill:var(--zone-color);stroke:rgba(255,255,255,.28);stroke-width:2;transition:filter .18s ease,stroke .18s ease,stroke-width .18s ease}.mystere-map-zone text{fill:#fff;font:800 30px Inter,Arial,sans-serif;text-anchor:middle;dominant-baseline:middle;pointer-events:none;text-shadow:0 2px 4px rgba(0,0,0,.55)}.mystere-map-zone:hover path,.mystere-map-zone:focus path{filter:brightness(1.1);stroke:#fff;stroke-width:4}.mystere-map-zone.is-active path{stroke:var(--ms-amber);stroke-width:6;filter:drop-shadow(0 0 10px rgba(255,176,0,.75))}
.mystere-stage{fill:#111116;stroke:rgba(255,176,0,.75);stroke-width:3}.mystere-stage-label{fill:#fff;font:800 31px Inter,Arial,sans-serif;text-anchor:middle;letter-spacing:.18em}.mystere-map-caption{text-align:center;margin:12px 0 2px}.mystere-map-caption strong{display:block;color:#fff;font-size:clamp(1.15rem,2vw,1.45rem)}.mystere-map-caption span{display:block;color:rgba(255,255,255,.72);font-size:.9rem;margin-top:5px}
.mystere-seat-detail{padding:20px;border-radius:20px;background:#fff;border:1px solid #e8e2ed;color:#21182a;box-shadow:0 12px 30px rgba(17,4,28,.08)}.mystere-seat-detail .tag{display:inline-block;font-size:.68rem;letter-spacing:.1em;text-transform:uppercase;font-weight:900;color:#171225;background:var(--ms-amber);padding:5px 8px;border-radius:999px}.mystere-seat-detail h3{margin:9px 0 8px;font-size:1.5rem}.mystere-seat-detail p{margin:0 0 16px;color:#5e5366;line-height:1.55}.mystere-seat-detail .cta{width:100%;text-align:center;justify-content:center}.mystere-legend{display:grid;gap:9px;margin-top:12px}.mystere-legend span{display:flex;align-items:center;gap:9px;font-size:.82rem;color:#6e6475}.mystere-legend i{width:14px;height:14px;border-radius:4px;background:var(--legend-color);box-shadow:0 0 12px color-mix(in srgb,var(--legend-color) 42%,transparent)}
.mystere-chart-gallery{position:relative}.mystere-chart-gallery:after{content:"Seating chart";position:absolute;left:12px;bottom:12px;padding:6px 9px;border-radius:999px;background:rgba(13,7,20,.82);color:#fff;font-size:.72rem;font-weight:800;letter-spacing:.04em;text-transform:uppercase;pointer-events:none}.mystere-chart-gallery img{object-fit:contain!important;background:#09060f}
#photos .gallery.gallery-4{grid-template-columns:repeat(2,minmax(0,1fr));grid-template-rows:repeat(2,minmax(0,1fr));height:560px}#photos .gallery.gallery-4 button:first-child{grid-row:auto}#photos .gallery.gallery-4 button{min-width:0;min-height:0}#photos .gallery.gallery-4 img{width:100%;height:100%;object-fit:cover}
.mystere-mobile-popover{display:none}.mystere-lb-nav{position:absolute!important;top:50%!important;transform:translateY(-50%);z-index:3;width:52px!important;height:52px!important;border-radius:50%!important;background:rgba(255,255,255,.94)!important;color:#17082e!important;font-size:2rem!important;line-height:1!important}.mystere-lb-prev{left:18px!important;right:auto!important}.mystere-lb-next{right:18px!important}.mystere-lb-count{position:absolute;left:50%;bottom:18px;transform:translateX(-50%);z-index:3;background:rgba(23,8,46,.82);color:#fff;padding:6px 11px;border-radius:999px;font-size:.8rem;font-weight:800;letter-spacing:.04em}
@media(max-width:820px){.mystere-seat-guide{grid-template-columns:1fr}.mystere-map-shell{padding:12px}.mystere-seat-detail,.mystere-legend{display:none}.mystere-mobile-popover{position:fixed;z-index:1100;left:14px;right:14px;bottom:98px;display:flex;align-items:flex-start;gap:12px;padding:14px 48px 14px 15px;border:1px solid rgba(255,176,0,.65);border-radius:16px;background:rgba(20,9,35,.96);box-shadow:0 14px 38px rgba(0,0,0,.38);color:#fff;opacity:0;pointer-events:none;transform:translateY(16px);transition:.2s}.mystere-mobile-popover.is-open{opacity:1;pointer-events:auto;transform:translateY(0)}.mystere-mobile-popover strong{display:block;font-size:1rem;margin:2px 0 4px}.mystere-mobile-popover p{margin:0;color:#ddd4e4;font-size:.82rem;line-height:1.45}.mystere-mobile-badge{display:inline-block;font-size:.62rem;font-weight:900;letter-spacing:.08em;text-transform:uppercase;color:#17082e;background:#ffb000;padding:4px 7px;border-radius:999px}.mystere-mobile-popover>button{position:absolute;right:9px;top:8px;width:30px;height:30px;border:0;border-radius:50%;background:rgba(255,255,255,.1);color:#fff;font-size:1.25rem}#photos .gallery.gallery-4{height:auto;grid-template-columns:1fr;grid-template-rows:auto}#photos .gallery.gallery-4 img{aspect-ratio:4/3}.mystere-chart-gallery img{object-fit:contain!important;aspect-ratio:4/3}.mystere-lb-nav{width:46px!important;height:46px!important}.mystere-lb-prev{left:8px!important}.mystere-lb-next{right:8px!important}.mystere-lb-count{bottom:100px}}
'''
CSS.parent.mkdir(parents=True, exist_ok=True)
CSS.write_text(css, encoding='utf-8')

js = r'''(()=>{
  const esc=s=>String(s??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
  async function mount(root){
    const url=root.dataset.layoutUrl,ticket=root.dataset.ticketUrl;
    try{
      const data=await fetch(url,{credentials:'same-origin'}).then(r=>{if(!r.ok)throw new Error(`HTTP ${r.status}`);return r.json()});
      const byId=Object.fromEntries(data.sections.map(s=>[s.id,s]));
      const zone=s=>`<g class="mystere-map-zone" data-zone="${esc(s.id)}" role="button" tabindex="0" aria-label="Section ${esc(s.label)}${s.badge?`, ${esc(s.badge)}`:''}" style="--zone-color:${esc(s.color)}"><path d="${esc(s.path)}"></path><text x="${esc(s.label_x)}" y="${esc(s.label_y)}">${esc(s.label)}</text></g>`;
      root.innerHTML=`<div><div class="mystere-map-shell"><svg viewBox="${esc(data.viewBox)}" role="img" aria-label="Mystère Theatre seating layout">${data.sections.map(zone).join('')}<path class="mystere-stage" d="${esc(data.stage.path)}"></path><text class="mystere-stage-label" x="${esc(data.stage.label_x)}" y="${esc(data.stage.label_y)}">STAGE</text></svg><div class="mystere-map-caption"><strong>${esc(data.venue)}</strong><span>${esc(data.address)}</span></div></div></div><div><div class="mystere-seat-detail" aria-live="polite"><span class="tag">Sweet spot</span><h3>Section 203</h3><p>${esc(byId['203'].description)}</p><a class="cta vs-ticket-primary" href="${esc(ticket)}" target="_blank" rel="noopener sponsored">Check seats →</a></div><div class="mystere-legend"><span><i style="--legend-color:#ff2e7e"></i>Sections 101–105 · lower level</span><span><i style="--legend-color:#8d3cff"></i>Sections 202–205 · Sweet spot / Our Pick</span><span><i style="--legend-color:#12c7b1"></i>Sections 201 & 206 · wider side view</span></div></div><div class="mystere-mobile-popover" aria-live="polite" aria-atomic="true"><div><span class="mystere-mobile-badge">Sweet spot</span><strong>Section 203</strong><p>${esc(byId['203'].description)}</p></div><button type="button" aria-label="Close seat description">×</button></div>`;
      const detail=root.querySelector('.mystere-seat-detail'),pop=root.querySelector('.mystere-mobile-popover');
      const badge=s=>s.badge||(s.our_pick?'Sweet spot':'Seat guide');
      const activate=(id,showPop=false)=>{
        const s=byId[id];if(!s)return;
        root.querySelectorAll('[data-zone]').forEach(el=>el.classList.toggle('is-active',el.dataset.zone===id));
        detail.querySelector('.tag').textContent=badge(s);
        detail.querySelector('h3').textContent=`Section ${s.label}`;
        detail.querySelector('p').textContent=s.description;
        pop.querySelector('.mystere-mobile-badge').textContent=badge(s);
        pop.querySelector('strong').textContent=`Section ${s.label}`;
        pop.querySelector('p').textContent=s.description;
        if(showPop&&matchMedia('(max-width:820px)').matches)pop.classList.add('is-open');
      };
      root.addEventListener('click',e=>{
        const z=e.target.closest('[data-zone]');if(z)activate(z.dataset.zone,true);
        if(e.target.closest('.mystere-mobile-popover>button'))pop.classList.remove('is-open');
      });
      root.addEventListener('keydown',e=>{
        const z=e.target.closest('[data-zone]');if(z&&(e.key==='Enter'||e.key===' ')){e.preventDefault();activate(z.dataset.zone,true)}
      });
      addEventListener('scroll',()=>pop.classList.remove('is-open'),{passive:true});
      activate('203');
    }catch(err){
      root.innerHTML='<p>Seat guide unavailable right now. Use the live ticket map to compare sections for your date.</p>';
      console.warn('Mystère Theatre seat guide:',err);
    }
  }
  function enhanceGallery(){
    const buttons=[...document.querySelectorAll('#photos .gallery button')],light=document.getElementById('lightbox');
    if(!buttons.length||!light)return;
    const img=light.querySelector('#lightboxImg, img');if(!img)return;
    let current=0,touchX=null,prev=light.querySelector('.mystere-lb-prev'),next=light.querySelector('.mystere-lb-next'),count=light.querySelector('.mystere-lb-count');
    if(!prev){
      prev=document.createElement('button');prev.type='button';prev.className='mystere-lb-nav mystere-lb-prev';prev.setAttribute('aria-label','Previous photo');prev.textContent='‹';light.appendChild(prev);
      next=document.createElement('button');next.type='button';next.className='mystere-lb-nav mystere-lb-next';next.setAttribute('aria-label','Next photo');next.textContent='›';light.appendChild(next);
      count=document.createElement('div');count.className='mystere-lb-count';light.appendChild(count);
    }
    const show=i=>{current=(i+buttons.length)%buttons.length;const thumb=buttons[current].querySelector('img');img.src=thumb.currentSrc||thumb.src;img.alt=thumb.alt||'Mystère photo';count.textContent=`${current+1} of ${buttons.length}`};
    buttons.forEach((b,i)=>b.addEventListener('click',()=>show(i)));
    prev.addEventListener('click',e=>{e.stopPropagation();show(current-1)});
    next.addEventListener('click',e=>{e.stopPropagation();show(current+1)});
    addEventListener('keydown',e=>{if(!light.classList.contains('open'))return;if(e.key==='ArrowLeft')show(current-1);if(e.key==='ArrowRight')show(current+1)});
    light.addEventListener('touchstart',e=>{touchX=e.changedTouches[0]?.clientX??null},{passive:true});
    light.addEventListener('touchend',e=>{if(touchX==null)return;const dx=(e.changedTouches[0]?.clientX??touchX)-touchX;touchX=null;if(Math.abs(dx)>45)show(current+(dx<0?1:-1))},{passive:true});
  }
  document.querySelectorAll('[data-seat-layout="mystere-theatre"]').forEach(mount);
  enhanceGallery();
})();
'''
JS.parent.mkdir(parents=True, exist_ok=True)
JS.write_text(js, encoding='utf-8')

d = json.loads(LAYOUT.read_text(encoding='utf-8'))
parts = [
    '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="1300" viewBox="0 0 1200 1300">',
    '<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#140923"/><stop offset="1" stop-color="#07070c"/></linearGradient><filter id="glow"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>',
    '<rect width="1200" height="1300" rx="42" fill="url(#bg)"/>',
    '<text x="70" y="72" fill="#fff" font-family="Arial,sans-serif" font-size="42" font-weight="800">vegas <tspan fill="#ff2e7e">sidekick</tspan></text>',
    '<text x="72" y="108" fill="#d9d1df" font-family="Arial,sans-serif" font-size="17" letter-spacing="5">SHOWS • TICKETS • GOOD TIMES</text>',
    '<g transform="translate(100 120)">'
]
for s in d['sections']:
    stroke = '#ffb000' if s.get('our_pick') else '#ffffff'
    sw = '5' if s.get('our_pick') else '2'
    sop = '1' if s.get('our_pick') else '.28'
    glow = ' filter="url(#glow)"' if s.get('our_pick') else ''
    parts.append(f'<path d="{html.escape(s["path"])}" fill="{s["color"]}" stroke="{stroke}" stroke-width="{sw}" stroke-opacity="{sop}"{glow}/>')
    parts.append(f'<text x="{s["label_x"]}" y="{s["label_y"]}" text-anchor="middle" dominant-baseline="middle" fill="#fff" font-family="Arial,sans-serif" font-size="30" font-weight="800">{html.escape(s["label"])}</text>')
parts += [
    f'<path d="{html.escape(d["stage"]["path"])}" fill="#111116" stroke="#ffb000" stroke-width="3" stroke-opacity=".75"/>',
    f'<text x="{d["stage"]["label_x"]}" y="{d["stage"]["label_y"]}" text-anchor="middle" fill="#fff" font-family="Arial,sans-serif" font-size="31" font-weight="800" letter-spacing="7">STAGE</text>',
    '</g>',
    '<rect x="350" y="1025" width="500" height="54" rx="27" fill="#ffb000"/>',
    '<text x="600" y="1061" text-anchor="middle" fill="#171225" font-family="Arial,sans-serif" font-size="21" font-weight="900" letter-spacing="2">OUR PICK · SECTIONS 202–205</text>',
    '<text x="600" y="1145" text-anchor="middle" fill="#fff" font-family="Arial,sans-serif" font-size="34" font-weight="800">Mystère Theatre – TI Hotel</text>',
    '<text x="600" y="1188" text-anchor="middle" fill="#d7cedd" font-family="Arial,sans-serif" font-size="21">3300 S Las Vegas Blvd, Las Vegas, NV 89109</text>',
    '<text x="600" y="1240" text-anchor="middle" fill="#a9a0b1" font-family="Arial,sans-serif" font-size="17">Sections are shown by physical location; Sweet spot is Vegas Sidekick’s recommendation.</text>',
    '</svg>'
]
SVG.parent.mkdir(parents=True, exist_ok=True)
SVG.write_text('\n'.join(parts), encoding='utf-8')

text = PAGE.read_text(encoding='utf-8')
text = sub_once(text, r'<title>.*?</title>', '<title>Mystère by Cirque du Soleil Las Vegas Tickets from $84</title>', 'title')
text = sub_once(text, r'<meta content="[^"]*" name="description"/>', '<meta content="Mystère by Cirque du Soleil is a 90-minute Cirque production at TI Las Vegas. Tickets from $84. Compare showtimes and seating sections." name="description"/>', 'meta description')
text = re.sub(r'<style>.*?</style>\s*', '', text, flags=re.S)

faqs = [
    ('How much are Mystère tickets?', 'Tickets currently start at $84. Other price points may be available depending on the performance and seating section.'),
    ('Which seats should I buy for Mystère?', 'Sections 202–205 are our sweet spot. They sit in the 200 level around the center of the room and give you a broad look at both the stage and aerial work.'),
    ('How long is Mystère?', 'About 90 minutes with no intermission.'),
    ('What days and times does Mystère perform?', 'Mystère performs Monday, Tuesday, Friday, Saturday and Sunday at 6:30 PM and 9 PM, with Wednesday and Thursday dark. Check the booking screen for the exact schedule on your date.'),
    ('Is Mystère good for kids?', 'Mystère is listed for all ages. The show leans on acrobatics, aerial work, physical comedy and visual spectacle, which makes it an easy Cirque option for mixed-age groups.'),
    ('6:30 PM or 9 PM — which should I pick?', 'The production is the same. I’d use 6:30 PM for families or if you want dinner afterward; 9 PM works better if you want dinner first and the show to be the main event.'),
    ('Where is Mystère?', 'Mystère Theatre is inside TI Las Vegas at 3300 S Las Vegas Blvd. Give yourself time to get from parking or rideshare through the property to the theater.')
]
faq_schema = {'@context':'https://schema.org','@type':'FAQPage','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in faqs]}
text = sub_once(text, r'<script type="application/ld\+json">\{"@context":"https://schema\.org","@type":"FAQPage".*?</script>', '<script type="application/ld+json">'+json.dumps(faq_schema, ensure_ascii=False, separators=(',',':'))+'</script>', 'FAQ schema')
text = re.sub(r'"dateModified":"[^"]+"', f'"dateModified":"{DATE}"', text)
text = re.sub(r'"lastReviewed":"[^"]+"', f'"lastReviewed":"{DATE}"', text)

head_assets = '''<link href="/assets/show-canonical.css?v=2" rel="stylesheet"/><link href="/assets/ticket-cta.css" rel="stylesheet"/><link href="/assets/show-savings.css" rel="stylesheet"/><link href="/assets/seat-layouts/mystere-theatre.css?v=1" rel="stylesheet"/><style id="mystere-benchmark-final">
@media (min-width:801px){
  .hero-grid{grid-template-columns:minmax(0,1.02fr) minmax(0,.98fr);overflow:visible}
  .hero-copy{position:relative;z-index:2;padding-right:72px}
  .hero-media{position:relative;z-index:1;margin-left:-112px;overflow:hidden}
  .hero-media img{object-position:center center}
  .hero-media:after{background:linear-gradient(90deg,#2c0b4e 0%,rgba(44,11,78,.94) 12%,rgba(44,11,78,.58) 28%,rgba(44,11,78,.16) 46%,transparent 62%)}
  #quick .verdict-grid{grid-template-columns:1fr;max-width:920px}
  #quick .decision{max-width:760px;margin-top:18px}
  #quick .decision-card.good{display:flex;align-items:center;gap:16px;padding:14px 18px;border-top:0;border-left:6px solid var(--gold);min-height:0}
  #quick .decision-card.good h3{margin:0;white-space:nowrap}
  #quick .decision-card.good p{margin:0}
}
</style>'''
text = re.sub(r'<link href="/assets/ticket-cta\.css" rel="stylesheet"/><link rel="stylesheet" href="/assets/show-savings\.css">', '', text)
text = text.replace('</head>', head_assets + '</head>', 1)

faq_html = ''.join(f'<details><summary>{html.escape(q)}</summary><div>{html.escape(a)}</div></details>' for q,a in faqs)
body = f'''<body data-canonical-layout="2"><div class="progress"></div><a class="skip" href="#main">Skip to content</a><div id="vs-header"></div>
<header class="hero"><div class="hero-grid"><div class="hero-copy"><div class="crumbs"><a href="/">Home</a><span>›</span><a href="/shows/cirque/">Cirque</a><span>›</span>Mystère</div><div class="eyebrow">Vegas Cirque · Mystère Theatre – TI Hotel</div><h1>Mystère</h1><p class="hero-dek">90 minutes of classic Cirque acrobatics, aerial work and physical comedy. Book it if you want the original Vegas Cirque formula without a giant story getting between you and the acts.</p><div class="chips"><span class="chip">90 minutes</span><span class="chip">All ages</span><span class="chip">Mystère Theatre – TI Hotel</span></div><div class="buybox"><div class="price"><small>Tickets from</small>$84</div><a class="cta vs-ticket-primary" href="{TICKET}" rel="noopener sponsored" target="_blank">Get Tickets →</a></div><div class="updated">Tickets start at $84. Other price points may be available.</div></div><div class="hero-media" data-mobile-fit="safe" style="--mobile-hero-image:url('/images/mystere-hero.jpg');--mobile-hero-position:center center"><img alt="Mystère by Cirque du Soleil at TI Las Vegas" fetchpriority="high" src="/images/mystere-hero.jpg"/></div></div></header>
<section class="facts"><div class="wrap facts-grid"><div class="fact"><strong>90 min</strong><span>Runtime</span></div><div class="fact"><strong>$84</strong><span>Tickets from</span></div><div class="fact"><strong>6:30 &amp; 9 PM</strong><span>Start times</span></div><div class="fact"><strong>All ages</strong><span>Age guidance</span></div></div></section>
<div class="ticker"><div class="ticker-track"><div class="ticker-set"><span class="ticker-item">Classic Cirque</span><span class="ticker-sep">✦</span><span class="ticker-item">Acrobatics</span><span class="ticker-sep">✦</span><span class="ticker-item">Aerial acts</span><span class="ticker-sep">✦</span><span class="ticker-item">Physical comedy</span><span class="ticker-sep">✦</span><span class="ticker-item">Sections 202–205 · Sweet spot</span><span class="ticker-sep">✦</span></div><div class="ticker-set"><span class="ticker-item">Classic Cirque</span><span class="ticker-sep">✦</span><span class="ticker-item">Acrobatics</span><span class="ticker-sep">✦</span><span class="ticker-item">Aerial acts</span><span class="ticker-sep">✦</span><span class="ticker-item">Physical comedy</span><span class="ticker-sep">✦</span><span class="ticker-item">Sections 202–205 · Sweet spot</span><span class="ticker-sep">✦</span></div></div></div>
<nav aria-label="On this page" class="subnav"><div class="wrap"><a href="#quick">Quick take</a><a href="#photos">Photos</a><a href="#seats">Seat guide</a><a href="#fit">Is it for you?</a><a href="#showtimes">Showtimes</a><a href="#faq">FAQ</a></div></nav>
<main id="main">
<section class="section" id="quick"><div class="wrap verdict-grid"><div class="copy"><div class="eyebrow">The 30-second answer</div><h2>Is Mystère worth seeing?</h2><p class="lede lede-highlight">Yes if you want Cirque at its most Cirque: bodies flying, impossible balance, weird little characters and a show that works even when you stop trying to understand the plot.</p><p>Mystère is less about one huge technical gimmick and more about the performers. The pacing keeps changing — aerial work, acrobatics, clowning, strength acts — so the show feels bigger than its 90-minute runtime. It is also one of the easier Cirque picks for a mixed-age group because the appeal is visual and the story is not doing much homework.</p><div class="take"><span>🌵</span><div><b>Kris’s take</b><p>I’d buy sections 202–205 before I’d chase the closest row. Mystère plays across the whole room, and that part of the 200 level gives you a broad look at the stage and aerial work without losing the overall picture.</p></div></div></div><div class="decision"><div class="decision-card good"><h3>Good fit</h3><p>You want acrobatics and classic Cirque weirdness more than a big narrative or concert soundtrack.</p></div></div></div></section>
<section class="section alt" id="photos"><div class="wrap"><div class="eyebrow">See the production</div><h2>Mystère photos</h2><div class="gallery gallery-4"><button aria-label="Open Mystère photo" type="button"><img alt="Mystère by Cirque du Soleil at TI Las Vegas" loading="lazy" src="/images/mystere-hero.jpg"/></button><button aria-label="Open Mystère performers photo" type="button"><img alt="Mystère performers at TI Las Vegas" loading="lazy" src="/images/mystere-show-2.jpg"/></button><button aria-label="Open Mystère stage photo" type="button"><img alt="Mystère stage at TI Las Vegas" loading="lazy" src="/images/mystere-show-3.jpg"/></button><button class="mystere-chart-gallery" aria-label="Open Mystère Theatre seating chart" type="button"><img alt="Mystère Theatre seating chart showing sections 101 through 206, with sections 202 through 205 marked as the Vegas Sidekick sweet spot" loading="lazy" src="/images/mystere-theatre-seating-chart.svg"/></button></div><p class="media-caption">Mystère Theatre · TI Las Vegas · 3300 S Las Vegas Blvd.</p></div></section>
<section class="section" id="seats"><div class="wrap"><div class="eyebrow">Seat guide</div><h2>Find your seat at Mystère Theatre</h2><p class="lede">Sections 202–205 are the sweet spot. They wrap around the center of the 200 level and give you a broad view of both the stage and the aerial space above it.</p><div id="mystere-seat-guide" class="mystere-seat-guide" data-seat-layout="mystere-theatre" data-layout-url="/data/seat-layouts/mystere-theatre.json" data-ticket-url="{TICKET}"><noscript><p>Mystère Theatre is arranged around the stage with lower sections 101–105 and upper sections 201–206. Vegas Sidekick’s sweet spot is sections 202–205.</p></noscript></div></div></section>
<section class="section alt" id="fit"><div class="wrap"><div class="eyebrow">Is it for you?</div><h2>Who it fits best</h2><div class="fit-grid solo"><div class="fit-card good"><h3>Good fit</h3><ul><li>You want the classic Cirque mix of acrobatics, aerial work and physical comedy.</li><li>You’re bringing a mixed-age group and want a show built around visual spectacle.</li><li>You’d rather have act-after-act variety than a heavy storyline.</li></ul></div></div></div></section>
<section class="section" id="showtimes"><div class="wrap"><div class="eyebrow">Plan the night</div><h2>Showtimes</h2><p class="lede">Monday, Tuesday, Friday, Saturday and Sunday · 6:30 PM &amp; 9 PM.</p><div class="schedule"><div class="day"><a href="{TICKET}" rel="noopener sponsored" target="_blank"><strong>Mon</strong><span>6:30 &amp; 9 PM</span></a></div><div class="day"><a href="{TICKET}" rel="noopener sponsored" target="_blank"><strong>Tue</strong><span>6:30 &amp; 9 PM</span></a></div><div class="day dark"><strong>Wed</strong><span>Dark</span></div><div class="day dark"><strong>Thu</strong><span>Dark</span></div><div class="day"><a href="{TICKET}" rel="noopener sponsored" target="_blank"><strong>Fri</strong><span>6:30 &amp; 9 PM</span></a></div><div class="day"><a href="{TICKET}" rel="noopener sponsored" target="_blank"><strong>Sat</strong><span>6:30 &amp; 9 PM</span></a></div><div class="day"><a href="{TICKET}" rel="noopener sponsored" target="_blank"><strong>Sun</strong><span>6:30 &amp; 9 PM</span></a></div></div><a class="later-date-cta" href="{TICKET}" rel="noopener sponsored" target="_blank">See available dates &amp; times →</a></div></section>
<section class="section alt" id="faq"><div class="wrap"><div class="eyebrow">Before you book</div><h2>Frequently asked questions</h2><div class="faq">{faq_html}</div></div></section>
<section class="section"><div class="wrap"><div class="eyebrow">Keep comparing</div><h2>You may also like</h2><div class="related-grid"><a class="related-card" href="/shows/cirque/o/"><img alt="O by Cirque du Soleil at Bellagio" loading="lazy" src="/images/o-show-2.jpg"/><div><strong>“O”</strong><small>Aquatic Cirque · Bellagio</small></div></a><a class="related-card" href="/shows/cirque/ka/"><img alt="KÀ by Cirque du Soleil at MGM Grand" loading="lazy" src="/images/ka-hero.jpg"/><div><strong>KÀ</strong><small>Big story · moving stage</small></div></a><a class="related-card" href="/shows/cirque/michael-jackson-one/"><img alt="Michael Jackson ONE by Cirque du Soleil" loading="lazy" src="/images/mj-one-hero.jpg"/><div><strong>Michael Jackson ONE</strong><small>Concert energy · Cirque production</small></div></a></div></div></section>
<section class="section alt"><div class="wrap"><div class="eyebrow">Still deciding?</div><h2>Make the next click useful</h2><div class="next-grid"><a class="next-card" href="/shows/cirque/" style="--accent:#6d28d9"><h3>Compare all Cirque shows →</h3><p>See the resident Cirque productions side by side before choosing.</p></a><a class="next-card" href="/guides/best-shows-for-families/" style="--accent:#0fb2c7"><h3>Bringing kids? →</h3><p>Compare Mystère with the other family-friendly Vegas picks.</p></a><a class="next-card" href="/guides/best-shows-for-first-timers/" style="--accent:#f43f8c"><h3>First trip to Vegas? →</h3><p>See where Mystère fits against the other easy first-night choices.</p></a></div></div></section>
<section class="section"><div class="wrap"><a class="author-card" href="/about/kris-kidd/"><img alt="Kris Kidd" loading="lazy" src="/images/kris-kidd.webp"/><div><strong>Kris Kidd · Vegas Sidekick</strong><p>Las Vegas show and ticketing guidance. Show info confirmed September 2026.</p></div></a><p class="disclosure-line">Vegas Sidekick may earn a commission when you buy through our links. <a href="/affiliate-disclosure/">Affiliate disclosure</a>.</p></div></section>
<section class="section alt final-section"><div class="wrap"><h2>Mystère tickets</h2><p class="lede">Starting at $84. Pick your date, then compare the available seating sections.</p><a class="cta vs-ticket-primary" href="{TICKET}" rel="noopener sponsored" target="_blank">See Tickets →</a></div></section>
</main><div id="vs-footer"></div><div class="mobile-bar"><div class="mobile-progress" id="mobileProgress"></div><div class="mobile-inner"><div class="mobile-price"><small>FROM</small>$84</div><a class="cta vs-ticket-primary" href="{TICKET}" rel="noopener sponsored" target="_blank">Get Tickets →</a></div></div><div aria-label="Mystère show photo" aria-modal="true" class="lightbox" id="lightbox" role="dialog"><button aria-label="Close photo" id="lightboxClose">×</button><img alt="" id="lightboxImg"/></div><script src="/components/header.js?v=14"></script><script src="/components/footer.js?v=14"></script><script src="/assets/show-canonical.js?v=2"></script><script src="/assets/seat-layouts/mystere-theatre.js?v=1" defer></script></body>'''
text = sub_once(text, r'<body>.*?</body>', body, 'body')
PAGE.write_text(text, encoding='utf-8')

site = SITEMAP.read_text(encoding='utf-8')
site = sub_once(site, r'(<loc>https://vegassidekick\.com/shows/cirque/mystere/</loc>.*?<lastmod>)[^<]+(</lastmod>)', r'\g<1>'+DATE+r'\g<2>', 'sitemap lastmod')
SITEMAP.write_text(site, encoding='utf-8')

# Regression assertions before repository commit.
p = PAGE.read_text(encoding='utf-8')
lower = p.lower()
required = [
    'Tickets start at $84. Other price points may be available.',
    '<span>Start times</span>',
    'See available dates &amp; times →',
    'Show info confirmed September 2026',
    '/data/seat-layouts/mystere-theatre.json',
    '/assets/seat-layouts/mystere-theatre.css?v=1',
    '/assets/seat-layouts/mystere-theatre.js?v=1',
    '/images/mystere-theatre-seating-chart.svg',
    'Sections 202–205 are the sweet spot',
    'Kris’s take',
    'Mystère Theatre – TI Hotel'
]
for s in required:
    if s not in p:
        raise SystemExit(f'Missing Mystere requirement: {s}')
banned = ['tradeoff','Think twice','The downside','Honest downside','Typical start','Last updated','Spike’s take','Booking tip']
for s in banned:
    if s.lower() in lower:
        raise SystemExit(f'Stale/banned Mystere wording remains: {s}')
if p.count('<div class="ticker-set">') != 2:
    raise SystemExit('Ticker is not exactly two duplicated sets')
if p.count('Show info confirmed September 2026') != 1:
    raise SystemExit('Freshness is missing or duplicated')
layout = json.loads(LAYOUT.read_text(encoding='utf-8'))
ids = {s['id'] for s in layout['sections']}
if ids != ({str(i) for i in range(101,106)} | {str(i) for i in range(201,207)}):
    raise SystemExit(f'Unexpected Mystere sections: {sorted(ids)}')
picks = {s['id'] for s in layout['sections'] if s.get('our_pick')}
if picks != {'202','203','204','205'}:
    raise SystemExit(f'Wrong sweet-spot sections: {sorted(picks)}')
svg = SVG.read_text(encoding='utf-8')
for sid in sorted(ids):
    if f'>{sid}</text>' not in svg:
        raise SystemExit(f'Static chart missing section {sid}')
if 'OUR PICK · SECTIONS 202–205' not in svg:
    raise SystemExit('Static chart missing sweet-spot callout')
db = json.loads((ROOT/'data/show-database.json').read_text(encoding='utf-8'))
rec = next(r for r in db['records'] if r['slug']=='mystere')
if rec['status']!='active' or rec['our_price']!=84 or rec['runtime_minutes']!=90:
    raise SystemExit('Mystere operational facts drifted')
if rec['venue']!='Mystère Theatre – TI Hotel':
    raise SystemExit('Mystere venue drifted')
if rec['ticket_url']!='https://spotlight.vegas/shows/cirque-du-soleil/mystere/ref/vegassidekick':
    raise SystemExit('Mystere ticket URL drifted')
print('Mystere rebuild and regression assertions passed')

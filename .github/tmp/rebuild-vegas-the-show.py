#!/usr/bin/env python3
from pathlib import Path
import json, re, html

ROOT = Path(__file__).resolve().parents[2]
PAGE = ROOT / 'shows/music/vegas-the-show/index.html'
DATA = ROOT / 'data/seat-layouts/saxe-theater.json'
CSS = ROOT / 'assets/seat-layouts/saxe-theater.css'
JS = ROOT / 'assets/seat-layouts/saxe-theater.js'
SVG = ROOT / 'images/saxe-theater-seating-chart.svg'
SITEMAP = ROOT / 'sitemap.xml'

TICKET = 'https://spotlight.vegas/shows/production/vegas-the-show/ref/vegassidekick'
VENUE = 'Saxe Theater • Miracle Mile • Planet Hollywood'
ADDRESS = '3663 S Las Vegas Blvd, Las Vegas, NV 89109'

layout = {
  'id': 'saxe-theater',
  'venue': VENUE,
  'address': ADDRESS,
  'viewBox': '0 0 1000 860',
  'room_outline': 'M42 92 L180 18 L560 208 L575 355 Q760 345 952 468 L862 770 H252 L205 602 L78 505 L42 330 Z',
  'stage': {
    'path': 'M255 760 Q500 650 745 760 L745 805 H255 Z',
    'label_x': 500,
    'label_y': 752
  },
  'zones': [
    {
      'id': 'vip-center', 'label': 'VIP Center', 'badge': 'Sweet spot', 'our_pick': True,
      'color': '#8d3cff',
      'paths': ['M390 455 L710 485 L640 700 Q505 668 370 700 Z'],
      'labels': [{'x': 525, 'y': 575, 'lines': ['VIP', 'CENTER', 'A–L']}],
      'description': 'Our pick. VIP Center gives you the straightest look at the wide stage while keeping the full choreography and costumes easy to take in.'
    },
    {
      'id': 'vip-sides', 'label': 'VIP Sides', 'badge': 'Sweet spot', 'our_pick': True,
      'color': '#ff2e7e',
      'paths': ['M198 515 L345 455 L382 690 L275 728 Z', 'M725 490 L870 535 L826 724 L655 700 Z'],
      'labels': [
        {'x': 290, 'y': 595, 'lines': ['VIP', 'SIDE', 'A–K']},
        {'x': 785, 'y': 600, 'lines': ['VIP', 'SIDE', 'A–J']}
      ],
      'description': 'Also part of our sweet spot. The two VIP Side blocks keep you close to the stage with an angled look across the production.'
    },
    {
      'id': 'middle', 'label': 'Middle', 'badge': 'Wider view', 'our_pick': False,
      'color': '#12c7b1',
      'paths': ['M92 290 L365 164 L536 248 L530 392 L180 472 Z'],
      'labels': [{'x': 318, 'y': 320, 'lines': ['MIDDLE', 'M–S']}],
      'description': 'A farther-back section with a wider overall perspective on the stage. A solid option when you want more of the full room in one view.'
    },
    {
      'id': 'rear', 'label': 'Rear', 'badge': 'Full-room view', 'our_pick': False,
      'color': '#64748b',
      'paths': ['M70 104 L180 36 L365 136 L112 258 Z'],
      'labels': [{'x': 192, 'y': 145, 'lines': ['REAR', 'T–X']}],
      'description': 'The farthest section from the stage, with the broadest overall look at the room and the full production picture.'
    }
  ]
}
DATA.parent.mkdir(parents=True, exist_ok=True)
DATA.write_text(json.dumps(layout, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

CSS.write_text(r'''.saxe-seat-guide{--sx-pink:#ff2e7e;--sx-purple:#8d3cff;--sx-amber:#ffb000;--sx-teal:#12c7b1;display:grid;grid-template-columns:minmax(0,1.24fr) minmax(280px,.76fr);gap:22px;align-items:start;margin-top:24px}
.saxe-map-shell{position:relative;overflow:hidden;border-radius:28px;padding:22px;background:radial-gradient(circle at 55% 84%,rgba(255,176,0,.13),transparent 24%),radial-gradient(circle at 18% 12%,rgba(141,60,255,.18),transparent 30%),linear-gradient(180deg,#140923 0%,#0b0613 64%,#08070d 100%);border:1px solid rgba(255,255,255,.16);box-shadow:0 24px 60px rgba(13,4,24,.28)}
.saxe-map-shell svg{display:block;width:100%;height:auto}.saxe-room-outline{fill:none;stroke:rgba(220,216,226,.38);stroke-width:22;stroke-linejoin:round}.saxe-map-zone{cursor:pointer;outline:none}.saxe-map-zone path{fill:var(--zone-color);stroke:rgba(255,255,255,.30);stroke-width:2;transition:filter .18s ease,stroke .18s ease,stroke-width .18s ease}.saxe-map-zone[data-pick="true"] path{stroke:rgba(255,176,0,.72);stroke-width:4}.saxe-map-zone text{fill:#fff;font:800 29px Inter,Arial,sans-serif;text-anchor:middle;pointer-events:none;text-shadow:0 2px 4px rgba(0,0,0,.6)}.saxe-map-zone text.sub{font-size:18px;font-weight:700;fill:rgba(255,255,255,.82)}.saxe-map-zone:hover path,.saxe-map-zone:focus path{filter:brightness(1.1);stroke:#fff;stroke-width:5}.saxe-map-zone.is-active path{stroke:var(--sx-amber);stroke-width:7;filter:drop-shadow(0 0 11px rgba(255,176,0,.82))}
.saxe-stage{fill:#101017;stroke:rgba(255,176,0,.82);stroke-width:3}.saxe-stage-label{fill:#fff;font:800 31px Inter,Arial,sans-serif;text-anchor:middle;letter-spacing:.18em}.saxe-map-caption{text-align:center;margin:12px 0 2px}.saxe-map-caption strong{display:block;color:#fff;font-size:clamp(1.08rem,2vw,1.35rem)}.saxe-map-caption span{display:block;color:rgba(255,255,255,.72);font-size:.88rem;margin-top:5px}
.saxe-seat-detail{padding:20px;border-radius:20px;background:#fff;border:1px solid #e8e2ed;color:#21182a;box-shadow:0 12px 30px rgba(17,4,28,.08)}.saxe-seat-detail .tag{display:inline-block;font-size:.68rem;letter-spacing:.1em;text-transform:uppercase;font-weight:900;color:#171225;background:var(--sx-amber);padding:5px 8px;border-radius:999px}.saxe-seat-detail h3{margin:9px 0 8px;font-size:1.5rem}.saxe-seat-detail p{margin:0 0 16px;color:#5e5366;line-height:1.55}.saxe-seat-detail .cta{width:100%;text-align:center;justify-content:center}.saxe-legend{display:grid;gap:9px;margin-top:12px}.saxe-legend span{display:flex;align-items:center;gap:9px;font-size:.82rem;color:#6e6475}.saxe-legend i{width:14px;height:14px;border-radius:4px;background:var(--legend-color);box-shadow:0 0 12px color-mix(in srgb,var(--legend-color) 42%,transparent)}
.saxe-chart-gallery{position:relative}.saxe-chart-gallery:after{content:"Seating chart";position:absolute;left:12px;bottom:12px;padding:6px 9px;border-radius:999px;background:rgba(13,7,20,.82);color:#fff;font-size:.72rem;font-weight:800;letter-spacing:.04em;text-transform:uppercase;pointer-events:none}.saxe-chart-gallery img{object-fit:contain!important;background:#09060f}
#photos .gallery.gallery-4{grid-template-columns:repeat(2,minmax(0,1fr));grid-template-rows:repeat(2,minmax(0,1fr));height:560px}#photos .gallery.gallery-4 button:first-child{grid-row:auto}#photos .gallery.gallery-4 button{min-width:0;min-height:0}#photos .gallery.gallery-4 img{width:100%;height:100%;object-fit:cover}
.saxe-mobile-popover{display:none}.saxe-lb-nav{position:absolute!important;top:50%!important;transform:translateY(-50%);z-index:3;width:52px!important;height:52px!important;border-radius:50%!important;background:rgba(255,255,255,.94)!important;color:#17082e!important;font-size:2rem!important;line-height:1!important}.saxe-lb-prev{left:18px!important;right:auto!important}.saxe-lb-next{right:18px!important}.saxe-lb-count{position:absolute;left:50%;bottom:18px;transform:translateX(-50%);z-index:3;background:rgba(23,8,46,.82);color:#fff;padding:6px 11px;border-radius:999px;font-size:.8rem;font-weight:800;letter-spacing:.04em}
@media(max-width:820px){.saxe-seat-guide{grid-template-columns:1fr}.saxe-map-shell{padding:10px}.saxe-seat-detail,.saxe-legend{display:none}.saxe-map-zone text{font-size:25px}.saxe-map-zone text.sub{font-size:16px}.saxe-mobile-popover{position:fixed;z-index:1100;left:14px;right:14px;bottom:98px;display:flex;align-items:flex-start;gap:12px;padding:14px 48px 14px 15px;border:1px solid rgba(255,176,0,.65);border-radius:16px;background:rgba(20,9,35,.96);box-shadow:0 14px 38px rgba(0,0,0,.38);color:#fff;opacity:0;pointer-events:none;transform:translateY(16px);transition:.2s}.saxe-mobile-popover.is-open{opacity:1;pointer-events:auto;transform:translateY(0)}.saxe-mobile-popover strong{display:block;font-size:1rem;margin:2px 0 4px}.saxe-mobile-popover p{margin:0;color:#ddd4e4;font-size:.82rem;line-height:1.45}.saxe-mobile-badge{display:inline-block;font-size:.62rem;font-weight:900;letter-spacing:.08em;text-transform:uppercase;color:#17082e;background:#ffb000;padding:4px 7px;border-radius:999px}.saxe-mobile-popover>button{position:absolute;right:9px;top:8px;width:30px;height:30px;border:0;border-radius:50%;background:rgba(255,255,255,.1);color:#fff;font-size:1.25rem}#photos .gallery.gallery-4{height:auto;grid-template-columns:1fr;grid-template-rows:auto}#photos .gallery.gallery-4 img{aspect-ratio:4/3}.saxe-chart-gallery img{object-fit:contain!important;aspect-ratio:4/3}.saxe-lb-nav{width:46px!important;height:46px!important}.saxe-lb-prev{left:8px!important}.saxe-lb-next{right:8px!important}.saxe-lb-count{bottom:100px}}
''', encoding='utf-8')

JS.write_text(r'''(()=>{
  const esc=s=>String(s??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
  const textLines=(labels)=>labels.map(l=>{const spans=l.lines.map((line,i)=>`<tspan x="${esc(l.x)}" dy="${i?25:0}" class="${i===l.lines.length-1&&line.includes('–')?'sub':''}">${esc(line)}</tspan>`).join('');return `<text x="${esc(l.x)}" y="${esc(l.y)}">${spans}</text>`}).join('');
  async function mount(root){
    const url=root.dataset.layoutUrl,ticket=root.dataset.ticketUrl;
    try{
      const data=await fetch(url,{credentials:'same-origin'}).then(r=>{if(!r.ok)throw new Error(`HTTP ${r.status}`);return r.json()});
      const byId=Object.fromEntries(data.zones.map(z=>[z.id,z]));
      const zone=z=>`<g class="saxe-map-zone" data-zone="${esc(z.id)}" data-pick="${z.our_pick?'true':'false'}" role="button" tabindex="0" aria-label="${esc(z.label)}${z.badge?`, ${esc(z.badge)}`:''}" style="--zone-color:${esc(z.color)}">${z.paths.map(p=>`<path d="${esc(p)}"></path>`).join('')}${textLines(z.labels||[])}</g>`;
      root.innerHTML=`<div><div class="saxe-map-shell"><svg viewBox="${esc(data.viewBox)}" role="img" aria-label="Saxe Theater seating layout"><path class="saxe-room-outline" d="${esc(data.room_outline)}"></path>${data.zones.map(zone).join('')}<path class="saxe-stage" d="${esc(data.stage.path)}"></path><text class="saxe-stage-label" x="${esc(data.stage.label_x)}" y="${esc(data.stage.label_y)}">STAGE</text></svg><div class="saxe-map-caption"><strong>${esc(data.venue)}</strong><span>${esc(data.address)}</span></div></div></div><div><div class="saxe-seat-detail" aria-live="polite"><span class="tag">Sweet spot</span><h3>VIP Center</h3><p>${esc(byId['vip-center'].description)}</p><a class="cta vs-ticket-primary" href="${esc(ticket)}" target="_blank" rel="noopener sponsored">Check seats →</a></div><div class="saxe-legend"><span><i style="--legend-color:#8d3cff"></i>VIP Center · Sweet Spot / Our Pick</span><span><i style="--legend-color:#ff2e7e"></i>VIP Sides · Sweet Spot / Our Pick</span><span><i style="--legend-color:#12c7b1"></i>Middle · wider view</span><span><i style="--legend-color:#64748b"></i>Rear · full-room view</span></div></div><div class="saxe-mobile-popover" aria-live="polite" aria-atomic="true"><div><span class="saxe-mobile-badge">Sweet spot</span><strong>VIP Center</strong><p>${esc(byId['vip-center'].description)}</p></div><button type="button" aria-label="Close seat description">×</button></div>`;
      const detail=root.querySelector('.saxe-seat-detail'),pop=root.querySelector('.saxe-mobile-popover');
      const badge=z=>z.badge||(z.our_pick?'Sweet spot':'Seat guide');
      const activate=(id,showPop=false)=>{
        const z=byId[id];if(!z)return;
        root.querySelectorAll('[data-zone]').forEach(el=>el.classList.toggle('is-active',el.dataset.zone===id));
        detail.querySelector('.tag').textContent=badge(z);detail.querySelector('h3').textContent=z.label;detail.querySelector('p').textContent=z.description;
        pop.querySelector('.saxe-mobile-badge').textContent=badge(z);pop.querySelector('strong').textContent=z.label;pop.querySelector('p').textContent=z.description;
        if(showPop&&matchMedia('(max-width:820px)').matches)pop.classList.add('is-open');
      };
      root.addEventListener('click',e=>{const z=e.target.closest('[data-zone]');if(z)activate(z.dataset.zone,true);if(e.target.closest('.saxe-mobile-popover>button'))pop.classList.remove('is-open')});
      root.addEventListener('keydown',e=>{const z=e.target.closest('[data-zone]');if(z&&(e.key==='Enter'||e.key===' ')){e.preventDefault();activate(z.dataset.zone,true)}});
      addEventListener('scroll',()=>pop.classList.remove('is-open'),{passive:true});activate('vip-center');
    }catch(err){root.innerHTML='<p>Seat guide unavailable right now. Use the live ticket map to compare sections for your date.</p>';console.warn('Saxe Theater seat guide:',err)}
  }
  function enhanceGallery(){
    const buttons=[...document.querySelectorAll('#photos .gallery button')],light=document.getElementById('lightbox');if(!buttons.length||!light)return;const img=light.querySelector('#lightboxImg, img');if(!img)return;
    let current=0,touchX=null,prev=light.querySelector('.saxe-lb-prev'),next=light.querySelector('.saxe-lb-next'),count=light.querySelector('.saxe-lb-count');
    if(!prev){prev=document.createElement('button');prev.type='button';prev.className='saxe-lb-nav saxe-lb-prev';prev.setAttribute('aria-label','Previous photo');prev.textContent='‹';light.appendChild(prev);next=document.createElement('button');next.type='button';next.className='saxe-lb-nav saxe-lb-next';next.setAttribute('aria-label','Next photo');next.textContent='›';light.appendChild(next);count=document.createElement('div');count.className='saxe-lb-count';light.appendChild(count)}
    const show=i=>{current=(i+buttons.length)%buttons.length;const thumb=buttons[current].querySelector('img');img.src=thumb.currentSrc||thumb.src;img.alt=thumb.alt||'VEGAS! The Show photo';count.textContent=`${current+1} of ${buttons.length}`};
    buttons.forEach((b,i)=>b.addEventListener('click',()=>show(i)));prev.addEventListener('click',e=>{e.stopPropagation();show(current-1)});next.addEventListener('click',e=>{e.stopPropagation();show(current+1)});
    addEventListener('keydown',e=>{if(!light.classList.contains('open'))return;if(e.key==='ArrowLeft')show(current-1);if(e.key==='ArrowRight')show(current+1)});
    light.addEventListener('touchstart',e=>{touchX=e.changedTouches[0]?.clientX??null},{passive:true});light.addEventListener('touchend',e=>{if(touchX==null)return;const dx=(e.changedTouches[0]?.clientX??touchX)-touchX;touchX=null;if(Math.abs(dx)>45)show(current+(dx<0?1:-1))},{passive:true});
  }
  document.querySelectorAll('[data-seat-layout="saxe-theater"]').forEach(mount);enhanceGallery();
})();
''', encoding='utf-8')

# Static SVG generated from the exact same layout data.
def label_svg(label):
    x, y, lines = label['x'], label['y'], label['lines']
    chunks=[]
    for i,line in enumerate(lines):
        cls=' font-size="18" opacity=".82"' if i==len(lines)-1 and '–' in line else ''
        chunks.append(f'<tspan x="{x}" dy="{25 if i else 0}"{cls}>{html.escape(line)}</tspan>')
    return f'<text x="{x}" y="{y}" text-anchor="middle" fill="#fff" font-family="Arial,sans-serif" font-size="29" font-weight="800">{"".join(chunks)}</text>'

parts=[
'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="1400" viewBox="0 0 1000 1160">',
'<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#140923"/><stop offset="1" stop-color="#07070c"/></linearGradient><filter id="glow"><feGaussianBlur stdDeviation="7" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>',
'<rect width="1000" height="1160" rx="36" fill="url(#bg)"/>',
'<text x="55" y="64" fill="#fff" font-family="Arial,sans-serif" font-size="34" font-weight="800">vegas <tspan fill="#ff2e7e">sidekick</tspan></text>',
'<text x="57" y="95" fill="#d9d1df" font-family="Arial,sans-serif" font-size="14" letter-spacing="4">SHOWS • TICKETS • GOOD TIMES</text>',
f'<path d="{layout["room_outline"]}" transform="translate(0 115)" fill="none" stroke="#d9d5de" stroke-opacity=".35" stroke-width="22" stroke-linejoin="round"/>'
]
for z in layout['zones']:
    stroke='#ffb000' if z.get('our_pick') else 'rgba(255,255,255,.28)'
    sw='5' if z.get('our_pick') else '2'
    for p in z['paths']:
        parts.append(f'<path d="{p}" transform="translate(0 115)" fill="{z["color"]}" stroke="{stroke}" stroke-width="{sw}"/>' )
    for lab in z['labels']:
        moved=dict(lab);moved['y']=lab['y']+115;parts.append(label_svg(moved))
parts += [
 f'<path d="{layout["stage"]["path"]}" transform="translate(0 115)" fill="#101017" stroke="#ffb000" stroke-opacity=".8" stroke-width="3"/>',
 f'<text x="{layout["stage"]["label_x"]}" y="{layout["stage"]["label_y"]+115}" text-anchor="middle" fill="#fff" font-family="Arial,sans-serif" font-size="31" font-weight="800" letter-spacing="8">STAGE</text>',
 '<rect x="275" y="1010" width="450" height="48" rx="24" fill="#ffb000"/>',
 '<text x="500" y="1041" text-anchor="middle" fill="#171225" font-family="Arial,sans-serif" font-size="18" font-weight="900" letter-spacing="2">OUR PICK · VIP CENTER + VIP SIDES</text>',
 f'<text x="500" y="1100" text-anchor="middle" fill="#fff" font-family="Arial,sans-serif" font-size="27" font-weight="800">{html.escape(VENUE)}</text>',
 f'<text x="500" y="1132" text-anchor="middle" fill="#d7cedd" font-family="Arial,sans-serif" font-size="17">{html.escape(ADDRESS)}</text>',
 '</svg>'
]
SVG.write_text('\n'.join(parts), encoding='utf-8')

faqs = [
 ('How much are VEGAS! The Show tickets?', 'Tickets currently start at $63. Other price points may be available depending on the performance and seating section.'),
 ('How long is VEGAS! The Show?', 'About 75 minutes with no intermission.'),
 ('Where is the Saxe Theater entrance?', 'Saxe Theater is inside Miracle Mile Shops at Planet Hollywood. Plan extra time to navigate the mall rather than treating the hotel lobby as the theater entrance.'),
 ('Is VEGAS! The Show good for kids?', 'The show is listed for all ages. It is built around music, costumes, dance and visual spectacle. For very young kids, the 75-minute no-intermission runtime is the practical thing to consider.'),
 ('What’s the difference between the seating sections?', 'VIP Center and VIP Sides are the Vegas Sidekick sweet spot. Middle and Rear sit farther back and give you a wider overall look at the production.'),
 ('When should I arrive?', 'I’d aim to be at Planet Hollywood about 45 minutes before showtime. That gives you time to find Saxe Theater inside Miracle Mile Shops and get settled without turning the mall into a scavenger hunt.')
]
faq_schema={'@context':'https://schema.org','@type':'FAQPage','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in faqs]}
event_schema={
 '@context':'https://schema.org','@type':'EventSeries','name':'VEGAS! The Show',
 'description':'A 75-minute classic Las Vegas production at Saxe Theater with showgirls, dancers, live music and old-school Strip spectacle.',
 'image':['https://vegassidekick.com/images/vegas-the-show-hero.webp','https://vegassidekick.com/images/vegas-the-show-2.webp','https://vegassidekick.com/images/vegas-the-show-3.webp'],
 'url':'https://vegassidekick.com/shows/music/vegas-the-show/','eventStatus':'https://schema.org/EventScheduled','eventAttendanceMode':'https://schema.org/OfflineEventAttendanceMode',
 'organizer':{'@type':'Organization','name':'VEGAS! The Show','url':'https://vegassidekick.com/shows/music/vegas-the-show/'},
 'location':{'@type':'Place','name':VENUE,'address':{'@type':'PostalAddress','streetAddress':'3663 S Las Vegas Blvd','addressLocality':'Las Vegas','addressRegion':'NV','postalCode':'89109','addressCountry':'US'}},
 'performer':{'@type':'PerformingGroup','name':'VEGAS! The Show'},
 'offers':{'@type':'Offer','price':63,'priceCurrency':'USD','availability':'https://schema.org/InStock','url':TICKET,'validFrom':'2026-01-01'},
 'duration':'PT75M','audience':{'@type':'Audience','audienceType':'No age restrictions.'}
}
breadcrumb={'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Home','item':'https://vegassidekick.com/'},{'@type':'ListItem','position':2,'name':'Music & Variety Shows','item':'https://vegassidekick.com/shows/music/'},{'@type':'ListItem','position':3,'name':'VEGAS! The Show','item':'https://vegassidekick.com/shows/music/vegas-the-show/'}]}
webpage={'@context':'https://schema.org','@type':'WebPage','url':'https://vegassidekick.com/shows/music/vegas-the-show/','dateModified':'2026-09-09','lastReviewed':'2026-09-09','author':{'@type':'Person','@id':'https://vegassidekick.com/about/kris-kidd/#kris','name':'Kris Kidd','url':'https://vegassidekick.com/about/kris-kidd/','image':'https://vegassidekick.com/images/kris-kidd.webp'}}
faq_html=''.join(f'<details><summary>{html.escape(q)}</summary><div>{html.escape(a)}</div></details>' for q,a in faqs)

page=f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/><meta content="width=device-width,initial-scale=1" name="viewport"/><link href="/favicon.png" rel="icon" type="image/png"/>
<title>VEGAS! The Show Las Vegas Tickets from $63 | Seat Guide</title><meta content="index,follow,max-image-preview:large" name="robots"/><meta content="VEGAS! The Show is a 75-minute classic Las Vegas production at Saxe Theater. Tickets from $63. Compare showtimes and seating sections." name="description"/><link href="https://vegassidekick.com/shows/music/vegas-the-show/" rel="canonical"/>
<meta content="Vegas Sidekick" property="og:site_name"/><meta content="VEGAS! The Show Tickets &amp; Show Guide | Vegas Sidekick" property="og:title"/><meta content="From $63 for 75 minutes of showgirls, live music and old-school Las Vegas spectacle at Saxe Theater." property="og:description"/><meta content="https://vegassidekick.com/images/vegas-the-show-hero.webp" property="og:image"/><meta content="VEGAS! The Show at Saxe Theater Las Vegas" property="og:image:alt"/><meta content="https://vegassidekick.com/shows/music/vegas-the-show/" property="og:url"/><meta content="website" property="og:type"/><meta content="summary_large_image" name="twitter:card"/><meta content="https://vegassidekick.com/images/vegas-the-show-hero.webp" name="twitter:image"/>
<link href="https://fonts.googleapis.com" rel="preconnect"/><link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/><link as="image" fetchpriority="high" href="/images/vegas-the-show-hero.webp" rel="preload" type="image/webp"/><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&amp;family=Plus+Jakarta+Sans:wght@600;700;800&amp;family=IBM+Plex+Mono:wght@500;600&amp;display=swap" rel="stylesheet"/>
<script type="application/ld+json">{json.dumps(event_schema,ensure_ascii=False,separators=(',',':'))}</script><script type="application/ld+json">{json.dumps(faq_schema,ensure_ascii=False,separators=(',',':'))}</script><script type="application/ld+json">{json.dumps(breadcrumb,ensure_ascii=False,separators=(',',':'))}</script><script type="application/ld+json">{json.dumps(webpage,ensure_ascii=False,separators=(',',':'))}</script>
<link href="/assets/show-canonical.css?v=2" rel="stylesheet"/><link href="/assets/ticket-cta.css" rel="stylesheet"/><link href="/assets/show-savings.css" rel="stylesheet"/><link href="/assets/seat-layouts/saxe-theater.css?v=1" rel="stylesheet"/>
<style id="vegas-show-benchmark-final">@media (min-width:801px){{.hero-grid{{grid-template-columns:minmax(0,1.02fr) minmax(0,.98fr);overflow:visible}}.hero-copy{{position:relative;z-index:2;padding-right:72px}}.hero-media{{position:relative;z-index:1;margin-left:-112px;overflow:hidden}}.hero-media img{{object-position:center center}}.hero-media:after{{background:linear-gradient(90deg,#2c0b4e 0%,rgba(44,11,78,.94) 12%,rgba(44,11,78,.58) 28%,rgba(44,11,78,.16) 46%,transparent 62%)}}#quick .verdict-grid{{grid-template-columns:1fr;max-width:920px}}#quick .decision{{max-width:760px;margin-top:18px}}#quick .decision-card.good{{display:flex;align-items:center;gap:16px;padding:14px 18px;border-top:0;border-left:6px solid var(--gold);min-height:0}}#quick .decision-card.good h3{{margin:0;white-space:nowrap}}#quick .decision-card.good p{{margin:0}}}}</style></head>
<body data-canonical-layout="2"><div class="progress"></div><a class="skip" href="#main">Skip to content</a><div id="vs-header"></div>
<header class="hero"><div class="hero-grid"><div class="hero-copy"><div class="crumbs"><a href="/">Home</a><span>›</span><a href="/shows/music/">Music &amp; Variety</a><span>›</span>VEGAS! The Show</div><div class="eyebrow">Classic Las Vegas · {VENUE}</div><h1>VEGAS! <span>The Show</span></h1><p class="hero-dek">Showgirls, dancers, live music and the old-school showroom version of Las Vegas in a tight 75-minute production at Saxe Theater.</p><div class="chips"><span class="chip">75 minutes</span><span class="chip">All ages</span><span class="chip">{VENUE}</span></div><div class="buybox"><div><div class="price"><small>Tickets from</small>$63</div><div class="vs-deal-line"><span class="vs-regular-price">Regular $101</span><span class="vs-save-badge">Save $38</span></div></div><a class="cta vs-ticket-primary" href="{TICKET}" rel="noopener sponsored" target="_blank">Get Tickets →</a></div><div class="updated">Tickets start at $63. Other price points may be available.</div></div><div class="hero-media" data-mobile-fit="safe" style="--mobile-hero-image:url('/images/vegas-the-show-hero.webp');--mobile-hero-position:center center"><img alt="VEGAS! The Show performer in a classic feathered showgirl costume at Saxe Theater" fetchpriority="high" src="/images/vegas-the-show-hero.webp"/></div></div></header>
<section class="facts"><div class="wrap facts-grid"><div class="fact"><strong>75 min</strong><span>Runtime</span></div><div class="fact"><strong>$63</strong><span>Tickets from</span></div><div class="fact"><strong>7 PM</strong><span>Start time</span></div><div class="fact"><strong>All ages</strong><span>Age guidance</span></div></div></section>
<div class="ticker"><div class="ticker-track"><div class="ticker-set"><span class="ticker-item">Classic showgirls</span><span class="ticker-sep">✦</span><span class="ticker-item">Live Vegas energy</span><span class="ticker-sep">✦</span><span class="ticker-item">75 minutes</span><span class="ticker-sep">✦</span><span class="ticker-item">All ages</span><span class="ticker-sep">✦</span><span class="ticker-item">VIP Center + VIP Sides · Sweet spot</span><span class="ticker-sep">✦</span></div><div class="ticker-set"><span class="ticker-item">Classic showgirls</span><span class="ticker-sep">✦</span><span class="ticker-item">Live Vegas energy</span><span class="ticker-sep">✦</span><span class="ticker-item">75 minutes</span><span class="ticker-sep">✦</span><span class="ticker-item">All ages</span><span class="ticker-sep">✦</span><span class="ticker-item">VIP Center + VIP Sides · Sweet spot</span><span class="ticker-sep">✦</span></div></div></div>
<nav aria-label="On this page" class="subnav"><div class="wrap"><a href="#quick">Quick take</a><a href="#photos">Photos</a><a href="#seats">Seat guide</a><a href="#fit">Is it for you?</a><a href="#showtimes">Showtimes</a><a href="#faq">FAQ</a></div></nav><main id="main">
<section class="section" id="quick"><div class="wrap verdict-grid"><div class="copy"><div class="eyebrow">The 30-second answer</div><h2>Is VEGAS! The Show worth seeing?</h2><p class="lede lede-highlight">Yes if “Vegas show” means feathers, dancers, live-stage energy and a little old-school Strip glamour in your head.</p><p>VEGAS! The Show leans into the city’s showroom tradition instead of trying to modernize it out of existence. The appeal is the visual scale: costumes, choreography, music and a cast moving across a wide stage. It is easy to follow, runs a tight 75 minutes and works especially well for first-time visitors who want something that actually feels tied to Las Vegas.</p><div class="take"><span>🌵</span><div><b>Kris’s take</b><p>VIP Center and VIP Sides are the sweet spot here. This is a wide, choreography-heavy show, so I care more about seeing the whole stage than chasing the closest possible row.</p></div></div></div><div class="decision"><div class="decision-card good"><h3>Good fit</h3><p>You want a classic Las Vegas production with dancers, costumes and live-stage energy.</p></div></div></div></section>
<section class="section alt" id="photos"><div class="wrap"><div class="eyebrow">See the production</div><h2>VEGAS! The Show photos</h2><div class="gallery gallery-4"><button aria-label="Open VEGAS! The Show showgirl photo" type="button"><img alt="VEGAS! The Show performer in a white feather costume" loading="lazy" src="/images/vegas-the-show-hero.webp"/></button><button aria-label="Open VEGAS! The Show cast photo" type="button"><img alt="VEGAS! The Show performers with feather fans" loading="lazy" src="/images/vegas-the-show-2.webp"/></button><button aria-label="Open VEGAS! The Show finale photo" type="button"><img alt="VEGAS! The Show cast on stage during the finale" loading="lazy" src="/images/vegas-the-show-3.webp"/></button><button class="saxe-chart-gallery" aria-label="Open Saxe Theater seating chart" type="button"><img alt="Saxe Theater seating chart for VEGAS! The Show, showing VIP Center, two VIP Side sections, Middle and Rear, with VIP Center and VIP Sides marked as the Vegas Sidekick sweet spot" loading="lazy" src="/images/saxe-theater-seating-chart.svg"/></button></div><p class="media-caption">{VENUE} · 3663 S Las Vegas Blvd.</p></div></section>
<section class="section" id="seats"><div class="wrap"><div class="eyebrow">Seat guide</div><h2>Find your seat at Saxe Theater</h2><p class="lede">The room fans away from a curved stage: VIP Center in the middle, VIP Side blocks on both sides, then Middle and Rear sections farther back. VIP Center and VIP Sides are the Sweet Spot / Our Pick.</p><div id="saxe-seat-guide" class="saxe-seat-guide" data-seat-layout="saxe-theater" data-layout-url="/data/seat-layouts/saxe-theater.json" data-ticket-url="{TICKET}"><noscript><p>Saxe Theater has VIP Center, VIP Side, Middle and Rear seating sections. Vegas Sidekick’s sweet spot is VIP Center and VIP Sides.</p></noscript></div></div></section>
<section class="section alt" id="fit"><div class="wrap"><div class="eyebrow">Is it for you?</div><h2>Who it fits best</h2><div class="fit-grid solo"><div class="fit-card good"><h3>Good fit</h3><ul><li>You want a classic Las Vegas production with dancers, costumes and live-stage energy.</li><li>You’re visiting Vegas for the first time and want something that feels tied to the city.</li><li>You like a tighter 75-minute show that leaves room for dinner, drinks or another stop afterward.</li></ul></div></div></div></section>
<section class="section" id="showtimes"><div class="wrap"><div class="eyebrow">Plan the night</div><h2>Showtimes</h2><p class="lede">Monday through Saturday · 7 PM.</p><div class="schedule"><div class="day"><a href="{TICKET}" rel="noopener sponsored" target="_blank"><strong>Mon</strong><span>7 PM</span></a></div><div class="day"><a href="{TICKET}" rel="noopener sponsored" target="_blank"><strong>Tue</strong><span>7 PM</span></a></div><div class="day"><a href="{TICKET}" rel="noopener sponsored" target="_blank"><strong>Wed</strong><span>7 PM</span></a></div><div class="day"><a href="{TICKET}" rel="noopener sponsored" target="_blank"><strong>Thu</strong><span>7 PM</span></a></div><div class="day"><a href="{TICKET}" rel="noopener sponsored" target="_blank"><strong>Fri</strong><span>7 PM</span></a></div><div class="day"><a href="{TICKET}" rel="noopener sponsored" target="_blank"><strong>Sat</strong><span>7 PM</span></a></div><div class="day dark"><strong>Sun</strong><span>Dark</span></div></div><p><strong>September 21, 2026:</strong> current ticket inventory lists a 5:30 PM performance.</p><p><b>Venue:</b> {VENUE} · 3663 S Las Vegas Blvd. The theater is inside the mall, so give yourself extra navigation time on your first visit.</p><a class="later-date-cta vs-ticket-primary" href="{TICKET}" rel="noopener sponsored" target="_blank">See available dates &amp; times →</a></div></section>
<section class="section alt" id="faq"><div class="wrap"><div class="eyebrow">Before you book</div><h2>Frequently asked questions</h2><div class="faq">{faq_html}</div></div></section>
<section class="section"><div class="wrap"><div class="eyebrow">Keep comparing</div><h2>You may also like</h2><div class="related-grid"><a class="related-card" href="/shows/music/all-shook-up/"><img alt="All Shook Up Las Vegas show" loading="lazy" src="/images/all-shook-up-hero.jpg"/><div><strong>All Shook Up</strong><small>Elvis tribute · music</small></div></a><a class="related-card" href="/shows/music/rat-pack-is-back/"><img alt="The Rat Pack Is Back Las Vegas show" loading="lazy" src="/images/rat-pack-is-back-hero.webp"/><div><strong>The Rat Pack Is Back</strong><small>Old-school Vegas · tribute</small></div></a><a class="related-card" href="/shows/music/mj-live/"><img alt="MJ Live Las Vegas show" loading="lazy" src="/images/mj-live-hero.webp"/><div><strong>MJ Live</strong><small>Michael Jackson tribute · music</small></div></a></div></div></section>
<section class="section alt"><div class="wrap"><div class="eyebrow">Still deciding?</div><h2>Make the next click useful</h2><div class="next-grid"><a class="next-card" href="/shows/music/" style="--accent:#6d28d9"><h3>Compare music &amp; variety shows →</h3><p>Want more concert energy or a different kind of stage production? Compare the other music and variety options.</p></a><a class="next-card" href="/venues/planet-hollywood/" style="--accent:#f43f8c"><h3>Explore Planet Hollywood shows →</h3><p>See what else is playing at Planet Hollywood and Miracle Mile Shops before adding another rideshare.</p></a><a class="next-card" href="/guides/best-shows-for-first-timers/" style="--accent:#0fb2c7"><h3>First trip to Vegas? →</h3><p>Compare our first-timer picks if you want the show that gives you the clearest “we’re in Vegas” moment.</p></a></div></div></section>
<section class="section"><div class="wrap"><a class="author-card" href="/about/kris-kidd/"><img alt="Kris Kidd" loading="lazy" src="/images/kris-kidd.webp"/><div><strong>Kris Kidd · Vegas Sidekick</strong><p>Las Vegas show and ticketing guidance. Show info confirmed September 2026.</p></div></a><p class="disclosure-line">Vegas Sidekick may earn a commission when you buy through our links. <a href="/affiliate-disclosure/">Affiliate disclosure</a>.</p></div></section>
<section class="section alt final-section"><div class="wrap"><h2>VEGAS! The Show tickets</h2><p class="lede">Tickets start at $63. Other price points may be available.</p><a class="cta vs-ticket-primary" href="{TICKET}" rel="noopener sponsored" target="_blank">See Tickets →</a></div></section></main>
<div id="vs-footer"></div><div class="mobile-bar"><div class="mobile-progress" id="mobileProgress"></div><div class="mobile-inner"><div class="mobile-price"><small>FROM</small>$63</div><a class="cta vs-ticket-primary" href="{TICKET}" rel="noopener sponsored" target="_blank">Get Tickets →</a></div></div><div aria-label="Show photo" aria-modal="true" class="lightbox" id="lightbox" role="dialog"><button aria-label="Close photo" id="lightboxClose">×</button><img alt="" id="lightboxImg"/></div>
<script src="/components/header.js?v=14"></script><script src="/components/footer.js?v=14"></script><script src="/assets/show-canonical.js?v=2"></script><script src="/assets/seat-layouts/saxe-theater.js?v=1" defer></script></body></html>'''
PAGE.write_text(page, encoding='utf-8')

# Update sitemap freshness for the rebuilt page.
s = SITEMAP.read_text(encoding='utf-8')
pat = r'(<loc>https://vegassidekick\.com/shows/music/vegas-the-show/</loc>\s*<lastmod>)[^<]+(</lastmod>)'
s2,n = re.subn(pat, r'\g<1>2026-09-09\g<2>', s, count=1)
if n:
    SITEMAP.write_text(s2, encoding='utf-8')

# Regression checks specific to this rebuild.
t = PAGE.read_text(encoding='utf-8')
assert VENUE in t
assert 'data-seat-layout="saxe-theater"' in t
assert '/images/saxe-theater-seating-chart.svg' in t
assert 'VIP Center and VIP Sides are the Sweet Spot / Our Pick.' in t
assert 'Typical start' not in t
assert 'tradeoff' not in t.lower()
assert 'Think Twice' not in t
assert 'Last updated' not in t
assert t.count('Show info confirmed September 2026') == 1
assert TICKET in t
assert '"price":63' in t
assert 'eventSchedule' not in t
assert 'September 21, 2026:' in t
assert 'Regular $101' in t and 'Save $38' in t
assert 'saxe-theater.js' in t
print('VEGAS! The Show rebuild and regression assertions passed')

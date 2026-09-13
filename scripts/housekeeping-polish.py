from pathlib import Path

CSS = r'''/* Vegas Sidekick shared UI polish — September 2026 */
:where(a,button,summary,input,select,textarea,[tabindex]):focus-visible{outline:3px solid #c6f22e;outline-offset:3px;border-radius:6px}
:where(button,.cta,.vs-ticket-primary,.nav-cta,.gallery button,.related a,.decision-card[href],.vs-day,.vs-time-grid a,.vs-primary-book,.vs-secondary-book){-webkit-tap-highlight-color:transparent}
:where(button,.cta,.vs-ticket-primary,.nav-cta,.gallery button,.related a,.decision-card[href],.vs-day,.vs-time-grid a,.vs-primary-book,.vs-secondary-book):active{transform:translateY(1px) scale(.985)}
.subnav a{position:relative;border-radius:8px;padding-left:8px;padding-right:8px;transition:color .18s ease,background .18s ease,box-shadow .18s ease}
.subnav a.is-active{color:#5b21b6;background:#f5f0ff;box-shadow:inset 0 -2px 0 #7c3aed}
main section[id],.section[id]{scroll-margin-top:122px}
.vs-polish-pulse{animation:vsPolishPulse .4s ease-out}
@keyframes vsPolishPulse{0%{filter:brightness(1);box-shadow:0 0 0 0 rgba(255,176,0,.35)}45%{filter:brightness(1.12);box-shadow:0 0 0 6px rgba(255,176,0,.16)}100%{filter:brightness(1);box-shadow:0 0 0 0 rgba(255,176,0,0)}}
@media(max-width:800px){body{padding-bottom:calc(86px + env(safe-area-inset-bottom))}.mobile-bar{padding-bottom:calc(14px + env(safe-area-inset-bottom))}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}.vs-polish-pulse{animation:none!important}:where(button,.cta,.vs-ticket-primary,.nav-cta,.gallery button,.related a,.decision-card[href],.vs-day,.vs-time-grid a,.vs-primary-book,.vs-secondary-book){transition:none!important}}
'''

JS = r'''/* Vegas Sidekick shared UI polish — active section nav + selection feedback. */
(()=>{'use strict';
 const subnav=document.querySelector('.subnav');
 if(subnav){
  const links=[...subnav.querySelectorAll('a[href^="#"]')];
  const pairs=links.map(link=>{const id=link.getAttribute('href').slice(1);return {link,section:document.getElementById(id)}}).filter(x=>x.section);
  const setActive=link=>links.forEach(item=>{const on=item===link;item.classList.toggle('is-active',on);if(on)item.setAttribute('aria-current','location');else item.removeAttribute('aria-current')});
  if(pairs.length){
   const observer=new IntersectionObserver(entries=>{
    const visible=entries.filter(e=>e.isIntersecting).sort((a,b)=>a.boundingClientRect.top-b.boundingClientRect.top);
    if(visible[0]){const pair=pairs.find(p=>p.section===visible[0].target);if(pair)setActive(pair.link)}
   },{rootMargin:'-28% 0px -62% 0px',threshold:[0,.01]});
   pairs.forEach(pair=>observer.observe(pair.section));
   links.forEach(link=>link.addEventListener('click',()=>setActive(link)));
   setActive((pairs.find(p=>p.section.getBoundingClientRect().bottom>120)||pairs[0]).link);
  }
 }
 document.addEventListener('click',event=>{
  const target=event.target.closest('.approved-seat-hit,.seat-zone,.vs-day,.vs-time-grid a');
  if(!target)return;
  target.classList.remove('vs-polish-pulse');
  void target.offsetWidth;
  target.classList.add('vs-polish-pulse');
 },true);
 document.addEventListener('animationend',event=>{if(event.target.classList?.contains('vs-polish-pulse'))event.target.classList.remove('vs-polish-pulse')});
})();
'''

Path('assets/site-polish.css').write_text(CSS, encoding='utf-8')
Path('assets/site-polish.js').write_text(JS, encoding='utf-8')

footer = Path('components/footer.js')
text = footer.read_text(encoding='utf-8')
text = text.replace('// Vegas Sidekick — Shared Footer Loader v19', '// Vegas Sidekick — Shared Footer Loader v20')
old = """  function add(src, marker){\n    if(marker && document.querySelector('script['+marker+']')) return;\n    var s=document.createElement('script');\n    s.src=src;\n    s.async=false;\n    if(marker) s.setAttribute(marker,'1');\n    document.body.appendChild(s);\n  }\n  add('/components/footer-core.js?v=15','data-vs-footer-core');"""
new = """  function add(src, marker){\n    if(marker && document.querySelector('script['+marker+']')) return;\n    var s=document.createElement('script');\n    s.src=src;\n    s.async=false;\n    if(marker) s.setAttribute(marker,'1');\n    document.body.appendChild(s);\n  }\n  function addStyle(href, marker){\n    if(marker && document.querySelector('link['+marker+']')) return;\n    var l=document.createElement('link');\n    l.rel='stylesheet';\n    l.href=href;\n    if(marker) l.setAttribute(marker,'1');\n    document.head.appendChild(l);\n  }\n  addStyle('/assets/site-polish.css?v=1','data-vs-site-polish');\n  add('/assets/site-polish.js?v=1','data-vs-site-polish-script');\n  add('/components/footer-core.js?v=15','data-vs-footer-core');"""
if old not in text:
    raise SystemExit('Expected footer loader block not found')
footer.write_text(text.replace(old, new), encoding='utf-8')

shin = Path('shows/magic/shin-lim/index.html')
html = shin.read_text(encoding='utf-8')
stray = '<p>Palazzo Theatre · The Venetian Resort Las Vegas Shin Lim LIMITLESS Two-Time AGT Winner. World-Record Card Magic.</p>'
if stray not in html:
    raise SystemExit('Expected Shin Lim stray paragraph not found')
html = html.replace(stray, '', 1)
html = html.replace('Ages 5+.', 'Ages 4+.')
html = html.replace('"lastReviewed":"2026-09-12"', '"lastReviewed":"2026-09-13"')
shin.write_text(html, encoding='utf-8')

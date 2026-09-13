from pathlib import Path
import re

ROOT = Path('.')

def read(path):
    return (ROOT / path).read_text(encoding='utf-8')

def write(path, text):
    (ROOT / path).write_text(text, encoding='utf-8')

# Shared UI layer: 17–24. Keep this idempotent so a rerun is harmless.
css_path = 'assets/site-polish.css'
css = read(css_path)
marker = '/* 17–24: gallery restraint, icon weight, showtime clarity, CTA fit, spacing, stacking, ticket links, reduced motion. */'
block = r'''

/* 17–24: gallery restraint, icon weight, showtime clarity, CTA fit, spacing, stacking, ticket links, reduced motion. */
:root{--vs-z-sticky:600;--vs-z-nav:900;--vs-z-mobile:1100;--vs-z-overlay:1900;--vs-z-modal:2100;--vs-final-gap:clamp(36px,5vw,58px)}

/* 17: one-image galleries do not pretend to be carousels. */
.gallery.vs-gallery-single{grid-template-columns:minmax(0,1fr)!important}
.gallery.vs-gallery-single>button{max-width:760px;width:100%;margin-inline:auto}
body.vs-single-gallery-open #lightbox :where(.nbt-lb-nav,.approved-lb-nav,.vs-gallery-nav,[class$="-lb-prev"],[class$="-lb-next"],[class$="-lb-count"]){display:none!important}

/* 18: arrows, chevrons and close controls share one visual weight. */
:where(.drawer-x,.lightbox button,#lightboxClose,.nbt-lb-nav,.approved-lb-nav,.vs-gallery-nav,.approved-seat-close){font-family:Inter,Arial,sans-serif!important;font-weight:700!important;line-height:1!important;text-rendering:geometricPrecision}
.vs-gallery-nav{position:absolute;top:50%;transform:translateY(-50%);z-index:3;width:48px;height:48px;border:1px solid rgba(255,255,255,.35);border-radius:999px;background:rgba(20,10,34,.72);color:#fff;font-size:2rem;display:grid;place-items:center;cursor:pointer;backdrop-filter:blur(8px)}
.vs-gallery-prev{left:18px}.vs-gallery-next{right:18px}.vs-gallery-count{position:absolute;left:50%;bottom:20px;transform:translateX(-50%);z-index:3;padding:6px 10px;border-radius:999px;background:rgba(20,10,34,.72);color:#fff;font:700 .76rem/1 Inter,sans-serif;letter-spacing:.03em}

/* 19: selected booking choices should read instantly, not subtly. */
.vs-day{position:relative}
.vs-day.is-active{outline:2px solid rgba(255,255,255,.72);outline-offset:-5px}
.vs-day.is-active:after{content:'✓';position:absolute;right:7px;top:6px;width:18px;height:18px;border-radius:50%;display:grid;place-items:center;background:#fff;color:#5d20c9;font:900 .68rem/1 Inter,sans-serif;box-shadow:0 2px 8px rgba(31,12,56,.22)}
.vs-time-grid a{position:relative;transition:background .16s ease,color .16s ease,box-shadow .16s ease,transform .16s ease}
.vs-time-grid a.is-selected{background:#6422cf!important;color:#fff!important;box-shadow:0 0 0 3px rgba(100,34,207,.17),0 8px 18px rgba(74,28,144,.18)}
.vs-time-grid a.is-selected:after{content:'✓';margin-left:8px;font-weight:900}

/* 20: booking CTAs stay deliberate on narrow screens. */
:where(.vs-primary-book,.vs-all-dates,.vs-ticket-primary,.mobile-bar .cta,.vs-runtime-mobile a){white-space:nowrap;text-wrap:nowrap;min-width:0}

/* 21: finish pages cleanly without mystery dead space before the footer. */
main>:last-child{margin-bottom:0}
#vs-footer{margin-top:0!important}
.vs-runtime-next:last-of-type,.author-card:last-child,.kris-card:last-child{margin-bottom:0!important}

/* 22: one stacking ladder for sticky UI, nav, mobile CTA and overlays. */
:where(.subnav,.vs-runtime-nav){z-index:var(--vs-z-sticky)!important}
#vs-nav{z-index:var(--vs-z-nav)!important}
:where(.mobile-bar,.vs-runtime-mobile){z-index:var(--vs-z-mobile)!important}
:where(.nav-overlay){z-index:var(--vs-z-overlay)!important}
:where(.nav-mobile-drawer,.lightbox,dialog[open]){z-index:var(--vs-z-modal)!important}

/* 23: verified external ticket links behave consistently. */
a.vs-external-ticket{transition:filter .16s ease,transform .16s ease,box-shadow .16s ease}
a.vs-external-ticket:hover{filter:brightness(.97)}
a.vs-external-ticket:focus-visible{outline:3px solid #c6f22e;outline-offset:3px}

@media(max-width:420px){
 :where(.vs-primary-book,.vs-all-dates,.mobile-bar .cta,.vs-runtime-mobile a){font-size:clamp(.78rem,3.7vw,.92rem)!important;padding-inline:clamp(10px,3.5vw,16px)!important;letter-spacing:-.01em}
 .vs-gallery-nav{width:44px;height:44px}.vs-gallery-prev{left:10px}.vs-gallery-next{right:10px}
}

/* 24: reduced motion applies to the whole interaction system, including legacy one-offs. */
@media(prefers-reduced-motion:reduce){
 html{scroll-behavior:auto!important}
 *,*::before,*::after{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important;scroll-behavior:auto!important}
 :where(.show-card,.guide-card,.dispatch-card,.article-card,.related a,.decision-card[href],.path,.shortcut,.vs-runtime-clickable-day):hover{transform:none!important}
}
'''
if marker not in css:
    css = css.rstrip() + block + '\n'
write(css_path, css)

js_path = 'assets/site-polish.js'
js = read(js_path)
js_marker = '/* 17–25: finish the shared housekeeping pass. */'
js_block = r'''

 /* 17–25: finish the shared housekeeping pass. */
 const galleries=[...document.querySelectorAll('#photos .gallery,.gallery')].filter((g,i,a)=>a.indexOf(g)===i);
 galleries.forEach(gallery=>{
  const buttons=[...gallery.querySelectorAll(':scope > button')];
  if(buttons.length===1){
   gallery.classList.add('vs-gallery-single');
   buttons[0].dataset.vsSingleGallery='1';
  }
 });
 document.addEventListener('click',event=>{
  const galleryButton=event.target.closest('.gallery>button');
  if(galleryButton){
   document.body.classList.toggle('vs-single-gallery-open',galleryButton.dataset.vsSingleGallery==='1');
  }
  if(event.target.closest('#lightboxClose,.lightbox.open') && !event.target.closest('.lightbox img')){
   requestAnimationFrame(()=>{if(!document.querySelector('.lightbox.open'))document.body.classList.remove('vs-single-gallery-open')});
  }
 },true);

 /* Fill the gap on galleries that have multiple images but no existing arrows/count/swipe enhancer. */
 const enhanceGallery=()=>{
  const gallery=document.querySelector('#photos .gallery,.gallery');
  const light=document.getElementById('lightbox');
  if(!gallery||!light)return;
  const buttons=[...gallery.querySelectorAll(':scope > button')];
  if(buttons.length<2)return;
  if(light.querySelector('[aria-label="Previous photo"],[aria-label="Next photo"],.nbt-lb-nav,.approved-lb-nav,[class$="-lb-prev"]'))return;
  const img=light.querySelector('#lightboxImg,img');
  if(!img)return;
  let current=0,touchX=null;
  const prev=document.createElement('button'),next=document.createElement('button'),count=document.createElement('div');
  prev.type=next.type='button';prev.className='vs-gallery-nav vs-gallery-prev';next.className='vs-gallery-nav vs-gallery-next';count.className='vs-gallery-count';
  prev.setAttribute('aria-label','Previous photo');next.setAttribute('aria-label','Next photo');prev.textContent='‹';next.textContent='›';
  light.append(prev,next,count);
  const show=i=>{current=(i+buttons.length)%buttons.length;const thumb=buttons[current].querySelector('img');if(!thumb)return;img.src=thumb.currentSrc||thumb.src;img.alt=thumb.alt||'Vegas show photo';count.textContent=`${current+1} of ${buttons.length}`};
  buttons.forEach((button,i)=>button.addEventListener('click',()=>show(i)));
  prev.addEventListener('click',e=>{e.stopPropagation();show(current-1)});next.addEventListener('click',e=>{e.stopPropagation();show(current+1)});
  addEventListener('keydown',e=>{if(!light.classList.contains('open'))return;if(e.key==='ArrowLeft')show(current-1);if(e.key==='ArrowRight')show(current+1)});
  light.addEventListener('touchstart',e=>{touchX=e.changedTouches[0]?.clientX??null},{passive:true});
  light.addEventListener('touchend',e=>{if(touchX==null)return;const dx=(e.changedTouches[0]?.clientX??touchX)-touchX;touchX=null;if(Math.abs(dx)>45)show(current+(dx<0?1:-1))},{passive:true});
 };
 setTimeout(enhanceGallery,80);

 /* 19: preserve a clear selected time on the page when the ticket opens in a new tab. */
 document.addEventListener('click',event=>{
  const time=event.target.closest('.vs-time-grid a');
  if(!time)return;
  time.closest('.vs-time-grid')?.querySelectorAll('a').forEach(a=>{a.classList.toggle('is-selected',a===time);if(a===time)a.setAttribute('aria-current','true');else a.removeAttribute('aria-current')});
 },true);

 /* 23: normalize only already-verified external ticket destinations; never invent a URL. */
 document.querySelectorAll('a[href*="spotlight.vegas"]').forEach(link=>{
  link.target='_blank';
  const rel=new Set((link.getAttribute('rel')||'').split(/\s+/).filter(Boolean));rel.add('noopener');rel.add('sponsored');link.setAttribute('rel',[...rel].join(' '));
  link.classList.add('vs-external-ticket');
 });

 /* 25: remove empty legacy chrome, never substantive content. */
 document.querySelectorAll('.media-caption,.updated,.eyebrow,.gallery-count,.image-count').forEach(el=>{if(!(el.textContent||'').trim()&&!el.querySelector('img,svg,a,button'))el.remove()});
'''
if js_marker not in js:
    idx = js.rfind('})();')
    if idx == -1:
        raise SystemExit('Could not find site-polish closure')
    js = js[:idx] + js_block + '\n' + js[idx:]
write(js_path, js)

# Keep the locked booking module itself correct for future pages as well as the shared override.
booking_css_path = 'assets/showtimes-booking.css'
booking_css = read(booking_css_path)
booking_marker = '/* Housekeeping 19–20: unmistakable selection + narrow CTA fit. */'
booking_block = r'''

/* Housekeeping 19–20: unmistakable selection + narrow CTA fit. */
.vs-day{position:relative}
.vs-day.is-active{outline:2px solid rgba(255,255,255,.72);outline-offset:-5px}
.vs-day.is-active:after{content:'✓';position:absolute;right:7px;top:6px;width:18px;height:18px;border-radius:50%;display:grid;place-items:center;background:#fff;color:#5d20c9;font:900 .68rem/1 Inter,sans-serif}
.vs-time-grid a.is-selected{background:#6422cf;color:#fff;box-shadow:0 0 0 3px rgba(100,34,207,.17),0 8px 18px rgba(74,28,144,.18)}
.vs-time-grid a.is-selected:after{content:'✓';margin-left:8px}
.vs-primary-book,.vs-all-dates{white-space:nowrap;text-wrap:nowrap;min-width:0}
@media(max-width:420px){.vs-primary-book,.vs-all-dates{font-size:clamp(.78rem,3.7vw,.92rem);padding-inline:clamp(10px,3.5vw,16px)}}
'''
if booking_marker not in booking_css:
    booking_css = booking_css.rstrip() + booking_block + '\n'
write(booking_css_path, booking_css)

booking_js_path = 'assets/showtimes-booking.js'
booking_js = """(()=>{document.querySelectorAll('.vs-booking-shell[data-ticket-url]').forEach(shell=>{const ticket=shell.dataset.ticketUrl,days=[...shell.querySelectorAll('.vs-day[data-day]')],label=shell.querySelector('[data-selected-day]'),grid=shell.querySelector('.vs-time-grid'),primary=shell.querySelector('.vs-primary-book');if(!days.length||!label||!grid||!primary)return;const bindTimes=()=>{[...grid.querySelectorAll('a')].forEach(a=>a.addEventListener('click',()=>{grid.querySelectorAll('a').forEach(x=>{const on=x===a;x.classList.toggle('is-selected',on);if(on)x.setAttribute('aria-current','true');else x.removeAttribute('aria-current')})}))};const render=btn=>{days.forEach(b=>{const on=b===btn;b.classList.toggle('is-active',on);b.setAttribute('aria-selected',on?'true':'false')});const day=btn.dataset.day,times=(btn.dataset.times||'').split('|').filter(Boolean);label.textContent=day;grid.innerHTML=times.map(t=>`<a href=\"${ticket}\" rel=\"noopener sponsored\" target=\"_blank\">${t}</a>`).join('');primary.textContent=`Get Tickets for ${day} →`;bindTimes()};days.forEach(btn=>btn.addEventListener('click',()=>render(btn)));const initial=days.find(b=>b.classList.contains('is-active'))||days[0];if(initial)render(initial)});})();\n"""
write(booking_js_path, booking_js)

# 25: remove stale fallback generation that conflicts with the current positive Good Fit rule.
runtime_path = 'components/show-canonical-runtime.js'
runtime = read(runtime_path)
new_fit = """function ensureFit(){if(hasHeading('good fit')||document.querySelector('.decision-card.good,.fit-grid'))return;var c=CAT[cat()];if(!c)return;var s=document.createElement('section');s.className='vs-runtime-fit';s.id='fit';s.innerHTML='<div class=\"vs-runtime-wrap\"><div class=\"vs-runtime-eyebrow\">Is it for you?</div><h2>Good fit</h2><div class=\"vs-runtime-fit-grid\"><div class=\"vs-runtime-fit-card\"><h3>Good fit</h3><p>'+c.good+'</p></div></div></div>';var q=document.getElementById('faq')||document.querySelector('.faq-section');if(q&&q.parentNode)q.parentNode.insertBefore(s,q);else insertBeforeFooter(s)}
function ensureRelated"""
runtime, n = re.subn(r"function ensureFit\(\)\{.*?\}\nfunction ensureRelated", new_fit, runtime, count=1, flags=re.S)
if n != 1:
    raise SystemExit('Could not patch ensureFit exactly once')
runtime = runtime.replace('.vs-runtime-fit-grid{display:grid;grid-template-columns:1fr 1fr;', '.vs-runtime-fit-grid{display:grid;grid-template-columns:1fr;')
write(runtime_path, runtime)

# Prevent the legacy page generator from reintroducing a deprecated label.
canon_path = 'scripts/canonicalize-show-pages.py'
canon = read(canon_path)
canon = canon.replace('time_fact = fact(first_time, "Typical start")', 'time_fact = fact(first_time, "Start time")')
write(canon_path, canon)

# 25: persistent audit for old UI generators/visible labels.
audit_path = ROOT / 'scripts/audit-orphan-ui.py'
audit_path.write_text(r'''#!/usr/bin/env python3
"""Fail on known deprecated show-page UI labels/generators."""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
problems = []

for path in root.glob('shows/*/*/index.html'):
    text = path.read_text(encoding='utf-8', errors='ignore')
    checks = [
        (r'>\s*Typical start\s*<', 'visible "Typical start" label'),
        (r'>\s*Think twice\s*<', 'visible recurring "Think twice" label'),
        (r'>\s*Honest downside\s*<', 'visible "Honest downside" label'),
    ]
    for pattern, label in checks:
        if re.search(pattern, text, re.I):
            problems.append(f'{path.relative_to(root)}: {label}')

runtime = (root / 'components/show-canonical-runtime.js').read_text(encoding='utf-8')
if 'Good fit / Think twice' in runtime or '<h3>Think twice</h3>' in runtime:
    problems.append('components/show-canonical-runtime.js: deprecated Think twice fallback generator')
canon = (root / 'scripts/canonicalize-show-pages.py').read_text(encoding='utf-8')
if 'fact(first_time, "Typical start")' in canon:
    problems.append('scripts/canonicalize-show-pages.py: deprecated Typical start generator')

if problems:
    print('Orphan UI audit FAILED:')
    for problem in problems:
        print(' -', problem)
    raise SystemExit(1)
print('Orphan UI audit passed.')
''', encoding='utf-8')

# Document the new audit in the execution guide.
agents_path = 'AGENTS.md'
agents = read(agents_path)
needle = 'python3 scripts/audit-catalog-js-syntax.py\ngit diff --check'
if 'audit-orphan-ui.py' not in agents and needle in agents:
    agents = agents.replace(needle, 'python3 scripts/audit-catalog-js-syntax.py\npython3 scripts/audit-orphan-ui.py\ngit diff --check')
write(agents_path, agents)

# Lock the gallery control rule into the benchmark if it is not already stated.
bench_path = 'SHOW-PAGE-BENCHMARK.md'
bench = read(bench_path)
bench_line = '- One image: do not show carousel arrows or an image count. Multiple images: support arrows, count, keyboard navigation and mobile swipe.'
if bench_line not in bench:
    anchor = '- Remove instructional sentences telling users to inspect the photos.'
    if anchor in bench:
        bench = bench.replace(anchor, anchor + '\n' + bench_line)
write(bench_path, bench)

print('Applied housekeeping 17–25.')

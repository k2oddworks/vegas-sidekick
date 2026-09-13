/* Vegas Sidekick shared UI polish — navigation, cards, images and modal behavior. */
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

 /* 11–12: hero imagery gets priority; everything else lazy-decodes against a soft placeholder. */
 const tuneImage=img=>{
  const hero=!!img.closest('.hero,.hero-media,.show-hero,[data-hero]');
  if(hero){img.loading='eager';if(!img.getAttribute('fetchpriority'))img.setAttribute('fetchpriority','high')}
  else{if(!img.hasAttribute('loading'))img.loading='lazy';if(!img.hasAttribute('decoding'))img.decoding='async'}
  img.classList.add('vs-img-loading');
  const done=()=>{img.classList.remove('vs-img-loading');img.classList.add('vs-img-loaded')};
  if(img.complete)done();else img.addEventListener('load',done,{once:true});
 };
 document.querySelectorAll('img').forEach(tuneImage);

 /* 14: only stretch cards that contain one link and no competing interactive control. */
 const cardSelector='.show-card,.guide-card,.dispatch-card,.article-card,.related-card';
 document.querySelectorAll(cardSelector).forEach(card=>{
  if(card.matches('a[href]'))return;
  const links=[...card.querySelectorAll('a[href]')];
  if(links.length!==1||card.querySelector('button,input,select,textarea,details,summary'))return;
  const link=links[0];card.classList.add('vs-whole-card');
  card.addEventListener('click',event=>{if(event.target.closest('a'))return;link.click()});
 });

 /* 16: lock only when a genuinely open viewport overlay is present. */
 const syncScrollLock=()=>{
  const locked=!!document.querySelector('.lightbox.open,.nav-mobile-drawer.open,dialog[open]');
  document.body.classList.toggle('vs-scroll-locked',locked);
 };
 const lockObserver=new MutationObserver(syncScrollLock);
 lockObserver.observe(document.documentElement,{subtree:true,attributes:true,attributeFilter:['class','open']});
 document.addEventListener('click',()=>requestAnimationFrame(syncScrollLock),true);
 document.addEventListener('keydown',event=>{if(event.key==='Escape')requestAnimationFrame(syncScrollLock)});
 syncScrollLock();


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

})();

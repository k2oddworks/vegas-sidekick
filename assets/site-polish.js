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
})();

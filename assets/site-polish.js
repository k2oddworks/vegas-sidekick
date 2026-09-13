/* Vegas Sidekick shared UI polish — active section nav + selection feedback. */
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

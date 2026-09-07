(function(){'use strict';
const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
const progress=document.querySelector('.progress');
addEventListener('scroll',()=>{if(!progress)return;const d=document.documentElement;const max=d.scrollHeight-innerHeight;progress.style.width=(max?Math.min(100,scrollY/max*100):0)+'%'},{passive:true});
if(!reduce){document.querySelectorAll('.fact strong[data-count]').forEach(el=>{const target=parseFloat(el.dataset.count);if(!isFinite(target))return;const prefix=el.dataset.prefix||'',suffix=el.dataset.suffix||'';let done=false;const io=new IntersectionObserver(es=>es.forEach(en=>{if(!en.isIntersecting||done)return;done=true;io.disconnect();const start=performance.now(),dur=720;function tick(now){const p=Math.min(1,(now-start)/dur),e=1-Math.pow(1-p,3);el.textContent=prefix+Math.round(target*e)+suffix;if(p<1)requestAnimationFrame(tick)}requestAnimationFrame(tick)}),{threshold:.35});io.observe(el)});}
const detail=document.querySelector('#seat-detail');
document.querySelectorAll('.seat-zone').forEach(btn=>btn.addEventListener('click',()=>{document.querySelectorAll('.seat-zone').forEach(b=>b.classList.remove('active'));btn.classList.add('active');if(detail){detail.querySelector('.tag').textContent=btn.dataset.tag||'Seat guide';detail.querySelector('h3').textContent=btn.dataset.title||'';detail.querySelector('p').textContent=btn.dataset.copy||'';}}));
const light=document.querySelector('.lightbox'),lightImg=light&&light.querySelector('img');
document.querySelectorAll('.gallery button').forEach(b=>b.addEventListener('click',()=>{if(!light||!lightImg)return;lightImg.src=b.querySelector('img').src;light.hidden=false;document.body.style.overflow='hidden'}));
if(light)light.addEventListener('click',()=>{light.hidden=true;document.body.style.overflow=''});
document.querySelectorAll('.faq details').forEach(d=>d.addEventListener('toggle',()=>{if(d.open)document.querySelectorAll('.faq details').forEach(o=>{if(o!==d)o.open=false})}));
})();
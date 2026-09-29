/* Data comes from the page's real gallery images; no duplicated photo inventory. */
(function(){
 'use strict';
 document.querySelectorAll('[data-show-gallery]').forEach(function(root){
  if(root.dataset.galleryReady)return;
  const track=root.querySelector('.vs-gallery-track');
  const slides=Array.from(track.querySelectorAll('.vs-gallery-slide'));
  if(!slides.length)return;
  root.dataset.galleryReady='true';
  const images=slides.map(s=>s.querySelector('img'));
  const reduced=matchMedia('(prefers-reduced-motion: reduce)');
  let current=0,frame=0,opener=null,oldOverflow='',touch=null;
  function button(label,cls,text){const b=document.createElement('button');b.type='button';b.className=cls;b.setAttribute('aria-label',label);b.textContent=text;return b;}
  const toolbar=document.createElement('div');toolbar.className='vs-gallery-toolbar';
  const position=document.createElement('span');position.className='vs-gallery-position';position.setAttribute('aria-live','polite');position.setAttribute('aria-atomic','true');
  const arrows=document.createElement('div');arrows.className='vs-gallery-arrows';
  const prev=button('Previous image','vs-gallery-arrow','‹'),next=button('Next image','vs-gallery-arrow','›');
  arrows.append(prev,next);toolbar.append(position,arrows);
  const thumbs=document.createElement('div');thumbs.className='vs-gallery-thumbs';thumbs.setAttribute('aria-label','Choose an image');
  const thumbButtons=images.map((img,i)=>{const b=button('Show '+(slides[i].dataset.chart?'seating chart':'photo '+(i+1)),'vs-gallery-thumb','');const t=img.cloneNode();t.alt='';t.loading='lazy';b.append(t);if(slides[i].dataset.chart)b.dataset.chart='true';b.addEventListener('click',()=>go(i));thumbs.append(b);return b;});
  root.append(toolbar,thumbs);
  const dialog=document.createElement('dialog');dialog.className='vs-gallery-dialog';dialog.setAttribute('aria-label',root.getAttribute('aria-label')||'Show photos');
  const full=document.createElement('img'),close=button('Close gallery','vs-gallery-close','×'),back=button('Previous image','vs-gallery-dialog-prev','‹'),forward=button('Next image','vs-gallery-dialog-next','›'),caption=document.createElement('div');caption.className='vs-gallery-dialog-caption';caption.setAttribute('aria-live','polite');
  dialog.append(full,close,back,forward,caption);document.body.append(dialog);
  function update(){
   const label=slides[current].dataset.chart?'Seating chart':'Photo '+(current+1);
   position.textContent=(current+1)+' / '+slides.length+(slides[current].dataset.chart?' · Seating chart':'');
   slides.forEach((s,i)=>s.tabIndex=i===current?0:-1);
   thumbButtons.forEach((b,i)=>b.setAttribute('aria-current',String(i===current)));
   if(dialog.open){full.src=images[current].currentSrc||images[current].src;full.alt=images[current].alt;caption.textContent=label+' · '+(current+1)+' / '+slides.length;}
  }
  function left(i){return slides[i].getBoundingClientRect().left-track.getBoundingClientRect().left+track.scrollLeft;}
  function go(i,instant){current=(i+slides.length)%slides.length;track.scrollTo({left:left(current),behavior:instant||reduced.matches?'instant':'smooth'});update();}
  track.addEventListener('scroll',()=>{cancelAnimationFrame(frame);frame=requestAnimationFrame(()=>{if(dialog.open)return;let best=0;slides.forEach((s,i)=>{if(Math.abs(left(i)-track.scrollLeft)<Math.abs(left(best)-track.scrollLeft))best=i;});if(current!==best){current=best;update();}});},{passive:true});
  slides.forEach((s,i)=>s.addEventListener('click',()=>{opener=s;current=i;oldOverflow=document.body.style.overflow;dialog.showModal();document.body.style.overflow='hidden';update();close.focus();}));
  prev.addEventListener('click',()=>go(current-1));next.addEventListener('click',()=>go(current+1));
  back.addEventListener('click',()=>go(current-1,true));forward.addEventListener('click',()=>go(current+1,true));
  close.addEventListener('click',()=>dialog.close());
  dialog.addEventListener('click',e=>{if(e.target===dialog)dialog.close();});
  dialog.addEventListener('close',()=>{document.body.style.overflow=oldOverflow;go(current,true);(opener||slides[current]).focus({preventScroll:true});});
  function keys(e){if(e.key!=='ArrowLeft'&&e.key!=='ArrowRight')return;e.preventDefault();go(current+(e.key==='ArrowRight'?1:-1),dialog.open);if(!dialog.open&&slides.includes(document.activeElement))slides[current].focus({preventScroll:true});}
  root.addEventListener('keydown',keys);dialog.addEventListener('keydown',keys);
  dialog.addEventListener('touchstart',e=>{touch=e.touches.length===1?{x:e.touches[0].clientX,y:e.touches[0].clientY}:null;},{passive:true});
  dialog.addEventListener('touchmove',e=>{if(e.touches.length!==1)touch=null;},{passive:true});
  dialog.addEventListener('touchend',e=>{if(!touch)return;const dx=e.changedTouches[0].clientX-touch.x,dy=e.changedTouches[0].clientY-touch.y;touch=null;if(Math.abs(dx)>50&&Math.abs(dx)>Math.abs(dy)*1.5)go(current+(dx<0?1:-1),true);},{passive:true});
  dialog.addEventListener('touchcancel',()=>{touch=null;},{passive:true});
  let resizeTimer;window.addEventListener('resize',()=>{clearTimeout(resizeTimer);resizeTimer=setTimeout(()=>go(current,true),100);});
  if(slides.length===1){toolbar.hidden=true;thumbs.hidden=true;back.hidden=true;forward.hidden=true;}
  update();
 });
})();

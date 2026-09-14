/* Artwork and hit boundaries stay in HTML; shared controller owns all selection behavior. */
(()=>{'use strict';
 document.querySelectorAll('.approved-seat-guide').forEach(root=>{
  const controls=[...root.querySelectorAll('.approved-seat-hit')];
  const detail=root.querySelector('.approved-seat-detail');
  detail.setAttribute('aria-live','off');
  const sections=controls.map(button=>({
   id:button.dataset.section,label:button.dataset.label,
   pick:button.dataset.pick==='true',description:button.dataset.copy
  }));
  window.VSSeatInteractions.mount({
   root,controls,sections,getId:button=>button.dataset.section,
   onSelect:(section,label)=>{
    detail.querySelector('.approved-seat-tag').textContent=label;
    detail.querySelector('h3').textContent=section.label;
    detail.querySelector('p').textContent=section.description;
   }
  });
 });
 const buttons=[...document.querySelectorAll('#photos .gallery button')],light=document.getElementById('lightbox'),img=document.getElementById('lightboxImg');
 if(!buttons.length||!light||!img)return;
 let current=0,startX=null;
 const prev=document.createElement('button'),next=document.createElement('button'),count=document.createElement('div');
 prev.type=next.type='button';prev.className='approved-lb-nav approved-lb-prev';next.className='approved-lb-nav approved-lb-next';count.className='approved-lb-count';
 prev.textContent='‹';next.textContent='›';prev.setAttribute('aria-label','Previous photo');next.setAttribute('aria-label','Next photo');light.append(prev,next,count);
 function show(index){current=(index+buttons.length)%buttons.length;const source=buttons[current].querySelector('img');img.src=source.currentSrc||source.src;img.alt=source.alt;count.textContent=`${current+1} of ${buttons.length}`}
 buttons.forEach((button,index)=>button.addEventListener('click',()=>show(index)));
 prev.addEventListener('click',event=>{event.stopPropagation();show(current-1)});next.addEventListener('click',event=>{event.stopPropagation();show(current+1)});
 addEventListener('keydown',event=>{if(!light.classList.contains('open'))return;if(event.key==='ArrowLeft')show(current-1);if(event.key==='ArrowRight')show(current+1)});
 light.addEventListener('touchstart',event=>{startX=event.changedTouches[0].clientX},{passive:true});
 light.addEventListener('touchend',event=>{if(startX===null)return;const dx=event.changedTouches[0].clientX-startX;startX=null;if(Math.abs(dx)>45)show(current+(dx<0?1:-1))},{passive:true});
})();

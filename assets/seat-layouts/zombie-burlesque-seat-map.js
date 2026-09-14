(()=>{
 const root=document.querySelector('.zb-seat-guide');if(!root)return;
 const zones={vip:{label:'VIP',description:'VIP covers rows A–L closest to the stage. It is the Vegas Sidekick Sweet Spot / Our Pick for Zombie Burlesque: close enough for performer detail while still giving the full stage room to read.',pick:true},rear:{label:'Rear',description:'Rear covers rows M–V. It gives you a wider full-stage perspective and is the value-focused way to see the same production.',pick:false}};
 const detail=root.querySelector('.zb-seat-detail');
 detail.setAttribute('aria-live','off');
 window.VSSeatInteractions.mount({
  root,controls:root.querySelectorAll('[data-zone]'),hitSelector:'.zb-seat-hit',
  sections:Object.entries(zones).map(([id,zone])=>({id,...zone})),
  getId:button=>button.dataset.zone,initialId:'vip',
  onSelect:(section)=>{
   detail.querySelector('h3').textContent=section.label;
   detail.querySelector('p').textContent=section.description;
   detail.querySelector('.zb-seat-pick').hidden=!section.pick;
  }
 });
})();

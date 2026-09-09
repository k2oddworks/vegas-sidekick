(()=>{
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

(()=>{
  const esc=s=>String(s??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
  async function mount(root){
    const url=root.dataset.layoutUrl,ticket=root.dataset.ticketUrl;
    try{
      const data=await fetch(url,{credentials:'same-origin'}).then(r=>{if(!r.ok)throw new Error(`HTTP ${r.status}`);return r.json()});
      const byId=Object.fromEntries(data.sections.map(s=>[s.id,s]));
      const zone=s=>`<g class="mystere-map-zone" data-zone="${esc(s.id)}" role="button" tabindex="0" aria-label="Section ${esc(s.label)}${s.badge?`, ${esc(s.badge)}`:''}" style="--zone-color:${esc(s.color)}"><path d="${esc(s.path)}"></path><text x="${esc(s.label_x)}" y="${esc(s.label_y)}">${esc(s.label)}</text></g>`;
      root.innerHTML=`<div><div class="mystere-map-shell"><svg viewBox="${esc(data.viewBox)}" role="img" aria-label="Mystère Theatre seating layout">${data.sections.map(zone).join('')}<path class="mystere-stage" d="${esc(data.stage.path)}"></path><text class="mystere-stage-label" x="${esc(data.stage.label_x)}" y="${esc(data.stage.label_y)}">STAGE</text></svg><div class="mystere-map-caption"><strong>${esc(data.venue)}</strong><span>${esc(data.address)}</span></div></div></div><div><div class="mystere-seat-detail" aria-live="polite"><span class="tag">Sweet spot</span><h3>Section 203</h3><p>${esc(byId['203'].description)}</p><a class="cta vs-ticket-primary" href="${esc(ticket)}" target="_blank" rel="noopener sponsored">Check seats →</a></div><div class="mystere-legend"><span><i style="--legend-color:#d99500"></i>Sections 102–104 · Sweet spot / Our Pick</span><span><i style="--legend-color:#8d3cff"></i>Sections 202–205 · Sweet spot / Our Pick</span><span><i style="--legend-color:#16c7e8"></i>Sections 101 &amp; 105 · close view</span><span><i style="--legend-color:#ff2e7e"></i>Sections 201 &amp; 206 · side view</span></div></div><div class="mystere-mobile-popover" aria-live="polite" aria-atomic="true"><div><span class="mystere-mobile-badge">Sweet spot</span><strong>Section 203</strong><p>${esc(byId['203'].description)}</p></div><button type="button" aria-label="Close seat description">×</button></div>`;
      const detail=root.querySelector('.mystere-seat-detail'),pop=root.querySelector('.mystere-mobile-popover');
      const badge=s=>s.badge||(s.our_pick?'Sweet spot':'Seat guide');
      const activate=(id,showPop=false)=>{
        const s=byId[id];if(!s)return;
        root.querySelectorAll('[data-zone]').forEach(el=>el.classList.toggle('is-active',el.dataset.zone===id));
        detail.querySelector('.tag').textContent=badge(s);
        detail.querySelector('h3').textContent=`Section ${s.label}`;
        detail.querySelector('p').textContent=s.description;
        pop.querySelector('.mystere-mobile-badge').textContent=badge(s);
        pop.querySelector('strong').textContent=`Section ${s.label}`;
        pop.querySelector('p').textContent=s.description;
        if(showPop&&matchMedia('(max-width:820px)').matches)pop.classList.add('is-open');
      };
      root.addEventListener('click',e=>{
        const z=e.target.closest('[data-zone]');if(z)activate(z.dataset.zone,true);
        if(e.target.closest('.mystere-mobile-popover>button'))pop.classList.remove('is-open');
      });
      root.addEventListener('keydown',e=>{
        const z=e.target.closest('[data-zone]');if(z&&(e.key==='Enter'||e.key===' ')){e.preventDefault();activate(z.dataset.zone,true)}
      });
      addEventListener('scroll',()=>pop.classList.remove('is-open'),{passive:true});
      activate('203');
    }catch(err){
      root.innerHTML='<p>Seat guide unavailable right now. Use the live ticket map to compare sections for your date.</p>';
      console.warn('Mystère Theatre seat guide:',err);
    }
  }
  function enhanceGallery(){
    const buttons=[...document.querySelectorAll('#photos .gallery button')],light=document.getElementById('lightbox');
    if(!buttons.length||!light)return;
    const img=light.querySelector('#lightboxImg, img');if(!img)return;
    let current=0,touchX=null,prev=light.querySelector('.mystere-lb-prev'),next=light.querySelector('.mystere-lb-next'),count=light.querySelector('.mystere-lb-count');
    if(!prev){
      prev=document.createElement('button');prev.type='button';prev.className='mystere-lb-nav mystere-lb-prev';prev.setAttribute('aria-label','Previous photo');prev.textContent='‹';light.appendChild(prev);
      next=document.createElement('button');next.type='button';next.className='mystere-lb-nav mystere-lb-next';next.setAttribute('aria-label','Next photo');next.textContent='›';light.appendChild(next);
      count=document.createElement('div');count.className='mystere-lb-count';light.appendChild(count);
    }
    const show=i=>{current=(i+buttons.length)%buttons.length;const thumb=buttons[current].querySelector('img');img.src=thumb.currentSrc||thumb.src;img.alt=thumb.alt||'Mystère photo';count.textContent=`${current+1} of ${buttons.length}`};
    buttons.forEach((b,i)=>b.addEventListener('click',()=>show(i)));
    prev.addEventListener('click',e=>{e.stopPropagation();show(current-1)});
    next.addEventListener('click',e=>{e.stopPropagation();show(current+1)});
    addEventListener('keydown',e=>{if(!light.classList.contains('open'))return;if(e.key==='ArrowLeft')show(current-1);if(e.key==='ArrowRight')show(current+1)});
    light.addEventListener('touchstart',e=>{touchX=e.changedTouches[0]?.clientX??null},{passive:true});
    light.addEventListener('touchend',e=>{if(touchX==null)return;const dx=(e.changedTouches[0]?.clientX??touchX)-touchX;touchX=null;if(Math.abs(dx)>45)show(current+(dx<0?1:-1))},{passive:true});
  }
  document.querySelectorAll('[data-seat-layout="mystere-theatre"]').forEach(mount);
  enhanceGallery();
})();

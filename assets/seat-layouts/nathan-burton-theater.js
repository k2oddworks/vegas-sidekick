(()=>{
  const esc=s=>String(s??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
  const slabs=(n,color)=>Array.from({length:n},()=>`<span class="nbt-slab" style="--zone-color:${esc(color)}"></span>`).join('');

  async function mount(root){
    const url=root.dataset.layoutUrl;
    const ticket=root.dataset.ticketUrl;
    try{
      const data=await fetch(url,{credentials:'same-origin'}).then(r=>{if(!r.ok) throw new Error(`HTTP ${r.status}`);return r.json()});
      const byId=Object.fromEntries(data.zones.map(z=>[z.id,z]));
      const side=byId['front-sides'],front=byId['front-center'];
      const centers=data.zones.filter(z=>z.placement==='center'&&z.id!=='front-center');
      const mapZone=(z,extra='')=>`<button type="button" class="nbt-map-zone ${extra}" data-zone="${esc(z.id)}" aria-label="${esc(z.label)}" style="--zone-color:${esc(z.color)}">${slabs(z.rows,z.color)}</button>`;
      const badge=z=>z.badge|| (z.our_pick?'Sweet spot':'');
      root.innerHTML=`
        <div>
          <div class="nbt-map-shell">
            <div class="nbt-stage">STAGE</div>
            <div class="nbt-front-row">
              ${mapZone(side,'side left')}
              ${mapZone(front)}
              ${mapZone(side,'side right')}
            </div>
            <div class="nbt-center-stack">${centers.map(z=>mapZone(z)).join('')}</div>
            <div class="nbt-map-caption"><strong>${esc(data.venue)}</strong><span>${esc(data.address)}</span></div>
          </div>
          <p class="nbt-disclaimer">${esc(data.disclaimer)}</p>
        </div>
        <div>
          <div class="nbt-zone-panel">
            ${data.zones.map(z=>`<button type="button" class="nbt-zone-card" data-zone="${esc(z.id)}" style="--zone-color:${esc(z.color)}"><div class="nbt-zone-card-head"><span class="nbt-dot"></span><h3>${esc(z.label)}</h3>${badge(z)?`<span class="nbt-pick">${esc(badge(z))}</span>`:''}</div><p>${esc(z.description)}</p></button>`).join('')}
          </div>
          <div class="nbt-seat-detail" aria-live="polite"><div class="tag">Sweet spot</div><h3>Center section</h3><p>${esc(byId['sweet-spot'].description)}</p><a class="cta vs-ticket-primary" href="${esc(ticket)}" target="_blank" rel="noopener sponsored">Check seats →</a></div>
        </div>
        <div class="nbt-mobile-popover" aria-live="polite" aria-atomic="true"><div><span class="nbt-mobile-badge">Sweet spot</span><strong>Center section</strong><p>${esc(byId['sweet-spot'].description)}</p></div><button type="button" aria-label="Close seat description">×</button></div>`;
      const detail=root.querySelector('.nbt-seat-detail');
      const pop=root.querySelector('.nbt-mobile-popover');
      const activate=(id,showPop=false)=>{
        const z=byId[id]; if(!z) return;
        root.querySelectorAll('[data-zone]').forEach(el=>el.classList.toggle('is-active',el.dataset.zone===id));
        const b=badge(z)||'Seat guide';
        detail.querySelector('.tag').textContent=b;
        detail.querySelector('h3').textContent=z.label;
        detail.querySelector('p').textContent=z.description;
        pop.querySelector('.nbt-mobile-badge').textContent=b;
        pop.querySelector('strong').textContent=z.label;
        pop.querySelector('p').textContent=z.description;
        if(showPop && matchMedia('(max-width:820px)').matches) pop.classList.add('is-open');
      };
      root.addEventListener('click',e=>{
        const zone=e.target.closest('[data-zone]');
        if(zone) activate(zone.dataset.zone,true);
        if(e.target.closest('.nbt-mobile-popover>button')) pop.classList.remove('is-open');
      });
      addEventListener('scroll',()=>pop.classList.remove('is-open'),{passive:true});
      activate('sweet-spot');
    }catch(err){
      root.innerHTML='<p>Seat guide unavailable right now. Use the live ticket map to compare sections for your date.</p>';
      console.warn('Nathan Burton Theater seat guide:',err);
    }
  }

  function enhanceGallery(){
    const buttons=[...document.querySelectorAll('#photos .gallery button')];
    const light=document.getElementById('lightbox');
    if(!buttons.length||!light) return;
    const img=light.querySelector('#lightboxImg, img');
    if(!img) return;
    let current=0,touchX=null;
    let prev=light.querySelector('.nbt-lb-prev'),next=light.querySelector('.nbt-lb-next'),count=light.querySelector('.nbt-lb-count');
    if(!prev){
      prev=document.createElement('button');prev.type='button';prev.className='nbt-lb-nav nbt-lb-prev';prev.setAttribute('aria-label','Previous photo');prev.textContent='‹';light.appendChild(prev);
      next=document.createElement('button');next.type='button';next.className='nbt-lb-nav nbt-lb-next';next.setAttribute('aria-label','Next photo');next.textContent='›';light.appendChild(next);
      count=document.createElement('div');count.className='nbt-lb-count';light.appendChild(count);
    }
    const show=i=>{
      current=(i+buttons.length)%buttons.length;
      const thumb=buttons[current].querySelector('img');
      img.src=thumb.currentSrc||thumb.src;
      img.alt=thumb.alt||'Nathan Burton Comedy Magic photo';
      count.textContent=`${current+1} of ${buttons.length}`;
    };
    buttons.forEach((b,i)=>b.addEventListener('click',()=>show(i)));
    prev.addEventListener('click',e=>{e.stopPropagation();show(current-1)});
    next.addEventListener('click',e=>{e.stopPropagation();show(current+1)});
    addEventListener('keydown',e=>{if(!light.classList.contains('open'))return;if(e.key==='ArrowLeft')show(current-1);if(e.key==='ArrowRight')show(current+1)});
    light.addEventListener('touchstart',e=>{touchX=e.changedTouches[0]?.clientX??null},{passive:true});
    light.addEventListener('touchend',e=>{if(touchX==null)return;const dx=(e.changedTouches[0]?.clientX??touchX)-touchX;touchX=null;if(Math.abs(dx)>45)show(current+(dx<0?1:-1))},{passive:true});
  }

  document.querySelectorAll('[data-seat-layout="nathan-burton-theater"]').forEach(mount);
  enhanceGallery();
})();

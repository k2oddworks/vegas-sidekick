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
            ${data.zones.map(z=>`<button type="button" class="nbt-zone-card" data-zone="${esc(z.id)}" style="--zone-color:${esc(z.color)}"><div class="nbt-zone-card-head"><span class="nbt-dot"></span><h3>${esc(z.label)}</h3>${z.our_pick?'<span class="nbt-pick">Our Pick</span>':''}</div><p>${esc(z.description)}</p></button>`).join('')}
          </div>
          <div class="nbt-seat-detail" aria-live="polite"><div class="tag">Our Pick</div><h3>Sweet spot</h3><p>${esc(byId['sweet-spot'].description)}</p><a class="cta vs-ticket-primary" href="${esc(ticket)}" target="_blank" rel="noopener sponsored">Check seats →</a></div>
        </div>`;
      const detail=root.querySelector('.nbt-seat-detail');
      const activate=id=>{
        const z=byId[id]; if(!z) return;
        root.querySelectorAll('[data-zone]').forEach(el=>el.classList.toggle('is-active',el.dataset.zone===id));
        detail.querySelector('.tag').textContent=z.our_pick?'Our Pick':'Seat guide';
        detail.querySelector('h3').textContent=z.label;
        detail.querySelector('p').textContent=z.description;
      };
      root.addEventListener('click',e=>{const el=e.target.closest('[data-zone]');if(el)activate(el.dataset.zone)});
      activate('sweet-spot');
    }catch(err){
      root.innerHTML='<p>Seat guide unavailable right now. Use the live ticket map to compare sections for your date.</p>';
      console.warn('Nathan Burton Theater seat guide:',err);
    }
  }
  document.querySelectorAll('[data-seat-layout="nathan-burton-theater"]').forEach(mount);
})();

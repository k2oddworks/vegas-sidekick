(()=>{
  const esc=s=>String(s??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
  const chair=(x,y,r=.7)=>`<circle class="chair" cx="${x}" cy="${y}" r="${r}"/>`;
  const tableMarkup=(z,t)=>{const x=Number(t.x),y=Number(t.y),r=Number(t.r||2.2);return `<g tabindex="0" role="button" aria-label="${esc(z.label)}" class="vs-room-table" data-zone="${esc(z.id)}">${chair(x,y-r-1)}${chair(x+r+1,y)}${chair(x,y+r+1)}${chair(x-r-1,y)}<circle class="table-top" cx="${x}" cy="${y}" r="${r}" fill="${esc(z.color)}"/></g>`};
  async function mount(root){
    const d=await fetch(root.dataset.layoutUrl,{credentials:'same-origin'}).then(r=>{if(!r.ok)throw Error(r.status);return r.json()});
    const ticket=root.dataset.ticketUrl,by=Object.fromEntries(d.zones.map(z=>[z.id,z]));
    if(d.image){
      root.classList.add('vs-room-image-layout');
      if(d.highlightMode==='precise-outline')root.classList.add('vs-room-precise-highlight');
      const galleryChart=document.querySelector('#photos .vs-chart-gallery img');
      if(galleryChart){
        galleryChart.src=d.image;
        galleryChart.alt=`${d.venue} seating chart showing ${d.zones.map(z=>z.label).join(', ')}`;
        const gallery=galleryChart.closest('.gallery');
        if(gallery&&gallery.querySelectorAll(':scope > button').length===4){
          gallery.classList.remove('gallery-1','gallery-2','gallery-3');
          gallery.classList.add('gallery-4');
        }
      }
    }
    let map='';
    if(d.image){
      const hits=d.zones.map(z=>(z.hitPaths||[]).map(p=>`<path tabindex="0" role="button" aria-label="${esc(z.label)}" data-zone="${esc(z.id)}" class="vs-room-zone vs-room-image-hit" d="${esc(p)}" fill="${esc(z.color)}" fill-opacity="0" stroke="none" pointer-events="all" vector-effect="non-scaling-stroke" style="--zone-color:${esc(z.color)}"/>`).join('')).join('');
      map=`<svg width="1200" height="1200" viewBox="${esc(d.viewBox)}" aria-label="${esc(d.venue)} seating layout"><image href="${esc(d.image)}" x="0" y="0" width="1200" height="1200" preserveAspectRatio="xMidYMid meet"/>${hits}</svg>`;
    }else{
      const shapes=d.zones.map(z=>{const rows=(z.rows||[]).map(y=>`<path class="vs-room-row" d="M4 ${y} H116" clip-path="url(#c-${esc(z.id)})"/>`).join('');const tables=(z.tables||[]).map(t=>tableMarkup(z,t)).join('');return `<g><clipPath id="c-${esc(z.id)}"><path d="${esc(z.path)}"/></clipPath><path tabindex="0" role="button" aria-label="${esc(z.label)}" data-zone="${esc(z.id)}" class="vs-room-zone" d="${esc(z.path)}" fill="${esc(z.color)}"/>${rows}${tables}<text x="${z.labelX}" y="${z.labelY}" text-anchor="middle" dominant-baseline="middle" class="vs-room-label ${z.our_pick?'dark':''}">${esc(z.mapLabel||z.label.replace('Section ',''))}</text></g>`}).join('');
      const structs=(d.structures||[]).map(s=>`<path class="vs-room-structure" d="${esc(s.path)}"/><text x="${s.labelX}" y="${s.labelY}" text-anchor="middle" dominant-baseline="middle" class="vs-room-structure-label">${esc(s.label)}</text>`).join('');
      map=`<svg width="1200" height="1000" viewBox="${esc(d.viewBox)}" aria-label="${esc(d.venue)} seating layout"><rect width="120" height="110" rx="5" fill="#0d0815"/>${shapes}${structs}<path class="vs-room-stage" d="${esc(d.stage.path)}"/><text x="${d.stage.labelX}" y="${d.stage.labelY}" text-anchor="middle" dominant-baseline="middle" class="vs-room-stage-label">${esc(d.stage.label||'STAGE')}</text></svg>`;
    }
    root.innerHTML=`<div class="vs-room-guide"><div class="vs-room-map">${map}</div><div><div class="vs-room-cards">${d.zones.map(z=>`<button type="button" class="vs-room-card ${z.our_pick?'is-pick':''}" data-zone="${esc(z.id)}" style="--zone-color:${esc(z.color)}"><strong>${esc(z.label)}</strong><span>${z.our_pick?'Sweet Spot / Our Pick':esc(z.badge)}</span></button>`).join('')}</div><div class="vs-room-detail" aria-live="polite"><div class="tag"></div><h3></h3><p></p><a class="cta vs-ticket-primary" href="${esc(ticket)}" target="_blank" rel="noopener sponsored">Check seats →</a></div></div></div><div class="vs-room-mobile" aria-live="polite"><strong></strong><p></p><button type="button" aria-label="Close seat description">×</button></div>`;
    const detail=root.querySelector('.vs-room-detail'),pop=root.querySelector('.vs-room-mobile'),mapEl=root.querySelector('.vs-room-map');
    function act(id,show,source){
      const z=by[id];if(!z)return;
      root.querySelectorAll('[data-zone]').forEach(x=>x.classList.toggle('is-active',x.dataset.zone===id));
      detail.querySelector('.tag').textContent=z.our_pick?'Sweet Spot / Our Pick':z.badge;
      detail.querySelector('h3').textContent=z.label;
      detail.querySelector('p').textContent=z.description;
      pop.querySelector('strong').textContent=(z.our_pick?'Sweet Spot · ':'')+z.label;
      pop.querySelector('p').textContent=z.description;
      if(show&&matchMedia('(max-width:820px)').matches){
        const card=source?.closest?.('.vs-room-card');
        if(card)card.insertAdjacentElement('afterend',pop);else mapEl.insertAdjacentElement('afterend',pop);
        pop.classList.add('is-open');
        if(root.dataset.mobilePopup!=='fixed')requestAnimationFrame(()=>pop.scrollIntoView({behavior:'smooth',block:'nearest'}));
      }
    }
    root.addEventListener('click',e=>{const z=e.target.closest('[data-zone]');if(z)act(z.dataset.zone,true,z);if(e.target.closest('.vs-room-mobile button'))pop.classList.remove('is-open')});
    root.addEventListener('keydown',e=>{const z=e.target.closest('[data-zone]');if(z&&(e.key==='Enter'||e.key===' ')){e.preventDefault();act(z.dataset.zone,true,z)}});
    act((d.zones.find(z=>z.our_pick)||d.zones[0]).id,false);
  }
  document.querySelectorAll('[data-seat-layout]').forEach(mount);
  const b=[...document.querySelectorAll('#photos .gallery button')],l=document.getElementById('lightbox');
  if(b.length&&l){const img=l.querySelector('#lightboxImg, img');let i=0,x=null;let p=l.querySelector('.vs-lb-prev'),n=l.querySelector('.vs-lb-next'),c=l.querySelector('.vs-lb-count');if(!p){p=document.createElement('button');p.type='button';p.className='vs-lb-nav vs-lb-prev';p.textContent='‹';p.setAttribute('aria-label','Previous photo');n=document.createElement('button');n.type='button';n.className='vs-lb-nav vs-lb-next';n.textContent='›';n.setAttribute('aria-label','Next photo');c=document.createElement('div');c.className='vs-lb-count';l.append(p,n,c)}const show=j=>{i=(j+b.length)%b.length;const t=b[i].querySelector('img');img.src=t.currentSrc||t.src;img.alt=t.alt||'Show photo';c.textContent=`${i+1} of ${b.length}`};b.forEach((q,j)=>q.addEventListener('click',()=>show(j)));p.onclick=e=>{e.stopPropagation();show(i-1)};n.onclick=e=>{e.stopPropagation();show(i+1)};addEventListener('keydown',e=>{if(!l.classList.contains('open'))return;if(e.key==='ArrowLeft')show(i-1);if(e.key==='ArrowRight')show(i+1)});l.addEventListener('touchstart',e=>x=e.changedTouches[0]?.clientX??null,{passive:true});l.addEventListener('touchend',e=>{if(x==null)return;const dx=(e.changedTouches[0]?.clientX??x)-x;x=null;if(Math.abs(dx)>45)show(i+(dx<0?1:-1))},{passive:true})}
})();

(()=>{
  const esc=s=>String(s??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
  async function mount(root){
    try{
      const data=await fetch(root.dataset.layoutUrl,{credentials:'same-origin'}).then(r=>{if(!r.ok)throw Error(r.status);return r.json()});
      const ticket=root.dataset.ticketUrl;
      const by=Object.fromEntries(data.zones.map(z=>[z.id,z]));
      const defs=data.zones.map(z=>`<clipPath id="mbt-clip-${esc(z.id)}"><path d="${esc(z.path)}"/></clipPath>`).join('');
      const shapes=data.zones.map(z=>{
        const [x1,,x2]=z.bbox;
        const rows=z.rowYs.map((y,i)=>`<path class="mbt-row-line" d="M${x1} ${y} Q${(x1+x2)/2} ${y+(i%2?0.7:-0.5)} ${x2} ${y}" clip-path="url(#mbt-clip-${esc(z.id)})"/>`).join('');
        return `<g class="mbt-zone-group" data-zone="${esc(z.id)}"><path tabindex="0" role="button" aria-label="${esc(z.label)}" class="mbt-shape" data-zone="${esc(z.id)}" d="${esc(z.path)}" fill="${esc(z.color)}"/>${rows}<text x="${z.labelX}" y="${z.labelY}" text-anchor="middle" dominant-baseline="middle" class="mbt-label ${z.our_pick?'':'side'}">${esc(z.id)}</text></g>`;
      }).join('');
      root.innerHTML=`
        <div class="mbt-map">
          <svg width="1200" height="1000" viewBox="${esc(data.viewBox)}" aria-label="Mandalay Bay Theatre seating layout">
            <defs>${defs}</defs>
            <rect width="120" height="100" rx="4" fill="#0d0815"/>
            ${shapes}
            <path class="mbt-stage" d="${esc(data.stage.path)}"/>
            <text x="${data.stage.labelX}" y="${data.stage.labelY}" text-anchor="middle" class="mbt-stage-label">STAGE</text>
            <rect x="39" y="93" width="42" height="4.8" rx="2.4" class="mbt-pick-pill"/>
            <text x="60" y="96.1" text-anchor="middle" class="mbt-pick-label">OUR PICK · SWEET SPOT</text>
          </svg>
        </div>
        <div>
          <div class="mbt-cards">${data.zones.map(z=>`<button type="button" class="mbt-card ${z.our_pick?'is-pick':''}" data-zone="${esc(z.id)}"><h3>${esc(z.label)}</h3><span class="mbt-badge">${z.our_pick?'Sweet Spot / Our Pick':esc(z.badge)}</span></button>`).join('')}</div>
          <div class="mbt-detail" aria-live="polite"><div class="tag"></div><h3></h3><p></p><a class="cta vs-ticket-primary" href="${esc(ticket)}" target="_blank" rel="noopener sponsored">Check seats →</a></div>
        </div>
        <div class="mbt-mobile" aria-live="polite"><strong></strong><p></p><button type="button" aria-label="Close seat description">×</button></div>`;
      const detail=root.querySelector('.mbt-detail'),pop=root.querySelector('.mbt-mobile');
      function activate(id,show){
        const z=by[id]; if(!z)return;
        root.querySelectorAll('.mbt-shape,.mbt-card').forEach(x=>x.classList.toggle('is-active',x.dataset.zone===id));
        detail.querySelector('.tag').textContent=z.our_pick?'Sweet Spot / Our Pick':z.badge;
        detail.querySelector('h3').textContent=z.label;
        detail.querySelector('p').textContent=z.description;
        pop.querySelector('strong').textContent=(z.our_pick?'Sweet Spot · ':'')+z.label;
        pop.querySelector('p').textContent=z.description;
        if(show&&matchMedia('(max-width:820px)').matches)pop.classList.add('is-open');
      }
      root.addEventListener('click',e=>{
        const z=e.target.closest('[data-zone]');
        if(z)activate(z.dataset.zone,true);
        if(e.target.closest('.mbt-mobile button'))pop.classList.remove('is-open');
      });
      root.addEventListener('keydown',e=>{
        const z=e.target.closest('.mbt-shape');
        if(z&&(e.key==='Enter'||e.key===' ')){e.preventDefault();activate(z.dataset.zone,true)}
      });
      activate('102',false);
    }catch(e){
      root.innerHTML='<p>Seat guide unavailable right now. Use the live ticket map to compare sections for your date.</p>';
    }
  }
  function gallery(){
    const b=[...document.querySelectorAll('#photos .gallery button')],l=document.getElementById('lightbox');
    if(!b.length||!l)return;
    const img=l.querySelector('#lightboxImg, img');let i=0,x=null,p=l.querySelector('.mbt-lb-prev'),n=l.querySelector('.mbt-lb-next'),c=l.querySelector('.mbt-lb-count');
    if(!p){p=document.createElement('button');p.type='button';p.className='mbt-lb-nav mbt-lb-prev';p.textContent='‹';p.setAttribute('aria-label','Previous photo');n=document.createElement('button');n.type='button';n.className='mbt-lb-nav mbt-lb-next';n.textContent='›';n.setAttribute('aria-label','Next photo');c=document.createElement('div');c.className='mbt-lb-count';l.append(p,n,c)}
    const show=j=>{i=(j+b.length)%b.length;const t=b[i].querySelector('img');img.src=t.currentSrc||t.src;img.alt=t.alt||'Michael Jackson ONE photo';c.textContent=`${i+1} of ${b.length}`};
    b.forEach((q,j)=>q.addEventListener('click',()=>show(j)));p.onclick=e=>{e.stopPropagation();show(i-1)};n.onclick=e=>{e.stopPropagation();show(i+1)};
    addEventListener('keydown',e=>{if(!l.classList.contains('open'))return;if(e.key==='ArrowLeft')show(i-1);if(e.key==='ArrowRight')show(i+1)});
    l.addEventListener('touchstart',e=>x=e.changedTouches[0]?.clientX??null,{passive:true});
    l.addEventListener('touchend',e=>{if(x==null)return;const d=(e.changedTouches[0]?.clientX??x)-x;x=null;if(Math.abs(d)>45)show(i+(d<0?1:-1))},{passive:true});
  }
  document.querySelectorAll('[data-seat-layout="mandalay-bay-theatre"]').forEach(mount);gallery();
})();

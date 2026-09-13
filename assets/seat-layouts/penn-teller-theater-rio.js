(()=>{
  const chartCache=new Map();

  async function loadChart(parts){
    const key=parts.join('|');
    if(chartCache.has(key)) return chartCache.get(key);
    const promise=Promise.all(parts.map(url=>fetch(url,{credentials:'same-origin'}).then(r=>{if(!r.ok)throw new Error(`Chart asset ${r.status}`);return r.text()}))).then(chunks=>`data:image/jpeg;base64,${chunks.join('')}`);
    chartCache.set(key,promise);
    return promise;
  }

  async function mount(root){
    const data=await fetch(root.dataset.layoutUrl,{credentials:'same-origin'}).then(r=>{if(!r.ok)throw new Error(`Layout ${r.status}`);return r.json()});
    const chartSrc=await loadChart(data.chart_parts);
    const ticket=root.dataset.ticketUrl;
    const byId=Object.fromEntries(data.zones.map(zone=>[zone.id,zone]));

    const mapShell=document.createElement('div');
    mapShell.className='ptr-map-shell';
    const map=document.createElement('div');
    map.className='ptr-seat-map';
    const chart=document.createElement('img');
    chart.src=chartSrc;
    chart.alt='Penn & Teller Theater seating chart showing Sections 1 through 9, AMP areas and booths, with Sections 1 through 6 as the Vegas Sidekick Sweet Spot';
    map.appendChild(chart);

    data.zones.forEach(zone=>{
      zone.hitboxes.forEach((box,index)=>{
        const hit=document.createElement('button');
        hit.type='button';
        hit.className='ptr-seat-hit';
        hit.dataset.zone=zone.id;
        hit.setAttribute('aria-label',`${zone.label}${zone.our_pick?', Sweet Spot / Our Pick':''}${index?' seating area':''}`);
        hit.style.left=`${box.left}%`;
        hit.style.top=`${box.top}%`;
        hit.style.width=`${box.width}%`;
        hit.style.height=`${box.height}%`;
        hit.style.setProperty('--hit-shape',box.clip);
        map.appendChild(hit);
      });
    });

    const popup=document.createElement('div');
    popup.className='ptr-seat-popup';
    popup.setAttribute('aria-live','polite');
    popup.setAttribute('aria-atomic','true');
    const popupTag=document.createElement('span');popupTag.className='tag';
    const popupTitle=document.createElement('strong');
    const popupCopy=document.createElement('p');
    const popupClose=document.createElement('button');popupClose.type='button';popupClose.className='ptr-seat-popup-close';popupClose.setAttribute('aria-label','Close seat description');popupClose.textContent='×';
    popup.append(popupTag,popupTitle,popupCopy,popupClose);
    map.appendChild(popup);

    const caption=document.createElement('div');
    caption.className='ptr-map-caption';
    const venue=document.createElement('strong');venue.textContent=data.venue;
    const address=document.createElement('span');address.textContent=data.address;
    caption.append(venue,address);
    mapShell.append(map,caption);

    const detail=document.createElement('div');
    detail.className='ptr-seat-detail';
    detail.setAttribute('aria-live','polite');
    const tag=document.createElement('span');tag.className='tag';
    const heading=document.createElement('h3');
    const copy=document.createElement('p');
    detail.append(tag,heading,copy);

    const legend=document.createElement('div');
    legend.className='ptr-seat-legend';
    legend.innerHTML='<span><i></i><b>Sweet Spot / Our Pick:</b>&nbsp;Sections 1–6</span><span><i></i><b>Wider view:</b>&nbsp;Sections 7–9</span><span><i></i><b>Stage-side:</b>&nbsp;AMP 1–3</span><span><i></i><b>Booth seating:</b>&nbsp;Booths</span>';

    const book=document.createElement('a');
    book.className='ptr-seat-book vs-ticket-primary';
    book.href=ticket;
    book.target='_blank';
    book.rel='noopener sponsored';
    book.textContent='Check tickets & seating →';

    const side=document.createElement('div');
    side.className='ptr-seat-side';
    side.append(detail,legend,book);
    root.replaceChildren(mapShell,side);

    function activate(id,showPopup=true){
      const zone=byId[id];
      if(!zone)return;
      root.querySelectorAll('[data-zone]').forEach(el=>el.classList.toggle('is-active',el.dataset.zone===id));
      const label=zone.our_pick?'Sweet spot':zone.badge;
      tag.textContent=label;
      heading.textContent=zone.label;
      copy.textContent=zone.description;
      popupTag.textContent=label;
      popupTitle.textContent=zone.label;
      popupCopy.textContent=zone.description;
      if(showPopup){
        popup.classList.remove('is-open');
        requestAnimationFrame(()=>popup.classList.add('is-open'));
      }
    }

    root.addEventListener('click',event=>{
      if(event.target.closest('.ptr-seat-popup-close')){popup.classList.remove('is-open');return;}
      const control=event.target.closest('[data-zone]');
      if(control)activate(control.dataset.zone,true);
    });
    root.addEventListener('keydown',event=>{
      const control=event.target.closest('[data-zone]');
      if(control&&(event.key==='Enter'||event.key===' ')){
        event.preventDefault();
        activate(control.dataset.zone,true);
      }
      if(event.key==='Escape')popup.classList.remove('is-open');
    });
    activate('section-2',false);

    const galleryChart=document.querySelector('.ptr-chart-gallery img');
    if(galleryChart){
      galleryChart.src=chartSrc;
      galleryChart.alt='Penn & Teller Theater seating chart showing Sections 1 through 9, AMP areas and booths, with Sections 1 through 6 as the Vegas Sidekick Sweet Spot';
    }
  }

  function enhanceGallery(){
    const buttons=[...document.querySelectorAll('#photos .gallery button')];
    const light=document.getElementById('lightbox');
    if(!buttons.length||!light)return;
    const img=light.querySelector('#lightboxImg, img');
    if(!img)return;
    let current=0,touchX=null;
    let prev=light.querySelector('.ptr-lb-prev');
    let next=light.querySelector('.ptr-lb-next');
    let count=light.querySelector('.ptr-lb-count');
    if(!prev){
      prev=document.createElement('button');prev.type='button';prev.className='ptr-lb-nav ptr-lb-prev';prev.setAttribute('aria-label','Previous photo');prev.textContent='‹';light.appendChild(prev);
      next=document.createElement('button');next.type='button';next.className='ptr-lb-nav ptr-lb-next';next.setAttribute('aria-label','Next photo');next.textContent='›';light.appendChild(next);
      count=document.createElement('div');count.className='ptr-lb-count';light.appendChild(count);
    }
    const show=index=>{
      current=(index+buttons.length)%buttons.length;
      const thumb=buttons[current].querySelector('img');
      img.src=thumb.currentSrc||thumb.src;
      img.alt=thumb.alt||'Penn & Teller photo';
      count.textContent=`${current+1} of ${buttons.length}`;
    };
    buttons.forEach((button,index)=>button.addEventListener('click',()=>show(index)));
    prev.addEventListener('click',event=>{event.stopPropagation();show(current-1)});
    next.addEventListener('click',event=>{event.stopPropagation();show(current+1)});
    addEventListener('keydown',event=>{if(!light.classList.contains('open'))return;if(event.key==='ArrowLeft')show(current-1);if(event.key==='ArrowRight')show(current+1)});
    light.addEventListener('touchstart',event=>{touchX=event.changedTouches[0]?.clientX??null},{passive:true});
    light.addEventListener('touchend',event=>{if(touchX==null)return;const dx=(event.changedTouches[0]?.clientX??touchX)-touchX;touchX=null;if(Math.abs(dx)>45)show(current+(dx<0?1:-1))},{passive:true});
  }

  const mounts=[...document.querySelectorAll('[data-seat-layout="penn-teller-theater-rio"]')].map(root=>mount(root).catch(err=>{
    root.textContent='Seat guide unavailable right now. Use the live ticket map to compare sections for your date.';
    console.warn('Penn & Teller seat guide:',err);
  }));
  Promise.allSettled(mounts).then(enhanceGallery);
})();

(()=>{
  async function mount(root){
    const data=await fetch(root.dataset.layoutUrl,{credentials:'same-origin'}).then(r=>r.json());
    const ticket=root.dataset.ticketUrl;
    const byId=Object.fromEntries(data.sections.map(section=>[section.id,section]));

    const mapShell=document.createElement('div');
    mapShell.className='mystere-map-shell';
    const map=document.createElement('div');
    map.className='mystere-seat-map';
    const chart=document.createElement('img');
    chart.src=data.chart_asset;
    chart.alt='Mystère Theatre seating chart showing sections 101 through 206, with sections 102 through 104 and 202 through 205 marked as the Vegas Sidekick sweet spot';
    map.appendChild(chart);

    data.sections.forEach(section=>{
      const hit=document.createElement('button');
      hit.type='button';
      hit.className='mystere-seat-hit';
      hit.dataset.zone=section.id;
      hit.setAttribute('aria-label',`Section ${section.label}${section.our_pick?', Sweet Spot':''}`);
      hit.style.setProperty('--hit-shape',section.hitbox);
      map.appendChild(hit);
    });

    const popup=document.createElement('div');
    popup.className='mystere-seat-popup';
    popup.setAttribute('aria-live','polite');
    popup.setAttribute('aria-atomic','true');
    const popupTag=document.createElement('span');
    popupTag.className='tag';
    const popupTitle=document.createElement('strong');
    const popupCopy=document.createElement('p');
    const popupClose=document.createElement('button');
    popupClose.type='button';
    popupClose.className='mystere-seat-popup-close';
    popupClose.setAttribute('aria-label','Close seat description');
    popupClose.textContent='×';
    popup.append(popupTag,popupTitle,popupCopy,popupClose);
    map.appendChild(popup);

    const caption=document.createElement('div');
    caption.className='mystere-map-caption';
    const venue=document.createElement('strong');
    venue.textContent=data.venue;
    const address=document.createElement('span');
    address.textContent=data.address;
    caption.append(venue,address);
    mapShell.append(map,caption);

    const detail=document.createElement('div');
    detail.className='mystere-seat-detail';
    detail.setAttribute('aria-live','polite');
    const tag=document.createElement('span');
    tag.className='tag';
    const heading=document.createElement('h3');
    const copy=document.createElement('p');
    detail.append(tag,heading,copy);

    const legend=document.createElement('div');
    legend.className='mystere-seat-legend';
    const legendRows=[
      ['pick','Sweet Spot / Our Pick','102–104, 202–205'],
      ['close','Close view','101, 105'],
      ['side','Side view','201, 206']
    ];
    legendRows.forEach(([kind,label,sections])=>{
      const row=document.createElement('div');
      row.className='mystere-seat-legend-row';
      const dot=document.createElement('span');
      dot.className=`mystere-seat-legend-dot ${kind}`;
      const text=document.createElement('div');
      const strong=document.createElement('strong');
      strong.textContent=label;
      const small=document.createElement('span');
      small.textContent=sections;
      text.append(strong,small);
      row.append(dot,text);
      legend.appendChild(row);
    });

    const side=document.createElement('div');
    side.className='mystere-seat-side';
    side.append(detail,legend);

    const book=document.createElement('a');
    book.className='mystere-seat-book vs-ticket-primary';
    book.href=ticket;
    book.target='_blank';
    book.rel='noopener sponsored';
    book.textContent='Check tickets & seating →';
    side.appendChild(book);

    root.replaceChildren(mapShell,side);

    function activate(id,showPopup=true){
      const section=byId[id];
      if(!section)return;
      root.querySelectorAll('[data-zone]').forEach(el=>el.classList.toggle('is-active',el.dataset.zone===id));
      const label=section.our_pick?'Sweet spot':section.badge;
      tag.textContent=label;
      heading.textContent=`Section ${section.label}`;
      copy.textContent=section.description;
      popupTag.textContent=label;
      popupTitle.textContent=`Section ${section.label}`;
      popupCopy.textContent=section.description;
      if(showPopup){
        popup.classList.remove('is-open');
        requestAnimationFrame(()=>popup.classList.add('is-open'));
      }
    }

    root.addEventListener('click',event=>{
      if(event.target.closest('.mystere-seat-popup-close')){
        popup.classList.remove('is-open');
        return;
      }
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
    activate('203',false);
  }

  function enhanceGallery(){
    const buttons=[...document.querySelectorAll('#photos .gallery button')];
    const light=document.getElementById('lightbox');
    if(!buttons.length||!light)return;
    const img=light.querySelector('#lightboxImg, img');
    if(!img)return;
    let current=0,touchX=null;
    let prev=light.querySelector('.mystere-lb-prev');
    let next=light.querySelector('.mystere-lb-next');
    let count=light.querySelector('.mystere-lb-count');
    if(!prev){
      prev=document.createElement('button');
      prev.type='button';
      prev.className='mystere-lb-nav mystere-lb-prev';
      prev.setAttribute('aria-label','Previous photo');
      prev.textContent='‹';
      light.appendChild(prev);
      next=document.createElement('button');
      next.type='button';
      next.className='mystere-lb-nav mystere-lb-next';
      next.setAttribute('aria-label','Next photo');
      next.textContent='›';
      light.appendChild(next);
      count=document.createElement('div');
      count.className='mystere-lb-count';
      light.appendChild(count);
    }
    const show=index=>{
      current=(index+buttons.length)%buttons.length;
      const thumb=buttons[current].querySelector('img');
      img.src=thumb.currentSrc||thumb.src;
      img.alt=thumb.alt||'Mystère photo';
      count.textContent=`${current+1} of ${buttons.length}`;
    };
    buttons.forEach((button,index)=>button.addEventListener('click',()=>show(index)));
    prev.addEventListener('click',event=>{event.stopPropagation();show(current-1)});
    next.addEventListener('click',event=>{event.stopPropagation();show(current+1)});
    addEventListener('keydown',event=>{
      if(!light.classList.contains('open'))return;
      if(event.key==='ArrowLeft')show(current-1);
      if(event.key==='ArrowRight')show(current+1);
    });
    light.addEventListener('touchstart',event=>{touchX=event.changedTouches[0]?.clientX??null},{passive:true});
    light.addEventListener('touchend',event=>{
      if(touchX==null)return;
      const dx=(event.changedTouches[0]?.clientX??touchX)-touchX;
      touchX=null;
      if(Math.abs(dx)>45)show(current+(dx<0?1:-1));
    },{passive:true});
  }

  document.querySelectorAll('[data-seat-layout="mystere-theatre"]').forEach(root=>mount(root).catch(()=>{
    root.textContent='Seat guide unavailable right now. Use the live ticket map to compare sections for your date.';
  }));
  enhanceGallery();
})();

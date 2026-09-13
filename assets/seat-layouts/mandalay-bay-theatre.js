(()=>{
  async function mount(root){
    try{
      const data=await fetch(root.dataset.layoutUrl,{credentials:'same-origin'}).then(r=>{
        if(!r.ok)throw new Error(`Layout ${r.status}`);
        return r.json();
      });
      const chartSrc=data.chart_image;
      const ticket=root.dataset.ticketUrl;
      const byId=Object.fromEntries(data.zones.map(zone=>[zone.id,zone]));

      const mapShell=document.createElement('div');
      mapShell.className='mbt-map-shell';
      const map=document.createElement('div');
      map.className='mbt-seat-map';
      const chart=document.createElement('img');
      chart.src=chartSrc;
      chart.alt='Michael Jackson ONE seating chart at Mandalay Bay showing Sections 101 through 103 and 201 through 205, with 101 through 103 and 202 through 204 as the Vegas Sidekick Sweet Spot';
      map.appendChild(chart);

      data.zones.forEach(zone=>{
        zone.hitboxes.forEach((box,index)=>{
          const hit=document.createElement('button');
          hit.type='button';
          hit.className='mbt-seat-hit';
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
      popup.className='mbt-seat-popup';
      popup.setAttribute('aria-live','polite');
      popup.setAttribute('aria-atomic','true');
      const popupTag=document.createElement('span'); popupTag.className='tag';
      const popupTitle=document.createElement('strong');
      const popupCopy=document.createElement('p');
      const popupClose=document.createElement('button');
      popupClose.type='button';
      popupClose.className='mbt-seat-popup-close';
      popupClose.setAttribute('aria-label','Close seat description');
      popupClose.textContent='×';
      popup.append(popupTag,popupTitle,popupCopy,popupClose);
      map.appendChild(popup);

      const caption=document.createElement('div');
      caption.className='mbt-map-caption';
      const venue=document.createElement('strong'); venue.textContent=data.venue;
      const address=document.createElement('span'); address.textContent=data.address;
      caption.append(venue,address);
      mapShell.append(map,caption);

      const detail=document.createElement('div');
      detail.className='mbt-seat-detail';
      detail.setAttribute('aria-live','polite');
      const tag=document.createElement('span'); tag.className='tag';
      const heading=document.createElement('h3');
      const copy=document.createElement('p');
      detail.append(tag,heading,copy);

      const legend=document.createElement('div');
      legend.className='mbt-seat-legend';
      legend.innerHTML='<span><i></i><b>Sweet Spot / Our Pick:</b>&nbsp;101–103, 202–204</span><span><i></i><b>Wider side view:</b>&nbsp;201, 205</span>';

      const book=document.createElement('a');
      book.className='mbt-seat-book vs-ticket-primary';
      book.href=ticket;
      book.target='_blank';
      book.rel='noopener sponsored';
      book.textContent='Check tickets & seating →';

      const side=document.createElement('div');
      side.className='mbt-seat-side';
      side.append(detail,legend,book);
      root.replaceChildren(mapShell,side);

      function activate(id,showPopup=true){
        const zone=byId[id];
        if(!zone)return;
        const hits=[...root.querySelectorAll('.mbt-seat-hit')];
        hits.forEach(el=>{
          const selected=el.dataset.zone===id;
          el.classList.toggle('is-active',selected);
          el.setAttribute('aria-pressed',selected?'true':'false');
          if(selected&&showPopup){
            el.classList.remove('is-tapped');
            void el.offsetWidth;
            el.classList.add('is-tapped');
          }
        });
        const label=zone.our_pick?'Sweet Spot / Our Pick':zone.badge;
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
        if(event.target.closest('.mbt-seat-popup-close')){
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
      root.addEventListener('animationend',event=>{
        if(event.target.classList?.contains('mbt-seat-hit'))event.target.classList.remove('is-tapped');
      });
      activate('102',false);

      const galleryChart=document.querySelector('.mbt-chart-gallery img');
      if(galleryChart){
        galleryChart.src=chartSrc;
        galleryChart.alt='Michael Jackson ONE seating chart at Mandalay Bay showing Sections 101 through 103 and 201 through 205, with 101 through 103 and 202 through 204 as the Vegas Sidekick Sweet Spot';
      }
    }catch(error){
      root.innerHTML='<p>Seat guide unavailable right now. Use the live ticket map to compare sections for your date.</p>';
      console.warn('Michael Jackson ONE seat guide:',error);
    }
  }

  function gallery(){
    const buttons=[...document.querySelectorAll('#photos .gallery button')];
    const light=document.getElementById('lightbox');
    if(!buttons.length||!light)return;
    const img=light.querySelector('#lightboxImg, img');
    if(!img)return;
    let current=0,touchX=null;
    let prev=light.querySelector('.mbt-lb-prev');
    let next=light.querySelector('.mbt-lb-next');
    let count=light.querySelector('.mbt-lb-count');
    if(!prev){
      prev=document.createElement('button'); prev.type='button'; prev.className='mbt-lb-nav mbt-lb-prev'; prev.textContent='‹'; prev.setAttribute('aria-label','Previous photo');
      next=document.createElement('button'); next.type='button'; next.className='mbt-lb-nav mbt-lb-next'; next.textContent='›'; next.setAttribute('aria-label','Next photo');
      count=document.createElement('div'); count.className='mbt-lb-count';
      light.append(prev,next,count);
    }
    const show=index=>{
      current=(index+buttons.length)%buttons.length;
      const thumb=buttons[current].querySelector('img');
      img.src=thumb.currentSrc||thumb.src;
      img.alt=thumb.alt||'Michael Jackson ONE photo';
      count.textContent=`${current+1} of ${buttons.length}`;
    };
    buttons.forEach((button,index)=>button.addEventListener('click',()=>show(index)));
    prev.onclick=event=>{event.stopPropagation();show(current-1)};
    next.onclick=event=>{event.stopPropagation();show(current+1)};
    addEventListener('keydown',event=>{
      if(!light.classList.contains('open'))return;
      if(event.key==='ArrowLeft')show(current-1);
      if(event.key==='ArrowRight')show(current+1);
    });
    light.addEventListener('touchstart',event=>touchX=event.changedTouches[0]?.clientX??null,{passive:true});
    light.addEventListener('touchend',event=>{
      if(touchX==null)return;
      const dx=(event.changedTouches[0]?.clientX??touchX)-touchX;
      touchX=null;
      if(Math.abs(dx)>45)show(current+(dx<0?1:-1));
    },{passive:true});
  }

  const mounts=[...document.querySelectorAll('[data-seat-layout="mandalay-bay-theatre"]')].map(root=>mount(root));
  Promise.allSettled(mounts).then(gallery);
})();


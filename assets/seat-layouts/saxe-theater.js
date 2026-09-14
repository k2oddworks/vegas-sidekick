(()=>{
  let chartUrlPromise=null;

  async function getChartUrl(data){
    if(chartUrlPromise)return chartUrlPromise;
    chartUrlPromise=(async()=>{
      if(data.chart_asset_chunks?.length){
        const parts=await Promise.all(data.chart_asset_chunks.map(url=>fetch(url,{credentials:'same-origin'}).then(response=>{
          if(!response.ok)throw new Error(`Chart chunk HTTP ${response.status}`);
          return response.text();
        })));
        const b64=parts.join('').replace(/\s+/g,'');
        const raw=atob(b64);
        const bytes=new Uint8Array(raw.length);
        for(let i=0;i<raw.length;i++)bytes[i]=raw.charCodeAt(i);
        return URL.createObjectURL(new Blob([bytes],{type:'image/webp'}));
      }
      if(data.chart_asset)return data.chart_asset;
      throw new Error('No seating chart asset configured');
    })();
    return chartUrlPromise;
  }

  async function mount(root){
    const data=await fetch(root.dataset.layoutUrl,{credentials:'same-origin'}).then(r=>{if(!r.ok)throw new Error(`HTTP ${r.status}`);return r.json()});
    const chartUrl=await getChartUrl(data);
    const ticket=root.dataset.ticketUrl;

    const mapShell=document.createElement('div');
    mapShell.className='saxe-map-shell';
    const map=document.createElement('div');
    map.className='saxe-seat-map';
    const chart=document.createElement('img');
    chart.src=chartUrl;
    chart.alt='VEGAS! The Show seating chart at Saxe Theater showing Center, Side and Rear sections, with Center as the Vegas Sidekick Sweet Spot';
    map.appendChild(chart);

    data.sections.forEach(section=>{
      section.hitboxes.forEach((box,index)=>{
        const hit=document.createElement('button');
        hit.type='button';
        hit.className='saxe-seat-hit';
        hit.dataset.zone=section.id;
        hit.setAttribute('aria-label',`${section.label}${section.our_pick?', Sweet Spot / Our Pick':''}${index>0?' seating':''}`);
        hit.style.left=`${box.left}%`;
        hit.style.top=`${box.top}%`;
        hit.style.width=`${box.width}%`;
        hit.style.height=`${box.height}%`;
        hit.style.setProperty('--hit-shape',box.clip);
        map.appendChild(hit);
      });
    });


    const caption=document.createElement('div');caption.className='saxe-map-caption';
    const venue=document.createElement('strong');venue.textContent=data.venue;
    const address=document.createElement('span');address.textContent=data.address;
    caption.append(venue,address);mapShell.append(map,caption);

    const detail=document.createElement('div');detail.className='saxe-seat-detail';detail.setAttribute('aria-live','off');
    const tag=document.createElement('span');tag.className='tag';
    const heading=document.createElement('h3');
    const copy=document.createElement('p');
    detail.append(tag,heading,copy);

    const legend=document.createElement('div');legend.className='saxe-seat-legend';
    legend.innerHTML='<span><i></i><b>Sweet Spot / Our Pick:</b>&nbsp;Center</span><span><i></i><b>Angled view:</b>&nbsp;Side</span><span><i></i><b>Wider full-stage view:</b>&nbsp;Rear</span>';

    const book=document.createElement('a');book.className='saxe-seat-book vs-ticket-primary';book.href=ticket;book.target='_blank';book.rel='noopener sponsored';book.textContent='Check tickets & seating →';
    const side=document.createElement('div');side.className='saxe-seat-side';side.append(detail,legend,book);
    root.replaceChildren(mapShell,side);

    window.VSSeatInteractions.mount({
      root,controls:root.querySelectorAll('[data-zone]'),
      sections:data.sections.map(section=>({
        id:section.id,label:section.label,
        description:section.description,pick:section.our_pick,badge:section.badge
      })),
      getId:button=>button.dataset.zone,initialId:'center',
      onSelect:(section,label)=>{
        tag.textContent=label;
        heading.textContent=section.label;
        copy.textContent=section.description;
      }
    });

    const galleryChart=document.querySelector('.saxe-chart-gallery img');
    if(galleryChart){galleryChart.src=chartUrl;galleryChart.alt='VEGAS! The Show seating chart at Saxe Theater showing Center, Side and Rear sections, with Center as the Vegas Sidekick Sweet Spot'}
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
  document.querySelectorAll('[data-seat-layout="saxe-theater"]').forEach(root=>mount(root).catch(err=>{root.textContent='Seat guide unavailable right now. Use the live ticket map to compare sections for your date.';console.warn('Saxe Theater seat guide:',err)}));enhanceGallery();
})();
